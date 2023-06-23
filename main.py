import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
from playsound import playsound
import random
import openai
import time
from prettytable import PrettyTable



myTable = PrettyTable(["Commands","Actions"])

myTable.add_row(["Wikipedia","Search Wikipedia"])
myTable.add_row(["Youtube","Opens Youtube"])
myTable.add_row(["stack overflow","Opens stack overflow"])
myTable.add_row(["Naya Raipur","Opens IIIT Naya Raipur Website"])
myTable.add_row(["Play Music","Plays song"])
myTable.add_row(["Using A.I","Search Prompt In ChatGPT"])
myTable.add_row(["Play Game","Opens Tic Tac Toe Game"])
myTable.add_row(["quit","Kills The Program"])


engine= pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)     
newVoiceRate = 130
engine.setProperty('rate',newVoiceRate)

print(myTable)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
 
 
def ai(prompt,a):
    openai.api_key = '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'
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")


    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)
    if(a==1):
        newVoiceRate = 250
        engine.setProperty('rate',newVoiceRate)

        speak(response["choices"][0]["text"])
    time.sleep(2)
 
def wishMe():
    hour= int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("good morning")
    elif hour>=12 and hour<=18:
        speak("good afternoon")
    else:
        speak("good evening")
        
    speak("I am Ella. How may I help you")

def takeCommand():
              
#takes microphone input from user and returns sting output

    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("LISTENING....")
        
        audio=r.listen(source)
    try:
        print("RECOGNIZING....")
        query= r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
        
    except Exception as e:
        print(e)
        print("say that again please....")
        return "none"
    return query    


    
    
if __name__=="__main__":
    newVoiceRate = 180
    engine.setProperty('rate',newVoiceRate)

    wishMe()
    while True:
        query = takeCommand()
        
        #logic for executing tasks based on query
        if ('Wikipedia' or 'wikipedia') in query:
            speak('searching wikipedia....')
            query = query.replace("wikipedia","")
            results= wikipedia.summary(query, sentences=2)
            speak("According to wikipedia...")
            print(results)
            speak(results)
        
        elif ('YouTube' or 'youtube') in query:
            webbrowser.open("www.youtube.com")
            time.sleep(2)
            
        elif ('Google' or 'google') in query:
            webbrowser.open("www.google.com")
            
        elif ('stack overflow' or 'Stack Overflow') in query:
            webbrowser.open("stackoverflow.com")
            time.sleep(2)
        elif ('Naya Raipur' or 'naya raipur') in query:
            webbrowser.open("www.iiitnr.ac.in") 
            time.sleep(2)
            
        elif ('play music') in query:
            playsound("C:\\Users\\asus\\Music\\_Lyrics__Qaafirana_%5BWORMONO_Lofi_Remake%5D___Kedarnath___Bollywood_Lofi___Without_Dialogues(48k).mp3")
            time.sleep(2)
        
        elif "using AI".lower() in query.lower():
            a=int(input("should i speak:-(Y/N)"))
            ai(query,a) 
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")
            
        
        elif ('game' or 'Game') in query:
            import tictactoe as tk
            tk.play()

        elif ('quit' or 'quit') in query:
            break
