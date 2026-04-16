import requests
import time
import json
import uuid
import sys

URL = "https://gemini-sandbox-agent-679926387543.us-east1.run.app/run"
SESSION_ID = f"sess_{uuid.uuid4().hex}"

def run_agent(text_prompt: str, invocation_id: str = None):
    payload = {
        "app_name": "sandbox_agent",
        "user_id": "test_tester",
        "session_id": SESSION_ID
    }
    if text_prompt:
        payload["new_message"] = {"role": "user", "parts": [{"text": text_prompt}]}
    if invocation_id:
        payload["invocation_id"] = invocation_id
        
    response = requests.post(URL, json=payload, timeout=900)
    try:
        data = response.json()
        with open("/tmp/response.json", "w") as f:
            json.dump(data, f)
        return data
    except Exception as e:
        return None

if __name__ == "__main__":
    prompt = "Can you cat /tmp/tictactoe_ralph.py and /tmp/test_tictactoe.py ? I just need to verify they exist in this container!"
    run_agent(prompt)
