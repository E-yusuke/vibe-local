#!/usr/bin/env python3
"""
Setup script for vibe-local Windows application.
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'VIBE_LOCAL_README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vibe-local',
    version='1.0.0',
    description='Local AI chat for Windows with SQLite and Excel support',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='vibe-local Contributors',
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'pandas>=1.5.0',
        'openpyxl>=3.8.0',
    ],
    py_modules=['vibe_local_chat', 'llm_client', 'local_tools'],
    entry_points={
        'console_scripts': [
            'vibe-local=vibe_local_chat:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
