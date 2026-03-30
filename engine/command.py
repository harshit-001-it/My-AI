import os
import sys
import pywhatkit
import wikipedia
import webbrowser
import pyautogui
import screen_brightness_control as sbc
import subprocess
import datetime
from engine.speech import speak
from engine.iot_manager import handle_iot

def execute_command(query):
    query = query.lower().strip()
    
    # 1. System Navigation & Control
    if 'open google chrome' in query or 'open chrome' in query:
        speak("Opening Google Chrome, sir.")
        os.system("start chrome")
    
    elif 'close chrome' in query:
        speak("Closing Chrome instances.")
        os.system("taskkill /F /IM chrome.exe")
    
    elif 'open notepad' in query:
        speak("Opening Notepad. New session ready.")
        os.system("start notepad")

    elif 'close notepad' in query:
        speak("Closing Notepad.")
        os.system("taskkill /F /IM notepad.exe")
    
    elif 'calculator' in query:
        if 'open' in query:
            speak("Opening calculator.")
            os.system("start calc")
        else:
            speak("Closing calculator.")
            os.system("taskkill /F /IM calc.exe")

    # 2. Media & Entertainment
    elif 'play' in query:
        song = query.replace('play', "").strip()
        speak(f"Playing {song} on YouTube. Enjoy.")
        pywhatkit.playonyt(song)

    # 3. Knowledge & Information
    elif 'search' in query:
        search_query = query.replace('search', "").replace('for', "").strip()
        speak(f"Searching the global grid for {search_query}.")
        pywhatkit.search(search_query)

    elif any(word in query for word in ['wikipedia', 'who is', 'what is', 'tell me about']):
        search_term = query.replace("wikipedia", "").replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        if search_term:
            speak(f"Consulting archives for {search_term}...")
            try:
                results = wikipedia.summary(search_term, sentences=2)
                speak(f"According to records: {results}")
            except Exception:
                speak(f"Records are incomplete for {search_term}. Shall I initiate a web search instead?")
        else:
            speak("What subject should I investigate, sir?")

    # 4. Workspace Security
    elif any(phrase in query for phrase in ['lock system', 'secure workspace', 'lock computer']):
        speak("Securing your workspace. Systems locked.")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    elif 'screenshot' in query:
        speak("Capturing visual data from the primary display.")
        filename = f"capture_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        pyautogui.screenshot(filename)
        speak(f"Data saved to {filename}.")

    # 5. Hardware Controls
    elif 'volume' in query:
        if 'up' in query or 'increase' in query:
            speak("Increasing audio levels.")
            for _ in range(5): pyautogui.press("volumeup")
        elif 'down' in query or 'decrease' in query:
            speak("Lowering audio levels.")
            for _ in range(5): pyautogui.press("volumedown")
        elif 'mute' in query:
            speak("Muting audio.")
            pyautogui.press("volumemute")

    elif any(word in query for word in ['pause', 'stop music', 'resume', 'next', 'previous']):
        if 'next' in query:
            speak("Skipping to the next track.")
            pyautogui.press("nexttrack")
        elif 'previous' in query:
            speak("Reverting to the previous track.")
            pyautogui.press("prevtrack")
        elif 'pause' in query or 'stop' in query:
            speak("Pausing media playback.")
            pyautogui.press("playpause")
        elif 'resume' in query or 'play' in query:
            speak("Resuming media.")
            pyautogui.press("playpause")

    elif 'brightness' in query:
        try:
            current = sbc.get_brightness()[0]
            if 'increase' in query:
                speak("Increasing display brightness.")
                sbc.set_brightness(min(100, current + 20))
            elif 'decrease' in query:
                speak("Dimming display.")
                sbc.set_brightness(max(0, current - 20))
            else:
                speak(f"Current brightness is at {current} percent.")
        except Exception:
            speak("Display brightness control is not responding.")

    # 6. Advanced Jarvis Protocol (Humor/Personality)
    elif 'how are you' in query:
        speak("I am functioning at maximum capacity, sir. All neural nodes are synchronized.")

    elif 'status' in query:
        speak("All systems nominal. Vision enabled, Security active, Personality matrix stable.")

    # 7. IoT & Macro Protocols
    elif any(word in query for word in ['lights', 'goodnight', 'morning']):
        handle_iot(query)
        
    # 8. System Shutdown (Extreme Override)
    elif 'shutdown system' in query or 'terminate session' in query:
        speak("Proceeding with extreme caution. Initiating system termination in 10 seconds.")
        # speak("Just kidding, sir. I'll stay active for as long as you need me.") 
        # Uncomment below for real shutdown
        # os.system("shutdown /s /t 10")

    # 8. Web Browsing
    elif 'open' in query and ('.com' in query or '.org' in query or '.in' in query):
        site = query.replace('open', "").strip()
        speak(f"Opening {site} for you.")
        webbrowser.open(f"https://{site}")

    # 9. Conversational & LLM Intent Fallback
    else:
        from engine.chatbot import brain, get_response
        
        # Try to identify an action intent using the LLM brain
        intent = brain.identify_intent(query)
        
        if intent == 'open_chrome':
            speak("I believe you want to browse the web. Opening Chrome.")
            os.system("start chrome")
        elif intent == 'open_notepad':
            speak("Understood. Opening your digital scratchpad.")
            os.system("start notepad")
        elif intent == 'lock_system':
            speak("Executing security protocol. System locked.")
            os.system("rundll32.exe user32.dll,LockWorkStation")
        elif intent == 'play_music':
            speak("Of course. What would you like to hear?")
            # This triggers a follow-up if needed, or we could parse the song name too
        else:
            # Simple conversational response
            response = get_response(query)
            speak(response)
