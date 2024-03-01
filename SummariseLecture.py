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
    api_key="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",
) 

# Get a list of audio/video files in current working directory 
current_dir = os.getcwd()
files_and_dirs = os.listdir(current_dir)
files = [file for file in files_and_dirs if (file.endswith('.mp4') or file.endswith('.wav')) and os.path.isfile(os.path.join(current_dir, file))]

print(files)
'''
# Audio to text function 
def audio_2_text(temp_audio_file):
    recogniser = sr.Recognizer()

    # Set up the System Role
    messages = [ {"role": "system", "content": "Summarise topic of the meeting in one word"} ]

    with sr.AudioFile(temp_audio_file) as source:
        audio_data = recogniser.record(source)
        text = recogniser.recognize_google(audio_data)
        messages.append({"role": "user", "content": text}) 

    return messages

# Convert audio to text
def convert_files(files):
    messages = []
  
    for file in files:
        if file.endswith('4'):
            video = mp.VideoFileClip(file)
            audio = video.audio
            temp_audio_file = "temp.wav"
            audio.write_audiofile(temp_audio_file)
            text = audio_2_text(temp_audio_file) 
            messages.extend(text)
        else: 
            text = audio_2_text(file) 
            messages.extend(text)
    return messages


# Set up the model and send the user prompt
def generate_completion(input_data, model="gpt-3.5-turbo"):

    # Send the messages to the GPT-3.5 model
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages= input_data
    ) 

    # Return the generated completion
    return response.choices[0].message

input_data = convert_files(files)
response = generate_completion(input_data)
print(response)'''