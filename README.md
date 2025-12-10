# GasClip Certificates Generator v4.0

Professional desktop application for generating calibration test certificates for GasClip gas detectors.

## 🎉 Version 4.0 - Clean Templates!

This version uses **clean PDF templates** with empty spaces, making certificate generation simpler and more reliable!

### ✨ Key Features

- **5 Product Support**: MGC-S+, SGC-O, SGC-C, MGC-S, SGC-H
- **Auto-Formatting Dates**: Type `26022025` → automatically becomes `26/02/2025`
- **Date Validation**: Prevents invalid dates (e.g., 31/02/2025)
- **Keyboard Navigation**: Press Enter to move to next field, ↑↓ arrows to navigate
- **Batch Processing**: Create multiple certificates in one session
- **Invoice Organization**: Group certificates by invoice number
- **Clean Templates**: No white rectangles needed - just write text in empty spaces!

## 🚀 Quick Start

### Windows
```batch
1. Download ZIP from GitHub
2. Extract to a folder
3. Double-click install_windows.bat
4. Double-click run_app.bat
```

### Mac/Linux
```bash
git clone https://github.com/geosampson/gasclip-certificates
cd gasclip-certificates
./install_unix.sh
./run_app.sh
```

## 📋 Supported Products

| Product | Prefix | Full Name | Detector Life | Calibration Days |
|---------|--------|-----------|---------------|------------------|
| MGC-S+  | D4PQ   | MGC-SIMPLEPLUS | 36 months | 1095 days |
| SGC-O   | SOSP   | Single Gas Clip O2 | 24 months | 730 days |
| SGC-C   | SCSQ   | Single Gas Clip CO | 24 months | 730 days |
| MGC-S   | D4SQ   | MGC-SIMPLE | 24 months | 730 days |
| SGC-H   | SHSP   | Single Gas Clip H2S | 24 months | 730 days |

## 💡 How to Use

### Step 1: Select Product
Choose from the dropdown menu (e.g., "SGC-C (Single Gas Clip CO)")

### Step 2: Enter Serial Number
Enter only the **digits** (e.g., `175392`)  
The prefix (e.g., `SCSQ`) is added automatically

### Step 3: Enter Dates
Type dates without slashes (e.g., `26022025`)  
The slashes are added automatically as you type: `26/02/2025`

**Example:**
- Activation Date: `26022025` → `26/02/2025`
- Gas Production: `19102023` → `19/10/2023`
- Calibration: `26022024` → `26/02/2024`

### Step 4: Enter Lot Number
Enter the lot number (e.g., `CO 100ppm`)

### Step 5: Generate Certificate
Click "Generate Certificate" button

The PDF is created instantly: `SCSQ175392.pdf`

### Step 6: Batch Processing
- Click "Yes" to create another certificate
- Repeat steps 2-5 for each certificate

### Step 7: Finish & Organize
- Click "Finish All Forms & Create Invoice Folder"
- Enter invoice number (e.g., `12345`)
- All certificates are moved to `output/Invoice_12345/`

## 📦 What's Generated

### Page 1: Calibration Certificate
- Serial Number (top right)
- Activation Date (below serial)
- Lot Number
- Gas Production Date
- Calibration Date

### Page 2: Detector Information
- Serial Number (after "sn:")
- Empty date boxes (for manual filling if needed)

## 🔧 Requirements

- **Python 3.7+**
- **tkinter** (GUI library, usually pre-installed)
- **PyPDF2** (PDF manipulation)
- **reportlab** (PDF generation)

All dependencies install automatically via the install scripts.

## 📁 Project Structure

```
gasclip-certificates/
├── app.py                      # Main application
├── product_coordinates.py      # Coordinate mappings for each product
├── requirements.txt            # Python dependencies
├── templates/                  # Clean PDF templates
│   ├── D4PQ236599_clean.pdf
│   ├── SOSP215459_clean.pdf
│   ├── SCSQ175392_clean.pdf
│   ├── D4SQ106733_clean.pdf
│   └── SHSP085112_clean.pdf
├── output/                     # Generated certificates
├── install_windows.bat         # Windows installation script
├── run_app.bat                 # Windows run script
├── install_unix.sh             # Mac/Linux installation script
└── run_app.sh                  # Mac/Linux run script
```

## 🎯 Features in Detail

### Auto-Formatting Dates
- Type numbers only: `26022025`
- Slashes added automatically: `26/02/2025`
- Cursor stays in the right position (no jumping!)
- Format: DD/MM/YYYY

### Date Validation
- Checks if date is valid (e.g., rejects 31/02/2025)
- Validates day, month, and year ranges
- Shows helpful error messages

### Keyboard Navigation
- **Enter**: Move to next field
- **↑ Arrow**: Move to previous field
- **↓ Arrow**: Move to next field
- Fast data entry workflow!

### Batch Processing
- Create multiple certificates in one session
- Certificates saved to `output/` folder
- Counter shows how many generated

### Invoice Organization
- Group certificates by invoice number
- Creates folder: `output/Invoice_12345/`
- Moves all certificates automatically
- Ready for archiving or sending to customer

## 🔍 Troubleshooting

### Application won't start?
- Make sure Python 3.7+ is installed
- Run the install script again
- Check that tkinter is installed: `python3 -m tkinter`

### Date input cursor jumping?
- This is fixed in v4.0!
- The cursor now stays in the correct position

### Text not appearing in PDF?
- Make sure you're using the clean templates (`*_clean.pdf`)
- Check that `product_coordinates.py` exists
- Verify templates are in the `templates/` folder

### Wrong coordinates?
- The coordinates are pre-calibrated for the clean templates
- If you modify templates, you'll need to update `product_coordinates.py`

## 📝 Version History

- **v4.0** (Current) - Clean templates, fixed date input cursor, simplified page 2
- **v3.2** - Dynamic coordinates for all products
- **v3.1** - Added white rectangles to cover old text
- **v3.0** - Initial working version with PDF overlay
- **v2.0** - Form-based approach (deprecated)
- **v1.0** - Basic file copying (deprecated)

## 🤝 Contributing

This is a private tool for internal use. For issues or feature requests, contact the development team.

## 📄 License

MIT License - See LICENSE file for details

## 🎓 Support

For questions or issues:
1. Check the USER_GUIDE.md for detailed instructions
2. Review the INSTALL.md for installation help
3. Read the QUICK_START.md for a 5-minute tutorial

## 🚀 What's New in v4.0

### Clean Templates
- No more white rectangles needed!
- Templates have empty spaces for data
- Simpler and more reliable

### Fixed Date Input
- Cursor no longer jumps when typing dates
- Smooth typing experience
- Slashes inserted automatically at the right position

### Simplified Page 2
- Only serial number is written
- Date boxes remain empty (visual guides only)
- Cleaner output

### Better Performance
- Faster PDF generation
- Less code complexity
- More maintainable

---

**Repository**: https://github.com/geosampson/gasclip-certificates  
**Version**: 4.0  
**Status**: ✅ Production Ready  
**Last Updated**: December 2024
