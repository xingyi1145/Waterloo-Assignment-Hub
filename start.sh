#!/bin/bash
# Quick start script for Waterloo CS Assignment Hub

echo "🚀 Starting Waterloo CS Assignment Hub..."
echo ""

# Check if already running
if pgrep -f "uvicorn.*main:app" > /dev/null; then
    echo "⚠️  Backend already running"
else
    echo "📡 Starting backend server..."
    cd /home/xingy/cs137-web-app
    source venv/bin/activate
    uvicorn src.backend.main:app --reload --host 127.0.0.1 --port 8000 > backend.log 2>&1 &
    sleep 2
    echo "✅ Backend started on http://localhost:8000"
fi

if pgrep -f "vite" > /dev/null; then
    echo "⚠️  Frontend already running"
else
    echo "🎨 Starting frontend server..."
    cd /home/xingy/cs137-web-app/src/frontend
    npm run dev > frontend.log 2>&1 &
    sleep 3
    echo "✅ Frontend started on http://localhost:5173"
fi

echo ""
echo "============================================"
echo "✨ Application ready!"
echo "============================================"
echo ""
echo "📖 API Docs:    http://localhost:8000/docs"
echo "🌐 Frontend:    http://localhost:5173"
echo ""
echo "To stop servers:"
echo "  pkill -f uvicorn"
echo "  pkill -f vite"
echo ""
echo "To view logs:"
echo "  tail -f /home/xingy/cs137-web-app/backend.log"
echo "  tail -f /home/xingy/cs137-web-app/src/frontend/frontend.log"
echo ""
