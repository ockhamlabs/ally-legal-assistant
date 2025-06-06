import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
app = FastAPI()

class ChatRequest(BaseModel):
    model: str
    messages: list

@app.post("/openai/chat")
async def chat(req: ChatRequest):
    try:
        response = openai.ChatCompletion.create(model=req.model, messages=req.messages)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
