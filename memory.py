import os
import json

memory_file = "jarvis_memory.json"
if not os.path.exists(memory_file):
    with open(memory_file, "w") as f:
        json.dump({}, f)

def save_to_memory(key, value):
    with open(memory_file, "r") as f:
        data = json.load(f)
    data[key] = value
    with open(memory_file, "w") as f:
        json.dump(data, f)

def recall_from_memory(key):
    with open(memory_file, "r") as f:
        data = json.load(f)
    return data.get(key, "I don't remember that, sir.")