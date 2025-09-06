"""
OS Detection utilities for FixIt
"""

import platform
import sys
from typing import Dict, Any

class OSDetector:
    """Detects the current operating system and provides system information"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        self.release = platform.release()
        self.version = platform.version()
    
    def get_os_name(self) -> str:
        """Get normalized OS name"""
        if self.system == "windows":
            return "windows"
        elif self.system == "linux":
            return "linux"
        elif self.system == "darwin":
            return "macos"
        else:
            raise Exception(f"Unsupported operating system: {self.system}")
    
    def get_architecture(self) -> str:
        """Get system architecture"""
        arch_mapping = {
            "x86_64": "x64",
            "amd64": "x64",
            "i386": "x86",
            "i686": "x86",
            "arm64": "arm64",
            "aarch64": "arm64"
        }
        return arch_mapping.get(self.machine, self.machine)
    
    def is_admin(self) -> bool:
        """Check if running with administrator/root privileges"""
        try:
            if self.system == "windows":
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                import os
                return os.geteuid() == 0
        except:
            return False
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        return {
            "os": self.get_os_name(),
            "architecture": self.get_architecture(),
            "release": self.release,
            "version": self.version,
            "python_version": sys.version.split()[0],
            "is_admin": self.is_admin()
        }
    
    def get_package_manager(self) -> str:
        """Get the appropriate package manager for the OS"""
        os_name = self.get_os_name()
        
        if os_name == "windows":
            # Check for chocolatey, winget, or scoop
            import subprocess
            try:
                subprocess.run(["choco", "--version"], 
                             capture_output=True, check=True)
                return "chocolatey"
            except:
                try:
                    subprocess.run(["winget", "--version"], 
                                 capture_output=True, check=True)
                    return "winget"
                except:
                    try:
                        subprocess.run(["scoop", "--version"], 
                                     capture_output=True, check=True)
                        return "scoop"
                    except:
                        return "manual"
        
        elif os_name == "linux":
            # Check for apt, yum, dnf, pacman, etc.
            import subprocess
            managers = [
                ("apt", "apt"),
                ("yum", "yum"),
                ("dnf", "dnf"),
                ("pacman", "pacman"),
                ("zypper", "zypper")
            ]
            
            for cmd, name in managers:
                try:
                    subprocess.run(["which", cmd], 
                                 capture_output=True, check=True)
                    return name
                except:
                    continue
            return "manual"
        
        elif os_name == "macos":
            # Check for brew
            import subprocess
            try:
                subprocess.run(["brew", "--version"], 
                             capture_output=True, check=True)
                return "homebrew"
            except:
                return "manual"
        
        return "manual"
