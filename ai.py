import requests
import json
from datetime import datetime

# Directly set the OpenAI API key
OPENAI_API_KEY = "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"
OPENAI_API_URL = "https://api.openai.com/v1/completions"
LOCAL_AI_URL = "http://localhost:11434/api/generate"

# Function to log responses to a file
def log_response(model_name, response):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {model_name}: {response}\n")

# Function to ask OpenAI model
def ask_openai(prompt):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        payload = {
            "model": "gpt-3.5-turbo",  # You can replace this with "gpt-4" if you have access
            "messages": [{"role": "user", "content": f"You are JARVIS. Reply concisely and helpfully.\n{prompt}"}],
            "max_tokens": 150
        }
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        
        # Debug: print the full response to inspect its structure
        data = response.json()
        print("OpenAI API Response:", json.dumps(data, indent=4))  # Add this line for debugging

        # Check if 'choices' exists in the response
        if 'choices' in data:
            return data['choices'][0]['message']['content']
        else:
            print("Error: 'choices' field is missing in the response.")
            return None
    except Exception as e:
        print(f"Error connecting to OpenAI API: {e}")
        return None

# Function to ask LLaMA model
def ask_llama(prompt):
    try:
        payload = {
            "model": "llama2",
            "prompt": f"You are Jarvis. Be short, polite, and helpful.\n{prompt}",
            "stream": False
        }
        res = requests.post(LOCAL_AI_URL, json=payload, timeout=30)
        llama_response = res.json().get("response", "No response.")
        # Log LLaMA response
        log_response("LLaMA", llama_response)
        return llama_response
    except Exception as e:
        print(f"Error connecting to local LLaMA model: {e}")
        return "Sir, local model is not responding."

# Function to ask either OpenAI or LLaMA based on availability
def ask_ai(prompt):
    if OPENAI_API_KEY:
        try:
            response = ask_openai(prompt)
            if response:
                return f"(OpenAI): Hi, sir, {response.strip()}"
        except Exception as e:
            print(f"Error connecting to OpenAI API: {e}")
    # Fallback to LLaMA if OpenAI doesn't respond
    return f"(LLaMA): Sir, {ask_llama(prompt).strip()}"

# Example usage
if __name__ == "__main__":
    prompt = "What's the weather like today?"
    response = ask_ai(prompt)
    print(response)
