# Create a Graphical User Interface where we can integrate speech 2 ChatGPT 

# Import libararies 
import tkinter as tk
import speech_recognition as sr
from openai import OpenAI

# Set API key 
client = OpenAI(
    api_key="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",
) 

def call_chatGPT(user_prompt):
    if user_prompt.strip() != "":
        # Prepare messages for ChatGPT
        messages = [{"role": "user", "content": user_prompt}, {"role": "system", "content": "Your responses should not exceed five sentences in length."}]

        # Call OpenAI API to generate response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Extract the content of the response message
        chatGPT_response = response.choices[0].message.content

        # Extract the text from the content string
        chatGPT_response_text = chatGPT_response.split('=')[-1].strip().strip("'").strip()

        return chatGPT_response_text
    else:
        return "Please enter a prompt."


def audio_prompt():
    # Set up microphone to record audio prompt
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Use the microphone to record audio
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        user_prompt = recognizer.recognize_google(audio)
        print(f"This is your ChatGPT Prompt: {user_prompt}")
        text_area.insert(tk.END, "Your prompt (from audio): " + user_prompt + "\n", "white")  # Insert user prompt in white text

        # Call the function to interact with ChatGPT
        chatGPT_response = call_chatGPT(user_prompt)

        print("ChatGPT response:", chatGPT_response)
        # Insert ChatGPT response in lighter blue text
        text_area.insert(tk.END, "ChatGPT response: " + chatGPT_response + "\n\n", "light_blue")

    except sr.UnknownValueError:
        print('Could not understand audio. Please try again.')
        text_area.insert(tk.END, "Could not understand audio. Please try again.\n\n")


def submit_prompt(event=None):
    user_prompt = prompt_entry.get()
    if user_prompt.strip() != "":
        print("Your prompt:", user_prompt)
        text_area.insert(tk.END, "Your prompt (typed): " + user_prompt + "\n", "white")  # Insert user prompt in white text

        # Call the function to interact with ChatGPT
        chatGPT_response = call_chatGPT(user_prompt)

        print("ChatGPT response:", chatGPT_response)
        # Insert ChatGPT response in lighter blue text
        text_area.insert(tk.END, "ChatGPT response: " + chatGPT_response + "\n\n", "light_blue")

        prompt_entry.delete(0, tk.END)  # Clear the entry widget after submitting the prompt
    else:
        print("Please enter a prompt.")

root = tk.Tk()
root.title("ChatGPT Prompt")

# Set window size and position
window_width = 600
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width / 2) - (window_width / 2)
y_coordinate = (screen_height / 2) - (window_height / 2)
root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

# Set window background color
root.configure(bg="black")

# Audio Prompt Button
audio_button = tk.Button(root, text="Audio Prompt", command=audio_prompt, font=("Arial", 14), bg="#4CAF50",
                         fg="white", padx=10, pady=5)
audio_button.pack(side=tk.TOP, pady=5)

# Label for the entry widget
entry_label = tk.Label(root, text="Type your prompt here:", font=("Arial", 12), bg="black", fg="white", anchor="w")
entry_label.pack(side=tk.TOP, pady=(10, 0), padx=10, fill='x')

# Entry widget for typing the prompt
prompt_entry = tk.Entry(root, font=("Arial", 12))
prompt_entry.pack(expand=False, fill="x", padx=10, pady=(0, 10))
prompt_entry.bind("<Return>", submit_prompt)  # Bind Enter key to submit_prompt function

# Text area for displaying prompts and responses
text_area = tk.Text(root, font=("Arial", 12), wrap="word", bg="black", fg="white")
text_area.pack(expand=True, fill="both", padx=10, pady=10)

# Configure text colors for model output 
text_area.tag_configure("light_blue", foreground="#ADD8E6") 

root.mainloop()