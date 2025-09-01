"""
Bilibili Content Analyzer - A comprehensive data analysis tool for Bilibili content.

This package provides tools for collecting, analyzing, and visualizing
Bilibili video content data with a focus on productivity-related topics.
"""

__version__ = "1.0.0"
__author__ = "Bilibili Content Analyzer Contributors"
__email__ = "contributors@example.com"

from .config import (
    BILIBILI_SEARCH_API,
    SEARCH_KEYWORDS,
    DATE_RANGE,
    DATA_STORAGE,
    ANALYSIS_CONFIG,
    VISUALIZATION_CONFIG,
    OUTPUT_CONFIG,
)

from .data_analyzer import DataAnalyzer
from .visualizer import Visualizer
from .font_utils import setup_chinese_font, get_available_chinese_fonts, print_font_info, create_font_test_chart

__all__ = [
    "DataAnalyzer",
    "Visualizer", 
    "setup_chinese_font",
    "get_available_chinese_fonts",
    "print_font_info",
    "create_font_test_chart",
    "BILIBILI_SEARCH_API",
    "SEARCH_KEYWORDS",
    "DATE_RANGE",
    "DATA_STORAGE",
    "ANALYSIS_CONFIG",
    "VISUALIZATION_CONFIG",
    "OUTPUT_CONFIG",
]