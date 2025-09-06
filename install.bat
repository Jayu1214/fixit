@echo off
REM Windows installer script for FixIt

echo 🚀 Installing FixIt - Cross-platform Software Installation Framework
echo ==================================================================

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.8+ from https://python.org and try again.
    pause
    exit /b 1
)

echo ✓ Python found
python --version

REM Check pip
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is required but not installed.
    pause
    exit /b 1
)

echo ✓ pip found

REM Install FixIt
echo 📦 Installing FixIt...
python -m pip install --user git+https://github.com/Jayu1214/fixit.git

if %errorlevel% neq 0 (
    echo ❌ Installation failed
    pause
    exit /b 1
)

echo ✅ FixIt installation completed!
echo.
echo 🎯 Usage:
echo   fixit list                    # List available software
echo   fixit install mongodb        # Install MongoDB
echo   fixit info nodejs            # Get Node.js information
echo.
echo 📚 Documentation: https://github.com/Jayu1214/fixit
echo.
echo Note: The fixit command should now be available in your terminal.

pause
