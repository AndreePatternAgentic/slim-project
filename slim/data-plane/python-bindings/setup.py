#!/usr/bin/env python3
"""
Setup script for SLIM Python bindings
"""

from setuptools import setup, find_packages

setup(
    name="slim-bindings",
    version="0.1.0",
    description="SLIM (Secure Low-Latency Interactive Messaging) Python bindings",
    author="AGNTCY Contributors",
    author_email="contributors@agntcy.com",
    url="https://github.com/agntcy/slim",
    packages=find_packages(),
    package_data={
        'slim_bindings': ['*.so', '*.pyd', '*.dll'],  # Include compiled binaries
    },
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - the bindings are self-contained
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Networking",
    ],
)