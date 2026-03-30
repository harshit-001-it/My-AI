import os
import time
import numpy as np
import cv2
import face_recognition
from engine.speech import speak, listen
from engine.registry import load_registry

# Security Constants
DB_PATH = "engine/db"
registry = load_registry()
VOICE_PIN = str(registry.get("voice_pin", "1010"))

class SecurityHub:
    def __init__(self):
        if not os.path.exists(DB_PATH):
            os.makedirs(DB_PATH)
        self.reference_encoding = self._load_reference()

    def _load_reference(self):
        ref_file = os.path.join(DB_PATH, "user_reference.jpg")
        if not os.path.exists(ref_file):
            return None
        
        try:
            img = cv2.imread(ref_file)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)
            return encodings[0] if encodings else None
        except Exception as e:
            print(f"Auth Error: Memory corruption in security file. {e}")
            return None

    def face_id_scan(self):
        """Perform a quick, non-intrusive face scan."""
        if self.reference_encoding is None:
            speak("Master, I have no records of your biometric data. Initiating registration.")
            return self.register_face()

        speak("Scanning biometric signatures.")
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        
        while time.time() - start_time < 8: # 8 second window
            ret, frame = cap.read()
            if not ret: continue
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                match = face_recognition.compare_faces([self.reference_encoding], face_encoding, tolerance=0.5)
                if True in match:
                    cap.release()
                    speak("Identity confirmed. Welcome back, Master.")
                    return True
        
        cap.release()
        speak("Biometric mismatch detected. Security protocols engaged.")
        return False

    def voice_pin_verification(self):
        """Two-factor authentication using Voice PIN."""
        speak("Please state your authorization PIN for level 2 clearance.")
        attempts = 3
        while attempts > 0:
            pin_query = listen()
            # If the PIN is found as a substring (e.g. user says "my pin is 1010")
            if VOICE_PIN in pin_query:
                speak("Voice signature matched. Clearance granted.")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    speak(f"Access denied. {attempts} attempts remaining. Re-state PIN.")
                else:
                    speak("Authorization failed. Lockdown initiated.")
        return False

    def register_face(self):
        """Registers a new master."""
        speak("Please look directly at the optical sensor. I'm capturing your neural map now.")
        cap = cv2.VideoCapture(0)
        time.sleep(2) # Give user time to position
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(os.path.join(DB_PATH, "user_reference.jpg"), frame)
            self.reference_encoding = self._load_reference()
            speak("Registration complete. Your signature has been uploaded to the local core.")
            cap.release()
            return True
        cap.release()
        return False

def authenticate():
    hub = SecurityHub()
    if hub.face_id_scan():
        # Enhanced security: Trigger voice PIN if configured
        # return hub.voice_pin_verification() 
        return True
    return False
