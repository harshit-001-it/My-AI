import cv2
import mediapipe as mp
import threading
import time
from engine.command import execute_command
from engine.speech import speak

class GestureProcessor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.is_running = False
        self.last_gesture_time = 0
        self.cooldown = 2.0 # Seconds between gesture triggers

    def start(self):
        self.is_running = True
        threading.Thread(target=self._process, daemon=True).start()
        print("Gesture recognition system active.")

    def stop(self):
        self.is_running = False

    def _process(self):
        cap = cv2.VideoCapture(0)
        while self.is_running:
            ret, frame = cap.read()
            if not ret:
                continue

            # Flip for mirror effect and convert to RGB
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = self._detect_gesture(hand_landmarks)
                    if gesture and (time.time() - self.last_gesture_time > self.cooldown):
                        self._trigger_action(gesture)
                        self.last_gesture_time = time.time()

            # Optional: Show debug window during development
            # cv2.imshow("Niva Vision", frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()
        cv2.destroyAllWindows()

    def _detect_gesture(self, landmarks):
        """Simple heuristic gesture detection."""
        # Get landmark points
        lm = landmarks.landmark
        
        # 1. 'Box' Gesture (Index and Thumb tips close, others folded)
        # We check distance between thumb tip (4) and index tip (8)
        dist_thumb_index = ((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2)**0.5
        
        # Check if other fingers are folded (tips below pips)
        middle_folded = lm[12].y > lm[10].y
        ring_folded = lm[16].y > lm[14].y
        pinky_folded = lm[20].y > lm[18].y

        if dist_thumb_index < 0.05 and middle_folded and ring_folded and pinky_folded:
            return "BOX"

        # 2. 'Peace/V' Gesture (Index and Middle up, others folded)
        index_up = lm[8].y < lm[6].y
        middle_up = lm[12].y < lm[10].y
        if index_up and middle_up and ring_folded and pinky_folded:
            return "PEACE"

        # 3. 'Open Palm' (All up)
        if index_up and middle_up and not ring_folded and not pinky_folded:
            return "PALM"

        return None

    def _trigger_action(self, gesture):
        print(f"Gesture Detected: {gesture}")
        if gesture == "BOX":
            speak("Gesture recognized: Opening application launcher.")
            execute_command("open calculator") # Example action
        elif gesture == "PEACE":
            speak("Peace gesture detected. All systems nominal.")
        elif gesture == "PALM":
            # Potentially used to 'pause' or 'stop' speech
            pass

def start_gestures():
    processor = GestureProcessor()
    processor.start()
    return processor
