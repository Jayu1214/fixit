#!/usr/bin/env python3
"""
Easy Installer - Cross-platform software installation framework
Main CLI entry point
"""

import argparse
import sys
import os
from src.core.installer import Installer
from src.utils.logger import setup_logger

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Easy Installer - Cross-platform software installation framework",
        prog="easy-installer"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available software")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install software")
    install_parser.add_argument("software", help="Software name to install")
    install_parser.add_argument("--version", help="Specific version to install")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove software")
    remove_parser.add_argument("software", help="Software name to remove")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update software")
    update_parser.add_argument("software", nargs="?", help="Software name to update (updates all if not specified)")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Get software information")
    info_parser.add_argument("software", help="Software name to get info about")
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Setup logger
    logger = setup_logger()
    
    try:
        installer = Installer(logger)
        
        if args.command == "list":
            installer.list_software()
        elif args.command == "install":
            installer.install_software(args.software, args.version)
        elif args.command == "remove":
            installer.remove_software(args.software)
        elif args.command == "update":
            if args.software:
                installer.update_software(args.software)
            else:
                installer.update_all_software()
        elif args.command == "info":
            installer.get_software_info(args.software)
        elif args.command == "version":
            print("Easy Installer version 1.0.1")
            print("Cross-platform software installation framework")
    
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
