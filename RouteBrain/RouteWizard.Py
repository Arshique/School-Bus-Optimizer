import tkinter as tk
from tkinter import ttk , messagebox
import mysql.connector
import folium
import webbrowser
import math

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Bff=n&s<3",
        database="RouteDb"
    )

# ---------- Functions ----------
def distance(a, b):
    lat1, lon1 = float(a[1]), float(a[2])
    lat2, lon2 = float(b[1]), float(b[2])
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def optimize_route(stops, school):
    route, rem, cur = [school], stops.copy(), school
    while rem:
        nxt = min(rem, key=lambda s: distance(cur, s))
        route.append(nxt); rem.remove(nxt); cur = nxt
    route.append(school)
    return route

def logintodb(user, passw):
    if not user or not passw:
        messagebox.showwarning("Input Error", "Please enter both username and password")
        return

    db = get_connection()
    if not db:
        messagebox.showerror("Connection Error", "Failed to connect to the database")
        return

    try:
        cursor = db.cursor()
        query = "select * from Admin Where Adm_username=%s AND Adm_passw=%s"
        cursor.execute(query,(user,passw))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Login Successful", f"Welcome, {user}!")
            return True
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Database query failed:\n{err}")
    finally:
        cursor.close()
        db.close()

def submitact(Username, password):
    user = Username.get()
    passw = password.get()
    print(f"The name entered by you is {user} and password = {passw}")
    if logintodb(user, passw):
        adm_dashboard(user)

def show_tables(table_name):
    db = get_connection()
    if not db:
        print("Failed to connect to the database")
        return

    try:
        right_buttons_dict = {
        "Admin": ["Add Admin", "Edit Admin", "Delete Admin","Exit"],
        "Student": ["Add Student", "Edit Student", "Delete Student","Exit"],
        "Driver": ["Add Driver", "Edit Driver", "Remove Driver","Exit"],
        "Bus": ["Add Bus", "Edit Bus", "Assign Route", "Delete Bus","Exit"],
        "Route": ["Add Route", "Edit Route", "Optimize Route", "Delete Route","Exit"],
        "Stop": ["Add Stop", "Edit Stop", "Remove Stop","Exit"]
        }

        cursor = db.cursor()
        cursor.execute(f"Describe {table_name}")

        columns = [col[0] for col in cursor.fetchall()]

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        for widget in frame2.winfo_children():
            widget.destroy()

        table_frame = tk.Frame(frame2, bg="#1e1e1e")
        table_frame.pack(fill="both", expand=True)    

        tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        tree.pack(side="left", fill='both', expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=len(col)*20, anchor='center')

        for row in rows:
            tree.insert('', 'end', values=row)    

        for widget in right_frame.winfo_children():
            widget.destroy()

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')

        buttons_to_add = right_buttons_dict.get(table_name, [])
        for btn_text in buttons_to_add:
            btn = tk.Button(right_frame, text=btn_text, bg="#3a7ca5", fg="white", width=20, command=lambda t=btn_text: handle_action(t, tree, table_name, columns))
            btn.pack(pady=5, fill="x")
        
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Treeview", background="#1e1e1e", foreground="#b0b0b0", fieldbackground="#1e1e1e", font=("Segoe UI", 12))

        style.map("Treeview", background=[('selected', '#3a7ca5')], foreground=[('selected', 'white')])

        style.configure("Treeview.Heading", background="#3a7ca5", foreground="white", font=("Segoe UI", 12, "bold"))
        style.map("Treeview.Heading", background=[('active', '#357ABD')])

        tree.configure(style="Treeview" , yscrollcommand=vsb.set)

        
    except mysql.connector.Error as err:
        print(f"Database query failed: {err}")

    finally:
        cursor.close()
        db.close()

def start_inline_edit(tree, rowid, col_index, table_name, columns, next_column=False):
    
    if col_index >= len(columns):
        return

    if col_index == 0:
        if next_column:
            return start_inline_edit(tree, rowid, 1, table_name, columns, next_column=True)
        return

    col_id = f"#{col_index+1}"
    bbox = tree.bbox(rowid, col_id)
    if not bbox:
        return
    x, y, width, height = bbox
    old_value = tree.item(rowid, "values")[col_index]

    entry = tk.Entry(tree, font=("Segoe UI", 12))
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, old_value)
    entry.focus()

    def save_edit(event=None):
        new_value = entry.get()
        values = list(tree.item(rowid, "values"))
        values[col_index] = new_value
        tree.item(rowid, values=values)
        entry.destroy()

        pk_col = columns[0]
        pk_val = values[0]

        try:
            db = get_connection()
            cursor = db.cursor()
            update_col = columns[col_index]
            cursor.execute(f"UPDATE {table_name} SET {update_col}=%s WHERE {pk_col}=%s", (new_value, pk_val))
            db.commit()
            cursor.close()
            db.close()
        except Exception as e:
            print("DB update failed:", e)

        if next_column and col_index + 1 < len(columns):
            tree.after(50, lambda: start_inline_edit(tree, rowid, col_index + 1, table_name, columns, True))

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", save_edit)

