import tkinter as tk
from tkinter import messagebox
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
def logintodb(user, passw):
    if not user or not passw:
        messagebox.showwarning("Input Error", "Please enter both username and password")
        return

    db = get_connection()
    if not db:
        return

    try:
        cursor = db.cursor()
        query = "select * from Admin Where Adm_username=%s AND Adm_passw=%s"
        cursor.execute(query,(user,passw))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Login Successful", f"Welcome, {user}!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
    except mysql.connector.Error as err:
        messagebox.showerror("Query Error", f"Database query failed:\n{err}")
    finally:
        cursor.close()
        db.close()

def submitact(Username, password):
    user = Username.get()
    passw = password.get()
    print(f"The name entered by you is {user} {passw}")
    logintodb(user, passw)
#----------- GUI Setup ----------
def main():
    root = tk.Tk()
    root.geometry("500x400")
    root.title("Login Page - Route Wizard v1.0")
    root.configure(bg="#121212")
    root.resizable(False, False)

    frame = tk.Frame(root,bg="#121212")
    frame .place(relx =0.5, rely =0.5, anchor = "center")

    head = tk.Label(root, text ="Login to Route Wizard",fg="#3a7ca5",bg="#121212", font=("Arial", 20 ,"bold"))
    head.place(relx=0.5, y= 30,anchor="n")

    lblfrstrow = tk.Label(frame, text ="Username",fg="#e0e0e0",bg="#121212", font=("Arial", 14))
    lblfrstrow.pack(pady=(0,5))

    Username = tk.Entry(frame, width = 35,bg="#1e1e1e",fg="#b0b0b0",justify="center")
    Username.pack(pady=(0,15), ipady = 5, ipadx = 10)
 
    lblsecrow = tk.Label(frame, text ="Password",fg="#e0e0e0",bg="#121212",font=("Arial", 14))
    lblsecrow.pack(pady=(0,5))

    password = tk.Entry(frame, width = 35,bg="#1e1e1e",fg="#b0b0b0",show="*",justify="center")
    password.pack(pady=(0,15), ipady = 5, ipadx = 10)

    submitbtn = tk.Button(frame, text ="Login", bg ='#3a7ca5',font=("Arial", 14),fg="white" ,command =lambda: submitact(Username , password))
    submitbtn.pack(pady =10, ipadx = 10, ipady = 2)

    root.mainloop()
main()