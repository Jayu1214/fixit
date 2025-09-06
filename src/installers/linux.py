"""
Linux-specific installer for FixIt
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, Any

class LinuxInstaller:
    """Handles Linux-specific installations"""
    
    def __init__(self, logger):
        self.logger = logger
        self.package_manager = self._detect_package_manager()
    
    def _detect_package_manager(self) -> str:
        """Detect available package manager"""
        managers = [
            ("apt", "apt-get"),
            ("yum", "yum"),
            ("dnf", "dnf"),
            ("pacman", "pacman"),
            ("zypper", "zypper"),
            ("snap", "snap")
        ]
        
        for cmd, manager in managers:
            try:
                subprocess.run(["which", cmd], 
                             capture_output=True, check=True)
                return manager
            except:
                continue
        
        return "manual"
    
    def install(self, installer_path: str, install_command: str, software_info: Dict[str, Any]) -> bool:
        """Install software on Linux"""
        try:
            # Format install command with installer path
            command = install_command.format(installer=installer_path)
            
            self.logger.debug(f"Running install command: {command}")
            
            # Check if we need sudo
            if not self._has_sudo_access():
                self.logger.error("Installation requires sudo access")
                return False
            
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
        """Remove software on Linux"""
        try:
            if self.package_manager == "apt-get":
                return self._remove_with_apt(software)
            elif self.package_manager == "yum":
                return self._remove_with_yum(software)
            elif self.package_manager == "dnf":
                return self._remove_with_dnf(software)
            elif self.package_manager == "pacman":
                return self._remove_with_pacman(software)
            elif self.package_manager == "zypper":
                return self._remove_with_zypper(software)
            elif self.package_manager == "snap":
                return self._remove_with_snap(software)
            else:
                self.logger.warning(f"No known package manager found. Cannot automatically remove {software}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to remove {software}: {e}")
            return False
    
    def _has_sudo_access(self) -> bool:
        """Check if user has sudo access"""
        try:
            result = subprocess.run(
                ["sudo", "-n", "true"],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _remove_with_apt(self, software: str) -> bool:
        """Remove software using apt"""
        try:
            result = subprocess.run([
                "sudo", "apt-get", "remove", "-y", software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully removed {software} using apt")
                return True
            return False
        except:
            return False
    
    def _remove_with_yum(self, software: str) -> bool:
        """Remove software using yum"""
        try:
            result = subprocess.run([
                "sudo", "yum", "remove", "-y", software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully removed {software} using yum")
                return True
            return False
        except:
            return False
    
    def _remove_with_dnf(self, software: str) -> bool:
        """Remove software using dnf"""
        try:
            result = subprocess.run([
                "sudo", "dnf", "remove", "-y", software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully removed {software} using dnf")
                return True
            return False
        except:
            return False
    
    def _remove_with_pacman(self, software: str) -> bool:
        """Remove software using pacman"""
        try:
            result = subprocess.run([
                "sudo", "pacman", "-R", "--noconfirm", software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully removed {software} using pacman")
                return True
            return False
        except:
            return False
    
    def _remove_with_zypper(self, software: str) -> bool:
        """Remove software using zypper"""
        try:
            result = subprocess.run([
                "sudo", "zypper", "remove", "-y", software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully removed {software} using zypper")
                return True
            return False
        except:
            return False
    
    def _remove_with_snap(self, software: str) -> bool:
        """Remove software using snap"""
        try:
            result = subprocess.run([
                "sudo", "snap", "remove", software
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Successfully removed {software} using snap")
                return True
            return False
        except:
            return False
    
    def _extract_deb(self, deb_path: str, extract_dir: str) -> bool:
        """Extract DEB file for inspection"""
        try:
            command = f'dpkg-deb -x "{deb_path}" "{extract_dir}"'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def _extract_rpm(self, rpm_path: str, extract_dir: str) -> bool:
        """Extract RPM file for inspection"""
        try:
            command = f'cd "{extract_dir}" && rpm2cpio "{rpm_path}" | cpio -idmv'
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
