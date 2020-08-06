#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox

#data
users = {'test':'supersecure'}

#Gui
window = tk.Tk()
window.title("Login form")
window.geometry('300x150')

#Variables
username, password = tk.StringVar(), tk.StringVar()
trials_left = 3

#Functions
def login(*args):
    global trials_left
    trials_left -= 1
    if trials_left == 0:
        window.quit()
    if username.get() not in users:
        messagebox.showerror('Denied','Incorrect username')
        return None
    if users[username.get()] != password.get():
       messagebox.showerror('Denied','Incorrect password')
       return None
    messagebox.showinfo('Granted','Login sucessful')


def clear():
    user_ety.delete(0, 'end')
    pass_ety.delete(0, 'end')
    user_ety.focus_set()

#Design
user_lbl = tk.Label(window, text = "Username")
user_lbl.grid(row = 0,column = 0, padx = 5, pady = 8)
pass_lbl = tk.Label(window, text = "Password")
pass_lbl.grid(row = 1,column = 0, padx = 5, pady = 8)
user_ety = tk.Entry(window, textvariable = username)
user_ety.grid(row = 0, column = 1, padx = 5, pady = 8)
pass_ety = tk.Entry(window, textvariable = password, show = '*')
pass_ety.grid(row = 1, column = 1, padx = 5, pady = 8)
login_btn = tk.Button(window, text = 'Login', command = login)
login_btn.grid(row = 2, column = 0, padx = 5, pady = 8)
clear_btn = tk.Button(window, text = 'Clear', command = clear)
clear_btn.grid(row = 2, column = 1, padx = 5, pady = 8)

#Event handling
user_ety.focus_set()
user_ety.bind('<Return>', lambda x : pass_ety.focus_set())
pass_ety.bind('<Return>', login)

#start
window.mainloop()
