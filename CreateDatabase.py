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

##Dropped specified columns stated in coursework specification
vendor_cols_to_drop = ['sunday_from_time1', 'sunday_to_time1', 'sunday_from_time2', 'sunday_to_time2',
                       'monday_from_time1', 'monday_to_time1', 'monday_from_time2', 'monday_to_time2',
                       'tuesday_from_time1', 'tuesday_to_time1', 'tuesday_from_time2', 'tuesday_to_time2',
                       'wednesday_from_time1', 'wednesday_to_time1', 'wednesday_from_time2', 'wednesday_to_time2',
                       'thursday_from_time1', 'thursday_to_time1', 'thursday_from_time2', 'thursday_to_time2',
                       'friday_from_time1', 'friday_to_time1', 'friday_from_time2', 'friday_to_time2',
                       'saturday_from_time1', 'saturday_to_time1', 'saturday_from_time2', 'saturday_to_time2']

vendors_tb = pd.read_csv("C://Users//ELISW//Desktop//COMP5000//Coursework//vendors.csv").drop(vendor_cols_to_drop, axis=1)

##Cleaning
##Renames the colums for consistency 
customer_colname = {'akeed_customer_id' : 'customer_id'}
customer_tb.rename(columns=customer_colname, inplace = True)

##Removes Duplicates so each id is unique
customer_tb.drop_duplicates(subset=['customer_id'], inplace = True)

##get unique vendor categories

unqiue_cat_vendors_tb = vendors_tb.drop_duplicates(subset=['vendor_category_id'])

## CREATE NEW TABLE THAT CONNCECTS LOCATION TO ORDER, USER_ID and LOCATIONNUM AS FK 




##CHOOSE HERE WHERE THE DB FILE IS READ FROM OR CREATED IF IT DOESNT EXIST
sql_name = "C://Users//ELISW//Desktop//COMP5000//Coursework//restaurant-delivery.db"

connection = sqlite3.connect(sql_name)
cursor = connection.cursor()

cursor.execute(""" DROP TABLE VENDOR""");

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

## got rid of, cityid, countryid, one_click, device_type, display_orders,commision rank redundent and all the same
## could come back to vendor_tags
create_vendor = """
 CREATE TABLE IF NOT EXISTS VENDOR(
     vendor_id int PRIMARY KEY,
     authentication_id int NOT NULL,
     latitude float NOT NULL,
     longitude float NOT NULL,
     vendor_category_id int NOT NULL,
     delivery_charge float NOT NULL,
     serving_distance int NOT NULL,
     is_open int NOT NULL,
     opening_time varchar(25),
     opening_time2 varchar(25),
     prepration_time int NOT NULL,
     discount int NOT NULL,
     status int NOT NULL,
     verified int NOT NULL,
     language varchr(3), 
     vendor_rating float NOT NULL,
     primary_tags varchar(70),
     vendor_tag varchar(20),
     vendor_tag_name varchar(200),
     created_at varchar(24) NOT NULL,
     updated_at varchar(24) NOT NULL,
     FOREIGN KEY(vendor_category_id) REFERENCES VENDOR_CAT(vendor_category_id)
     );
 """
create_vendorCat = """
 CREATE TABLE IF NOT EXISTS VENDOR_CAT(
     vendor_category_id int PRIMARY KEY,
     vendor_category varchar(50)
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

def populate_customer_func():
    count = 0
    for index, row in customer_tb.iterrows():
        
        populate_customer = """
        INSERT INTO CUSTOMERS(
         customer_id, gender, dob, status, verified, language, created_at, updated_at)
         VALUES (?,?,?,?,?,?,?,?);"""
         
        populate_customer_tuple =( row['customer_id'], row['gender'], row['dob'], row['status'],row['verified'], row['language'], row['created_at'],row['updated_at'] )
        cursor.execute(populate_customer, populate_customer_tuple)
        count += 1

def populate_vendor_cat_func():
     count = 0
     for index, row in unqiue_cat_vendors_tb.iterrows():
         
         populate_vendor_cat = """ 
         INSERT INTO VENDOR_CAT(
             vendor_category_id,vendor_category)
             VALUES (?, ?);"""
         populate_vendor_cat_tuple = (row['vendor_category_id'], row['vendor_category_en'])
         cursor.execute(populate_vendor_cat, populate_vendor_cat_tuple)
         count +=1

def populate_vendor_func():
    count = 0
    for index, row, in vendors_tb.iterrows():
        #21
        populate_vendors = """
        INSERT INTO VENDOR(
                 vendor_id,
     authentication_id,
     latitude,
     longitude,
     vendor_category_id,
     delivery_charge,
     serving_distance,
     is_open,
     opening_time,
     opening_time2,
     prepration_time,
     discount,
     status,
     verified,
     language, 
     vendor_rating,
     primary_tags,
     vendor_tag,
     vendor_tag_name,
     created_at,
     updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
        
        populate_vendor_tuple = (row['id'], row['authentication_id'], row['latitude'], row['longitude'], row['vendor_category_id'], row['delivery_charge'],	row['serving_distance'],
                                row['is_open'],	row['OpeningTime'],	row['OpeningTime2'], row['prepration_time'], row['discount_percentage'],	
                                row['status'], row['verified'],	row['language'], row['vendor_rating'], row['primary_tags'], row['vendor_tag'], row['vendor_tag_name'],
                                row['created_at'],row['updated_at'])
        cursor.execute(populate_vendors, populate_vendor_tuple)
        count +=1
                                                   


populate_vendor_func()
#populate_customer_func()
#populate_vendor_cat_func()




connection.commit()
connection.close()