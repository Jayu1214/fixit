"""
Test registry functionality
"""

import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.registry import Registry

class TestRegistry(unittest.TestCase):
    """Test registry functionality"""
    
    def setUp(self):
        self.registry = Registry()
    
    def test_software_exists(self):
        """Test software existence check"""
        self.assertTrue(self.registry.software_exists('mongodb'))
        self.assertTrue(self.registry.software_exists('nodejs'))
        self.assertFalse(self.registry.software_exists('nonexistent'))
    
    def test_get_software(self):
        """Test getting software information"""
        mongodb = self.registry.get_software('mongodb')
        self.assertIsNotNone(mongodb)
        self.assertEqual(mongodb['name'], 'MongoDB')
    
    def test_list_software(self):
        """Test listing all software"""
        software_list = self.registry.list_software()
        self.assertIsInstance(software_list, list)
        self.assertIn('mongodb', software_list)
        self.assertIn('nodejs', software_list)
    
    def test_get_platform_info(self):
        """Test getting platform-specific information"""
        windows_info = self.registry.get_platform_info('mongodb', 'windows')
        self.assertIsNotNone(windows_info)
        self.assertIn('download_url', windows_info)
        self.assertIn('install_command', windows_info)
    
    def test_get_latest_version(self):
        """Test getting latest version"""
        version = self.registry.get_latest_version('mongodb')
        self.assertIsNotNone(version)
        self.assertIsInstance(version, str)

if __name__ == '__main__':
    unittest.main()
