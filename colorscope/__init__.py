#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ColorScope-CLI - Lightweight Terminal Color Contrast & Accessibility Analysis Engine
轻量级终端颜色对比度检查与可访问性分析引擎

Author: ColorScope Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "ColorScope Team"
__description__ = "Lightweight Terminal Color Contrast & Accessibility Analysis Engine"

from .contrast import ContrastChecker, Color, ContrastResult
from .colorblind import ColorBlindnessSimulator
from .suggestions import ColorSuggester
from .report import ReportGenerator

__all__ = [
    "ContrastChecker",
    "Color",
    "ContrastResult",
    "ColorBlindnessSimulator",
    "ColorSuggester",
    "ReportGenerator",
]
