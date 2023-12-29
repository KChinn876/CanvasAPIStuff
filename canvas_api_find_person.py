from canvasapi import Canvas
from decouple import config

API_URL = config('API_URL')
API_KEY = config('API_KEY')

canvas = Canvas(API_URL, API_KEY)

course_id = config('COURSE_ID')
course = canvas.get_course(course_id)

student_count = 0
ta_count = 0

for student in course.get_users(enrollment_type=['student']):
    student_count += 1
for ta in course.get_users(enrollment_type=['ta']):
    ta_count += 1

print(f"There are {student_count} students enrolled in this class and {ta_count} TAs.")

print("Are you looking for a TA or a Student?")
user_type = input()
if user_type == "Student" or user_type == "student":
    print("What is the name of the student you want to find?")
    student_name = input()
    # Find the student SIS id of the student
    student_id = 0
    for student in course.get_users(enrollment_type=['student']):
        if student.name == student_name:
            print("✅ Found Student!")
            student_id = student.id
            print(f"Found student with name {student_name} and id {student_id}.")
            break

elif user_type == "TA" or user_type == "ta":
    print("What is the name of the TA you want to find?")
    ta_name = input()
    # Find the student SIS id of the student
    ta_id = 0
    for ta in course.get_users(enrollment_type=['ta']):
        if ta.name == ta_name:
            print("✅ Found TA!")
            ta_id = ta.id
            print(f"Found TA with name {ta_name} and ID {ta_id}.")
            break
else:
    print("Invalid input. Please try again.")
    


