import time
from canvasapi import Canvas
from decouple import config

# Canvas API URL
API_URL = config('API_URL')

# Canvas API key
API_KEY = config('API_KEY')

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# This is the course id for the course you want to create the assignment in
course_id = config('COURSE_ID')

# Get the course object
course = canvas.get_course(course_id)

def change_due_date():
    due_date = '2024-03-06T04:59:00Z'  # 11:59 PM with timezone offset (ISO 8601 format)

    print("What is the name of the assignment you want to change?")
    assignment_name = input()

    print("Changing due date...")
    time.sleep(3)

    # Find the id of the assignment
    assignment_id = 0
    for assignment in course.get_assignments():
        if assignment.name == assignment_name:
            assignment_id = assignment.id
            break

    assignment = course.get_assignment(assignment_id)

    # Edit the assignment's due date
    assignment.edit(assignment={'due_at': due_date})

    # Check to see if due date was changed
    if assignment.due_at == due_date:
        print("✅ Due date changed successfully!")
    else:
        print("❌ Due date not changed.")

def change_assignment_name():
    print("What is the name of the assignment you want to change?")
    assignment_name = input()
    print("What is the new name of the assignment?")
    new_assignment_name = input()

    print("Changing name...")
    time.sleep(3)

    # Find the id of the assignment
    assignment_id = 0
    for assignment in course.get_assignments():
        if assignment.name == assignment_name:
            assignment_id = assignment.id
            break

    assignment = course.get_assignment(assignment_id)

    # Edit the assignment's name
    assignment.edit(assignment={'name': new_assignment_name})

    # Check to see if name was changed
    if assignment.name == new_assignment_name:
        print("✅ Name changed successfully!")
    else:
        print("❌ Name not changed.")

def create_assignment():
    # Create a new assignment
    print("What is the name of the assignment you want to create?")
    assignment_name = input()
    print("How many points is this assignment worth?")
    assignment_points = input()
    assignment = course.create_assignment(
        assignment={'name': assignment_name, 'submission_types': 'online_url', 'points_possible': assignment_points})

    print("Creating assignment...")
    time.sleep(3)

    # Check to see if assignment was created. If so, print success message
    if assignment.name == assignment_name:
        print("✅ Assignment created successfully!")
    else:
        print("❌ Assignment not created.")

def delete_assignment():
    print("What is the name of the assignment you want to delete?")
    assignment_name = input()
    count = 0
    for assignment in course.get_assignments():
        if assignment.name == assignment_name:
            count += 1
            assignment.delete()
    if count == 0:
        print("❌ Assignment not found.")
    elif count == 1:
        print("✅ Assignment deleted successfully!")
    elif count > 1:
        print("✅ Assignments deleted successfully!")

print("1. Change the due date of an assignment. \n2. Change the name of an assignment. \n3. Create an assignment. \n4. Delete an assignment.")

# Prompt user to enter a number 1 - 3
print("Enter a number 1 - 4:")

# Get the user's input
user_input = input()

if user_input == "1":
    change_due_date()
elif user_input == "2":
    change_assignment_name()
elif user_input == "3":
    create_assignment()
elif user_input == "4":
    delete_assignment()
else:
    print("Invalid input. Please enter a number 1 - 4.")
