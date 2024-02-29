# Summarise a Lecture and Its Conent 
# Author: Harrison Bailye
# Date: 29/02/2024
# This file takes in an audio file and summarises its contents 

# Import libaries 
from openai import OpenAI
import moviepy.editor as mp
import speech_recognition as sr 
import pyaudio
import os 

# Set API key 
client = OpenAI(
    api_key="",
) 

# Set up the System Role
messages = [ {"role": "system", "content": "Summarise the meeting in one sentence."} ]

# Set up microphone to record audio prompt 
recogniser = sr.Recognizer()
microphone = sr.Microphone(device_index= 0) # Change this according to your microphone

# Get a list of files in current working directory 
current_dir = os.getcwd()
files_and_dirs = os.listdir(current_dir)

# Filter out only the mp4 and wav files
files = [file for file in files_and_dirs if file.endswith('.mp4') or file.endswith('.wav') and os.path.isfile(os.path.join(current_dir, file))]



# Audio to text function 
def audio_2_text(temp_audio_file):
    recogniser = sr.Recognizer()
    messages = []

    with sr.AudioFile(temp_audio_file) as source:
        audio_data = recogniser.record(source)
        text = recogniser.recognize_google(audio_data)
        messages.append({"role": "user", "content": text}) 

    return messages

# Convert audio to text
def convert_files(files):
  
  for file in files:
    if file.endswith('4'):
      video = mp.VideoFileClip(file)
      audio = video.audio
      temp_audio_file = "temp.wav"
      audio.write_audiofile(temp_audio_file)
      
      text = audio_2_text(temp_audio_file) 
      print(text)
    else: 
      text = audio_2_text(file) 
      print(text)
     

print(convert_files(files))



'''
# Set up the model and send the user prompt
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages= messages
) 

# Print the model output 
print(response.choices[0].message)
'''