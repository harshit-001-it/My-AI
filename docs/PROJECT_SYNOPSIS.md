# PROJECT SYNOPSIS: Niva AI Assistant

## 🎯 Project Identity
**Niva** is a highly intelligent, multimodal personal AI assistant. It is designed to behave like a Jarvis-style entity, capable of voice, gesture, and visual understanding.

---

## 📜 The Jarvis Mandate
- **Multimodal**: Text, Voice, and Gesture recognition.
- **Security**: Face/Voice/PIN authentication.
- **Visuals**: A transparent, pulsing "Heartbeat" UI.
- **Intelligence**: Context-aware memory and proactive assistance.

---

## 🏗️ Architecture & Stack
- **Backend**: Python 3.13+ (Core Logic)
- **Frontend**: HTML5, CSS3, JavaScript (Eel Framework)
- **Security**: 2FA Security (MediaPipe Face Detection + Voice PIN Verification)
- **Interaction**: edge-tts (Premium Neural Voices) & SpeechRecognition (Google API)
- **Reasoning**: Gemini 1.5 Flash (Primary) with Heuristic Fallback
- **UI Logic**: Chrome/Edge browser instance via Eel

---

## 🧩 Core Modules (`engine/`)

### 1. `main.py` (Orchestrator)
- Initializes the Eel web server (`www/`).
- Handles auto-dependency installation from `requirements.txt`.
- Manages the main background loop (`niva_loop`) and wake-word detection.

### 2. `speech.py` (Voice Engine)
- **Speak**: Uses a background thread with a queue. Prioritizes `edge-tts` (Neural Voices: Ryan/Madhur) with a `pyttsx3` offline fallback. Managed via `pygame` for low-latency playback.
- **Listen**: High-sensitivity capture via `SpeechRecognition` (Google API). Supports `en-IN` and `hi-IN` with automatic cross-translation for logic processing.

### 3. `command.py` (Skill Layer)
- Maps voice/text queries to system actions:
    - Browser control (Chrome, Edge).
    - System utilities (Volume, Brightness, Screenshots).
    - Information retrieval (Wikipedia, Google Search, YouTube).
    - Fallback: Passes general queries to `chatbot.py`.

### 4. `face_auth.py` (Security)
- Implements a streamlined **Biometric Security Grid**.
- Uses MediaPipe for rapid human presence detection.
- Requires a secondary **Voice PIN** (stored in `registry.json`) to grant full system clearance.

### 5. `chatbot.py` (Brain)
- **Remote**: Integrated with **Gemini 1.5 Flash** for high-reasoning conversational depth.
- **Protocol**: Forces structured JSON output for system intent extraction.
- **Local**: Features a local intent pre-processor to handle system commands (shutdown, browser launch) instantly without API latency.

---

## 🛠️ Environment & Setup
- **Backend & Python version**: Native support for Python 3.13+
- **Dependencies**: Listed in `requirements.txt`. Core modules include `psutil` and `eel`.
- **MediaPipe Fallback**: The vision modules (`gestures.py`, `face_auth.py`) gracefully fallback to Voice PIN and disable tracking when the legacy `solutions` API isn't available (common on newer Python 3.13 environments).
- **Hardware**: Requires a Microphone and Camera.
- **Languages**: Default recognition is `en-IN`. Response language shifts depending on voice triggers.

---

## 🚀 Future Roadmap for Agents
1. **Advanced Vision**: Enhance `gestures.py` with more complex control patterns (volume sliding, window dragging).
2. **Skill Expansion**: Add deeper system integration (File Explorer navigation, Battery management, Email drafting).
3. **UI Enhancements**: Modernize the `www/style.css` for a more premium "Star Trek" console look with real-time telemetry graphs.
4. **Offline NLP**: Integrate local small LLMs (like Llama 3 or Phi-3) to ensure 100% functionality without an internet connection.

---

## ⚠️ Notes for Future Agents
- **Avoid Over-Speaking**: The system should remain silent until the wake word "Niva" (or phonetic matches) is heard.
- **Port Conflict**: Eel defaults to port 8000; ensure this is clear or dynamically allocated.
- **Translation Lag**: Avoid heavy translation in the `listen()` loop to maintain low latency.
