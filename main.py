from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Math Operations API")

class CalculationRequest(BaseModel):
    x: float
    y: float

class CalculationResponse(BaseModel):
    sum: float
    mult: float

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Math Operations API",
        "features": ["Addition", "Multiplication"],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/calculate", response_model=CalculationResponse)
async def calculate(request: CalculationRequest):
    return {
        "sum": request.x + request.y,
        "mult": request.x * request.y
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
