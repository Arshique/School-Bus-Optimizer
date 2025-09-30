import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # change if needed
        password="Bff=n&s<3", # your MySQL password
        database="SchlDb"
    )

# ---------- Functions ----------
# def add_student():
#     name = entry_name.get()
#     student_class = entry_class.get()
#     address = entry_address.get()
#     pickup_point = entry_pickup.get()
#     school_id = entry_school_id.get()

#     if not (name and student_class and address and pickup_point and school_id):
#         messagebox.showwarning("Input Error", "Please fill all fields")
#         return

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO students (name, student_class, address, pickup_point, school_id) VALUES (%s, %s, %s, %s, %s)",
#         (name, student_class, address, pickup_point, school_id)
#     )
#     conn.commit()
#     conn.close()

#     messagebox.showinfo("Success", "Student added successfully")
#     clear_entries()
#     show_students()


# def add_bus():
#     bus_no = entry_bus_no.get()
#     capacity = entry_capacity.get()
#     driver = entry_driver.get()
#     phone = entry_phone.get()

#     if not (bus_no and capacity):
#         messagebox.showwarning("Input Error", "Bus No and Capacity are required")
#         return

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO buses (bus_no, capacity, driver_name, phone) VALUES (%s, %s, %s, %s)",
#         (bus_no, capacity, driver, phone)
#     )
#     conn.commit()
#     conn.close()

#     messagebox.showinfo("Success", "Bus added successfully")
#     clear_entries()
#     show_buses()


# def add_school():
#     school_name = entry_school_name.get()
#     school_address = entry_school_address.get()

#     if not (school_name and school_address):
#         messagebox.showwarning("Input Error", "Please fill all fields")
#         return

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO schools (name, address) VALUES (%s, %s)",
#         (school_name, school_address)
#     )
#     conn.commit()
#     conn.close()

#     messagebox.showinfo("Success", "School added successfully")
#     clear_entries()
#     show_schools()


# def assign_student_bus():
#     student_id = entry_stud_id.get()
#     bus_id = entry_bus_id.get()

