import os
import subprocess
import sys
import requests
import json
import time
import datetime
import psutil
import re
import shutil
import speech
import ai
import utils
import memory
import temporary_memory

def handle_command(text):
    text = text.lower()

    # File Explorer Navigation Commands
    if "open drive" in text:
        drive_letter = text.replace("open drive", "").strip().upper()
        if drive_letter and drive_letter[-1] != ":":
            drive_letter = drive_letter + ":"
        
        if os.path.exists(drive_letter + "\\"):
            subprocess.Popen(f'explorer {drive_letter}\\')
            speech.speak(f"Opening {drive_letter} drive, sir.")
        else:
            speech.speak(f"Drive {drive_letter} not found, sir.")
    
    elif "open folder" in text or "open directory" in text:
        folder_path = text.replace("open folder", "").replace("open directory", "").strip()
        
        if os.path.exists(folder_path):
            subprocess.Popen(f'explorer "{folder_path}"')
            speech.speak(f"Opening folder {folder_path}, sir.")
        else:
            speech.speak(f"Folder {folder_path} not found, sir.")
    
    elif "file manager" in text:
        path = text.replace("explore", "").strip()
        if path == "":
            # Open default file explorer
            subprocess.Popen('explorer')
            speech.speak("Opening file explorer, sir.")
        elif os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')
            speech.speak(f"Exploring {path}, sir.")
        else:
            speech.speak(f"Path {path} not found, sir.")
    
    elif "go to" in text and ("folder" in text or "directory" in text or "drive" in text):
        path = text.replace("go to", "").replace("folder", "").replace("directory", "").replace("drive", "").strip()
        if path and path[-1] == ":":
            path = path + "\\"
        
        if os.path.exists(path):
            subprocess.Popen(f'explorer "{path}"')
            speech.speak(f"Navigating to {path}, sir.")
        else:
            speech.speak(f"Path {path} not found, sir.")
    
    elif "remember" in text:
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

    # File and Folder Management
    elif "create file" in text:
        file_path = text.replace("create file", "").strip()
        
        # Check if path is specified (contains "in" or has drive letter)
        if " in " in file_path:
            parts = file_path.split(" in ")
            file_name = parts[0].strip()
            location = parts[1].strip()
            # Combine location and file name
            full_path = os.path.join(location, file_name)
            utils.create_file(full_path)
            speech.speak(f"Created file {file_name} in {location}, sir.")
        elif ":" in file_path:  # Contains drive letter like D:
            # This is already a full path
            utils.create_file(file_path)
            speech.speak(f"Created file at {file_path}, sir.")
        else:
            # Default behavior - create in current directory
            utils.create_file(file_path)
            speech.speak(f"Created file {file_path}, sir.")

    elif "create folder" in text:
        folder_path = text.replace("create folder", "").strip()
        
        # Check if path is specified (contains "in" or has drive letter)
        if " in " in folder_path:
            parts = folder_path.split(" in ")
            folder_name = parts[0].strip()
            location = parts[1].strip()
            # Combine location and folder name
            full_path = os.path.join(location, folder_name)
            utils.create_folder(full_path)
            speech.speak(f"Created folder {folder_name} in {location}, sir.")
        elif ":" in folder_path:  # Contains drive letter like D:
            # This is already a full path
            utils.create_folder(folder_path)
            speech.speak(f"Created folder at {folder_path}, sir.")
        else:
            # Default behavior - create in current directory
            utils.create_folder(folder_path)
            speech.speak(f"Created folder {folder_path}, sir.")

    elif "delete file" in text:
        file_path = text.replace("delete file", "").strip()
        utils.delete_file(file_path)
        speech.speak(f"Deleted file {file_path}, sir.")

    elif "delete folder" in text:
        folder_path = text.replace("delete folder", "").strip()
        utils.delete_folder(folder_path)
        speech.speak(f"Deleted folder {folder_path}, sir.")

    elif "rename file" in text:
        if " to " in text:
            parts = text.split(" to ")
            old_name = parts[0].replace("rename file", "").strip()
            new_name = parts[1].strip()
            utils.rename_file(old_name, new_name)
            speech.speak(f"Renamed file from {old_name} to {new_name}, sir.")
        else:
            speech.speak("Please specify old and new names separated by 'to', sir.")
            
    elif "copy" in text and "to" in text:
        parts = text.split("to")
        source = parts[0].replace("copy", "").strip()
        destination = parts[1].strip()
        utils.copy_file(source, destination)
        speech.speak(f"Copied {source} to {destination}, sir.")

    elif "paste" in text:
        clipboard_content = utils.get_clipboard_content()
        if clipboard_content:
            destination = text.replace("paste", "").strip()
            utils.paste_content(clipboard_content, destination)
            speech.speak(f"Pasted content to {destination}, sir.")
        else:
            speech.speak("Clipboard is empty, sir.")
            
    elif "rename folder" in text:
        if " to " in text:
            parts = text.split(" to ")
            old_name = parts[0].replace("rename folder", "").strip()
            new_name = parts[1].strip()
            utils.rename_folder(old_name, new_name)
            speech.speak(f"Renamed folder from {old_name} to {new_name}, sir.")
        else:
            speech.speak("Please specify old and new names separated by 'to', sir.")

    elif "move file" in text:
        if " to " in text:
            parts = text.split(" to ")
            source = parts[0].replace("move file", "").strip()
            destination = parts[1].strip()
            utils.move_file(source, destination)
            speech.speak(f"Moved file from {source} to {destination}, sir.")
        else:
            speech.speak("Please specify source and destination separated by 'to', sir.")

    elif "move folder" in text:
        if " to " in text:
            parts = text.split(" to ")
            source = parts[0].replace("move folder", "").strip()
            destination = parts[1].strip()
            utils.move_folder(source, destination)
            speech.speak(f"Moved folder from {source} to {destination}, sir.")
        else:
            speech.speak("Please specify source and destination separated by 'to', sir.")

    # List Directory Contents
    elif "list" in text and ("folder" in text or "directory" in text or "files" in text or "drive" in text):
        path = text.replace("list", "").replace("folder", "").replace("directory", "").replace("files", "").replace("drive", "").replace("in", "").strip()
        
        if path == "":
            path = os.getcwd()
        
        if os.path.exists(path):
            items = os.listdir(path)
            if items:
                speech.speak(f"Contents of {path}:")
                for item in items[:10]:  # Limit to first 10 items to avoid long speeches
                    full_path = os.path.join(path, item)
                    item_type = "Folder" if os.path.isdir(full_path) else "File"
                    speech.speak(f"{item_type}: {item}")
                
                if len(items) > 10:
                    speech.speak(f"And {len(items) - 10} more items, sir.")
            else:
                speech.speak(f"The directory {path} is empty, sir.")
        else:
            speech.speak(f"Path {path} not found, sir.")

    # Software and Media Controls
    elif "open" in text:
        name = text.replace("open", "").strip()
        utils.open_software(name)
        speech.speak(f"Opening {name}, sir.")

    elif "play" in text and any(kw in text for kw in ["music", "song"]):
        song_name = text.replace("play", "").replace("music", "").replace("song", "").strip()
        results = utils.find_file(song_name, [utils.MUSIC_FOLDER])
        if results:
            utils.play_media(results[0])
            speech.speak(f"Playing {song_name}, sir.")
        else:
            speech.speak(f"I couldn't find {song_name}, sir.")

    elif "play" in text and any(kw in text for kw in ["video", "movie", "film"]):
        video_name = text.replace("play", "").replace("video", "").replace("movie", "").replace("film", "").strip()
        results = utils.find_file(video_name, [utils.VIDEOS_FOLDER])
        if results:
            utils.play_media(results[0], player="vlc")
            speech.speak(f"Playing {video_name}, sir.")
        else:
            speech.speak(f"I couldn't find {video_name}, sir.")

    elif "find file" in text:
        file_name = text.replace("find file", "").strip()
        
        # Check if search path is specified
        search_paths = [utils.DESKTOP_FOLDER, utils.DOCUMENTS_FOLDER, utils.DOWNLOADS_FOLDER]
        if " in " in file_name:
            parts = file_name.split(" in ")
            file_name = parts[0].strip()
            search_path = parts[1].strip()
            search_paths = [search_path]
        
        results = utils.find_file(file_name, search_paths)
        if results:
            speech.speak(f"Found {file_name}, sir. Opening location.")
            subprocess.Popen(f'explorer /select,"{results[0]}"')
        else:
            speech.speak("File not found, sir.")

    # Windows System Commands
    elif "check disk space" in text:
        drive = text.replace("check disk space", "").replace("on", "").strip()
        if not drive:
            drive = "C:"
        elif drive[-1] != ":":
            drive = drive + ":"
        
        if os.path.exists(drive):
            total, used, free = shutil.disk_usage(drive)
            speech.speak(f"{drive} drive has {free // (2**30)} GB free out of {total // (2**30)} GB total, sir.")
        else:
            speech.speak(f"Drive {drive} not found, sir.")
    
    elif "system info" in text or "computer info" in text:
        info = utils.get_system_info()
        speech.speak(info)
    
    elif text in ["task manager", "open task manager"]:
        subprocess.Popen("taskmgr.exe")
        speech.speak("Opening task manager, sir.")
    
    elif "kill process" in text or "end process" in text or "terminate process" in text:
        process_name = text.replace("kill process", "").replace("end process", "").replace("terminate process", "").strip()
        if process_name:
            try:
                os.system(f"taskkill /F /IM {process_name}")
                speech.speak(f"Terminated process {process_name}, sir.")
            except:
                speech.speak(f"Failed to terminate process {process_name}, sir.")
        else:
            speech.speak("Please specify a process name, sir.")
    
    elif "restart computer" in text:
        confirmation = input("Are you sure you want to restart the computer? (yes/no): ")
        if confirmation.lower() == "yes":
            speech.speak("Restarting computer, sir.")
            os.system("shutdown /r /t 10")
        else:
            speech.speak("Restart cancelled, sir.")
    
    elif "shutdown computer" in text:
        confirmation = input("Are you sure you want to shut down the computer? (yes/no): ")
        if confirmation.lower() == "yes":
            speech.speak("Shutting down computer, sir.")
            os.system("shutdown /s /t 10")
        else:
            speech.speak("Shutdown cancelled, sir.")
    
    elif "cancel shutdown" in text:
        os.system("shutdown /a")
        speech.speak("Shutdown cancelled, sir.")

    # Misc and AI Commands
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
        project_name = text.replace("create project folder", "").strip()
        if not project_name:
            project_name = "project"
        
        project_folder = os.path.join(utils.DOCUMENTS_FOLDER, project_name)
        if not os.path.exists(project_folder):
            os.makedirs(project_folder)
            speech.speak(f"{project_name} folder created, sir.")
        else:
            speech.speak(f"{project_name} folder already exists, sir.")

    elif "open project folder in vs code" in text:
        project_name = text.replace("open project folder in vs code", "").strip()
        if not project_name:
            project_name = "project"
        
        project_folder = os.path.join(utils.DOCUMENTS_FOLDER, project_name)
        if os.path.exists(project_folder):
            path = utils.get_program_path("vscode")
            if path:
                speech.speak(f"Opening {project_name} folder in VS Code, sir.")
                subprocess.Popen([path, project_folder])
            else:
                speech.speak("VS Code not found, sir.")
        else:
            speech.speak(f"{project_name} folder does not exist, sir.")

    elif any(cmd in text for cmd in ["stop", "exit", "quit", "goodbye"]):
        speech.speak("Shutting down, sir.")
        sys.exit()

    else:
        response = ai.ask_ai(text)
        speech.speak(response)