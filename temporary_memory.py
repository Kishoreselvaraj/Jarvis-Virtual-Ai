temporary_memory = {}

def save_to_temporary_memory(key, value):
    temporary_memory[key] = value

def recall_from_temporary_memory(key):
    return temporary_memory.get(key, "I don't remember that, sir.")