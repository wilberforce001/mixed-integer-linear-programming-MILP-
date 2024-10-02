import pulp as plp

# Initialization of the model
model = plp.LpProblem("Production_Scheduling_Optimization", plp.LpMinimize)

# Time periods (months)
months = [1, 2, 3, 4]

# Demand for bands and coils (in tons)
demand_bands = [3000, 6000, 4000, 2000]
demand_coils = [1000, 2500, 2500, 3000]

# Resources available each month
labor_available = [8000, 7000, 6000, 9000]
machine_available = [4000, 5000, 6000, 9000]
steel_available = [4000, 4000, 5000, 5000]

# Production costs, backlog costs, and inventory costs
prod_cost_bands = [10, 9, 10, 9]
prod_cost_coils = [11, 12, 11, 12]
backlog_cost_bands = [10, 10, 11, 15]
backlog_cost_coils = [10, 9, 10, 14]
inventory_cost_bands = [2.5, 2, 3, 2]
inventory_cost_coils = [3, 3, 2, 3]

# Decision variables: production, inventory, and backlog
P_bands = plp.LpVariable.dicts("P_bands", months, lowBound=0)
P_coils = plp.LpVariable.dicts("P_coils", months, lowBound=0)
I_bands = plp.LpVariable.dicts("I_bands", months, lowBound=0)
I_coils = plp.LpVariable.dicts("I_coils", months, lowBound=0)
B_bands = plp.LpVariable.dicts("B_bands", months, lowBound=0)
B_coils = plp.LpVariable.dicts("B_coils", months, lowBound=0)

# Objective function: minimize total production, inventory, and backlog costs
model += plp.lpSum([
    prod_cost_bands[m-1] * P_bands[m] + prod_cost_coils[m-1] * P_coils[m]
    + inventory_cost_bands[m-1] * I_bands[m] + inventory_cost_coils[m-1] * I_coils[m]
    + backlog_cost_bands[m-1] * B_bands[m] + backlog_cost_coils[m-1] * B_coils[m]
    for m in months
])

# Constraints: demand satisfaction, resource availability, ending conditions
for m in months:
    # Demand satisfaction
    if m == 1:
        model += P_bands[m] - I_bands[m] + B_bands[m] == demand_bands[m-1]
        model += P_coils[m] - I_coils[m] + B_coils[m] == demand_coils[m-1]
    else:
        model += P_bands[m] + I_bands[m-1] - I_bands[m] + B_bands[m-1] - B_bands[m] == demand_bands[m-1]
        model += P_coils[m] + I_coils[m-1] - I_coils[m] + B_coils[m-1] - B_coils[m] == demand_coils[m-1]
    
    # Resource availability
    model += 1 * P_bands[m] + 1.5 * P_coils[m] <= labor_available[m-1]
    model += 0.5 * P_bands[m] + 1 * P_coils[m] <= machine_available[m-1]
    model += 0.5 * P_bands[m] + 0.5 * P_coils[m] <= steel_available[m-1]

# Target ending inventory and backlog limits
model += I_bands[4] >= 200
model += I_coils[4] >= 200
for m in months:
    model += B_bands[m] <= 1000
    model += B_coils[m] <= 1000

# Solve the model
model.solve()

# Print the results
for m in months:
    print(f"Month {m}:")
    print(f"  Bands produced: {P_bands[m].varValue} tons")
    print(f"  Coils produced: {P_coils[m].varValue} tons")
    print(f"  Bands inventory: {I_bands[m].varValue} tons")
    print(f"  Coils inventory: {I_coils[m].varValue} tons")
    print(f"  Bands backlog: {B_bands[m].varValue} tons")
    print(f"  Coils backlog: {B_coils[m].varValue} tons")