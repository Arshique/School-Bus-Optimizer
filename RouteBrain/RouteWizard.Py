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