#     if not (student_id and bus_id):
#         messagebox.showwarning("Input Error", "Please enter Student ID and Bus ID")
#         return

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(
#         "INSERT INTO student_bus_allocation (student_id, bus_id) VALUES (%s, %s)",
#         (student_id, bus_id)
#     )
#     conn.commit()
#     conn.close()

#     messagebox.showinfo("Success", "Student assigned to bus successfully")
#     clear_entries()
#     show_allocations()


# # ---------- Show Data ----------
# def show_students():
#     for row in tree_students.get_children():
#         tree_students.delete(row)

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM students")
#     rows = cur.fetchall()
#     for row in rows:
#         tree_students.insert("", tk.END, values=row)
#     conn.close()


# def show_buses():
#     for row in tree_buses.get_children():
#         tree_buses.delete(row)

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM buses")
#     rows = cur.fetchall()
#     for row in rows:
#         tree_buses.insert("", tk.END, values=row)
#     conn.close()


# def show_schools():
#     for row in tree_schools.get_children():
#         tree_schools.delete(row)

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM schools")
#     rows = cur.fetchall()
#     for row in rows:
#         tree_schools.insert("", tk.END, values=row)
#     conn.close()


# def show_allocations():
#     for row in tree_allocations.get_children():
#         tree_allocations.delete(row)

#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("""SELECT a.id, s.name, b.bus_no
#                    FROM student_bus_allocation a
#                    JOIN students s ON a.student_id = s.id
#                    JOIN buses b ON a.bus_id = b.id""")
#     rows = cur.fetchall()
#     for row in rows:
#         tree_allocations.insert("", tk.END, values=row)
#     conn.close()


# def clear_entries():
#     for entry in (entry_name, entry_class, entry_address, entry_pickup, entry_school_id,
#                   entry_bus_no, entry_capacity, entry_driver, entry_phone,
#                   entry_school_name, entry_school_address, entry_stud_id, entry_bus_id):
#         entry.delete(0, tk.END)


# # ---------- Tkinter GUI ----------
# root = tk.Tk()
# root.title("🚍 School Bus Optimiser")
# root.geometry("1100x750")
# root.configure(bg="#f0f4f7")

# # ttk Style
# style = ttk.Style()
# style.theme_use("clam")
# style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#1e90ff", foreground="white")
# style.configure("Treeview", font=("Arial", 10), rowheight=25)
# style.configure("TButton", font=("Arial", 10, "bold"), padding=6, background="#1e90ff", foreground="black")

# notebook = ttk.Notebook(root)
# notebook.pack(fill="both", expand=True, padx=10, pady=10)

# # ---------- Students Tab ----------
# frame_students = ttk.Frame(notebook)
# notebook.add(frame_students, text="👩‍🎓 Students")

# tk.Label(frame_students, text="Add Student", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(pady=10)

# form_frame = tk.Frame(frame_students, bg="#f0f4f7")
# form_frame.pack()

# labels = ["Name", "Class", "Address", "Pickup Point", "School ID"]
# entries = []
# for i, text in enumerate(labels):
#     tk.Label(form_frame, text=text, font=("Arial", 11), bg="#f0f4f7").grid(row=i, column=0, sticky="e", padx=5, pady=5)
#     entry = tk.Entry(form_frame, width=30)
#     entry.grid(row=i, column=1, padx=5, pady=5)
#     entries.append(entry)

# entry_name, entry_class, entry_address, entry_pickup, entry_school_id = entries
# tk.Button(form_frame, text="Add Student", command=add_student, bg="#1e90ff", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

# tree_students = ttk.Treeview(frame_students, columns=("id", "name", "class", "address", "pickup", "school_id"), show="headings", height=10)
# for col in ("id", "name", "class", "address", "pickup", "school_id"):
#     tree_students.heading(col, text=col.capitalize())
# tree_students.pack(fill="x", padx=10, pady=10)
# show_students()


# # ---------- Buses Tab ----------
# frame_buses = ttk.Frame(notebook)
# notebook.add(frame_buses, text="🚌 Buses")

# tk.Label(frame_buses, text="Add Bus", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(pady=10)

# bus_frame = tk.Frame(frame_buses, bg="#f0f4f7")
# bus_frame.pack()

# bus_labels = ["Bus No", "Capacity", "Driver Name", "Phone"]
# bus_entries = []
# for i, text in enumerate(bus_labels):
#     tk.Label(bus_frame, text=text, font=("Arial", 11), bg="#f0f4f7").grid(row=i, column=0, sticky="e", padx=5, pady=5)
#     entry = tk.Entry(bus_frame, width=30)
#     entry.grid(row=i, column=1, padx=5, pady=5)
#     bus_entries.append(entry)

# entry_bus_no, entry_capacity, entry_driver, entry_phone = bus_entries
# tk.Button(bus_frame, text="Add Bus", command=add_bus, bg="#1e90ff", fg="white").grid(row=4, column=0, columnspan=2, pady=10)

# tree_buses = ttk.Treeview(frame_buses, columns=("id", "bus_no", "capacity", "driver", "phone"), show="headings", height=10)
# for col in ("id", "bus_no", "capacity", "driver", "phone"):
#     tree_buses.heading(col, text=col.capitalize())
# tree_buses.pack(fill="x", padx=10, pady=10)
# show_buses()


# # ---------- Schools Tab ----------
# frame_schools = ttk.Frame(notebook)
# notebook.add(frame_schools, text="🏫 Schools")

# tk.Label(frame_schools, text="Add School", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(pady=10)

# school_frame = tk.Frame(frame_schools, bg="#f0f4f7")
# school_frame.pack()

# tk.Label(school_frame, text="School Name", font=("Arial", 11), bg="#f0f4f7").grid(row=0, column=0, sticky="e", padx=5, pady=5)
# entry_school_name = tk.Entry(school_frame, width=30); entry_school_name.grid(row=0, column=1, padx=5, pady=5)

# tk.Label(school_frame, text="Address", font=("Arial", 11), bg="#f0f4f7").grid(row=1, column=0, sticky="e", padx=5, pady=5)
# entry_school_address = tk.Entry(school_frame, width=30); entry_school_address.grid(row=1, column=1, padx=5, pady=5)

# tk.Button(school_frame, text="Add School", command=add_school, bg="#1e90ff", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

# tree_schools = ttk.Treeview(frame_schools, columns=("id", "name", "address"), show="headings", height=10)
# for col in ("id", "name", "address"):
#     tree_schools.heading(col, text=col.capitalize())
# tree_schools.pack(fill="x", padx=10, pady=10)
# show_schools()


# # ---------- Allocation Tab ----------
# frame_allocation = ttk.Frame(notebook)
# notebook.add(frame_allocation, text="📌 Allocations")

# tk.Label(frame_allocation, text="Assign Student to Bus", font=("Arial", 14, "bold"), bg="#f0f4f7").pack(pady=10)

# alloc_frame = tk.Frame(frame_allocation, bg="#f0f4f7")
# alloc_frame.pack()

# tk.Label(alloc_frame, text="Student ID", font=("Arial", 11), bg="#f0f4f7").grid(row=0, column=0, sticky="e", padx=5, pady=5)
# entry_stud_id = tk.Entry(alloc_frame, width=30); entry_stud_id.grid(row=0, column=1, padx=5, pady=5)

# tk.Label(alloc_frame, text="Bus ID", font=("Arial", 11), bg="#f0f4f7").grid(row=1, column=0, sticky="e", padx=5, pady=5)
# entry_bus_id = tk.Entry(alloc_frame, width=30); entry_bus_id.grid(row=1, column=1, padx=5, pady=5)

# tk.Button(alloc_frame, text="Assign", command=assign_student_bus, bg="#1e90ff", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

# tree_allocations = ttk.Treeview(frame_allocation, columns=("id", "student", "bus"), show="headings", height=10)
# for col in ("id", "student", "bus"):
#     tree_allocations.heading(col, text=col.capitalize())
# tree_allocations.pack(fill="x", padx=10, pady=10)
# show_allocations()

# root.mainloop()
