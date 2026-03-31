import cv2
import threading
import time
import mediapipe as mp
from engine.core.command import execute_command
from engine.io.speech import speak

try:
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
except AttributeError:
    mp_hands = None
    mp_draw = None

class GestureProcessor:
    def __init__(self):
        if mp_hands is None:
            raise Exception("MediaPipe 'solutions' not supported in this Python version.")
        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.is_running = False
        self.last_gesture_time = 0
        self.cooldown = 1.5 
        self.prev_x = 0
        self.prev_y = 0
        self.presence_lost_count = 0
        self.MAX_ABSENCE = 20 # 20 cycles of absence before shield

    def start(self):
        self.is_running = True
        threading.Thread(target=self._process, daemon=True).start()
        print("Niva Vision: Gesture Node Active.")

    def stop(self):
        self.is_running = False

    def _process(self):
        cap = cv2.VideoCapture(0)
        while self.is_running:
            ret, frame = cap.read()
            if not ret: continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                self.presence_lost_count = 0
                import eel
                try: eel.set_privacy_shield(False)()
                except: pass
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = self._detect_gesture(hand_landmarks)
                    if gesture and (time.time() - self.last_gesture_time > self.cooldown):
                        self._trigger_action(gesture)
                        self.last_gesture_time = time.time()
                    self._track_movement(hand_landmarks)
            else:
                self.presence_lost_count += 1
                if self.presence_lost_count > self.MAX_ABSENCE:
                    import eel
                    try: eel.set_privacy_shield(True)()
                    except: pass

            # In production, we don't need a debug window
            # if cv2.waitKey(1) & 0xFF == ord('q'): break

        cap.release()

    def _detect_gesture(self, landmarks):
        lm = landmarks.landmark
        index_up = lm[8].y < lm[6].y
        middle_up = lm[12].y < lm[10].y
        ring_up = lm[16].y < lm[14].y
        pinky_up = lm[20].y < lm[18].y
        thumb_up = lm[4].x > lm[3].x if lm[4].x > 0.5 else lm[4].x < lm[3].x

        if index_up and middle_up and ring_up and pinky_up: return "STOP"
        if index_up and middle_up and not ring_up and not pinky_up: return "PEACE"
        dist_it = ((lm[4].x - lm[8].x)**2 + (lm[4].y - lm[8].y)**2)**0.5
        if dist_it < 0.05 and not middle_up and not ring_up: return "PINCH"
        if thumb_up and pinky_up and not index_up and not middle_up and not ring_up: return "CALL"
        return None

    def _track_movement(self, landmarks):
        curr_x = landmarks.landmark[8].x
        curr_y = landmarks.landmark[8].y
        self.prev_x = curr_x
        self.prev_y = curr_y

    def _trigger_action(self, gesture):
        print(f"Niva Vision: Intent Cluster matched gesture -> {gesture}")
        if gesture == "STOP":
            speak("All ongoing tasks paused.")
        elif gesture == "PEACE":
            speak("Systems are optimal, Master.")
        elif gesture == "PINCH":
            execute_command("calculator open")
        elif gesture == "CALL":
            speak("Initiating secure communication link.")

def start_gestures():
    try:
        processor = GestureProcessor()
        processor.start()
        return processor
    except Exception as e:
        print(f"Failed to start Niva GestureProcessor: {e}")
        return None
