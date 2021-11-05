import pandas as pd
from ortools.sat.python import cp_model
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# class Edge:
#     def __init__(self, weight, neighbourId):
#         self.w = weight
#         self.n = neighbourId

# class Node:
#     def __init__(self, nodeId, edges):
#         self.neighbours = edges
#         self.id = nodeId


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
def main():
    model = cp_model.CpModel()
    num_vals = 2

    n,data,edges = read_data("agraph",'r+')
    # print("   0 \t 1\t 2\t 3\t 4\t 5\t 6\t 7\t 8\t 9\t 10\t 11\t 12\t 13 \t 14\t")
    # print("------------------------------------------------------------------------------------------------------------------------------------------")
    # for i in range(len(data)):
    #     print(i,end="  ")
    #     for j in range(len(data[i])):
    #         print(data[i][j],end="\t")
    #     print(" ]")

    vars = []
    for i in range(n):
        vars.append(model.NewIntVar( 0, n-1, "a"+str(i)))

    for i in range(n):
        if i != n-1:
            model.AddAllowedAssignments( (vars[i],vars[i+1]), edges)

    model.AddAllDifferent(vars)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    print( "Status:", status )

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for v in vars:
            print(v,' = %i' % solver.Value(v))
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()