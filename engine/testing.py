import subprocess
import os
import pvporcupine
import pyaudio
import struct
import queue
import threading
import whisper
import asyncio
import edge_tts
import google.generativeai as genai  # Import Gemini library
import sounddevice as sd
import numpy as np
import wave


# ✅ Initialize Porcupine Wake Word Detection
try:
    porcupine = pvporcupine.create(
        access_key="alPmGL8rWMeKKWg8Nfv7yblKKQ0zQooTQc5AgcjcY4enP7JmfzwlKQ==", 
        keyword_paths=[r"C:\Users\shubh\OneDrive\Desktop\JARVIS\engine\jarvis.ppn"]
    )
except Exception as e:
    print(f"Error initializing Porcupine: {e}")
    exit(1)

# ✅ Initialize PyAudio for Wake Word Detection
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

# ✅ Load Whisper Model for Fast Speech Recognition
print("Loading Whisper model...")
whisper_model = whisper.load_model("base.en")

# ✅ Initialize Gemini API Key and Configuration
API_Key = 'AIzaSyDBV5E5JDvwc6b_UTvoqWDIGs13_haHirI'
genai.configure(api_key=API_Key)

# ✅ Define Fallback Model Name
model_name = "gemini-1.5-pro-latest"  # You may need to check for available models manually if necessary

# ✅ Queue to Handle Audio Processing Tasks
audio_queue = queue.Queue()

# ✅ Function: Record Audio After Wake Word
def record_audio(filename="input_audio.wav", duration=5, sample_rate=16000):
    print("Recording audio...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()
    wave_file = wave.open(filename, "wb")
    wave_file.setnchannels(1)
    wave_file.setsampwidth(2)
    wave_file.setframerate(sample_rate)
    wave_file.writeframes(audio_data.tobytes())
    wave_file.close()
    print("Recording complete!")

# ✅ Function: Convert Text to Speech
async def text_to_speech(text):
    tts = edge_tts.Communicate(text, "en-US-GuyNeural")
    await tts.save("response.mp3")
    mpg123_path = r"C:\Users\shubh\OneDrive\Desktop\mpg123\mpg123-1.32.10-static-x86-64\mpg123.exe"
    subprocess.run([mpg123_path, "response.mp3"], shell=True)  # Opens in the default audio player

# ✅ Function: Listen for Wake Word
def listen_for_wake_word():
    print("Listening for wake word...")
    while True:
        try:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            result = porcupine.process(pcm)
            if result >= 0:
                print("Wake word detected!")
                audio_queue.put("wake")
        except Exception as e:
            print(f"Error in wake word detection: {e}")

# ✅ Function: Process Speech After Wake Word is Detected
def process_speech():
    while True:
        if not audio_queue.empty():
            audio_queue.get()
            record_audio()  # Record user speech

            # Ensure audio file exists before processing
            if not os.path.exists("input_audio.wav"):
                print("Error: Recorded audio not found!")
                continue

            # Whisper Speech-to-Text
            print("Processing speech...")
            result = whisper_model.transcribe("input_audio.wav")
            text = result["text"].strip()
            print(f"You: {text}")

            # Gemini API Response with error handling for unavailable model
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(text)
                if response and response.text:
                    reply = response.text.strip()
                    print(f"Assistant: {reply}")

                    # Speak Response
                    asyncio.run(text_to_speech(reply))
                else:
                    print("Assistant: Sorry, I could not find any relevant information.")
                    asyncio.run(text_to_speech("Sorry, I could not find any relevant information."))
            except Exception as e:
                print(f"Error: {e}")
                print("Assistant: Sorry, I couldn't process your request.")
                asyncio.run(text_to_speech("Sorry, I couldn't process your request."))

# ✅ Start Wake Word Detection & Speech Processing Threads
wake_word_thread = threading.Thread(target=listen_for_wake_word)
speech_thread = threading.Thread(target=process_speech)

wake_word_thread.start()
speech_thread.start()

wake_word_thread.join()
speech_thread.join()
