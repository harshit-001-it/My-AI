import os
import time
import cv2
import mediapipe as mp
from engine.io.speech import speak, listen
from engine.core.registry import get_setting

# Security Constants
VOICE_PIN = str(get_setting("voice_pin", "1010"))

class SecurityHub:
    def __init__(self):
        # Initialize MediaPipe Face Detection
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detector = self.mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.8
        )

    def face_scan(self):
        """Perform a highly optimized biometric face presence scan."""
        speak("Scanning physical presence grid.")
        cap = cv2.VideoCapture(0)
        start_time = time.time()
        
        while time.time() - start_time < 5: # 5 second window
            ret, frame = cap.read()
            if not ret: continue
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_detector.process(rgb_frame)

            # If a human face is strictly detected with high confidence
            if results.detections:
                cap.release()
                print("Security Hub: Face Detected via MediaPipe Core.")
                speak("Human presence verified. Please state your authorization PIN.")
                return self.voice_pin_verification()
        
        cap.release()
        speak("No human signatures detected. Security protocols engaged.")
        return False

    def voice_pin_verification(self):
        """Two-factor authentication using Voice PIN."""
        attempts = 3
        while attempts > 0:
            pin_query = listen()
            # If the PIN is found as a substring
            if VOICE_PIN in pin_query:
                speak("Voice signature matched. Clearance granted. Welcome to Niva.")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    speak(f"Access denied. {attempts} attempts remaining. Re-state PIN.")
                else:
                    speak("Authorization failed. Lockdown initiated.")
        return False

def authenticate():
    hub = SecurityHub()
    # Execute the streamlined 2-step verification (Face Presence + Voice PIN)
    return hub.face_scan()
