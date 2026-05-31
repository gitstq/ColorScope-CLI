#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Color suggestion engine for improving accessibility.
颜色建议引擎，用于改善可访问性

Provides intelligent suggestions for adjusting colors to meet WCAG requirements.
提供智能建议来调整颜色以满足WCAG要求
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import math

from .contrast import Color, ContrastChecker, WCAGLevel


@dataclass
class ColorSuggestion:
    """A suggested color adjustment"""
    original: Color
    suggested: Color
    adjustment: str
    new_ratio: float
    wcag_level: WCAGLevel
    
    def to_dict(self) -> dict:
        return {
            "original": self.original.to_hex(),
            "suggested": self.suggested.to_hex(),
            "adjustment": self.adjustment,
            "new_ratio": round(self.new_ratio, 2),
            "wcag_level": self.wcag_level.value,
        }


class ColorSuggester:
    """
    Intelligent color suggestion engine.
    智能颜色建议引擎
    
    Provides suggestions for adjusting colors to meet WCAG contrast requirements.
    """
    
    def __init__(self):
        self.checker = ContrastChecker()
    
    def suggest_foreground(self, fg: Color, bg: Color, 
                           target_level: WCAGLevel = WCAGLevel.AA,
                           max_iterations: int = 50) -> List[ColorSuggestion]:
        """
        Suggest foreground color adjustments to meet target WCAG level.
        建议前景色调整以满足目标WCAG级别
        
        Args:
            fg: Original foreground color
            bg: Background color (fixed)
            target_level: Target WCAG level
            max_iterations: Maximum number of iterations
        
        Returns:
            List of color suggestions
        """
        suggestions = []
        target_ratio = self._get_target_ratio(target_level)
        
        # Get current ratio
        current_result = self.checker.check(fg, bg)
        
        if current_result.ratio >= target_ratio:
            return [ColorSuggestion(
                original=fg,
                suggested=fg,
                adjustment="No adjustment needed - already meets target",
                new_ratio=current_result.ratio,
                wcag_level=current_result.wcag_level,
            )]
        
        # Determine if we need to darken or lighten
        fg_luminance = fg.get_luminance()
        bg_luminance = bg.get_luminance()
        
        if fg_luminance > bg_luminance:
            # Foreground is lighter, we need to make it even lighter
            suggestions.extend(self._lighten_suggestions(fg, bg, target_ratio, max_iterations))
        else:
            # Foreground is darker, we need to make it even darker
            suggestions.extend(self._darken_suggestions(fg, bg, target_ratio, max_iterations))
        
        return suggestions
    
    def suggest_background(self, fg: Color, bg: Color,
                           target_level: WCAGLevel = WCAGLevel.AA,
                           max_iterations: int = 50) -> List[ColorSuggestion]:
        """
        Suggest background color adjustments to meet target WCAG level.
        建议背景色调整以满足目标WCAG级别
        
        Args:
            fg: Foreground color (fixed)
            bg: Original background color
            target_level: Target WCAG level
            max_iterations: Maximum number of iterations
        
        Returns:
            List of color suggestions
        """
        suggestions = []
        target_ratio = self._get_target_ratio(target_level)
        
        # Get current ratio
        current_result = self.checker.check(fg, bg)
        
        if current_result.ratio >= target_ratio:
            return [ColorSuggestion(
                original=bg,
                suggested=bg,
                adjustment="No adjustment needed - already meets target",
                new_ratio=current_result.ratio,
                wcag_level=current_result.wcag_level,
            )]
        
        # Determine if we need to darken or lighten
        fg_luminance = fg.get_luminance()
        bg_luminance = bg.get_luminance()
        
        if bg_luminance > fg_luminance:
            # Background is lighter, we need to make it even lighter
            suggestions.extend(self._lighten_suggestions(bg, fg, target_ratio, max_iterations, is_bg=True))
        else:
            # Background is darker, we need to make it even darker
            suggestions.extend(self._darken_suggestions(bg, fg, target_ratio, max_iterations, is_bg=True))
        
        return suggestions
    
    def suggest_both(self, fg: Color, bg: Color,
                     target_level: WCAGLevel = WCAGLevel.AA) -> List[Tuple[ColorSuggestion, ColorSuggestion]]:
        """
        Suggest adjustments for both foreground and background.
        建议同时调整前景色和背景色
        
        Args:
            fg: Original foreground color
            bg: Original background color
            target_level: Target WCAG level
        
        Returns:
            List of (foreground_suggestion, background_suggestion) tuples
        """
        suggestions = []
        target_ratio = self._get_target_ratio(target_level)
        
        # Try adjusting foreground first
        fg_suggestions = self.suggest_foreground(fg, bg, target_level)
        
        # Try adjusting background
        bg_suggestions = self.suggest_background(fg, bg, target_level)
        
        # Combine suggestions
        for i, fg_sug in enumerate(fg_suggestions[:3]):
            for j, bg_sug in enumerate(bg_suggestions[:3]):
                if i + j > 0:  # Skip both unchanged
                    suggestions.append((fg_sug, bg_sug))
        
        return suggestions[:5]  # Return top 5 combinations
    
    def _lighten_suggestions(self, color: Color, other: Color, 
                             target_ratio: float, max_iterations: int,
                             is_bg: bool = False) -> List[ColorSuggestion]:
        """Generate suggestions by lightening the color"""
        suggestions = []
        
        # Convert to HSL for easier manipulation
        h, s, l = color.to_hsl()
        
        # Try progressively lighter values
        for step in [5, 10, 15, 20, 25, 30, 40, 50]:
            new_l = min(100, l + step)
            new_color = Color.from_hsl(h, s, new_l)
            
            if is_bg:
                result = self.checker.check(other, new_color)
            else:
                result = self.checker.check(new_color, other)
            
            suggestion = ColorSuggestion(
                original=color,
                suggested=new_color,
                adjustment=f"Lightened by {step}% (L: {l:.1f} → {new_l:.1f})",
                new_ratio=result.ratio,
                wcag_level=result.wcag_level,
            )
            suggestions.append(suggestion)
            
            if result.ratio >= target_ratio:
                break
        
        return suggestions
    
    def _darken_suggestions(self, color: Color, other: Color,
                            target_ratio: float, max_iterations: int,
                            is_bg: bool = False) -> List[ColorSuggestion]:
        """Generate suggestions by darkening the color"""
        suggestions = []
        
        # Convert to HSL for easier manipulation
        h, s, l = color.to_hsl()
        
        # Try progressively darker values
        for step in [5, 10, 15, 20, 25, 30, 40, 50]:
            new_l = max(0, l - step)
            new_color = Color.from_hsl(h, s, new_l)
            
            if is_bg:
                result = self.checker.check(other, new_color)
            else:
                result = self.checker.check(new_color, other)
            
            suggestion = ColorSuggestion(
                original=color,
                suggested=new_color,
                adjustment=f"Darkened by {step}% (L: {l:.1f} → {new_l:.1f})",
                new_ratio=result.ratio,
                wcag_level=result.wcag_level,
            )
            suggestions.append(suggestion)
            
            if result.ratio >= target_ratio:
                break
        
        return suggestions
    
    def get_accessible_alternatives(self, fg: Color, bg: Color,
                                    target_level: WCAGLevel = WCAGLevel.AA) -> dict:
        """
        Get all accessible color alternatives.
        获取所有可访问的颜色替代方案
        
        Args:
            fg: Original foreground color
            bg: Original background color
            target_level: Target WCAG level
        
        Returns:
            Dictionary with all suggestions
        """
        return {
            "foreground_suggestions": [s.to_dict() for s in self.suggest_foreground(fg, bg, target_level)],
            "background_suggestions": [s.to_dict() for s in self.suggest_background(fg, bg, target_level)],
            "combined_suggestions": [
                {"foreground": fg.to_dict(), "background": bg.to_dict()}
                for fg, bg in self.suggest_both(fg, bg, target_level)
            ],
        }
    
    def _get_target_ratio(self, level: WCAGLevel) -> float:
        """Get target contrast ratio for WCAG level"""
        ratios = {
            WCAGLevel.AA_LARGE: 3.0,
            WCAGLevel.AA: 4.5,
            WCAGLevel.AAA: 7.0,
        }
        return ratios.get(level, 4.5)
    
    @staticmethod
    def generate_accessible_palette(base_color: Color, 
                                    target_level: WCAGLevel = WCAGLevel.AA) -> List[Color]:
        """
        Generate an accessible color palette based on a base color.
        基于基础颜色生成可访问的颜色调色板
        
        Args:
            base_color: Base color for the palette
            target_level: Target WCAG level
        
        Returns:
            List of accessible colors
        """
        h, s, l = base_color.to_hsl()
        palette = []
        
        # Generate colors with different lightness values
        for lightness in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
            color = Color.from_hsl(h, s, lightness)
            palette.append(color)
        
        # Generate colors with different saturation values
        for saturation in [20, 40, 60, 80, 100]:
            color = Color.from_hsl(h, saturation, l)
            palette.append(color)
        
        return palette
