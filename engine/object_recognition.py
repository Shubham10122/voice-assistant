# import cv2
# import torch
# import pyttsx3
# from PIL import Image
# from ultralytics import YOLO
# from lavis.models import load_model_and_preprocess

# # Setup device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load BLIP-2 model
# blip_model, vis_processors, _ = load_model_and_preprocess(
#     name="blip2_opt",
#     model_type="blip2_opt_2.7b",
#     is_eval=True,
#     device=device
# )

# # Load YOLOv8
# yolo_model = YOLO("yolov8n.pt")  # Lightweight model, change to yolov8s.pt for better accuracy

# # TTS engine
# engine = pyttsx3.init()

# # Start webcam
# cap = cv2.VideoCapture(0)
# print("[INFO] Starting real-time object + brand recognition. Press 'q' to quit.")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     results = yolo_model(frame)[0]
#     crops = []

#     # Extract each detected object
#     for box in results.boxes:
#         x1, y1, x2, y2 = map(int, box.xyxy[0])
#         cropped_img = frame[y1:y2, x1:x2]
#         crops.append((cropped_img, (x1, y1, x2, y2)))

#     for crop, box in crops:
#         # Convert crop to PIL and preprocess
#         img_pil = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
#         image_tensor = vis_processors["eval"](img_pil).unsqueeze(0).to(device)

#         # Generate brand-aware caption
#         prompt = "Describe the object with brand or label if visible."
#         with torch.no_grad():
#             description = blip_model.generate({"image": image_tensor, "prompt": prompt})[0]

#         # Draw on frame
#         x1, y1, x2, y2 = box
#         cv2.putText(frame, description, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
#         print(f"[INFO] BLIP-2 says: {description}")
#         engine.say(f"I think this is {description}")
#         engine.runAndWait()

#     cv2.imshow("Object + Brand Recognition", frame)
#     if cv2.waitKey(1) & 0xFF == ord("q"):
#         break

# cap.release()
# cv2.destroyAllWindows()



import asyncio
import cv2
import numpy as np
import time
import io
import webcolors
from PIL import Image
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import os
import google.generativeai as genai
from engine.command import *


# Configure Gemini API
genai.configure(api_key="AIzaSyDBV5E5JDvwc6b_UTvoqWDIGs13_haHirI")   # Replace with your Gemini API key
model = genai.GenerativeModel(model_name="gemini-pro-vision")
@eel.expose
def get_object_description(image_path):
    print("function called")
    with open(image_path, "rb") as img_file:
        print("file opened")
        img = Image.open(io.BytesIO(img_file.read()))
        print("done")
        response = model.generate_content(["Describe the main object in this image.", img])
        print(response)
        return response.text

 
@eel.expose
def get_object_description(image_path):
    print("function called")
    with open(image_path, "rb") as img_file:
        print("file opened")
        img = Image.open(io.BytesIO(img_file.read()))
        print("done")
        response = model.generate_content(["Describe the main object in this image.", img])
        print(response)
        return response.text

def estimate_distance(box_width_pixels, known_width_cm=7.0, focal_length=700):
    return (known_width_cm * focal_length) / box_width_pixels

def closest_color(requested_color):
    def rgb_tuple(hex_value):
        return webcolors.hex_to_rgb(hex_value)

    named_colors = {
        'black': '#000000', 'white': '#FFFFFF', 'red': '#FF0000', 'green': '#008000',
        'blue': '#0000FF', 'yellow': '#FFFF00', 'cyan': '#00FFFF', 'magenta': '#FF00FF',
        'gray': '#808080', 'orange': '#FFA500', 'pink': '#FFC0CB', 'brown': '#A52A2A',
        'purple': '#800080',
    }

    min_colors = {}
    for name, hex_value in named_colors.items():
        r_c, g_c, b_c = rgb_tuple(hex_value)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name

    return min_colors[min(min_colors.keys())]

def detect_color_name(image):
    pixels = np.float32(image.reshape(-1, 3))
    _, _, palette = cv2.kmeans(pixels, 1, None,
                               (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2),
                               10, cv2.KMEANS_RANDOM_CENTERS)
    dominant = palette[0].astype(int)
    return closest_color((dominant[2], dominant[1], dominant[0]))  # BGR to RGB

def translate_and_speak(text, lang_code):
    try:
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        print(f"Translated: {translated}")
        tts = gTTS(text=translated, lang=lang_code)
        filename = "translated.mp3"
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        asyncio.run(speak("Sorry, I couldn't translate. Please try again."))
        print(e)

def scan_object():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        asyncio.run(speak("Camera failed to open."))
        return
    eel.DisplayMessage("Opening camera. Hold the object in front of me.")
    asyncio.run(speak("Opening camera. Hold the object in front of me."))

    start_time = time.time()
    captured_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            speak("Failed to read from camera.")
            break

        cv2.imshow("Jarvis Camera Feed - Hold Object", frame)

        # Store one good frame after 5 seconds
        if time.time() - start_time > 5 and captured_frame is None:
            captured_frame = frame.copy()
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    if captured_frame is None:
        speak("Failed to capture image.")
        cap.release()
        cv2.destroyAllWindows()
        return
    print("camera")
    image_path = "captured_object.jpg"
    
    cv2.imwrite(image_path, captured_frame)
    print("camera")
    asyncio.run(speak("Image captured. Scanning..."))

    
    description = get_object_description(image_path)
    if description:
        print(description)
    else:
        print("None")
    #color_name = detect_color_name(captured_frame)

    # full_description = (
    #     f"Color of the object is {color_name}. "
    #     f"Estimated distance is {int(distance)} centimeters. "
    #     f"Description: {description}"
    # )

    asyncio.run(speak("Here is what I found."))
    # asyncio.run(speak(f"Color of the object is {color_name}."))
    # asyncio.run(speak(f"Estimated distance is {int(distance)} centimeters."))
    eel.DisplayMessage(description)
    print(description)
    asyncio.run(speak(f"Description: {description}"))

    # asyncio.run(speak("Do you want to listen in another language?"))
    # lang_input = takecommand()

    # if lang_input:
    #     lang_map = {
    #         "bengali": "bn",
    #         "hindi": "hi",
    #         "spanish": "es",
    #         "french": "fr",
    #         "german": "de"
    #     }
    #     for key in lang_map:
    #         if key in lang_input:
    #             translate_and_speak(full_description, lang_map[key])
    #             break
    #     else:
    #         speak("Language not supported.")

    cap.release()
    cv2.destroyAllWindows()

# def main():
#     speak("Hello, I am Jarvis. How can I help you?")
#     while True:
#         command = listen_command()
#         if command and "open camera" in command:
#             scan_object()
#             break
#         elif command:
#             speak("Please say 'open camera' to begin.")

# if __name__ == "__main__":
#     main()

# from ultralytics import YOLO
# import cv2

# # 1. Load YOLOv8 model (Nano = fastest, ideal for real-time)
# model = YOLO('yolov8n.pt')

# # 2. Access webcam
# cap = cv2.VideoCapture(0)

# # 3. Check webcam access
# if not cap.isOpened():
#     print("Error: Could not open webcam.")
#     exit()

# # 4. Start real-time loop
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         print("Error: Failed to read frame.")
#         break

#     # 5. Run YOLOv8 detection on frame
#     results = model(frame)

#     # 6. Draw bounding boxes and labels on frame
#     annotated_frame = results[0].plot()

#     # 7. Show the detected objects live
#     cv2.imshow("Object Detection - Voice Assistant", annotated_frame)

#     # 8. Quit when 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # 9. Release resources
# cap.release()
# cv2.destroyAllWindows()
