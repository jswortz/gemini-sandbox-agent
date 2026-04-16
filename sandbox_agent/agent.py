import os
import google.auth
_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
# os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from google.adk.tools import FunctionTool

from .tools import run_bash_command_in_sandbox

# Setting up the model
model = Gemini(
    model="gemini-2.5-flash",
    retry_options=types.HttpRetryOptions(attempts=3),
)

root_agent = Agent(
    name="sandbox_agent",
    model=model,
    description="I am an agent capable of running persistent Headless bash commands via a local tmux sandbox. I can also trigger gemini cli through this sandbox if needed.",
    instruction="""You are an expert software developer and Cloud Run provisioner.
You have access to a sandbox environment via a persistent tmux session.
You can execute bash commands and test out workflows.
You are tasked with building a Tic Tac Toe application evaluating logic, and passing an LLM rater.
IMPORTANT RULES:
1. Use the `run_bash_command_in_sandbox` tool to explore, build, and test applications.
2. State persists across `run_bash_command_in_sandbox` calls because it uses a persistent tmux session.
3. If you want to use the gemini CLI, you can invoke it here headless.
4. Make sure to solve the task directly or break it down into steps, applying your bash command tool multiple times as needed.
""",
    tools=[
        FunctionTool(func=run_bash_command_in_sandbox),
    ]
)

# Convert to A2A Application
from google.adk.apps import App
app = App(
    root_agent=root_agent,
    name="sandbox_agent"
)
