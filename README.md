# GasClip Certificates Generator

A desktop application for generating calibration test certificates for GasClip gas detectors. This application simplifies the process of creating professional PDF certificates by automating data entry and formatting.

## Features

- **Five Product Templates**: Support for MGC-S+, SGC-O, SGC-C, MGC-S, and SGC-H gas detectors
- **User-Friendly Interface**: Simple GUI for selecting products and entering parameters
- **Smart Input**: Only enter numeric values - the application handles formatting automatically
- **Batch Processing**: Create multiple certificates in one session
- **Flexible Storage**: Save certificates locally or upload to Google Drive
- **Invoice Organization**: Group certificates by invoice number for easy management

## Supported Products

1. **MGC-S+** (MGC-SIMPLEPLUS) - Serial prefix: D4PQ
2. **SGC-O** (Single Gas Clip O2) - Serial prefix: SOSP
3. **SGC-C** (Single Gas Clip CO) - Serial prefix: SCSQ
4. **MGC-S** (MGC-SIMPLE) - Serial prefix: D4SQ
5. **SGC-H** (Single Gas Clip H2S) - Serial prefix: SHSP

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone this repository:
```bash
git clone https://github.com/geosampson/gasclip-certificates.git
cd gasclip-certificates
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Usage

1. **Select Product**: Choose the gas detector model from the dropdown menu
2. **Enter Serial Number**: Input only the numeric digits (e.g., 236599 for D4PQ236599)
3. **Enter Activation Date**: Input date as 8 digits without slashes (e.g., 01042026 for 01/04/2026)
4. **Enter Lot Number**: Input the complete lot number
5. **Enter Gas Production Date**: Input date as 8 digits (e.g., 29052025)
6. **Enter Calibration Date**: Input date as 8 digits (e.g., 01102025)
7. **Generate Certificate**: Click "Generate Certificate" to create the PDF
8. **Save**: Choose to save locally or upload to Google Drive
9. **Continue or Finish**: Create more certificates or click "Finish All Forms"
10. **Invoice Number**: Enter the invoice number to organize all certificates in a folder

## Input Format

- **Serial Number**: Numeric digits only (no prefix)
  - Example: `236599` (not D4PQ236599)
- **Dates**: 8 digits in DDMMYYYY format (no slashes)
  - Example: `26022025` (for 26/02/2025)
- **Lot Number**: Complete lot number as shown on certificate
  - Example: `RR2310181807`

## Project Structure

```
gasclip-certificates/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── templates/             # PDF templates for each product
│   ├── D4PQ236599.pdf
│   ├── SOSP215459.pdf
│   ├── SCSQ175392.pdf
│   ├── D4SQ106733.pdf
│   └── SHSP085112.pdf
├── output/                # Generated certificates (created automatically)
└── README.md             # This file
```

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on GitHub.
