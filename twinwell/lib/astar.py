
#from lib.PrioDict import priorityDictionary
import copy
#import model.node
def stress(node):
    pass


def astar(G, start, end, costMap):
    """Returns a list of tuples as a path from the given start to the given end in the given graph
    G[node1][node2] = {'travel-time': travel time, 'stress': stress}
    g = travel time cost
    h = mahattanDist(end) + stress
    f = g + h
    """

    # Create start and end node
    #print(G)
    aMap = {}
    P = {}

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
        #print(open_list)

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
        if current_node == end:
            path = []
            current = current_node
            while current:
                path.append(current)
                current = P[current]
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        #print('current_node is:', current_node)
        for success_node in G[current_node]:
            #print('This is success_node for' , current_node, ':', success_node)
            #G[success_node]['parent'] = current_node
            # Append
            children.append(success_node)
            P[success_node] = current_node

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
    return path


def main():


    '''
    G = {'s':{'u':{'travel-time':-9}, 'x':{'travel-time':5}},'v':{'y':{'travel-time':4}},'x':{'y':{'travel-time':-4},'s':{'travel-time':3}},'u':{'y':{'travel-time':1},'z':{'travel-time':3}}}
    D1,P1=Dijkstra(G,'x','z')
    print D1,D1['z']
    print P1
    print shortestPathNode(G,'x','u')
    '''
    # As an example of the input format, here is the graph from Cormen, Leiserson,
    #    and Rivest (Introduction to Algorithms, 1st edition), page 528:
    G = {'s':('u', 'x'), 
         'u':('v', 'x'),
         'v':('y'), 
         'x':('u', 'v', 'y'),
         'y':('s', 'v')
         }

    costMap = { 's':{'u':{'tc': 10, 'stress': 0},'x': {'tc': 5, 'stress': 0}}, 
                'u':{'v':{'tc': 1, 'stress': 0}, 'x':{'tc': 2, 'stress': 0}},
                'v':{'y':{'tc': 4, 'stress': 0}}, 
                'x':{'u':{'tc': 3, 'stress': 0}, 'v':{'tc': 9, 'stress': 0}, 'y': {'tc': 2, 'stress': 0}},
                'y':{'s':{'tc': 7, 'stress': 0}, 'v': {'tc': 6, 'stress': 0}}
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

    path = astar(G, 's', 'u', costMap)
    print(path)


if __name__ == '__main__':
    main()