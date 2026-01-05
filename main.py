from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI app instance

app = FastAPI()

class SumRequest(BaseModel):
    a: float
    b: float

class SumResponse(BaseModel):
    result: float

@app.post("/sum", response_model=SumResponse)
async def sum_numbers(request: SumRequest):
    return SumResponse(result=request.a + request.b)
