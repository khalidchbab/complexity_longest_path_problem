from ortools.sat.python import cp_model

model = cp_model.CpModel()

# value achieved from combination of different moves of type A
# (moves_A (rows)) and different moves of type B (moves_B (columns))
# for e.g. 2 move of type A and 3 move of type B will give value = 2
value = [
    [-1, 5, 3, 2, 2],
    [2, 4, 2, -1, 1],
    [4, 4, 0, -1, 2],
    [5, 1, -1, 2, 2],
    [0, 0, 0, 0, 0],
    [2, 1, 1, 2, 0],
]

min_value = min([min(i) for i in value])
max_value = max([max(i) for i in value])

# 6 moves of type A
num_moves_A = len(value)

# 5 moves of type B
num_moves_B = len(value[0])

# number of positions
num_positions = 5

type_move_A_position = [
    model.NewIntVar(0, num_moves_A - 1, f"move_A[{i}]") for i in range(num_positions)
]

model.AddAllDifferent(type_move_A_position)

type_move_B_position = [
    model.NewIntVar(0, num_moves_B - 1, f"move_B[{i}]") for i in range(num_positions)
]

model.AddAllDifferent(type_move_B_position)

value_position = [
    model.NewIntVar(min_value, max_value, f"value_position[{i}]")
    for i in range(num_positions)
]

tuples_list = []
for i in range(num_moves_A):
    for j in range(num_moves_B):
        tuples_list.append((i, j, value[i][j]))

for i in range(num_positions):
    model.AddAllowedAssignments(
        [type_move_A_position[i], type_move_B_position[i], value_position[i]],
        tuples_list,
    )

model.Maximize(sum(value_position))

# Solve
solver = cp_model.CpSolver()
status = solver.Solve(model)

solver.ObjectiveValue()

for i in range(num_positions):
    print(
        str(i)
        + "--"
        + str(solver.Value(type_move_A_position[i]))
        + "--"
        + str(solver.Value(type_move_B_position[i]))
        + "--"
        + str(solver.Value(value_position[i]))
    )
