#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fashion Advisor - Quick Launch Script
"""

import sys
import os

# Ensure we're in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Add script directory to path
sys.path.insert(0, script_dir)

# Import and run main application
from main import main

if __name__ == "__main__":
    main()
