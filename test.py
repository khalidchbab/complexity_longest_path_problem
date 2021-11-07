from os import read


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

n,g,edg = read_data("graph","r+")

# print((4,13)," ",(4,13) in edg)
# print((13,14)," ",(13,14) in edg)
# print((14,3)," ",(14,3) in edg)
# print((3,9)," ",(3,9) in edg)
# print((9,10)," ",(9,10) in edg)
# print((10,0)," ",(10,0) in edg)
# print((0,1)," ",(0,1) in edg)
# print((1,2)," ",(1,2) in edg)
# print((2,5)," ",(2,5) in edg)
# print((5,6)," ",(5,6) in edg)
# print((6,7)," ",(6,7) in edg)
# print((7,8)," ",(7,8) in edg)
# print((8,11)," ",(8,11)in edg)
# print((11,12),(11,12) in edg)
print(n)