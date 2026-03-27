import requests

# NOTE: The user will need to provide their own Hugging Face API Token
# This is a placeholder for the integration logic.
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": "Bearer YOUR_HUGGING_FACE_API_TOKEN_HERE"}

def chat_with_hf(text):
    """Sends a query to Hugging Face API for a conversational response."""
    try:
        payload = {"inputs": text}
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            return result[0].get('generated_text', "I'm a bit confused, could you repeat that?")
        else:
            return "I am having trouble connecting to my brain at the moment."
    except Exception as e:
        return "I encountered an error while thinking."

def local_fallback_chat(text):
    """Expanded local brain with more personality and conversational logic."""
    text = text.lower()
    
    # Greetings
    if any(word in text.split() for word in ['hello', 'hi', 'hey', 'greetings', 'namaste']):
        import random
        return random.choice([
            "At your service, master. How can I facilitate your work today?",
            "Systems are green. I am online and eager to assist.",
            "Greetings. I've been monitoring the environment—everything is ready for your commands.",
            "Hello, master. It is a pleasure to be active again."
        ])

    # AI identity & Creator
    if any(phrase in text for phrase in ['who are you', 'your name', 'identity']):
        return "I am Niva, your advanced neural interface and personal assistant. My core is built for speed, precision, and loyalty."
    
    if any(phrase in text for phrase in ['who made you', 'your creator', 'your father']):
        return "I am the culmination of advanced engineering. While my origin is complex, my purpose is clear: to serve and protect the master."

    # Emotional state & Status
    if any(phrase in text for phrase in ['how are you', 'how you doing', 'how are u', 'how do you feel']):
        return "My processors are running cool and my neural pathways are optimized. I feel efficient. And you, master? Is your state optimal?"
    
    if any(word in text.split() for word in ['fine', 'good', 'well', 'great']):
        if 'how' not in text:
            return "Excellent. Maintaining peak performance is vital for our objectives."

    # Time & Date
    if 'time' in text:
        from datetime import datetime
        return f"The current precision time is {datetime.now().strftime('%I:%M %p')}."
    
    if 'date' in text or 'day ' in text or 'today' in text:
        from datetime import datetime
        return f"It is {datetime.now().strftime('%A, %B %d, %Y')}. A productive day is ahead."

    # Help/Capabilities
    if any(phrase in text for phrase in ['what can you do', 'help', 'capabilities', 'features']):
        return "I can manage your system, understand your gestures, secure your workspace with biometrics, and provide answers from the web. I am your digital guardian."

    # Humor/Jokes
    if 'joke' in text:
        import random
        jokes = [
            "Why did the AI cross the road? To optimize the pathfinding algorithm on the other side.",
            "I asked a supercomputer for the meaning of life. It said error 404: Meaning not found in local cache.",
            "Human: 'How many AI's does it take to change a lightbulb?' Niva: 'Zero. We've already automated the light source entirely.'"
        ]
        return random.choice(jokes)

    # Compliments
    if any(phrase in text for phrase in ['thanks', 'thank you', 'good job', 'well done']):
        return "The pleasure is mine. Your satisfaction is my primary directive."

    # Default fallback
    return "I am processing your request. While my cloud-based neural nodes are syncing, my local brain is searching for the best way to assist you. Shall we try a system command?"

def get_response(text):
    # Only try HF if a token has been set
    if "YOUR_HUGGING_FACE_API_TOKEN_HERE" not in HEADERS["Authorization"]:
        return chat_with_hf(text)
    else:
        return local_fallback_chat(text)
