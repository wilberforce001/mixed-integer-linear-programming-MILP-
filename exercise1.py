import pulp as plp

# Define the problem
problem = plp.LpProblem("Department_Location_Problem", plp.LpMaximize)

# Definition of the cities and departments
cities = ['Bristol', 'Brighton', 'London']
departments = ['A', 'B', 'C', 'D', 'E']

# A definition of the benefits associated with each department 
benefits = {
    'A': {'London': 0, 'Bristol': 10, 'Brighton': 10},
    'B': {'London': 0, 'Bristol': 15, 'Brighton': 20},
    'C': {'London': 0, 'Bristol': 10, 'Brighton': 15},
    'D': {'London': 0, 'Bristol': 20, 'Brighton': 15},
    'E': {'London': 0, 'Bristol': 5, 'Brighton': 15},
}

# Communication costs and requirements between departments 
Cik = {
    ('A', 'B'): 0.0, ('A', 'C'): 1.0, ('A', 'D'): 1.5, ('A', 'E'): 0.0,
    ('B', 'C'): 1.4, ('B', 'D'): 1.2, ('B', 'E'): 0.0,
    ('C', 'D'): 0.0, ('C', 'E'): 2.0,
    ('D', 'E'): 0.7,
}

# Cost per unit of communication between locations (in pounds)
Djl = {
    ('London', 'London'): 10, ('London', 'Bristol'): 13, ('London', 'Brighton'): 9,
    ('Bristol', 'London'): 13, ('Bristol', 'Bristol'): 5, ('Bristol', 'Brighton'): 14,
    ('Brighton', 'London'): 9, ('Brighton', 'Bristol'): 14, ('Brighton', 'Brighton'): 5,
}

# Creation of decision variables for the optimization model and the 
# location of each deapartment in a city
locate = plp.LpVariable.dicts("Locate", ((d, l) for d in departments for l in cities), 
                              cat="Binary")

# Communication decision variables between departments (linearized)
comm_locate = plp.LpVariable.dicts(
    "CommLocate", ((i, k, j, l) for (i, k) in Cik.keys() for j in cities for l in cities), 
    lowBound=0, cat="Continuous"
)

# Objective: Maximize the total benefit minus communication costs
problem += (
    plp.lpSum(benefits[d][l] * locate[(d, l)] for d in departments for l in cities) 
    - plp.lpSum(Cik[(i, k)] * Djl[(j, l)] * comm_locate[(i, k, j, l)]
                for i, k in Cik.keys() for j in cities for l in cities)
)

# Constraints: Each department must be in one location
for d in departments:
    problem += plp.lpSum(locate[(d, l)] for l in cities) == 1

# Constraints: No more than 3 departments in any city
for l in cities:
    problem += plp.lpSum(locate[(d, l)] for d in departments) <= 3

# Communication constraints: Ensure comm_locate variables match the decision to place departments
for (i, k) in Cik.keys():
    for j in cities:
        for l in cities:
            # The communication between departments can only occur if they are located in those cities
            problem += comm_locate[(i, k, j, l)] <= locate[(i, j)]
            problem += comm_locate[(i, k, j, l)] <= locate[(k, l)]
            # This ensures that if department i is located in city j and department k in city l,
            # only then will there be a communication cost between them.

# Solve the problem
problem.solve()

# Display the results
print(f"Status: {plp.LpStatus[problem.status]}")
for d in departments:
    for l in cities:
        if plp.value(locate[(d, l)]) == 1:
            print(f"Department {d} should be located in {l}")

# Objective value
print(f"Total benefit (minus communication costs): £{plp.value(problem.objective)} thousand per year")
