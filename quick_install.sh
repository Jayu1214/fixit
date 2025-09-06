#!/bin/bash
# Quick install script for FixIt - Cross-platform Software Installer
# Usage: curl -sSL https://raw.githubusercontent.com/Jayu1214/fixit/main/install.sh | bash

set -e

echo "🚀 FixIt Installer - Cross-platform Software Installation Framework"
echo "=================================================================="

# Detect OS
FIXIT_OS=""
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    FIXIT_OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    FIXIT_OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    FIXIT_OS="windows"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "✓ Detected OS: $FIXIT_OS"

# Check for Python
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python is required but not installed."
    echo "Please install Python 3.8+ and try again:"
    echo "  Linux: sudo apt install python3 python3-pip"
    echo "  macOS: brew install python3"
    echo "  Windows: Download from https://python.org"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
echo "✓ Found Python $PYTHON_VERSION"

# Check Python version
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
    echo "❌ Python 3.8+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Create installation directory
INSTALL_DIR="$HOME/.local/share/fixit"
echo "📂 Installing to: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"

# Download FixIt
echo "📥 Downloading FixIt..."
# Download and install FixIt
DOWNLOAD_URL="https://github.com/Jayu1214/fixit/archive/main.zip"
TEMP_ZIP="/tmp/fixit-main.zip"

if command -v curl &> /dev/null; then
    curl -L "$DOWNLOAD_URL" -o "$TEMP_ZIP"
elif command -v wget &> /dev/null; then
    wget "$DOWNLOAD_URL" -O "$TEMP_ZIP"
else
    echo "❌ curl or wget is required to download FixIt"
    exit 1
fi

# Extract
echo "📦 Extracting FixIt..."
if command -v unzip &> /dev/null; then
    unzip -q "$TEMP_ZIP" -d "/tmp/"
    cp -r "/tmp/fixit-main/"* "$INSTALL_DIR/"
else
    echo "❌ unzip is required to extract FixIt"
    exit 1
fi

# Install dependencies
echo "📋 Installing dependencies..."
cd "$INSTALL_DIR"
$PYTHON_CMD -m pip install --user -r requirements.txt

# Create wrapper script
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

cat > "$BIN_DIR/fixit" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
$PYTHON_CMD fixit.py "\$@"
EOF

chmod +x "$BIN_DIR/fixit"

# Add to PATH
echo "🔧 Configuring PATH..."
SHELL_RC=""
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
elif [[ -f "$HOME/.profile" ]]; then
    SHELL_RC="$HOME/.profile"
fi

if [[ -n "$SHELL_RC" ]]; then
    if ! grep -q "export PATH=\"\$HOME/.local/bin:\$PATH\"" "$SHELL_RC" 2>/dev/null; then
        echo "" >> "$SHELL_RC"
        echo "# Added by FixIt installer" >> "$SHELL_RC"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        echo "✓ Added to PATH in $SHELL_RC"
    fi
fi

# Cleanup
rm -f "$TEMP_ZIP"
rm -rf "/tmp/fixit-main"

echo ""
echo "✅ FixIt installation completed successfully!"
echo ""
echo "🎯 Getting Started:"
echo "  fixit list                    # List available software"
echo "  fixit install mongodb        # Install MongoDB"
echo "  fixit info nodejs            # Get Node.js information"
echo ""
echo "📚 Documentation: https://github.com/Jayu1214/fixit"
echo ""
echo "Note: Restart your terminal or run 'source $SHELL_RC' to use the fixit command."
echo ""
echo "🎉 Happy installing!"
