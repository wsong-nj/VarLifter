#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:53:08 2024

@author: lyc
"""

from setuptools import setup

setup(
    name="VarLifter",
    version="1.0.0",
    py_modules=["main", "gui"],
    entry_points={
        "console_scripts": [
            "VarLifter=main:main",
        ],
        "gui_scripts": [
            "VarLifter_gui=gui:main",
        ],
    },
    install_requires=[
     
        # 'numpy', 'requests'
    ],
)



