import pandas as pd
from ortools.sat.python import cp_model
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

class Edge:
    def __init__(self, weight, neighbourId):
        self.w = weight
        self.n = neighbourId

class Node:
    def __init__(self, nodeId, edges):
        self.neighbours = edges
        self.id = nodeId


def read_data(filePath, mode):
    numNodes = 0
    file = open(filePath, mode)
    line = file.readline().strip()
    numNodes = int(line)
    graph = [ [0]*numNodes for i in range(numNodes)]
    edges = []
    # Last line is an empty string.
    while line != ['']:
         line = file.readline().strip().split(" ")
         try:
            src = int(line[0])
            dest = int(line[1])
            weight = int(line[2])
            if graph[src][dest] == 0 and graph[dest][src] == 0:
                graph[src][dest] = weight
                graph[dest][src] = weight
                edges.append((src,dest))
         except ValueError:
            # Last line.
            break
    return (numNodes, graph,edges)

def create_data_model():
    data = {}
    n,graph,edges = read_data("agraph",'r+')
    data['distance_matrix'] = graph
    data['num_vehicles'] = 1
    data['depot'] = 0
    print("   0 \t 1\t 2\t 3\t 4\t 5\t 6\t 7\t 8\t 9\t 10\t 11\t 12\t 13 \t 14\t")
    print("------------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(len(graph)):
        print(i,end="  ")
        for j in range(len(graph[i])):
            print(graph[i][j],end="\t")
        print(" ]")
    return n,data,edges

model = cp_model.CpModel()
num_vals = 2

# def print_solution(manager, routing, solution):
#     """Prints solution on console."""
#     print('Objective: {} miles'.format(solution.ObjectiveValue()))
#     index = routing.Start(0)
#     plan_output = 'Route for vehicle 0:\n'
#     route_distance = 0
#     while not routing.IsEnd(index):
#         plan_output += ' {} ->'.format(manager.IndexToNode(index))
#         previous_index = index
#         index = solution.Value(routing.NextVar(index))
#         route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
#     plan_output += ' {}\n'.format(manager.IndexToNode(index))
#     print(plan_output)
#     plan_output += 'Route distance: {}miles\n'.format(route_distance)

# def main():
#     """Entry point of the program."""
#     # Instantiate the data problem.
#     n,data,edges = create_data_model()
#     reversedEdges = [ (x,y) for (y,x) in edges ]
#     # Create the routing index manager.
#     manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
#                                            data['num_vehicles'], data['depot'])

#     # Create Routing Model.
#     routing = pywrapcp.RoutingModel(manager)
#     # routing.add


#     def distance_callback(from_index, to_index):
#         """Returns the distance between the two nodes."""
#         # Convert from routing variable Index to distance matrix NodeIndex.
#         from_node = manager.IndexToNode(from_index)
#         to_node = manager.IndexToNode(to_index)
#         return data['distance_matrix'][from_node][to_node]

#     transit_callback_index = routing.RegisterTransitCallback(distance_callback)

#     # Define cost of each arc.
#     routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

#     # Setting first solution heuristic.
#     search_parameters = pywrapcp.DefaultRoutingSearchParameters()
#     search_parameters.first_solution_strategy = (
#         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

#     # Solve the problem.
#     solution = routing.SolveWithParameters(search_parameters)

#     # Print solution on console.
#     if solution:
#         print_solution(manager, routing, solution)
#     else:
#         print("no solution")


if __name__ == '__main__':
    main()
