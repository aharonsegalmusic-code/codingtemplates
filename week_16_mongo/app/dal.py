from connection import collection
from connection import collection

# 1 -----------------
def get_engineering_high_salary_employees():
    filter_query = {"job_role.department": "Engineering", "salary": {"$gt": 65000}}
    projection = {"_id": 0, "employee_id": 1, "name": 1, "salary": 1}
    documents = collection.find(filter_query, projection)
    return list(documents)

# 2 -----------------
def get_employees_by_age_and_role():
    filter_query = {
        "age": {"$gte": 30, "$lte": 45},
        "job_role.title": {"$in": ["Engineer", "Specialist"]},
    }
    projection = {"_id": 0}
    documents = collection.find(filter_query, projection)
    return list(documents)

# 3 -----------------
def get_top_seniority_employees_excluding_hr():
    filter_query = {"job_role.department": {"$ne": "HR"}}
    projection = {"_id": 0}
    documents = collection.find(filter_query, projection).sort("years_at_company", -1).limit(7)
    return list(documents)

# 4 -----------------
def get_employees_by_age_or_seniority():
    filter_query = {
        "$or": [
            {"age": {"$gt": 50}},
            {"years_at_company": {"$lt": 3}},
        ]
    }
    projection = {"_id": 0, "employee_id": 1, "name": 1, "age": 1, "years_at_company": 1}
    documents = collection.find(filter_query, projection)
    return list(documents)

# 5 -----------------
def get_managers_excluding_departments():
    filter_query = {
        "job_role.title": "Manager",
        "job_role.department": {"$nin": ["Sales", "Marketing"]},
    }
    projection = {"_id": 0}
    documents = collection.find(filter_query, projection)
    return list(documents)

# 6 -----------------
def get_employees_by_lastname_and_age():
    filter_query = {
        "$or": [
            {"name": {"$regex": "Wright$"}},
            {"name": {"$regex": "Nelson$"}},
        ],
        "age": {"$lt": 35},
    }
    projection = {"_id": 0, "name": 1, "age": 1, "job_role.department": 1}
    documents = collection.find(filter_query, projection)
    return list(documents)