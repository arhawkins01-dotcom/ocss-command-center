#!/bin/bash
# OCSS Command Center - Unix/Linux/Mac Launcher
# This script starts the OCSS Command Center application and opens it in your browser

echo "========================================"
echo "  OCSS Command Center - Starting..."
echo "========================================"
echo ""

# Get the script's directory and navigate to app folder
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR="$(dirname "$SCRIPT_DIR")/app"

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    echo "✓ Python found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    echo "✓ Python found: $(python --version)"
else
    echo "✗ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

# Navigate to app directory
cd "$APP_DIR" || exit 1
echo "✓ App directory: $APP_DIR"

# Check if dependencies are installed
echo ""
echo "Checking dependencies..."
if ! $PYTHON_CMD -c "import streamlit" &> /dev/null; then
    echo "Installing dependencies from requirements.txt..."
    $PYTHON_CMD -m pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Start the application
echo ""
echo "========================================"
echo "  Starting OCSS Command Center..."
echo "========================================"
echo ""
echo "The application will open in your browser at:"
echo "  http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

# Launch Streamlit
$PYTHON_CMD -m streamlit run app.py
