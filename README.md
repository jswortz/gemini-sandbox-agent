# Gemini Sandbox Agent

A Python ADK container that exposes an A2A-compliant agent card capable of running persistent Headless bash commands using a local `tmux` sandbox. It allows Gemini Enterprise agents to perform background compute tasks, build code, and execute bash sequentially, acting exactly as a persistent Linux endpoint.

## Configuration & Deployment

This agent relies on the Google GenAI SDK. To bypass Vertex AI quotas and explicitly use the Gemini Developer API, you must configure a `GEMINI_API_KEY`.

### Local Deployment
To run locally:
```bash
export GEMINI_API_KEY="your-api-key"
adk api_server . --a2a --auto_create_session
```

### Cloud Run Deployment
Deploy to Cloud Run by mounting your Secret Manager key:

```bash
gcloud run deploy gemini-sandbox-agent \
  --source . \
  --region us-east1 \
  --project <your-project-id> \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest" \
  --allow-unauthenticated
```

The A2A endpoint will be available at:
`https://<your-cloud-run-domain>/a2a/sandbox_agent`

The properly formatted Agent Card is served dynamically on:
`https://<your-cloud-run-domain>/a2a/sandbox_agent/.well-known/agent-card.json`
