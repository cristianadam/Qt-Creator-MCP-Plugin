#!/bin/bash

# Qt MCP Plugin - Build Script Wrapper
# Calls the cross-platform Python build script

echo "🔧 Qt MCP Plugin - Build Script"
echo "================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    echo "   Please install Python 3 and try again"
    exit 1
fi

# Run the Python build script
echo "🐍 Running cross-platform build script..."
python3 build.py

# Exit with the same code as the Python script
exit $?
