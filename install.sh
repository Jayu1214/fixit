#!/bin/bash
# Universal installer script for FixIt

set -e

echo "🚀 Installing FixIt - Cross-platform Software Installation Framework"
echo "=================================================================="

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "✓ Detected OS: $OS"

# Check Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is required but not installed."
    echo "Please install Python 3.8+ and try again."
    exit 1
fi

PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "✓ Python found: $($PYTHON_CMD --version)"

# Check pip
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ pip is required but not installed."
    exit 1
fi

echo "✓ pip found"

# Install FixIt
echo "📦 Installing FixIt..."
$PYTHON_CMD -m pip install --user git+https://github.com/Jayu1214/fixit.git

# Add to PATH (if needed)
echo "🔧 Configuring PATH..."
if [[ "$OS" == "linux" || "$OS" == "macos" ]]; then
    SHELL_RC=""
    if [[ -f ~/.bashrc ]]; then
        SHELL_RC="$HOME/.bashrc"
    elif [[ -f ~/.zshrc ]]; then
        SHELL_RC="$HOME/.zshrc"
    elif [[ -f ~/.profile ]]; then
        SHELL_RC="$HOME/.profile"
    fi
    
    if [[ -n "$SHELL_RC" ]]; then
        if ! grep -q "# FixIt PATH" "$SHELL_RC"; then
            echo "" >> "$SHELL_RC"
            echo "# FixIt PATH" >> "$SHELL_RC"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
            echo "✓ Added FixIt to PATH in $SHELL_RC"
        fi
    fi
fi

echo "✅ FixIt installation completed!"
echo ""
echo "🎯 Usage:"
echo "  fixit list                    # List available software"
echo "  fixit install mongodb        # Install MongoDB"
echo "  fixit info nodejs            # Get Node.js information"
echo ""
echo "📚 Documentation: https://github.com/Jayu1214/fixit"
echo ""
echo "Note: You may need to restart your terminal or run 'source ~/.bashrc' for the fixit command to be available."
