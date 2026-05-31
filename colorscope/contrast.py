#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core contrast calculation engine implementing WCAG 2.1 standards.
核心对比度计算引擎，实现WCAG 2.1标准
"""

import re
import math
from dataclasses import dataclass
from typing import Tuple, Optional, List, Union
from enum import Enum


class WCAGLevel(Enum):
    """WCAG compliance levels"""
    FAIL = "fail"
    AA_LARGE = "AA Large"
    AA = "AA"
    AAA = "AAA"


@dataclass
class Color:
    """
    RGB Color representation with conversion utilities.
    RGB颜色表示，包含转换工具
    """
    r: int  # 0-255
    g: int  # 0-255
    b: int  # 0-255
    
    def __post_init__(self):
        """Validate RGB values"""
        for val in [self.r, self.g, self.b]:
            if not 0 <= val <= 255:
                raise ValueError(f"RGB values must be between 0 and 255, got {val}")
    
    @classmethod
    def from_hex(cls, hex_color: str) -> "Color":
        """
        Create Color from hex string.
        从十六进制字符串创建颜色
        
        Args:
            hex_color: Hex color string (e.g., "#FF5733", "FF5733", "#fff")
        
        Returns:
            Color instance
        """
        # Remove # if present
        hex_color = hex_color.lstrip("#")
        
        # Handle shorthand hex (e.g., "fff" -> "ffffff")
        if len(hex_color) == 3:
            hex_color = "".join([c * 2 for c in hex_color])
        
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: #{hex_color}")
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return cls(r, g, b)
    
    @classmethod
    def from_rgb(cls, r: int, g: int, b: int) -> "Color":
        """Create Color from RGB values"""
        return cls(r, g, b)
    
    @classmethod
    def from_rgb_tuple(cls, rgb: Tuple[int, int, int]) -> "Color":
        """Create Color from RGB tuple"""
        return cls(rgb[0], rgb[1], rgb[2])
    
    def to_hex(self, include_hash: bool = True) -> str:
        """Convert to hex string"""
        hex_str = f"{self.r:02X}{self.g:02X}{self.b:02X}"
        return f"#{hex_str}" if include_hash else hex_str
    
    def to_rgb(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple"""
        return (self.r, self.g, self.b)
    
    def to_hsl(self) -> Tuple[float, float, float]:
        """
        Convert RGB to HSL.
        将RGB转换为HSL
        
        Returns:
            Tuple of (hue, saturation, lightness) where hue is 0-360, others are 0-100
        """
        r, g, b = self.r / 255, self.g / 255, self.b / 255
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        diff = max_val - min_val
        
        # Lightness
        l = (max_val + min_val) / 2
        
        # Saturation
        if diff == 0:
            s = 0
            h = 0
        else:
            s = diff / (1 - abs(2 * l - 1))
            
            # Hue
            if max_val == r:
                h = (60 * ((g - b) / diff) + 360) % 360
            elif max_val == g:
                h = 60 * ((b - r) / diff) + 120
            else:
                h = 60 * ((r - g) / diff) + 240
        
        return (h, s * 100, l * 100)
    
    @classmethod
    def from_hsl(cls, h: float, s: float, l: float) -> "Color":
        """
        Create Color from HSL values.
        从HSL值创建颜色
        
        Args:
            h: Hue (0-360)
            s: Saturation (0-100)
            l: Lightness (0-100)
        """
        s /= 100
        l /= 100
        
        if s == 0:
            r = g = b = l
        else:
            def hue_to_rgb(p, q, t):
                if t < 0:
                    t += 1
                if t > 1:
                    t -= 1
                if t < 1/6:
                    return p + (q - p) * 6 * t
                if t < 1/2:
                    return q
                if t < 2/3:
                    return p + (q - p) * (2/3 - t) * 6
                return p
            
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            
            r = hue_to_rgb(p, q, h/360 + 1/3)
            g = hue_to_rgb(p, q, h/360)
            b = hue_to_rgb(p, q, h/360 - 1/3)
        
        return cls(int(r * 255), int(g * 255), int(b * 255))
    
    def get_luminance(self) -> float:
        """
        Calculate relative luminance according to WCAG 2.1.
        根据WCAG 2.1计算相对亮度
        
        Returns:
            Relative luminance (0.0 - 1.0)
        """
        def adjust(c):
            c = c / 255
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
        
        r, g, b = adjust(self.r), adjust(self.g), adjust(self.b)
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    def __str__(self) -> str:
        return self.to_hex()
    
    def __repr__(self) -> str:
        return f"Color(r={self.r}, g={self.g}, b={self.b}, hex={self.to_hex()})"


