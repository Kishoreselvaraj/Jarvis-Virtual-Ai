import os
import subprocess
import sys
import requests
import json
import psutil
import re
import shutil

USER_HOME = os.path.expanduser("~")
DOWNLOADS_FOLDER = os.path.join(USER_HOME, "Downloads")
DOCUMENTS_FOLDER = os.path.join(USER_HOME, "Documents")
DESKTOP_FOLDER = os.path.join(USER_HOME, "Desktop")
VIDEOS_FOLDER = os.path.join(USER_HOME, "Videos")
MUSIC_FOLDER = os.path.join(USER_HOME, "Music")
PICTURES_FOLDER = os.path.join(USER_HOME, "Pictures")

def create_file(file_path):
    try:
        with open(file_path, 'w') as file:
            file.write("")  # Create an empty file
        print(f"File '{file_path}' created successfully.")
    except Exception as e:
        print(f"Error creating file: {e}")

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"Folder '{folder_path}' created successfully.")
    except Exception as e:
        print(f"Error creating folder: {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"Error deleting file: {e}")

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Folder '{folder_path}' not found.")
    except Exception as e:
        print(f"Error deleting folder: {e}")

def rename_file(old_path, new_path):
    try:
        os.rename(old_path, new_path)
        print(f"File '{old_path}' renamed to '{new_path}' successfully.")
    except FileNotFoundError:
        print(f"File '{old_path}' not found.")
    except Exception as e:
        print(f"Error renaming file: {e}")

def rename_folder(old_path, new_path):
    try:
        os.rename(old_path, new_path)
        print(f"Folder '{old_path}' renamed to '{new_path}' successfully.")
    except FileNotFoundError:
        print(f"Folder '{old_path}' not found.")
    except Exception as e:
        print(f"Error renaming folder: {e}")

def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        print(f"File '{source_path}' moved to '{destination_path}' successfully.")
    except FileNotFoundError:
        print(f"File '{source_path}' not found.")
    except Exception as e:
        print(f"Error moving file: {e}")

def move_folder(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        print(f"Folder '{source_path}' moved to '{destination_path}' successfully.")
    except FileNotFoundError:
        print(f"Folder '{source_path}' not found.")
    except Exception as e:
        print(f"Error moving folder: {e}")

def get_program_path(program):
    program_paths = {
        "vscode": [
            rf"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        ],
        "chrome": [
            r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
        ],
        "explorer": [r"C:\\Windows\\explorer.exe"]
    }
    paths = program_paths.get(program.lower(), [])
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def open_software(name):
    folder_map = {
        "downloads": DOWNLOADS_FOLDER,
        "documents": DOCUMENTS_FOLDER,
        "desktop": DESKTOP_FOLDER,
        "music": MUSIC_FOLDER,
        "pictures": PICTURES_FOLDER,
        "videos": VIDEOS_FOLDER,
        "project": os.path.join(DOCUMENTS_FOLDER, "project")  # Customize your folder name
    }

    if name in folder_map:
        path = folder_map[name]
        if os.path.exists(path):
            print(f"Opening {name} folder, sir.")
            subprocess.Popen(f'explorer "{path}"')
        else:
            print(f"I couldn't find the {name} folder, sir.")
    elif "file manager" in name or "explorer" in name:
        print("Opening File Explorer.")
        subprocess.Popen("explorer")
    elif "code" in name or "vs code" in name:
        path = get_program_path("vscode")
        if path:
            print("Opening Visual Studio Code.")
            subprocess.Popen([path])
        else:
            print("VS Code not found, sir.")
    elif "vlc" in name:
        path = get_program_path("vlc")
        if path:
            print("Opening VLC Media Player.")
            subprocess.Popen([path])
        else:
            print("VLC Media Player not found, sir.")
    elif "chrome" in name:
        path = get_program_path("chrome")
        if path:
            print("Opening Google Chrome.")
            subprocess.Popen([path])
        else:
            print("Google Chrome not found, sir.")
    else:
        try:
            subprocess.Popen(name)
            print(f"Opening {name}, sir.")
        except:
            print(f"I couldn't open {name}, sir.")
            
def find_file(file_name, search_dirs):
    found_files = []
    for folder in search_dirs:
        if os.path.exists(folder):
            for root, dirs, files in os.walk(folder):
                for file in files:
                    if file_name.lower() in file.lower():
                        found_files.append(os.path.join(root, file))
                    if len(found_files) >= 5:
                        break
    return found_files

def play_media(file_path, player="vlc"):
    if os.path.exists(file_path):
        subprocess.Popen([file_path])
        print(f"Playing {os.path.basename(file_path)}.")
    else:
        print("File not found, sir.")

def get_system_status():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return f"Sir, CPU usage is {cpu} percent, memory at {mem} percent, and disk usage is {disk} percent."