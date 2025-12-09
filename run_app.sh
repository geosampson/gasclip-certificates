#!/bin/bash

echo "Starting GasClip Certificates Generator..."
python3 app.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start the application"
    echo "Make sure you have run ./install_unix.sh first"
    read -p "Press Enter to continue..."
fi
