import time
import tkinter as tk
from canvasapi import Canvas
from decouple import config

# Canvas API URL
API_URL = config('API_URL')

# Canvas API key
API_KEY = config('API_KEY')

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

# This is the course id for the course you want to create the assignment in
course_id = 498634

# Get the course object
course = canvas.get_course(course_id)

def change_due_date():
    due_date = '2024-03-06T04:59:00Z'  # 11:59 PM with timezone offset (ISO 8601 format)

    # Create a popup window
    popup = tk.Toplevel()
    popup.title("Change Due Date")

    label = tk.Label(popup, text="Assignment Name:")
    label.pack()
    assignment_name = tk.Entry(popup)
    assignment_name.pack()

    def change_due_date_inner():
        name = assignment_name.get()
        assignment_id = None

        for assignment in course.get_assignments():
            if assignment.name == name:
                assignment_id = assignment.id
                break

        if assignment_id is not None:
            assignment = course.get_assignment(assignment_id)
            assignment.edit(assignment={'due_at': due_date})

            if assignment.due_at == due_date:
                result_label.config(text="✅ Due date changed successfully!")
            else:
                result_label.config(text="❌ Due date not changed.")
        else:
            result_label.config(text="❌ Assignment not found.")

    change_button = tk.Button(popup, text="Change Due Date", command=change_due_date_inner)
    change_button.pack()

    result_label = tk.Label(popup, text="")
    result_label.pack()

def change_assignment_name():
    popup = tk.Toplevel()
    popup.title("Change Assignment Name")

    label_old = tk.Label(popup, text="Old Assignment Name:")
    label_old.pack()
    assignment_name_old = tk.Entry(popup)
    assignment_name_old.pack()

    label_new = tk.Label(popup, text="New Assignment Name:")
    label_new.pack()
    assignment_name_new = tk.Entry(popup)
    assignment_name_new.pack()

    def change_assignment_name_inner():
        name_old = assignment_name_old.get()
        name_new = assignment_name_new.get()
        assignment_id = None

        for assignment in course.get_assignments():
            if assignment.name == name_old:
                assignment_id = assignment.id
                break

        if assignment_id is not None:
            assignment = course.get_assignment(assignment_id)
            assignment.edit(assignment={'name': name_new})

            if assignment.name == name_new:
                result_label.config(text="✅ Name changed successfully!")
            else:
                result_label.config(text="❌ Name not changed.")
        else:
            result_label.config(text="❌ Assignment not found.")

    change_button = tk.Button(popup, text="Change Assignment Name", command=change_assignment_name_inner)
    change_button.pack()

    result_label = tk.Label(popup, text="")
    result_label.pack()

def create_assignment():
    popup = tk.Toplevel()
    popup.title("Create Assignment")

    label_name = tk.Label(popup, text="Assignment Name:")
    label_name.pack()
    assignment_name = tk.Entry(popup)
    assignment_name.pack()

    label_points = tk.Label(popup, text="Points Possible:")
    label_points.pack()
    assignment_points = tk.Entry(popup)
    assignment_points.pack()

    def create_assignment_inner():
        name = assignment_name.get()
        points = assignment_points.get()

        assignment = course.create_assignment(
            assignment={'name': name, 'submission_types': 'online_url', 'points_possible': points})

        if assignment.name == name:
            result_label.config(text="✅ Assignment created successfully!")
        else:
            result_label.config(text="❌ Assignment not created.")

    create_button = tk.Button(popup, text="Create Assignment", command=create_assignment_inner)
    create_button.pack()

    result_label = tk.Label(popup, text="")
    result_label.pack()

def delete_assignment():
    popup = tk.Toplevel()
    popup.title("Delete Assignment")

    label = tk.Label(popup, text="Assignment Name:")
    label.pack()
    assignment_name = tk.Entry(popup)
    assignment_name.pack()

    def delete_assignment_inner():
        name = assignment_name.get()
        count = 0

        for assignment in course.get_assignments():
            if assignment.name == name:
                count += 1
                assignment.delete()

        if count == 0:
            result_label.config(text="❌ Assignment not found.")
        elif count == 1:
            result_label.config(text="✅ Assignment deleted successfully!")
        elif count > 1:
            result_label.config(text="✅ Assignments deleted successfully!")

    delete_button = tk.Button(popup, text="Delete Assignment", command=delete_assignment_inner)
    delete_button.pack()

    result_label = tk.Label(popup, text="")
    result_label.pack()

root = tk.Tk()
root.title("Canvas Tasks")

change_due_date_button = tk.Button(root, text="Change Due Date", command=change_due_date)
change_due_date_button.pack()

change_assignment_name_button = tk.Button(root, text="Change Assignment Name", command=change_assignment_name)
change_assignment_name_button.pack()

create_assignment_button = tk.Button(root, text="Create Assignment", command=create_assignment)
create_assignment_button.pack()

delete_assignment_button = tk.Button(root, text="Delete Assignment", command=delete_assignment)
delete_assignment_button.pack()

root.mainloop()
