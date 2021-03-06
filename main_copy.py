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

def search(n,d,t,solutions,file):
    if n < 2:
        return solutions
    print(n)
    model = cp_model.CpModel()

    n_n,data,edges = read_data(file,'r+')
    data_flat = list(chain.from_iterable(data))
    min_w = min(data_flat)
    max_w = max(data_flat)
    vars = []
    weights = []
    vars.append(model.NewIntVar(d,d,"s"))
    for i in range(n-2):
        vars.append(model.NewIntVar( 0, n-1, "a"+str(i)))
    vars.append(model.NewIntVar(t,t,"t"))
    model.AddAllDifferent(vars)
    for i in range(n-1):
        weights.append(model.NewIntVar(min_w,max_w,"w"+str(1)))
    model.AddAllDifferent(weights)
    for i in range(n-1):
        model.AddAllowedAssignments( (vars[i],vars[i+1],weights[i]), edges)
    model.Maximize(sum(weights))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    rr = solver.ObjectiveValue()
    s = 0
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for w in weights:
            s = s + solver.Value(w)
        solutions.append(([solver.Value(vars[i]) for i in range(n)],[solver.Value(weights[i]) for i in range(n-1)],s))
        if n < 2:
            return solutions
        else :
            return search(n-1,d,t,solutions,file)
    else:
        if n < 2:
            return solutions
        else :
            return search(n-1,d,t,solutions,file)
    print('\n')

def find_solution(solutions):
    m = 0
    path_f = []
    weight_f = []
    for path,weight,w in solutions:
        if w > m:
            m = w
            path_f = path
            weight_f = weight
    return path_f,weight_f,m

def print_result(path,weights,w):
    print(f"the weight of the path is : {w} and it's degree is : {len(path)}")
    for i in range(len(path)-1):
        print(f"{path[i]} --({weights[i]})-->",end=" ")
    print(path[-1])

def main(d,t,file):
    solutions = []
    n,data,edges = read_data(file,'r+')
    solutions = search(n,d,t,solutions,file)
    path,weights,w = find_solution(solutions)
    print_result(path,weights,w)

if __name__ == '__main__':
    main(0,2,"graph4")