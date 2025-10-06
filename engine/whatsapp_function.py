
import asyncio
from cmath import e
import os
import pickle
import time
import pywhatkit as kit
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pyautogui

#from engine.command import speak

#from engine.command import speak

#from engine.command import speak
    

# Define the scope for the Google People API
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

print("Current Working Directory:", os.getcwd())
def authenticate():
    """Authenticates the user and returns the People API service."""
    try:
        creds = None
        token_file = 'token.pickle'
        #token_file=f'token_{email}.pickle'
        # Check if the token.pickle file already exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials are available, initiate the OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    r'C:\Users\shubh\OneDrive\Desktop\JARVIS\engine\client_secret.json', SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for future use
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # Build the People API service
        service = build('people', 'v1', credentials=creds)
        return service
    except Exception as e:
        print("authentication failed :",e)
        return None

def fetch_contacts():
    """Fetches contacts using the People API."""
    service = authenticate()
    contacts_dict={}
    #while True:
    try:
            # Make an API call to fetch connections
            results = service.people().connections().list(
            resourceName='people/me',
            pageSize=500,  # Adjust the page size as needed
            personFields='names,phoneNumbers,emailAddresses'
        ).execute()

            connections = results.get('connections', [])
            # all_contacts.extend(connections)

           
            # time.sleep(1)
    # except HttpError as error:
    #         if error.resp.status==429:
    #             print("Rate limit exceeded. Retrying after 60 seconds...")
    #             time.sleep(60)
    #         else:
    #             raise
            
            for person in connections:
                names=person.get('names',[])
                phone_numbers=person.get('phoneNumbers',[])
                
                if names:
                    #print(f"Name: {names[0].get('displayName')}")
                    name= names[0].get('displayName')
                
                if phone_numbers:
                    #print(f"PhoneNumber: {phone_numbers[0].get('value')}")
                    number=phone_numbers[0].get('value')

                #storing the value in dictionary  
                contacts_dict[name.lower()]=number.strip()
                
                #print("------------------------------")
            
            return contacts_dict
    except Exception as e:
        #speak("error fetching contacts")
        print(f"error fetching contacts: {e}")
                                 

def find_contact(contacts,name):
    name=name.lower()
    print(name)
    for contact_name in contacts.keys():
        if name in contact_name:
            return contacts[contact_name]
    return None

def send_whatsapp_message(message,phone_number):
    """
    Sends a WhatsApp message to the specified phone number.
    """
    phone_number=phone_number.replace(" ","").strip()
    try:
        # Ensure the phone number is in international format (e.g., +911234567890)
        kit.sendwhatmsg_instantly(phone_number, message, wait_time=15)
        #asyncio.run(speak("message sent successfully"))
        print(f"Message sent to {phone_number} successfully!")
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
        
#from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from urllib.parse import quote
# import time

# def send_whatsapp_message(message,phone_number):
#     # Make sure phone_number is in international format without '+'
#     phone_number=phone_number[1:]
#     chrome_profile_path = r"C:\Users\shubh\AppData\Local\Google\Chrome\User Data\Profile 1"
#     options = webdriver.ChromeOptions()
#     options.add_argument(f"user-data-dir={chrome_profile_path}")

#     driver = webdriver.Chrome(options=options)
#     encoded_message = quote(message)  
#     driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}")
#     time.sleep(15)  # Wait for chat to load

#     try:
#         # Use JavaScript to find and type in the message box
#         script = """
#         var messageBox = document.querySelector('[title="Type a message"]');
#         if (messageBox) {
#             messageBox.focus();
#             messageBox.innerHTML = arguments[0];  // Set message
#             messageBox.dispatchEvent(new Event('input', { bubbles: true }));
#         }
#         """
#         driver.execute_script(script, message)
#         time.sleep(2)

#         # Use JavaScript to click the send button
#         script_send = """
#         var sendButton = document.querySelector('[data-testid="send"]');
#         if (sendButton) {
#             sendButton.click();
#         }
#         """
#         driver.execute_script(script_send)
#         time.sleep(2)

#         print(f"✅ Message sent to {phone_number} successfully!")

#     except Exception as e:
#         print(f"❌ Failed to send the message: {e}")

#     driver.quit()




# def initiate_call(phone_number):
#     try:
#         # Open WhatsApp Desktop
#         pyautogui.hotkey('win', 's')
#         time.sleep(1)
#         pyautogui.write('WhatsApp', interval=0.1)
#         time.sleep(1)
#         pyautogui.press('enter')
#         time.sleep(5)

#         # Search for the contact
#         pyautogui.click(x=200, y=100)  # Adjust coordinates
#         time.sleep(1)
#         pyautogui.write(phone_number, interval=0.1)
#         time.sleep(2)
#         pyautogui.press('enter')
#         time.sleep(1)

#         # Click on the call button
#         pyautogui.click(x=1350, y=80)  # Adjust coordinates for call button
#         time.sleep(1)
#         #speak("Call initiated successfully")
#         print(f"Call initiated to {phone_number} successfully!")
#     except Exception as e:
#         print(f"Failed to initiate call: {e}")


