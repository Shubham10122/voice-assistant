ASSISTANT_NAME='JARVIS'
# import google.generativeai as genai

# #Replace with your valid Gemini API key
# API_KEY = "AIzaSyAaohoFzRjZwIJshSd13xPuZVb6eiWDxmU"
# genai.configure(api_key=API_KEY)

# # Fetch and display all supported models
# models = genai.list_models()

# for model in models:
#     print("=" * 60)
#     print(f"Model Name: {model.name}")
#     print(f"  Description: {model.description}")
#     print(f"  Input Token Limit: {model.input_token_limit}")
#     print(f"  Output Token Limit: {model.output_token_limit}")

#     # Safe check: Only print attributes that exist
#     if hasattr(model, 'temperature'):
#         print(f"  Default Temperature: {model.temperature}")
#     if hasattr(model, 'top_k'):
#         print(f"  Top-K: {model.top_k}")
#     if hasattr(model, 'top_p'):
#         print(f"  Top-P: {model.top_p}")
#     if hasattr(model, 'stop_sequences'):
#         print(f"  Stop Sequences: {model.stop_sequences}")
#     # ⚠️ supports_streaming is not a valid attribute in Gemini SDK (remove this)
