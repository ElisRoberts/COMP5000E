# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 16:32:54 2021

@author: ELISW
"""

import tkinter as tk
from tkinter import *
import sqlite3
import pandas as pd

##CHOOSE HERE WHERE THE DB FILE IS READ FROM OR CREATED IF IT DOESNT EXIST

sql_name = "C://Users//ELISW//Desktop//COMP5000//Coursework//restaurant-delivery.db"

connection = sqlite3.connect(sql_name)
cursor = connection.cursor()


connection.commit()
connection.close()


#Creates new window for adding new user
# def add_user_window():
#     add_user = Toplevel()
#     add_user.title("Add User")
#     add_user.geometry("400x400")    
#     gender_label = tk.label(add_user, text = "Gender", font = ('Ariel', 12), width= 12, anchor="l")
#     gender_label.grid(row = 0, column =1)
#     home_btn = Button(add_user, text = "Back", command=add_user.destroy)
#     home_btn.grid(row=1, column = 1)


def add_user_window():
    gender_opt = ["male", "female"]
    
    
    add_user = Toplevel()
    gender_var = StringVar(add_user)
    dob = StringVar()
    lang = StringVar()
    gender = StringVar()
    gender_var.set(gender_opt[0])
    add_user.title("Add User")
    add_user.geometry("400x110")
    
    
    l_gen = tk.Label(add_user, text = "Gender:", font = ('Ariel', 12), width = 20)
    l_gen.grid(row = 0, column = 1)
    
    gender_drop = OptionMenu(add_user, gender_var, *gender_opt)
    gender_drop.config(width = 20)
    gender_drop.grid(row = 0, column = 2)
    
    l_dob = tk.Label(add_user, text = "Year of Birth (e.g. 2005):", font = ('Ariel', 12), width = 20)
    l_dob.grid(row = 1, column = 1)
    t_dob = tk.Entry(add_user)
    t_dob.grid(row =1, column =2 )
    
    l_lang = tk.Label(add_user, text = "Language (Max 3 Chars)",font = ('Ariel', 12), width = 20)
    l_lang.grid(row =2, column = 1)
    t_lang = tk.Entry(add_user)
    t_lang.grid(row = 2, column = 2) 
    
    save_btn = Button(add_user, text = "Save",font = ('Ariel', 10), width = 5
                      , anchor ="e")
    save_btn.grid(row = 3, column = 1)
    
    home_btn = Button(add_user, text = "Back", command=add_user.destroy , font = ('Ariel', 10), width = 5, anchor = "w")
    home_btn.grid(row=3, column = 0)
    
    








# 
Home = tk.Tk()
Home.geometry("400x250")
Home.title("Food Delivery Database GUI")

l1 = tk.Label(Home, text = "Please make selection", font =('Ariel', 20), width = 25
              , anchor ="c" )
l1.grid(row=1,column=1,columnspan=1) 

new_user_btn = Button(Home, text = "Add New User", command = add_user_window, font = ('Ariel', 20), width = 20)
new_user_btn.grid(row=2,column=1,columnspan=1) 



print_means_btn = Button(Home, text = "Show Means", font = ('Ariel', 20), width = 20)
print_means_btn.grid(row=3,column=1,columnspan=1)

plot_hist_btn = Button(Home, text = "Plot Histogram", font = ('Ariel', 20), width = 20)
plot_hist_btn.grid(row=4,column=1,columnspan=1)

Home.mainloop()