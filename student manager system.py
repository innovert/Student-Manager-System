#STUDENT MANAGER SYSTEM

import tkinter as tk
from tkinter import messagebox
import json
import os

# ======== OOP CLASSES ========

class Student:
    def __init__(self, sid, name, age, programme):
        self.sid = sid
        self.name = name
        self.age = age
        self.programme = programme

    def to_dict(self):
        return {"sid": self.sid, "name": self.name, "age": self.age, "programme": self.programme}

    @classmethod
    def from_dict(cls, data):
        return cls(data["sid"], data["name"], data["age"], data["programme"])

    def __str__(self):
        return f"{self.sid} - {self.name}, {self.age} yrs, {self.programme}"

class StudentManager:
    def __init__(self):
        self.students = []
        self.next_id = 1
        self.file_path = "students.json"
        self.load_students()

    def add_student(self, name, age, programme):
        student = Student(self.next_id, name, age, programme)
        self.students.append(student)
        self.next_id += 1
        self.save_students()
        return student

    def get_all(self):
        return self.students

    def find_by_id_or_name(self, keyword):
        keyword = keyword.strip().lower()
        for s in self.students:
            if str(s.sid) == keyword or s.name.lower() == keyword:
                return s
        return None

    def delete_student(self, student):
        if student in self.students:
            self.students.remove(student)
            self.save_students()
            return True
        return False

    def save_students(self):
        data = [s.to_dict() for s in self.students]
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def load_students(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                data = json.load(file)
                self.students = [Student.from_dict(d) for d in data]
                if self.students:
                    self.next_id = max(s.sid for s in self.students) + 1

# ======== GUI SETUP ========

manager = StudentManager()

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    programme = programme_entry.get()
    if name and age and programme:
        student = manager.add_student(name, age, programme)
        messagebox.showinfo("Success", f"Student {student.name} added.")
        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        programme_entry.delete(0, tk.END)
        refresh_list()
    else:
        messagebox.showwarning("Missing Info", "Please fill all fields.")

def refresh_list():
    student_listbox.delete(0, tk.END)
    for s in manager.get_all():
        student_listbox.insert(tk.END, str(s))

def search_student():
    keyword = search_entry.get()
    if not keyword:
        messagebox.showinfo("Input Needed", "Enter name or ID to search.")
        return
    student = manager.find_by_id_or_name(keyword)
    if student:
        messagebox.showinfo("Student Found", str(student))
    else:
        messagebox.showwarning("Not Found", "No student matched your input.")

def delete_selected():
    selected = student_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Student", "Please select a student from the list.")
        return
    student_str = student_listbox.get(selected[0])
    sid = int(student_str.split(" - ")[0])
    student = manager.find_by_id_or_name(str(sid))
    if student and manager.delete_student(student):
        messagebox.showinfo("Deleted", f"Student ID {sid} deleted.")
        refresh_list()
    else:
        messagebox.showwarning("Error", "Could not delete student.")

# Main window
window = tk.Tk()
window.title("Student Record Manager")
window.geometry("550x550")

# Entry fields
tk.Label(window, text="Name").pack()
name_entry = tk.Entry(window)
name_entry.pack()

tk.Label(window, text="Age").pack()
age_entry = tk.Entry(window)
age_entry.pack()

tk.Label(window, text="Programme").pack()
programme_entry = tk.Entry(window)
programme_entry.pack()

# Buttons
tk.Button(window, text="Add Student", command=add_student).pack(pady=5)

# Search field + button
tk.Label(window, text="Search by ID or Name").pack()
search_entry = tk.Entry(window)
search_entry.pack()
tk.Button(window, text="Search", command=search_student).pack()

# Student List
student_listbox = tk.Listbox(window, width=60, height=10)
student_listbox.pack(pady=10)

tk.Button(window, text="Delete Selected", command=delete_selected).pack(pady=5)
tk.Button(window, text="Refresh List", command=refresh_list).pack()

# Start with existing data
refresh_list()

# Main loop
window.mainloop()