"""
Configuration management for FixIt
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Manages FixIt configuration"""
    
    def __init__(self):
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._config = self._load_config()
    
    def _get_config_dir(self) -> Path:
        """Get configuration directory based on OS"""
        if os.name == 'nt':  # Windows
            config_dir = Path(os.environ.get('APPDATA', '')) / 'FixIt'
        else:  # Unix-like
            config_dir = Path.home() / '.config' / 'fixit'
        return config_dir
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "download_dir": str(self.config_dir / "downloads"),
            "log_level": "INFO",
            "verify_ssl": True,
            "timeout": 600,
            "max_retries": 3,
            "auto_cleanup": True,
            "parallel_downloads": False,
            "remote": {
            "registry_url": "https://raw.githubusercontent.com/Jayu1214/fixit/main/registry/software.json",
        },
            "update_check": True,
            "telemetry": False
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception:
                pass
        else:
            self._save_config(default_config)
        
        return default_config
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        self._config[key] = value
        self._save_config(self._config)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration"""
        return self._config.copy()
    
    def reset(self):
        """Reset configuration to defaults"""
        if self.config_file.exists():
            self.config_file.unlink()
        self._config = self._load_config()
    
    def export_config(self, file_path: str):
        """Export configuration to file"""
        with open(file_path, 'w') as f:
            json.dump(self._config, f, indent=2)
    
    def import_config(self, file_path: str):
        """Import configuration from file"""
        with open(file_path, 'r') as f:
            imported_config = json.load(f)
        self._config.update(imported_config)
        self._save_config(self._config)
