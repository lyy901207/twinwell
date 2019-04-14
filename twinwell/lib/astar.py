
#from lib.PrioDict import priorityDictionary
import copy
#import model.node

def graphStress1(G_time, G_stress, start, end):
    # this function improve the graph of G_stress (based on turnings) as this graph does not include the origin and destination
    # start is the start node and origin is a virtual point connecting to start node virtually.
    # end is the end node and destination is a virtual point connecting to end node virtually.
    # this function includes the origin and destination into the graph with stress of 0.
    # origin point is noted as O and destination point is noted as D
    # G_time is in the following format:   {node1:{node2:{'travel-time':time1,'speed':speed1,...},node3:{'travel-time':time2,'speed':speed2,...}},node3:{},node4:{}.......}
    # G_stress is in the following format: {node1:{node2:{node0:stress1,node00:stress1,...},node3:{...}...},node3:{}....}, \
    # \ which means a turning from link01(from node0 to node1) to link12(from node1 to node2)

    # put O and virtual link from O to start into the graph of G_stress
    if start not in G_time:
        print(ERROR: no
        link
        starting
        from the node
        of
        ", start)
        else:
        for node2 in G_time[start]:
            if
        start in G_stress:
        if node2 in G_stress[start]:
            G_stress[start][node2]['O'] = 0
        else:
            G_stress[start][node2] = {}
        G_stress[start][node2]['O'] = 0
        else:
        G_stress[start] = {}
        G_stress[start][node2] = {}
        G_stress[start][node2]['O'] = 0

        # put D and virtual link from end to D into the graph of G_stress
        # actually the following part will not be used in the route searching
        count_end = 0  # for counting when the end-node of a link is the given end
        for node1 in G_time:
            if
        end in G_time[node1]:  # end--node2
        count_end += 1
        if end in G_stress:
            G_stress[end]['D'] = {}
        G_stress[end]['D'][node1] = 0
        else:
        G_stress[end] = {}
        G_stress[end]['D'] = {}
        G_stress[end]['D'][node1] = 0
        if count_end >= 1:
            return G_stress
        else:
            print("ERROR: no links ending at the node of", end)

def generateCostMap(G):
    '''
    This function return costMap which should be used in astar
    :param G:
    :return:
    '''
    aMap = {}
    for neighbors in G.keys():
        #print(neighbors)
        aMap[neighbors] = {}
        for node in G[neighbors]:
            #print(node)
            aMap[neighbors][node] = {}
            aMap[neighbors][node]['tc'] = G[neighbors][node].travelTime  # TODO: function for travel cost
            aMap[neighbors][node]['stress'] =  0.0 # TODO: Stress Map
    return aMap



def astar(G, start, end, costMap):
    '''
    This function applied a star algorithm to find the lowest cost path
        G[node1][node2] = {'travel-time': travel time, 'stress': stress}
        g = travel time cost
        h = mahattanDist(end) + stress
        f = g + h
    :param G: road graph
    :param start: start node
    :param end: end node
    :param costMap: cost for node1 to node2
    :return: return the list of node for lowest cost path
    '''

    aMap = {} # dict to store g, h, f
    P = {} # dict to store parent node

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
            return path[::-1] # Return reversed path

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
            #print('child is:', child)

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            aMap[child] = {'g':0.0, 'h':0.0, 'f':0.0}
            aMap[child]['g_cost'] = aMap[current_node]['g_cost'] + costMap[current_node][child]['tc']
            #child.h = child.manhattanDist(end) + [current_node][child]
            aMap[child]['h_cost'] = costMap[current_node][child]['stress']
            aMap[child]['f_cost'] = aMap[child]['g_cost'] + aMap[child]['h_cost']

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and aMap[child]['g_cost'] > aMap[open_node]['g_cost']:
                    continue

            # Add the child to the open list
            open_list.append(child)


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

    print(generateCostMap(G))
    path = astar(G, 's', 'y', costMap)
    #print(path)


if __name__ == '__main__':
    main()