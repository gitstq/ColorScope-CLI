#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color blindness simulation module.
色盲模拟模块

Simulates how colors appear to people with different types of color blindness.
模拟不同类型色盲人群看到的颜色效果
"""

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional
import math

from .contrast import Color


class ColorBlindnessType(Enum):
    """Types of color blindness"""
    PROTANOPIA = "protanopia"        # Red blindness (红绿色盲-红色盲)
    DEUTERANOPIA = "deuteranopia"    # Green blindness (红绿色盲-绿色盲)
    TRITANOPIA = "tritanopia"        # Blue blindness (蓝黄色盲)
    ACHROMATOPSIA = "achromatopsia"  # Total color blindness (全色盲)
    PROTANOMALY = "protanomaly"      # Red weakness (红色弱)
    DEUTERANOMALY = "deuteranomaly"  # Green weakness (绿色弱，最常见)
    TRITANOMALY = "tritanomaly"      # Blue weakness (蓝色弱)


@dataclass
class SimulationResult:
    """Result of color blindness simulation"""
    original: Color
    simulated: Color
    blindness_type: ColorBlindnessType
    description: str
    
    def to_dict(self) -> dict:
        return {
            "original": self.original.to_hex(),
            "simulated": self.simulated.to_hex(),
            "blindness_type": self.blindness_type.value,
            "description": self.description,
        }


class ColorBlindnessSimulator:
    """
    Simulates color blindness using color space transformation matrices.
    使用色彩空间变换矩阵模拟色盲效果
    
    Based on the work of:
    - Brettel, Viénot & Mollon (1997)
    - Viénot, Brettel & Mollon (1999)
    - Machado, Oliveira & Fernandes (2009)
    """
    
    # Color blindness simulation matrices (RGB to RGB transformation)
    # Based on Machado et al. (2009) simulation matrices
    
    # Protanopia (no red cones)
    PROTANOPIA_MATRIX = [
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758],
    ]
    
    # Deuteranopia (no green cones) - most common
    DEUTERANOPIA_MATRIX = [
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700],
    ]
    
    # Tritanopia (no blue cones)
    TRITANOPIA_MATRIX = [
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525],
    ]
    
    # Protanomaly (reduced red sensitivity)
    PROTANOMALY_MATRIX = [
        [0.817, 0.183, 0.000],
        [0.333, 0.667, 0.000],
        [0.000, 0.125, 0.875],
    ]
    
    # Deuteranomaly (reduced green sensitivity) - most common
    DEUTERANOMALY_MATRIX = [
        [0.800, 0.200, 0.000],
        [0.258, 0.742, 0.000],
        [0.000, 0.142, 0.858],
    ]
    
    # Tritanomaly (reduced blue sensitivity)
    TRITANOMALY_MATRIX = [
        [0.967, 0.033, 0.000],
        [0.000, 0.733, 0.267],
        [0.000, 0.183, 0.817],
    ]
    
    # Achromatopsia (no color perception - grayscale)
    ACHROMATOPSIA_MATRIX = [
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114],
    ]
    
    # Descriptions for each type
    DESCRIPTIONS = {
        ColorBlindnessType.PROTANOPIA: "红绿色盲（红色盲）- 无法区分红色，约占男性的1%",
        ColorBlindnessType.DEUTERANOPIA: "红绿色盲（绿色盲）- 无法区分绿色，约占男性的1%",
        ColorBlindnessType.TRITANOPIA: "蓝黄色盲 - 无法区分蓝色和黄色，非常罕见",
        ColorBlindnessType.ACHROMATOPSIA: "全色盲 - 只能看到灰度，极为罕见",
        ColorBlindnessType.PROTANOMALY: "红色弱 - 红色感知减弱，约占男性的1%",
        ColorBlindnessType.DEUTERANOMALY: "绿色弱 - 绿色感知减弱，最常见的色盲类型，约占男性的5%",
        ColorBlindnessType.TRITANOMALY: "蓝色弱 - 蓝色感知减弱，非常罕见",
    }
    
    ENGLISH_DESCRIPTIONS = {
        ColorBlindnessType.PROTANOPIA: "Protanopia - Red blindness, affects ~1% of males",
        ColorBlindnessType.DEUTERANOPIA: "Deuteranopia - Green blindness, affects ~1% of males",
        ColorBlindnessType.TRITANOPIA: "Tritanopia - Blue blindness, very rare",
        ColorBlindnessType.ACHROMATOPSIA: "Achromatopsia - Total color blindness, extremely rare",
        ColorBlindnessType.PROTANOMALY: "Protanomaly - Reduced red sensitivity, affects ~1% of males",
        ColorBlindnessType.DEUTERANOMALY: "Deuteranomaly - Reduced green sensitivity, most common type (~5% of males)",
        ColorBlindnessType.TRITANOMALY: "Tritanomaly - Reduced blue sensitivity, very rare",
    }
    
    def __init__(self, language: str = "zh"):
        """
        Initialize the simulator.
        
        Args:
            language: Language for descriptions ("zh" or "en")
        """
        self.language = language
        self.descriptions = self.DESCRIPTIONS if language == "zh" else self.ENGLISH_DESCRIPTIONS
    
    def simulate(self, color: Color, blindness_type: ColorBlindnessType) -> SimulationResult:
        """
        Simulate how a color appears to someone with color blindness.
        模拟色盲人群看到的颜色
        
        Args:
            color: Original color
            blindness_type: Type of color blindness to simulate
        
        Returns:
            SimulationResult with original and simulated colors
        """
        # Get the appropriate matrix
        matrix = self._get_matrix(blindness_type)
        
        # Apply transformation
        r = color.r * matrix[0][0] + color.g * matrix[0][1] + color.b * matrix[0][2]
        g = color.r * matrix[1][0] + color.g * matrix[1][1] + color.b * matrix[1][2]
        b = color.r * matrix[2][0] + color.g * matrix[2][1] + color.b * matrix[2][2]
        
        # Clamp values to valid range
        r = max(0, min(255, int(round(r))))
        g = max(0, min(255, int(round(g))))
        b = max(0, min(255, int(round(b))))
        
        simulated = Color(r, g, b)
        
        return SimulationResult(
            original=color,
            simulated=simulated,
            blindness_type=blindness_type,
            description=self.descriptions[blindness_type],
        )
    
    def simulate_all(self, color: Color) -> dict:
        """
        Simulate all types of color blindness.
        模拟所有类型的色盲
        
        Args:
            color: Original color
        
        Returns:
            Dictionary mapping blindness types to simulation results
        """
        results = {}
        for blindness_type in ColorBlindnessType:
            results[blindness_type.value] = self.simulate(color, blindness_type)
        return results
    
    def simulate_pair(self, fg: Color, bg: Color, 
                      blindness_type: ColorBlindnessType) -> Tuple[Color, Color]:
        """
        Simulate color blindness for a foreground/background pair.
        模拟前景色/背景色对的色盲效果
        
        Args:
            fg: Foreground color
            bg: Background color
            blindness_type: Type of color blindness
        
        Returns:
            Tuple of (simulated_fg, simulated_bg)
        """
        fg_result = self.simulate(fg, blindness_type)
        bg_result = self.simulate(bg, blindness_type)
        return (fg_result.simulated, bg_result.simulated)
    
    def _get_matrix(self, blindness_type: ColorBlindnessType) -> list:
        """Get the simulation matrix for a color blindness type"""
        matrices = {
            ColorBlindnessType.PROTANOPIA: self.PROTANOPIA_MATRIX,
            ColorBlindnessType.DEUTERANOPIA: self.DEUTERANOPIA_MATRIX,
            ColorBlindnessType.TRITANOPIA: self.TRITANOPIA_MATRIX,
            ColorBlindnessType.ACHROMATOPSIA: self.ACHROMATOPSIA_MATRIX,
            ColorBlindnessType.PROTANOMALY: self.PROTANOMALY_MATRIX,
            ColorBlindnessType.DEUTERANOMALY: self.DEUTERANOMALY_MATRIX,
            ColorBlindnessType.TRITANOMALY: self.TRITANOMALY_MATRIX,
        }
        return matrices[blindness_type]
    
    @staticmethod
    def get_prevalence(blindness_type: ColorBlindnessType) -> dict:
        """
        Get prevalence statistics for a color blindness type.
        获取色盲类型的流行度统计
        
        Args:
            blindness_type: Type of color blindness
        
        Returns:
            Dictionary with prevalence statistics
        """
        prevalence = {
            ColorBlindnessType.PROTANOPIA: {"males": "1.0%", "females": "0.02%", "total": "~1%"},
            ColorBlindnessType.DEUTERANOPIA: {"males": "1.0%", "females": "0.01%", "total": "~1%"},
            ColorBlindnessType.TRITANOPIA: {"males": "0.01%", "females": "0.01%", "total": "~0.01%"},
            ColorBlindnessType.ACHROMATOPSIA: {"males": "0.003%", "females": "0.002%", "total": "~0.003%"},
            ColorBlindnessType.PROTANOMALY: {"males": "1.0%", "females": "0.02%", "total": "~1%"},
            ColorBlindnessType.DEUTERANOMALY: {"males": "5.0%", "females": "0.4%", "total": "~5%"},
            ColorBlindnessType.TRITANOMALY: {"males": "0.01%", "females": "0.01%", "total": "~0.01%"},
        }
        return prevalence.get(blindness_type, {})
