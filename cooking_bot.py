import json
import pyttsx3
from vosk import Model, KaldiRecognizer
import pyaudio
import google.generativeai as genai
import time
import os

# 🔧 Remove broken proxy env var
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)

# --------- Gemini API setup ---------
genai.configure(api_key="***********************************")
model = genai.GenerativeModel('models/gemini-1.5-flash')

# --------- Vosk speech recognition ---------
vosk_model_path = r"D:\driving bot\vosk-model-en-in-0.5"
vosk_model = Model(vosk_model_path)
recognizer = KaldiRecognizer(vosk_model, 16000)

# --------- Audio input setup ---------
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)
stream.start_stream()

# --------- Text-to-speech ---------
tts_engine = pyttsx3.init()
def speak(text):
    print("ChefBot:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

print("👩‍🍳 Welcome to your Gemini Cooking Guide! Say 'exit' to stop.")

# 🧠 Cooking memory context
history = []

while True:
    data = stream.read(4096, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        user_text = result.get("text", "").strip()
        if not user_text:
            continue

        print("You said:", user_text)

        if user_text.lower() in ["exit", "quit", "stop"]:
            speak("Happy cooking! Goodbye!")
            break

        # Add memory for context (optional)
        history.append({"role": "user", "parts": [user_text]})

        try:
            # Request Gemini to act like a cooking assistant
            prompt = (
                "You are a friendly step-by-step Indian cooking assistant. "
                "Only give the next cooking instruction clearly. If the user says 'next' or 'what's next', continue. "
                "Answer this: " + user_text
            )
            response = model.generate_content(prompt)
            reply = response.text.strip()
            history.append({"role": "model", "parts": [reply]})
            speak(reply)
        except Exception as e:
            print("❌ Error:", e)
            speak("Sorry, I couldn't help with that. Try again.")
        time.sleep(0.5)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
