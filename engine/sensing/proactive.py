import psutil
import time
from engine.io.speech import speak

class ProactiveReflex:
    def __init__(self):
        self.start_time = time.time()
        self.last_check = time.time()
        self.suggestions = {
            "break": "Master, you've been focused for over two hours. Perhaps a short break would optimize your neural performance.",
            "performance": "Sir, background processes are consuming significant resources. Shall we initiate a focus-clear protocol?",
            "energy": "The internal environment is becoming high-energy. Recommend dimming the lights for improved Focus."
        }

    def check_status(self):
        """Analyzes system and session state for natural suggestions."""
        current_time = time.time()
        
        # 1. Check Session Duration
        session_hours = (current_time - self.start_time) / 3600
        if session_hours > 2 and (current_time - self.last_check > 3600):
            # Suggest a break
            self.last_check = current_time
            return self.suggestions["break"]
        
        # 2. Check System Load
        cpu = psutil.cpu_percent()
        if cpu > 85:
            return self.suggestions["performance"]
            
        return None

proactive = ProactiveReflex()

def get_proactive_suggestion():
    return proactive.check_status()
