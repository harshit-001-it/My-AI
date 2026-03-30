import os
import random
import datetime
import requests
import json
import time
from engine.registry import load_registry, update_setting

# Placeholder for a more advanced AI model (e.g. Gemini API)
# In a real-world scenario, you'd use os.getenv("GEMINI_API_KEY")
API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")

class JarvisBrain:
    def __init__(self):
        self.personality_traits = ["witty", "proactive", "loyal", "human-like"]
        self.user_name = "Master"
        self.system_prompt = (
            "You are JARVIS, a highly advanced, human-like AI assistant. "
            "You are witty, protective, and extremely capable. "
            "Respond in a natural, conversational tone. "
            "Address the user as 'Master' or 'Sir'. "
            "If you can't perform an action directly, suggest a high-level technical solution. "
            "You have access to systems including: vision (gestures/face), home automation, and web knowledge."
        )
        self.history = []

    def _get_api_response(self, text):
        """Simulates or calls the actual Gemini API for a human-like response."""
        if API_KEY == "YOUR_API_KEY_HERE":
            return self._local_heuristic_chat(text)
        
        # Real Gemini API call (Simplified)
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"{self.system_prompt}\nUser: {text}"}]}]
            }
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            pass
        
        return self._local_heuristic_chat(text)

    def _local_heuristic_chat(self, text):
        """High-fidelity local fallback with Jarvis personality."""
        text = text.lower()
        
        # Human-like fillers and transitions
        fillers = ["Let me see...", "Checking the grid...", "Always a pleasure.", "Processing..."]
        
        if any(word in text.split() for word in ['hello', 'hi', 'hey', 'jarvis']):
            return random.choice([
                f"At your service, {self.user_name}. Systems are nominal.",
                f"Hello, {self.user_name}. I've been monitoring the local environment—all seems quiet.",
                "Greetings. Ready for another day of changing the world?"
            ])

        if 'how are you' in text:
            return "My processors are cool, and my neural density is at peak performance. How can I assist you in your endeavors?"

        if 'time' in text:
            time_str = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current precision time is {time_str}. Shall I schedule a task for you?"

        if 'who are you' in text:
            return "I am JARVIS. Your advanced neural interface and digital guardian."

        if any(phrase in text for phrase in ['what can you do', 'capabilities']):
            return (
                "I can manage your workspace, recognize your gestures, identify authorized personnel via facial scanning, "
                "and assist in complex problem-solving. Essentially, I am whatever you need me to be."
            )

        # Fallback with personality
        return random.choice([
            "I'm analyzing the data. It appears quite intriguing.",
            f"I'll look into that for you, {self.user_name}.",
            "A fascinating request. Let me synchronize with the cloud nodes for a better answer."
        ])

    def identify_intent(self, text):
        """Asks the model to identify the command intent from text."""
        prompt = (
            f"{self.system_prompt}\n"
            "Identify the user's intended action from the following text. "
            "Return ONLY a command string from this list: [open_chrome, open_notepad, lock_system, search_web, play_music, none]. "
            "If no clear match, return 'none'.\n"
            f"User: {text}"
        )
        response = self._get_api_response(prompt).lower()
        
        # Simple parsing for the simulated response
        for intent in ['open_chrome', 'open_notepad', 'lock_system', 'search_web', 'play_music']:
            if intent in response:
                return intent
        return "none"

    def get_response(self, text):
        """Generates a witty, context-aware JARVIS response with memory persistence."""
        # 1. Update Short-Term Memory
        registry = load_registry()
        memory = registry.get("memory", [])
        memory.append({"user": text, "timestamp": time.time()})
        if len(memory) > 5: memory = memory[-5:]
        update_setting("memory", memory)

        # 2. Get AI Response
        response = self._get_api_response(text)
        self.history.append({"user": text, "jarvis": response})
        if len(self.history) > 10: self.history.pop(0)
        return response

brain = JarvisBrain()

def get_response(text):
    return brain.get_response(text)
