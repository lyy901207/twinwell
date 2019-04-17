
#from lib.PrioDict import priorityDictionary
import copy
#import model.node
#import model.turn
import model.lane


def generateCostMap(G, network):
    '''
    This function return costMap which should be used in astar
    :param G:
    :return:
    '''
    aMap = {}
    for neighbors in G.id.keys():
        #print(neighbors)
        aMap[neighbors] = {}
        for node in G[neighbors]:
            #print(node)
            aMap[neighbors][node] = {}
            aMap[neighbors][node]['tc'] = network.idLaneMap[neighbors][node].travelTime  # TODO: function for travel cost
            aMap[neighbors][node]['stress'] =  0.0 # TODO: Stress Map
    return aMap



def astar(G, start, end, network):
    '''
    G is a dictionary, indexed by vertices.  For any vertex v, G[v] is itself a dictionary, indexed by the neighbors
    of v.  For any edge v->w, G[v][w] is the length of the edge.
    This function applied a star algorithm to find the lowest cost path
        G[node1][node2] = {'travel-time': travel time, 'stress': stress}
        g = travel time cost
        h = mahattanDist(end) + stress
        f = g + h
    D: {node1: distance from start to node1, node2: distance from start to node2,...}
    P: {node1: parent of node1, node2: parent of node2,...}
    :param G: road graph
    :param start: start node
    :param end: end node
    :return: (D, P)
    '''

    aMap = {} # dict to store g, h, f
    P = {} # dict to store parent node
    D = {} # dict to store final cost

    start_node = start
    end_node = end
    #print(start_node, end_node)

    aMap[start_node] = {'g_cost':0.0, 'h_cost':0.0, 'f_cost':0.0}
    aMap[end_node] = {'g_cost':0.0, 'h_cost':0.0, 'f_cost':0.0}

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while open_list:
        print('Open_list is:', open_list)

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if aMap[item]['f_cost'] < aMap[current_node]['f_cost']:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        D[current_node] = aMap[current_node]['f_cost']
        # Found the goal
        if current_node == end_node:
            #break
            path = []
            current = current_node
            while current:
                print('path current is:', current)
                path.append(current)
                if current != start_node:
                    current = P[current]
                else:
                    break
            return (D, P)
            #return path[::-1] # Return reversed path

        # Generate children
        children = []
        #print('current_node is:', current_node)
        for success_node in G[current_node]:
            print('This is success_node for' , current_node, ':', success_node)
            #G[success_node]['parent'] = current_node
            # Append
            children.append(success_node)
            P[success_node] = current_node
            print('P is :', P)

        # Loop through children
        for child in children:
            print('child is:', child)

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            aMap[child] = {'g':0.0, 'h':0.0, 'f':0.0}
            aMap[child]['g_cost'] = aMap[current_node]['g_cost'] + G[current_node][child].travelTime
            #child.h = child.manhattanDist(end) + [current_node][child]
            aMap[child]['h_cost'] = network.idNodeMap[child].manhattanDist(network.idNodeMap[end_node])
            aMap[child]['f_cost'] = aMap[child]['g_cost'] + aMap[child]['h_cost']

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and aMap[child]['g_cost'] > aMap[open_node]['g_cost']:
                    continue

            # Add the child to the open list
            open_list.append(child)


def shortestPathNode(G, start, end, network):
    # revised by Gong
    # this function returns a dictionary of cost (time or distance) along the path, \
    # and a dictionary of node-pair of links in the shortest path given a graph and a pair of origin-destination.
    # these two dictionaries have the same style as Dijkstra
    #D, P = Dijkstra(G, start, end)
    D, P = astar(G, start, end, network)
    Path = []

    reach = 0
    if end in P:
        reach = 1
    else:
        reach = 0

    dic_path = {}  # {node3:node2,node2:node5,node5:node1....}
    if reach == 1:
        while 1:
            Path.append(end)
            if end == start: break
            end = P[end]
        Path.reverse()
        for i in range(0, len(Path) - 1):
            dic_path[Path[i]] = Path[i + 1]
        return D, dic_path
    else:
        return D, dic_path

