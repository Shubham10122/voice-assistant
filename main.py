import os
import eel
import threading
from engine.features import *
from engine.command import *

# Initialize eel

# Function to open the assistant's interface
def start():
    eel.init("www")
    playAssistantSound()
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')
    eel.start('index.html', mode=None, host="localhost", block=True)




#Function to play the welcome sound
