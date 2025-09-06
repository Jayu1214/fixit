"""
Setup script for distributing FixIt as a Python package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="fixit-installer",
    version="1.0.0",
    author="FixIt Team",
    author_email="team@fixit.dev",
    description="Cross-platform software installation framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jayu1214/fixit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Installation/Setup",
        "Topic :: System :: Software Distribution",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fixit=fixit:main",
        ],
    },
    scripts=["fixit.py"],
    include_package_data=True,
    package_data={
        "": ["registry/*.json"],
    },
    project_urls={
        "Bug Reports": "https://github.com/Jayu1214/fixit/issues",
        "Source": "https://github.com/Jayu1214/fixit",
        "Documentation": "https://github.com/Jayu1214/fixit/wiki",
    },
)
