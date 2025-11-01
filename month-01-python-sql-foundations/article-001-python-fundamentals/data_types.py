# data_types.py - Understanding Python Data Types

# 1. LISTS - Ordered, mutable collections
sales_data = [12000, 15000, 18000, 14000, 20000]
print("Sales Data (List):", sales_data)
print("First month sales:", sales_data[0])  # Indexing starts at 0
print("Last month sales:", sales_data[-1])  # Negative indexing

# Adding to list
sales_data.append(22000)
print("After adding new month:", sales_data)

# List slicing
first_three_months = sales_data[0:3]
print("First 3 months:", first_three_months)

print("\n" + "="*50 + "\n")

# 2. TUPLES - Ordered, immutable collections
database_config = ("localhost", 5432, "postgres", "mydb")
host, port, user, database = database_config  # Unpacking
print(f"Database Config: {host}:{port}/{database} (user: {user})")

print("\n" + "="*50 + "\n")

# 3. DICTIONARIES - Key-value pairs (like JSON)
employee = {
    "name": "Surani",
    "role": "Data Engineer",
    "skills": ["Python", "SQL", "AWS"],
    "experience_years": 2,
    "is_remote": True
}

print("Employee Data (Dictionary):")
print(f"Name: {employee['name']}")
print(f"Role: {employee['role']}")
print(f"Skills: {', '.join(employee['skills'])}")

# Adding new key
employee["location"] = "Pune"
print(f"Location: {employee['location']}")

print("\n" + "="*50 + "\n")

# 4. SETS - Unordered, unique collections
skills_team_a = {"Python", "SQL", "AWS", "Docker"}
skills_team_b = {"Python", "Java", "AWS", "Kubernetes"}

# Set operations
common_skills = skills_team_a & skills_team_b  # Intersection
all_skills = skills_team_a | skills_team_b      # Union
unique_to_a = skills_team_a - skills_team_b     # Difference

print("Common Skills:", common_skills)
print("All Skills:", all_skills)
print("Unique to Team A:", unique_to_a)

print("\n" + "="*50 + "\n")

# 5. TYPE CHECKING
print("Type Checking:")
print(f"sales_data is {type(sales_data)}")
print(f"database_config is {type(database_config)}")
print(f"employee is {type(employee)}")
print(f"skills_team_a is {type(skills_team_a)}")