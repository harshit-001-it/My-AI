import os
import time
from engine.speech import speak
from engine.registry import load_registry, update_setting

class IoTManager:
    def __init__(self):
        self.devices = {
            "main_lights": {"status": "OFF", "level": 100},
            "security_perimeter": {"status": "ARMED", "level": 100},
            "workspace_monitor": {"status": "ON", "level": 100}
        }

    def control_device(self, device_name, action, level=None):
        """Simulated control for IoT devices."""
        if device_name in self.devices:
            self.devices[device_name]["status"] = action
            if level is not None:
                self.devices[device_name]["level"] = level
            
            speak(f"Syncing with {device_name.replace('_', ' ')}. Action: {action}.")
            print(f"IoT Logic: {device_name} is now {action} ({level if level else ''})")
            return True
        return False

    def execute_macro(self, macro_name):
        """Executes a series of predefined actions (Macros)."""
        registry = load_registry()
        macros = registry.get("macros", {
            "goodnight": [
                {"type": "iot", "device": "main_lights", "action": "OFF"},
                {"type": "system", "action": "lock"},
                {"type": "speech", "text": "Goodnight, Master. Sleep well."}
            ],
            "morning": [
                {"type": "iot", "device": "main_lights", "action": "ON", "level": 50},
                {"type": "speech", "text": "Good morning, Sir. Your schedule is synchronized."}
            ]
        })

        if macro_name in macros:
            speak(f"Initiating {macro_name} protocol.")
            for step in macros[macro_name]:
                self._run_step(step)
            return True
        return False

    def _run_step(self, step):
        t = step.get("type")
        if t == "iot":
            self.control_device(step["device"], step["action"], step.get("level"))
        elif t == "system":
            if step["action"] == "lock":
                os.system("rundll32.exe user32.dll,LockWorkStation")
        elif t == "speech":
            speak(step["text"])

iot = IoTManager()

def handle_iot(query):
    query = query.lower()
    if 'lights' in query:
        if 'off' in query: iot.control_device("main_lights", "OFF")
        elif 'on' in query: iot.control_device("main_lights", "ON")
    elif 'goodnight' in query:
        iot.execute_macro("goodnight")
    elif 'morning' in query:
        iot.execute_macro("morning")
