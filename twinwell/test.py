from util.readNetwork import *
from util.readOd import *
from model.network import Network
from model.turn import *
from lib.astar import *

startTs = datetime.datetime(2019, 1, 1, 7, 0, 0)
totalSteps = 20 #2000
timeStep = 1

jamDensity = 124
medianValueTime = 50
random.seed(10)

vehicleId = 0

network = Network(startTs)

fNode = open("C:/Users/lyy90/OneDrive/Documents/GitHub/twinwell/twinwell/Sioux Falls network/nodes-SiouxFalls_gong.csv")
fNode.readline()
fLane = open("C:/Users/lyy90/OneDrive/Documents/GitHub/twinwell/twinwell/Sioux Falls network/lanes-SiouxFalls_gong.csv")
fLane.readline()
pOd = "C:/Users/lyy90/OneDrive/Documents/GitHub/twinwell/twinwell/OD_data_test"

readNodes(fNode, network)
readLanes(fLane, network)
tsPairNodePairTypeMap = readOd(pOd)
genVehicle(tsPairNodePairTypeMap, "random", vehicleId, medianValueTime, network)
#genVehicle(tsPairNodePairTypeMap, "uniform", vehicleId, medianValueTime, network)
t = sorted([vehicle.startTs for vehicle in network.idVehicleMap.values()])


for vid in network.idVehicleMap:
    print(network.idVehicleMap[vid])

networks = [network]

#turn = turnGen(network)
#sMap = stressMap(turn)
#print(sMap)

for i in range(totalSteps):
    #print(i)
    network = networks[-1] # current network

    print(network.ts)

    # update best route
    for vid in network.idVehicleMap:
        vehicle = network.idVehicleMap[vid]
        if not vehicle.isRunning(network.ts): continue

        # TODO: updating


        # TODO: add new searching algorithm
        vehicle.updateShortestPath()

    # update lane features
    network.updateLanes()

    # update vehicle location
    for vehicle in network.idVehicleMap.values():
        if not vehicle.isRunning(network.ts): continue
        vehicle.updateLocation(1) #update for 1 SECOND!

    # decision

    print(network.runningVehicleCount(), 'running')
    print(network.finishVehicleCount(), 'finished')

    # copy network to i+1
    network_next = copy.deepcopy(network)
    network_next.ts += datetime.timedelta(seconds=1)
    networks.append(network_next)

