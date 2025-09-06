"""
File downloader utilities for FixIt
"""

import os
import requests
import tempfile
from pathlib import Path
from urllib.parse import urlparse
from tqdm import tqdm

class Downloader:
    """Handles downloading files from URLs"""
    
    def __init__(self, logger):
        self.logger = logger
        self.download_dir = Path(tempfile.gettempdir()) / "fixit_downloads"
        self.download_dir.mkdir(exist_ok=True)
    
    def download(self, url: str, software: str) -> str:
        """Download file from URL and return local path"""
        try:
            # Parse URL to get filename
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            if not filename:
                # Generate filename based on software name and URL
                extension = self._get_extension_from_url(url)
                filename = f"{software}_installer{extension}"
            
            local_path = self.download_dir / filename
            
            # Check if file already exists
            if local_path.exists():
                self.logger.debug(f"File already exists: {local_path}")
                return str(local_path)
            
            # Download file with progress bar
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(local_path, 'wb') as f:
                if total_size > 0:
                    with tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=filename
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    # No content-length header, download without progress bar
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            
            self.logger.info(f"Downloaded: {filename}")
            return str(local_path)
            
        except requests.RequestException as e:
            self.logger.error(f"Download failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during download: {e}")
            return None
    
    def _get_extension_from_url(self, url: str) -> str:
        """Get file extension from URL or guess based on content"""
        # Common installer extensions by platform
        extensions = {
            'windows': '.exe',
            'linux': '.deb',
            'macos': '.dmg'
        }
        
        # Try to guess from URL
        if '.exe' in url:
            return '.exe'
        elif '.msi' in url:
            return '.msi'
        elif '.deb' in url:
            return '.deb'
        elif '.rpm' in url:
            return '.rpm'
        elif '.dmg' in url:
            return '.dmg'
        elif '.pkg' in url:
            return '.pkg'
        elif '.tar.gz' in url:
            return '.tar.gz'
        elif '.zip' in url:
            return '.zip'
        else:
            return '.bin'
    
    def cleanup(self):
        """Clean up downloaded files"""
        try:
            import shutil
            if self.download_dir.exists():
                shutil.rmtree(self.download_dir)
                self.logger.debug("Cleaned up download directory")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup downloads: {e}")
    
    def get_file_size(self, url: str) -> int:
        """Get file size without downloading"""
        try:
            response = requests.head(url)
            response.raise_for_status()
            return int(response.headers.get('content-length', 0))
        except:
            return 0
