#!/bin/bash
# Quick launcher script for Bone Mineralization Simulator

echo "🦴 Bone Mineralization Integrated Model - Python Version"
echo "=========================================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8 or later."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip."
    exit 1
fi

echo "✅ Python and pip found."
echo ""

# Install/update dependencies
echo "📦 Installing/updating dependencies..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully."
else
    echo "❌ Failed to install dependencies."
    exit 1
fi

echo ""
echo "🚀 Launching Bone Mineralization Simulator..."
echo ""
echo "   Opening at: http://localhost:8501"
echo "   Press Ctrl+C to stop the server"
echo ""

# Run the single-page app
streamlit run app_single.py
