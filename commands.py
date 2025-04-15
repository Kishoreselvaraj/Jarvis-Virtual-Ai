import os
import subprocess
import sys
import requests
import json
import time
import datetime
import psutil
import re
import speech
import ai
import utils
import memory
import temporary_memory

def handle_command(text):
    text = text.lower()

    if "remember" in text:
        parts = text.split("remember")
        key = parts[0].strip()
        value = parts[1].strip()
        temporary_memory.save_to_temporary_memory(key, value)
        speech.speak(f"I'll remember that, sir.")

    elif "do you remember" in text:
        key = text.replace("do you remember", "").strip()
        value = temporary_memory.recall_from_temporary_memory(key)
        speech.speak(value)

    elif "my name is" in text:
        name = text.split("my name is")[-1].strip()
        memory.save_to_memory("name", name)
        speech.speak(f"I'll remember that your name is {name}, sir.")

    elif "what is my name" in text:
        name = memory.recall_from_memory("name")
        speech.speak(f"Your name is {name}.")

    elif "create file" in text:
        file_name = text.replace("create file", "").strip()
        utils.create_file(file_name)

    elif "create folder" in text:
        folder_name = text.replace("create folder", "").strip()
        utils.create_folder(folder_name)

    elif "delete file" in text:
        file_name = text.replace("delete file", "").strip()
        utils.delete_file(file_name)

    elif "delete folder" in text:
        folder_name = text.replace("delete folder", "").strip()
        utils.delete_folder(folder_name)

    elif "rename file" in text:
        parts = text.split("to")
        old_name = parts[0].replace("rename file", "").strip()
        new_name = parts[1].strip()
        utils.rename_file(old_name, new_name)

    elif "rename folder" in text:
        parts = text.split("to")
        old_name = parts[0].replace("rename folder", "").strip()
        new_name = parts[1].strip()
        utils.rename_folder(old_name, new_name)

    elif "move file" in text:
        parts = text.split("to")
        source = parts[0].replace("move file", "").strip()
        destination = parts[1].strip()
        utils.move_file(source, destination)

    elif "move folder" in text:
        parts = text.split("to")
        source = parts[0].replace("move folder", "").strip()
        destination = parts[1].strip()
        utils.move_folder(source, destination)

    elif "open" in text:
        name = text.replace("open", "").strip()
        utils.open_software(name)

    elif "play" in text and any(kw in text for kw in ["music", "song"]):
        song_name = text.replace("play", "").replace("music", "").replace("song", "").strip()
        results = utils.find_file(song_name, [utils.MUSIC_FOLDER])
        if results:
            utils.play_media(results[0])
        else:
            speech.speak(f"I couldn't find {song_name}, sir.")

    elif "play" in text and any(kw in text for kw in ["video", "movie", "film"]):
        video_name = text.replace("play", "").replace("video", "").replace("movie", "").replace("film", "").strip()
        results = utils.find_file(video_name, [utils.VIDEOS_FOLDER])
        if results:
            utils.play_media(results[0], player="vlc")
        else:
            speech.speak(f"I couldn't find {video_name}, sir.")

    elif "find file" in text:
        file_name = text.replace("find file", "").strip()
        results = utils.find_file(file_name, [utils.DESKTOP_FOLDER, utils.DOCUMENTS_FOLDER, utils.DOWNLOADS_FOLDER])
        if results:
            speech.speak(f"Found {file_name}, sir. Opening location.")
            subprocess.Popen(f'explorer /select,"{results[0]}"')
        else:
            speech.speak("File not found, sir.")

    elif "note" in text or "remember" in text:
        note = text.replace("note", "").replace("remember", "").strip()
        with open("note.txt", "a") as f:
            f.write(f"{datetime.datetime.now()}: {note}\n")
        speech.speak(f"Noted: {note}, sir.")

    elif "search" in text:
        query = text.replace("search", "").strip().replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"
        path = utils.get_program_path("chrome")
        if path:
            subprocess.Popen([path, url])
        else:
            subprocess.Popen(['start', url], shell=True)
        speech.speak(f"Searching Google for {query.replace('+', ' ')}, sir.")

    elif "what" in text or "who" in text or "how" in text:
        response = ai.ask_ai(text)
        speech.speak(response)

    elif "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speech.speak(f"The time is {now}, sir.")

    elif "date" in text:
        date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speech.speak(f"Today is {date}, sir.")

    elif "system status" in text or "usage" in text:
        speech.speak(utils.get_system_status())

    elif "create project folder" in text:
        project_folder = os.path.join(utils.DOCUMENTS_FOLDER, "project")
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
            speech.speak("Project folder created, sir.")
        else:
            speech.speak("Project folder already exists, sir.")

    elif "open project folder in vs code" in text:
        project_folder = os.path.join(utils.DOCUMENTS_FOLDER, "project")
        if os.path.exists(project_folder):
            path = utils.get_program_path("vscode")
            if path:
                speech.speak("Opening project folder in VS Code, sir.")
                subprocess.Popen([path, project_folder])
            else:
                speech.speak("VS Code not found, sir.")
        else:
            speech.speak("Project folder does not exist, sir.")

    elif "stop" in text or "exit" in text:
        speech.speak("Shutting down, sir.")
        sys.exit()

    else:
        response = ai.ask_ai(text)
        speech.speak(response)