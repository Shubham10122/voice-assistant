import asyncio
from pipes import quote
import re
import subprocess
import PyDictionary
from playsound import playsound
import eel
import pyaudio
import pvporcupine
import time
import struct

import pyautogui
import requests
import wikipedia
from engine.command import speak, takecommand
from engine.config import ASSISTANT_NAME
import os
import pywhatkit as kit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from engine.helper import extract_yt_term, remove_words
import webbrowser
from hugchat import hugchat
import google.generativeai as genai
con=sqlite3.connect('jarvis.db')
cursor=con.cursor()

#assistant boot sound function
@eel.expose
def playAssistantSound():
    music_dir="www\\assets\\audio\\openSound.mp3"
    playsound(music_dir)


#open Command function
import subprocess
import webbrowser



def openCommand(recognized_txt):
    recognized_txt=recognized_txt.replace(ASSISTANT_NAME,"")
    recognized_txt=recognized_txt.replace("open","")

    app_name=recognized_txt.strip()
    if app_name:
        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            result = cursor.fetchall()
            
            if result:
                eel.DisplayMessage('opening'+recognized_txt)
                asyncio.run(speak("opening"+recognized_txt))
                os.startfile(result[0][0])

            elif len(result)==0:
                recognized_txt = recognized_txt.replace(" ", "")

                if "." not in recognized_txt:
                    website_name = recognized_txt + ".com"
                else:
                    website_name = recognized_txt+"com"
                url = f"https://{website_name}"
                eel.DisplayMessage('opening' +" "+ recognized_txt)
                asyncio.run(speak('opening'+recognized_txt))
                print('opening'+recognized_txt)
                try:
                    webbrowser.open(url)
                except:
                    asyncio.run(speak('website not found'))
        except:
            asyncio.run(speak('website cant be loaded'))


    # if recognized_txt:
    #     eel.DisplayMessage('Opening'+ recognized_txt)
    #     speak('opening'+recognized_txt)
    #     os.system('start' +recognized_txt)

    
    else:
        speak("not found")

def PlayYoutube(query):
    
    search_term = extract_yt_term(query)
    eel.DisplayMessage("Playing" +" "+ search_term +" "+ "on youtube")
    asyncio.run(speak("Playing "+search_term+" on YouTube"))
    print('playing'+search_term+'on youtube')
    kit.playonyt(search_term)

def search_weather():
    asyncio.run(speak("say the location"))
    city=takecommand().strip()
    api_key="a3c3ff9c45901760f3cd9575f87dc7e3"
    base_url="http://api.openweathermap.org/data/2.5/weather"
    params={"q":city,
            "appid":api_key,
            "units":"metric"}
    try:
        response=requests.get(base_url, params=params)
        weather_data=response.json()
        print(weather_data)
        if weather_data["cod"] == 200:
            temperature = weather_data["main"]["temp"]
            weather_description = weather_data["weather"][0]["description"]
            city_name = weather_data["name"]
            asyncio.run(speak(f"The weather in {city_name} is {weather_description} with a temperature of {temperature}°C."))
        else:
            asyncio.run(speak("Sorry I could not find the weather details for that location"))
    except Exception as e:
        asyncio.run(speak(f"error fetching weather data:{e}"))

def get_news():
    api_key = 'dd1bb04f0ecc4691afd2e2c526db00f3' 
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    response = requests.get(url)
    articles = response.json()['articles'][:5]  # top 5 headlines

    for i, article in enumerate(articles, start=1):
        eel.DisplayMessage(article['title'])
        asyncio.run(speak(article['title']))
        print(f"News {i}: {article['title']}")

def search_wikipedia(query):
    wikipedia.set_lang("en")  # Set language to English
    result = wikipedia.summary(query, sentences=2)
    print("Wikipedia says:", result)
    eel.DisplayMessage(result)
    asyncio.run(speak(result))

def get_definition(word):
    dictionary=PyDictionary()
    meaning=dictionary.meaning(word)
    if meaning:
        for part_of_speech, definitions in meaning.items():
            print(f"{part_of_speech}: {definitions[0]}")
            break

def send_email(subject,email_body):
    #asyncio.run(speak("say the recipient address"))
    recipient="shubham.bhawani402@gmail.com"
    
    # print(recipient.strip())
    # replacements={"dot":".",
    #               "at the rate":"@",
    #               "at":"@",
    #               "underscore":"_"}
    # for key,value in replacements.items:
    #     recipient=recipient.replace(key,value)
    sender_email="jarvisofficial.ai@gmail.com"
    sender_password="mbejqstomfokekkw"
    
    try:
        # Setting up the SMTP server (Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password ) #login to smtp server
        
        # Email content
        message = MIMEMultipart()
        message["From"] = 'jarvisofficial.ai@gmail.com'
        message["To"] = recipient
        message["Subject"] = subject

        # Adding the message body
        message.attach(MIMEText(email_body, "plain"))

        # Sending the email
        server.sendmail(sender_email, recipient, message.as_string())
        server.quit()

        print("Email sent successfully!")
        asyncio.run(speak("email sent successfully"))

    except Exception as e:
        print(f"Error: {e}")
    
    

import google.generativeai as genai

    

# Set your API key

# Initialize the model

def search_engine(query):
    genai.configure(api_key="AIzaSyAaohoFzRjZwIJshSd13xPuZVb6eiWDxmU")
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    try:
        response = model.generate_content(query)
        answer = response.text
        print(answer)
        asyncio.run(speak(answer))  # assuming speak() is a regular function
        
    except Exception as e:
        error_msg = f"Sorry, I couldn't complete the search. Error: {str(e)}"
        asyncio.run(speak(error_msg))
        return error_msg
#whatsapp automation
# def findContact(query):
    
#     words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
#     query = remove_words(query, words_to_remove)

#     try:
#         query = query.strip().lower()
#         cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#         results = cursor.fetchall()
#         mobile_number_str = str(results[0][0])
#         if ":" in mobile_number_str:
#             for i in range(len(mobile_number_str)):
#                 if mobile_number_str[i]==":":
#                     index=i
#                     break
#         mobile_number_str=mobile_number_str[0:index]
#         print(mobile_number_str)

#         if not mobile_number_str.startswith('+91'):
#             mobile_number_str = '+91' + mobile_number_str

#         return mobile_number_str, query
#     except:
#         asyncio.run(speak('does not exist in contacts'))
#         return 0, 0
    

# def whatsApp(mobile_no, message, flag, name):

    # if flag == 'message':
    #     target_tab = 12
    #     jarvis_message = "message sent successfully to "+name

    # elif flag == 'call':
    #     target_tab = 7
    #     message = ''
    #     jarvis_message = "calling to "+name

    # else:
    #     target_tab = 6
    #     message = ''
    #     jarvis_message = "staring video call with "+name

    # # Encoded the message for URL
    # print(message)
    # encoded_message = quote(message)
    # if "'" in encoded_message:
    #     encoded_message=encoded_message.replace("'","")
    # print(encoded_message)

    # # Construct the URL
    # whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # # Construct the full command
    # #full_command = f'start "" "{whatsapp_url}"'
    # full_command=['start', '', whatsapp_url]

    # # Open WhatsApp with the constructed URL using cmd.exe
    # subprocess.run(full_command, shell=True)
    # time.sleep(5)
    # subprocess.run(full_command, shell=True)
    
    # pyautogui.hotkey('ctrl', 'f')

    # for i in range(1, target_tab):
    #     pyautogui.hotkey('tab')

    # pyautogui.hotkey('enter')
    # speak(jarvis_message)
