import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json

# Password Generator Function
def generate_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    length = simpledialog.askinteger("Password Length", "Enter password length:", minvalue=6, maxvalue=32)
    if length:
        password = "".join(random.choices(characters, k=length))
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

# Save Password Function
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if not website or not username or not password:
        messagebox.showwarning("Warning", "Please fill in all fields!")
        return
    
    data = {website: {"username": username, "password": password}}
    try:
        with open("passwords.json", "r") as file:
            stored_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        stored_data = {}
    
    stored_data.update(data)
    with open("passwords.json", "w") as file:
        json.dump(stored_data, file, indent=4)
    
    messagebox.showinfo("Success", "Password saved successfully!")
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Retrieve Password Function
def retrieve_password():
    website = simpledialog.askstring("Retrieve Password", "Enter website name:")
    try:
        with open("passwords.json", "r") as file:
            stored_data = json.load(file)
        if website in stored_data:
            username = stored_data[website]["username"]
            password = stored_data[website]["password"]
            messagebox.showinfo("Password Found", f"Username: {username}\nPassword: {password}")
        else:
            messagebox.showerror("Error", "No details found for this website.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No saved passwords found.")

# GUI Setup
root = tk.Tk()
root.title("Password Manager")
root.geometry("400x300")

# Labels and Entry Fields
tk.Label(root, text="Website:").pack()
website_entry = tk.Entry(root, width=40)
website_entry.pack()

tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root, width=40)
username_entry.pack()

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, width=40)
password_entry.pack()

# Buttons
tk.Button(root, text="Generate Password", command=generate_password).pack(pady=5)
tk.Button(root, text="Save Password", command=save_password).pack(pady=5)
tk.Button(root, text="Retrieve Password", command=retrieve_password).pack(pady=5)

root.mainloop()
