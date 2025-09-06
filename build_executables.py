"""
Create standalone executables that don't require Python installation
"""

import subprocess
import sys
import os

def build_executables():
    """Build standalone executables for different platforms"""
    
    print("🏗️  Building FixIt standalone executables...")
    
    # Install PyInstaller if not available
    try:
        import PyInstaller
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Common PyInstaller options
    base_cmd = [
        "pyinstaller",
        "--onefile",
        "--clean",
        "--noconfirm"
    ]
    
    # Platform-specific builds
    if sys.platform == "win32":
        # Windows executable
        cmd = base_cmd + [
            "--name", "fixit",
            "--add-data", "registry;registry",
            "--add-data", "src;src",
            "fixit.py"
        ]
        print("🪟 Building Windows executable...")
        subprocess.run(cmd)
        
    elif sys.platform == "darwin":
        # macOS executable
        cmd = base_cmd + [
            "--name", "fixit-macos",
            "--add-data", "registry:registry",
            "--add-data", "src:src", 
            "fixit.py"
        ]
        print("🍎 Building macOS executable...")
        subprocess.run(cmd)
        
    else:
        # Linux executable
        cmd = base_cmd + [
            "--name", "fixit-linux",
            "--add-data", "registry:registry",
            "--add-data", "src:src",
            "fixit.py"
        ]
        print("🐧 Building Linux executable...")
        subprocess.run(cmd)
    
    print("✅ Build complete! Executables are in the dist/ folder")
    print("Users can download and run them directly without installing Python")

if __name__ == "__main__":
    build_executables()
