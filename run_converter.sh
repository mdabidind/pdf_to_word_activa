#!/bin/bash

echo "Starting PDF to Word Converter..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed."
    echo "Please install Python 3.7 or higher from https://www.python.org/downloads/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "Installing required dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Run the application
echo "Starting application..."
python3 run.py "$@"

read -p "Press Enter to exit..."