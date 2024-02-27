from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver("SAT")

verts = [0,1,2] #side view, top to bottom 0-2
hors = [0,1,2]# back view, left to right 0-2
depth = [0,1,2,3,4,5,6] # side view and top view, left to right. 0-6

x = [[[solver.BoolVar("x"+str(d)+str(h)+str(v)) for v in verts] for h in hors] for d in depth]

side_constraints = [[1,1,1,1,1,1,1],[1,1,1,1,1,1,0],[1,1,1,1,0,0,0]]
back_constraints = [[1,1,1] for i in range(3)] # all 1s
top_constraints = [[1,1,1] for i in range(7)]  # all 1s

for v in verts:
    for d in depth:
        solver.Add(solver.Sum([x[d][h][v] for h in hors]) >= side_constraints[v][d])

for v in verts:
    for h in hors:
        solver.Add(solver.Sum([x[d][h][v] for d in depth]) >= back_constraints[v][h])

for d in depth:
    for h in hors:
        solver.Add(solver.Sum([x[d][h][v] for v in verts]) >= top_constraints[d][h])

# gravity
for d in depth:
    for h in hors:
        for v in [0,1]:
            solver.Add(x[d][h][v] >= x[d][h][v+1])

print("Number of constraints =", solver.NumConstraints())

solver.Minimize(solver.Sum(x[d][h][v] for d in depth for h in hors for v in verts))

print(f"Solving with {solver.SolverVersion()}")
status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print("Solution:")
    print(f"Objective value = {solver.Objective().Value():0.1f}")
    
    for d in depth:
        for h in hors:
            for v in verts:
                print(f"{x[d][h][v].name} = {x[d][h][v].solution_value():0.1f}")
else:
    print("The problem does not have an optimal solution.")