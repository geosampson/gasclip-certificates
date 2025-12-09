#!/usr/bin/env python3
"""
Coordinate Calibration Tool
Generates test PDFs with text at different positions to help find the perfect coordinates.
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, blue, green
import io
import json

def load_coordinates():
    """Load coordinates from JSON file"""
    coord_file = Path("coordinates.json")
    if coord_file.exists():
        with open(coord_file, 'r') as f:
            return json.load(f)
    return None

def create_test_overlay_with_offsets(offset_x=0, offset_y=0):
    """Create test overlay with adjustable offsets"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    # Load coordinates
    coords = load_coordinates()
    if not coords:
        print("ERROR: coordinates.json not found")
        return None
    
    # Test data
    data = {
        "serial": "SOSP55555",
        "activation": "02/10/2025",
        "lot": "TEST123456",
        "gas_prod": "21/03/2024",
        "calibration": "02/10/2025",
        "calibration_exp": "02/10/2027"
    }
    
    # Page 1
    can.setFillColor(red)
    can.setFont("Helvetica-Bold", 10)
    
    p1 = coords["page1"]
    
    # Serial number
    x = p1["serial_number"]["x"] + offset_x
    y = p1["serial_number"]["y"] + offset_y
    can.drawString(x, y, data["serial"])
    
    # Activation before
    x = p1["activation_before"]["x"] + offset_x
    y = p1["activation_before"]["y"] + offset_y
    can.drawString(x, y, data["activation"])
    
    # Lot number
    x = p1["lot_number"]["x"] + offset_x
    y = p1["lot_number"]["y"] + offset_y
    can.drawString(x, y, data["lot"])
    
    # Gas production
    x = p1["gas_production"]["x"] + offset_x
    y = p1["gas_production"]["y"] + offset_y
    can.drawString(x, y, data["gas_prod"])
    
    # Calibration date
    x = p1["calibration_date"]["x"] + offset_x
    y = p1["calibration_date"]["y"] + offset_y
    can.drawString(x, y, data["calibration"])
    
    can.showPage()
    
    # Page 2
    can.setFillColor(blue)
    can.setFont("Helvetica-Bold", 10)
    
    p2 = coords["page2"]
    
    # Serial number
    x = p2["serial_number"]["x"] + offset_x
    y = p2["serial_number"]["y"] + offset_y
    can.drawString(x, y, data["serial"])
    
    # Activation boxes
    activation_digits = data["activation"].replace('/', '')
    start_x = p2["activation_boxes"]["start_x"] + offset_x
    y = p2["activation_boxes"]["y"] + offset_y
    spacing = p2["activation_boxes"]["spacing"]
    
    for i, digit in enumerate(activation_digits):
        x = start_x + (i * spacing)
        can.drawString(x, y, digit)
    
    # Expiration boxes
    expiration_digits = data["calibration_exp"].replace('/', '')
    start_x = p2["expiration_boxes"]["start_x"] + offset_x
    y = p2["expiration_boxes"]["y"] + offset_y
    spacing = p2["expiration_boxes"]["spacing"]
    
    for i, digit in enumerate(expiration_digits):
        x = start_x + (i * spacing)
        can.drawString(x, y, digit)
    
    can.save()
    packet.seek(0)
    return packet

def generate_calibration_tests():
    """Generate multiple test PDFs with different offsets"""
    print("=" * 70)
    print("Coordinate Calibration Tool")
    print("=" * 70)
    
    template_path = Path("templates/SOSP215459.pdf")
    if not template_path.exists():
        print(f"ERROR: Template not found: {template_path}")
        return
    
    output_dir = Path("calibration_tests")
    output_dir.mkdir(exist_ok=True)
    
    # Test different offsets
    test_offsets = [
        (0, 0, "baseline"),
        (10, 0, "right_10"),
        (-10, 0, "left_10"),
        (0, 10, "up_10"),
        (0, -10, "down_10"),
        (5, 5, "right_5_up_5"),
        (-5, -5, "left_5_down_5"),
        (20, 0, "right_20"),
        (0, 20, "up_20"),
    ]
    
    for offset_x, offset_y, name in test_offsets:
        print(f"\nGenerating test: {name} (offset_x={offset_x}, offset_y={offset_y})")
        
        # Create overlay
        overlay_pdf = create_test_overlay_with_offsets(offset_x, offset_y)
        if not overlay_pdf:
            continue
        
        # Merge with template
        template = PdfReader(str(template_path))
        overlay_reader = PdfReader(overlay_pdf)
        writer = PdfWriter()
        
        for i, page in enumerate(template.pages):
            if i < len(overlay_reader.pages):
                page.merge_page(overlay_reader.pages[i])
            writer.add_page(page)
        
        # Save
        output_path = output_dir / f"test_{name}.pdf"
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        print(f"  ✓ Created: {output_path}")
    
    print("\n" + "=" * 70)
    print(f"✓ Generated {len(test_offsets)} test PDFs in: {output_dir}")
    print("\nInstructions:")
    print("1. Open each test PDF and see which one looks best")
    print("2. Note the offset that works (e.g., 'right_10_up_5')")
    print("3. Update coordinates.json with those offsets")
    print("4. Run this script again to verify")
    print("=" * 70)

if __name__ == "__main__":
    generate_calibration_tests()
