import pandas as pd
from ortools.sat.python import cp_model
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from itertools import chain

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
                edges.append((src,dest,weight))
                edges.append((dest,src,weight))
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

def objectif_func(list,weights):
    tmp = []
    for i in range(len(list)-1):
        t = list[i]
        t_1 = list[i+1]
        print(t)
        tmp.append(weights[t][t_1])
    return sum(tmp)

def main():
    model = cp_model.CpModel()

    n,data,edges = read_data("graph",'r+')
    print(edges)
    data_flat = list(chain.from_iterable(data))
    min_w = min(data_flat)
    max_w = max(data_flat)
    vars = []
    weights = []

    for i in range(n):
        vars.append(model.NewIntVar( 0, n-1, "a"+str(i)))
    model.AddAllDifferent(vars)
    for i in range(n-1):
        weights.append(model.NewIntVar(min_w,max_w,"w"+str(1)))
    model.AddAllDifferent(weights)
    for i in range(n-1):
        model.AddAllowedAssignments( (vars[i],vars[i+1],weights[i]), edges)

    model.Maximize(sum(weights))

    # model.Maximize(objectif_func(vars,data))
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    s = 0
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for w in weights:
            s = s + solver.Value(w)
        print(s)
    else:
        print('No solution found.')

    solver.ObjectiveValue()
    for i in range(n):
        if i < n-1:
            print(solver.Value(vars[i]),"-",solver.Value(weights[i]),"->",end=" ")
        else :
            print(solver.Value(vars[i]))

    print('\n')
    s = 0
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for w in weights:
            s = s + solver.Value(w)
        print(s)
    else:
        print('No solution found.')

if __name__ == '__main__':
    main()