"""
Main installer logic for FixIt
"""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

from .registry import Registry
from .os_detector import OSDetector
from ..utils.downloader import Downloader
from ..utils.env_manager import EnvironmentManager
from ..installers.windows import WindowsInstaller
from ..installers.linux import LinuxInstaller
from ..installers.macos import MacOSInstaller

class Installer:
    """Main installer class that orchestrates the installation process"""
    
    def __init__(self, logger):
        self.logger = logger
        self.registry = Registry()
        self.os_detector = OSDetector()
        self.downloader = Downloader(logger)
        self.env_manager = EnvironmentManager(logger)
        
        # Get platform-specific installer
        os_name = self.os_detector.get_os_name()
        if os_name == "windows":
            self.platform_installer = WindowsInstaller(logger)
        elif os_name == "linux":
            self.platform_installer = LinuxInstaller(logger)
        elif os_name == "macos":
            self.platform_installer = MacOSInstaller(logger)
        else:
            raise Exception(f"Unsupported platform: {os_name}")
    
    def install(self, software: str, version: Optional[str] = None, force: bool = False) -> int:
        """Install software"""
        try:
            self.logger.info(f"Installing {software}...")
            
            # Check if software exists in registry
            if not self.registry.software_exists(software):
                self.logger.error(f"Software '{software}' not found in registry")
                self.logger.info("Use 'fixit list' to see available software")
                return 1
            
            # Get system info
            system_info = self.os_detector.get_system_info()
            self.logger.debug(f"System info: {system_info}")
            
            # Check if already installed
            if not force and self._is_installed(software):
                self.logger.info(f"{software} is already installed. Use --force to reinstall.")
                return 0
            
            # Get software info
            software_info = self.registry.get_software(software)
            platform = system_info["os"]
            
            # Use specified version or latest
            install_version = version or self.registry.get_latest_version(software)
            
            # Get platform-specific info
            platform_info = self.registry.get_platform_info(software, platform)
            if not platform_info:
                self.logger.error(f"{software} is not available for {platform}")
                return 1
            
            # Download installer
            download_url = self.registry.get_download_url(software, platform, install_version)
            if not download_url:
                self.logger.error(f"No download URL found for {software} on {platform}")
                return 1
            
            self.logger.info(f"Downloading {software} from {download_url}")
            installer_path = self.downloader.download(download_url, software)
            
            if not installer_path:
                self.logger.error("Failed to download installer")
                return 1
            
            # Install software
            self.logger.info(f"Installing {software}...")
            install_command = self.registry.get_install_command(software, platform)
            
            if not self.platform_installer.install(installer_path, install_command, software_info):
                self.logger.error(f"Failed to install {software}")
                return 1
            
            # Configure environment variables
            env_vars = self.registry.get_env_vars(software, platform)
            if env_vars:
                self.logger.info("Configuring environment variables...")
                self.env_manager.update_environment(env_vars)
            
            # Verify installation
            verify_command = self.registry.get_verify_command(software)
            if verify_command:
                self.logger.info("Verifying installation...")
                if self._verify_installation(verify_command):
                    self.logger.info(f"✓ {software} installed successfully!")
                else:
                    self.logger.warning(f"Installation completed but verification failed")
            else:
                self.logger.info(f"✓ {software} installation completed!")
            
            # Cleanup
            try:
                os.remove(installer_path)
            except:
                pass
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Installation failed: {e}")
            return 1
    
    def list_software(self, installed_only: bool = False) -> int:
        """List available or installed software"""
        try:
            software_list = self.registry.list_software()
            
            if not software_list:
                self.logger.info("No software available in registry")
                return 0
            
            self.logger.info("Available software:")
            self.logger.info("-" * 50)
            
            for software in sorted(software_list):
                info = self.registry.get_software_info(software)
                status = ""
                
                if installed_only:
                    if not self._is_installed(software):
                        continue
                    status = " [INSTALLED]"
                else:
                    if self._is_installed(software):
                        status = " [INSTALLED]"
                
                self.logger.info(f"  {info['name']}{status}")
                if info['description']:
                    self.logger.info(f"    {info['description']}")
                self.logger.info(f"    Version: {info['latest_version']}")
                self.logger.info("")
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Failed to list software: {e}")
            return 1
    
    def remove(self, software: str) -> int:
        """Remove installed software"""
        try:
            self.logger.info(f"Removing {software}...")
            
            if not self._is_installed(software):
                self.logger.info(f"{software} is not installed")
                return 0
            
            # Platform-specific removal
            if self.platform_installer.remove(software):
                self.logger.info(f"✓ {software} removed successfully!")
                return 0
            else:
                self.logger.error(f"Failed to remove {software}")
                return 1
                
        except Exception as e:
            self.logger.error(f"Removal failed: {e}")
            return 1
    
    def update(self, software: Optional[str] = None) -> int:
        """Update software"""
        try:
            if software:
                # Update specific software
                self.logger.info(f"Updating {software}...")
                return self.install(software, force=True)
            else:
                # Update all installed software
                self.logger.info("Updating all installed software...")
                software_list = self.registry.list_software()
                
                for sw in software_list:
                    if self._is_installed(sw):
                        self.logger.info(f"Updating {sw}...")
                        self.install(sw, force=True)
                
                return 0
                
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
            return 1
    
    def info(self, software: str) -> int:
        """Show software information"""
        try:
            if not self.registry.software_exists(software):
                self.logger.error(f"Software '{software}' not found in registry")
                return 1
            
            info = self.registry.get_software_info(software)
            
            self.logger.info(f"Software Information: {info['name']}")
            self.logger.info("=" * 50)
            self.logger.info(f"Description: {info['description']}")
            self.logger.info(f"Latest Version: {info['latest_version']}")
            self.logger.info(f"Supported Platforms: {', '.join(info['platforms'])}")
            self.logger.info(f"Verify Command: {info['verify_command']}")
            self.logger.info(f"Homepage: {info['homepage']}")
            self.logger.info(f"License: {info['license']}")
            
            if self._is_installed(software):
                self.logger.info("Status: INSTALLED")
            else:
                self.logger.info("Status: NOT INSTALLED")
            
            return 0
            
        except Exception as e:
            self.logger.error(f"Failed to get software info: {e}")
            return 1
    
    def _is_installed(self, software: str) -> bool:
        """Check if software is installed"""
        verify_command = self.registry.get_verify_command(software)
        if not verify_command:
            return False
        
        return self._verify_installation(verify_command)
    
    def _verify_installation(self, verify_command: str) -> bool:
        """Verify installation by running verification command"""
        try:
            result = subprocess.run(
                verify_command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0
        except:
            return False
