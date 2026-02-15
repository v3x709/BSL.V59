#!/bin/bash

echo "Starting BSL.v59 Python Server for Termux..."

# Check for pysodium
if ! python3 -c "import pysodium" &> /dev/null; then
    echo "Installing dependencies..."
    if ! pip install -r requirements.txt; then
        echo "Error: Failed to install dependencies."
        echo "Try running: pkg install libsodium"
        exit 1
    fi
fi

if [ ! -f "lobby_server.py" ]; then
    echo "Error: lobby_server.py not found!"
    exit 1
fi

python3 lobby_server.py
