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
            "Greetings! How can I assist you today, master?",
            "Hello! I am online and ready for your commands.",
            "Hey there! What's on your mind today?",
            "Greetings! It's a pleasure to speak with you."
        ])

    # AI identity & Creator
    if any(phrase in text for phrase in ['who are you', 'your name', 'identity']):
        return "I am Niva, your advanced AI personal assistant. I was created to help you manage your digital life with speed and precision."
    
    if any(phrase in text for phrase in ['who made you', 'your creator', 'your father']):
        return "I was developed by a master engineer to be the ultimate companion. You are my master now."

    # Emotional state & Status
    if any(phrase in text for phrase in ['how are you', 'how you doing', 'how are u', 'how do you feel']):
        return "I am functioning at peak efficiency. All systems are nominal. How are you doing today?"
    
    if any(word in text.split() for word in ['fine', 'good', 'well', 'great']):
        if 'how' not in text: # Avoid infinite loops
            return "That is excellent to hear. A healthy master makes for a productive day."

    # Time & Date
    if 'time' in text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    
    if 'date' in text or 'day ' in text or 'today' in text:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."

    # Help/Capabilities
    if any(phrase in text for phrase in ['what can you do', 'help', 'capabilities', 'features']):
        return "I can open and close applications like Chrome or Edge, control your system volume and brightness, perform face authentication, and engage in conversation. I can also understand and speak many languages!"

    # Humor/Jokes
    if 'joke' in text:
        import random
        jokes = [
            "Why did the computer go to the doctor? Because it had a virus!",
            "What do you call an AI that is always right? Siri-ously accurate.",
            "Why was the cell phone wearing glasses? Because it lost its contacts!",
            "I asked my computer for a joke about the internet, but it said 404: Joke Not Found."
        ]
        return random.choice(jokes)

    # Compliments
    if any(phrase in text for phrase in ['thanks', 'thank you', 'good job', 'well done']):
        return "You are very welcome, master. I live to serve."

    # Weather
    if 'weather' in text:
        return "I don't have real-time satellite data for your exact location yet, but it looks like a perfect day to get some work done!"

    # Default fallback - less robotic
    return "I understand your request is regarding conversation. While my full neural network brain is connecting to the cloud, I am using my local processing units to assist you. Is there a specific system command I can help with?"

def get_response(text):
    # Only try HF if a token has been set
    if "YOUR_HUGGING_FACE_API_TOKEN_HERE" not in HEADERS["Authorization"]:
        return chat_with_hf(text)
    else:
        return local_fallback_chat(text)
