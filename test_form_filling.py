#!/usr/bin/env python3
"""
Test PDF form filling functionality
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime, timedelta

def test_form_filling():
    """Test filling a PDF form with sample data"""
    print("=" * 70)
    print("Testing PDF Form Filling")
    print("=" * 70)
    
    # Test data
    serial_number = "SOSP55555"
    activation_date = "02/10/2025"
    lot_number = "TEST123456"
    gas_prod_date = "21/03/2024"
    calibration_date = "02/10/2025"
    
    # Calculate expiration (730 days for SGC-O)
    parts = activation_date.split('/')
    activation = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
    expiration = activation + timedelta(days=730)
    calibration_exp = expiration.strftime("%d/%m/%Y")
    
    data = {
        "serial": serial_number,
        "activation": activation_date,
        "lot": lot_number,
        "gas_prod": gas_prod_date,
        "calibration": calibration_date,
        "calibration_exp": calibration_exp
    }
    
    print("\nTest Data:")
    for key, value in data.items():
        print(f"  {key}: {value}")
    
    # Template path
    template_path = Path("templates_with_forms/SOSP215459.pdf")
    output_path = Path("output/TEST_FORM_FILLED.pdf")
    
    if not template_path.exists():
        print(f"\n✗ ERROR: Form template not found: {template_path}")
        print("Please run: python create_form_templates.py")
        return False
    
    print(f"\n✓ Template found: {template_path}")
    
    try:
        # Read template
        reader = PdfReader(str(template_path))
        writer = PdfWriter()
        
        # Copy pages
        for page in reader.pages:
            writer.add_page(page)
        
        print(f"✓ Template has {len(reader.pages)} pages")
        
        # Check if template has form fields
        if reader.get_form_text_fields():
            print(f"✓ Template has form fields:")
            for field_name in reader.get_form_text_fields().keys():
                print(f"    - {field_name}")
        else:
            print("✗ WARNING: Template has no form fields!")
        
        # Prepare form data
        activation_digits = data["activation"].replace('/', '')
        expiration_digits = data["calibration_exp"].replace('/', '')
        
        form_data = {
            'serial_number': data["serial"],
            'activation_before': data["activation"],
            'lot_number': data["lot"],
            'gas_production': data["gas_prod"],
            'calibration_date': data["calibration"],
            'serial_number_p2': data["serial"],
            # Activation date boxes
            'act_d1': activation_digits[0] if len(activation_digits) > 0 else '',
            'act_d2': activation_digits[1] if len(activation_digits) > 1 else '',
            'act_m1': activation_digits[2] if len(activation_digits) > 2 else '',
            'act_m2': activation_digits[3] if len(activation_digits) > 3 else '',
            'act_y1': activation_digits[4] if len(activation_digits) > 4 else '',
            'act_y2': activation_digits[5] if len(activation_digits) > 5 else '',
            'act_y3': activation_digits[6] if len(activation_digits) > 6 else '',
            'act_y4': activation_digits[7] if len(activation_digits) > 7 else '',
            # Expiration date boxes
            'exp_d1': expiration_digits[0] if len(expiration_digits) > 0 else '',
            'exp_d2': expiration_digits[1] if len(expiration_digits) > 1 else '',
            'exp_m1': expiration_digits[2] if len(expiration_digits) > 2 else '',
            'exp_m2': expiration_digits[3] if len(expiration_digits) > 3 else '',
            'exp_y1': expiration_digits[4] if len(expiration_digits) > 4 else '',
            'exp_y2': expiration_digits[5] if len(expiration_digits) > 5 else '',
            'exp_y3': expiration_digits[6] if len(expiration_digits) > 6 else '',
            'exp_y4': expiration_digits[7] if len(expiration_digits) > 7 else '',
        }
        
        print(f"\n✓ Prepared {len(form_data)} form field values")
        
        # Fill form fields
        writer.update_page_form_field_values(writer.pages[0], form_data)
        if len(writer.pages) > 1:
            writer.update_page_form_field_values(writer.pages[1], form_data)
        
        print("✓ Form fields filled")
        
        # Write output
        output_path.parent.mkdir(exist_ok=True)
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        print(f"✓ Output written: {output_path}")
        print(f"✓ File size: {output_path.stat().st_size} bytes")
        
        print("\n" + "=" * 70)
        print("✓ PDF Form Filling Test PASSED!")
        print("\nPlease check the generated PDF:")
        print(f"  {output_path.absolute()}")
        print("\nVerify that all data appears correctly in the certificate.")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    import sys
    success = test_form_filling()
    sys.exit(0 if success else 1)
