from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from rag_service import RAGSystem
import config
import os

# Initialize FastAPI app
app = FastAPI(
    title="Simple RAG API with PDF",
    description="A simple RAG API using ChromaDB, Google Gemini, and PDF as knowledge base",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = RAGSystem()


# Pydantic models
class ChatRequest(BaseModel):
    query: str
    k: Optional[int] = 3


class ChatResponse(BaseModel):
    query: str
    response: str
    context_used: int
    context: List[str]
    sources: Optional[List[dict]] = []


class UploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    pages_processed: int
    chunks_created: Optional[int] = 0


# API Routes
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the RAG system using PDF knowledge base"""
    try:
        result = rag_system.chat_with_sources(request.query, request.k)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")


@app.post("/upload-pdf", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Upload a PDF file to create/update the knowledge base"""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        # Read file content
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")

        # Process PDF using RAG system
        result = rag_system.load_pdf_from_bytes(content, file.filename)

        if result["success"]:
            return UploadResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/upload-pdf-from-path", response_model=UploadResponse)
async def upload_pdf_from_path(pdf_path: str):
    """Upload a PDF file from local path (for development/testing)"""
    try:
        # Validate path
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail=f"File not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")

        result = rag_system.load_pdf_from_file(pdf_path)

        if result["success"]:
            return UploadResponse(**result)
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading PDF from path: {str(e)}")


@app.get("/")
async def root():
    """API root endpoint with basic information"""
    kb_info = rag_system.get_knowledge_base_info()
    return {
        "message": "Simple RAG API with PDF - Enhanced with PyPDFLoader",
        "version": "1.1.0",
        "model": config.GEMINI_MODEL,
        "knowledge_base": {
            "type": "PDF Documents",
            "documents_count": kb_info.get("count", 0)
        },
        "endpoints": [
            "POST /chat - Chat with the RAG system",
            "POST /upload-pdf - Upload a PDF to knowledge base",
            "POST /upload-pdf-from-path - Load PDF from local path",
            "GET /knowledge-base/info - Get knowledge base information",
            "GET /knowledge-base/summary - Get document summary",
            "DELETE /knowledge-base/clear - Clear knowledge base",
            "GET /ui - Chat UI interface",
            "GET /health - Health check"
        ]
    }


@app.get("/ui")
async def chat_ui():
    """Serve the chat UI"""
    try:
        return FileResponse("chat.html")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Chat UI not found")


@app.delete("/knowledge-base/clear")
async def clear_knowledge_base():
    """Clear the knowledge base"""
    try:
        success = rag_system.clear_knowledge_base()
        if success:
            return {"success": True, "message": "Knowledge base cleared successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to clear knowledge base")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing knowledge base: {str(e)}")


@app.get("/knowledge-base/info")
async def get_knowledge_base_info():
    """Get information about the PDF knowledge base"""
    try:
        info = rag_system.get_knowledge_base_info()
        return {"success": True, "info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting knowledge base info: {str(e)}")


@app.get("/knowledge-base/summary")
async def get_document_summary():
    """Get summary of loaded documents"""
    try:
        summary = rag_system.get_document_summary()
        return {"success": True, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting document summary: {str(e)}")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Simple RAG API with PDF",
        "model": config.GEMINI_MODEL,
        "knowledge_base": "PDF"
    }


if __name__ == "__main__":
    print(f"Server URL: http://{config.SERVER_HOST}:{config.SERVER_PORT}")
    print(f"API Documentation: http://{config.SERVER_HOST}:{config.SERVER_PORT}/docs")
    print(f"Chat UI: http://{config.SERVER_HOST}:{config.SERVER_PORT}/ui")
    print(f"AI Model: {config.GEMINI_MODEL}")
    print(f"Document Loader: PyPDFLoader (langchain_community)")
    print(f"Vector Store: ChromaDB")
    
    # Check if knowledge base has any documents
    kb_info = rag_system.get_knowledge_base_info()
    if kb_info.get("count", 0) > 0:
        print(f"Knowledge Base: {kb_info['count']} document chunks loaded")
    else:
        print("Knowledge Base: Empty - Upload a PDF to get started")
    
    print("\n" + "="*50 + "\n")

    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=True
    )