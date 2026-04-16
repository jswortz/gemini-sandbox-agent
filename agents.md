# Agent Architecture & Skills

## Deployed Agents
- **sandbox_agent**: The root agent exposed via A2A (`to_a2a`).
  - **Model**: `gemini-3-flash-preview`
  - **Tool**: `run_bash_command_in_sandbox`
  - **Instructions**: Tasked with building complex logic, like passing an LLM rater for a Tic-Tac-Toe Python implementation.
  - **Evaluation (Evals)**: In the future, test automation will incorporate a "ralph loop" that evaluates generated code outputs.

## Development Loop (RALPH)
Read-Act-Log-Plan-Halt (or typical LLM loops).
The agent uses `run_bash_command_in_sandbox` to:
1. Initialize the project file structures.
2. Draft solutions.
3. Use tests or an LLM Rater to inspect the solution quality.
4. Iterate and fix dynamically using bash `sed` or file writes.
