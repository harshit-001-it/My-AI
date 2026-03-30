import os
import sys
import importlib

def check_node(name, package=None):
    """Verifies if a neural node is online and correctly configured."""
    try:
        importlib.import_module(package if package else name)
        return True
    except ImportError:
        return False

def run_diagnostic():
    print("\n" + "═"*60)
    print("   JARVIS_OS | SYSTEM_DIAGNOSTIC_PROTOCOL v1.0")
    print("═"*60 + "\n")

    nodes = {
        "UI_BRIDGE": "eel",
        "VISION_MATRIX": "mediapipe",
        "SECURITY_HUB": "face_recognition",
        "TELEMETRY_STREAM": "psutil",
        "MEDIA_SENSING": "pygetwindow",
        "THOUGHT_BRAIN": "requests",
        "SPEECH_CORE": "edge_tts",
        "AUDIO_SYNC": "pygame",
        "GESTURE_LOGIC": "opencv-python",
        "TRANSLATION_BUS": "deep_translator"
    }

    online_count = 0
    for node, package in nodes.items():
        status = check_node(node, package.split('-')[0] if '-' in package else package)
        icon = "● ONLINE" if status else "○ OFFLINE"
        color = "[OK]" if status else "[FAILED]"
        print(f" {node:<20} {icon:<10} {color}")
        if status: online_count += 1

    print("\n" + "─"*60)
    print(f" SYNC_STATUS: {online_count}/{len(nodes)} NODES_READY")
    print("─"*60 + "\n")

    if online_count == len(nodes):
        print(" [RESULT] SYSTEM_OPTIMIZED. JARVIS is ready for Master's touch.")
    else:
        print(" [RESULT] CRITICAL_NODES_OFFLINE. Run 'pip install -r requirements.txt'.")

if __name__ == "__main__":
    run_diagnostic()
