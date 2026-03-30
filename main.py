import os
import sys
import time
import threading
import eel
import psutil
import pygetwindow as gw

# Production-Grade Modular Imports
from engine.io.speech import speak, listen
from engine.core.command import execute_command
from engine.sensing.face_auth import authenticate
from engine.sensing.gestures import start_gestures
from engine.sensing.intelligence import get_briefing
from engine.sensing.proactive import get_proactive_suggestion

# Configuration
eel.init('www')

# ──────────────────────────────────────────────
# UI Bridge Functions (Exposed to JS)
# ──────────────────────────────────────────────

@eel.expose
def trigger_auth():
    """Triggered from the security.html 'Initialize Protocol' button."""
    print("Security Hub: Initiating Biometric Scan...")
    if authenticate():
        # Transition to Dashboard
        eel.show_dashboard()() # Call JS function
        threading.Thread(target=niva_loop, daemon=True).start()
        # Start Workers
        threading.Thread(target=telemetry_worker, daemon=True).start()
        threading.Thread(target=media_sensing_worker, daemon=True).start()
        threading.Thread(target=intelligence_worker, daemon=True).start()
        threading.Thread(target=proactive_worker, daemon=True).start()
    else:
        eel.auth_failed()()

@eel.expose
def manual_command(text):
    """Triggered if user types a command instead of speaking."""
    execute_command(text)

@eel.expose
def shutdown_niva():
    speak("Synchronizing final data packets. Goodbye, Master.")
    os._exit(0)

# ──────────────────────────────────────────────
# Core Logic Loop
# ──────────────────────────────────────────────

def niva_loop():
    """Main background loop for processing voice commands."""
    print("Niva Logic Node: Online.")
    
    wake_words = ['niva', 'neva', 'niva ai', 'hey niva', 'hi niva']
    
    while True:
        # Communicate to UI that we are listening
        eel.update_status("IDLE")()
        query = listen()
        
        if query != "None":
            query_lower = query.lower().strip()
            
            # Check for wake word
            has_wake_word = False
            for ww in wake_words:
                if ww in query_lower:
                    has_wake_word = True
                    query_lower = query_lower.replace(ww, '').strip()
                    break
            
            if has_wake_word:
                eel.update_status("PROCESSING")()
                eel.update_intent(query_lower if query_lower else "WAKE_WORD_TRIGGER")()
                if not query_lower:
                    speak("I am here, Sir. How can I assist?")
                else:
                    print(f"Niva Logic: Processing intent -> {query_lower}")
                    execute_command(query_lower)
            
        eel.sleep(0.5)

def telemetry_worker():
    """Background thread to stream system stats to the UI."""
    while True:
        try:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            eel.update_telemetry(cpu, ram)()
        except:
            pass
        eel.sleep(2.0)

def media_sensing_worker():
    """Background thread to detect active media windows."""
    last_media = ""
    while True:
        try:
            all_windows = gw.getAllTitles()
            media_apps = ['Spotify', 'YouTube', 'VLC', 'Media Player', 'Chrome']
            active_media = "NO_ACTIVE_MEDIA"
            active_artist = "Master-Link-Online"
            
            for title in all_windows:
                for app in media_apps:
                    if app in title and len(title) > len(app) + 3:
                        active_media = title
                        active_artist = app
                        break
                if active_media != "NO_ACTIVE_MEDIA": break
            
            if active_media != last_media:
                eel.update_media(active_media[:20] + "...", active_artist)()
                last_media = active_media
        except:
            pass
        eel.sleep(5.0)

def intelligence_worker():
    """Periodically fetches and streams news/weather briefings."""
    while True:
        try:
            briefing = get_briefing()
            top_news = briefing['news'][0] if briefing['news'] else "GRID_QUIET"
            weather = briefing['weather']
            eel.update_briefing(top_news, weather['temp'], weather['condition'])()
        except:
            pass
        eel.sleep(300.0)

def proactive_worker():
    """Monitors system for proactive suggestions."""
    while True:
        try:
            suggestion = get_proactive_suggestion()
            if suggestion:
                speak(suggestion)
                # Also show as alert in UI
                eel.show_alert(suggestion[:50] + "...")()
        except:
            pass
        eel.sleep(600.0) # Check every 10 minutes

# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == '__main__':
    # Start on the security screen
    print("Initialising NIVA Core...")
    
    try:
        # Launch window (Chrome app mode for premium feel)
        eel.start('security.html', mode='chrome', 
                  cmdline_args=['--window-size=1280,800', '--start-maximized'],
                  block=False)
    except Exception:
        # Fallback to default browser
        eel.start('security.html', block=False)

    # Keep main thread alive
    while True:
        eel.sleep(1.0)
