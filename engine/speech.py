import os
import queue
import threading
import time
import asyncio
import edge_tts
import pygame # For playing edge-tts mp3 locally
import pyttsx3
import speech_recognition as sr
from deep_translator import GoogleTranslator

# Initialize Pygame for audio playback (faster and more reliable for mp3 than other libs)
pygame.mixer.init()

# Multi-language state
user_lang = "en"
recognition_lang = "en-IN"
is_speaking = False

def switch_language(lang_code):
    """Switches the global language state. 'en' or 'hi'."""
    global user_lang, recognition_lang
    if lang_code == "hi":
        user_lang = "hi"
        recognition_lang = "hi-IN"
        speak("Hindi language protocol activated. I am now listening in your mother tongue, Sir.")
    else:
        user_lang = "en"
        recognition_lang = "en-IN"
        speak("English language protocol restored. All systems standardized.")

# Speech Queue
speech_queue = queue.Queue()

def speak(text):
    """Adds text to the speech queue."""
    speech_queue.put(text)

async def _edge_speak(text):
    """Internal async function for edge-tts."""
    # Choose a high-quality human-like voice (Ryan is good for Jarvis feel)
    voice = "en-US-RyanMultilingualNeural" if user_lang == "en" else "hi-IN-MadhurNeural"
    communicate = edge_tts.Communicate(text, voice)
    output_file = "speech_temp.mp3"
    await communicate.save(output_file)
    
    # Play the file
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        await asyncio.sleep(0.1)
    pygame.mixer.music.unload()
    try: os.remove(output_file)
    except: pass

def speech_worker():
    """Background worker for handling speech with edge-tts and pyttsx3 fallback."""
    global is_speaking
    print("Jarvis Speech Node Active.")
    
    # Create or get event loop for this thread (needed for edge-tts)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        try:
            text = speech_queue.get(timeout=1)
            if not text: continue

            is_speaking = True
            print(f"Jarvis: {text}")

            # Optional Hindi translation if state is Hindi
            if user_lang == 'hi':
                try:
                    text = GoogleTranslator(source='auto', target='hindi').translate(text)
                except: pass

            # Try Premium Voice (Edge-TTS)
            try:
                loop.run_until_complete(_edge_speak(text))
            except Exception as e:
                print(f"Premium voice failed: {e}. Falling back to system voice.")
                # Fallback to pyttsx3
                engine = pyttsx3.init()
                engine.setProperty('rate', 165)
                engine.say(text)
                engine.runAndWait()
            
            speech_queue.task_done()
            is_speaking = False
        except queue.Empty:
            is_speaking = False
            continue
        except Exception as e:
            is_speaking = False
            print(f"Speech Loop Error: {e}")

# Start speech thread
threading.Thread(target=speech_worker, daemon=True).start()

def listen():
    """High-sensitivity audio capture for commands."""
    global is_speaking
    if not sr: return "None"

    # Wait if Jarvis is currently speaking
    while is_speaking or not speech_queue.empty():
        time.sleep(0.1)

    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300 
    
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Ambient noise adjustment
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
    except Exception as e:
        print(f"Mic Error: {e}")
        return "None"

    try:
        print("Processing...")
        query = r.recognize_google(audio, language=recognition_lang)
        print(f"User: {query}")
        return query.lower()
    except:
        return "None"
