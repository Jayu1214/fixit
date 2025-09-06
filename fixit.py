#!/usr/bin/env python3
"""
FixIt - Cross-platform software installation framework
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
        description="FixIt - Cross-platform software installation framework",
        prog="fixit"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Install command
    install_parser = subparsers.add_parser("install", help="Install software")
    install_parser.add_argument("software", help="Software to install")
    install_parser.add_argument("--version", help="Specific version to install")
    install_parser.add_argument("--force", action="store_true", help="Force reinstall")
    install_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available software")
    list_parser.add_argument("--installed", action="store_true", help="Show only installed software")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove installed software")
    remove_parser.add_argument("software", help="Software to remove")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update software")
    update_parser.add_argument("software", nargs="?", help="Software to update (all if not specified)")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show software information")
    info_parser.add_argument("software", help="Software to show info for")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Setup logging
    logger = setup_logger(verbose=getattr(args, 'verbose', False))
    
    try:
        installer = Installer(logger)
        
        if args.command == "install":
            return installer.install(args.software, args.version, args.force)
        elif args.command == "list":
            return installer.list_software(args.installed)
        elif args.command == "remove":
            return installer.remove(args.software)
        elif args.command == "update":
            return installer.update(args.software)
        elif args.command == "info":
            return installer.info(args.software)
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if getattr(args, 'verbose', False):
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
