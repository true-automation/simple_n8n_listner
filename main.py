from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from bytez import Bytez
import os

app = FastAPI(
    title="Math & Chat API",
    description="API for performing math operations and chat interactions",
    version="2.0.0"
)

# Initialize Bytez SDK
BYTEZ_API_KEY = os.getenv("BYTEZ_API_KEY", "03ba600d1e40ba3aaa1b44538b3543a0")
sdk = Bytez(BYTEZ_API_KEY)
model = sdk.model("zai-org/GLM-4.6V-Flash")

class Numbers(BaseModel):
    x: float
    y: float

class Result(BaseModel):
    sum: float
    mult: float

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: Optional[str]
    error: Optional[str]

@app.get("/")
async def root():
    return {
        "message": "Math & Chat API",
        "endpoints": {
            "/calculate": "POST - Calculate sum and multiplication of two numbers",
            "/chat": "POST - Send a question and get AI response"
        }
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
        request: Object containing the question
    
    Returns:
        JSON object with answer and error fields
    """
    try:
        # Send input to model
        output, error = model.run([
            {
                "role": "user",
                "content": request.question
            }
        ])
        
        return ChatResponse(
            answer=output if not error else None,
            error=error if error else None
        )
    
    except Exception as e:
        return ChatResponse(
            answer=None,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}