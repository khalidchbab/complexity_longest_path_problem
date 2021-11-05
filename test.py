from main_copy import read_data


n,data,edges = read_data("agraph",'r+')

print((2,3) in edges)
print((3,4) in edges)
print((4,8) in edges)
print((8,0) in edges)
print((0,14) in edges)
print((14,12) in edges)
print((12,13) in edges)
print((13,6) in edges)
print((6,7) in edges)
