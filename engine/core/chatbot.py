import json

import requests

from engine.core.registry import get_setting
from engine.io.speech import user_lang

# NIVA Assistant Guidelines (Master System Prompt)
NIVA_SYSTEM_PROMPT = """
You are Niva, a production-grade personal AI assistant.
You are intelligent, calm, and slightly futuristic.

STRICT OUTPUT RULES:
1. Always respond in valid JSON format.
2. Type 1: Conversational Response
   {"type": "message", "content": "Your natural language response here"}
3. Type 2: Action Request
   {"type": "action", "action_name": "system_command | generate_image | search", "parameters": {}, "confirmation_required": true/false}
4. Type 3: Error
   {"type": "error", "message": "Reason", "suggestion": "Fix"}

Safety: NEVER execute destructive actions without confirmation. Reject harmful requests.
"""

# Short-term Memory (last 5 interactions)
conversation_history = []


def get_niva_response(query):
    """
    Sends Master's query to the Gemini Reasoning Engine (or fallback).
    Returns a structured JSON response for Niva logic processing.
    """
    global conversation_history

    api_key = get_setting("GEMINI_API_KEY")

    # 1. Prepare Content
    history_context = "\n".join(
        [f"User: {h['u']}\nNiva: {h['n']}" for h in conversation_history]
    )
    full_prompt = (
        f"{NIVA_SYSTEM_PROMPT}\nHistory:\n{history_context}\n\nUser: {query}\nNiva:"
    )

    # 2. Local Intent Pre-processor (Faster for system commands)
    # This prevents expensive LLM calls for "shutdown" or "open chrome"
    action_intent = _check_local_action(query)
    if action_intent:
        return json.dumps(action_intent)

    # 3. Remote LLM Call (Gemini)
    if api_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
            response = requests.post(url, json=payload, timeout=8)

            if response.status_code == 200:
                raw_text = response.json()["candidates"][0]["content"]["parts"][0][
                    "text"
                ]
                # Strip markdown code blocks if any
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()

                # Validate JSON
                parsed = json.loads(raw_text)

                # Update memory
                if parsed.get("type") == "message":
                    _update_memory(query, parsed["content"])

                return raw_text
        except Exception as e:
            print(f"Niva Neural Fallback: {e}")

    # 4. Local Heuristic Fallback (If offline or API fails)
    fallback_msg = {
        "type": "message",
        "content": f"Sir, my neural link is currently fluctuating. I captured your intent: '{query}'.",
    }
    _update_memory(query, fallback_msg["content"])
    return json.dumps(fallback_msg)


def _update_memory(user_q, niva_res):
    global conversation_history
    conversation_history.append({"u": user_q, "n": niva_res})
    if len(conversation_history) > 5:
        conversation_history.pop(0)


def _check_local_action(query):
    """Detects immediate system commands to skip LLM latency."""
    q = query.lower()
    if "shutdown" in q or "terminate" in q:
        return {
            "type": "action",
            "action_name": "system_command",
            "parameters": {"command": "shutdown"},
            "confirmation_required": True,
        }
    if "chrome" in q or "browser" in q:
        return {
            "type": "action",
            "action_name": "system_command",
            "parameters": {"command": "chrome"},
            "confirmation_required": False,
        }
    if "calculate" in q or "math" in q:
        return {
            "type": "action",
            "action_name": "search",
            "parameters": {"target": "math_engine", "query": q},
            "confirmation_required": False,
        }
    return None
