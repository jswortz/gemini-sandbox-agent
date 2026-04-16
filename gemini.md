# Gemini Enterprise Sandbox Agent

This repository contains an ADK agent that runs within an ephemeral sandbox powered by Cloud Run and interacts bidirectionally with Gemini Enterprise using the A2A (Agent-To-Agent) protocol.
This setup confirms that a custom agent built via the Agent Development Kit (ADK) can provision sandboxes for head-less development tasks.

## Architecture

*   **Agent Development Kit (ADK)**: Facilitates tool invocation, LLM routing, and basic conversational flows.
*   **A2A Protocol**: Allows Dolphin / Gemini Enterprise instances to "talk" to the ADK agent, streaming responses reliably.
*   **Sticky Sessions**: Tmux is used under the hood in the `run_bash_command_in_sandbox` tool. This satisfies the requirement for stateful directory navigation or long-term background processes, surviving single turn disconnections.

## Future Path
We will integrate a `BigQueryLoggerConfig` for analytics and further evaluation skills for LLM-level self-raters in evaluating codebase modifications. 
