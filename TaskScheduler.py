import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, title, description, due_date, priority):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def remove(self, data):
        current_node = self.head
        if current_node and current_node.data == data:
            self.head = current_node.next
            return
        prev_node = None
        while current_node and current_node.data != data:
            prev_node = current_node
            current_node = current_node.next
        if current_node is None:
            return
        prev_node.next = current_node.next

    def selection_sort(self):
        if self.head is None:
            return

        current_node = self.head
        while current_node:
            min_node = current_node
            next_node = current_node.next
            while next_node:
                if next_node.data.priority < min_node.data.priority:
                    min_node = next_node
                next_node = next_node.next
            if min_node != current_node:
                current_node.data, min_node.data = min_node.data, current_node.data
            current_node = current_node.next

    def display_tasks(self):
        tasks = []
        current_node = self.head
        while current_node:
            tasks.append(current_node.data)
            current_node = current_node.next
        return tasks

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def is_empty(self):
        return len(self.items) == 0

class Scheduler:
    def __init__(self):
        self.tasks = LinkedList()
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def add_task(self, task):
        self.tasks.append(task)
        self.undo_stack.push(('add', task))

    def remove_task(self, task):
        self.tasks.remove(task)
        self.undo_stack.push(('remove', task))

    def undo(self):
        if not self.undo_stack.is_empty():
            action, task = self.undo_stack.pop()
            if action == 'add':
                self.tasks.remove(task)
                self.redo_stack.push(('add', task))
            elif action == 'remove':
                self.tasks.append(task)
                self.redo_stack.push(('remove', task))

    def redo(self):
        if not self.redo_stack.is_empty():
            action, task = self.redo_stack.pop()
            if action == 'add':
                self.tasks.append(task)
                self.undo_stack.push(('add', task))
            elif action == 'remove':
                self.tasks.remove(task)
                self.undo_stack.push(('remove', task))

class TaskSchedulerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Scheduler")

        self.scheduler = Scheduler()

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Title:")
        self.title_label.grid(row=0, column=0, sticky=tk.E)
        self.title_entry = tk.Entry(self.master)
        self.title_entry.grid(row=0, column=1)

        self.desc_label = tk.Label(self.master, text="Description:")
        self.desc_label.grid(row=1, column=0, sticky=tk.E)
        self.desc_entry = tk.Entry(self.master)
        self.desc_entry.grid(row=1, column=1)

        self.due_label = tk.Label(self.master, text="Due Date:")
        self.due_label.grid(row=2, column=0, sticky=tk.E)
        self.due_entry = tk.Entry(self.master)
        self.due_entry.grid(row=2, column=1)

        self.priority_label = tk.Label(self.master, text="Priority:")
        self.priority_label.grid(row=3, column=0, sticky=tk.E)
        self.priority_entry = tk.Entry(self.master)
        self.priority_entry.grid(row=3, column=1)

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.E + tk.W)

        self.undo_button = tk.Button(self.master, text="Undo", command=self.undo)
        self.undo_button.grid(row=5, column=0, pady=10)

        self.redo_button = tk.Button(self.master, text="Redo", command=self.redo)
        self.redo_button.grid(row=5, column=1, pady=10)

        self.tasks_listbox = tk.Listbox(self.master, width=50, height=10)
        self.tasks_listbox.grid(row=6, columnspan=2)

        self.tasks_listbox.bind("<Double-Button-1>", self.display_description)

        self.description_label_header = tk.Label(self.master, text="Description:")
        self.description_label_header.grid(row=7, column=0, columnspan=2)

        self.description_label = tk.Label(self.master, text="")
        self.description_label.grid(row=8, column=0, columnspan=2, pady=5)

        self.refresh_tasks()

    def add_task(self):
        title = self.title_entry.get()
        description = self.desc_entry.get()
        due_date = self.due_entry.get()
        priority = int(self.priority_entry.get())

        if title and description and due_date and priority:
            task = Task(title, description, due_date, priority)
            self.scheduler.add_task(task)
            messagebox.showinfo("Success", "Task added successfully.")
            self.refresh_tasks()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def undo(self):
        self.scheduler.undo()
        self.refresh_tasks()

    def redo(self):
        self.scheduler.redo()
        self.refresh_tasks()

    def refresh_tasks(self):
        self.scheduler.tasks.selection_sort()
        self.tasks_listbox.delete(0, tk.END)
        tasks = self.scheduler.tasks.display_tasks()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"{task.title} - {task.due_date}")

    def display_description(self, event):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            selected_task = self.scheduler.tasks.display_tasks()[selected_index[0]]
            self.description_label.config(text=selected_task.description)


def main():
    root = tk.Tk()
    app = TaskSchedulerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()