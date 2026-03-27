try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

import eel
import threading
import queue
import time
try:
    from deep_translator import GoogleTranslator
    has_translator = True
except ImportError:
    has_translator = False
    print("deep-translator not found. Translation features disabled.")

# Multi-language state
user_lang = "en" # Language for responding
recognition_lang = "en-IN" # Language for specialized recognition

# Speech Queue and Thread
speech_queue = queue.Queue()

def speak(text):
    """Adds text to the speech queue to be spoken by the background thread."""
    speech_queue.put(text)

# We need a way to track if we are currently speaking so we don't listen to ourselves.
is_speaking = False

def speech_worker():
    """Background worker for handling speech on a dedicated thread."""
    global is_speaking
    print("Speech worker thread started.")
    while True:
        try:
            text = speech_queue.get(timeout=1)
            if not text:
                continue

            is_speaking = True
            print(f"Speech worker processing: '{text}'")
            global user_lang
            
            # Translate back to user's language if not English
            if user_lang and user_lang != 'en' and has_translator:
                try:
                    print(f"Translating to {user_lang}...")
                    text = GoogleTranslator(source='auto', target=user_lang).translate(text)
                except Exception as e:
                    print(f"Translation Output Error: {e}. Stick to English.")

            print(f"Niva: {text}")
            eel.update_status(text)
            
            # Initialize engine for each request to ensure it's "fresh" and active
            try:
                _engine = None
                try:
                    _engine = pyttsx3.init('sapi5')
                except:
                    _engine = pyttsx3.init()
                
                if _engine:
                    voices = _engine.getProperty('voices')
                    indian_voice = next((v for v in voices if any(x in v.name for x in ["India", "Heera", "Ravi", "Kalpana"])), None)
                    
                    if indian_voice:
                        _engine.setProperty('voice', indian_voice.id)
                    elif len(voices) > 1:
                        _engine.setProperty('voice', voices[1].id)
                    
                    _engine.setProperty('rate', 150) # Balanced sweet tone
                    _engine.setProperty('volume', 1.0)
                    
                    _engine.say(text)
                    _engine.runAndWait()
                    _engine.stop()
            except Exception as e:
                print(f"TTS Error during speech: {e}")
                
            speech_queue.task_done()
            is_speaking = False
        except queue.Empty:
            is_speaking = False
            continue
        except Exception as e:
            is_speaking = False
            print(f"Unexpected error in speech_worker: {e}")

# Start the speech worker thread
if pyttsx3:
    threading.Thread(target=speech_worker, daemon=True).start()

def listen():
    global is_speaking
    if not sr:
        print("Speech recognition not available (missing libraries).")
        return "None"

    # Don't listen while currently speaking (prevent echo loop)
    while is_speaking or not speech_queue.empty():
        time.sleep(0.1)

    r = sr.Recognizer()
    # OPTIMIZATION: Better sensitivity
    r.dynamic_energy_threshold = True
    r.energy_threshold = 600 # Lowered for better sensitivity
    r.dynamic_energy_adjustment_damping = 0.15
    r.dynamic_energy_ratio = 1.5
    
    try:
        with sr.Microphone() as source:
            print("Niva: Listening for command...")
            eel.update_status("LISTENING...")
            eel.set_amplitude(1)
            
            r.pause_threshold = 1.0 # Allow longer pauses between words
            r.adjust_for_ambient_noise(source, duration=0.8) # Better noise sampling
            
            audio = r.listen(source, timeout=10, phrase_time_limit=12)
    except Exception as e:
        print(f"Microphone error: {e}")
        return "None"

    try:
        print("Niva: Processing neural patterns...")
        eel.update_status("THINKING...")
        eel.set_amplitude(0)
        
        global recognition_lang
        query = r.recognize_google(audio, language=recognition_lang)
        print(f"User (Input): {query}")

        global user_lang
        try:
            if has_translator:
                try:
                    translated_query = GoogleTranslator(source='auto', target='en').translate(query)
                except:
                    translated_query = query
                
                if translated_query.lower() != query.lower():
                    print(f"User (Translated): {translated_query}")
                    user_lang = 'hi' 
                    recognition_lang = 'en-IN'
                    return translated_query.lower()
                else:
                    return query.lower()
            else:
                return query.lower()
                
        except Exception as e:
            print(f"Translation logic error: {e}")
            return query.lower()

    except sr.UnknownValueError:
        print("Niva: I heard some sound but could not identify any words.")
        return "None"
    except sr.RequestError as e:
        print(f"Niva: API connection failure; {e}")
        speak("I am having trouble connecting to my cognitive networks. Please check your internet.")
        return "None"
    except Exception as e:
        print(f"Detection Error: {e}")
        return "None"
