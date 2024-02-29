# Summarise a Lecture and Its Conent 
# Author: Harrison Bailye
# Date: 29/02/2024
# This file takes in an audio file and summarises its contents 

# Import libaries 
from openai import OpenAI
import moviepy.editor as mp
import pandas as pd
import speech_recognition as sr 
import pyaudio

# Set API key 
client = OpenAI(
    api_key="",
) 

# Define the System Role
messages = [ {"role": "system", "content": "Your response should summarise the meeting."} ]

# Set up microphone to record audio prompt 
recogniser = sr.Recognizer()
microphone = sr.Microphone(device_index= 0) # Change this according to your microphone

# Define audio file
lecture_audio = 'Lecture.wav'
lecture_video = 'LectureVideo.MP4'

# MP4 to text 
video = mp.VideoFileClip(lecture_video)
audio = video.audio
temp_audio_file = "temp.wav"
audio.write_audiofile(temp_audio_file)


# Convert audio file 
with sr.AudioFile(temp_audio_file) as source:
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
