#!/usr/bin/env python3
"""
Responsive Design Validation Script for Research Gap Finder
Validates CSS rules, touch targets, and responsive behavior
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class ResponsiveValidator:
    """Validates responsive design implementation"""
    
    def __init__(self, css_file_path: str = "research_gap_finder.py"):
        self.css_file_path = css_file_path
        self.issues = []
        self.warnings = []
        self.success_count = 0
        
    def extract_css_from_streamlit(self) -> str:
        """Extract CSS content from Streamlit file"""
        try:
            with open(self.css_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract CSS from st.markdown blocks
            css_pattern = r'st\.markdown\(\s*""".*?<style>(.*?)</style>.*?"""\s*,\s*unsafe_allow_html=True\)'
            matches = re.findall(css_pattern, content, re.DOTALL)
            
            if matches:
                return matches[0]  # Return the first (main) CSS block
            else:
                self.issues.append("No CSS found in Streamlit file")
                return ""
                
        except FileNotFoundError:
            self.issues.append(f"File not found: {self.css_file_path}")
            return ""
        except Exception as e:
            self.issues.append(f"Error reading file: {e}")
            return ""
    
    def validate_media_queries(self, css_content: str) -> None:
        """Validate media query breakpoints"""
        print("🔍 Validating Media Queries...")
        
        # Expected breakpoints
        expected_breakpoints = ['768px', '1024px']
        found_breakpoints = []
        
        # Find all media queries
        media_queries = re.findall(r'@media\s*\([^)]+\)\s*{', css_content)
        
        for query in media_queries:
            # Extract pixel values
            pixels = re.findall(r'(\d+)px', query)
            found_breakpoints.extend(pixels)
        
        # Check for expected breakpoints
        for breakpoint in expected_breakpoints:
            if breakpoint.replace('px', '') in found_breakpoints:
                print(f"  ✅ Found breakpoint: {breakpoint}")
                self.success_count += 1
            else:
                self.warnings.append(f"Missing expected breakpoint: {breakpoint}")
        
        # Check for mobile-first approach
        if 'min-width' in css_content:
            print("  ✅ Mobile-first approach detected (min-width queries)")
            self.success_count += 1
        else:
            self.issues.append("No mobile-first media queries found")
    
    def validate_touch_targets(self, css_content: str) -> None:
        """Validate touch target sizes"""
        print("🔍 Validating Touch Targets...")
        
        # Look for button and interactive element sizing
        button_rules = re.findall(r'\.stButton[^}]*min-height:\s*(\d+)px[^}]*}', css_content, re.DOTALL)
        chat_button_rules = re.findall(r'\.stChatInput\s+button[^}]*min-width:\s*(\d+)px[^}]*}', css_content, re.DOTALL)
        
        # Check button min-height (should be >= 44px for iOS)
        for height in button_rules:
            if int(height) >= 44:
                print(f"  ✅ Button min-height: {height}px (iOS compliant)")
                self.success_count += 1
            else:
                self.issues.append(f"Button min-height too small: {height}px (should be ≥44px)")
        
        # Check chat button sizing
        for width in chat_button_rules:
            if int(width) >= 44:
                print(f"  ✅ Chat button min-width: {width}px (iOS compliant)")
                self.success_count += 1
            else:
                self.issues.append(f"Chat button min-width too small: {width}px (should be ≥44px)")
        
        # Check for padding on interactive elements
        if 'padding: 12px' in css_content or 'padding: 0.75rem' in css_content:
            print("  ✅ Adequate padding found on interactive elements")
            self.success_count += 1
        else:
            self.warnings.append("Consider adding more padding to interactive elements")
    
    def validate_font_sizes(self, css_content: str) -> None:
        """Validate font sizes for mobile readability"""
        print("🔍 Validating Font Sizes...")
        
        # Check for 16px font size in inputs (prevents iOS zoom)
        if 'font-size: 16px' in css_content:
            print("  ✅ Found 16px font size (prevents iOS zoom)")
            self.success_count += 1
        else:
            self.warnings.append("Consider using 16px font size for inputs to prevent iOS zoom")
        
        # Check for responsive font sizes
        responsive_font_pattern = r'@media[^}]*font-size:\s*[\d.]+(?:rem|px|em)'
        if re.search(responsive_font_pattern, css_content):
            print("  ✅ Responsive font sizes detected")
            self.success_count += 1
        else:
            self.warnings.append("Consider adding responsive font sizes")
    
    def validate_layout_properties(self, css_content: str) -> None:
        """Validate layout and spacing properties"""
        print("🔍 Validating Layout Properties...")
        
        # Check for flexbox usage
        if 'display: flex' in css_content:
            print("  ✅ Flexbox layout detected")
            self.success_count += 1
        
        # Check for flex-wrap for responsive behavior
        if 'flex-wrap: wrap' in css_content:
            print("  ✅ Flex-wrap found for responsive behavior")
            self.success_count += 1
        else:
            self.warnings.append("Consider using flex-wrap for better responsive behavior")
        
        # Check for word-wrap properties
        if 'word-wrap: break-word' in css_content or 'overflow-wrap: break-word' in css_content:
            print("  ✅ Word wrapping configured")
            self.success_count += 1
        else:
            self.issues.append("Missing word-wrap properties for long text")
        
        # Check for box-sizing
        if 'box-sizing: border-box' in css_content:
            print("  ✅ Box-sizing: border-box found")
            self.success_count += 1
        else:
            self.warnings.append("Consider adding box-sizing: border-box for consistent sizing")
    
    def validate_cross_browser_compatibility(self, css_content: str) -> None:
        """Validate cross-browser compatibility features"""
        print("🔍 Validating Cross-Browser Compatibility...")
        
        # Check for vendor prefixes
        webkit_prefixes = ['-webkit-appearance', '-webkit-tap-highlight-color', '-webkit-touch-callout']
        moz_prefixes = ['-moz-appearance', '-moz-osx-font-smoothing']
        
        webkit_found = any(prefix in css_content for prefix in webkit_prefixes)
        moz_found = any(prefix in css_content for prefix in moz_prefixes)
        
        if webkit_found:
            print("  ✅ WebKit vendor prefixes found")
            self.success_count += 1
        
        if moz_found:
            print("  ✅ Mozilla vendor prefixes found")
            self.success_count += 1
        
        # Check for browser-specific rules
        if '@-moz-document' in css_content:
            print("  ✅ Firefox-specific rules found")
            self.success_count += 1
        
        if '@supports' in css_content:
            print("  ✅ Feature queries (@supports) found")
            self.success_count += 1
    
    def validate_accessibility(self, css_content: str) -> None:
        """Validate accessibility features"""
        print("🔍 Validating Accessibility...")
        
        # Check for focus indicators
        if ':focus' in css_content or 'focus-within' in css_content:
            print("  ✅ Focus indicators found")
            self.success_count += 1
        else:
            self.warnings.append("Consider adding focus indicators for keyboard navigation")
        
        # Check for high contrast considerations
        if 'color:' in css_content and 'background:' in css_content:
            print("  ✅ Color and background properties found")
            self.success_count += 1
    
    def run_validation(self) -> Dict[str, any]:
        """Run all validation checks"""
        print("🚀 Starting Responsive Design Validation...\n")
        
        css_content = self.extract_css_from_streamlit()
        if not css_content:
            return self.get_results()
        
        # Run all validation checks
        self.validate_media_queries(css_content)
        print()
        
        self.validate_touch_targets(css_content)
        print()
        
        self.validate_font_sizes(css_content)
        print()
        
        self.validate_layout_properties(css_content)
        print()
        
        self.validate_cross_browser_compatibility(css_content)
        print()
        
        self.validate_accessibility(css_content)
        print()
        
        return self.get_results()
    
    def get_results(self) -> Dict[str, any]:
        """Get validation results"""
        return {
            'success_count': self.success_count,
            'issues': self.issues,
            'warnings': self.warnings,
            'total_checks': self.success_count + len(self.issues) + len(self.warnings)
        }
    
    def print_summary(self, results: Dict[str, any]) -> None:
        """Print validation summary"""
        print("=" * 60)
        print("📊 VALIDATION SUMMARY")
        print("=" * 60)
        
        print(f"✅ Successful checks: {results['success_count']}")
        print(f"❌ Issues found: {len(results['issues'])}")
        print(f"⚠️  Warnings: {len(results['warnings'])}")
        print(f"📈 Total checks: {results['total_checks']}")
        
        if results['issues']:
            print("\n❌ ISSUES TO FIX:")
            for i, issue in enumerate(results['issues'], 1):
                print(f"  {i}. {issue}")
        
        if results['warnings']:
            print("\n⚠️  WARNINGS:")
            for i, warning in enumerate(results['warnings'], 1):
                print(f"  {i}. {warning}")
        
        if not results['issues']:
            print("\n🎉 No critical issues found! Your responsive design looks good.")
        
        # Calculate score
        if results['total_checks'] > 0:
            score = (results['success_count'] / results['total_checks']) * 100
            print(f"\n📊 Overall Score: {score:.1f}%")
            
            if score >= 90:
                print("🏆 Excellent responsive design implementation!")
            elif score >= 75:
                print("👍 Good responsive design with room for improvement")
            elif score >= 60:
                print("⚠️  Adequate but needs significant improvements")
            else:
                print("❌ Poor responsive design - major fixes needed")

def main():
    """Main function"""
    validator = ResponsiveValidator()
    results = validator.run_validation()
    validator.print_summary(results)
    
    # Exit with error code if critical issues found
    if results['issues']:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
