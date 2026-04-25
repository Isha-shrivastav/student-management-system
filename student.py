import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database connection
conn = sqlite3.connect("students.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll TEXT PRIMARY KEY,
    name TEXT,
    course TEXT
)
""")
conn.commit()

# Add student
def add_student():
    try:
        roll = entry_roll.get()
        name = entry_name.get()
        course = entry_course.get()

        cursor.execute("INSERT INTO students VALUES (?, ?, ?)", (roll, name, course))
        conn.commit()

        messagebox.showinfo("Success", "Student added successfully!")
        clear_fields()
        view_students()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll number already exists!")

# View students
def view_students():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row)

# Delete student
def delete_student():
    try:
        selected = listbox.get(listbox.curselection())
        roll = selected[0]

        cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
        conn.commit()

        messagebox.showinfo("Deleted", "Student deleted successfully!")
        view_students()

    except:
        messagebox.showerror("Error", "Please select a student")

# Update student
def update_student():
    try:
        selected = listbox.get(listbox.curselection())
        roll = selected[0]

        cursor.execute("UPDATE students SET name=?, course=? WHERE roll=?",
                       (entry_name.get(), entry_course.get(), roll))
        conn.commit()

        messagebox.showinfo("Updated", "Student updated successfully!")
        view_students()

    except:
        messagebox.showerror("Error", "Select a student to update")

# Clear fields
def clear_fields():
    entry_roll.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_course.delete(0, tk.END)

# GUI Window
root = tk.Tk()
root.title("Student Management System")
root.geometry("500x400")

# Labels & Entries
tk.Label(root, text="Roll No").pack()
entry_roll = tk.Entry(root)
entry_roll.pack()

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Course").pack()
entry_course = tk.Entry(root)
entry_course.pack()

# Buttons
tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="Update Student", command=update_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)
tk.Button(root, text="View Students", command=view_students).pack(pady=5)
tk.Button(root, text="Clear", command=clear_fields).pack(pady=5)

# Listbox
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)

view_students()

root.mainloop()