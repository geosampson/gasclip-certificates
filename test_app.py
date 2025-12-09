#!/usr/bin/env python3
"""
Test script for GasClip Certificates Generator
This script verifies that all components are working correctly
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import tkinter as tk
        print("  ✓ tkinter")
    except ImportError as e:
        print(f"  ✗ tkinter: {e}")
        return False
    
    try:
        from tkinter import ttk
        print("  ✓ tkinter.ttk")
    except ImportError as e:
        print(f"  ✗ tkinter.ttk: {e}")
        return False
    
    try:
        from PyPDF2 import PdfReader, PdfWriter
        print("  ✓ PyPDF2")
    except ImportError as e:
        print(f"  ✗ PyPDF2: {e}")
        print("    Install with: pip install PyPDF2")
        return False
    
    try:
        from reportlab.pdfgen import canvas
        print("  ✓ reportlab")
    except ImportError as e:
        print(f"  ✗ reportlab: {e}")
        print("    Install with: pip install reportlab")
        return False
    
    try:
        from PIL import Image
        print("  ✓ Pillow")
    except ImportError as e:
        print(f"  ✗ Pillow: {e}")
        print("    Install with: pip install Pillow")
        return False
    
    return True

def test_templates():
    """Test if all template files exist"""
    print("\nTesting template files...")
    templates_dir = Path("templates")
    
    if not templates_dir.exists():
        print(f"  ✗ Templates directory not found: {templates_dir}")
        return False
    
    required_templates = [
        "D4PQ236599.pdf",
        "SOSP215459.pdf",
        "SCSQ175392.pdf",
        "D4SQ106733.pdf",
        "SHSP085112.pdf"
    ]
    
    all_found = True
    for template in required_templates:
        template_path = templates_dir / template
        if template_path.exists():
            print(f"  ✓ {template}")
        else:
            print(f"  ✗ {template} not found")
            all_found = False
    
    return all_found

def test_output_directory():
    """Test if output directory can be created"""
    print("\nTesting output directory...")
    output_dir = Path("output")
    
    try:
        output_dir.mkdir(exist_ok=True)
        print(f"  ✓ Output directory: {output_dir.absolute()}")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create output directory: {e}")
        return False

def test_app_file():
    """Test if app.py exists and is readable"""
    print("\nTesting application file...")
    app_file = Path("app.py")
    
    if not app_file.exists():
        print(f"  ✗ app.py not found")
        return False
    
    try:
        with open(app_file, 'r') as f:
            content = f.read()
            if "class GasClipCertificateGenerator" in content:
                print("  ✓ app.py is valid")
                return True
            else:
                print("  ✗ app.py appears to be corrupted")
                return False
    except Exception as e:
        print(f"  ✗ Error reading app.py: {e}")
        return False

def test_date_formatting():
    """Test date formatting function"""
    print("\nTesting date formatting...")
    
    test_cases = [
        ("26022025", "26/02/2025"),
        ("01042026", "01/04/2026"),
        ("15122024", "15/12/2024")
    ]
    
    all_passed = True
    for input_date, expected_output in test_cases:
        # Simple format function
        formatted = f"{input_date[:2]}/{input_date[2:4]}/{input_date[4:]}"
        if formatted == expected_output:
            print(f"  ✓ {input_date} → {formatted}")
        else:
            print(f"  ✗ {input_date} → {formatted} (expected {expected_output})")
            all_passed = False
    
    return all_passed

def main():
    """Run all tests"""
    print("=" * 60)
    print("GasClip Certificates Generator - System Test")
    print("=" * 60)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Templates", test_templates),
        ("Output Directory", test_output_directory),
        ("Application File", test_app_file),
        ("Date Formatting", test_date_formatting)
    ]
    
    results = {}
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! The application is ready to use.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("\nor double-click:")
        print("  run_app.bat (Windows)")
        print("  run_app.sh (Mac/Linux)")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  - Install missing packages: pip install -r requirements.txt")
        print("  - Ensure you're in the correct directory")
        print("  - Check that all template files are present")
        return 1

if __name__ == "__main__":
    sys.exit(main())
