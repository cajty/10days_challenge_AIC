import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional
import config


class ChromaDBManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=config.CHROMA_DB_PATH,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Initialize embeddings with Gemini
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=config.GEMINI_API_KEY
        )

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

        # Initialize or get existing collection
        self.vectorstore = self._get_or_create_collection()

    def _get_or_create_collection(self):
        """Get existing collection or create new one"""
        try:
            # Try to get existing collection first
            try:
                existing_collection = self.client.get_collection(config.COLLECTION_NAME)
                print(f"Using existing collection: {config.COLLECTION_NAME}")
            except:
                # Collection doesn't exist, will be created by Chroma constructor
                print(f"Creating new collection: {config.COLLECTION_NAME}")
                pass
            
            return Chroma(
                client=self.client,
                collection_name=config.COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=config.CHROMA_DB_PATH
            )
        except Exception as e:
            print(f"Error initializing collection: {e}")
            # Try once more
            return Chroma(
                client=self.client,
                collection_name=config.COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=config.CHROMA_DB_PATH
            )

    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None):
        """Add documents to the vector store"""
        try:
            if not texts:
                print("No texts provided to add")
                return False

            # Split texts into chunks
            documents = []
            document_metadatas = []

            for i, text in enumerate(texts):
                if not text or not text.strip():
                    continue
                    
                chunks = self.text_splitter.split_text(text)
                documents.extend(chunks)

                # Add metadata for each chunk
                for chunk_idx, chunk in enumerate(chunks):
                    metadata = {
                        "document_id": i,
                        "chunk_id": chunk_idx,
                        "source": f"document_{i}"
                    }
                    if metadatas and i < len(metadatas):
                        metadata.update(metadatas[i])
                    document_metadatas.append(metadata)

            if not documents:
                print("No valid chunks created from provided texts")
                return False

            # Add to vector store
            self.vectorstore.add_texts(
                texts=documents,
                metadatas=document_metadatas
            )
            print(f"Added {len(documents)} chunks from {len(texts)} documents")
            return True
        except Exception as e:
            print(f"Error adding documents: {e}")
            return False

    def similarity_search(self, query: str, k: int = 3):
        """Search for similar documents"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []

    def similarity_search_with_score(self, query: str, k: int = 3):
        """Search for similar documents with similarity scores"""
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Error searching documents with score: {e}")
            return []

    def delete_collection(self):
        """Delete the collection"""
        try:
            self.client.delete_collection(config.COLLECTION_NAME)
            print(f"Collection '{config.COLLECTION_NAME}' deleted successfully")
            
            # Reinitialize the vectorstore after deletion
            self.vectorstore = self._get_or_create_collection()
            return True
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False

    def get_collection_info(self):
        """Get information about the collection"""
        try:
            collection = self.client.get_collection(config.COLLECTION_NAME)
            return {
                "name": collection.name,
                "count": collection.count(),
                "metadata": collection.metadata
            }
        except Exception as e:
            # Collection doesn't exist or other error - return empty info
            return {
                "name": config.COLLECTION_NAME,
                "count": 0,
                "metadata": {}
            }