import speech_recognition as sr
import pyttsx3
import winsound
import pygame
import time

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')

# Set a mild male voice
for voice in voices:
    if "male" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def play_notification():
    winsound.Beep(1000, 200)

def play_introduction():
    pygame.mixer.init()
    pygame.mixer.music.load("audio/jarvisIntro.mp3")  # Replace with your introduction audio file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def listen_for_wake_word():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for wake word...")
        while True:
            audio = recognizer.listen(source)
            try:
                trigger = recognizer.recognize_google(audio).lower()
                if "jarvis" in trigger:
                    play_notification()
                    play_introduction()
                    return
            except:
                continue

def get_command():
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print("Heard:", text)
            return text
        except:
            print("I didn't catch that, sir.")
            return None