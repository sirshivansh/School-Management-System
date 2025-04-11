import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Password for accessing the system
SYSTEM_PASSWORD = "123456789"

# Database setup
def setup_database():
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()

    # Only create tables if they do not already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            class TEXT,
            roll_number TEXT UNIQUE,
            password TEXT DEFAULT 'defaultpass'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            TID TEXT UNIQUE,
            name TEXT,
            subject TEXT,
            salary REAL,
            password TEXT DEFAULT 'defaultpass'
        )
    ''')

    conn.commit()
    conn.close()

# Main application
def main_app():
    app.title("School Management System")

    # Main Frame
    main_frame = tk.Frame(app)
    main_frame.pack(pady=10)

    # Tabs for Students and Teachers
    tab_control = ttk.Notebook(main_frame)
    student_tab = ttk.Frame(tab_control)
    teacher_tab = ttk.Frame(tab_control)

    tab_control.add(student_tab, text='Student Management')
    tab_control.add(teacher_tab, text='Teacher Management')
    tab_control.pack(expand=1, fill='both')

    # Student Management
    setup_student_tab(student_tab)

    # Teacher Management
    setup_teacher_tab(teacher_tab)

def setup_student_tab(tab):
    # Labels and Entries
    tk.Label(tab, text="Name").grid(row=0, column=0)
    tk.Label(tab, text="Age").grid(row=1, column=0)
    tk.Label(tab, text="Class").grid(row=2, column=0)
    tk.Label(tab, text="Roll Number").grid(row=3, column=0)

    global name_entry, age_entry, class_entry, roll_entry
    name_entry = tk.Entry(tab)
    age_entry = tk.Entry(tab)
    class_entry = tk.Entry(tab)
    roll_entry = tk.Entry(tab)

    name_entry.grid(row=0, column=1)
    age_entry.grid(row=1, column=1)
    class_entry.grid(row=2, column=1)
    roll_entry.grid(row=3, column=1)

    # Buttons
    tk.Button(tab, text="Add Student", command=add_student).grid(row=4, column=0, pady=10)
    tk.Button(tab, text="Delete Student", command=lambda: delete_student(roll_entry.get())).grid(row=4, column=1, pady=10)
    tk.Button(tab, text="View Students", command=view_students).grid(row=5, column=0, columnspan=2)
    tk.Button(tab, text="Search Student", command=search_student).grid(row=6, column=0, columnspan=2)

    # Treeview for displaying students
    global student_tree
    student_tree = ttk.Treeview(tab, columns=("ID", "Name", "Age", "Class", "Roll Number"), show="headings")
    student_tree.grid(row=7, column=0, columnspan=2)
    student_tree.heading("ID", text="ID")
    student_tree.heading("Name", text="Name")
    student_tree.heading("Age", text="Age")
    student_tree.heading("Class", text="Class")
    student_tree.heading("Roll Number", text="Roll Number")

def add_student():
    name = name_entry.get()
    age = age_entry.get()
    class_name = class_entry.get()
    roll_number = roll_entry.get()

    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (name, age, class, roll_number) VALUES (?, ?, ?, ?)", (name, age, class_name, roll_number))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully.")
        view_students()  # Refresh the view
        clear_student_fields()  # Clear input fields
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Roll Number must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def clear_student_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)

def delete_student(roll_number):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE roll_number = ?", (roll_number,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Student deleted successfully.")
    view_students()  # Refresh the view

def view_students():
    for row in student_tree.get_children():
        student_tree.delete(row)  # Clear existing entries
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, age, class, roll_number FROM students")
    for row in cursor.fetchall():
        student_tree.insert("", "end", values=row)
    conn.close()

def search_student():
    roll_number = roll_entry.get()
    for row in student_tree.get_children():
        student_tree.delete(row)  # Clear existing entries
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, name, age, class, roll_number FROM students WHERE roll_number = ?", (roll_number,))
    results = cursor.fetchall()
    for row in results:
        student_tree.insert("", "end", values=row)
    if not results:
        messagebox.showinfo("Info", "No student found with that Roll Number.")
    conn.close()

def setup_teacher_tab(tab):
    # Labels and Entries
    tk.Label(tab, text="TID").grid(row=0, column=0)  # Added TID label
    tk.Label(tab, text="Name").grid(row=1, column=0)
    tk.Label(tab, text="Subject").grid(row=2, column=0)
    tk.Label(tab, text="Salary").grid(row=3, column=0)

    global tid_entry, teacher_name_entry, subject_entry, salary_entry
    tid_entry = tk.Entry(tab)  # Entry for TID
    teacher_name_entry = tk.Entry(tab)
    subject_entry = tk.Entry(tab)
    salary_entry = tk.Entry(tab)

    tid_entry.grid(row=0, column=1)  # Position for TID entry
    teacher_name_entry.grid(row=1, column=1)
    subject_entry.grid(row=2, column=1)
    salary_entry.grid(row=3, column=1)

    # Buttons
    tk.Button(tab, text="Add Teacher", command=add_teacher).grid(row=4, column=0, pady=10)
    tk.Button(tab, text="Delete Teacher", command=lambda: delete_teacher(tid_entry.get())).grid(row=4, column=1, pady=10)
    tk.Button(tab, text="View Teachers", command=view_teachers).grid(row=5, column=0, columnspan=2)
    tk.Button(tab, text="Search Teacher", command=search_teacher).grid(row=6, column=0, columnspan=2)

    # Treeview for displaying teachers
    global teacher_tree
    teacher_tree = ttk.Treeview(tab, columns=("ID", "TID", "Name", "Subject", "Salary"), show="headings")
    teacher_tree.grid(row=7, column=0, columnspan=2)
    teacher_tree.heading("ID", text="ID")
    teacher_tree.heading("TID", text="TID")
    teacher_tree.heading("Name", text="Name")
    teacher_tree.heading("Subject", text="Subject")
    teacher_tree.heading("Salary", text="Salary")

def add_teacher():
    tid = tid_entry.get()  # Get TID
    name = teacher_name_entry.get()
    subject = subject_entry.get()
    salary = salary_entry.get()

    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO teachers (TID, name, subject, salary) VALUES (?, ?, ?, ?)", (tid, name, subject, salary))
        conn.commit()
        messagebox.showinfo("Success", "Teacher added successfully.")
        view_teachers()  # Refresh the view
        clear_teacher_fields()  # Clear input fields
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "TID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

def clear_teacher_fields():
    tid_entry.delete(0, tk.END)
    teacher_name_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)

def delete_teacher(tid):
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE TID = ?", (tid,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Teacher deleted successfully.")
    view_teachers()  # Refresh the view

def view_teachers():
    for row in teacher_tree.get_children():
        teacher_tree.delete(row)  # Clear existing entries
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_id, TID, name, subject, salary FROM teachers")
    for row in cursor.fetchall():
        teacher_tree.insert("", "end", values=row)
    conn.close()

def search_teacher():
    tid = tid_entry.get()
    for row in teacher_tree.get_children():
        teacher_tree.delete(row)  # Clear existing entries
    conn = sqlite3.connect('school_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT teacher_id, TID, name, subject, salary FROM teachers WHERE TID = ?", (tid,))
    results = cursor.fetchall()
    for row in results:
        teacher_tree.insert("", "end", values=row)
    if not results:
        messagebox.showinfo("Info", "No teacher found with that TID.")
    conn.close()

# Password Check
def check_password():
    if password_entry.get() == SYSTEM_PASSWORD:
        login_frame.pack_forget()
        main_app()
    else:
        messagebox.showerror("Error", "Incorrect Password!")

# Application GUI
app = tk.Tk()
app.title("Login - School Management System")

# Login Frame
login_frame = tk.Frame(app)
login_frame.pack(pady=50)

tk.Label(login_frame, text="Enter Password:").grid(row=0, column=0)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=0, column=1)

tk.Button(login_frame, text="Login", command=check_password).grid(row=1, column=0, columnspan=2)

setup_database()  # Initialize database when app starts

app.mainloop()
