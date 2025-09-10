from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
import config
from database import ChromaDBManager
import tempfile
import os


class RAGSystem:
    def __init__(self):
        self.db_manager = ChromaDBManager()

        # Initialize Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=config.GEMINI_MODEL,
            google_api_key=config.GEMINI_API_KEY,
            temperature=0.7,
            max_tokens=800,
            top_p=0.9,
            top_k=40
        )

        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_template("""
You are a helpful AI assistant that answers questions based on the provided document context. 
Use the context below to answer the user's question accurately and comprehensively. 
If the context doesn't contain enough information to answer the question, say so politely.
Always be concise, helpful, and cite relevant information from the context.

Context from document:
{context}

Question: {question}

Please provide a helpful answer based on the context above.
""")

    def add_documents(self, texts: List[str], metadatas: List[Dict] = None) -> bool:
        """Add documents to the knowledge base"""
        return self.db_manager.add_documents(texts, metadatas)

    def retrieve_context(self, query: str, k: int = 3) -> List[str]:
        """Retrieve relevant context from the knowledge base"""
        results = self.db_manager.similarity_search(query, k=k)
        return [doc.page_content for doc in results]

    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate response using LangChain with retrieved context"""
        try:
            # Format context
            context_str = "\n\n".join([f"Context {i + 1}: {ctx}" for i, ctx in enumerate(context)])

            # Create messages for the chat model
            messages = self.prompt_template.format_messages(
                context=context_str,
                question=query
            )

            # Get response from LLM
            response = self.llm.invoke(messages)
            return response.content

        except Exception as e:
            print(f"Error generating response: {e}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"

    def chat(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Main RAG chat function using LangChain"""
        try:
            # Check if knowledge base has content
            kb_info = self.get_knowledge_base_info()
            if not kb_info or kb_info.get("count", 0) == 0:
                return {
                    "query": query,
                    "response": "No PDF document has been uploaded yet. Please upload a PDF file first to start chatting.",
                    "context_used": 0,
                    "context": []
                }

            # Retrieve relevant context
            context = self.retrieve_context(query, k=k)

            # Generate response using LangChain
            response = self.generate_response(query, context)

            return {
                "query": query,
                "response": response,
                "context_used": len(context),
                "context": context[:2] if context else []  # Return first 2 contexts for transparency
            }

        except Exception as e:
            return {
                "query": query,
                "response": f"Error processing query: {str(e)}",
                "context_used": 0,
                "context": []
            }

    def chat_with_sources(self, query: str, k: int = 3) -> Dict[str, Any]:
        """Chat function that returns sources information"""
        try:
            # Check if knowledge base has content
            kb_info = self.get_knowledge_base_info()
            if not kb_info or kb_info.get("count", 0) == 0:
                return {
                    "query": query,
                    "response": "No PDF document has been uploaded yet. Please upload a PDF file first to start chatting.",
                    "context_used": 0,
                    "context": [],
                    "sources": []
                }

            # Retrieve relevant documents with metadata
            results = self.db_manager.similarity_search(query, k=k)
            
            # Extract context and sources
            context = [doc.page_content for doc in results]
            sources = []
            
            for doc in results:
                if hasattr(doc, 'metadata') and doc.metadata:
                    sources.append({
                        "source": doc.metadata.get("source", "Unknown"),
                        "page": doc.metadata.get("page", 0),
                        "filename": doc.metadata.get("filename", "Unknown")
                    })

            # Generate response using LangChain
            response = self.generate_response(query, context)

            return {
                "query": query,
                "response": response,
                "context_used": len(context),
                "context": context[:2] if context else [],  # Return first 2 contexts for transparency
                "sources": sources
            }

        except Exception as e:
            return {
                "query": query,
                "response": f"Error processing query: {str(e)}",
                "context_used": 0,
                "context": [],
                "sources": []
            }

    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """Get information about the knowledge base"""
        return self.db_manager.get_collection_info()

    def clear_knowledge_base(self) -> bool:
        """Clear the knowledge base"""
        result = self.db_manager.delete_collection()
        if result:
            # Reinitialize the database manager to ensure clean state
            from database import ChromaDBManager
            self.db_manager = ChromaDBManager()
        return result

    def load_pdf_from_file(self, pdf_path: str) -> Dict[str, Any]:
        """Load PDF from file path"""
        try:
            if not os.path.exists(pdf_path):
                return {
                    "success": False,
                    "message": f"File not found: {pdf_path}",
                    "filename": os.path.basename(pdf_path),
                    "pages_processed": 0
                }

            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # Extract text from documents
            texts = [doc.page_content for doc in documents]
            
            # Add metadata
            metadatas = [{
                "source": os.path.basename(pdf_path),
                "page": i + 1,
                "filename": os.path.basename(pdf_path)
            } for i in range(len(texts))]
            
            # Add to knowledge base
            success = self.add_documents(texts, metadatas)
            
            return {
                "success": success,
                "message": f"Successfully processed {len(texts)} pages" if success else "Failed to process PDF",
                "filename": os.path.basename(pdf_path),
                "pages_processed": len(texts),
                "chunks_created": len(texts)
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing PDF: {str(e)}",
                "filename": pdf_path,
                "pages_processed": 0
            }

    def load_pdf_from_bytes(self, pdf_content: bytes, filename: str) -> Dict[str, Any]:
        """Load PDF from bytes content"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(pdf_content)
                temp_path = temp_file.name
            
            try:
                # Use the file path method
                result = self.load_pdf_from_file(temp_path)
                # Update filename in result
                result["filename"] = filename
                return result
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing PDF: {str(e)}",
                "filename": filename,
                "pages_processed": 0
            }

    def get_document_summary(self) -> str:
        """Get summary of loaded documents"""
        try:
            kb_info = self.get_knowledge_base_info()
            if kb_info.get("count", 0) == 0:
                return "No documents loaded"
            
            # Get some sample documents for summary
            sample_docs = self.db_manager.similarity_search("summary", k=3)
            
            if not sample_docs:
                return f"Knowledge base contains {kb_info['count']} document chunks"
            
            # Generate summary using LLM
            context = "\n\n".join([doc.page_content[:200] + "..." for doc in sample_docs])
            
            summary_prompt = ChatPromptTemplate.from_template("""
Based on the following document excerpts, provide a brief summary of the content:

{context}

Summary:""")
            
            messages = summary_prompt.format_messages(context=context)
            response = self.llm.invoke(messages)
            
            return f"Documents: {kb_info['count']} chunks\nSummary: {response.content}"
            
        except Exception as e:
            return f"Error generating summary: {str(e)}"