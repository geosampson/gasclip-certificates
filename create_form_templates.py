#!/usr/bin/env python3
"""
Create fillable PDF form templates from existing PDFs
This tool adds text form fields at specified positions
"""

from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import (
    DictionaryObject,
    ArrayObject,
    TextStringObject,
    NumberObject,
    NameObject,
    IndirectObject
)
import sys

def create_text_field(writer, name, x, y, width, height, page_num=0):
    """
    Create a text form field
    
    Args:
        writer: PdfWriter object
        name: Field name
        x, y: Position from bottom-left (in points)
        width, height: Field dimensions
        page_num: Page number (0-indexed)
    """
    # Create the field dictionary
    field = DictionaryObject()
    field.update({
        NameObject("/FT"): NameObject("/Tx"),  # Field Type: Text
        NameObject("/T"): TextStringObject(name),  # Field Name
        NameObject("/V"): TextStringObject(""),  # Value (empty initially)
        NameObject("/Rect"): ArrayObject([
            NumberObject(x),
            NumberObject(y),
            NumberObject(x + width),
            NumberObject(y + height)
        ]),
        NameObject("/F"): NumberObject(4),  # Flags: Print
        NameObject("/Ff"): NumberObject(0),  # Field flags
    })
    
    return field

def add_form_fields_to_pdf(input_path, output_path, fields_config):
    """
    Add form fields to a PDF
    
    Args:
        input_path: Path to input PDF
        output_path: Path to output PDF with form fields
        fields_config: Dictionary with field configurations
    """
    print(f"\nProcessing: {input_path}")
    print(f"Output: {output_path}")
    
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    # Copy all pages
    for page in reader.pages:
        writer.add_page(page)
    
    # Create form fields
    fields = []
    
    for field_name, field_info in fields_config.items():
        page_num = field_info.get('page', 0)
        x = field_info['x']
        y = field_info['y']
        width = field_info.get('width', 100)
        height = field_info.get('height', 15)
        
        field = create_text_field(writer, field_name, x, y, width, height, page_num)
        fields.append(field)
        
        print(f"  Added field: {field_name} at ({x}, {y}) on page {page_num + 1}")
    
    # Add AcroForm to the PDF
    if fields:
        writer._root_object.update({
            NameObject("/AcroForm"): DictionaryObject({
                NameObject("/Fields"): ArrayObject(fields),
                NameObject("/NeedAppearances"): NameObject("/true")
            })
        })
    
    # Write output
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"✓ Created form template with {len(fields)} fields\n")

def get_field_configurations():
    """
    Define field configurations for each template
    Based on visual analysis of the PDFs
    """
    # Common configuration for all templates (they have the same layout)
    common_config = {
        # Page 1 fields
        'serial_number': {'page': 0, 'x': 520, 'y': 727, 'width': 80, 'height': 12},
        'activation_before': {'page': 0, 'x': 520, 'y': 712, 'width': 80, 'height': 12},
        'lot_number': {'page': 0, 'x': 145, 'y': 475, 'width': 120, 'height': 12},
        'gas_production': {'page': 0, 'x': 145, 'y': 460, 'width': 80, 'height': 12},
        'calibration_date': {'page': 0, 'x': 190, 'y': 555, 'width': 80, 'height': 12},
        
        # Page 2 fields - Serial number
        'serial_number_p2': {'page': 1, 'x': 520, 'y': 750, 'width': 80, 'height': 12},
        
        # Page 2 - Activation date boxes (8 individual digit fields)
        'act_d1': {'page': 1, 'x': 545, 'y': 477, 'width': 12, 'height': 12},
        'act_d2': {'page': 1, 'x': 560, 'y': 477, 'width': 12, 'height': 12},
        'act_m1': {'page': 1, 'x': 590, 'y': 477, 'width': 12, 'height': 12},
        'act_m2': {'page': 1, 'x': 605, 'y': 477, 'width': 12, 'height': 12},
        'act_y1': {'page': 1, 'x': 650, 'y': 477, 'width': 12, 'height': 12},
        'act_y2': {'page': 1, 'x': 665, 'y': 477, 'width': 12, 'height': 12},
        'act_y3': {'page': 1, 'x': 680, 'y': 477, 'width': 12, 'height': 12},
        'act_y4': {'page': 1, 'x': 695, 'y': 477, 'width': 12, 'height': 12},
        
        # Page 2 - Expiration date boxes (8 individual digit fields)
        'exp_d1': {'page': 1, 'x': 545, 'y': 397, 'width': 12, 'height': 12},
        'exp_d2': {'page': 1, 'x': 560, 'y': 397, 'width': 12, 'height': 12},
        'exp_m1': {'page': 1, 'x': 590, 'y': 397, 'width': 12, 'height': 12},
        'exp_m2': {'page': 1, 'x': 605, 'y': 397, 'width': 12, 'height': 12},
        'exp_y1': {'page': 1, 'x': 650, 'y': 397, 'width': 12, 'height': 12},
        'exp_y2': {'page': 1, 'x': 665, 'y': 397, 'width': 12, 'height': 12},
        'exp_y3': {'page': 1, 'x': 680, 'y': 397, 'width': 12, 'height': 12},
        'exp_y4': {'page': 1, 'x': 695, 'y': 397, 'width': 12, 'height': 12},
    }
    
    return {
        'D4PQ236599.pdf': common_config,
        'SOSP215459.pdf': common_config,
        'SCSQ175392.pdf': common_config,
        'D4SQ106733.pdf': common_config,
        'SHSP085112.pdf': common_config,
    }

def main():
    """Main function to create form templates"""
    print("=" * 70)
    print("PDF Form Template Creator")
    print("=" * 70)
    
    templates_dir = Path("templates")
    forms_dir = Path("templates_with_forms")
    forms_dir.mkdir(exist_ok=True)
    
    if not templates_dir.exists():
        print(f"ERROR: Templates directory not found: {templates_dir}")
        return 1
    
    field_configs = get_field_configurations()
    
    created_count = 0
    for template_name, fields_config in field_configs.items():
        input_path = templates_dir / template_name
        output_path = forms_dir / template_name
        
        if not input_path.exists():
            print(f"WARNING: Template not found: {input_path}")
            continue
        
        try:
            add_form_fields_to_pdf(str(input_path), str(output_path), fields_config)
            created_count += 1
        except Exception as e:
            print(f"ERROR processing {template_name}: {e}")
            import traceback
            traceback.print_exc()
    
    print("=" * 70)
    print(f"✓ Created {created_count} form templates in: {forms_dir}")
    print("\nNote: These templates now have fillable form fields.")
    print("The application can fill these fields programmatically.")
    print("=" * 70)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
