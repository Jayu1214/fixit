"""
Test OS detector functionality
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.os_detector import OSDetector

class TestOSDetector(unittest.TestCase):
    """Test OS detection functionality"""
    
    def setUp(self):
        self.detector = OSDetector()
    
    def test_get_os_name(self):
        """Test OS name detection"""
        os_name = self.detector.get_os_name()
        self.assertIn(os_name, ['windows', 'linux', 'macos'])
    
    def test_get_architecture(self):
        """Test architecture detection"""
        arch = self.detector.get_architecture()
        self.assertIn(arch, ['x64', 'x86', 'arm64'])
    
    def test_get_system_info(self):
        """Test system information retrieval"""
        info = self.detector.get_system_info()
        
        required_keys = ['os', 'architecture', 'release', 'version', 'python_version', 'is_admin']
        for key in required_keys:
            self.assertIn(key, info)
    
    def test_get_package_manager(self):
        """Test package manager detection"""
        pm = self.detector.get_package_manager()
        self.assertIsInstance(pm, str)

if __name__ == '__main__':
    unittest.main()
