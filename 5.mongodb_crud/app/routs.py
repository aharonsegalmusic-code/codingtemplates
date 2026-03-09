from fastapi import APIRouter
import dal

router = APIRouter()

@router.get("/employees/engineering/high-salary")
def employees_engineering_high_salary():
    return dal.get_engineering_high_salary_employees()


@router.get("/employees/by-age-and-role")
def employees_by_age_and_role():
    return dal.get_employees_by_age_and_role()


@router.get("/employees/top-seniority")
def employees_top_seniority():
    return dal.get_top_seniority_employees_excluding_hr()


@router.get("/employees/age-or-seniority")
def employees_age_or_seniority():
    return dal.get_employees_by_age_or_seniority()


@router.get("/employees/managers/excluding-departments")
def employees_managers_excluding_departments():
    return dal.get_managers_excluding_departments()


@router.get("/employees/by-lastname-and-age")
def employees_by_lastname_and_age():
    return dal.get_employees_by_lastname_and_age()