#!/bin/bash

# Claude Code API 启动脚本

PORT=${PORT:-8000}
HOST=${HOST:-127.0.0.1}

cd "$(dirname "$0")"

echo "Starting Claude Code API..."
echo "Host: $HOST"
echo "Port: $PORT"
echo ""

uvicorn app.main:app --host $HOST --port $PORT
