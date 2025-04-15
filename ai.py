import os
import requests
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-pro:generateContent"
LOCAL_AI_URL = "http://localhost:11434/api/generate"

def ask_gemini(prompt):
    try:
        headers = {"Content-Type": "application/json"}
        url = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": f"You are JARVIS. Reply concisely and helpfully.\n{prompt}"}]}]
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except:
        return None

def ask_llama(prompt):
    try:
        payload = {
            "model": "llama2",
            "prompt": f"You are Jarvis. Be short, polite, and helpful.\n{prompt}",
            "stream": False
        }
        res = requests.post(LOCAL_AI_URL, json=payload, timeout=30)
        return res.json().get("response", "No response.")
    except:
        return "Sir, local model is not responding."

def ask_ai(prompt):
    if GEMINI_API_KEY:
        try:
            response = ask_gemini(prompt)
            if response:
                return f"Hi, sir, {response.strip()}"
        except Exception as e:
            print(f"Error connecting to Gemini AI: {e}")
            pass
    return f"Sir, {ask_llama(prompt).strip()}"