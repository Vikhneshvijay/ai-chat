import os
import httpx
from fastapi import HTTPException

OLLAMA_API = os.getenv("OLLAMA_API", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")

async def generate_response(prompt: str, model: str = MODEL_NAME) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_API}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30
            )

        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Ollama API error")

        return response.json().get("response", "")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {str(e)}")

def check_health() -> bool:
    try:
        httpx.get(f"{OLLAMA_API}/api/tags", timeout=5)
        return True
    except:
        return False

def list_models() -> dict:
    try:
        response = httpx.get(f"{OLLAMA_API}/api/tags", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Failed to fetch models from Ollama")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch models: {str(e)}")
