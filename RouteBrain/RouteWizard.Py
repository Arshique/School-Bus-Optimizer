import tkinter as tk
from tkinter import *
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
    if passw:
        db = get_connection()
        cursor = db.cursor()
    else:
        db = get_connection()
        cursor = db.cursor()

    savequery = "select * from Admin"
    try:
        cursor.execute(savequery)
        myresult = cursor.fetchall()
        for x in myresult:
            print(x)
        print("Query Executed successfully")
    except:
        db.rollback()
        print("Error occurred")

#----------- GUI Setup ----------

root = tk.Tk()
root.geometry("500x400")
root.title("Login Page - Route Wizard v1.0")
root.configure(bg="#121212")

frame = tk.Frame(root,bg="#121212")
frame .place(relx =0.5, rely =0.5, anchor = CENTER)

head = tk.Label(root, text ="Login to Route Wizard",fg="#4DD0E1",bg="#121212", font=("Arial", 20 ,"bold"))
head.place(x=100, y= 30)

lblfrstrow = tk.Label(frame, text ="Username",fg="#e0e0e0",bg="#121212", font=("Arial", 14))
lblfrstrow.pack(pady=(0,5))

Username = tk.Entry(frame, width = 35,bg="#1e1e1e",fg="#b0b0b0",justify= CENTER)
Username.pack(pady=(0,15), ipady = 5, ipadx = 10)
 
lblsecrow = tk.Label(frame, text ="Password",fg="#e0e0e0",bg="#121212",font=("Arial", 14))
lblsecrow.pack(pady=(0,5))

password = tk.Entry(frame, width = 35,bg="#1e1e1e",fg="#b0b0b0",show="*",justify= CENTER)
password.pack(pady=(0,15), ipady = 5, ipadx = 10)

submitbtn = tk.Button(frame, text ="Login", bg ='#4DD0E1',font=("Arial", 14),fg="white") #command = submitact)
submitbtn.pack(pady =10, ipadx = 10, ipady = 2)

root.mainloop()