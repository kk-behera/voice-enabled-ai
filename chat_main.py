# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 23:02:03 2018

@author: Kamalakanta
"""

import pickle
import mode_operations as mop
import db_operations as dbo
import pyttsx3 as vo
import wolframalpha as wo
import category_operations as cop
import speech_recognition as sr
import schedule as sc

# Setup global variables
engine = None
voices = []
global current_mode
current_mode = "standard"
listen_mode = True
general_text = "Say something: "
inp = ""
client = wo.Client("3HH6H6-2WPW4W566Y")
welcome_text = "Welcome everyone. Good {} . I'm your friend Alice, an artificially inteligent computational engine. For any help in using me say help".format(cop.timeOfDay())

## Speech related operations ##
def setUpVoiceEngine():
    global engine
    engine = vo.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    voices[1].name = 'Alice'

def speedUpVoice():
    global engine
    engine.setProperty('rate',engine.getProperty('rate') +25) 

def slowDownVoice():
    global engine
    engine.setProperty('rate',engine.getProperty('rate') -25)

def toggleSpeaker():
    global engine
    if engine is not None:        
        engine.stop()
        engine = None       
    else:
        setUpVoiceEngine()

def sayIt(engine, text):
    if engine is not None:
        engine.say(text)
        engine.runAndWait() 
        
def sayAndWrite(engine, text):
    print(text)
    if engine is not None:
        engine.say(text)
        engine.runAndWait() 

def showHelp():
    sayAndWrite(engine,"For switching off listening say, text only")
    sayAndWrite(engine,"For start listening again say, listen now")
    sayAndWrite(engine,"For switching on or off speaking say, toggle speaker")
    sayAndWrite(engine,"For increasing my talking speed say , speed up voice")
    sayAndWrite(engine,"For decreasing my talking speed say , slow down voice")
    return
####################################    
        
def checkSystemCommand(command):
    is_system_command = True
    if command == 'text only':
        sayAndWrite(engine,"Listening mode switched off")
        global listen_mode
        listen_mode = False
    elif command == 'listen now':
        sayAndWrite(engine,"Listening mode switched on")
        listen_mode = True
    elif command == 'toggle speaker':
        toggleSpeaker()
        sayAndWrite(engine, "Speaker mode toggled")
    elif command == 'speed up voice':
        speedUpVoice()
        sayAndWrite(engine, "Voice speeded up")
    elif command == 'slow down voice':
        slowDownVoice()
        sayAndWrite(engine, "Voice slowed down") 
    elif command == 'help':
        showHelp()
    else:
        is_system_command = False
    return is_system_command

open_classifier = open("vect.pickle","rb")
vect = pickle.load(open_classifier)

#Classifier setup
open_classifier = open("logistic.pickle","rb")
logistic = pickle.load(open_classifier)

#Listenng setup
r = sr.Recognizer()
active = False
wakeup_word_found = False
# Start the speech
setUpVoiceEngine()
sayAndWrite(engine, welcome_text)

while True:
    if listen_mode == True:       
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                listened_text = r.recognize_google(audio)
                if(active == False):
                    if('hello alice' in listened_text.lower()):
                        active = True
                        sayAndWrite(engine, "Welcome! Listening enabled now")
                else:
                    inp = listened_text                    
            except:
                if(active == True):
                   sayAndWrite(engine, "I can't listen")
    else:
        inp = input(general_text)
    if('stop' in inp.lower() or 'exit' in inp.lower()):
        sayAndWrite(engine, "Ending conversation. Bye bye")
        dbo.clear_training_session_data()
        if engine is not None:
            engine.stop()
        break
    elif('mode' in inp.lower()):
        current_mode = mop.activateRequestedMode(inp.lower(), current_mode, engine)
        inp = ""
        continue
    try:
        if inp != "":
            is_system_command = checkSystemCommand(inp)
            if is_system_command:
                inp = ""
                continue
            input_list = []
            input_list.append(inp)
            X_act_test = vect.transform(input_list)
            statement_category = logistic.predict(X_act_test)
            cop.perform_category_operations(statement_category[0], engine, client, inp)
            mop.perform_extra_mode_operations(current_mode, statement_category[0], engine, client, inp)
            sc.run_pending()
            inp = ""
    except Exception as e:
        print("Exception occured "+str(e))