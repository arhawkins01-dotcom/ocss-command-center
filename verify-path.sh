#!/bin/bash
# Verify Main File Path
# This script checks if the main Streamlit app file exists at the correct location

echo "=========================================="
echo "OCSS Command Center - Path Verification"
echo "=========================================="
echo ""

# Check if we're in the repository root
if [ ! -d ".git" ]; then
    echo "❌ ERROR: Not in repository root directory"
    echo "   Please run this script from the repository root"
    exit 1
fi

echo "✓ Running from repository root"
echo ""

# Check for main file
MAIN_FILE="app/app.py"
echo "Checking for main file: $MAIN_FILE"

if [ -f "$MAIN_FILE" ]; then
    echo "✓ Main file found!"
    echo ""
    echo "File details:"
    ls -lh "$MAIN_FILE"
    echo ""
    
    # Check file size (should be around 69KB)
    FILE_SIZE=$(stat -f%z "$MAIN_FILE" 2>/dev/null || stat -c%s "$MAIN_FILE" 2>/dev/null)
    if [ $FILE_SIZE -gt 50000 ]; then
        echo "✓ File size looks correct (${FILE_SIZE} bytes)"
    else
        echo "⚠️  WARNING: File size seems small (${FILE_SIZE} bytes)"
        echo "   Expected around 69,000 bytes"
    fi
    echo ""
    
    # Check if it's a Python file
    if head -1 "$MAIN_FILE" | grep -q "python\|import"; then
        echo "✓ File appears to be a Python script"
    else
        echo "⚠️  WARNING: File may not be a valid Python script"
    fi
    echo ""
    
    echo "=========================================="
    echo "✅ VERIFICATION PASSED"
    echo "=========================================="
    echo ""
    echo "Main file path for Streamlit Cloud:"
    echo "  $MAIN_FILE"
    echo ""
    echo "You can now deploy to Streamlit Cloud!"
    exit 0
else
    echo "❌ Main file NOT found at: $MAIN_FILE"
    echo ""
    echo "Searching for app.py files..."
    find . -name "app.py" -type f | grep -v __pycache__
    echo ""
    echo "Please ensure the file exists at: $MAIN_FILE"
    exit 1
fi
