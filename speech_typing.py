import os
import time
import pyautogui
import requests
import pyttsx3
import pyperclip
import speech_recognition as sr
import subprocess
import webbrowser
import psutil
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()
GROQ_API_KEY = os.getenv("groq_api")

saved_urls = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "amazon": "https://www.amazon.in",
    "whatsapp": "https://web.whatsapp.com"
}

saved_apps = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "file": "explorer.exe",
    "command prompt": "cmd.exe",
    "notepad": "notepad.exe",
    "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
    "world": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
}

engine = pyttsx3.init()

def speak(text, announce=True):
    print(f"Assistant: {text}")
    if announce:
        engine.say(text)
        engine.runAndWait()

def recognize_speech(recognizer, microphone, lang="en", timeout=6):
    lang_code = "en-IN" if lang == "en" else "mr-IN"

    print("\nAssistant: Listening...")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)
        except sr.WaitTimeoutError:
            print("Assistant: No speech detected. Try again.")
            return None

    print("Assistant: Recognizing...")

    try:
        text = recognizer.recognize_google(audio, language=lang_code)
        print(f"Assistant: Recognized → {text}")
        return text
    except sr.UnknownValueError:
        print("Assistant: Could not understand the audio.")
        return None
    except sr.RequestError:
        print("Assistant: Speech recognition request failed.")
        return None

def type_text(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")

def get_groq_answer(question):
    if not GROQ_API_KEY:
        return "API key missing!"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "gllama-3.1-8b-instant",
        "messages": [{"role": "user", "content": f"Give a short answer: {question}"}],
        "max_tokens": 500
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        if response.status_code == 200 and "choices" in response_data:
            return response_data["choices"][0]["message"]["content"].strip()
        return f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
    except Exception:
        return "Error: Unable to fetch the answer."

def save_url(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "").split(".")[0]
    saved_urls[domain] = f"https://{parsed_url.netloc}"
    speak(f"Website {domain} saved")

def kill_head_mouse():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "eye_mouse_control" in proc.info['name'].lower():
            os.system(f"taskkill /F /PID {proc.info['pid']}")

def main():
    speak("Calibrating eye coordinates")

    recognizer = sr.Recognizer()
    microphone = sr.Microphone(device_index=1)

    while True:
        text = recognize_speech(recognizer, microphone, lang="en", timeout=6)
        if text:
            text_lower = text.lower()

            if text_lower.startswith("type"):
                filtered_text = text_lower.replace("type", "").strip(":")
                type_text(filtered_text)
                speak(filtered_text)

            elif "marathi type" in text_lower:
                speak("Listening for Marathi text")
                marathi_text = recognize_speech(recognizer, microphone, lang="mr", timeout=8)
                if marathi_text:
                    type_text(marathi_text)
                    speak(marathi_text)

            elif text_lower.startswith("save"):
                url = text_lower.replace("save", "").strip()
                save_url(url)

            elif text_lower.startswith("open web"):
                name = text_lower.replace("open web", "").strip()
                if name in saved_urls:
                    webbrowser.open(saved_urls[name])
                    speak(f"Opening {name}")
                else:
                    speak(f"Website {name} not found")

            elif text_lower.startswith("open app"):
                name = text_lower.replace("open app", "").strip()
                if name in saved_apps:
                    subprocess.Popen(saved_apps[name])
                    speak(f"Opening {name}")
                else:
                    speak(f"Application {name} not found")

            elif text_lower.startswith("play"):
                song_name = text_lower.replace("play", "").strip()
                if song_name:
                    query = song_name.replace(" ", "+")
                    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
                    speak(f"Playing {song_name} on YouTube")

            elif "answer the question" in text_lower:
                question = text_lower.replace("answer the question", "").strip()
                if question:
                    answer = get_groq_answer(question)
                    type_text(answer)

            actions = {
                "scroll down": lambda: pyautogui.scroll(-500),
                "scroll up": lambda: pyautogui.scroll(500),
                "right click": pyautogui.rightClick,
                "double click": pyautogui.doubleClick,
                "back": lambda: pyautogui.hotkey("alt", "left"),
                "play video": lambda: pyautogui.press("space"),
                "pause video": lambda: pyautogui.press("space"),
                "clear all": lambda: (pyautogui.hotkey("ctrl", "a"), pyautogui.press("backspace")),
                "enter": lambda: pyautogui.press("enter"),
                "delete": lambda: pyautogui.hotkey("ctrl", "backspace"),
            }

            if text_lower in actions:
                actions[text_lower]()
                speak(f"Performed {text_lower}", announce=False)

            elif "exit" in text_lower:
                speak("Exiting all processes")
                kill_head_mouse()
                os._exit(0)

        time.sleep(1)

if __name__ == "__main__":
    main()
