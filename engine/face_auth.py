try:
    import cv2
    import face_recognition
except ImportError:
    cv2 = None
    face_recognition = None

import os
import time
import numpy as np

def capture_reference():
    if not cv2:
        print("Camera/OpenCV not available.")
        return

    video_capture = cv2.VideoCapture(0)
    print("Please look at the camera for face registration...")
    
    while True:
        ret, frame = video_capture.read()
        if not ret or frame is None:
            continue
            
        cv2.imshow('Registration - Press Space to Capture', frame)
        
        if cv2.waitKey(1) & 0xFF == ord(' '):
            if not os.path.exists("engine/db"):
                os.makedirs("engine/db")
            # Save a clean copy
            cv2.imwrite("engine/db/user_reference.jpg", frame)
            break
            
    video_capture.release()
    cv2.destroyAllWindows()
    print("Reference image captured successfully.")

def check_for_uploads():
    """Scans the db folder for manual uploads and processes them into a reference."""
    db_path = "engine/db"
    if not os.path.exists(db_path):
        return None

    # Supported formats
    image_exts = ['.jpg', '.jpeg', '.png']
    video_exts = ['.mp4', '.avi', '.mov']

    files = os.listdir(db_path)
    
    # Check if reference already exists, if so, just return it
    if "user_reference.jpg" in files:
        return "engine/db/user_reference.jpg"

    print("Checking uploaded media for a valid face...")
    for file in files:
        if file == "user_reference.jpg": continue
        full_path = os.path.join(db_path, file)
        ext = os.path.splitext(file)[1].lower()

        if ext in image_exts:
            try:
                img = cv2.imread(full_path)
                if img is None: 
                    print(f"Skipping {file}: Could not read image.")
                    continue
                
                # Convert to RGB and ensure it's C-contiguous (Numpy 2.0 compatibility)
                rgb = np.ascontiguousarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), dtype=np.uint8)
                
                print(f"Scanning {file}...")
                if face_recognition.face_encodings(rgb):
                    print(f"Found face in {file}. Registering as reference...")
                    cv2.imwrite("engine/db/user_reference.jpg", img)
                    return "engine/db/user_reference.jpg"
            except Exception as e:
                print(f"Error scanning {file}: {e}")
                continue

        elif ext in video_exts:
            try:
                cap = cv2.VideoCapture(full_path)
                print(f"Scanning video {file}...")
                # Sample 5 frames from the video
                for _ in range(30): # Skip some early frames
                    cap.grab()
                
                for i in range(5): # Check 5 frames
                    ret, frame = cap.read()
                    if not ret: break
                    rgb = np.ascontiguousarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), dtype=np.uint8)
                    if face_recognition.face_encodings(rgb):
                        print(f"Found face in video {file} (frame {i}). Registering...")
                        cv2.imwrite("engine/db/user_reference.jpg", frame)
                        cap.release()
                        return "engine/db/user_reference.jpg"
                    # Skip 10 frames for variety
                    for _ in range(10): cap.grab()
                cap.release()
            except Exception as e:
                print(f"Error scanning video {file}: {e}")
                continue
    
    return None

def authenticate():
    if not cv2 or not face_recognition:
        print("Face authentication dependencies missing.")
        return False

    # Check for manual uploads first
    ref_path = check_for_uploads()
    
    if not ref_path:
        print("No reference image found. Please register your face first.")
        capture_reference()
        ref_path = "engine/db/user_reference.jpg"
        if not os.path.exists(ref_path):
            return False

    try:
        # Load using cv2 and force 8-bit conversion
        img = cv2.imread("engine/db/user_reference.jpg")
        if img is None:
            print("Error: Could not read reference image file.")
            if os.path.exists("engine/db/user_reference.jpg"):
                os.remove("engine/db/user_reference.jpg")
            return False
            
        # Resize if image is too large (to speed up encoding)
        height, width = img.shape[:2]
        if width > 1000:
            ratio = 1000.0 / width
            img = cv2.resize(img, (1000, int(height * ratio)))

        # Convert to RGB and explicitly cast to uint8 and ensure C-contiguous
        reference_image = np.ascontiguousarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), dtype=np.uint8)
        
        print(f"Loading reference... Image info: {reference_image.shape}, {reference_image.dtype}, Contiguous: {reference_image.flags.c_contiguous}")
        
        encodings = face_recognition.face_encodings(reference_image)
        if not encodings:
            print("Error: No face detected in the reference image. Deleting reference to try again.")
            os.remove("engine/db/user_reference.jpg")
            return False
            
        reference_encoding = encodings[0]
    except Exception as e:
        print(f"Error during authentication setup: {e}")
        # If it fails here, the reference might be corrupted
        if os.path.exists("engine/db/user_reference.jpg"):
            os.remove("engine/db/user_reference.jpg")
        return False

    video_capture = cv2.VideoCapture(0)
    auth_success = False
    start_time = time.time()
    
    while time.time() - start_time < 10:
        ret, frame = video_capture.read()
        if not ret:
            continue
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([reference_encoding], face_encoding)
            if True in matches:
                auth_success = True
                break
        
        if auth_success:
            break
            
        cv2.imshow('Authentication - Scanning...', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return auth_success
