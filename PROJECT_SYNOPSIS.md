# PROJECT SYNOPSIS: Niva AI Assistant

## 🎯 Project Identity
**Niva** is a personal AI assistant developed for Windows laptops. It combines voice interaction, facial security, and system automation to provide a "master-companion" experience.

---

## 🏗️ Architecture & Stack
- **Backend**: Python 3.13+
- **Frontend**: HTML5, CSS3, JavaScript (Eel Framework)
- **Security**: Face Recognition (dlib/OpenCV)
- **Interaction**: pyttsx3 (Text-to-Speech) & SpeechRecognition (Google API)
- **UI Logic**: Chrome/Edge browser instance via Eel

---

## 🧩 Core Modules (`engine/`)

### 1. `main.py` (Orchestrator)
- Initializes the Eel web server (`www/`).
- Handles auto-dependency installation from `requirements.txt`.
- Manages the main background loop (`niva_loop`) and wake-word detection.

### 2. `speech.py` (Voice Engine)
- **Speak**: Uses a background thread with a queue to prevent blocking. Supports multi-language translation (via `deep-translator`).
- **Listen**: Recognizes speech using Google Web Speech API. Includes automatic translation of foreign languages to English for system commands.

### 3. `command.py` (Skill Layer)
- Maps voice/text queries to system actions:
    - Browser control (Chrome, Edge).
    - System utilities (Volume, Brightness, Screenshots).
    - Information retrieval (Wikipedia, Google Search, YouTube).
    - Fallback: Passes general queries to `chatbot.py`.

### 4. `face_auth.py` (Security)
- Handles user registration (saving a reference to `engine/db/user_reference.jpg`).
- Compares live camera feed with the reference image using `face_recognition`.
- Gracefully bypasses security if hardware/libraries are missing.

### 5. `chatbot.py` (Brain)
- **Remote**: Optional Hugging Face integration (`Blenderbot 400M`).
- **Local**: A robust fallback system for offline interaction, personality responses, and utility queries (time, date, jokes).

---

## 🛠️ Environment & Setup
- **Dependencies**: Listed in `requirements.txt`. Automatic installation is handled by `main.py`.
- **Hardware**: Requires a Microphone and Camera.
- **Languages**: Default recognition is `en-IN`. Response language defaults to `en` but shifts to `hi` if Hindi is detected.

---

## 🚀 Future Roadmap for Agents
1. **API Integration**: Complete the Hugging Face token integration in `chatbot.py`.
2. **Skill Expansion**: Add more system commands like "Shutdown", "Restart", or File Explorer navigation.
3. **UI Enhancements**: Modernize the `www/style.css` for a more premium "Star Trek" console look.
4. **Offline NLP**: Investigate small local LLMs to replace the simple `local_fallback_chat`.

---

## ⚠️ Notes for Future Agents
- **Avoid Over-Speaking**: The system should remain silent until the wake word "Niva" (or phonetic matches) is heard.
- **Port Conflict**: Eel defaults to port 8000; ensure this is clear or dynamically allocated.
- **Translation Lag**: Avoid heavy translation in the `listen()` loop to maintain low latency.
