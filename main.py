import os
import sys
import subprocess
import threading

# ──────────────────────────────────────────────
# AUTO-INSTALL: Install missing packages on startup
# ──────────────────────────────────────────────
def auto_install_dependencies():
    """Reads requirements.txt and pip-installs any missing packages."""
    req_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
    if not os.path.exists(req_file):
        print("requirements.txt not found, skipping auto-install.")
        return

    with open(req_file, "r") as f:
        packages = []
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith("#"):
                continue
            packages.append(line)

    if not packages:
        return

    # Map pip package names to their import names (for checking)
    pip_to_import = {
        "eel": "eel",
        "pyttsx3": "pyttsx3",
        "pywhatkit": "pywhatkit",
        "wikipedia": "wikipedia",
        "pyautogui": "pyautogui",
        "requests": "requests",
        "screen_brightness_control": "screen_brightness_control",
        "opencv-python": "cv2",
        "SpeechRecognition": "speech_recognition",
        "face_recognition": "face_recognition",
        "PyAudio": "pyaudio",
        "cmake": "cmake",
        "deep-translator": "deep_translator",
    }

    missing = []
    for pkg in packages:
        # Get the base package name (strip version specifiers)
        base_name = pkg.split("==")[0].split(">=")[0].split("<=")[0].strip()
        import_name = pip_to_import.get(pkg, pip_to_import.get(base_name, base_name))
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"AUTOMATION: Neural dependencies missing for mission: {', '.join(missing)}")
        for pkg in missing:
            print(f"  -> Deploying {pkg}...")
            # Try standard install first
            cmd = [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--no-cache-dir"]
            try:
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                print(f"  ✓ {pkg} integrated.")
            except subprocess.CalledProcessError:
                # If it fails, try with --break-system-packages (for PEP 668)
                try:
                    print(f"  ! Retrying {pkg} with environment overrides...")
                    subprocess.check_call(cmd + ["--break-system-packages"], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    print(f"  ✓ {pkg} integrated via override.")
                except Exception as e:
                    print(f"  ✗ Failed to install {pkg}. Please run: 'pip install {pkg}' manually.")
    else:
        print("All neural dependencies are online.")

auto_install_dependencies()

# Dependency Check & Flags
HAS_FACE_RECOGNITION = True
HAS_SPEECH = True

try:
    import eel
    import pyttsx3
    import speech_recognition as sr
    import cv2
    import face_recognition
    import pywhatkit
    import wikipedia
    import pyautogui
    import requests
    import screen_brightness_control as sbc
except ImportError as e:
    print(f"Warning: Missing dependency -> {e.name}")
    if e.name in ['face_recognition', 'dlib']:
        HAS_FACE_RECOGNITION = False
        print("Running without Face Authentication.")
    elif e.name in ['speech_recognition', 'pyaudio']:
        HAS_SPEECH = False
        print("Running without Voice Recognition.")
    else:
        print(f"Critical error: {e.name} is required.")
        # sys.exit(1) # Commented out to allow partial UI testing

from engine.speech import speak, listen
from engine.command import execute_command
from engine.face_auth import authenticate
from engine.gestures import start_gestures

# Initialize Eel
eel.init('www')

def niva_loop():
    """Main background loop for processing voice commands."""
    while True:
        query = listen()
        if query != "None":
            query_lower = query.lower()
            # Wake word logic with phonetic fallbacks for Indian English
            wake_words = ['niva', 'neeva', 'niwa', 'neva', 'nahin vah', 'nirva', 'meeva']
            
            has_wake_word = any(ww in query_lower for ww in wake_words)
            
            if has_wake_word:
                # Process command...
                clean_query = query_lower
                for ww in wake_words:
                    clean_query = clean_query.replace(f'hey {ww}', '').replace(f'he {ww}', '').replace(f'hi {ww}', '').replace(ww, '')
                clean_query = clean_query.strip()
                
                if 'stop' in clean_query or 'exit' in clean_query or 'bye' in clean_query:
                    speak("Shutting down systems. Goodbye, master.")
                    os._exit(0)
                    
                if clean_query:
                    execute_command(clean_query)
                else:
                    speak("I am listening, master. How can I assist?")
        eel.sleep(0.1)

@eel.expose
def start_niva():
    """Exposed function to start the assistant."""
    print("Starting Niva...")
    
    # Start Gesture Recognition in background
    try:
        start_gestures()
    except Exception as e:
        print(f"Gesture system failed to start: {e}")

    if not HAS_FACE_RECOGNITION:
        speak("Security protocols bypassed. Welcome back.")
        threading.Thread(target=niva_loop, daemon=True).start()
        return

    print("Authenticating...")
    if authenticate():
        speak("Authentication successful. I am at your service.")
        threading.Thread(target=niva_loop, daemon=True).start()
    else:
        speak("Access denied.")
        eel.update_status("ACCESS DENIED")

if __name__ == '__main__':
    # Start the web app with transparency and frameless flags
    try:
        eel.start('index.html', mode='chrome', 
                  cmdline_args=['--window-size=400,600', '--transparent-window-control', '--frameless', '--always-on-top'],
                  host='localhost', port=8000, block=False)
    except:
        # Fallback for non-chrome environments
        eel.start('index.html', host='localhost', port=8000, block=False)

    print("Niva Core Active...")
    
    # AUTOMATION: Automatically trigger Niva initialization after UI loads
    threading.Timer(2.0, start_niva).start()
    
    while True:
        eel.sleep(1.0)
