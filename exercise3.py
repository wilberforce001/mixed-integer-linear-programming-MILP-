from ortools.sat.python import cp_model

# Activity definition for different computer models
activities = {
    "Model A": [
        {"label": "InstallCPU", "duration": 8, "resource": "CPUInstaller", "precedents": []},
        {"label": "InstallDisk", "duration": 5, "resource": "DriveInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallOptDevice", "duration": 4, "resource": "DriveInstaller", "precedents": ["InstallDisk"]},
        {"label": "InstallGPU", "duration": 4, "resource": "CardInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallBluetooth", "duration": 5, "resource": "CommInstaller", "precedents": ["InstallGPU", "InstallOptDevice"]},
        {"label": "Test", "duration": 10, "resource": "Tester", "precedents": ["InstallBluetooth"]},
        {"label": "Pack", "duration": 5, "resource": "Packer", "precedents": ["Test"]}
    ],
    "Model B": [
        {"label": "InstallCPU", "duration": 9, "resource": "CPUInstaller", "precedents": []},
        {"label": "InstallDisk", "duration": 6, "resource": "DriveInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallOptDevice", "duration": 5, "resource": "DriveInstaller", "precedents": ["InstallDisk"]},
        {"label": "InstallGPU", "duration": 6, "resource": "CardInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallBluetooth", "duration": 6, "resource": "CommInstaller", "precedents": ["InstallGPU", "InstallOptDevice"]},
        {"label": "Test", "duration": 12, "resource": "Tester", "precedents": ["InstallBluetooth"]},
        {"label": "Pack", "duration": 6, "resource": "Packer", "precedents": ["Test"]}
    ],
    "Model C": [
        {"label": "InstallCPU", "duration": 7, "resource": "CPUInstaller", "precedents": []},
        {"label": "InstallDisk", "duration": 6, "resource": "DriveInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallOptDevice", "duration": 4, "resource": "DriveInstaller", "precedents": ["InstallDisk"]},
        {"label": "InstallGPU", "duration": 5, "resource": "CardInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallBluetooth", "duration": 4, "resource": "CommInstaller", "precedents": ["InstallGPU", "InstallOptDevice"]},
        {"label": "Test", "duration": 8, "resource": "Tester", "precedents": ["InstallBluetooth"]},
        {"label": "Pack", "duration": 5, "resource": "Packer", "precedents": ["Test"]}
    ],
    "Model D": [
        {"label": "InstallCPU", "duration": 8, "resource": "CPUInstaller", "precedents": []},
        {"label": "InstallDisk", "duration": 5, "resource": "DriveInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallOptDevice", "duration": 3, "resource": "DriveInstaller", "precedents": ["InstallDisk"]},
        {"label": "InstallGPU", "duration": 6, "resource": "CardInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallBluetooth", "duration": 7, "resource": "CommInstaller", "precedents": ["InstallGPU", "InstallOptDevice"]},
        {"label": "Test", "duration": 10, "resource": "Tester", "precedents": ["InstallBluetooth"]},
        {"label": "Pack", "duration": 5, "resource": "Packer", "precedents": ["Test"]}
    ],
    "Model E": [
        {"label": "InstallCPU", "duration": 9, "resource": "CPUInstaller", "precedents": []},
        {"label": "InstallDisk", "duration": 5, "resource": "DriveInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallOptDevice", "duration": 5, "resource": "DriveInstaller", "precedents": ["InstallDisk"]},
        {"label": "InstallGPU", "duration": 4, "resource": "CardInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallBluetooth", "duration": 5, "resource": "CommInstaller", "precedents": ["InstallGPU", "InstallOptDevice"]},
        {"label": "Test", "duration": 10, "resource": "Tester", "precedents": ["InstallBluetooth"]},
        {"label": "Pack", "duration": 5, "resource": "Packer", "precedents": ["Test"]}
    ],
    "Model F": [
        {"label": "InstallCPU", "duration": 7, "resource": "CPUInstaller", "precedents": []},
        {"label": "InstallDisk", "duration": 4, "resource": "DriveInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallOptDevice", "duration": 3, "resource": "DriveInstaller", "precedents": ["InstallDisk"]},
        {"label": "InstallGPU", "duration": 5, "resource": "CardInstaller", "precedents": ["InstallCPU"]},
        {"label": "InstallBluetooth", "duration": 6, "resource": "CommInstaller", "precedents": ["InstallGPU", "InstallOptDevice"]},
        {"label": "Test", "duration": 9, "resource": "Tester", "precedents": ["InstallBluetooth"]},
        {"label": "Pack", "duration": 4, "resource": "Packer", "precedents": ["Test"]}
    ]
}


# Defintion of activities and their parameters 
quantities = {
    "Model A": 5,
    "Model B": 3,
    "Model C": 4,
    "Model D": 2,
    "Model E": 6,
    "Model F": 1
}

# Definition of the CP-SAT model
model = cp_model.CpModel()

# Decision variables for each activity of each computer
activity_vars = {}
for model_name, act_list in activities.items():
    for i in range(len(act_list)):
        for q in range(quantities[model_name]):
            start_var = model.NewIntVar(0, 10000, f'start_{model_name}_{i}_{q}')
            duration = act_list[i]['duration']
            activity_var = model.NewIntervalVar(start_var, duration, start_var + duration, f'activity_{model_name}_{i}_{q}')
            activity_vars[(model_name, i, q)] = activity_var

# Precedence constraints
for model_name, act_list in activities.items():
    for i in range(len(act_list)):
        for pred in act_list[i]['precedents']:
            pred_index = next(index for index, act in enumerate(act_list) if act['label'] == pred)
            for q in range(quantities[model_name]):
                model.Add(activity_vars[(model_name, pred_index, q)].EndExpr() <= activity_vars[(model_name, i, q)].StartExpr())

# Resource constraints
resources = {}
for model_name, act_list in activities.items():
    for i in range(len(act_list)):
        resource = act_list[i]['resource']
        if resource not in resources:
            resources[resource] = []
        for q in range(quantities[model_name]):
            resources[resource].append(activity_vars[(model_name, i, q)])

# Ensure no overlap in resource usage
for resource, intervals in resources.items():
    model.AddNoOverlap(intervals)

# Define the objective to minimize the makespan (the time to complete all activities)
makespan = model.NewIntVar(0, 10000, 'makespan')

# Collect end times of the last activities
end_times = []
for model_name, act_list in activities.items():
    last_activity_index = len(act_list) - 1  
    for q in range(quantities[model_name]):
        end_times.append(activity_vars[(model_name, last_activity_index, q)].EndExpr())

# Set the makespan as the maximum of all collected end times
model.AddMaxEquality(makespan, end_times)

# Minimize the makespan
model.Minimize(makespan)

# Solve the model
solver = cp_model.CpSolver()
status = solver.Solve(model)

# Output results
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print("Optimal Schedule:")
    for model_name, act_list in activities.items():
        for i in range(len(act_list)):
            for q in range(quantities[model_name]):
                start_time = solver.Value(activity_vars[(model_name, i, q)].StartExpr())
                print(f'{act_list[i]["label"]} for {model_name} starts at {start_time}')
else:
    print("No solution found.")
