# FixIt - Cross-platform Software Installation Framework

🚀 Install any software on any platform with a single command. Like pip/npm, but for desktop applications.

```bash
fixit install mongodb    # Works on Windows, Linux, macOS
fixit install nodejs     # Automatic PATH configuration
fixit install docker     # Silent installation with progress
```

## ✨ Features

- 🌍 **Cross-platform**: Windows, Linux, macOS
- ⚡ **One-command install**: No more manual downloads
- 🔧 **Auto-configuration**: PATH and environment setup
- ✅ **Verification**: Confirms installation success
- 📦 **7+ packages**: MongoDB, Node.js, Docker, PostgreSQL, Git, Python, VS Code
- 🔍 **Smart detection**: Automatically detects your OS and architecture

## 🚀 Quick Start

### One-line install:
```bash
# Linux/macOS
curl -sSL https://raw.githubusercontent.com/[username]/fixit/main/quick_install.sh | bash

# Windows (PowerShell)
iwr -useb https://raw.githubusercontent.com/[username]/fixit/main/quick_install.bat | iex
```

### Or install via pip:
```bash
pip install fixit-installer
```

### Or manual install:
```bash
git clone https://github.com/Jayu1214/fixit.git
cd fixit
pip install -r requirements.txt
```

## 📖 Usage

### List available software
```bash
fixit list                    # Show all available packages
fixit list --installed       # Show only installed packages
```

### Install software
```bash
fixit install mongodb        # Install latest MongoDB
fixit install nodejs --version 18.17.0  # Install specific version
fixit install docker --force # Force reinstall
```

### Get information
```bash
fixit info mongodb           # Show package details
```

### Remove software
```bash
fixit remove mongodb         # Uninstall package
```

### Update software
```bash
fixit update nodejs          # Update specific package
fixit update                 # Update all packages
```

## 📦 Supported Software

- **MongoDB** - Document database
- **Node.js** - JavaScript runtime
- **PostgreSQL** - Relational database  
- **Docker** - Containerization platform
- **Git** - Version control system
- **Python** - Programming language
- **VS Code** - Code editor

*More packages coming soon! Contribute by adding to the [software registry](registry/software.json).*

## 🛠️ How It Works

1. **Detects your OS** (Windows/Linux/macOS) and architecture
2. **Downloads** the appropriate installer from official sources
3. **Installs silently** using OS-specific methods
4. **Configures environment** variables (PATH, etc.)
5. **Verifies installation** by running version checks
6. **Cleans up** temporary files

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add new software**: Update [registry/software.json](registry/software.json)
2. **Fix bugs**: Create issues and submit pull requests
3. **Improve docs**: Help us make the documentation better
4. **Test on different platforms**: Ensure compatibility

See our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📋 Requirements

- Python 3.8+
- Internet connection for downloads
- Administrator/sudo privileges for installations

## 🔒 Security

- All downloads are from official vendor sources
- Package integrity verified where possible
- No telemetry or data collection
- Open source and auditable

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by package managers like pip, npm, and homebrew
- Built with ❤️ for the developer community
