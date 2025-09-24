#!/bin/bash

# Launch Qt Creator with MCP Plugin
# This script ensures the MCP Plugin is loaded when Qt Creator starts

echo "🚀 Launching Qt Creator with MCP Plugin..."
echo "📍 Plugin path: /Users/davec/Library/Application Support/QtProject/qtcreator/plugins"

# Kill any existing Qt Creator instances and wait for them to fully exit
echo "🛑 Stopping any existing Qt Creator instances..."
pkill -f "Qt Creator" 2>/dev/null || true

# CRITICAL: Always clean up previous plugin versions to avoid conflicts
echo "🧹 Cleaning up previous plugin versions..."
cmake --build . --target CleanOldPlugins 2>/dev/null || echo "⚠️  CMake clean failed, manually cleaning..."

# Also clean any plugins that might be in the Qt Creator app bundle
echo "🧹 Cleaning Qt Creator app bundle..."
rm -f "/Users/davec/Developer/Qt/Qt Creator.app/Contents/PlugIns/qtcreator/libQt_MCP_Plugin.dylib" 2>/dev/null || true
rm -f "/Users/davec/Developer/Qt/Qt Creator.app/Contents/PlugIns/qtcreator/Qt_MCP_Plugin.json" 2>/dev/null || true

# Build and install the latest plugin
echo "🔨 Building and installing latest plugin..."
cmake --build . && cmake --build . --target InstallPlugin

# Wait a moment for processes to fully terminate
sleep 2

# Verify no Qt Creator processes are still running
if pgrep -f "Qt Creator" > /dev/null; then
    echo "⚠️  Force killing remaining Qt Creator processes..."
    pkill -9 -f "Qt Creator" 2>/dev/null || true
    sleep 1
fi

# Launch Qt Creator with plugin path
echo "▶️  Starting Qt Creator..."
"/Users/davec/Developer/Qt/Qt Creator.app/Contents/MacOS/Qt Creator" \
    -pluginpath "/Users/davec/Library/Application Support/QtProject/qtcreator/plugins" \
    "$@" &

echo "✅ Qt Creator launched with MCP Plugin v1.31.0"
echo "🔌 MCP Server will be available on port 3001"
echo "💡 Use Tools > MCP Plugin > About MCP Plugin to verify it's loaded"