def convert_ppath_to_pathids(dic_ppath, dic_graph, start, end):
    '''
    This function converts node id based shortest path output by shortestPathNode()
    Further info @ Dijkstra2
    :param dic_ppath: dic_ppath = P in shortestPathNode()
    :param dic_graph: G is the input Graph
    :param start_nodeid: start node id
    :param end_nodeid: end node id
    :return: dictionary of lane graph: {laneid1:laneid12,laneid12:laneid21,laneid21:laneid3,...}
    '''
    id1 = start
    list_laneids = []  # result in the process, list of lanes that compose the shortest path
    dic_routes = {}  # output
    # print "convert the node-pairs to list-of-lanes"
    if len(dic_ppath) > 0:
        while id1 != end:
            id2 = dic_ppath[id1]
            laneid = dic_graph[id1][id2].id
            list_laneids.append(laneid)
            id1 = copy.deepcopy(id2)
    # print "convert the list-of-lanes to dic-of-lanes"
    if len(list_laneids) > 1:
        for i in range(0, len(list_laneids) - 1):
            dic_routes[list_laneids[i]] = list_laneids[i + 1]

    # check the number of items in each dictionary and list
    # print "the number of node-pairs:", len(dic_ppath)
    # print "the number of lanes:     ", len(list_laneids)
    # print "the number of lane-pairs:", len(dic_routes)
    return dic_routes


def bestLaneBestNodeTimeCost(G, start, end, network):
    D, P = shortestPathNode(G, start, end, network)
    bestRouteLane = convert_ppath_to_pathids(P, G, start, end)
    return (bestRouteLane, P, D[end])


def main():
    '''
    G = {'s':{'u':{'travel-time':-9}, 'x':{'travel-time':5}},'v':{'y':{'travel-time':4}},
    'x':{'y':{'travel-time':-4},'s':{'travel-time':3}},'u':{'y':{'travel-time':1},'z':{'travel-time':3}}}
    D1,P1=Dijkstra(G,'x','z')
    print D1,D1['z']
    print P1
    print shortestPathNode(G,'x','u')
    '''
    # As an example of the input format, here is the graph from Cormen, Leiserson,
    #    and Rivest (Introduction to Algorithms, 1st edition), page 528:A
    G = {'s':('u', 'v'),
         'u':('y'),
         'v':('y'),
         'y':('u'),
         }

    costMap = { 's':{'u':{'tc': 10, 'stress': 1}, 'v':{'tc': 5, 'stress': 4}},
                'u':{'y':{'tc': 1, 'stress': 0}},
                'v':{'y':{'tc': 4, 'stress': 2}},
                'y':{'u':{'tc':20, 'stress': 0}}
                }

    #print(shortestPath(G, 'x', 'u'))
    # The shortest path from s to v is ['s', 'x', 'u', 'v'] and has length 9.

    # print "next example"
    # G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'s':7, 'v':6}}
    # Path = shortestPath(G,'s','v')
    # print 'The shortest path from s to v: ', Path

    # not reachable
    # print "the 3rd example"
    # G = {'s':{'u':10, 'x':5}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'v':6}}
    # Path = shortestPath(G,'y','s')
    # print 'The shortest path from y to s: ', Path

    # test for broken roads
    # G = {'s':{'u':10, 'x':5, 'p':7}, 'u':{'v':1, 'x':2}, 'v':{'y':4}, 'x':{'u':3, 'v':9, 'y':2}, 'y':{'v':6}}
    # Path = shortestPath(G,'s','v')
    # print 'The shortest path from s to v: ', Path

    #start = (0, 0)
    #end = (7, 6)

    #print(generateCostMap(G))
    aMap , P = astar(G, 's', 'y', costMap)
    print('The fist return of astar() is:', aMap)
    print('The second return of astar() is:', P)
    #path = bestLaneBestNodeTimeCost(G, 's', 'y', costMap)
    #print(path)


if __name__ == '__main__':
    main()