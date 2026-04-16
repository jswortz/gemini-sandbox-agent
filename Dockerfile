FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tmux bash && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We copy everything so the repo is visible as /app, with sandbox_agent dir inside
COPY . /app

EXPOSE 8080

CMD ["adk", "api_server", ".", "--host", "0.0.0.0", "--port", "8080", "--a2a", "--auto_create_session"]
