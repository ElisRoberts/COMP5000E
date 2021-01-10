# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 16:32:54 2021

@author: ELISW
"""
#Libraries 
import tkinter as tk
from tkinter import *
import sqlite3
import uuid
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure

##CHOOSE HERE WHERE THE DB FILE IS READ

sql_name = "C://Users//ELISW//Desktop//COMP5000//Coursework//restaurant-delivery.db"



     #Function that saves the new user to the database
def save_user():
    
    
       verified = 1
       status = 1 #Fields that need to be filled in the db
       created_at = datetime.now() #User for the user creating/update time
       user_id = uuid.uuid4().hex[:7].upper() #Randomly generates User_id out of letters and numbers
       input_dob = dob.get() #Gets the data inputed in the input window
       input_lang = lang.get()
       input_gender = gender_var.get()
       
       connection = sqlite3.connect(sql_name)
       cursor= connection.cursor()
       add_data = """INSERT INTO CUSTOMERS(customer_id, gender, dob, status, verified, language, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?);"""    
       add_data_tupple = (user_id, input_gender, input_dob, status,
                           verified, input_lang, created_at, created_at)
       cursor.execute(add_data, add_data_tupple)     #Adds the new user details into the database
       connection.commit()
       connection.close()
       
       
       saved = Toplevel() #Messagebox pops up to say user has been saved
       saved.title("User Saved")
       saved.geometry("100x50")
       l_sv = tk.Label(saved, text = "User Succesfully Saved", font = ('Ariel, 8'), width = 20).pack()
       ok_btn = Button(saved, text = "OK", command=saved.destroy , font = ('Ariel', 8), width = 8, anchor = "c").pack()

#function that created the add user window    
def add_user_window():
        gender_opt = ["male", "female"] #Gender options for the dropdown list
        
        global dob
        global lang #variables set to global so they can be used in the save_user function
        global gender_var
        global status
        add_user = Toplevel() #Creates new window
        gender_var = StringVar(add_user)
        dob = StringVar()
        lang = StringVar()
        gender = StringVar() #Creates variable strings that what is entered into the text box gets saved for the user
        status = StringVar()
    
        gender_var.set(gender_opt[0])
        add_user.title("Add User")
        add_user.geometry("400x115")
        
        
        l_gen = tk.Label(add_user, text = "Gender:", font = ('Ariel', 12), width = 20) #Drop list for gender
        l_gen.grid(row = 0, column = 1)
        
        gender_drop = OptionMenu(add_user, gender_var, *gender_opt)
        gender_drop.config(width = 20)
        gender_drop.grid(row = 0, column = 2)
        
        l_dob = tk.Label(add_user, text = "Year of Birth (e.g. 2005):", font = ('Ariel', 12), width = 20)
        l_dob.grid(row = 1, column = 1)
        t_dob = tk.Entry(add_user, textvariable = dob) #Textbox for DoB
        t_dob.grid(row =1, column =2 )
        
        l_lang = tk.Label(add_user, text = "Language (Max 3 Chars)",font = ('Ariel', 12), width = 20)
        l_lang.grid(row =2, column = 1)
        t_lang = tk.Entry(add_user, textvariable = lang)  #Textbox for language
        t_lang.grid(row = 2, column = 2) 
        
        save_btn = Button(add_user, text = "Save", command = save_user, font = ('Ariel', 10), width = 5 #Save button that runs the save_user function
                          , anchor ="e")
        save_btn.grid(row = 3, column = 2)
        l_status = tk.Label(add_user,text = "", textvariable = status, font = ('Ariel', 12), width = 20,  anchor ="e")
        l_status.grid(row=4, column=2)
        
        home_btn = Button(add_user, text = "Back", command=add_user.destroy , font = ('Ariel', 10), width = 5, anchor = "w") #takes back to home page
        home_btn.grid(row=3, column = 0)
        
#Function that gets the means requested in the specs
def mean_window():
    item_mean = StringVar()
    cost_mean = StringVar() # Varibales that the query results get placed in
    mean_win = Toplevel() # Creates new window
    mean_win.title("Means")
    mean_win.geometry("400x150")
    
    connection = sqlite3.connect(sql_name)
    cursor= connection.cursor()
    
    cursor.execute("""SELECT AVG(item_count) FROM ORDERS""") #queries for the avg item count
    item_mean = cursor.fetchone() #stored the query result in variable
    
    cursor.execute("""SELECT AVG(grand_total) FROM ORDERS""") #queries for the avg total 
    cost_mean = cursor.fetchone() # stored the query result in variable
    connection.commit()
    connection.close()

    
    

    l_item = tk.Label(mean_win, text = "The mean of number of items purchesed: " , font = ('Ariel', 12), width = 40, anchor = "c").grid(row=1,column=1)
    l_item_out = tk.Label(mean_win, text = item_mean, font = ('Ariel', 12), width = 40, anchor = "c").grid(row=2,column=1) #shows the content of the variable to string
    
    l_total = tk.Label(mean_win, text = "The mean of number of grand total cost: " , font = ('Ariel', 12), width = 40, anchor = "c").grid(row=3,column=1)
    l_total_out = tk.Label(mean_win, text = cost_mean,  font = ('Ariel', 12), width = 40, anchor = "c").grid(row=4,column=1) #shows the content of the variable to string
    
    home_btn = Button(mean_win, text = "Back", command=mean_win.destroy , font = ('Ariel', 10), width = 5, anchor = "c")
    home_btn.grid(row=5, column = 1)
  
#Function that displays the histograph
def hist_window():

    connection = sqlite3.connect(sql_name)
    cursor= connection.cursor()
    
    #cursor.execute("""SELECT devliery_distance, count(devliery_distance) FROM ORDERS GROUP BY devliery_distance""")
    sql_query = ("""SELECT devliery_distance FROM ORDERS""") #query that get the data required for the histograph

    df = pd.read_sql(sql_query, connection)
    connection.commit()
    connection.close()
    
    
 
    df = df.hist(bins = 20, ylim=(0,1))# stores the graph to df
    
    f = Figure(figsize=()(5,5), dpi= 100)
    a = f.add_subplot(111) #set up for the graph page
    
    a.Plot(df) # plots/shows the graph as another window
    

#Home GUI
Home = tk.Tk()
Home.geometry("400x250")
Home.title("Food Delivery Database GUI")
    
l1 = tk.Label(Home, text = "Please make selection", font =('Ariel', 20), width = 25
                  , anchor ="c" )
l1.grid(row=1,column=1,columnspan=1) 
    
new_user_btn = Button(Home, text = "Add New User", command = add_user_window, font = ('Ariel', 20), width = 20) #Button that runs the add_user_window function
new_user_btn.grid(row=2,column=1,columnspan=1) 
    
    
    
print_means_btn = Button(Home, text = "Show Means", command = mean_window, font = ('Ariel', 20), width = 20) #Button that runs the mean_window function
print_means_btn.grid(row=3,column=1,columnspan=1)
    
plot_hist_btn = Button(Home, text = "Plot Histogram",command = hist_window ,font = ('Ariel', 20), width = 20) #Button that runs the hist_window function
plot_hist_btn.grid(row=4,column=1,columnspan=1)

    
Home.mainloop()