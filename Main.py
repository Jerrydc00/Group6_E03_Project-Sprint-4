import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

def initialize_db():
    conn = sqlite3.connect("emergency_db.sqlite")
    cursor = conn.cursor()

    # Table for users (Username, Password, Address, Sex, Blood Type, Medical Conditions, Emergency Contacts)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            address TEXT,
            sex TEXT,
            bloodtype TEXT,
            medical_conditions TEXT,
            emergency_contact_person TEXT,
            emergency_contact_number TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS police_emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            emergency_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospital_emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            emergency_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fire_emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            emergency_type TEXT
        )
    """)

    conn.commit()
    conn.close()

initialize_db()


root = Tk()
root.title("NCR Emergency Response Chatbot")
root.geometry("1920x1080")
root.configure(bg="black")

#img = PhotoImage(file="aaaa.png")
#label = Label(root, image=img)
#label.pack()


global logged_in_user
logged_in_user = None

def login():
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x300")
    
    Label(login_window, text="Username:", font=("Times New Roman", 14)).pack(pady=5)
    username_entry = Entry(login_window, font=("Times New Roman", 14))
    username_entry.pack(pady=5)

    Label(login_window, text="Password:", font=("Times New Roman", 14)).pack(pady=5)
    password_entry = Entry(login_window, font=("Times New Roman", 14), show="*")
    password_entry.pack(pady=5)
    
    def verify_login():
        global logged_in_user
        username = username_entry.get()
        password = password_entry.get()
        conn = sqlite3.connect("emergency_db.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            logged_in_user = username
            login_window.destroy()
            setup_main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    Button(login_window, text="Login", font=("Times New Roman", 14), bg="gray", fg="white", command=verify_login).pack(pady=10)
    
    
def register():
    register_window = Toplevel(root)
    register_window.title("Register")
    register_window.geometry("400x600")

    Label(register_window, text="Username:", font=("Times New Roman", 14)).pack(pady=5)
    username_entry = Entry(register_window, font=("Times New Roman", 14))
    username_entry.pack(pady=5)

    Label(register_window, text="Password:", font=("Times New Roman", 14)).pack(pady=5)
    password_entry = Entry(register_window, font=("Times New Roman", 14), show="*")
    password_entry.pack(pady=5)

    Label(register_window, text="Address:", font=("Times New Roman", 14)).pack(pady=5)
    address_entry = Entry(register_window, font=("Times New Roman", 14))
    address_entry.pack(pady=5)

    Label(register_window, text="Sex (Male/Female):", font=("Times New Roman", 14)).pack(pady=5)
    sex_entry = Entry(register_window, font=("Times New Roman", 14))
    sex_entry.pack(pady=5)

    Label(register_window, text="Blood Type (A/B/O/AB):", font=("Times New Roman", 14)).pack(pady=5)
    bloodtype_entry = Entry(register_window, font=("Times New Roman", 14))
    bloodtype_entry.pack(pady=5)

    Label(register_window, text="Medical Conditions:", font=("Times New Roman", 14)).pack(pady=5)
    medical_conditions_entry = Entry(register_window, font=("Times New Roman", 14))
    medical_conditions_entry.pack(pady=5)

    Label(register_window, text="Emergency Contact Person:", font=("Times New Roman", 14)).pack(pady=5)
    emergency_contact_person_entry = Entry(register_window, font=("Times New Roman", 14))
    emergency_contact_person_entry.pack(pady=5)

    Label(register_window, text="Emergency Contact Number:", font=("Times New Roman", 14)).pack(pady=5)
    emergency_contact_number_entry = Entry(register_window, font=("Times New Roman", 14))
    emergency_contact_number_entry.pack(pady=5)

    def process_register():
        username = username_entry.get()
        password = password_entry.get()
        address = address_entry.get()
        sex = sex_entry.get()
        bloodtype = bloodtype_entry.get()
        medical_conditions = medical_conditions_entry.get()
        emergency_contact_person = emergency_contact_person_entry.get()
        emergency_contact_number = emergency_contact_number_entry.get()

        if all([username, password, address, sex, bloodtype, medical_conditions, emergency_contact_person, emergency_contact_number]):
            conn = sqlite3.connect("emergency_db.sqlite")
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (username, password, address, sex, bloodtype, medical_conditions, emergency_contact_person, emergency_contact_number) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (username, password, address, sex, bloodtype, medical_conditions, emergency_contact_person, emergency_contact_number))
                conn.commit()
                messagebox.showinfo("Registration Successful", "You can now log in.")
                register_window.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Registration Failed", "Username already exists.")
            conn.close()
        else:
            messagebox.showerror("Registration Failed", "All fields are required.")

    Button(register_window, text="Register", font=("Times New Roman", 14), bg="blue", fg="white", command=process_register).pack(pady=10)
