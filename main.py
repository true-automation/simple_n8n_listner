from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import os
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Math & Chat API",
    description="API for performing math operations and chat interactions",
    version="2.1.1"
)

# Bytez API Configuration
BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")
BYTEZ_API_URL = "https://api.bytez.com/models/v2/deepseek-ai/DeepSeek-V3.2"
CHAT_ENABLED = bool(BYTEZ_API_KEY)

# --- Models ---
class Numbers(BaseModel):
    x: float
    y: float

class Result(BaseModel):
    sum: float
    mult: float

class ChatRequest(BaseModel):
    question: str
    stream: bool = False
    max_length: int = 500
    temperature: float = 0.7

class ChatResponse(BaseModel):
    answer: Optional[str] = None
    error: Optional[str] = None

# --- Routes ---
@app.get("/")
async def root():
    return {
        "message": "Math & Chat API",
        "endpoints": {
            "/calculate": "POST - Calculate sum and multiplication of two numbers",
            "/chat": "POST - Send a question and get AI response",
            "/health": "GET - Health check"
        },
        "chat_enabled": CHAT_ENABLED
    }

@app.post("/calculate", response_model=Result)
async def calculate(numbers: Numbers) -> Result:
    return Result(
        sum=numbers.x + numbers.y,
        mult=numbers.x * numbers.y
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    if not CHAT_ENABLED:
        return ChatResponse(
            answer=None,
            error="Chat feature is not available. BYTEZ_API_KEY not configured."
        )

    try:
        logger.info(f"Processing chat request: {request.question[:50]}...")

        payload = {
            "messages": [{"role": "user", "content": request.question}],
            "stream": request.stream,
            "params": {
                "max_length": request.max_length,
                "temperature": request.temperature
            }
        }

        headers = {
    "Authorization": BYTEZ_API_KEY,
    "Content-Type": "application/json"
}

        response = requests.post(BYTEZ_API_URL, json=payload, headers=headers, timeout=30)
        logger.info(f"Bytez API response status: {response.status_code}")

        if response.status_code != 200:
            error_msg = f"Bytez API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return ChatResponse(answer=None, error=error_msg)

        result = response.json()
        logger.info(f"Bytez API response: {result}")

        # --- Extract answer safely ---
        answer = None

        # Common top-level keys
        for key in ("output", "response", "text", "content", "message"):
            if isinstance(result, dict) and key in result:
                answer = result[key]
                break

        # OpenAI-style "choices" array
        if not answer and isinstance(result, dict) and "choices" in result:
            choices = result.get("choices", [])
            if choices and isinstance(choices[0], dict):
                answer = choices[0].get("message", {}).get("content")

        # Data field
        if not answer and isinstance(result, dict) and "data" in result:
            data = result["data"]
            if isinstance(data, dict):
                answer = data.get("content") or data.get("text")
            elif isinstance(data, str):
                answer = data

        # Fallback: if result is a string
        if not answer and isinstance(result, str):
            answer = result

        # Final fallback: dump full JSON as string
        if not answer:
            answer = str(result)

        return ChatResponse(answer=answer, error=None)

    except requests.exceptions.Timeout:
        error_msg = "Request timed out. The AI model took too long to respond."
        logger.error(error_msg)
        return ChatResponse(answer=None, error=error_msg)

    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        return ChatResponse(answer=None, error=error_msg)

    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return ChatResponse(answer=None, error=error_msg)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "chat_enabled": CHAT_ENABLED}
