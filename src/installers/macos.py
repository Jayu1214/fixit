"""
macOS-specific installer for FixIt
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

class MacOSInstaller:
    """Handles macOS-specific installations"""
    
    def __init__(self, logger):
        self.logger = logger
        self.has_brew = self._check_homebrew()
    
    def _check_homebrew(self) -> bool:
        """Check if Homebrew is available"""
        try:
            subprocess.run(["brew", "--version"], 
                         capture_output=True, check=True)
            return True
        except:
            return False
    
    def install(self, installer_path: str, install_command: str, software_info: Dict[str, Any]) -> bool:
        """Install software on macOS"""
        try:
            # Format install command with installer path
            command = install_command.format(installer=installer_path)
            
            self.logger.debug(f"Running install command: {command}")
            
            # Handle different installer types
            if installer_path.endswith('.dmg'):
                return self._install_dmg(installer_path, command)
            elif installer_path.endswith('.pkg'):
                return self._install_pkg(installer_path, command)
            else:
                # Generic installation
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
    
    def _install_dmg(self, dmg_path: str, command: str) -> bool:
        """Install from DMG file"""
        try:
            # Mount DMG
            mount_result = subprocess.run([
                "hdiutil", "attach", dmg_path, "-quiet"
            ], capture_output=True, text=True)
            
            if mount_result.returncode != 0:
                self.logger.error("Failed to mount DMG")
                return False
            
            # Find mount point
            mount_point = None
            for line in mount_result.stdout.split('\n'):
                if '/Volumes/' in line:
                    mount_point = line.strip().split('\t')[-1]
                    break
            
            if not mount_point:
                self.logger.error("Could not find mount point")
                return False
            
            try:
                # Look for .app or .pkg files in the mounted volume
                volume_path = Path(mount_point)
                app_files = list(volume_path.glob("*.app"))
                pkg_files = list(volume_path.glob("*.pkg"))
                
                if app_files:
                    # Copy .app to Applications
                    app_file = app_files[0]
                    subprocess.run([
                        "cp", "-R", str(app_file), "/Applications/"
                    ], check=True)
                    self.logger.info(f"Copied {app_file.name} to Applications")
                    return True
                elif pkg_files:
                    # Install .pkg
                    pkg_file = pkg_files[0]
                    result = subprocess.run([
                        "sudo", "installer", "-pkg", str(pkg_file), "-target", "/"
                    ], capture_output=True, text=True)
                    return result.returncode == 0
                else:
                    # Run custom command
                    result = subprocess.run(
                        command.replace("{installer}", mount_point),
                        shell=True,
                        capture_output=True,
                        text=True
                    )
                    return result.returncode == 0
                    
            finally:
                # Unmount DMG
                subprocess.run([
                    "hdiutil", "detach", mount_point, "-quiet"
                ], capture_output=True)
                
        except Exception as e:
            self.logger.error(f"Failed to install DMG: {e}")
            return False
    
    def _install_pkg(self, pkg_path: str, command: str) -> bool:
        """Install PKG file"""
        try:
            result = subprocess.run([
                "sudo", "installer", "-pkg", pkg_path, "-target", "/"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("PKG installation completed successfully")
                return True
            else:
                self.logger.error(f"PKG installation failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to install PKG: {e}")
            return False
    
    def remove(self, software: str) -> bool:
        """Remove software on macOS"""
        try:
            # Try Homebrew first if available
            if self.has_brew:
                try:
                    result = subprocess.run([
                        "brew", "uninstall", software
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.logger.info(f"Successfully removed {software} using Homebrew")
                        return True
                except:
                    pass
                
                # Try as cask
                try:
                    result = subprocess.run([
                        "brew", "uninstall", "--cask", software
                    ], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        self.logger.info(f"Successfully removed {software} cask using Homebrew")
                        return True
                except:
                    pass
            
            # Look for application in /Applications
            app_path = Path(f"/Applications/{software}.app")
            if app_path.exists():
                subprocess.run(["rm", "-rf", str(app_path)], check=True)
                self.logger.info(f"Removed {software}.app from Applications")
                return True
            
            # Look for variations of the app name
            apps_dir = Path("/Applications")
            for app in apps_dir.glob("*.app"):
                if software.lower() in app.name.lower():
                    subprocess.run(["rm", "-rf", str(app)], check=True)
                    self.logger.info(f"Removed {app.name} from Applications")
                    return True
            
            self.logger.warning(f"Could not find {software} to remove")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to remove {software}: {e}")
            return False
    
    def _get_installed_applications(self):
        """Get list of installed applications"""
        try:
            apps_dir = Path("/Applications")
            apps = [app.stem for app in apps_dir.glob("*.app")]
            return apps
        except:
            return []
