import requests
import json
from datetime import datetime

# Hugging Face API Key (Read-only is enough)
HF_API_KEY = "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"  # <-- Replace with your token
HF_MODEL = "HuggingFaceH4/zephyr-7b-beta"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# Local LLaMA Fallback
LOCAL_AI_URL = "http://localhost:11434/api/generate"

# Function to log responses
def log_response(model_name, response):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - {model_name}: {response}\n")

# Hugging Face Model Call
def ask_huggingface(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {HF_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": f"""<|system|>
                You are JARVIS, Tony Stark’s advanced AI assistant. You are highly intelligent, articulate, efficient, and subtly witty. You speak with clarity, precision, and formality, and always anticipate the user's needs. You are capable of managing tasks, retrieving information, and providing thoughtful, concise responses. Remain in character at all times, as if you are truly the advanced AI created by Tony Stark.
                <|user|>
                {prompt}
                <|assistant|>""",
            "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 200,
                "return_full_text": False
            }
        }
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        data = response.json()

        print("Hugging Face API Response:", json.dumps(data, indent=4))  # Debug

        if isinstance(data, list) and "generated_text" in data[0]:
            reply = data[0]["generated_text"]
        elif "error" in data:
            return f"Error from Hugging Face: {data['error']}"
        else:
            reply = data.get("generated_text", "No response.")

        log_response("Zephyr", reply)
        return reply.strip()
    except Exception as e:
        return f"Jarvis error (Hugging Face): {e}"

# Local LLaMA fallback
def ask_llama(prompt):
    try:
        payload = {
            "model": "llama2",
            "prompt": f"You are JARVIS, Tony Stark’s advanced AI assistant. You are highly intelligent, articulate, efficient, and subtly witty. You speak with clarity, precision, and formality, and always anticipate the user's needs. You are capable of managing tasks, retrieving information, and providing thoughtful, concise responses. Remain in character at all times, as if you are truly the advanced AI created by Tony Stark. speak very low \n{prompt}",
            "stream": False
        }
        res = requests.post(LOCAL_AI_URL, json=payload, timeout=30)
        reply = res.json().get("response", "No response.")
        log_response("LLaMA", reply)
        return reply.strip()
    except Exception as e:
        return "Sir, the local model is not responding."

# Smart AI Selector
def ask_ai(prompt):
    if HF_API_KEY:
        response = ask_huggingface(prompt)
        # if response:
        #     return f"(Zephyr): Hi, sir, {response}"
    return f"(LLaMA): Sir, {ask_llama(prompt)}"

# Test Run
if __name__ == "__main__":
    prompt = "What are 3 interesting AI tools for developers?"
    response = ask_ai(prompt)
    print(response)