def handle_action(action, tree, table_name, columns):
    sel = tree.selection()

    if action.startswith("Add"):
        try:
            db = get_connection()
            cursor = db.cursor()
            cursor.execute(f"DESCRIBE {table_name}")
            col_info = cursor.fetchall()

            insert_cols, insert_values = [], []

            fk_values = {}
            for field, ftype, null, key, default, extra in col_info:
                if "auto_increment" in extra.lower():
                    continue
                insert_cols.append(field)

                if "int" in ftype.lower() and ("id" in field.lower()):
                    
                    ref_table_query = f"""
                    SELECT REFERENCED_TABLE_NAME 
                    FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
                    WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='{table_name}' AND COLUMN_NAME='{field}'
                    """
                    cursor.execute(ref_table_query)
                    ref_table = cursor.fetchone()
                    if ref_table:
                        ref_table = ref_table[0]
                        
                        cursor.execute(f"SELECT {field} FROM {ref_table}")
                        parent_ids = [str(r[0]) for r in cursor.fetchall()]
                        
                        if parent_ids:
                            sel_window = tk.Toplevel()
                            sel_window.title(f"Select {field} for {table_name}")
                            sel_window.geometry("250x100")
                            tk.Label(sel_window, text=f"Select {field}").pack(pady=5)
                            var = tk.StringVar(sel_window)
                            var.set(parent_ids[0])
                            dropdown = tk.OptionMenu(sel_window, var, *parent_ids)
                            dropdown.pack(pady=5)

                            sel_done = tk.BooleanVar()
                            tk.Button(sel_window, text="OK", command=lambda: sel_done.set(True)).pack(pady=5)
                            sel_window.wait_variable(sel_done)
                            insert_values.append(int(var.get()))
                            sel_window.destroy()
                        else:
                            insert_values.append(None)
                    else:
                        insert_values.append(None)

                elif "enum" in ftype.lower():
                    first_val = ftype[ftype.find("(")+1:ftype.find(")")].split(",")[0].strip("'")
                    insert_values.append(first_val)

                elif "int" in ftype.lower():
                    insert_values.append(0)

                else:
                    insert_values.append("")

            placeholders = ", ".join(["%s"] * len(insert_values))
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(insert_cols)}) VALUES ({placeholders})", insert_values)
            db.commit()

            cursor.execute(f"SELECT * FROM {table_name} ORDER BY {col_info[0][0]} DESC LIMIT 1")
            new_row = cursor.fetchone()
            cursor.close()
            db.close()

            new_id = tree.insert('', 'end', values=new_row)
            start_inline_edit(tree, new_id, 1, table_name, [c[0] for c in col_info], next_column=True)

        except Exception as e:
            print("Add failed:", e)

    elif action.startswith("Edit"):
        if sel:
            row_id = sel[0]
            start_inline_edit(tree, row_id, 1, table_name, columns, next_column=True)
        else:
            messagebox.showwarning("Select row", "Please select a row to edit")

    elif action.startswith("Delete") or action.startswith("Remove"):
        if sel:
            values = tree.item(sel[0], "values")
            pk_val = values[0]
            try:
                db = get_connection()
                cursor = db.cursor()
                query = f"DELETE FROM {table_name} WHERE {columns[0]}=%s"
                cursor.execute(query, (pk_val,))
                db.commit()
                cursor.close()
                db.close()
                tree.delete(sel[0])
            except Exception as e:
                print("Delete failed:", e)
        else:
            messagebox.showwarning("Select row", "Please select a row to delete")

    elif action.startswith("Exit"):
        for widget in frame2.winfo_children():
            widget.destroy()
        for widget in right_frame.winfo_children():
            widget.destroy()

    elif action == "Assign Route":
        messagebox.showinfo("Info", "Assign Route functionality is not yet implemented.")

    elif action == "Optimize Route":
        try:
            db = get_connection()
            cursor = db.cursor()

            cursor.execute("Select Stp_name, Latitude, Longitude from Stop")
            rows = cursor.fetchall()
            stops = []
            for name, lat, lon in rows:
                try:
                    stops.append((name, float(lat), float(lon)))
                except ValueError:
                    print(f"Skipping invalid coordinates for stop: {name}")
            school= ("St.Arnold's School" , 22.2187296, 84.7791764)
            optimized = optimize_route(stops, school)
            m = folium.Map(location=[school[1], school[2]], zoom_start=13)
            folium.PolyLine([(s[1], s[2]) for s in optimized], color="blue", weight=3).add_to(m)
            for s in optimized:
                folium.Marker([s[1], s[2]], tooltip=s[0]).add_to(m)
            m.save("optimized_route.html")
            webbrowser.open("optimized_route.html")
            print("Optimized Route Order:") 
            for s in optimized:
                print(f" → {s[0]} ({s[1]}, {s[2]})")
            messagebox.showinfo("Route Optimized", "Check terminal for stop order!")
            
        except Exception as e:
            messagebox.showwarning("Optimize Route failed:", e)
