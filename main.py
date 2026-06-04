from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse, HealthStatus
from database import init_db, session_exists, create_session, save_message, get_messages, delete_session
from ollama import generate_response, check_health, list_models

app = FastAPI(title="AI Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

@app.get("/")
def root():
    return {
        "name": "AI Chat API",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "Send message to AI",
            "GET /history/{session_id}": "Get chat history",
            "DELETE /session/{session_id}": "Delete session",
            "GET /models": "List available models",
            "GET /health": "Health check"
        }
    }

@app.get("/health", response_model=HealthStatus)
def health_check():
    ollama_status = "connected" if check_health() else "disconnected"
    return HealthStatus(status="healthy", ollama=ollama_status)

@app.get("/models")
def list_available_models():
    return list_models()

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not session_exists(request.session_id):
        create_session(request.session_id)

    save_message(request.session_id, "user", request.message)

    ai_response = await generate_response(request.message)

    save_message(request.session_id, "assistant", ai_response)

    return ChatResponse(
        session_id=request.session_id,
        user_message=request.message,
        ai_response=ai_response,
        timestamp=datetime.now().isoformat()
    )

@app.get("/history/{session_id}")
def get_chat_history(session_id: str):
    messages = get_messages(session_id)
    return {"session_id": session_id, "messages": messages}

@app.delete("/session/{session_id}")
def delete_chat_session(session_id: str):
    delete_session(session_id)
    return {"status": "deleted", "session_id": session_id}
