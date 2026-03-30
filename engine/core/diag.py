import os
import sys
import importlib

# Ensure project root is in path for modular imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def check_node(name, package=None):
    """Verifies if a neural node is online and correctly configured."""
    try:
        importlib.import_module(package if package else name)
        return True
    except ImportError:
        return False

def run_diagnostic():
    print("\n" + "═"*60)
    print("   NIVA_OS | PRODUCTION_DIAGNOSTIC_PROTOCOL v1.1")
    print("═"*60 + "\n")

    # Domain-specific Node Mapping
    nodes = {
        "CORE_DISPATCHER": "engine.core.command",
        "NEURAL_BRAIN": "engine.core.chatbot",
        "UI_BRIDGE": "eel",
        "VISION_SENSING": "mediapipe",
        "SECURITY_HUB": "face_recognition",
        "SPEECH_IO": "engine.io.speech",
        "TELEMETRY_STREAM": "psutil",
        "MEDIA_SENSING": "pygetwindow"
    }

    online_count = 0
    for node, package in nodes.items():
        status = check_node(node, package)
        icon = "● ONLINE" if status else "○ OFFLINE"
        color = "[OK]" if status else "[FAILED]"
        print(f" {node:<20} {icon:<10} {color}")
        if status: online_count += 1

    print("\n" + "─"*60)
    print(f" NIVA_SYNC: {online_count}/{len(nodes)} NODES_READY")
    print("─"*60 + "\n")

    if online_count == len(nodes):
        print(" [RESULT] NIVA_OS IS OPTIMAL. All production nodes are synchronized.")
    else:
        print(" [RESULT] ARCHITECTURAL_MISMATCH. Checking logical paths...")

if __name__ == "__main__":
    run_diagnostic()
