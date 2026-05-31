#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for ColorScope contrast module.
"""

import pytest
from colorscope.contrast import Color, ContrastChecker, WCAGLevel, ContrastResult


class TestColor:
    """Tests for Color class"""
    
    def test_from_hex_with_hash(self):
        """Test creating color from hex with hash"""
        color = Color.from_hex("#FF5733")
        assert color.r == 255
        assert color.g == 87
        assert color.b == 51
    
    def test_from_hex_without_hash(self):
        """Test creating color from hex without hash"""
        color = Color.from_hex("FF5733")
        assert color.r == 255
        assert color.g == 87
        assert color.b == 51
    
    def test_from_hex_shorthand(self):
        """Test creating color from shorthand hex"""
        color = Color.from_hex("#FFF")
        assert color.r == 255
        assert color.g == 255
        assert color.b == 255
    
    def test_from_rgb(self):
        """Test creating color from RGB values"""
        color = Color.from_rgb(255, 87, 51)
        assert color.r == 255
        assert color.g == 87
        assert color.b == 51
    
    def test_to_hex(self):
        """Test converting color to hex"""
        color = Color(255, 87, 51)
        assert color.to_hex() == "#FF5733"
        assert color.to_hex(include_hash=False) == "FF5733"
    
    def test_to_rgb(self):
        """Test converting color to RGB tuple"""
        color = Color(255, 87, 51)
        assert color.to_rgb() == (255, 87, 51)
    
    def test_to_hsl(self):
        """Test converting color to HSL"""
        color = Color(255, 0, 0)  # Pure red
        h, s, l = color.to_hsl()
        assert h == 0
        assert s == 100
        assert l == 50
    
    def test_from_hsl(self):
        """Test creating color from HSL"""
        color = Color.from_hsl(0, 100, 50)  # Pure red
        assert color.r == 255
        assert color.g == 0
        assert color.b == 0
    
    def test_get_luminance_black(self):
        """Test luminance of pure black"""
        color = Color(0, 0, 0)
        assert color.get_luminance() == 0.0
    
    def test_get_luminance_white(self):
        """Test luminance of pure white"""
        color = Color(255, 255, 255)
        assert color.get_luminance() == 1.0
    
    def test_invalid_rgb_value(self):
        """Test that invalid RGB values raise error"""
        with pytest.raises(ValueError):
            Color(300, 0, 0)


class TestContrastChecker:
    """Tests for ContrastChecker class"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.checker = ContrastChecker()
    
    def test_black_white_contrast(self):
        """Test contrast between black and white (should be 21:1)"""
        result = self.checker.check("#000000", "#FFFFFF")
        assert result.ratio == pytest.approx(21.0, rel=0.01)
    
    def test_same_color_contrast(self):
        """Test contrast between same colors (should be 1:1)"""
        result = self.checker.check("#FF5733", "#FF5733")
        assert result.ratio == pytest.approx(1.0, rel=0.01)
    
    def test_wcag_aa_pass(self):
        """Test WCAG AA compliance for high contrast"""
        result = self.checker.check("#000000", "#FFFFFF")
        assert result.aa_normal is True
        assert result.aa_large is True
    
    def test_wcag_aa_fail(self):
        """Test WCAG AA non-compliance for low contrast"""
        result = self.checker.check("#777777", "#888888")
        assert result.aa_normal is False
    
    def test_wcag_aaa_pass(self):
        """Test WCAG AAA compliance for very high contrast"""
        result = self.checker.check("#000000", "#FFFFFF")
        assert result.aaa_normal is True
    
    def test_wcag_aaa_fail(self):
        """Test WCAG AAA non-compliance"""
        # This should pass AA but fail AAA
        result = self.checker.check("#767676", "#FFFFFF")
        assert result.aa_normal is True
        assert result.aaa_normal is False
    
    def test_check_with_string_colors(self):
        """Test checking with hex string colors"""
        result = self.checker.check("#FF5733", "#FFFFFF")
        assert isinstance(result, ContrastResult)
    
    def test_check_with_tuple_colors(self):
        """Test checking with RGB tuple colors"""
        result = self.checker.check((255, 87, 51), (255, 255, 255))
        assert isinstance(result, ContrastResult)
    
    def test_check_with_color_objects(self):
        """Test checking with Color objects"""
        fg = Color(255, 87, 51)
        bg = Color(255, 255, 255)
        result = self.checker.check(fg, bg)
        assert isinstance(result, ContrastResult)
    
    def test_batch_check(self):
        """Test batch checking multiple color pairs"""
        pairs = [
            ("#000000", "#FFFFFF"),
            ("#FF5733", "#FFFFFF"),
            ("#767676", "#FFFFFF"),
        ]
        results = self.checker.check_batch(pairs)
        assert len(results) == 3
        assert all(isinstance(r, ContrastResult) for r in results)
    
    def test_get_required_ratio_aa_normal(self):
        """Test getting required ratio for AA normal text"""
        ratio = ContrastChecker.get_required_ratio("aa", False)
        assert ratio == 4.5
    
    def test_get_required_ratio_aa_large(self):
        """Test getting required ratio for AA large text"""
        ratio = ContrastChecker.get_required_ratio("aa", True)
        assert ratio == 3.0
    
    def test_get_required_ratio_aaa_normal(self):
        """Test getting required ratio for AAA normal text"""
        ratio = ContrastChecker.get_required_ratio("aaa", False)
        assert ratio == 7.0


class TestContrastResult:
    """Tests for ContrastResult class"""
    
    def test_is_accessible_aa(self):
        """Test is_accessible method for AA level"""
        checker = ContrastChecker()
        result = checker.check("#000000", "#FFFFFF")
        assert result.is_accessible(WCAGLevel.AA) is True
    
    def test_is_accessible_aaa(self):
        """Test is_accessible method for AAA level"""
        checker = ContrastChecker()
        result = checker.check("#000000", "#FFFFFF")
        assert result.is_accessible(WCAGLevel.AAA) is True
    
    def test_to_dict(self):
        """Test converting result to dictionary"""
        checker = ContrastChecker()
        result = checker.check("#000000", "#FFFFFF")
        d = result.to_dict()
        
        assert "foreground" in d
        assert "background" in d
        assert "ratio" in d
        assert "wcag_level" in d
        assert "aa_normal" in d
        assert "aaa_normal" in d


class TestWCAGLevel:
    """Tests for WCAGLevel enum"""
    
    def test_level_values(self):
        """Test WCAGLevel enum values"""
        assert WCAGLevel.FAIL.value == "fail"
        assert WCAGLevel.AA_LARGE.value == "AA Large"
        assert WCAGLevel.AA.value == "AA"
        assert WCAGLevel.AAA.value == "AAA"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
