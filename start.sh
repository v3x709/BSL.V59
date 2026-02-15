#!/bin/bash
echo "Starting BSL.v59 Python Server for Termux..."
pip install -r requirements.txt
python3 lobby_server.py
