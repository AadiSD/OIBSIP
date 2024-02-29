import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")


        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 500) // 2
        y = (screen_height - 300) // 2

        self.root.geometry(f"500x300+{x}+{y}")
        self.text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=58, height=14)
        self.text_box.grid(row=0, column=0, padx=10, pady=10)
        self.listen_button = tk.Button(root, text="Listen", command=self.listen_command)
        self.listen_button.grid(row=1, column=0, padx=10, pady=10)

        # Initialize speech recognition and text-to-speech engines
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_command(self):
        self.text_box.insert(tk.END, "Listening...\n")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            self.text_box.insert(tk.END, "Recognizing...\n")
            command = self.recognizer.recognize_google(audio).lower()
            self.text_box.insert(tk.END, f"You said: {command}\n")
            self.execute_command(command)
        except sr.UnknownValueError:
            self.text_box.insert(tk.END, "Sorry, I didn't catch that. Can you please repeat?\n")
        except sr.RequestError as e:
            self.text_box.insert(tk.END, f"Error connecting to Google Speech Recognition service: {e}\n")

    def execute_command(self, command):
        if command is not None and command.strip():
            if "hello" in command:
                self.speak("Hello! How can I assist you today?")
            elif "time" in command:
                current_time = datetime.datetime.now().strftime("%H:%M")
                self.speak(f"The current time is {current_time}")
            elif "date" in command:
                current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                self.speak(f"Today's date is {current_date}")
            elif "search" in command:
                search_query = command.replace("search", "").strip()
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                self.speak(f"Here are the search results for {search_query}")
            elif "exit" in command or "quit" in command:
                self.speak("Goodbye! Have a great day.")
                exit()
            else:
                self.speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistant(root)
    root.mainloop()
