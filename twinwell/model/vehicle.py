#from lib.Dijkstra2 import bestLaneBestNodeTimeCost
from lib.astar import bestLaneBestNodeTimeCost

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
        self.delayingTime = 0

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
                                                                          startNode.id, self.nodeDest.id, self.network)
        self.bestLaneRoute = bestLaneRoute
        self.bestNodeMap = bestNodeMap
        self.timeBudget = timeCost
        if not self.currentLane:
            self.currentLane = self.network.typeGraphMap[self.laneType][startNode.id][bestNodeMap[startNode.id]]
            self.currentLaneProgress = 0
        #print(self.bestLaneRoute, self.timeBudget, bestNodeMap, self.currentLane)

    def updateLocation(self, timeInSecond, delayType='fix'):
        """
        This function updates the location of vehicle in LANE
        :param timeInSecond
        :return: currentLaneProcess
        """
        remainingTime = timeInSecond

        while True:
            # if self.id == 1: print(self.currentLane, self.currentLaneProgress, self.bestLaneRoute)
            timeUseToFinishLane = 3600.0 * (
                        1.0 - self.currentLaneProgress) * self.currentLane.link.lengthInKm / self.currentLane.speed
            # if self.id == 1: print(timeUseToFinishLane)
            # if delay in node, updating time as below
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
                        #self.delayingTime = 5 # currently the delaying time is fix, later it may be change
                        # There are 4 types of delay strategy
                        self.delayingTime = self.currentLane.delayCalculation(delayType)
                        self.updateShortestPath()
                        self.currentLane = self.network.typeGraphMap[self.laneType][self.currentLane.link.node2.id][
                            self.bestNodeMap[self.currentLane.link.node2.id]]
                        self.currentLaneProgress = 0.0
                else:
                    break
        #update location
        self.currentLaneProgress += (self.currentLane.speed * remainingTime) / self.currentLane.link.lengthInKm / 3600.0
