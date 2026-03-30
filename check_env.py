import importlib
import sys

packages = [
    'eel', 'pyttsx3', 'pywhatkit', 'wikipedia', 'pyautogui', 'requests',
    'screen_brightness_control', 'cv2', 'speech_recognition', 'face_recognition',
    'pyaudio', 'cmake', 'deep_translator', 'mediapipe'
]

print("Checking packages...")
for pkg in packages:
    try:
        importlib.import_module(pkg)
        print(f"✓ {pkg} is installed.")
    except ImportError:
        print(f"✗ {pkg} is NOT installed.")
    except Exception as e:
        print(f"! {pkg} import error: {e}")

try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"Total voices found: {len(voices)}")
    for v in voices:
        print(f" - {v.name} ({v.id})")
except Exception as e:
    print(f"TTS Test Error: {e}")
