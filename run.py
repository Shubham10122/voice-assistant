import multiprocessing
import queue
import struct
import threading
import time
import pvporcupine
import pyaudio
from engine.command import *
import os


stop_event=threading.Event()
process_thread=None
# To run Jarvis
def startJarvis():
        # Code for process 1
        print("Starting JARVIS..")
        # from main import start           
        # start()
        eel.init("www")
        from engine.features import playAssistantSound
        playAssistantSound()
        os.system('start msedge.exe --app="http://localhost:8000/index.html"')
        eel.start('index.html', mode=None, host="localhost", block=True)

try:
    porcupine = pvporcupine.create(
        access_key="alPmGL8rWMeKKWg8Nfv7yblKKQ0zQooTQc5AgcjcY4enP7JmfzwlKQ==", 
        keyword_paths=[r"C:\Users\shubh\OneDrive\Desktop\JARVIS\engine\jarvis.ppn"]
    )
except Exception as e:
    print(f"Error initializing Porcupine: {e}")
    exit(1)

try:
    porcupine_exit = pvporcupine.create(
        access_key="alPmGL8rWMeKKWg8Nfv7yblKKQ0zQooTQc5AgcjcY4enP7JmfzwlKQ==",
        keywords=['terminator']
    )
except Exception as e:
    print(f'Error initializing exit detection: {e}')
    exit(1)

# Initialize PyAudio for Wake Word Detection
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

audio_queue = queue.Queue()
def listen_for_wake_word():
    print("Listening for wake word...")
    asyncio.run(speak("Hello Sir, all systems are fully operational. How may I assist you"))
    while True:                    
        try:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            
            if result>=0:
            
                print("Wake word detected!")
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                audio_queue.put("wake")
        except Exception as e:
            print(f"Error in wake word detection: {e}")

#Initialize pyaudio for exit detection
pa2 = pyaudio.PyAudio()
stream2 = pa2.open(
        rate=porcupine_exit.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine_exit.frame_length
    )

def listen_exit_word():
    print("Listening for exit word...")
    while True:
        try:
            pcm = stream2.read(porcupine_exit.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine_exit.frame_length, pcm)
            result = porcupine_exit.process(pcm)

            if result >= 0:
                print("Exit hotword detected!")
                audio_queue.put("sleep")
                #break  # optional: break this loop
        except Exception as e:
            print(f"Error in exit detection: {e}")


def interrupt_command():
    global stop_event,process_thread
    if process_thread and process_thread.is_alive():
        print("Interrupting current command...")
        stop_event.set()
        process_thread.join()
        stop_event.clear()

def run_command():
    allCommands(message=1,stop_event=stop_event)
    
def start_processing_thread():
    global process_thread
    interrupt_command()
    time.sleep(0.5)
    print("Starting speech processing thread...")
    process_thread = threading.Thread(target=run_command)
    process_thread.start()

start_thread=threading.Thread(target=startJarvis)
wake_word_thread = threading.Thread(target=listen_for_wake_word)
exit_thread = threading.Thread(target=listen_exit_word)

start_thread.start()
time.sleep(1)
wake_word_thread.start()
exit_thread.start()

start_thread.join()
wake_word_thread.join()
exit_thread.join()

while True:
     if not audio_queue.empty:
        message=audio_queue.get()
        if message=="wake":
            start_processing_thread()
        elif message=="sleep":
            asyncio.run(speak("Have a nice day sir.."))
            break


          
# if __name__ == '__main__':
#         p1 = multiprocessing.Process(target=startJarvis)
#         p2 = multiprocessing.Process(target=listen_for_wake_word)
#         p1.start()
#         p2.start()
#         p1.join()
#         p2.join()
          
        