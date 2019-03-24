from util.readNetwork import *
from util.readOd import *
from model.network import Network
startTs = datetime.datetime(2019, 1, 1, 7, 0, 0)
totalSteps = 5 #2000
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
pOd = "C:/Users/lyy90/OneDrive/Documents/GitHub/twinwell/twinwell/OD_data"

readNodes(fNode, network)
readLanes(fLane, network)
tsPairNodePairTypeMap = readOd(pOd)
genVehicle(tsPairNodePairTypeMap, "random", vehicleId, medianValueTime, network)
#genVehicle(tsPairNodePairTypeMap, "uniform", vehicleId, medianValueTime, network)
t = sorted([vehicle.startTs for vehicle in network.idVehicleMap.values()])
print(len(t))


