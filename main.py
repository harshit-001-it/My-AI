import os
import sys
import time
import threading
import eel
from engine.speech import speak, listen
from engine.command import execute_command
from engine.face_auth import authenticate
from engine.gestures import start_gestures

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
        threading.Thread(target=jarvis_loop, daemon=True).start()
    else:
        eel.auth_failed()()

@eel.expose
def manual_command(text):
    """Triggered if user types a command instead of speaking."""
    execute_command(text)

@eel.expose
def shutdown_jarvis():
    speak("Synchronizing final data packets. Goodbye, Master.")
    os._exit(0)

# ──────────────────────────────────────────────
# Core Logic Loop
# ──────────────────────────────────────────────

def jarvis_loop():
    """Main background loop for processing voice commands."""
    print("Jarvis Logic Node: Online.")
    
    wake_words = ['jarvis', 'javis', 'javis', 'hey jarvis', 'hi jarvis']
    
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
                    print(f"Jarvis Logic: Processing intent -> {query_lower}")
                    execute_command(query_lower)
            
        eel.sleep(0.5)

# ──────────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────────

if __name__ == '__main__':
    # Start on the security screen
    print("Initialising JARVIS Core...")
    
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
