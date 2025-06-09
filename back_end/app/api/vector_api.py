from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import asyncio
import os

from services.vector_service import VectorService

class DocumentInput(BaseModel):
    text: str

class DocumentsInput(BaseModel):
    texts: List[str]

class SearchInput(BaseModel):
    query: str
    n_results: Optional[int] = 10

class DocumentOutput(BaseModel):
    id: str
    text: str

class SearchResult(BaseModel):
    id: str
    text: str
    score: float

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]


router = APIRouter(prefix="/vector", tags=["Vector Database"])

def get_db() -> VectorService:
    return VectorService(collection_name="documents")


@router.post("/documents", response_model= Dict[str, str])
async def add_document(document: DocumentInput, db: VectorService = Depends(get_db)):
    doc_id = await db.add(document.text)
    return {"id": doc_id}

@router.post("/documents/batch", response_model= Dict[str, str])
async def add_documents(documents: DocumentsInput, db: VectorService = Depends(get_db)):
    for document in documents.texts:
        await db.add(document)
    return {"status": "success"}

@router.post("/search", response_model= SearchResponse)
async def search(search: SearchInput, db: VectorService = Depends(get_db)):
    results = await db.search(search.query, search.n_results)
    return results

@router.get('/documents/{doc_id}', response_model=DocumentOutput)
def get_document(doc_id:str, db:VectorService = Depends(get_db)):
    document = db.get_document(doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete('/documents/{doc_id}', response_model= Dict[str, bool])
def delete_document(doc_id:str, db:VectorService = Depends(get_db)):
    success = db.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"success": success}

@router.put("/documents/{doc_id}", response_model= Dict[str, bool])
def update_document(doc_id: str, document: DocumentInput, db: VectorService = Depends(get_db)):
    success = db.update_document(doc_id, document.text)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return {"success": success}

