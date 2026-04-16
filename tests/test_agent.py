import sys; sys.path.append("/tmp"); import monkey_patch2
import sys; sys.path.append("/tmp"); import monkey_patch
import google.genai._api_client
original_req = google.genai._api_client.BaseApiClient.async_request
async def mock_req(self, method, path, r, h):
    print(f"ADK HITTING: {path}")
    return await original_req(self, method, path, r, h)
google.genai._api_client.BaseApiClient.async_request = mock_req

import os
import google.auth
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

import os
import subprocess
import time
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from app.tools import run_bash_command_in_sandbox

def run_ralph():
    session_service = InMemorySessionService()
    session = session_service.create_session_sync(user_id="ralph", app_name="tictactoe")
    runner = Runner(agent=root_agent, session_service=session_service, app_name="tictactoe")

    print("> Starting RALPH Loop for Tic Tac Toe")
    
    prompt = """
    You are an autonomous developer Agent. Your goal is to build a high-quality Tic Tac Toe application in Python.
    
    STEPS:
    1. Write the complete, runnable Python code for a command-line Tic-Tac-Toe game to /tmp/tictactoe_ralph.py using the `run_bash_command_in_sandbox` tool.
       The game must include a simple AI opponent or a mocked run so it can be tested without user input, or use parameterized test cases.
       Make sure the code quality is excellent (passes an LLM rater).
    2. Write a minimal test file `/tmp/test_tictactoe.py` testing basic logic (like winning conditions).
    3. Run `python /tmp/test_tictactoe.py` via the bash tool.
    4. If it fails, fix the code and run again.
    5. Summarize your results and declare SUCCESS when tests pass.
    """
    
    message = types.Content(
        role="user", parts=[types.Part.from_text(text=prompt)]
    )

    print("Sending prompt to Agent...")
    for event in runner.run(
        new_message=message,
        user_id="ralph",
        session_id=session.id,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(f"Agent: {part.text}")
                elif getattr(part, 'function_call', None):
                    print(f"Tool Call: {part.function_call.name}({part.function_call.args})")
        if getattr(event, 'tool_response', None):
            print(f"Tool Result: {event.tool_response}")
            
    print("> RALPH Loop execution finished.")

    # Verification
    print("> Verifying Output...")
    output = run_bash_command_in_sandbox("cat /tmp/tictactoe_ralph.py")
    if "def" in output:
        print("Success! /tmp/tictactoe_ralph.py was created.")
    else:
        print("Failed to find valid code in /tmp/tictactoe_ralph.py")
        
    test_out = run_bash_command_in_sandbox("python /tmp/test_tictactoe.py")
    print("Test output:")
    print(test_out)

if __name__ == "__main__":
    run_ralph()
