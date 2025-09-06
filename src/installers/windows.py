"""
Windows-specific installer for FixIt
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

class WindowsInstaller:
    """Handles Windows-specific installations"""
    
    def __init__(self, logger):
        self.logger = logger
    
    def install(self, installer_path: str, install_command: str, software_info: Dict[str, Any]) -> bool:
        """Install software on Windows"""
        try:
            # Format install command with installer path
            command = install_command.format(installer=installer_path)
            
            self.logger.debug(f"Running install command: {command}")
            
            # Run installation command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            if result.returncode == 0:
                self.logger.debug("Installation command completed successfully")
                return True
            else:
                self.logger.error(f"Installation failed with return code {result.returncode}")
                if result.stdout:
                    self.logger.debug(f"STDOUT: {result.stdout}")
                if result.stderr:
                    self.logger.debug(f"STDERR: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error("Installation timed out")
            return False
        except Exception as e:
            self.logger.error(f"Installation error: {e}")
            return False
    
    def remove(self, software: str) -> bool:
        """Remove software on Windows"""
        try:
            # Try to find software in installed programs
            self.logger.info(f"Looking for {software} in installed programs...")
            
            # Use wmic to find installed software
            result = subprocess.run([
                "wmic", "product", "where", f"name like '%{software}%'", "get", "name,version"
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and software.lower() in result.stdout.lower():
                # Try to uninstall using wmic
                uninstall_result = subprocess.run([
                    "wmic", "product", "where", f"name like '%{software}%'", "call", "uninstall"
                ], capture_output=True, text=True)
                
                if uninstall_result.returncode == 0:
                    self.logger.info(f"Successfully uninstalled {software}")
                    return True
            
            # Try chocolatey if available
            try:
                subprocess.run(["choco", "uninstall", software, "-y"], 
                             check=True, capture_output=True)
                self.logger.info(f"Successfully uninstalled {software} using Chocolatey")
                return True
            except:
                pass
            
            # Try winget if available
            try:
                subprocess.run(["winget", "uninstall", software], 
                             check=True, capture_output=True)
                self.logger.info(f"Successfully uninstalled {software} using Winget")
                return True
            except:
                pass
            
            self.logger.warning(f"Could not automatically remove {software}. Please remove manually.")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove {software}: {e}")
            return False
    
    def _run_elevated_command(self, command: str) -> bool:
        """Run command with elevated privileges"""
        try:
            # Create a temporary PowerShell script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False) as f:
                f.write(f"""
Start-Process -FilePath "cmd" -ArgumentList "/c {command}" -Verb RunAs -Wait
""")
                script_path = f.name
            
            try:
                result = subprocess.run([
                    "powershell", "-ExecutionPolicy", "Bypass", "-File", script_path
                ], capture_output=True, text=True)
                
                return result.returncode == 0
            finally:
                os.unlink(script_path)
                
        except Exception as e:
            self.logger.error(f"Failed to run elevated command: {e}")
            return False
    
    def _extract_msi(self, msi_path: str, extract_dir: str) -> bool:
        """Extract MSI file for inspection"""
        try:
            command = f'msiexec /a "{msi_path}" /qn TARGETDIR="{extract_dir}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _get_installed_programs(self):
        """Get list of installed programs"""
        try:
            result = subprocess.run([
                "wmic", "product", "get", "name,version,vendor"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            return ""
        except:
            return ""
