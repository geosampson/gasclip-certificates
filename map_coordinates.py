#!/usr/bin/env python3
"""
Create test PDFs with coordinate grids to find exact text positions
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, blue, green
import io

def create_coordinate_grid():
    """Create a transparent overlay with coordinate grid"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4
    
    # Draw grid lines every 50 points
    can.setStrokeColor(blue)
    can.setLineWidth(0.5)
    
    # Vertical lines
    for x in range(0, int(width), 50):
        can.line(x, 0, x, height)
        can.setFont("Helvetica", 6)
        can.drawString(x + 2, 5, str(x))
    
    # Horizontal lines
    for y in range(0, int(height), 50):
        can.line(0, y, width, y)
        can.setFont("Helvetica", 6)
        can.drawString(5, y + 2, str(y))
    
    # Test positions for SOSP template
    can.setFillColor(red)
    can.setFont("Helvetica-Bold", 10)
    
    # Based on visual inspection, these are approximate positions
    # Page 1 positions (from bottom-left)
    test_positions = [
        # Serial number (top right area)
        (480, 730, "SOSP55555"),
        (500, 730, "SOSP55555"),
        (520, 730, "SOSP55555"),
        
        # Activation date (below serial)
        (480, 710, "24/02/2026"),
        (500, 710, "24/02/2026"),
        (520, 710, "24/02/2026"),
        
        # Lot number (middle left area)
        (140, 475, "RR2408261440"),
        (150, 475, "RR2408261440"),
        (160, 475, "RR2408261440"),
        
        # Gas production date (below lot)
        (140, 455, "25/04/2025"),
        (150, 455, "25/04/2025"),
        (160, 455, "25/04/2025"),
        
        # Calibration date (lower area)
        (180, 555, "24/02/2025"),
        (190, 555, "24/02/2025"),
        (200, 555, "24/02/2025"),
    ]
    
    for x, y, text in test_positions:
        can.drawString(x, y, text)
    
    can.showPage()
    
    # Page 2 - test box positions
    can.setFillColor(green)
    can.setFont("Helvetica-Bold", 10)
    
    # Serial number
    can.drawString(480, 750, "SOSP55555")
    can.drawString(500, 750, "SOSP55555")
    can.drawString(520, 750, "SOSP55555")
    
    # Activation date boxes (8 individual digits)
    # These boxes are typically in the middle-right area
    box_y = 480  # Approximate
    box_x_start = 340
    box_spacing = 20
    
    activation = "02102025"
    for i, digit in enumerate(activation):
        x = box_x_start + (i * box_spacing)
        can.drawString(x, box_y, digit)
        can.drawString(x, box_y - 20, digit)
        can.drawString(x, box_y + 20, digit)
    
    # Calibration expiration boxes
    exp_y = 400  # Approximate
    expiration = "02102027"
    for i, digit in enumerate(expiration):
        x = box_x_start + (i * box_spacing)
        can.drawString(x, exp_y, digit)
        can.drawString(x, exp_y - 20, digit)
        can.drawString(x, exp_y + 20, digit)
    
    can.save()
    packet.seek(0)
    return packet

def create_test_overlay():
    """Create test PDF with coordinate grid"""
    template_path = Path("templates/SOSP215459.pdf")
    
    if not template_path.exists():
        print(f"ERROR: Template not found: {template_path}")
        return
    
    print("Creating coordinate grid overlay...")
    
    # Create grid overlay
    grid_pdf = create_coordinate_grid()
    
    # Load template
    template = PdfReader(str(template_path))
    grid_reader = PdfReader(grid_pdf)
    writer = PdfWriter()
    
    # Merge pages
    for i, page in enumerate(template.pages):
        if i < len(grid_reader.pages):
            page.merge_page(grid_reader.pages[i])
        writer.add_page(page)
    
    # Save output
    output_path = Path("output/COORDINATE_MAP.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'wb') as f:
        writer.write(f)
    
    print(f"✓ Coordinate map created: {output_path}")
    print("\nOpen this PDF to see:")
    print("  - Blue grid lines every 50 points")
    print("  - Red test text at various positions (Page 1)")
    print("  - Green test text at various positions (Page 2)")
    print("\nUse this to find the exact coordinates for text placement.")

if __name__ == "__main__":
    create_test_overlay()
