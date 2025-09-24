@echo off
REM Launch Qt Creator with MCP Plugin
REM This script ensures the MCP Plugin is loaded when Qt Creator starts

echo 🚀 Launching Qt Creator with MCP Plugin...
echo 📍 Plugin path: %LOCALAPPDATA%\QtProject\qtcreator\plugins

REM Kill any existing Qt Creator instances
echo 🛑 Stopping any existing Qt Creator instances...
taskkill /F /IM "Qt Creator.exe" 2>NUL || echo No Qt Creator instances to kill

REM CRITICAL: Always clean up previous plugin versions to avoid conflicts
echo 🧹 Cleaning up previous plugin versions...
cmake --build . --target CleanOldPlugins 2>NUL || echo ⚠️  CMake clean failed, manually cleaning...

REM Build and install the latest plugin
echo 🔨 Building and installing latest plugin...
cmake --build . && cmake --build . --target InstallPlugin

REM Wait a moment for processes to terminate
timeout /t 2 /nobreak >NUL

REM Launch Qt Creator with plugin path
echo ▶️ Starting Qt Creator...
start "" "C:\Qt\Qt Creator\6.9.2\msvc2022_64\bin\Qt Creator.exe" -pluginpath "%LOCALAPPDATA%\QtProject\qtcreator\plugins" %*

echo ✅ Qt Creator launched with MCP Plugin v1.31.0
echo 🔌 MCP Server will be available on port 3001
echo 💡 Use Tools ^> MCP Plugin ^> About MCP Plugin to verify it's loaded