#----------- GUI Setup ----------
def main():
    global root
    root = tk.Tk()
    root.geometry("500x400")
    root.title("Login Page - Route Wizard v1.0")
    root.configure(bg="#121212")
    root.resizable(False, False)

    frame = tk.Frame(root,bg="#121212")
    frame.place(relx =0.5, rely =0.5, anchor = "center")

    head = tk.Label(root, text ="Login to Route Wizard",fg="#3a7ca5",bg="#121212", font=("Segoe UI", 20 ,"bold"))
    head.place(relx=0.5, y= 30,anchor="n")

    lblfrstrow = tk.Label(frame, text ="Username",fg="#e0e0e0",bg="#121212", font=("Segoe UI", 14))
    lblfrstrow.pack(pady=(0,5))

    Username = tk.Entry(frame, width = 35,bg="#1e1e1e",fg="#b0b0b0",justify="center")
    Username.pack(pady=(0,15), ipady = 5, ipadx = 10)
 
    lblsecrow = tk.Label(frame, text ="Password",fg="#e0e0e0",bg="#121212",font=("Segoe UI", 14))
    lblsecrow.pack(pady=(0,5))

    password = tk.Entry(frame, width = 35,bg="#1e1e1e",fg="#b0b0b0",show="*",justify="center")
    password.pack(pady=(0,15), ipady = 5, ipadx = 10)

    submitbtn = tk.Button(frame, text ="Login", bg ='#3a7ca5',font=("Segoe UI", 14),fg="white" ,command =lambda: submitact(Username , password))
    submitbtn.pack(pady =10, ipadx = 10, ipady = 2)

    root.mainloop()

def adm_dashboard(user):
    root.destroy()
    global frame2 , right_frame

    dashboard = tk.Tk()
    dashboard.title("Admin Dashboard")
    dashboard.geometry("1366x768")
    dashboard.configure(bg="#121212")

    head = tk.Label(dashboard, text=f"Welcome {user}!!", fg="#3a7ca5", bg="#121212", font=("Segoe UI", 20, "bold"))
    head.pack(pady=20)

    frame = tk.Frame(dashboard,bg="#121212")
    frame.pack(pady=20)

    button_frame = tk.Frame(dashboard, bg="#121212")
    button_frame.pack(pady=10)

    buttons = [
    "Admin Management",
    "Student Management",
    "Driver Management",
    "Bus Management",
    "Route Management",
    "Stop Management"
    ]

    for i, text in enumerate(buttons):
        btn = tk.Button(button_frame, text=text, bg="#3a7ca5", fg="white",
                    font=("Segoe UI", 14), width=20, command=lambda t=text: show_tables(t.split()[0]))
        btn.grid(row=i//3, column=i%3, padx=50, pady=20)

    content_frame = tk.Frame(dashboard, bg="#121212")
    content_frame.pack(fill="both", expand=True, padx=20, pady=20)

    center_frame = tk.Frame(content_frame, bg="#1e1e1e")
    center_frame.pack()

    frame2 = tk.Frame(center_frame, bg="#1e1e1e", width=700, height=400)
    frame2.pack(side="left", padx=(20, 20), pady=20)

    right_frame = tk.Frame(center_frame, bg="#1e1e1e")
    right_frame.pack(side="left", padx=(20, 20), pady=20, anchor="n")

    dashboard.mainloop()

main()

