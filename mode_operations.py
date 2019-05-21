# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 23:12:09 2018

@author: Kamalakanta
"""
import db_operations as dbo
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

def sayAndWrite(engine, text):
    print(text)
    if engine is not None:
        engine.say(text)
        engine.runAndWait()

def activateMode(voice, requested_mode):
    text = "{} mode activated".format(requested_mode)
    sayAndWrite(voice, text)
    return requested_mode

def record_conversation(content, statement_category):
    dbo.store_training_data(content, statement_category)

def show_stastistics():
    stop_words = set(stopwords.words("english"))
    content = dbo.fetch_training_data()
    words = word_tokenize(content)
    filtered_content = []
    for w in words:
        if w not in stop_words:
            filtered_content.append(w)     
    return nltk.FreqDist(filtered_content).most_common(10)

def activateRequestedMode(content, current_mode, voice):
    mode = ""
    if('smart' in content):
        mode = activateMode(voice, "smart")
    elif('train' in content):
        mode = activateMode(voice, "training")
    elif('standard' in content):
        activateMode(voice, "standard")
    else:
        sayAndWrite(voice, "Could not find such a mode. Please try again")
        return False
    return mode
    
def perform_extra_mode_operations(current_mode, statement_category, engine, client, inp):
    if(current_mode == 'training'):
        if(statement_category == 4):
            sayAndWrite(engine, "You asked me a question. Am I correct?")
            inp = input("yes or no ")
            print(inp)
            sayAndWrite(engine, "Thank you for helping me improve")
        if(statement_category == 3):
            sayAndWrite(engine, "You greeted me. Am I correct?")
            inp = input("yes or no ")
            print(inp)
            sayAndWrite(engine, "Thank you for helping me improve")
        if(statement_category == 2):
            sayAndWrite(engine, "You want to end the conversation. Am I correct?")
            inp = input("yes or no ")
            print(inp)
            sayAndWrite(engine, "Thank you for helping me improve")
    if(current_mode == 'smart'):
        record_conversation(inp, statement_category)
        if 'statistics' in inp:
            sayAndWrite(engine,"Below are the most used words with their count")
            most_used_words = show_stastistics()
            print(most_used_words)

def voice_engine_check(engine):
    if engine is None:
        engine = Engine()
    return engine
                
class Engine:
    def say(self, text):
        print()
    def runAndWait(self):
        print()   
