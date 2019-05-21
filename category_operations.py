# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 09:49:20 2018

@author: Kamalakanta
"""
import wikipedia as wiki
import db_operations as dbo
import datetime
import re
import schedule as sc

def timeOfDay():
   dt = datetime.datetime.now()
   if dt.time() > datetime.time(4) and dt.time() <= datetime.time(12):
       return "Morning"
   elif dt.time() > datetime.time(12) and dt.time() <= datetime.time(17):
       return "Afternoon"
   else:
      return "Evening"

def sayAndWrite(engine, text):
    print(text)
    if engine is not None:
        engine.say(text)
        engine.runAndWait()

def sayIt(engine, text):
    if engine is not None:
        engine.say(text)
        engine.runAndWait()

def perform_Cat0n1_ops(engine, spoken_text):
    text = "You said "+spoken_text +" and this is a statement"
    sayAndWrite(engine, text)
    sayAndWrite(engine, "I'm sorry. I don't have enough training data to respond to normal conversations")

def perform_Cat2_ops(category, engine, spoken_text):
    sayAndWrite(engine, "You said "+spoken_text+" and this is a way of ending conversation")
    message = dbo.fetch_dialog_for_intent(category)
    sayAndWrite(engine, message)
    
def perform_Cat3_ops(category, engine, spoken_text):
    sayAndWrite(engine, "You said "+spoken_text+" and this is a way of greeting others")
    message = dbo.fetch_dialog_for_intent(category)
    message = str(message).format(timeOfDay())
    sayAndWrite(engine, message)
        
def perform_Cat4_ops(engine, client, spoken_text):
    sayAndWrite(engine, "You asked "+spoken_text+" and this is a question")
    sayAndWrite(engine, "Please wait till I find a suitable answer for you")
    if('name' in spoken_text):
        sayAndWrite(engine, "My name is Alice")
        return
    try:
        raw_answer = client.query(spoken_text)
        answer = next(raw_answer.results).text
        print(answer)
        sayIt(engine, answer)
    except:
        try:
            answer = wiki.summary(spoken_text,3)
            print(answer)
            sayIt(engine, answer)
        except:
            text = "I can't answer your question. Please rephrase it"
            print(text)
            sayIt(engine, text)               

def setAlarm(engine):
    print("Dear User ... You have asked me to remind you now to do a task.")
    sayIt(engine,"Dear User ... You have asked me to remind you now to do a task.")

def schedule_task(engine, hour, minute):
    sc.every().day.at('{}:{}'.format(hour,minute)).do(setAlarm, engine)
 
def perform_Cat5_ops(engine, spoken_text):
    sayAndWrite(engine, "You said "+spoken_text+" and this belongs to reminder category")
    try:
        match = re.search(r'\d{2}:\d{2}', spoken_text)
        date = datetime.datetime.strptime(match.group() , '%H:%M')
        schedule_task(engine, date.hour,date.minute)
        sayAndWrite(engine, "Task scheduled at {}:{}".format(date.hour,date.minute))
    except Exception as e:
        print("Exception occured while scheduling task")
    
def perform_category_operations(category, engine, client, spoken_text):
    
    if category == 0 or category == 1:
        perform_Cat0n1_ops(engine, spoken_text)
    elif category == 2:
        perform_Cat2_ops(category, engine, spoken_text)
    elif category == 3:
        print(category)
        perform_Cat3_ops(category, engine, spoken_text)
    elif category == 4:
        perform_Cat4_ops(engine, client, spoken_text)
    elif category == 5:
        perform_Cat5_ops(engine, spoken_text)
        
timeOfDay()

class Engine:
    def say(self, text):
        print()
    def runAndWait(self):
        print() 
        