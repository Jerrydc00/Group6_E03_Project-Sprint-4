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

def logout():
    global logged_in_user
    logged_in_user = None
    setup_main_screen() 

def return_to_main():
    for widget in root.winfo_children():
        widget.destroy()
    setup_main_screen()

def show_emergency_form(emergency_type):
    global logged_in_user

    # Clear previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Display the selected emergency type message
    Label(root, text=f"Welcome, you have chosen {emergency_type} Emergency", font=("Times New Roman", 30, "bold"), bg="lightgray").pack(pady=40)

    # Initialize the emergency types dropdown dynamically
    if emergency_type == "Police":
        emergency_values = [
            "Burglary", "Robbery", "Assault", "Theft", "Domestic Violence", "Kidnapping",
            "Missing Persons", "Traffic Accidents", "Drug-Related Incident", "Firearms Incident",
            "Homicide", "Vandalism", "Public Disturbance"
        ]
    elif emergency_type == "Hospital":
        emergency_values = [
            "General Emergency", "Cardiac Emergency", "Trauma Emergency", "Pediatric Emergency",
            "OB-GYN Emergency", "Poisoning", "COVID-19 or Infectious Disease", "Burn Injuries",
            "Choking", "Seizures", "Stroke", "Fractures", "Allergic Reactions", "Heat Stroke"
        ]
    else:  # Fire Emergency
        emergency_values = [
            "Fire Incident", "Gas Leak", "Electrical Fire", "Smoke Inhalation", "Explosion", 
            "Wildfire", "Rescue Operations", "Vehicle Fire", "Fireworks Accident", "Fire Hazards", 
            "Burn Injuries"
        ]

    # Emergency dropdown (Dynamic based on selected emergency type)
    emergency_dropdown = ttk.Combobox(root, values=emergency_values, state="readonly", width=68, font=("Times New Roman", 18))
    emergency_dropdown.pack(pady=10)
    emergency_dropdown.current(0)

    # User details (if logged in)
    if logged_in_user:
        conn = sqlite3.connect("emergency_db.sqlite")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT address, sex, bloodtype, medical_conditions, emergency_contact_person, emergency_contact_number 
            FROM users WHERE username = ?
        """, (logged_in_user,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            user_address, user_sex, user_bloodtype, user_medical_conditions, user_emergency_contact_person, user_contact_number = user_data
        else:
            user_address = user_sex = user_bloodtype = user_medical_conditions = user_emergency_contact_person = user_contact_number = "N/A"

        Label(root, text=f"Name: {logged_in_user}", font=("Times New Roman", 18), bg="lightgray").pack()
        Label(root, text=f"Address: {user_address}", font=("Times New Roman", 18), bg="lightgray").pack()
        Label(root, text=f"Sex: {user_sex}", font=("Times New Roman", 18), bg="lightgray").pack()
        Label(root, text=f"Blood Type: {user_bloodtype}", font=("Times New Roman", 18), bg="lightgray").pack()
        Label(root, text=f"Medical Conditions: {user_medical_conditions}", font=("Times New Roman", 18), bg="lightgray").pack()
        Label(root, text=f"Emergency Contact Person: {user_emergency_contact_person}", font=("Times New Roman", 18), bg="lightgray").pack()
        Label(root, text=f"Emergency Contact Number: {user_contact_number}", font=("Times New Roman", 18), bg="lightgray").pack()

    else:
        # User is not logged in, display input fields
        Label(root, text="Please fill up the boxes to send an authorized personnel to your location.", font=("Times New Roman", 20), bg="lightgray").pack(pady=20)

        Label(root, text="Name:", font=("Times New Roman", 18), bg="lightgray").pack()
        name_entry = Entry(root, width=70, font=("Times New Roman", 18))
        name_entry.pack(pady=10)

        Label(root, text="Address:", font=("Times New Roman", 18), bg="lightgray").pack()
        address_entry = Entry(root, width=70, font=("Times New Roman", 18))
        address_entry.pack(pady=10)

        Label(root, text="Emergency Contact Number:", font=("Times New Roman", 18), bg="lightgray").pack()
        contact_number_entry = Entry(root, width=70, font=("Times New Roman", 18))
        contact_number_entry.pack(pady=10)

    # Function to save the entered data to the database
    def save_to_db():
        global logged_in_user

        emergency_type_selected = emergency_dropdown.get()

        if logged_in_user:
            conn = sqlite3.connect("emergency_db.sqlite")
            cursor = conn.cursor()
            cursor.execute("SELECT address, emergency_contact_person, emergency_contact_number FROM users WHERE username = ?", (logged_in_user,))
            user_data = cursor.fetchone()
            conn.close()

            if not user_data:
                messagebox.showerror("Error", "User data not found.")
                return

            name = logged_in_user
            address = user_data[0]
            contact_person = user_data[1]
            contact_number = user_data[2] if user_data[2] != "" else "N/A"

        else:
            name = name_entry.get()
            address = address_entry.get()
            contact_number = contact_number_entry.get()
            contact_person = "N/A"  # Default if not logged in

            if not name or not address or not contact_number:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

        table_mapping = {
            "Police": "police_emergencies",
            "Hospital": "hospital_emergencies",
            "Fire": "fire_emergencies"
        }

        table_name = table_mapping.get(emergency_type)
        if not table_name:
            messagebox.showerror("Error", "Invalid emergency type.")
            return

        conn = sqlite3.connect("emergency_db.sqlite")
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO {table_name} (name, address, emergency_type) VALUES (?, ?, ?)", 
                       (name, address, emergency_type_selected))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"An authorized personnel is on the way!\n\nDetails:\nName: {name}\nAddress: {address}\nEmergency Type: {emergency_type_selected}\nContact Person: {contact_person}\nContact: {contact_number}")
        restart_program()

    Button(root, text="Submit", font=("Times New Roman", 18, "bold"), bg="green", fg="white", 
           width=20, height=2, command=save_to_db).pack(pady=40)
    Button(root, text="Go Back", font=("Times New Roman", 18, "bold"), bg="gray", fg="white", 
           width=20, height=2, command=restart_program).pack(pady=20)



def view_history(emergency_type):
    conn = sqlite3.connect("emergency_db.sqlite")
    cursor = conn.cursor()
    
    table_name = f"{emergency_type.lower()}_emergencies"
    cursor.execute(f"SELECT * FROM {table_name}")
    records = cursor.fetchall()
    conn.close()
    
    history_window = Toplevel(root)
    history_window.title(f"{emergency_type} Emergency History")
    history_window.geometry("800x600")
    
    text_area = Text(history_window, font=("Times New Roman", 14))
    text_area.pack(expand=True, fill=BOTH, padx=10, pady=10)
    
    for record in records:
        text_area.insert(END, f"ID: {record[0]}\nName: {record[1]}\nAddress: {record[2]}\nEmergency Type: {record[3]}\n{'-'*50}\n")

def restart_program():
    for widget in root.winfo_children():
        widget.destroy()
    setup_main_screen()


def setup_main_screen():
    # Create the main screen
    root.configure(bg="lightgray")

    Label(root, text="Welcome to the NCR Emergency Response Chatbot!", font=("Times New Roman", 28, "bold"), bg="lightgray").pack(pady=10)
    Label(root, text="How to use: Click on the type of emergency you are facing -> Provide the Information -> Submit",
          font=("Times New Roman", 20), bg="lightgray").pack()

    # Emergency Buttons
    Button(root, text="Police Emergency", font=("Times New Roman", 24, "bold"), width=70, height=5, fg='white', bg='red', command=lambda: show_emergency_form("Police")).pack(pady=30)
    Button(root, text="Hospital Emergency", font=("Times New Roman", 24, "bold"), width=70, height=5, fg='white', bg='blue', command=lambda: show_emergency_form("Hospital")).pack(pady=30)
    Button(root, text="Fire Emergency", font=("Times New Roman", 24, "bold"), width=70, height=5, fg='white', bg='orange', command=lambda: show_emergency_form("Fire")).pack(pady=30)

    Button(root, text="View Police Emergency History", font=("Times New Roman", 14), bg="gray", fg="white",
       width=30, height=2, command=lambda: view_history("police")).place(x=400, y=900)

    Button(root, text="View Hospital Emergency History", font=("Times New Roman", 14), bg="gray", fg="white",
       width=30, height=2, command=lambda: view_history("hospital")).place(x=800, y=900)  # Increased spacing

    Button(root, text="View Fire Emergency History", font=("Times New Roman", 14), bg="gray", fg="white",
       width=30, height=2, command=lambda: view_history("fire")).place(x=1200, y=900)  # Increased spacing
    if logged_in_user:
        Button(root, text="Logout", font=("Times New Roman", 14), bg="red", fg="white", width=30, command=logout).place(x=1550, y=10)
    else:
        Button(root, text="Login", font=("Times New Roman", 14), bg="gray", fg="white", width=15, command=login).place(x=1700, y=10)
        Button(root, text="Register", font=("Times New Roman", 14), bg="blue", fg="white", width=15, command=register).place(x=1550, y=10)

        
setup_main_screen()
root.mainloop()
