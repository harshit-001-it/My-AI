import os
import pywhatkit
import wikipedia
import webbrowser
import pyautogui
import screen_brightness_control as sbc
from engine.speech import speak

def execute_command(query):
    if 'open google chrome' in query or 'open chrome' in query:
        speak("Opening Google Chrome, master.")
        os.system("start chrome")
        speak("Chrome is now active.")
    
    elif 'close google chrome' in query or 'close chrome' in query:
        speak("Closing Google Chrome.")
        os.system("taskkill /F /IM chrome.exe")
        speak("Done. Chrome has been shut down.")
    
    elif 'open microsoft edge' in query or 'open edge' in query:
        speak("Opening Microsoft Edge.")
        os.system("start msedge")
        speak("Edge is ready for use.")

    elif 'close microsoft edge' in query or 'close edge' in query:
        speak("Closing Microsoft Edge.")
        os.system("taskkill /F /IM msedge.exe")
        speak("Edge is now closed.")
        speak("Edge closed.")

    elif 'open notepad' in query:
        speak("Opening Notepad")
        os.system("start notepad")

    elif 'close notepad' in query:
        speak("Closing Notepad")
        os.system("taskkill /F /IM notepad.exe")
    
    elif 'open calculator' in query:
        speak("Opening Calculator")
        os.system("start calc")

    elif 'close calculator' in query:
        speak("Closing Calculator")
        os.system("taskkill /F /IM CalculatorApp.exe")
        os.system("taskkill /F /IM calc.exe")

    elif 'play' in query:
        song = query.replace('play', "")
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif 'search' in query:
        search_query = query.replace('search', "")
        speak(f"Searching for {search_query} on Google")
        pywhatkit.search(search_query)

    elif 'wikipedia' in query or 'who is' in query or 'what is' in query:
        search_term = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").strip()
        if search_term:
            speak(f"Searching for {search_term}...")
            try:
                results = wikipedia.summary(search_term, sentences=2)
                speak("Found this on Wikipedia:")
                speak(results)
            except Exception:
                speak(f"I couldn't find a specific page for {search_term}, would you like me to search Google instead?")
        else:
            speak("What would you like me to look up?")

    elif 'lock system' in query or 'secure workspace' in query:
        speak("Securing your workspace, master. All systems locked.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif 'screenshot' in query:
        speak("Capturing your screen session.")
        pyautogui.screenshot(f"screenshot_{os.urandom(2).hex()}.png")
        speak("Screenshot saved.")

    elif 'volume up' in query:
        speak("Adjusting audio levels upward.")
        pyautogui.press("volumeup")

    elif 'volume down' in query:
        speak("Lowering audio levels.")
        pyautogui.press("volumedown")

    elif 'brightness' in query:
        if 'increase' in query:
            speak("Enhancing display brightness.")
            current = sbc.get_brightness()
            sbc.set_brightness(min(100, current[0] + 10))
        elif 'decrease' in query:
            speak("Dimming display for comfort.")
            current = sbc.get_brightness()
            sbc.set_brightness(max(0, current[0] - 10))

    elif 'shutdown system' in query:
        speak("Initiating system termination protocol.")
        os.system("shutdown /s /t 5")

    else:
        from engine.chatbot import get_response
        response = get_response(query)
        speak(response)
