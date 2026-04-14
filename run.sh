#!/bin/bash

# Define cleanup function
cleanup() {
    echo ""
    echo "Shutting down servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit 0
}

# Trap SIGINT (Ctrl+C) and call cleanup
trap cleanup SIGINT

echo "🚀 Starting Nexus Intelligence Pipeline..."

echo "==> Starting FastAPI Backend"
source venv/bin/activate
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "==> Starting Next.js Dashboard"
cd frontend
npm run dev -- -p 3000 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Everything is running!"
echo "➡️  Dashboard available at: http://localhost:3000"
echo "➡️  API available at: http://localhost:8000"
echo "Press Ctrl+C to stop both servers."

wait $BACKEND_PID $FRONTEND_PID
