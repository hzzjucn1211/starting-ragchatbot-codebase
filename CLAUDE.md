# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development
- **Start the application**: `./run.sh` or `cd backend && uv run uvicorn app:app --reload --port 8000 --host 0.0.0.0`
- **Install dependencies**: `uv sync`
- **Access the application**: 
  - Web Interface: http://localhost:8000
  - API Documentation: http://localhost:8000/docs

### Environment Setup
- Requires `.env` file in root with `ZHIPU_API_KEY=your_zhipuai_api_key_here`
- Python 3.13+ and uv package manager required
- Embedding model stored locally in `./models/all-MiniLM-L6-v2/`

### Troubleshooting
- If "Failed to fetch" error occurs, ensure server is started from root directory with `./run.sh`
- Server must be accessible at `0.0.0.0:8000` for frontend to connect properly
- Check `.env` file contains valid ZHIPU_API_KEY

## Architecture

This is a RAG (Retrieval-Augmented Generation) system for querying course materials with the following architecture:

### Core Components
- **RAGSystem** (backend/rag_system.py:10): Main orchestrator coordinating all components and handling query flow
- **VectorStore** (backend/vector_store.py:34): ChromaDB-based vector storage with SentenceTransformers embeddings
- **AIGenerator** (backend/ai_generator.py:4): ZhipuAI GLM-4-Plus integration for response generation
- **DocumentProcessor** (backend/document_processor.py:6): Processes course documents with sentence-based chunking
- **SessionManager** (backend/session_manager.py:10): Manages conversation history with configurable limits
- **ToolManager/CourseSearchTool** (backend/search_tools.py:20,119): Function-calling tools for semantic search

### Data Models
- **Course** (backend/models.py:10): Contains title, instructor, lessons, and course_link
- **Lesson** (backend/models.py:4): Individual lessons with lesson_number, title, and lesson_link  
- **CourseChunk** (backend/models.py:17): Text chunks for vector storage with course/lesson metadata

### Application Flow & Data Processing
1. **Startup**: Documents processed from `/docs` folder into Course/Lesson objects
2. **Indexing**: Content chunked with sentence-boundary detection and stored in ChromaDB
3. **Query Processing**: 
   - Frontend sends query via REST API to FastAPI backend
   - RAGSystem uses ToolManager for semantic search through CourseSearchTool
   - ZhipuAI processes search results with function calling
   - Response generated with retrieved context and conversation history
4. **Session Management**: Conversation history maintained per session with configurable limits
5. **Vector Search**: Dual-collection approach for course metadata and content chunks

### Key Configuration (backend/config.py:9)
- **AI Model**: ZhipuAI GLM-4-Plus (not Anthropic Claude)
- **Embedding Model**: SentenceTransformers "all-MiniLM-L6-v2" (stored locally)
- **Chunking**: 800 characters with 100 character overlap, sentence-boundary aware
- **Vector Storage**: ChromaDB with persistent storage in `./chroma_db/`
- **Search Limits**: Max 5 results per query, Max 2 conversation messages in history
- **Collections**: Separate ChromaDB collections for course metadata and content chunks

### Frontend Architecture
- **Static Files**: HTML/CSS/JS served by FastAPI StaticFiles mount at root path
- **API Communication**: Frontend uses relative `/api` endpoints for cross-origin compatibility
- **Error Handling**: Enhanced JavaScript error logging and "Failed to fetch" debugging
- **Real-time Updates**: Async/await pattern for API calls with loading states
- **Session State**: Client-side session management with server-generated session IDs

### API Endpoints
- `POST /api/query` (backend/app.py:56): Main query processing with session management
- `GET /api/courses` (backend/app.py:79): Course statistics and metadata retrieval
- `GET /docs`: Interactive API documentation (FastAPI auto-generated)
- `GET /`: Static frontend files (index.html, script.js, style.css)

### Data Models (backend/models.py)
- **Course**: title, course_link, instructor, lessons[]
- **Lesson**: lesson_number, title, lesson_link
- **CourseChunk**: content, course_title, lesson_number, chunk_index
- **Message**: role (user/assistant), content
- **SearchResults**: documents[], metadata[], distances[], error handling