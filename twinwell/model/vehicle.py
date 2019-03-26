from lib.Dijkstra2 import bestLaneBestNodeTimeCost

class Vehicle(object):
    def __init__(self, id, type, driverType, maxSpeed, valueTime, probLaneChange, startTs, nodeOrigin, nodeDest, network):
        self.id = id
        self.type = type
        self.driverType = driverType
        self.maxSpeed = maxSpeed
        self.valueTime = valueTime
        self.probLaneChange = probLaneChange
        self.startTs = startTs
        self.nodeOrigin = nodeOrigin
        self.nodeDest = nodeDest
        self.delayTime = 0

        self.network = network
        self.network.registerVehicle(self)

        self.finishTs = None

        self.laneType = '0'

        # store real-time info
        self.bestLaneRoute = None
        self.currentLane = None
        self.currentLaneProgress = None # percentage on the lane
        self.timeBudget = None
        # parameters below should be calculated on every tick
        #self.timeBudget = timeBudget
        #self.expectedEndTs = expectedEndTs
        #self.listTs = listTs
        #self.tsLocationMap = tsLocationMap
        #self.tsRouteMap = tsRouteMap

    def isBegin(self, ts):
        """
        This function judge whether the simulation starts
        :param ts: current time
        :return: y/n
        """
        return ts >= self.startTs

    def isFinish(self, ts):
        """
        This function judge whether the simulation finishes
        :param ts: current time
        :return: y/n
        """
        return not not self.finishTs

    def isRunning(self, ts):
        """
        This function judge whether the vehicle is running or not
        :param ts: current time
        :return: y/n
        """
        return self.isBegin(ts) and not self.isFinish(ts)

    def __repr__(self):
        return "<" + " ".join([str(self.id), self.type, str(self.driverType), str(self.maxSpeed),
                         str(self.valueTime), str(self.probLaneChange),
                         str(self.startTs), str(self.nodeOrigin), str(self.nodeDest)]) + ">"

    def updateShortestPath(self):
        """
        This function is to update next shortest path
        :return:
        """
        startNode = self.currentLane.link.node2 if self.currentLane else self.nodeOrigin #determine node1 of next lane

       # print(self.currentLane, startNode.id, self.nodeDest.id)
        (bestLaneRoute, bestNodeMap, timeCost) = bestLaneBestNodeTimeCost(self.network.typeGraphMap[self.laneType],
                                                                          startNode.id, self.nodeDest.id)
        self.bestLaneRoute = bestLaneRoute
        self.bestNodeMap = bestNodeMap
        self.timeBudget = timeCost
        if not self.currentLane:
            self.currentLane = self.network.typeGraphMap[self.laneType][startNode.id][bestNodeMap[startNode.id]]
            self.currentLaneProgress = 0
        #print(self.bestLaneRoute, self.timeBudget, bestNodeMap, self.currentLane)

    def updateLocation(self, timeInSecond):
        """
        This function updates the location of vehicle in LANE
        :param timeInSecond
        :param delayStrategy
        :return: currentLaneProcess
        """
        remainingTime = timeInSecond

        while True:
            # if self.id == 1: print(self.currentLane, self.currentLaneProgress, self.bestLaneRoute)
            timeUseToFinishLane = 3600.0 * (
                        1.0 - self.currentLaneProgress) * self.currentLane.link.lengthInKm / self.currentLane.speed
            # if self.id == 1: print(timeUseToFinishLane)
            if self.delayingTime > 0:
                if self.delayingTime < remainingTime:
                    remainingTime -= self.delayingTime
                    self.delayingTime = 0
                else:
                    self.delayingTime -= remainingTime
                    remainingTime = 0
                    break
            else:
                if remainingTime > timeUseToFinishLane:
                    remainingTime -= timeUseToFinishLane

                    if self.currentLane.link.node2 == self.nodeDest:
                        # finish
                        self.finishTs = self.network.ts
                        self.currentLane = None
                        self.currentLaneProgress = None
                        print(self, "finished at", self.finishTs)
                        return
                    else:
                        self.delayingTime = 5
                        self.updateShortestPath()
                        self.currentLane = self.network.typeGraphMap[self.laneType][self.currentLane.link.node2.id][
                            self.bestNodeMap[self.currentLane.link.node2.id]]
                        self.currentLaneProgress = 0.0
                else:
                    break
        #update location
        self.currentLaneProgress += (self.currentLane.speed * remainingTime) / self.currentLane.link.lengthInKm / 3600.0

    def updateDelay(self, delayStrategy, timeInSecond, aver_delay=0.05, delay_at_least=0, delay_at_most=3,
                          effect_distance=50):
        """
        ## TODO
        # this function is used to update the delay at each node (intersection) if a strategy of dynamic delay is selected.
        # delay is a feature of a node and it is updated due to different delay strategy.
        # if a delay at a node is necessary in the algorithm, just visit the feature of delay at a node.
        # a defect of using this function is updating and calculating the delay at each simulation step
        :param timeInSecond: current time
        :param aver_delay:
        :param delay_at_least:
        :param delay_at_most:
        :param effect_distance:
        :return:
        """
        pre_timestamp = get_Pre_Timestamp(curr_timestamp, timestep)
        for node_id in dic_nodes:
            if delayStrategy == "vol-simple":
                delay = delay_by_Vol_Simple(node_id, pre_timestamp, aver_delay)
            elif delayStrategy == "vol-dist":
                delay = delay_by_Vol_in_a_Dist(node_id, pre_timestamp, delay_at_least, delay_at_most, effect_distance)
            elif strategy == "random":
                delay = delay_by_Random(delay_at_least, delay_at_most)
            idNodeMap[node.id]['delay'] = delay
        return