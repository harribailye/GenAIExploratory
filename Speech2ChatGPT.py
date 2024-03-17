# Exploration of OpenAI API to ChatGPT model 
# Author: Harrison Bailye
# Date: 29/02/2024
# This file takes user input as speech, sends it to the openAI API (ChatGPT-3.5-turbo model) and returns the model output 

# Import libaries 
from openai import OpenAI
import speech_recognition as sr 
import pyaudio

# Set API key 
client = OpenAI(
    api_key="",
) 

# Define the System Role
messages = [ {"role": "system", "content": "Your responses should not exceed five sentences in length."} ]

# Text prompt 
# user_prompt = input("Enter your question (or type 'exit' to quit): ")

# Set up microphone to record audio prompt 
recogniser = sr.Recognizer()
microphone = sr.Microphone(device_index= 0) # Change this according to your microphone

# Use the microphone to record audio
with microphone as source:
  print("Listening...")
  audio = recogniser.listen(source)
  try:
    user_prompt = recogniser.recognize_google(audio)
    print(f"This is your ChatGPT Prompt: {user_prompt}")
    messages.append({"role": "user", "content": user_prompt}) # Add prompt to the message to send to the model 
  except:
    print('Could not understand. Please try again.')

# Set up the model and send the user prompt
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages= messages
) 

# Print the model output 
print(response.choices[0].message)
