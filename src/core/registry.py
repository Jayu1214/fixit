"""
Registry management for FixIt
Handles loading and managing software registry
"""

import json
import os
from typing import Dict, Any, Optional, List
from pathlib import Path

class Registry:
    """Manages the software registry"""
    
    def __init__(self, registry_path: Optional[str] = None):
        if registry_path is None:
            # Default to registry/software.json relative to project root
            project_root = Path(__file__).parent.parent.parent
            registry_path = project_root / "registry" / "software.json"
        
        self.registry_path = Path(registry_path)
        self._registry_data = None
        self._load_registry()
    
    def _load_registry(self):
        """Load registry data from file"""
        try:
            if self.registry_path.exists():
                with open(self.registry_path, 'r', encoding='utf-8') as f:
                    self._registry_data = json.load(f)
            else:
                self._registry_data = {}
        except Exception as e:
            raise Exception(f"Failed to load registry from {self.registry_path}: {e}")
    
    def get_software(self, name: str) -> Optional[Dict[str, Any]]:
        """Get software information by name"""
        return self._registry_data.get(name.lower())
    
    def list_software(self) -> List[str]:
        """List all available software"""
        return list(self._registry_data.keys())
    
    def get_platform_info(self, software: str, platform: str) -> Optional[Dict[str, Any]]:
        """Get platform-specific information for software"""
        software_info = self.get_software(software)
        if not software_info:
            return None
        
        platforms = software_info.get("platforms", {})
        return platforms.get(platform)
    
    def get_download_url(self, software: str, platform: str, version: Optional[str] = None) -> Optional[str]:
        """Get download URL for software on specific platform"""
        platform_info = self.get_platform_info(software, platform)
        if not platform_info:
            return None
        
        download_url = platform_info.get("download_url")
        if version and "{version}" in download_url:
            download_url = download_url.replace("{version}", version)
        
        return download_url
    
    def get_install_command(self, software: str, platform: str) -> Optional[str]:
        """Get install command for software on specific platform"""
        platform_info = self.get_platform_info(software, platform)
        if not platform_info:
            return None
        
        return platform_info.get("install_command")
    
    def get_env_vars(self, software: str, platform: str) -> Dict[str, str]:
        """Get environment variables for software on specific platform"""
        platform_info = self.get_platform_info(software, platform)
        if not platform_info:
            return {}
        
        return platform_info.get("env_vars", {})
    
    def get_verify_command(self, software: str) -> Optional[str]:
        """Get verification command for software"""
        software_info = self.get_software(software)
        if not software_info:
            return None
        
        return software_info.get("verify_command")
    
    def get_latest_version(self, software: str) -> Optional[str]:
        """Get latest version for software"""
        software_info = self.get_software(software)
        if not software_info:
            return None
        
        return software_info.get("latest_version")
    
    def software_exists(self, software: str) -> bool:
        """Check if software exists in registry"""
        return software.lower() in self._registry_data
    
    def get_software_info(self, software: str) -> Dict[str, Any]:
        """Get complete software information"""
        software_info = self.get_software(software)
        if not software_info:
            return {}
        
        return {
            "name": software_info.get("name", software),
            "description": software_info.get("description", ""),
            "latest_version": software_info.get("latest_version", "unknown"),
            "platforms": list(software_info.get("platforms", {}).keys()),
            "verify_command": software_info.get("verify_command", ""),
            "homepage": software_info.get("homepage", ""),
            "license": software_info.get("license", "")
        }
