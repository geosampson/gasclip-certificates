#!/usr/bin/env python3
"""
Analyze PDF to find exact text positions
"""

from PyPDF2 import PdfReader
from pathlib import Path

def analyze_pdf(pdf_path):
    """Extract text and positions from PDF"""
    print(f"\nAnalyzing: {pdf_path}")
    print("=" * 80)
    
    reader = PdfReader(pdf_path)
    
    for page_num, page in enumerate(reader.pages):
        print(f"\n--- Page {page_num + 1} ---")
        
        # Get page dimensions
        mediabox = page.mediabox
        width = float(mediabox.width)
        height = float(mediabox.height)
        print(f"Page size: {width} x {height} points")
        print(f"Page size: {width/72:.2f} x {height/72:.2f} inches")
        
        # Extract text
        text = page.extract_text()
        print(f"\nExtracted text preview:")
        print("-" * 40)
        lines = text.split('\n')[:20]  # First 20 lines
        for i, line in enumerate(lines, 1):
            if line.strip():
                print(f"{i:2d}: {line}")
        
        total_lines = len(text.split('\n'))
        if total_lines > 20:
            print(f"... ({total_lines - 20} more lines)")

# Analyze all templates
templates_dir = Path("templates")
for template in templates_dir.glob("*.pdf"):
    analyze_pdf(template)
    print("\n" + "=" * 80)

print("\n\nNOTE: PDF coordinates are measured from BOTTOM-LEFT corner")
print("Standard A4 size: 595.276 x 841.890 points (8.27 x 11.69 inches)")