@dataclass
class ContrastResult:
    """
    Result of contrast ratio calculation.
    对比度计算结果
    """
    foreground: Color
    background: Color
    ratio: float
    wcag_level: WCAGLevel
    aa_normal: bool
    aa_large: bool
    aaa_normal: bool
    aaa_large: bool
    
    def is_accessible(self, level: WCAGLevel = WCAGLevel.AA) -> bool:
        """Check if the contrast meets specified WCAG level"""
        if level == WCAGLevel.AA:
            return self.aa_normal
        elif level == WCAGLevel.AA_LARGE:
            return self.aa_large
        elif level == WCAGLevel.AAA:
            return self.aaa_normal
        elif level == WCAGLevel.FAIL:
            return False
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "foreground": self.foreground.to_hex(),
            "background": self.background.to_hex(),
            "ratio": round(self.ratio, 2),
            "wcag_level": self.wcag_level.value,
            "aa_normal": self.aa_normal,
            "aa_large": self.aa_large,
            "aaa_normal": self.aaa_normal,
            "aaa_large": self.aaa_large,
        }


class ContrastChecker:
    """
    WCAG 2.1 Contrast Ratio Checker.
    WCAG 2.1对比度检查器
    
    Implements the contrast ratio calculation as defined in:
    https://www.w3.org/TR/WCAG21/#contrast-minimum
    """
    
    # WCAG 2.1 contrast ratio thresholds
    RATIO_AA_NORMAL = 4.5    # AA for normal text
    RATIO_AA_LARGE = 3.0     # AA for large text (18pt or 14pt bold)
    RATIO_AAA_NORMAL = 7.0   # AAA for normal text
    RATIO_AAA_LARGE = 4.5    # AAA for large text
    
    def __init__(self):
        pass
    
    def calculate_ratio(self, fg: Color, bg: Color) -> float:
        """
        Calculate contrast ratio between two colors.
        计算两个颜色之间的对比度
        
        Args:
            fg: Foreground color
            bg: Background color
        
        Returns:
            Contrast ratio (1:1 to 21:1)
        """
        l1 = fg.get_luminance()
        l2 = bg.get_luminance()
        
        # Ensure l1 is the lighter color
        if l1 < l2:
            l1, l2 = l2, l1
        
        # WCAG contrast ratio formula
        ratio = (l1 + 0.05) / (l2 + 0.05)
        
        return ratio
    
    def check(self, fg: Union[Color, str, Tuple[int, int, int]], 
              bg: Union[Color, str, Tuple[int, int, int]]) -> ContrastResult:
        """
        Check contrast ratio between two colors.
        检查两个颜色之间的对比度
        
        Args:
            fg: Foreground color (Color, hex string, or RGB tuple)
            bg: Background color (Color, hex string, or RGB tuple)
        
        Returns:
            ContrastResult with detailed information
        """
        # Convert to Color objects
        fg_color = self._to_color(fg)
        bg_color = self._to_color(bg)
        
        # Calculate ratio
        ratio = self.calculate_ratio(fg_color, bg_color)
        
        # Determine WCAG compliance
        aa_normal = ratio >= self.RATIO_AA_NORMAL
        aa_large = ratio >= self.RATIO_AA_LARGE
        aaa_normal = ratio >= self.RATIO_AAA_NORMAL
        aaa_large = ratio >= self.RATIO_AAA_LARGE
        
        # Determine overall level
        if aaa_normal:
            level = WCAGLevel.AAA
        elif aa_normal:
            level = WCAGLevel.AA
        elif aa_large:
            level = WCAGLevel.AA_LARGE
        else:
            level = WCAGLevel.FAIL
        
        return ContrastResult(
            foreground=fg_color,
            background=bg_color,
            ratio=ratio,
            wcag_level=level,
            aa_normal=aa_normal,
            aa_large=aa_large,
            aaa_normal=aaa_normal,
            aaa_large=aaa_large,
        )
    
    def check_batch(self, color_pairs: List[Tuple]) -> List[ContrastResult]:
        """
        Check multiple color pairs.
        批量检查多个颜色对
        
        Args:
            color_pairs: List of (foreground, background) tuples
        
        Returns:
            List of ContrastResult objects
        """
        return [self.check(fg, bg) for fg, bg in color_pairs]
    
    def _to_color(self, color: Union[Color, str, Tuple[int, int, int]]) -> Color:
        """Convert various color formats to Color object"""
        if isinstance(color, Color):
            return color
        elif isinstance(color, str):
            return Color.from_hex(color)
        elif isinstance(color, tuple):
            return Color.from_rgb_tuple(color)
        else:
            raise ValueError(f"Unsupported color format: {type(color)}")
    
    @staticmethod
    def get_required_ratio(level: str = "aa", is_large_text: bool = False) -> float:
        """
        Get required contrast ratio for a WCAG level.
        获取指定WCAG级别所需的对比度
        
        Args:
            level: WCAG level ("aa" or "aaa")
            is_large_text: Whether the text is large (18pt+ or 14pt bold)
        
        Returns:
            Required contrast ratio
        """
        level = level.lower()
        
        if level == "aaa":
            return ContrastChecker.RATIO_AAA_LARGE if is_large_text else ContrastChecker.RATIO_AAA_NORMAL
        else:  # aa
            return ContrastChecker.RATIO_AA_LARGE if is_large_text else ContrastChecker.RATIO_AA_NORMAL
