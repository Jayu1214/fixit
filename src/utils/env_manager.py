"""
Environment variable management for FixIt
"""

import os
import platform
import subprocess
from typing import Dict

class EnvironmentManager:
    """Manages environment variables across different platforms"""
    
    def __init__(self, logger):
        self.logger = logger
        self.system = platform.system().lower()
    
    def update_environment(self, env_vars: Dict[str, str]):
        """Update environment variables"""
        for var_name, var_value in env_vars.items():
            if var_name.upper() == "PATH":
                self._update_path(var_value)
            else:
                self._set_env_var(var_name, var_value)
    
    def _update_path(self, new_path: str):
        """Add directory to PATH environment variable"""
        try:
            if self.system == "windows":
                self._update_windows_path(new_path)
            else:
                self._update_unix_path(new_path)
        except Exception as e:
            self.logger.error(f"Failed to update PATH: {e}")
    
    def _update_windows_path(self, new_path: str):
        """Update PATH on Windows using registry"""
        try:
            # Get current PATH from registry
            result = subprocess.run([
                "reg", "query", 
                "HKEY_CURRENT_USER\\Environment", 
                "/v", "PATH"
            ], capture_output=True, text=True)
            
            current_path = ""
            if result.returncode == 0:
                # Parse registry output
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if 'PATH' in line and 'REG_' in line:
                        parts = line.split(None, 3)
                        if len(parts) >= 4:
                            current_path = parts[3]
                        break
            
            # Check if path already exists
            if new_path.lower() in current_path.lower():
                self.logger.debug(f"Path already in PATH: {new_path}")
                return
            
            # Add new path
            if current_path:
                updated_path = f"{current_path};{new_path}"
            else:
                updated_path = new_path
            
            # Update registry
            subprocess.run([
                "reg", "add", 
                "HKEY_CURRENT_USER\\Environment", 
                "/v", "PATH", 
                "/t", "REG_EXPAND_SZ", 
                "/d", updated_path, 
                "/f"
            ], check=True)
            
            # Notify system of environment change
            subprocess.run([
                "powershell", "-Command",
                "[Environment]::SetEnvironmentVariable('PATH', $env:PATH + ';' + $args[0], 'User')",
                new_path
            ])
            
            self.logger.info(f"Added to PATH: {new_path}")
            self.logger.info("Note: You may need to restart your terminal for PATH changes to take effect")
            
        except Exception as e:
            self.logger.error(f"Failed to update Windows PATH: {e}")
    
    def _update_unix_path(self, new_path: str):
        """Update PATH on Unix-like systems"""
        try:
            # Check current PATH
            current_path = os.environ.get("PATH", "")
            if new_path in current_path:
                self.logger.debug(f"Path already in PATH: {new_path}")
                return
            
            # Determine shell configuration file
            shell_configs = [
                os.path.expanduser("~/.bashrc"),
                os.path.expanduser("~/.bash_profile"),
                os.path.expanduser("~/.zshrc"),
                os.path.expanduser("~/.profile")
            ]
            
            config_file = None
            for config in shell_configs:
                if os.path.exists(config):
                    config_file = config
                    break
            
            if not config_file:
                config_file = os.path.expanduser("~/.bashrc")
            
            # Add export statement to shell config
            export_line = f'export PATH="$PATH:{new_path}"\n'
            
            # Check if line already exists
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    if new_path in content:
                        self.logger.debug(f"Path already configured in {config_file}")
                        return
            except FileNotFoundError:
                pass
            
            # Append to config file
            with open(config_file, 'a') as f:
                f.write(f"\n# Added by FixIt\n{export_line}")
            
            self.logger.info(f"Added to PATH in {config_file}: {new_path}")
            self.logger.info("Note: You may need to restart your terminal or run 'source ~/.bashrc' for PATH changes to take effect")
            
        except Exception as e:
            self.logger.error(f"Failed to update Unix PATH: {e}")
    
    def _set_env_var(self, var_name: str, var_value: str):
        """Set environment variable"""
        try:
            if self.system == "windows":
                # Set environment variable in Windows registry
                subprocess.run([
                    "reg", "add",
                    "HKEY_CURRENT_USER\\Environment",
                    "/v", var_name,
                    "/t", "REG_SZ",
                    "/d", var_value,
                    "/f"
                ], check=True)
                
                self.logger.info(f"Set environment variable: {var_name}={var_value}")
            else:
                # Add to shell configuration file
                shell_configs = [
                    os.path.expanduser("~/.bashrc"),
                    os.path.expanduser("~/.bash_profile"),
                    os.path.expanduser("~/.zshrc"),
                    os.path.expanduser("~/.profile")
                ]
                
                config_file = None
                for config in shell_configs:
                    if os.path.exists(config):
                        config_file = config
                        break
                
                if not config_file:
                    config_file = os.path.expanduser("~/.bashrc")
                
                export_line = f'export {var_name}="{var_value}"\n'
                
                with open(config_file, 'a') as f:
                    f.write(f"\n# Added by FixIt\n{export_line}")
                
                self.logger.info(f"Set environment variable in {config_file}: {var_name}={var_value}")
                
        except Exception as e:
            self.logger.error(f"Failed to set environment variable {var_name}: {e}")
    
    def get_env_var(self, var_name: str) -> str:
        """Get environment variable value"""
        return os.environ.get(var_name, "")
