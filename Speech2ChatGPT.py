# Exploration of OpenAI API to ChatGPT model 
# Author: Harrison Bailye
# Date: 29/02/2024

# Import libaries 
from openai import OpenAI
import os
import pandas as pd
import speech_recognition as sr 
import pyaudio

# Set API key 
client = OpenAI(
    api_key="",
) 

# Define the System Role
messages = [ {"role": "system", "content": "Your responses should not exceed five sentences in length."} ]

# Get user input & add to messages array to send to the model
recogniser = sr.Recognizer()
device_index = 0  # Change this according to your microphone
microphone = sr.Microphone(device_index=device_index)

# Use the microphone to record audio
with microphone as source:
    print("Listening...")
    audio = recogniser.listen(source)
    user_prompt = recogniser.recognize_google(audio)
    print(f"This is your ChatGPT Prompt: {user_prompt}")


# User types prompt
# user_prompt = input("Enter your question (or type 'exit' to quit): ")
messages.append({"role": "user", "content": user_prompt})

# Set up the model and send user messages 
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages= messages
) 

# Print the model output 
print(response.choices[0].message)
