from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, Any, List
import os
import logging
import requests

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Math & Chat API",
    description="API for performing math operations and chat interactions",
    version="2.1.0"
)

# Bytez API Configuration
BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY")
BYTEZ_API_URL = "https://api.bytez.com/models/v2/zai-org/GLM-4.6V-Flash"
CHAT_ENABLED = True if BYTEZ_API_KEY else False

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
    """
    Calculate the sum and multiplication of two numbers.
    
    Args:
        numbers: Object containing x and y values
    
    Returns:
        JSON object with sum and mult fields
    """
    return Result(
        sum=numbers.x + numbers.y,
        mult=numbers.x * numbers.y
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Send a question to the AI chat model and get a response.
    
    Args:
        request: Object containing the question and optional parameters
    
    Returns:
        JSON object with answer and error fields
    """
    if not CHAT_ENABLED:
        return ChatResponse(
            answer=None,
            error="Chat feature is not available. BYTEZ_API_KEY not configured."
        )
    
    try:
        logger.info(f"Processing chat request: {request.question[:50]}...")
        
        # Prepare the request payload according to Bytez API v2 format
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": request.question
                }
            ],
            "stream": request.stream,
            "params": {
                "max_length": request.max_length,
                "temperature": request.temperature
            }
        }
        
        # Make request to Bytez API
        headers = {
            "Authorization": BYTEZ_API_KEY,
            "Content-Type": "application/json"
        }
        
        logger.info(f"Calling Bytez API: {BYTEZ_API_URL}")
        
        response = requests.post(
            BYTEZ_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        logger.info(f"Bytez API response status: {response.status_code}")
        
        if response.status_code != 200:
            error_msg = f"Bytez API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return ChatResponse(
                answer=None,
                error=error_msg
            )
        
        # Parse response
        result = response.json()
        logger.info(f"Bytez API response: {result}")
        
        # Extract answer from response
        # The response format may vary, try different common formats
        answer = None
        
        if isinstance(result, dict):
            # Try common response keys
            answer = (
                result.get("output") or
                result.get("response") or
                result.get("text") or
                result.get("content") or
                result.get("message")
            )
            
            # Check if there's a choices array (OpenAI-like format)
            if not answer and "choices" in result:
                choices = result.get("choices", [])
                if choices and len(choices) > 0:
                    first_choice = choices[0]
                    if isinstance(first_choice, dict):
                        message = first_choice.get("message", {})
                        answer = message.get("content")
            
            # Check if there's a data field
            if not answer and "data" in result:
                data = result.get("data")
                if isinstance(data, dict):
                    answer = data.get("content") or data.get("text")
                elif isinstance(data, str):
                    answer = data
        
        elif isinstance(result, str):
            answer = result
        
        # If still no answer, convert entire response to string
        if not answer:
            answer = str(result)
        
        return ChatResponse(
            answer=answer,
            error=None
        )
    
    except requests.exceptions.Timeout:
        error_msg = "Request timed out. The AI model took too long to respond."
        logger.error(error_msg)
        return ChatResponse(
            answer=None,
            error=error_msg
        )
    
    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {str(e)}"
        logger.error(error_msg)
        return ChatResponse(
            answer=None,
            error=error_msg
        )
    
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return ChatResponse(
            answer=None,
            error=error_msg
        )

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "chat_enabled": CHAT_ENABLED
    }