import tkinter as tk

from tkinter import simpledialog

from canvasapi import Canvas

from decouple import config

API_URL = config('API_URL')

API_KEY = config('API_KEY')

canvas = Canvas(API_URL, API_KEY)

course_id = 498634

course = canvas.get_course(course_id)

if course is None:
    print("❌ Error connecting to Canvas")
else:
    print("✅ Connected to Canvas")

def create_discussion():
    title = simpledialog.askstring("Input", "What is the name of the discussion?")
    message = simpledialog.askstring("Input", "What is the message of the discussion?")
    discussion = course.create_discussion_topic(
        title=title,
        message=message,
        discussion_type="side_comment"
    )
    # check if it worked
    if discussion is None:
        result_message = "❌ Error creating discussion"
    else:
        result_message = "✅ Discussion created"
    result_label.config(text=result_message)

def reply_to_discussion():
    topics = course.get_discussion_topics()
    if not topics:
        result_message = "❌ No discussion topics found"
        result_label.config(text=result_message)
        return

    reply_window = tk.Toplevel(root)
    reply_window.title("Select Discussion to Reply")

    def select_discussion(topic_id):
        reply_window.destroy()
        reply = simpledialog.askstring("Input", "What is your reply?")
        if reply:
            topic = course.get_discussion_topic(topic_id)
            if topic:
                topic.reply(reply)
                result_message = "✅ Reply posted"
                result_label.config(text=result_message)
            else:
                result_message = "❌ Discussion not found"
                result_label.config(text=result_message)

    for topic in topics:
        topic_title = topic.title
        reply_button = tk.Button(reply_window, text=f"Reply to '{topic_title}'", command=lambda topic_id=topic.id: select_discussion(topic_id))
        reply_button.pack()

def edit_discussion():
    topics = course.get_discussion_topics()
    if not topics:
        result_message = "❌ No discussion topics found"
        result_label.config(text=result_message)
        return

    edit_window = tk.Toplevel(root)
    edit_window.title("Select Discussion to Edit")

    def select_discussion(topic_id):
        edit_window.destroy()
        topic = course.get_discussion_topic(topic_id)
        if topic:
            new_title = simpledialog.askstring("Input", "What is the new title?")
            new_message = simpledialog.askstring("Input", "What is the new message?")
            topic.edit(title=new_title, message=new_message)
            result_message = "✅ Discussion edited"
            result_label.config(text=result_message)
        else:
            result_message = "❌ Discussion not found"
            result_label.config(text=result_message)

    for topic in topics:
        topic_title = topic.title
        edit_button = tk.Button(edit_window, text=f"Edit '{topic_title}'", command=lambda topic_id=topic.id: select_discussion(topic_id))
        edit_button.pack()

def delete_discussion():
    topics = course.get_discussion_topics()
    if not topics:
        result_message = "❌ No discussion topics found"
        result_label.config(text=result_message)
        return

    delete_window = tk.Toplevel(root)
    delete_window.title("Select Discussion to Delete")

    def confirm_delete(topic_id):
        confirm_window = tk.Toplevel(delete_window)
        confirm_window.title("Confirm Deletion")
        confirm_message = tk.Label(confirm_window, text=f"Do you want to delete this discussion?")
        confirm_message.pack()

        def do_delete():
            topic = course.get_discussion_topic(topic_id)
            if topic:
                topic.delete()
                result_message = "✅ Discussion deleted"
                result_label.config(text=result_message)
            else:
                result_message = "❌ Discussion not found"
                result_label.config(text=result_message)
            confirm_window.destroy()
            delete_window.destroy()

        confirm_button = tk.Button(confirm_window, text="Yes", command=do_delete)
        confirm_button.pack()
        cancel_button = tk.Button(confirm_window, text="No", command=confirm_window.destroy)
        cancel_button.pack()

    for topic in topics:
        topic_title = topic.title
        delete_button = tk.Button(delete_window, text=f"Delete '{topic_title}'", command=lambda topic_id=topic.id: confirm_delete(topic_id))
        delete_button.pack()

root = tk.Tk()
root.title("Discussion Tasks")

root.geometry("400x200")

result_label = tk.Label(root, text="", padx=10, pady=10)
result_label.pack(side="bottom")

create_discussion_button = tk.Button(root, text="Create Post", command=create_discussion)
create_discussion_button.pack()

reply_button = tk.Button(root, text="Reply to Post", command=reply_to_discussion)
reply_button.pack()

edit_button = tk.Button(root, text="Edit Post", command=edit_discussion)
edit_button.pack()

delete_button = tk.Button(root, text="Delete Post", command=delete_discussion)
delete_button.pack()

root.mainloop()
