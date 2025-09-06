@echo off
REM One-line installer for FixIt on Windows
REM Usage: Run this script directly or via: curl -o install_fixit.bat https://raw.githubusercontent.com/Jayu1214/fixit/main/quick_install.bat && install_fixit.bat

echo 🚀 FixIt Installer - Cross-platform Software Installation Framework
echo ==================================================================

REM Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✓ Found Python
python --version

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

REM Create installation directory
set INSTALL_DIR=%USERPROFILE%\AppData\Local\FixIt
echo 📂 Installing to: %INSTALL_DIR%
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Download FixIt using PowerShell
echo 📥 Downloading FixIt...
REM Download URL
set DOWNLOAD_URL=https://github.com/Jayu1214/fixit/archive/main.zip
set TEMP_ZIP=%TEMP%\fixit-main.zip

powershell -Command "try { Invoke-WebRequest -Uri '%DOWNLOAD_URL%' -OutFile '%TEMP_ZIP%' -UseBasicParsing } catch { Write-Host 'Failed to download FixIt'; exit 1 }"
if %errorlevel% neq 0 (
    echo ❌ Failed to download FixIt
    pause
    exit /b 1
)

REM Extract using PowerShell
echo 📦 Extracting FixIt...
powershell -Command "try { Expand-Archive -Path '%TEMP_ZIP%' -DestinationPath '%TEMP%' -Force; Copy-Item '%TEMP%\fixit-main\*' -Destination '%INSTALL_DIR%' -Recurse -Force } catch { Write-Host 'Failed to extract FixIt'; exit 1 }"
if %errorlevel% neq 0 (
    echo ❌ Failed to extract FixIt
    pause
    exit /b 1
)

REM Install dependencies
echo 📋 Installing dependencies...
cd /d "%INSTALL_DIR%"
python -m pip install --user -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

REM Create batch wrapper
set BIN_DIR=%USERPROFILE%\AppData\Local\Microsoft\WindowsApps
if not exist "%BIN_DIR%" set BIN_DIR=%USERPROFILE%\AppData\Local\bin
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo @echo off > "%BIN_DIR%\fixit.bat"
echo cd /d "%INSTALL_DIR%" >> "%BIN_DIR%\fixit.bat"
echo python fixit.py %%* >> "%BIN_DIR%\fixit.bat"

REM Add to PATH if needed
echo 🔧 Configuring PATH...
powershell -Command "
$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
$binDir = '%BIN_DIR%'
if ($currentPath -notlike '*' + $binDir + '*') {
    $newPath = $currentPath + ';' + $binDir
    [Environment]::SetEnvironmentVariable('PATH', $newPath, 'User')
    Write-Host '✓ Added to PATH'
} else {
    Write-Host '✓ Already in PATH'
}
"

REM Cleanup
del "%TEMP_ZIP%" >nul 2>&1
rmdir /s /q "%TEMP%\fixit-main" >nul 2>&1

echo.
echo ✅ FixIt installation completed successfully!
echo.
echo 🎯 Getting Started:
echo   fixit list                    # List available software
echo   fixit install mongodb        # Install MongoDB
echo   fixit info nodejs            # Get Node.js information
echo.
echo 📚 Documentation: https://github.com/Jayu1214/fixit
echo.
echo Note: Restart your terminal to use the fixit command.
echo.
echo 🎉 Happy installing!

pause
