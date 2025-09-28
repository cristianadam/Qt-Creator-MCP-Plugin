#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Qt MCP Plugin - Qt Installation Configuration
Cross-platform configuration for Qt installation paths.

Users should modify this file if their Qt installation is not in the standard locations.
"""

import os
import platform
import socket
import subprocess
import re

# =============================================================================
# CUSTOM QT INSTALLATION PATHS - MODIFY THESE FOR YOUR SYSTEM
# =============================================================================
# 
# If your Qt installation is not in the standard locations, modify the paths 
# below to match your system. These paths will be used when the hostname 
# contains "pandora" (indicating a custom installation).
#
# For other systems, you can modify the hostname detection logic below or
# add your own hostname to the custom_path condition.
#
# =============================================================================

    # Custom Qt installation base paths for different platforms
CUSTOM_QT_PATHS = {
    "windows": "C:/Users/davec/Developer/Qt",  # Windows custom Qt path
    "darwin": "/Users/davec/Developer/Qt",     # macOS custom Qt path  
    "linux": "/opt"                           # Linux custom Qt path
}

# Custom hostname detection - add your hostname here if needed
CUSTOM_HOSTNAMES = ["pandora"]  # List of hostnames that should use custom paths

# Note: No fallback version - Qt Creator installation is required

# =============================================================================
# END OF CUSTOM CONFIGURATION
# =============================================================================

# Constants to eliminate duplicate strings
QT_CREATOR_PROCESSES = {
    "windows": "qtcreator.exe",
    "darwin": "Qt Creator", 
    "linux": "qtcreator"
}

QT_CREATOR_BINARIES = {
    "windows": "qtcreator.exe",
    "darwin": "Qt Creator",
    "linux": "qtcreator"
}

KILL_COMMANDS = {
    "windows": ["taskkill", "/F", "/IM", "qtcreator.exe"],
    "darwin": ["pkill", "-f", "Qt Creator"],
    "linux": ["pkill", "-f", "qtcreator"]
}

TEST_COMMANDS = {
    "windows": ["telnet", "localhost", "3001"],
    "darwin": ["nc", "-w", "3", "localhost", "3001"],
    "linux": ["nc", "-w", "3", "localhost", "3001"]
}

PLUGIN_EXTENSIONS = {
    "windows": ".dll",
    "darwin": ".dylib",
    "linux": ".so"
}

PLUGIN_DIRECTORIES = {
    "windows": "plugins",
    "darwin": "PlugIns/qtcreator",
    "linux": "plugins"
}

# Path construction helpers
def build_qt_creator_path(base_path, system):
    """Build Qt Creator path from base path"""
    if system == "windows":
        return "{}/Tools/QtCreator/lib".format(base_path)
    elif system == "darwin":
        return "{}/Qt Creator.app/Contents/Resources".format(base_path)
    else:  # linux
        return "{}/qtcreator".format(base_path)

def build_qt_creator_bin_path(base_path, system):
    """Build Qt Creator binary path from base path"""
    if system == "windows":
        return "{}/Tools/QtCreator/bin/qtcreator.exe".format(base_path)
    elif system == "darwin":
        return "{}/Qt Creator.app/Contents/MacOS/Qt Creator".format(base_path)
    else:  # linux
        return "{}/qtcreator/bin/qtcreator".format(base_path)

def discover_qt_version(qt_creator_bin):
    """
    Discover the Qt version that Qt Creator was built with
    
    Args:
        qt_creator_bin (str): Path to Qt Creator binary
        
    Returns:
        str: Qt version (e.g., "6.9.2") or None if discovery fails
    """
    try:
        system = platform.system().lower()
        
        if system == "windows":
            # Use qtdiag.exe on Windows
            qtdiag_path = qt_creator_bin.replace("qtcreator.exe", "qtdiag.exe")
        elif system == "darwin":
            # On macOS, qtdiag is in the same MacOS directory as Qt Creator
            import os.path as osp
            qtdiag_path = osp.join(osp.dirname(qt_creator_bin), "qtdiag")
        else:
            # On Linux, qtdiag is in the same directory as qtcreator
            qtdiag_path = qt_creator_bin.replace("qtcreator", "qtdiag")
        
        # Run qtdiag to get Qt version information
        result = subprocess.run([qtdiag_path], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Parse the output to find Qt version
            for line in result.stdout.split('\n'):
                if 'Qt' in line and ('x86_64' in line or 'arm64' in line or 'gcc' in line or 'Apple LLVM' in line):
                    # Extract version from line like "Qt 6.9.2 (arm64-little_endian-lp64..."
                    match = re.search(r'Qt (\d+\.\d+\.\d+)', line)
                    if match:
                        version = match.group(1)
                        return version
        
        return None
        
    except Exception as e:
        return None

def get_qt_config():
    """
    Get comprehensive Qt installation configuration including version discovery and build-specific fields.
    
    Returns:
        dict: Complete configuration for build scripts
        
    Raises:
        RuntimeError: If Qt Creator is not found or Qt version cannot be discovered
    """
    system = platform.system().lower()
    hostname = socket.gethostname()
    
    # Check if current hostname should use custom paths
    custom_path = any(custom_hostname.lower() in hostname.lower() for custom_hostname in CUSTOM_HOSTNAMES)
    
    # Standard installation paths
    standard_paths = {
        "windows": "C:/Qt",
        "darwin": "/Applications", 
        "linux": "/opt"
    }
    
    # Choose base path based on hostname detection
    if custom_path:
        base_path = CUSTOM_QT_PATHS[system]
    else:
        base_path = standard_paths[system]
    
    # Build paths using helper functions
    qt_creator_path = build_qt_creator_path(base_path, system)
    qt_creator_bin = build_qt_creator_bin_path(base_path, system)
    
    # CRITICAL: Check if Qt Creator binary exists before proceeding
    if not os.path.exists(qt_creator_bin):
        print("=" * 80)
        print("❌ ERROR: Qt Creator not found!")
        print("=" * 80)
        print(f"Expected Qt Creator binary at: {qt_creator_bin}")
        print(f"Current hostname: {hostname}")
        print(f"Using {'custom' if custom_path else 'standard'} paths")
        print(f"Base path: {base_path}")
        print("")
        print("SOLUTION:")
        print("1. Install Qt Creator if not already installed")
        print("2. OR update the custom path in qt_config.py")
        print("")
        print("To use a custom path, edit qt_config.py and modify:")
        print("   CUSTOM_QT_PATHS = {")
        print(f'       "darwin": "/your/custom/qt/path",  # Update this line')
        print("       ...")
        print("   }")
        print("")
        print("Then add your hostname to CUSTOM_HOSTNAMES:")
        print("   CUSTOM_HOSTNAMES = [\"your_hostname\"]")
        print("=" * 80)
        raise RuntimeError(f"Qt Creator binary not found at: {qt_creator_bin}")
    
    # Check if Qt Creator lib directory exists
    if not os.path.exists(qt_creator_path):
        print("=" * 80)
        print("❌ ERROR: Qt Creator lib directory not found!")
        print("=" * 80)
        print(f"Expected Qt Creator lib directory at: {qt_creator_path}")
        print(f"Qt Creator binary found at: {qt_creator_bin}")
        print("")
        print("This usually means Qt Creator is not properly installed or")
        print("the installation path is incorrect.")
        print("")
        print("SOLUTION:")
        print("1. Reinstall Qt Creator")
        print("2. OR update the custom path in qt_config.py (see above)")
        print("=" * 80)
        raise RuntimeError(f"Qt Creator lib directory not found at: {qt_creator_path}")
    
    # Discover Qt version dynamically - this is required
    qt_version = discover_qt_version(qt_creator_bin)
    if qt_version is None:
        print("=" * 80)
        print("❌ ERROR: Could not discover Qt version!")
        print("=" * 80)
        print(f"Qt Creator binary found at: {qt_creator_bin}")
        print(f"Qt Creator lib directory found at: {qt_creator_path}")
        print("")
        print("This usually means:")
        print("1. Qt Creator is not properly installed")
        print("2. The qtdiag tool is missing or broken")
        print("3. The installation is corrupted")
        print("")
        print("SOLUTION:")
        print("1. Reinstall Qt Creator")
        print("2. OR update the custom path in qt_config.py (see above)")
        print("=" * 80)
        raise RuntimeError("Could not discover Qt version from Qt Creator installation. Please ensure Qt Creator is properly installed and accessible.")
    
    # Platform names
    platform_names = {
        "windows": "Windows",
        "darwin": "macOS", 
        "linux": "Linux"
    }
    
    # Build base configuration
    config = {
        "name": platform_names[system],
        "qt_path": base_path,
        "qt_creator_path": qt_creator_path,
        "qt_creator_bin": qt_creator_bin,
        "process_name": QT_CREATOR_PROCESSES[system],
        "kill_command": KILL_COMMANDS[system],
        "test_command": TEST_COMMANDS[system],
        "plugin_extension": PLUGIN_EXTENSIONS[system],
        "plugin_directory": PLUGIN_DIRECTORIES[system]
    }
    
    # Add build-specific fields
    if system == "darwin":
        config["qt_creator_app"] = qt_creator_path.replace("/Contents/Resources", "")
        config["qt6_path"] = base_path + "/{}/macos".format(qt_version)
    elif system == "windows":
        config["qt_creator_app"] = None  # Windows doesn't use app bundles
        config["qt6_path"] = base_path + "/Qt/{}/msvc2022_64".format(qt_version)
    else:  # linux
        config["qt_creator_app"] = None  # Linux doesn't use app bundles
        config["qt6_path"] = base_path + "/{}/gcc_64".format(qt_version)
    
    return config


def get_qt_version_path():
    """
    Get the Qt version path (e.g., 6.9.2/msvc2022_64 for Windows)
    
    Returns:
        str: Qt version path for the current platform
        
    Raises:
        RuntimeError: If Qt version cannot be discovered
    """
    system = platform.system().lower()
    config = get_qt_config()
    
    # Discover Qt version dynamically - this is required
    qt_version = discover_qt_version(config["qt_creator_bin"])
    if qt_version is None:
        raise RuntimeError("Could not discover Qt version from Qt Creator installation. Please ensure Qt Creator is properly installed.")
    
    # Platform-specific compiler paths
    compiler_paths = {
        "windows": "msvc2022_64",
        "darwin": "clang_64", 
        "linux": "gcc_64"
    }
    
    return "{}/{}".format(qt_version, compiler_paths[system])

def get_cmake_prefix_path():
    """
    Get the CMake prefix path for Qt Creator
    
    Returns:
        str: CMake prefix path
    """
    config = get_qt_config()
    return config["qt_creator_path"]

def get_plugin_install_path():
    """
    Get the plugin installation path
    
    Returns:
        str: Path where plugins should be installed
    """
    config = get_qt_config()
    return os.path.join(config["qt_creator_path"], config["plugin_directory"])

def get_plugin_binary_name():
    """
    Get the plugin binary name for the current platform
    
    Returns:
        str: Plugin binary name
    """
    system = platform.system().lower()
    
    # Platform-specific plugin binary names
    plugin_names = {
        "windows": "Qt_MCP_Plugin.dll",
        "darwin": "libQt_MCP_Plugin.1.dylib",
        "linux": "libQt_MCP_Plugin.so.1"
    }
    
    return plugin_names[system]

def get_windeployqt_path():
    """
    Get the windeployqt executable path for Windows
    
    Returns:
        str: Path to windeployqt.exe
        
    Raises:
        RuntimeError: If Qt version cannot be discovered or not on Windows
    """
    system = platform.system().lower()
    if system != "windows":
        raise RuntimeError("windeployqt is only available on Windows")
    
    config = get_qt_config()
    
    # Discover Qt version dynamically - this is required
    qt_version = discover_qt_version(config["qt_creator_bin"])
    if qt_version is None:
        raise RuntimeError("Could not discover Qt version from Qt Creator installation. Please ensure Qt Creator is properly installed.")
    
    # Build windeployqt path
    return "{}/Qt/{}/msvc2022_64/bin/windeployqt.exe".format(config["qt_path"], qt_version)

def get_cmake_paths():
    """
    Get possible CMake installation paths for the current platform
    
    Returns:
        list: List of possible CMake paths to search
    """
    system = platform.system().lower()
    config = get_qt_config()
    
    if system == "windows":
        # Windows CMake paths - use Qt installation and common system paths
        cmake_paths = [
            "{}/Tools/CMake_64/bin".format(config["qt_path"]),
            "C:/Program Files/CMake/bin",
            "C:/Program Files (x86)/CMake/bin"
        ]
    elif system == "darwin":
        # macOS CMake paths
        cmake_paths = [
            "/usr/local/bin",
            "/opt/homebrew/bin", 
            "/usr/bin"
        ]
    else:  # linux
        # Linux CMake paths
        cmake_paths = [
            "/usr/bin",
            "/usr/local/bin",
            "/opt/cmake/bin"
        ]
    
    return cmake_paths

def validate_qt_installation():
    """
    Validate that Qt Creator is installed in the expected location
    
    Returns:
        tuple: (is_valid, error_message)
    """
    config = get_qt_config()
    
    # Check if Qt Creator binary exists
    if not os.path.exists(config["qt_creator_bin"]):
        return False, f"Qt Creator binary not found at: {config['qt_creator_bin']}"
    
    # Check if Qt Creator lib directory exists
    if not os.path.exists(config["qt_creator_path"]):
        return False, f"Qt Creator lib directory not found at: {config['qt_creator_path']}"
    
    return True, "Qt installation validated successfully"

if __name__ == "__main__":
    # Test the configuration
    config = get_qt_config()
    print("Qt MCP Plugin - Configuration Test")
    print("=" * 40)
    print(f"Platform: {config['name']}")
    print(f"Qt Creator Binary: {config['qt_creator_bin']}")
    print(f"Qt Creator Path: {config['qt_creator_path']}")
    print(f"Plugin Extension: {config['plugin_extension']}")
    print(f"Plugin Directory: {config['plugin_directory']}")
    print(f"CMake Prefix Path: {get_cmake_prefix_path()}")
    print(f"Plugin Install Path: {get_plugin_install_path()}")
    print(f"Plugin Binary Name: {get_plugin_binary_name()}")
    
    # Test version discovery
    qt_version = discover_qt_version(config["qt_creator_bin"])
    if qt_version:
        print(f"Discovered Qt Version: {qt_version}")
    else:
        print("Qt Version: Could not discover (will use fallback)")
    
    # Validate installation
    is_valid, message = validate_qt_installation()
    if is_valid:
        print(f"\n[OK] {message}")
    else:
        print(f"\n[ERROR] {message}")
        print("\nTo fix this, modify the paths in qt_config.py")
