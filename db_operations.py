# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 21:50:08 2018

@author: Kamalakanta
"""

import sqlite3
import random


connection = sqlite3.connect('chatbot.db')
cur = connection.cursor()

def insert_data_into_post_class_structure(categories):
    for i in range(len(categories)):
        insert_sql = """insert into post_class_structure (post_class, post_class_num) values ("{}", {});""".format(categories[i], i)
        try:
            cur.execute(insert_sql)
        except Exception as e:
            print(e)
    connection.commit()   

def insert_data_into_post_text(content, class_num): 
    try:
        insert_sql = """insert into classification_data (post_text, post_class_num, active) values ("{}", {}, 'Y');""".format(content, class_num)
        cur.execute(insert_sql)
        connection.commit() 
    except Exception as e:
        print(e)
    
def fetch_post_texts():
    cur.execute("select post_text from classification_data where active = 'Y' ")
    result = cur.fetchall()
    posts_text = []
    for i in result:
        posts_text.append(i[0]) 
    return posts_text

def fetch_post_class_num():
    cur.execute("select post_class_num from classification_data where active = 'Y' ")
    result = cur.fetchall()
    posts_class_num = []
    for i in result:
        posts_class_num.append(i[0]) 
    return posts_class_num

def fetch_dialog_for_intent(intent_type):
    cur.execute("select message from Dialog where intent_type = {}".format(intent_type))
    result = cur.fetchall()
    messages = []
    for i in result:
        messages.append(i[0])
    message = messages[random.choice(range(len(messages))) - 1]   
    return message

def store_training_data(content, statement_category):
    try:
        insert_sql = """insert into training_session_data (post_text, post_class_num) values ("{}", {});""".format(content, statement_category)
        cur.execute(insert_sql)
        connection.commit() 
    except Exception as e:
        print(e)
        
def clear_training_session_data():
    try:
        delete_sql = "delete from training_session_data"
        cur.execute(delete_sql)
        connection.commit() 
    except Exception as e:
        print(e)
    

def fetch_training_data():
    cur.execute("select post_text from training_session_data ")
    result = cur.fetchall()
    messages = ""
    for i in result:
        messages = messages + " "+ str(i[0])
    return messages
