# Summarise a Lecture and Its Conent 
# Author: Harrison Bailye
# Date: 29/02/2024
# This file takes in an audio file and summarises its contents 

# Import libaries 
from openai import OpenAI
import pandas as pd
import speech_recognition as sr 
import pyaudio

# Set API key 
client = OpenAI(
    api_key="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",
) 

# Define the System Role
messages = [ {"role": "system", "content": "Your responses should summarise everything in one sentence."} ]

# Set up microphone to record audio prompt 
recogniser = sr.Recognizer()
microphone = sr.Microphone(device_index= 0) # Change this according to your microphone

# Define audio file
lecture_audio = 'Lecture.wav'

# Convert audio file 
with sr.AudioFile(lecture_audio) as source:
    audio_data = recogniser.record(source)
    text = recogniser.recognize_google(audio_data)
    messages.append({"role": "user", "content": text}) 

# Set up the model and send the user prompt
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages= messages
) 

# Print the model output 
print(response.choices[0].message)
