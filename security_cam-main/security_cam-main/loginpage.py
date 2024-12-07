

import tkinter as tk
from tkinter import messagebox
import requests
import connectui 

def authenticate():
    
    username = username_entry.get()
    password = password_entry.get()

    
    try:
     auth_url = 'http://127.0.0.1:8000/api/auth/login/'
    except:
       messagebox.showinfo("Prompt", "An error occured")
        
    
    response = requests.post(auth_url, data={'username': username, 'password': password})

    
    if response.status_code == 200:
        token = response.json()['token']
        print(token)
        print(type(token))
        messagebox.showinfo("Prompt", "Authentication successful.")
        root.destroy()
        connect_window = connectui.Connect(token)
        connect_window.connect()
        
    else:
        messagebox.showinfo("Prompt", "Authentication failed")
        


root = tk.Tk()
root.title("Login Page")


username_label = tk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

password_label = tk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(root, text="Login", command=authenticate)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
