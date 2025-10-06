import re


def extract_yt_term(command): #need to learn
    pattern=r'play\s+(.*?)\s+on\s+youtube'
    match=re.search(pattern,command,re.IGNORECASE) #using re.search to find the match in the command
    if match:
        return match.group(1) #if a match is found then return the extracted item name to search 
    else:
        return None

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

# import os
# print(os.path.exists("input_audio.wav"))  # Should return True if the file exists
# import google.generativeai as genai

# API_Key = 'AIzaSyDBV5E5JDvwc6b_UTvoqWDIGs13_haHirI'
# genai.configure(api_key=API_Key)

# # Fetch available models
# models = genai.list_models()

# # Print the available models
# for model in models:
#     print(model.name)

import phonenumbers
from phonenumbers import geocoder, carrier

numbers = phonenumbers.parse("+919546605667", None)
print(geocoder.description_for_number(numbers, "en"))
print(carrier.name_for_number(numbers, "en"))

