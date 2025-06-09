from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


from .services.mistral_service import MistralService
from .services.vector_service import VectorService, Encoder
from .services.message_builder import MessageBuilder

app = FastAPI(title="Documentation Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role:str
    content:str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    useRag: Optional[bool] = True

class ChatResponse(BaseModel):
    response: str

mistral_service = MistralService()
vector_service = VectorService(collection_name = "mistral_docs", 
                               persist_directory="data/mistral_doc")
message_builder = MessageBuilder()
persist_directory = "data/doc"

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.get("/api/search")
async def search(query: str, n_results: int = 5):
    results = await vector_service.search(query, n_results)
    return results 

@app.post("/api/chat", response_model = ChatResponse)
async def chat_endpoint(request: ChatRequest):
    history_and_query = request.messages
    query = history_and_query[-1].content
    history = history_and_query[:-1]

    retrieving_results = await search(query, n_results=5) if request.useRag else {"result": []}
    
    message_builder.set_rag(request.useRag)
    
    messages = [
        message_builder.build_system_message(),
        message_builder.build_user_message(query, retrieving_results, history)
    ]
    response = await mistral_service.generate_response(messages)
    return {"response": response}


@app.post("/api/chat/complete", response_model=ChatResponse)
async def chat_complete(request: ChatRequest):
    return await chat_endpoint(request)


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
