# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:46:56 2021

@author: ELISW
"""




import sqlite3
import pandas as pd



customer_tb = pd.read_csv("C://Users//ELISW//Desktop//COMP5000//Coursework//train_customers.csv")
location_tb = pd.read_csv("C://Users//ELISW//Desktop//COMP5000//Coursework//train_locations.csv")
orders_tb = pd.read_csv("C://Users//ELISW//Desktop//COMP5000//Coursework//orders.csv")


vendor_cols_to_drop = ['sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2',
                       'monday_from_time1', 'monday_to_time1', 'monday_from_time2', 'monday_to_time2',
                       'tuesday_from_time1', 'tuesday_to_time1', 'tuesday_from_time2', 'tuesday_to_time2',
                       'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2', 'wednesday_to_time2',
                       'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
                       'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2',
                       'saturday_from_time1', 'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2']

vendors_tb = pd.read_csv("C://Users//ELISW//Desktop//COMP5000//Coursework//vendors.csv").drop(vendor_cols_to_drop, axis=1)

customer_colname = {'akeed_customer_id' : 'customer_id'}

customer_tb.rename(columns=customer_colname, inplace = True)

sql_name = "restaurant-delivery.db"

connection = sqlite3.connect(sql_name)
cursor = connection.cursor()

cursor.execute(""" DROP TABLE CUSTOMERS""");

create_customer = """
 CREATE TABLE IF NOT EXISTS CUSTOMERS(                         
    customer_id varchar(7) PRIMARY KEY,
    gender varchar(20),
    dob int,
    status int NOT NULL,
    verified int NOT NULL,
    language varchar(3),
    created_at varchar(24) NOT NULL,
    updated_at varchar(24) NOT NULL    
    );
"""
create_vendor = """
 CREATE TABLE IF NOT EXISTS VENDOR(
     vendor_id int PRIMARY KEY,
     authentication_id int NOT NULL,
     latitude float NOT NULL,
     longitude float NOT NULL,
     delivery_charge float NOT NULL,
     serving_distance int NOT NULL,
     opening_time varchar(25) NOT NULL,
     opening_time2 varchar(25) NOT NULL,
     commission int NOT NULL,
     discount int NOT NULL,
     status int NOT NULL,
     verified int NOT NULL,
     language varchr(3), 
     vndor_rating float NOT NULL,
     primary_tags varchar(70),
     open_close int NOT NULL,
     vendor_tag varchar(20) NOT NULL,
     vendor_tag_name varchar(200) NOT NULL,
     one_click int NOT NULL,
     country_id NOT NULL,
     city_id NOT NULL,
     created_at varchar(24) NOT NULL,
     updated_at varchar(24) NOT NULL,
     device_type int NOT NULL,
     display_orders int NOT NULL
     );
 """
create_vendorCat = """
 CREATE TABLE IF NOT EXISTS VENDOR_CAT(
     vendor_catagory_id int PRIMARY KEY,
     vendor_id int NOT NULL,
     vendor_catagory varchar(50),
     FOREIGN KEY(vendor_id) REFERENCES VENDOR(vendor_id)
     );
 """
 
create_locations = """
 CREATE TABLE IF NOT EXISTS LOCATION(
    location_id int PRIMARY KEY,
    customer_id varchar(7) NOT NULL,
    location_number int NOT NULL,
    location_type varchar(14),
    latitude float NOT NULL,
    longitude float NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id)
    );
 """
 ##NOT 100% sure on how to do location, location ID is here for trial basis
create_orders = """
 CREATE TABLE IF NOT EXISTS ORDERS(
     order_id int PRIMARY KEY,
     customer_id varchar(7) NOT NULL,
     item_count int NOT NULL,
     grand_total float NOT NULL,
     payment_mode int NOT NULL,
     promo_code varchar(100),
     vendor_discount_amount int NOT NULL,
     promo_code_discount_percent int,
     is_favourite varchar(3),
     is_rated varchar(3),
     vendor_rating int,
     driver_rating int,
     devliery_distance int NOT NULL,
     preperation_time int,
     order_accept_time varchar(24),
     driver_accept_time verchar(24),
     ready_for_pickup_time varchar(24),
     picked_up_time varchar(24),
     delivered_time varchar(24),
     delviery_date varchar(24),
     vendor_id int NOT NULL,
     created_at varchar(24) NOT NULL,
     location_id int NOT NULL, 
     FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id),
     FOREIGN KEY(vendor_id) REFERENCES VENDOR(vendor_id)
     FOREIGN KEY(location_id) REFERENCES LOCATION(location_id)
     );
"""


cursor.execute(create_customer)
cursor.execute(create_vendor)
cursor.execute(create_vendorCat)
cursor.execute(create_locations)
cursor.execute(create_orders)

count = 0
for index, row in customer_tb.iterrows():
    
    populate_customer = """
    INSERT INTO CUSTOMERS(
     customer_id, gender, dob, status, verified, language, created_at, updated_at)
     VALUES (?,?,?,?,?,?,?,?);"""
     
    populate_customer_tuple =( row['customer_id'], row['gender'], row['dob'], row['status'],row['verified'], row['language'], row['created_at'],row['updated_at'] )
    cursor.execute(populate_customer, populate_customer_tuple)
    count += 1



connection.commit()
connection.close()