from util.readNetwork import *
from util.readOd import *
from model.network import Network
from model.turn import *
from lib.astar import *


# set the location of the output results

#for checking the simulation logs
#outfile = open(r"C:\Users\lyy90\OneDrive\Documents\GitHub\twinwell\twinwell\outfile_process_during_simulation.csv","ab")
#writer_log = csv.writer(outfile)

#for storing the status of lanes and vehicles
#outfile_lane_features = open(r'C:\Users\lyy90\OneDrive\Documents\GitHub\twinwell\twinwell\outfile_lane_features.csv',"ab")
#writer_lane_features = csv.writer(outfile_lane_features)

#outfile_veh_features = open(r'C:\Users\lyy90\OneDrive\Documents\GitHub\twinwell\twinwell\outfile_veh_features.csv',"ab")
#writer_veh_features = csv.writer(outfile_veh_features)

#outfile_OD_features = open(r'C:\Users\lyy90\OneDrive\Documents\GitHub\twinwell\twinwell\outfile_OD_features.csv',"ab")
#writer_OD_features = csv.writer(outfile_OD_features)

#outfile_statistic1 = open(r'C:\Users\lyy90\OneDrive\Documents\GitHub\twinwell\twinwell\outfile_statistics_along_timestamps.csv',"ab")
#writer_statistic_along_timestamps = csv.writer(outfile_statistic1)

outfile_statistic2 = open(r'C:\Users\lyy90\OneDrive\Documents\GitHub\twinwell\twinwell\outfile_statistics_whole_simulation.csv',"ab")
#writer_statistic_whole_simulation = csv.writer(outfile_statistic2)


startTs = datetime.datetime(2019, 1, 1, 7, 0, 0)
totalSteps = 20 #2000
timeStep = 1

jamDensity = 124
medianValueTime = 50
random.seed(10)

#writer_log.writerow('This simulation is for:', 'delay type:', delayingType, 'vehicle generation:', genVehicle)

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
    print('This is step:', i, 'in', totalSteps)

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

