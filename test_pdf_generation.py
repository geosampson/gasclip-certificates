#!/usr/bin/env python3
"""
Test PDF generation with text overlay
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black
import io

def create_test_certificate():
    """Generate a test certificate to verify PDF overlay works"""
    
    print("Testing PDF generation with text overlay...")
    print("=" * 60)
    
    # Test data
    data = {
        "serial": "SOSP55555",
        "activation": "02/10/2025",
        "lot": "TEST123456",
        "gas_prod": "21/32/1321",
        "calibration": "02/10/2025",
        "calibration_exp": "02/10/2027"
    }
    
    # Positions for SGC-O template
    positions = {
        "page1": {
            "serial": (665, 115),
            "activation_before": (665, 100),
            "lot_number": (145, 367),
            "gas_production": (145, 352),
            "calibration_date": (195, 287),
        },
        "page2": {
            "serial": (665, 90),
            "activation_boxes": [
                (545, 365), (565, 365),
                (595, 365), (615, 365),
                (655, 365), (675, 365), (695, 365), (715, 365)
            ],
            "expiration_boxes": [
                (545, 285), (565, 285),
                (595, 285), (615, 285),
                (655, 285), (675, 285), (695, 285), (715, 285)
            ]
        }
    }
    
    # Create overlay
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)
    can.setFillColor(black)
    
    # Page 1 overlays
    print("\nPage 1 - Writing data:")
    print(f"  Serial: {data['serial']} at {positions['page1']['serial']}")
    can.drawString(positions["page1"]["serial"][0], positions["page1"]["serial"][1], 
                  data["serial"])
    
    print(f"  Activation: {data['activation']} at {positions['page1']['activation_before']}")
    can.drawString(positions["page1"]["activation_before"][0], 
                  positions["page1"]["activation_before"][1], 
                  data["activation"])
    
    print(f"  Lot: {data['lot']} at {positions['page1']['lot_number']}")
    can.drawString(positions["page1"]["lot_number"][0], 
                  positions["page1"]["lot_number"][1], 
                  data["lot"])
    
    print(f"  Gas Prod: {data['gas_prod']} at {positions['page1']['gas_production']}")
    can.drawString(positions["page1"]["gas_production"][0], 
                  positions["page1"]["gas_production"][1], 
                  data["gas_prod"])
    
    print(f"  Calibration: {data['calibration']} at {positions['page1']['calibration_date']}")
    can.drawString(positions["page1"]["calibration_date"][0], 
                  positions["page1"]["calibration_date"][1], 
                  data["calibration"])
    
    can.showPage()
    
    # Page 2 overlays
    print("\nPage 2 - Writing data:")
    print(f"  Serial: {data['serial']} at {positions['page2']['serial']}")
    can.drawString(positions["page2"]["serial"][0], positions["page2"]["serial"][1], 
                  data["serial"])
    
    # Activation date in boxes
    activation_digits = data["activation"].replace('/', '')
    print(f"  Activation boxes: {activation_digits}")
    for i, digit in enumerate(activation_digits):
        if i < len(positions["page2"]["activation_boxes"]):
            x, y = positions["page2"]["activation_boxes"][i]
            print(f"    Digit '{digit}' at ({x}, {y})")
            can.drawString(x, y, digit)
    
    # Expiration date in boxes
    expiration_digits = data["calibration_exp"].replace('/', '')
    print(f"  Expiration boxes: {expiration_digits}")
    for i, digit in enumerate(expiration_digits):
        if i < len(positions["page2"]["expiration_boxes"]):
            x, y = positions["page2"]["expiration_boxes"][i]
            print(f"    Digit '{digit}' at ({x}, {y})")
            can.drawString(x, y, digit)
    
    can.save()
    packet.seek(0)
    
    # Load template
    template_path = Path("templates/SOSP215459.pdf")
    if not template_path.exists():
        print(f"\n✗ ERROR: Template not found: {template_path}")
        return False
    
    print(f"\n✓ Template found: {template_path}")
    
    # Merge overlay with template
    template_pdf = PdfReader(str(template_path))
    overlay_reader = PdfReader(packet)
    writer = PdfWriter()
    
    print(f"✓ Template pages: {len(template_pdf.pages)}")
    print(f"✓ Overlay pages: {len(overlay_reader.pages)}")
    
    # Merge each page
    for i, page in enumerate(template_pdf.pages):
        if i < len(overlay_reader.pages):
            print(f"  Merging page {i+1}...")
            page.merge_page(overlay_reader.pages[i])
        writer.add_page(page)
    
    # Write output
    output_path = Path("output/TEST_SOSP55555.pdf")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"\n✓ Test certificate generated: {output_path}")
    print(f"✓ File size: {output_path.stat().st_size} bytes")
    
    print("\n" + "=" * 60)
    print("✓ PDF generation test PASSED!")
    print("\nPlease check the generated PDF:")
    print(f"  {output_path.absolute()}")
    print("\nVerify that the data appears on the certificate.")
    
    return True

if __name__ == "__main__":
    try:
        success = create_test_certificate()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
