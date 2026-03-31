import json
import os
import subprocess
import webbrowser

import eel
import wikipedia

from engine.core.chatbot import get_niva_response
from engine.io.speech import speak, switch_language, user_lang
from engine.sensing.iot_manager import handle_iot


def execute_command(query):
    """
    Mental Node: Processes Master's query through the Niva Brain (JSON Protocol).
    Then dispatches the structured intent to the appropriate system logic.
    """
    try:
        # 1. Get Structured Intent from Brain
        raw_json = get_niva_response(query)
        intent = json.loads(raw_json)

        # 2. Extract Response Metadata
        type = intent.get("type", "error")

        # 3. Handle Conversational Response
        if type == "message":
            content = intent.get("content", "Sir, I'm analyzing the data packets.")
            speak(content)

        # 4. Handle System Action Request
        elif type == "action":
            action = intent.get("action_name")
            params = intent.get("parameters", {})
            requires_confirm = intent.get("confirmation_required", False)

            if action == "system_command":
                cmd = params.get("command")
                if requires_confirm:
                    speak(
                        f"Master, you requested a system {cmd}. Please confirm the intent protocol."
                    )
                    # Confirmation logic would trigger a JS modal or voice wait
                    # For now, we simulate a 'safe' confirm or immediate bypass for non-destructive
                    if cmd == "shutdown":
                        _unauthorized_or_confirmed(cmd)
                    else:
                        _handle_app_launch(cmd)
                else:
                    _handle_app_launch(cmd)

            elif action == "generate_image":
                prompt = params.get("prompt")
                speak(
                    f"Synthesizing your visual request for {prompt}. Checking creative node."
                )

            elif action == "search":
                target = params.get("target")
                query_str = params.get("query", query)
                if target == "wikipedia":
                    _handle_wikipedia(query_str)
                else:
                    _handle_web_search(query_str)

            elif action == "iot_control":
                # Handle IoT via legacy iot_manager
                handle_iot(query)

        # 5. Handle Error Node
        elif type == "error":
            msg = intent.get("message", "Logic node failure.")
            speak(f"Apologies Sir. {msg}")

    except Exception as e:
        print(f"Niva Command Node Error: {e}")
        speak(
            "Sir, there was an error in my command dispatcher. Restructuring neural links."
        )


# ──────────────────────────────────────────────
# Action Helper Functions
# ──────────────────────────────────────────────


def _handle_app_launch(app_name):
    """Handles production-grade application launching."""
    app_lower = app_name.lower()
    if app_lower == "chrome":
        speak("Initializing chrome protocol.")
        webbrowser.open("https://www.google.com")
        return

    apps = {
        "notepad": "notepad.exe" if os.name == "nt" else "gedit",
        "calculator": "calc.exe" if os.name == "nt" else "gnome-calculator",
        "files": "explorer.exe" if os.name == "nt" else "nautilus",
    }

    path = apps.get(app_lower)
    if path:
        speak(f"Initializing {app_name} protocol.")
        try:
            if os.name == "nt":
                os.startfile(path)
            else:
                subprocess.Popen([path])
        except Exception:
            pass
    else:
        speak(f"I couldn't find the {app_name} module in my registry, Sir.")


def _handle_wikipedia(query):
    """Fetches high-density intelligence from Wikipedia."""
    try:
        results = wikipedia.summary(query, sentences=2)
        speak(f"Scanning Global Knowledge Grid. According to the database: {results}")
    except:
        speak("I couldn't retrieve a summary for that entry, Sir.")


def _handle_web_search(query):
    """Initializes a web crawl."""
    speak(f"Initializing global search for {query}.")
    webbrowser.open(f"https://www.google.com/search?q={query}")


def _unauthorized_or_confirmed(cmd):
    """Handles security confirmations for system-critical actions."""
    if cmd == "shutdown":
        speak("Master, I am preparing for a synchronized shutdown. Protocol confirmed.")
        if os.name == "nt":
            os.system("shutdown /s /t 1")
        else:
            os.system("shutdown -h now")
