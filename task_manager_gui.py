import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Define the filename for storing tasks
TASKS_FILE = 'tasks.json'

class Task:
    """
    A class to represent a Task.
    """
    def __init__(self, id, title, completed=False):
        self.id = id
        self.title = title
        self.completed = completed

    def to_dict(self):
        """
        Convert the Task instance to a dictionary.
        """
        return {
            'id': self.id,
            'title': self.title,
            'completed': self.completed
        }

    @staticmethod
    def from_dict(task_dict):
        """
        Create a Task instance from a dictionary.
        """
        return Task(
            id=task_dict['id'],
            title=task_dict['title'],
            completed=task_dict['completed']
        )

def load_tasks():
    """
    Load tasks from the JSON file.
    Returns a list of Task instances.
    """
    if not os.path.exists(TASKS_FILE):
        return []

    with open(TASKS_FILE, 'r') as file:
        try:
            tasks_data = json.load(file)
            return [Task.from_dict(task) for task in tasks_data]
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Corrupted tasks.json file.")
            return []

def save_tasks(tasks):
    """
    Save the list of Task instances to the JSON file.
    """
    with open(TASKS_FILE, 'w') as file:
        tasks_data = [task.to_dict() for task in tasks]
        json.dump(tasks_data, file, indent=4)

def add_task(tasks_listbox):
    """
    Add a new task to the task list.
    """
    title = simpledialog.askstring("Input", "Enter task title:")
    if not title:
        messagebox.showwarning("Input Error", "Task title cannot be empty.")
        return
    tasks = load_tasks()
    task_id = max([task.id for task in tasks], default=0) + 1
    new_task = Task(id=task_id, title=title)
    tasks.append(new_task)
    save_tasks(tasks)
    refresh_tasks(tasks_listbox)

def view_tasks(tasks_listbox):
    """
    Display all tasks with their status in the Listbox.
    """
    tasks = load_tasks()
    tasks_listbox.delete(0, tk.END)
    if not tasks:
        tasks_listbox.insert(tk.END, "No tasks available.")
        return
    for task in tasks:
        status = "✔️ Completed" if task.completed else "❌ Pending"
        tasks_listbox.insert(tk.END, f"ID: {task.id} | {task.title} | {status}")

def delete_task(tasks_listbox):
    """
    Delete a task by its ID.
    """
    task_id = simpledialog.askinteger("Input", "Enter the ID of the task to delete:")
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            refresh_tasks(tasks_listbox)
            messagebox.showinfo("Success", f"Task with ID {task_id} has been deleted.")
            return
    messagebox.showwarning("Error", f"No task found with ID {task_id}.")

def mark_task_complete(tasks_listbox):
    """
    Mark a task as completed by its ID.
    """
    task_id = simpledialog.askinteger("Input", "Enter the ID of the task to mark as complete:")
    tasks = load_tasks()
    for task in tasks:
        if task.id == task_id:
            if task.completed:
                messagebox.showinfo("Info", "Task is already marked as completed.")
            else:
                task.completed = True
                save_tasks(tasks)
                refresh_tasks(tasks_listbox)
                messagebox.showinfo("Success", f"Task with ID {task_id} has been marked as completed.")
            return
    messagebox.showwarning("Error", f"No task found with ID {task_id}.")

def refresh_tasks(tasks_listbox):
    """
    Refresh the tasks displayed in the Listbox.
    """
    view_tasks(tasks_listbox)

def main():
    """
    The main function to run the Tkinter GUI application.
    """
    root = tk.Tk()
    root.title("Task Manager")
    root.geometry("600x400")
    root.configure(bg='magenta')


    # Create Listbox to display tasks
    tasks_listbox = tk.Listbox(root, height=10, width=50)
    tasks_listbox.pack(pady=10)

    # Add buttons
    btn_add = tk.Button(root, text="Add Task", command=lambda: add_task(tasks_listbox))
    btn_add.pack(pady=5)

    btn_delete = tk.Button(root, text="Delete Task", command=lambda: delete_task(tasks_listbox))
    btn_delete.pack(pady=5)

    btn_mark_complete = tk.Button(root, text="Mark Task as Complete", command=lambda: mark_task_complete(tasks_listbox))
    btn_mark_complete.pack(pady=5)

    btn_refresh = tk.Button(root, text="Refresh Tasks", command=lambda: refresh_tasks(tasks_listbox))
    btn_refresh.pack(pady=5)

    # Initially display tasks
    view_tasks(tasks_listbox)

    root.mainloop()

if __name__ == "__main__":
    main()
