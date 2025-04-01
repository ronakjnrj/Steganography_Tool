import tkinter as tk
from tkinter import messagebox
import cv2
import sqlite3
from PIL import Image, ImageTk
import subprocess

# Create database if not exists
def create_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)
    conn.commit()
    conn.close()

# Signup function
def signup():
    # Remove login form and show signup form in the same window
    for widget in frame.winfo_children():
        widget.destroy()

    def register_user():
        new_username = entry_username_signup.get()
        new_password = entry_password_signup.get()

        if new_username == "" or new_password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration Successful")
            show_login()  # Return to login screen after signup
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    # Signup Form UI
    tk.Label(frame, text="Create Account", font=("Helvetica", 18, "bold"), bg="#7093c4", fg="white").pack(pady=10)
    tk.Label(frame, text="Username:", bg="#7093c4", fg="white", font=("Arial", 14)).pack()
    entry_username_signup = tk.Entry(frame, font=("Arial", 12), bd=3, relief=tk.SUNKEN)
    entry_username_signup.pack(pady=5)

    tk.Label(frame, text="Password:", bg="#7093c4", fg="white", font=("Arial", 14)).pack()
    entry_password_signup = tk.Entry(frame, show="*", font=("Arial", 12), bd=3, relief=tk.SUNKEN)
    entry_password_signup.pack(pady=5)

    tk.Button(frame, text="Sign Up", font=("Arial", 14), bg="green", fg="white", bd=3, command=register_user).place(relx=0.5, rely=0.7, anchor=tk.CENTER) 

    tk.Button(frame, text="Back to Login", font=("Helvetica", 12), bg="#7093c4", fg="black", activebackground="#7093c4", bd=0, command=show_login).place(relx=0.5, rely=0.84, anchor=tk.CENTER)

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Success", f"Welcome {username}")
        root.destroy()  # Close the login window
        subprocess.Popen(["python", "main.py"])  
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Function to display login form
def show_login():
    for widget in frame.winfo_children():
        widget.destroy()

    global entry_username, entry_password

    tk.Label(frame, text="Login", font=("Helvetica", 18, "bold"), bg="#7093c4", fg="white").pack(pady=10)
    tk.Label(frame, text="Username:", bg="#7093c4", fg="white", font=("Arial", 14)).pack()
    entry_username = tk.Entry(frame, font=("Arial", 12), bd=3, relief=tk.SUNKEN)
    entry_username.pack(pady=5)

    tk.Label(frame, text="Password:", bg="#7093c4", fg="white", font=("Arial", 14)).pack()
    entry_password = tk.Entry(frame, show="*", font=("Arial", 12), bd=3, relief=tk.SUNKEN)
    entry_password.pack(pady=5)

    tk.Label(frame, text="Don't Have an Account", bg="#7093c4", fg="white", font=("Century Gothic", 10)).pack(pady=(10, 0))
    tk.Button(frame, text="Signup", font=("Helvetica", 14), bg="#7093c4", fg="black", activebackground="#7093c4", bd=0, command=signup).pack(pady=2)

def capture_image():
    # Get entered username and password
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Username and Password cannot be empty!")
        return  # Stop execution if fields are empty

    # Check if the user exists in the database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        messagebox.showerror("Error", "Invalid credentials! Please enter a registered username and password.")
        return  # Stop execution if user is not found in the database

    # Proceed with capturing image only if the user exists
    _, frame = cap.read()
    cv2.imwrite("captured_image.jpg", frame)

    # Hide camera frame and "Authorize Face" button
    camera_frame.place_forget()
    button_capture.place_forget()

    # Show the login button
    button_login.place(relx=0.5, rely=0.40, anchor=tk.N)


# Show camera feed
def show_frame():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame to make it smaller (adjust width & height as needed)
    img = Image.fromarray(frame)
    img = img.resize((500, 373), Image.LANCZOS)  # Use LANCZOS for better quality

    imgtk = ImageTk.PhotoImage(image=img)
    camera_label.imgtk = imgtk
    camera_label.configure(image=imgtk)
    camera_label.after(10, show_frame)

# Initialize camera
cap = cv2.VideoCapture(0)
# create_db()

# Create main window
root = tk.Tk()
root.title("Login Page")
root.geometry("1270x800")
root.configure(bg="#7093c4")

# Frame for login/signup
frame = tk.Frame(root, bg="#7093c4", bd=0, relief=tk.RIDGE)
frame.place(relx=0.5, rely=0.05, anchor=tk.N, width=600, height=300)

# Frame for camera
camera_frame = tk.Frame(root, bg="#7093c4", bd=5, relief=tk.RIDGE)
camera_frame.place(relx=0.5, rely=0.39, anchor=tk.N, width=400, height=250)

camera_label = tk.Label(camera_frame, bg="#000000")
camera_label.pack(fill=tk.BOTH, expand=True)

# Capture  & Login button
button_login = tk.Button(root, text="Login", font=("Arial", 14), bg="green", width="15", fg="white", bd=3, command=login)
button_capture = tk.Button(root, text="Authorize Face", command=capture_image, font=("Arial", 14), bg="#0266bd", fg="white", bd=3)
button_capture.place(relx=0.5, rely=0.72, anchor=tk.N)

# Load login screen initially
show_login()

# Start the camera feed
show_frame()

# Run the Tkinter event loop
root.mainloop()

# Release the camera when the script exits
cap.release()
