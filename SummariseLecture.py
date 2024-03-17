# Summarise a Lecture and Its Conent 
# Author: Harrison Bailye
# Date: 29/02/2024
# This file takes in an audio or video file and summarises its contents 

# Import libaries 
from openai import OpenAI
import moviepy.editor as mp
import speech_recognition as sr 
import os 

# Set API key 
client = OpenAI(
    api_key="",
)

# FUNCTION - Audio to text function 
def audio_2_text(temp_audio_file):

    recogniser = sr.Recognizer()
    messages = []

    with sr.AudioFile(temp_audio_file) as source:
        audio_data = recogniser.record(source)
        text = recogniser.recognize_google(audio_data)
        messages.append({"role": "user", "content": text}) 

    return messages

# FUNCTION - Convert files to correct format and then call the Audio_2_Text function
def convert_files(file):
    messages = []
    temp_audio_file = "temp.wav"

    try:
        if file.lower().endswith('.wav'): # Can convert wav files to text straight away 
            text = audio_2_text(file)
            messages.extend(text)
        elif file.lower().endswith(('.mp4', '.mp3', '.m4a')): # have to to convert mp4 and mp3 before converting them to text 
            video = mp.VideoFileClip(file) if file.lower().endswith(('.mp4')) else None
            audio = video.audio if video else mp.AudioFileClip(file)
            audio.write_audiofile(temp_audio_file)
            text = audio_2_text(temp_audio_file)
            messages.extend(text)
    except Exception as e:
        print(f"Error processing file {file}: {e}")
    finally:
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)  # Delete temp audio file after processing

    return messages


# FUNCTION - Set up the model and send the text from the files
def generate_completion(input_data, model="gpt-3.5-turbo"):
    completions = []
    max_tokens = 50  # Set the maximum token limit for each completion

    # Set up the system role message and add to a new list combining input data and system message
    system_message = {"role": "system", "content": "Summarise topic of the lecture in dot points"}
    combined_data = input_data + [system_message]

    # Send the message to the GPT-3.5 model
    response = client.chat.completions.create(
        model=model,
        messages=combined_data,
        max_tokens=max_tokens
    ) 

    # Append the generated completion to the list of completions
    completions.append(response.choices[0].message.content)

    # Return the list of completions
    return completions


# Get a list of audio/video files in TestData working directory 
current_dir = os.path.join(os.getcwd(), "TestData")
files = [file for file in os.listdir(current_dir) if (file.endswith('.MP4') or file.endswith('.wav') or file.endswith('.mp3') or file.endswith('.m4a')) and os.path.isfile(os.path.join(current_dir, file))]

# Call the functions and print responses 
for file in files:
    input_data = convert_files(os.path.join(current_dir, file))
    responses = generate_completion(input_data)
    print(f"{file} Summary: {responses}")
