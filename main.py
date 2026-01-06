from fastapi import FastAPI
from pydantic import BaseModel
import os
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str | None = None
    error: str | None = None

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        response = model.generate_content(req.question)
        return ChatResponse(answer=response.text)
    except Exception as e:
        return ChatResponse(error=str(e))
