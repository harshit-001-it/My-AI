import json
import os

REGISTRY_FILE = "engine/registry.json"

DEFAULT_SETTINGS = {
    "user_name": "Master",
    "voice_pin": "1234",
    "theme": "obsidian_kinetic",
    "preferred_browser": "chrome",
    "task_history": [],
    "last_login": None,
}


def load_registry():
    if not os.path.exists(REGISTRY_FILE):
        save_registry(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        save_registry(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_registry(data):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def update_setting(key, value):
    data = load_registry()
    data[key] = value
    save_registry(data)


def get_setting(key, default_value=None):
    data = load_registry()
    return data.get(key, default_value)


def add_task(task_desc):
    data = load_registry()
    data["task_history"].append(
        {
            "timestamp": str(os.times()),  # Placeholder for real timestamp
            "task": task_desc,
        }
    )
    if len(data["task_history"]) > 50:
        data["task_history"].pop(0)
    save_registry(data)


# Initialize
if __name__ == "__main__":
    print("Registry initialized.")
    registry = load_registry()
    print(f"User: {registry['user_name']}")
