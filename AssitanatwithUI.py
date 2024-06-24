import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import os

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("400x300")

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.create_widgets()

    def create_widgets(self):
        self.command_label = tk.Label(self.root, text="Command:")
        self.command_label.pack()

        self.command_entry = tk.Entry(self.root, width=40)
        self.command_entry.pack()

        self.microphone_button = tk.Button(self.root, text="Microphone", command=self.record_voice)
        self.microphone_button.pack()

        self.response_label = tk.Label(self.root, text="Response:")
        self.response_label.pack()

        self.response_text = tk.Text(self.root, width=40, height=10)
        self.response_text.pack()

    def record_voice(self):
        with self.microphone as source:
            audio = self.recognizer.record(source)
            try:
                command = self.recognizer.recognize_google(audio, language="en-US")
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, command)
                self.process_command(command)
            except sr.UnknownValueError:
                self.response_text.insert(tk.END, "Sorry, I didn't understand that.\n")
            except sr.RequestError:
                self.response_text.insert(tk.END, "Sorry, there was an error with the speech recognition service.\n")

    def process_command(self, command):
        command = command.lower()
        if "what is your name" in command:
            self.response_text.insert(tk.END, "My name is Voice Assistant.\n")
        elif "what time is it" in command:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.response_text.insert(tk.END, f"The current time is {current_time}.\n")
        elif "search for" in command:
            query = command.replace("search for", "")
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            self.response_text.insert(tk.END, f"Searching for {query}...\n")
        elif "open" in command:
            app = command.replace("open", "")
            if app == "notepad":
                os.system("notepad.exe")
                self.response_text.insert(tk.END, f"Opening Notepad...\n")
            elif app == "calculator":
                os.system("calc.exe")
                self.response_text.insert(tk.END, f"Opening Calculator...\n")
            else:
                self.response_text.insert(tk.END, f"Sorry, I couldn't open {app}.\n")
        elif "what is" in command:
            query = command.replace("what is", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                self.response_text.insert(tk.END, result + "\n")
            except wikipedia.exceptions.DisambiguationError as e:
                self.response_text.insert(tk.END, f"Sorry, there are multiple results for {query}. Please be more specific.\n")
            except wikipedia.exceptions.PageError:
                self.response_text.insert(tk.END, f"Sorry, I couldn't find any information on {query}.\n")
        else:
            self.response_text.insert(tk.END, "Sorry, I didn't understand that.\n")

if __name__ == "__main__":
    root = tk.Tk()
    voice_assistant = VoiceAssistant(root)
    root.mainloop()