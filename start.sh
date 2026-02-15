#!/bin/bash

echo "Starting BSL.v59 Python Server for Termux..."

# Check for pynacl and try to install it with the fix if missing
if ! python3 -c "import nacl" &> /dev/null; then
    echo "Installing dependencies..."
    export SODIUM_INSTALL=system
    if ! pip install -r requirements.txt; then
        echo "Error: Failed to install dependencies."
        echo "Try running: pkg install libsodium libsodium-dev"
        echo "Then: export SODIUM_INSTALL=system && pip install pynacl"
        exit 1
    fi
fi

if [ ! -f "lobby_server.py" ]; then
    echo "Error: lobby_server.py not found!"
    exit 1
fi

python3 lobby_server.py
