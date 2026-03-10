"""
reads student grade data from a json file and prints a grade summary report
gets: students.json file with student names and subject grades
gives: formatted grade report printed to terminal
"""

"""
flow:
    1. reads students.json from the same directory as the script
    2. for each student, calculates the average of their grades
    3. prints each student's name and average (or "no grades" if empty)
    4. calculates the class average across all students who have grades
    5. finds and prints the top student with the highest average

components:
    student_list - list of student dicts loaded from students.json
    averages - dict mapping student name to their calculated average
    class_average - the mean of all individual student averages who have grades

strategy:
    - students with no grades are skipped when calculating class average
      so they do not cause a division by zero or skew the result
    - averages is built as a dict keyed by name so finding the max is
      a single call to max() without a second loop over the list
    - the script uses os.path to locate students.json relative to the script
      so it works from any working directory, not just the project folder
"""

import json
import os


def load_students(file_path):
    """
    reads the students json file and returns the list of student records
    receives: file_path — the full path to the json file as a string
    returns: a list of dicts, each with a name key and a grades dict
    """
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def calculate_average(grades):
    """
    calculates the numeric average of a grades dictionary
    receives: grades — a dict mapping subject names to numeric grade values
    returns: the average rounded to one decimal place, or None if grades is empty
    """
    if not grades:
        return None
    total = sum(grades.values())
    return round(total / len(grades), 1)


def format_student_line(student_name, average):
    """
    formats one line of the grade report for a single student
    receives: student_name — the student's name as a string
              average — a float with their average grade, or None if no grades
    returns: a formatted string ready to print to the terminal
    """
    if average is None:
        return f"{student_name:<8} — no grades"
    return f"{student_name:<8} — average: {average}"


def print_report(student_list):
    """
    builds and prints the full grade report for all students in the list
    receives: student_list — a list of student dicts with name and grades fields
    returns: nothing, prints the report directly to the terminal
    """
    averages = {}

    # print each student's individual result
    for student in student_list:
        student_name = student["name"]
        grades = student["grades"]
        average = calculate_average(grades)
        if average is not None:
            averages[student_name] = average
        print(format_student_line(student_name, average))

    print()

    # calculate and print the overall class average
    if averages:
        class_average = round(sum(averages.values()) / len(averages), 1)
        print(f"Class average: {class_average}")

        # find and print the student with the highest average
        top_student_name = max(averages, key=averages.get)
        top_average = averages[top_student_name]
        print(f"Top student: {top_student_name} ({top_average})")


# locate students.json in the same folder as this script
script_directory = os.path.dirname(os.path.abspath(__file__))
students_file_path = os.path.join(script_directory, "students.json")

# load the student data from the json file
student_list = load_students(students_file_path)

# print the full grade report
print_report(student_list)
