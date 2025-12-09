# GasClip Certificates Generator

A desktop application for generating calibration test certificates for GasClip gas detectors.

## Features

✅ **Five Product Support**
- MGC-S+ (MGC-SIMPLEPLUS) - D4PQ prefix
- SGC-O (Single Gas Clip O2) - SOSP prefix  
- SGC-C (Single Gas Clip CO) - SCSQ prefix
- MGC-S (MGC-SIMPLE) - D4SQ prefix
- SGC-H (Single Gas Clip H2S) - SHSP prefix

✅ **User-Friendly Interface**
- Simple dropdown product selection
- Auto-formatting dates (DD/MM/YYYY) as you type
- Date validation (prevents invalid dates like 31/02/2025)
- Keyboard navigation (Enter to advance, ↑↓ arrows to navigate)
- Input validation to prevent errors

✅ **Smart Workflow**
1. Select product → Enter data → Generate certificate
2. Repeat for multiple certificates
3. Click "Finish" → Enter invoice number
4. All certificates organized in `Invoice_XXXX` folder

✅ **Automatic Calculations**
- Calculates calibration expiration dates automatically
- Adds product-specific prefixes to serial numbers
- Validates all date inputs

## Quick Start

### Windows

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download the Application**
   ```cmd
   git clone https://github.com/geosampson/gasclip-certificates.git
   cd gasclip-certificates
   ```

3. **Install Dependencies**
   ```cmd
   install_windows.bat
   ```

4. **Run the Application**
   ```cmd
   run_app.bat
   ```

### Mac/Linux

1. **Clone the Repository**
   ```bash
   git clone https://github.com/geosampson/gasclip-certificates.git
   cd gasclip-certificates
   ```

2. **Install Dependencies**
   ```bash
   chmod +x install_unix.sh
   ./install_unix.sh
   ```

3. **Run the Application**
   ```bash
   chmod +x run_app.sh
   ./run_app.sh
   ```

## Usage

### Generating a Certificate

1. **Select Product** from the dropdown menu
2. **Enter Serial Number** (digits only, prefix is added automatically)
   - Example: `236599` becomes `SOSP236599`
3. **Enter Activation Date** (type numbers only, slashes added automatically)
   - Type: `26022025` → Becomes: `26/02/2025`
4. **Enter Lot Number**
   - Example: `RR2310181807` or `25-3348`
5. **Enter Gas Production Date** (auto-formatted)
   - Type: `19102023` → Becomes: `19/10/2023`
6. **Enter Calibration Date** (auto-formatted)
   - Type: `26022024` → Becomes: `26/02/2024`
7. **Click "Generate Certificate"**

The application will:
- Validate all inputs
- Calculate expiration date automatically
- Generate the PDF certificate
- Save it to the `output/` folder

### Batch Processing

1. Generate multiple certificates one after another
2. When finished, click **"Finish All Forms & Create Invoice Folder"**
3. Enter the invoice number
4. All certificates will be moved to `output/Invoice_XXXX/` folder

### Keyboard Shortcuts

- **Enter**: Move to next field
- **↑ Arrow**: Move to previous field
- **↓ Arrow**: Move to next field

## File Structure

```
gasclip-certificates/
├── app.py                      # Main application
├── templates/                  # Original PDF templates
│   ├── D4PQ236599.pdf
│   ├── SOSP215459.pdf
│   ├── SCSQ175392.pdf
│   ├── D4SQ106733.pdf
│   └── SHSP085112.pdf
├── output/                     # Generated certificates
│   └── Invoice_XXXX/          # Organized by invoice
├── coordinates.json            # Text position configuration
├── calibrate_coordinates.py    # Coordinate calibration tool
├── requirements.txt            # Python dependencies
├── install_windows.bat         # Windows installer
├── run_app.bat                # Windows launcher
├── install_unix.sh            # Mac/Linux installer
└── run_app.sh                 # Mac/Linux launcher
```

## Coordinate Calibration (Optional)

If the text positioning needs adjustment:

1. **Edit `coordinates.json`** to adjust text positions
2. **Run calibration tool** to test different positions:
   ```bash
   python calibrate_coordinates.py
   ```
3. **Check generated test PDFs** in `calibration_tests/` folder
4. **Update coordinates.json** with the best values

## Troubleshooting

### Text Not Appearing in PDFs

The coordinates may need adjustment for your specific PDF templates:
1. Run `python calibrate_coordinates.py`
2. Check the test PDFs in `calibration_tests/`
3. Find the offset that looks best
4. Update `coordinates.json` with those values

### Date Validation Errors

- Dates must be valid (e.g., 31/02/2025 is invalid)
- Month must be 01-12
- Day must be 01-31
- Year must be 2000-2100

### Application Won't Start

- Ensure Python 3.7+ is installed
- Run the install script again
- Check that all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

## Technical Details

### Dependencies

- Python 3.7+
- tkinter (GUI framework)
- PyPDF2 (PDF manipulation)
- reportlab (PDF text overlay)

### Product Specifications

| Product | Prefix | Detector Life | Calibration Days |
|---------|--------|---------------|------------------|
| MGC-S+  | D4PQ   | 36 months     | 1095 days        |
| SGC-O   | SOSP   | 24 months     | 730 days         |
| SGC-C   | SCSQ   | 24 months     | 730 days         |
| MGC-S   | D4SQ   | 24 months     | 730 days         |
| SGC-H   | SHSP   | 24 months     | 730 days         |

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions
- Review [INSTALL.md](INSTALL.md) for installation help

## Version History

### v3.0 (Current)
- ✅ Working PDF text overlay
- ✅ Auto-formatting dates with slashes
- ✅ Date validation
- ✅ Keyboard navigation (Enter, ↑↓ arrows)
- ✅ Batch processing with invoice folders
- ✅ Coordinate calibration tools

### v2.0
- PDF form field approach (experimental)

### v1.0
- Initial release with basic functionality

---

**Made with ❤️ for efficient certificate generation**
