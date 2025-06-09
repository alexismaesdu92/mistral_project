from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio

from services.mistral_service import MistralService
router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.1
    max_tokens: Optional[int] = 4000

class QueryRequest(BaseModel):
    query:str
    n_results: Optional[int] = 10
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    message: str

def get_chatbot() -> MistralService:
    return MistralService()

@router.post("/complete", response_model = ChatResponse)
async def chat_complete(
    request: ChatRequest,
    chatbot: MistralService = Depends(get_chatbot)
):
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        response = await chatbot.chat_complete_async(
            messages = messages,
            temperature = request.temperature,
            max_tokens = request.max_tokens
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Mistral API: {str(e)}")
    

