#!/bin/bash

# Create necessary directories
mkdir -p docs 

# Check if backend directory exists
if [ ! -d "backend" ]; then
    echo "Error: backend directory not found"
    exit 1
fi

echo "Starting Course Materials RAG System..."
echo "Web Interface will be available at: http://localhost:8000"
echo "API Documentation will be available at: http://localhost:8000/docs"
echo "Make sure you have set your ZHIPU_API_KEY in .env"
echo ""

# Change to backend directory and start the server
cd backend && uv run uvicorn app:app --reload --port 8000 --host 0.0.0.0