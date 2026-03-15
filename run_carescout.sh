#!/bin/bash

echo "Checking for existing processes..."

if lsof -ti :5000 > /dev/null 2>&1; then
    echo "  Port 5000 in use. Killing old backend process..."
    lsof -ti :5000 | xargs kill -9 2>/dev/null
    echo "  Port 5000 cleared"
fi

if lsof -ti :3000 > /dev/null 2>&1; then
    echo "  Port 3000 in use. Killing old frontend process..."
    lsof -ti :3000 | xargs kill -9 2>/dev/null
    echo "  Port 3000 cleared"
fi

pkill -f backend_flask.py 2>/dev/null && echo "  Cleaned up backend processes"

pkill -f "react-scripts/scripts/start.js" 2>/dev/null && echo "  Cleaned up React processes"

sleep 1
echo ""

pip3 show flask-cors >/dev/null 2>&1 || pip3 install flask-cors

echo "Starting backend..."
python3 backend_flask.py &
BACKEND_PID=$!

sleep 2

if [[ -d "frontend" ]]; then
    cd frontend || { echo "Failed to enter frontend directory"; exit 1; }
    
    # Install npm dependencies if needed
    if [[ ! -d "node_modules" ]]; then
        echo "Installing npm dependencies..."
        npm install
    fi
else
    echo "Frontend directory not found inside $PROJECT_DIR"
    exit 1
fi

echo "Starting frontend..."
PORT=3000 npm start &
FRONTEND_PID=$!

sleep 2

echo ""
echo "Backend and frontend are now running!"
echo "   Backend PID: $BACKEND_PID (http://localhost:5000)"
echo "   Frontend PID: $FRONTEND_PID (http://localhost:3000)"
echo ""
echo "Use 'jobs' to see them"
echo "Press Ctrl+C or run './stop.sh' to stop both servers"
echo ""

trap "echo ''; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

wait
