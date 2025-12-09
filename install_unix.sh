#!/bin/bash

echo "========================================"
echo "GasClip Certificates Generator"
echo "Linux/Mac Installation Script"
echo "========================================"
echo ""

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

python3 --version
echo ""

echo "Installing required packages..."
echo ""

pip3 install PyPDF2==3.0.1
pip3 install reportlab==4.0.7
pip3 install Pillow==10.1.0

echo ""
echo "========================================"
echo "Installation complete!"
echo "========================================"
echo ""
echo "To run the application: ./run_app.sh"
echo "Or run: python3 app.py"
echo ""
