# AI Chat API

FastAPI application with local LLM integration using Ollama and PostgreSQL for chat history.

## Features

- Chat with local LLM (Mistral, Llama2, etc. via Ollama)
- Chat history persistence in PostgreSQL
- Session-based conversations
- Health check and model listing endpoints
- Production-ready with Docker and ECS deployment
- CI/CD with GitHub Actions

## Local Development

### Prerequisites
- Docker and Docker Compose installed

### Run Locally

```bash
docker compose up
```

The application will be available at `http://localhost:8000`

### Endpoints

- `POST /chat` - Send message to AI
- `GET /history/{session_id}` - Get chat history
- `DELETE /session/{session_id}` - Delete session
- `GET /models` - List available models
- `GET /health` - Health check
- `GET /` - API documentation

### API Examples

```bash
# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "user1", "message": "What is AI?"}'

# Get history
curl http://localhost:8000/history/user1

# List models
curl http://localhost:8000/models

# Health check
curl http://localhost:8000/health
```

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `OLLAMA_API` - Ollama API endpoint (default: http://ollama:11434)
- `MODEL_NAME` - Ollama model to use (default: mistral)

## Deployment

### ECS Deployment

The app is deployed to AWS ECS Fargate using Terraform. GitHub Actions automatically:
1. Builds Docker image
2. Pushes to ECR
3. Updates ECS service

### Required AWS Secrets in GitHub

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_ID
```

## Architecture

```
FastAPI (port 8000)
    ↓
Ollama API (port 11434)
    ↓
PostgreSQL (port 5432)
```

## Development

Edit `main.py` - changes hot-reload due to `--reload` flag in docker-compose.

## Stopping

```bash
docker compose down
```

To remove volumes:

```bash
docker compose down -v
```
# Test CI/CD
