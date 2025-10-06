import asyncio
import os
import re
import subprocess
import sys
import wave
import edge_tts
import numpy as np
import pyttsx3
import speech_recognition as sr
import eel
import time
import sounddevice as sd
import whisper

#  Function: Convert Text to Speech
@eel.expose
async def speak(text):                                                                            
    tts = edge_tts.Communicate(text, "en-US-GuyNeural")
    await tts.save("response.mp3")
    mpg123_path = r"C:\Users\shubh\OneDrive\Desktop\mpg123\mpg123-1.32.10-static-x86-64\mpg123.exe"
    subprocess.run([mpg123_path, "response.mp3"], shell=True)  # Opens in the default audio player                                                                       
                                                                                                                
#  Function: Record Audio After Wake Word
@eel.expose
def takecommand(filename="input_audio.wav", duration=5, sample_rate=16000):
    print("Listening...")
    eel.DisplayMessage("Listening...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    wave_file = wave.open(filename, "wb")
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(audio_data.tobytes())
    wave_file.close()
    print("Recording complete!")
    try:
        # Ensure audio file exists before processing
        if not os.path.exists("input_audio.wav"):
            print("Error: Recorded audio not found!")
        # Whisper Speech-to-Text
        print("Processing speech...")
        eel.DisplayMessage("Processing speech...")
        whisper_model = whisper.load_model("base.en")
        result = whisper_model.transcribe("input_audio.wav")
        text = result["text"].strip()
        eel.DisplayMessage(text)
        print(f"You: {text}")  
        return text.lower()[:-1] 
    except Exception as e:
        return "" 
    

@eel.expose
def takeecommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..")
        eel.DisplayMessage("Listening..") #backend sending message to frontend controller js
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source)

        audio=r.listen(source,timeout=None)
    try:
        print("recognizing..")
        eel.DisplayMessage("recognizing..") #backend sending message to frontend controller js
        recognized_txt=r.recognize_google(audio,language='en-in')
        eel.DisplayMessage(recognized_txt) #backend sending message to frontend controller js
        print(f"User Said : {recognized_txt}")
    except Exception as e:
        return ""
    return recognized_txt.lower()

@eel.expose
def allCommands(message=1):
    # if stop_event and stop_event.is_set():
    #     print("[JARVIS] Command aborted before starting.")
    #     return
    if message==1:
        recognized_txt= takecommand()
        recognized_txt.lower()
        eel.senderText(recognized_txt)

    else:
        recognized_txt=message
        recognized_txt.lower()
        eel.senderText(recognized_txt)

    try:
        # if stop_event and stop_event.is_set():
        #     print("[JARVIS] Command aborted before starting.")
        #     return
        
        if "open" in recognized_txt:
            # if stop_event and stop_event.is_set():
            #     print("[JARVIS] Command aborted before starting.")
            #     return
            from engine.features import openCommand
            openCommand(recognized_txt)

        elif 'on youtube' in recognized_txt:

            from engine.features import PlayYoutube
            PlayYoutube(recognized_txt)
        elif "news" in recognized_txt:
            from engine.features import get_news
            get_news()

        elif "send a message to" in recognized_txt or "call" in recognized_txt or "video call" in recognized_txt:
                
                message = ""
                from engine.whatsapp_function import fetch_contacts
                contacts_dict= fetch_contacts()
                
                if(contacts_dict != 0):

                    if "send a message to" in recognized_txt:
                        name=recognized_txt.replace("send a message to","").strip()
                        from engine.whatsapp_function import find_contact
                        phone_number=find_contact(contacts_dict,name)
                        

                        if phone_number:
                            asyncio.run(speak("what message to send"))              
                            message = takecommand()
                            from engine.whatsapp_function import send_whatsapp_message
                            send_whatsapp_message(message,phone_number)
                        else:
                            asyncio.run(speak("contact not found"))
                        
                    elif "call" in recognized_txt:
                        name=recognized_txt.replace("call","").strip()
                        from engine.whatsapp_function import find_contact
                        phone_number=find_contact(contacts_dict,name)
                        if phone_number:
                            from engine.whatsapp_function import initiate_call
                            initiate_call(phone_number[3:])
                        else:
                            asyncio.run(speak("contact not found"))
                    else:
                        message = 'video call'
                        
                    
        elif 'send email' in recognized_txt:
            print("Say the recipient's email address:")
            #recipient = 'kunaloffcial14@gmail.com'

            print("Say the email subject:")
            asyncio.run(speak("Say the email subject"))
            subject = takecommand()

            print("Say the email message:")
            asyncio.run(speak("say the email message"))
            message = takecommand()

            if subject and message:
                from engine.features import send_email
                send_email(subject,message)
        elif 'wikipedia' in recognized_txt:
            from engine.features import search_wikipedia
            search_wikipedia(recognized_txt) 

        elif "define" in recognized_txt:
            word=recognized_txt.replace("define","").strip()
            from engine.features import get_definition
            get_definition(word)

        elif "weather status" in recognized_txt:
            
            from engine.features import search_weather
            search_weather()

        elif " detect object " in recognized_txt:
            from engine.object_recognition import scan_object
            scan_object()

        elif "set brightness" in recognized_txt:
            import screen_brightness_control as sbc
            numbers=re.findall(r'\d+',recognized_txt)
            if numbers:
                level=int(numbers[0])
            if level is not None:
                if 0<=level<=100:
                    sbc.set_brightness(level)
                    print(f"Brightness set to {level}%")
                    eel.DisplayMessage(f"Brightness set to {level}%")
                    asyncio.run(speak(f"Brightness set to {level}%"))
                else:
                    asyncio.run(speak("Brightness must be between 0 and 100"))
            else:
                asyncio.run(speak("Couldn't catch the brightness level"))
                
            sbc.set_brightness(level)

        elif "shut down" in recognized_txt:
            os.system('shutdown/s/t 1')

        elif "restart" in recognized_txt:
            os.system('shutdown/r/t 1')
        else:
            from engine.features import search_engine
            search_engine(recognized_txt)
    
    except:
        asyncio.run(speak("can you please repeat again?"))
    eel.DisplayHood()
        
eel.init("www")
@eel.expose
def wakeup():
    while True:
        print("wakeup invoked")
        permission=takecommand()
        if "wake up" in permission:
            print("wake up command detected")
            #pressing shorcut key win+j
            import pyautogui as autogui
            autogui.keyDown("win")
            autogui.press("j")
            time.sleep(2)
            autogui.keyUp("win")
        elif "exit" in permission:
            eel.DisplayHood()
            eel.DisplayMessage("It was a pleasure assisting you")
            speak("It was a pleasure assisting you")
            break




        # time.sleep(2)
        # eel.DisplayHood()

