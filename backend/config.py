import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

@dataclass
class Config:
    """Configuration settings for the RAG system"""
    # ZhipuAI API settings
    ZHIPU_API_KEY: str = os.getenv("ZHIPU_API_KEY", "c3b8da47b8ca43c28952d4ae88b4a3a0.LEzxXL1cMCdwK13A")  # ZhipuAI API key
    ZHIPU_MODEL: str = "glm-4-plus"  # GLM-4.5 model name
    
    # Embedding model settings
    EMBEDDING_MODEL: str = "../models/all-MiniLM-L6-v2"
    
    # Document processing settings
    CHUNK_SIZE: int = 800       # Size of text chunks for vector storage
    CHUNK_OVERLAP: int = 100     # Characters to overlap between chunks
    MAX_RESULTS: int = 5         # Maximum search results to return
    MAX_HISTORY: int = 2         # Number of conversation messages to remember
    
    # Database paths
    CHROMA_PATH: str = "./chroma_db"  # ChromaDB storage location

config = Config()


