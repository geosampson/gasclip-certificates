# GasClip Certificates Generator - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Step-by-Step Usage](#step-by-step-usage)
5. [Input Format Reference](#input-format-reference)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

## Introduction

The GasClip Certificates Generator is a desktop application designed to streamline the creation of calibration test certificates for GasClip gas detectors. Instead of manually filling out PDF forms, you can quickly generate professional certificates by entering only the essential numeric data.

### Supported Products

The application supports five GasClip gas detector models:

| Product | Full Name | Serial Prefix | Detector Life | Calibration Validity |
|---------|-----------|---------------|---------------|---------------------|
| MGC-S+ | MGC-SIMPLEPLUS | D4PQ | 36 months | 1095 days |
| SGC-O | Single Gas Clip O2 | SOSP | 24 months | 730 days |
| SGC-C | Single Gas Clip CO | SCSQ | 24 months | 730 days |
| MGC-S | MGC-SIMPLE | D4SQ | 24 months | 730 days |
| SGC-H | Single Gas Clip H₂S | SHSP | 24 months | 730 days |

## Installation

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **Disk Space**: At least 50 MB free space
- **RAM**: Minimum 2 GB

### Installation Steps

#### Windows

1. **Install Python** (if not already installed):
   - Download Python from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download the Application**:
   ```cmd
   git clone https://github.com/geosampson/gasclip-certificates.git
   cd gasclip-certificates
   ```

3. **Install Dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```cmd
   python app.py
   ```

#### macOS / Linux

1. **Install Python** (if not already installed):
   ```bash
   # macOS (using Homebrew)
   brew install python3
   
   # Linux (Ubuntu/Debian)
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. **Download the Application**:
   ```bash
   git clone https://github.com/geosampson/gasclip-certificates.git
   cd gasclip-certificates
   ```

3. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python3 app.py
   ```

### Creating a Desktop Shortcut (Optional)

#### Windows

Create a batch file `run_gasclip.bat`:
```batch
@echo off
cd /d "C:\path\to\gasclip-certificates"
python app.py
pause
```

#### macOS

Create a shell script `run_gasclip.sh`:
```bash
#!/bin/bash
cd "/path/to/gasclip-certificates"
python3 app.py
```

Make it executable:
```bash
chmod +x run_gasclip.sh
```

## Quick Start

### Basic Workflow

1. **Launch** the application
2. **Select** a product from the dropdown menu
3. **Enter** the serial number (digits only)
4. **Enter** the activation date (DDMMYYYY format)
5. **Enter** the lot number
6. **Enter** the gas production date (DDMMYYYY format)
7. **Enter** the calibration date (DDMMYYYY format)
8. **Click** "Generate Certificate"
9. **Repeat** steps 2-8 for additional certificates
10. **Click** "Finish All Forms & Create Invoice Folder"
11. **Enter** the invoice number
12. **Done!** All certificates are organized in a folder

## Step-by-Step Usage

### Step 1: Select Product

Click the "Select Product" dropdown and choose the gas detector model you're creating a certificate for. The serial number prefix will automatically appear below the dropdown.

**Example**: Select "SGC-H (Single Gas Clip H2S)" → Prefix shows "SHSPXXXXXX"

### Step 2: Enter Serial Number

Enter **only the numeric digits** of the serial number. Do not include the prefix letters.

**Correct Input Examples**:
- For serial D4PQ236599 → Enter: `236599`
- For serial SHSP085112 → Enter: `085112`
- For serial SOSP215459 → Enter: `215459`

**Incorrect Input Examples**:
- ❌ D4PQ236599 (includes prefix)
- ❌ 23-6599 (includes dash)
- ❌ 23 6599 (includes space)

### Step 3: Enter Activation Date

Enter the activation date as **8 consecutive digits** in DDMMYYYY format (day, month, year). Think of it like entering a credit card expiration date.

**Correct Input Examples**:
- For 26/02/2025 → Enter: `26022025`
- For 01/04/2026 → Enter: `01042026`
- For 15/12/2024 → Enter: `15122024`

**Incorrect Input Examples**:
- ❌ 26/02/2025 (includes slashes)
- ❌ 2025-02-26 (wrong format)
- ❌ 26-02-2025 (includes dashes)

### Step 4: Enter Lot Number

Enter the complete lot number exactly as it appears on the certificate. This can include letters, numbers, and dashes.

**Examples**:
- `RR2310181807`
- `25-3348`
- `RR2408261440`
- `252938`

### Step 5: Enter Gas Production Date

Enter the gas production date as **8 consecutive digits** in DDMMYYYY format.

**Examples**:
- For 19/10/2023 → Enter: `19102023`
- For 29/05/2025 → Enter: `29052025`

### Step 6: Enter Calibration Date

Enter the calibration date as **8 consecutive digits** in DDMMYYYY format.

**Examples**:
- For 26/02/2024 → Enter: `26022024`
- For 01/10/2025 → Enter: `01102025`

### Step 7: Generate Certificate

Click the "✓ Generate Certificate" button. The application will:
- Validate all inputs
- Create a PDF certificate based on the template
- Save it to the `output` folder
- Display a success message

You'll be asked if you want to create another certificate:
- Click **Yes** to clear the form and create another certificate
- Click **No** if you're done or want to finish the batch

### Step 8: Create Invoice Folder

When you've generated all certificates for an invoice:

1. Click "📁 Finish All Forms & Create Invoice Folder"
2. Enter the invoice number in the dialog
3. Click "Create Folder"

The application will:
- Create a folder named `Invoice_[number]` in the `output` directory
- Move all generated certificates into this folder
- Reset the counter for a new batch

## Input Format Reference

### Quick Reference Table

| Field | Format | Example Input | Displays As |
|-------|--------|---------------|-------------|
| Serial Number | Digits only | `236599` | D4PQ236599 |
| Activation Date | DDMMYYYY | `26022025` | 26/02/2025 |
| Lot Number | As shown | `RR2310181807` | RR2310181807 |
| Gas Production Date | DDMMYYYY | `19102023` | 19/10/2023 |
| Calibration Date | DDMMYYYY | `26022024` | 26/02/2024 |

### Date Format Conversion

To convert a date from DD/MM/YYYY to DDMMYYYY:

1. Remove all slashes
2. Keep the order: day, month, year

**Examples**:

| Original Date | Remove Slashes | Input |
|---------------|----------------|-------|
| 26/02/2025 | 26 02 2025 | `26022025` |
| 01/04/2026 | 01 04 2026 | `01042026` |
| 15/12/2024 | 15 12 2024 | `15122024` |

### Common Mistakes to Avoid

1. **Including the serial prefix**
   - ❌ Wrong: D4PQ236599
   - ✅ Correct: 236599

2. **Using slashes in dates**
   - ❌ Wrong: 26/02/2025
   - ✅ Correct: 26022025

3. **Wrong date format (YYYY-MM-DD)**
   - ❌ Wrong: 20250226
   - ✅ Correct: 26022025

4. **Spaces or special characters**
   - ❌ Wrong: 236 599
   - ✅ Correct: 236599

## Troubleshooting

### Application Won't Start

**Problem**: Double-clicking the application does nothing or shows an error.

**Solutions**:
1. Ensure Python is installed: Open terminal/command prompt and type `python --version`
2. Install dependencies: Run `pip install -r requirements.txt`
3. Check for error messages in the terminal when running `python app.py`

### "Template Not Found" Error

**Problem**: Error message says template PDF is missing.

**Solutions**:
1. Ensure you're running the application from the correct directory
2. Check that the `templates` folder exists and contains all 5 PDF files
3. Re-download the repository if files are missing

### Invalid Input Errors

**Problem**: Application shows "Invalid input" or validation errors.

**Solutions**:
1. Check that serial number contains only digits
2. Verify all dates are exactly 8 digits in DDMMYYYY format
3. Ensure no spaces or special characters in numeric fields

### Generated PDFs Look Wrong

**Problem**: The generated PDFs don't have the correct data.

**Solutions**:
1. This version creates copies of templates - data overlay will be added in future updates
2. For now, you can manually edit the PDFs using a PDF editor
3. Ensure you selected the correct product template

### Can't Find Generated Certificates

**Problem**: Don't know where the certificates were saved.

**Solutions**:
1. Look in the `output` folder inside the application directory
2. After creating an invoice folder, look for `output/Invoice_[number]`
3. The success message shows the full path to the folder

## FAQ

### Q: Can I use this on multiple computers?

**A**: Yes! Simply install Python and the dependencies on each computer, then copy the application folder.

### Q: Can I customize the templates?

**A**: Yes, you can replace the PDF files in the `templates` folder with your own templates. Make sure to keep the same filenames.

### Q: How do I backup my certificates?

**A**: Simply copy the `output` folder to a backup location (external drive, cloud storage, etc.).

### Q: Can I edit a certificate after generating it?

**A**: Yes, you can open the PDF with any PDF editor (Adobe Acrobat, PDF-XChange, etc.) and make changes.

### Q: What if I make a mistake?

**A**: Just delete the incorrect PDF from the `output` folder and generate a new one with the correct information.

### Q: Can I upload directly to Google Drive?

**A**: The current version saves files locally. You can manually upload the invoice folders to Google Drive, or use Google Drive's desktop sync feature.

### Q: How many certificates can I generate at once?

**A**: There's no limit! Generate as many as you need before clicking "Finish All Forms".

### Q: Can I use this offline?

**A**: Yes, once installed, the application works completely offline.

### Q: What if I need to add a new product type?

**A**: Contact the developer or modify the `products` dictionary in `app.py` to add new product configurations.

### Q: Is my data stored anywhere?

**A**: No, all data is processed locally on your computer. Nothing is sent to any server.

## Support

For additional help or to report issues:

- **GitHub Issues**: https://github.com/geosampson/gasclip-certificates/issues
- **Email**: Contact your system administrator

## Tips for Efficient Use

1. **Prepare Your Data**: Before starting, have all serial numbers, dates, and lot numbers ready in a spreadsheet
2. **Use Tab Key**: Press Tab to move between fields quickly
3. **Copy-Paste**: You can copy lot numbers from other sources and paste them directly
4. **Batch Processing**: Generate all certificates for one invoice before clicking "Finish"
5. **Verify First**: Always check the first certificate to ensure all data is correct
6. **Regular Backups**: Periodically backup your `output` folder

## Keyboard Shortcuts

- **Tab**: Move to next field
- **Shift+Tab**: Move to previous field
- **Enter**: (when in a field) Move to next field
- **Ctrl+A**: Select all text in current field
- **Ctrl+C**: Copy selected text
- **Ctrl+V**: Paste text

---

**Version**: 1.0  
**Last Updated**: December 2025  
**Author**: GasClip Certificates Team
