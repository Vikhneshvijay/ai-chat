#!/bin/bash
set -e

echo "Starting Ollama..."
ollama serve > /dev/null 2>&1 &
OLLAMA_PID=$!

echo "Waiting for Ollama to be ready..."
sleep 5

echo "Pulling gemma3:1b model..."
ollama pull gemma3:1b > /dev/null 2>&1

echo "Model ready!"
wait $OLLAMA_PID
