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

# FUNCTION - Audio to text function 
def audio_2_text(temp_audio_file):
    # Set up the System Role
    # messages = [ {"role": "system", "content": "Summarise topic of the meeting in under 10 words"} ]

    recogniser = sr.Recognizer()
    messages = []
    with sr.AudioFile(temp_audio_file) as source:
        audio_data = recogniser.record(source)
        text = recogniser.recognize_google(audio_data)
        messages.append({"role": "user", "content": text}) 
    return messages

# FUNCTION - Convert audio to text
def convert_files(files):
    messages = []
  
    for file in files:
        if file.endswith('.MP43'):
            video = mp.VideoFileClip(file)
            audio = video.audio
            temp_audio_file = "temp.wav"
            audio.write_audiofile(temp_audio_file)
            text = audio_2_text(temp_audio_file) 
            messages.extend(text)
        elif file.endswith('.wav'): 
            text = audio_2_text(file) 
            messages.extend(text)

    return messages


# FUNCTION - Set up the model and send the user prompt
def generate_completion(input_data, model="gpt-3.5-turbo"):
    completions = []
    max_tokens = 50  # Set the maximum token limit for each completion

    for message in input_data:
        # Set up the system role message
        system_message = {"role": "system", "content": "Summarise topic of the meeting in under 10 words"}
        
        # Create a new list for the system message
        system_data = [system_message]
        
        # Extend the input_data list with the system message list
        input_data.extend(system_data)

        # Send the message to the GPT-3.5 model
        response = client.chat.completions.create(
            model=model,
            messages=[message],
            max_tokens=max_tokens
        ) 

        # Append the generated completion to the list of completions
        completions.append(response.choices[0].message.content)

    # Return the list of completions
    return completions


# Get a list of audio/video files in current working directory 
current_dir = os.getcwd()
files_and_dirs = os.listdir(current_dir)
files = [file for file in files_and_dirs if (file.endswith('.MP4') or file.endswith('.wav')) and os.path.isfile(os.path.join(current_dir, file))]

# Call the functions 
input_data = convert_files(files)
responses = generate_completion(input_data)

# Print the model's response 
for response in responses:
  print(response)