# Installation Guide - GasClip Certificates Generator

## Quick Start

### Windows Users

1. **Download the repository**:
   - Click the green "Code" button on GitHub
   - Select "Download ZIP"
   - Extract the ZIP file to a folder (e.g., `C:\GasClip`)

2. **Install Python** (if not already installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - **IMPORTANT**: Check "Add Python to PATH" during installation
   - Restart your computer after installation

3. **Install the application**:
   - Double-click `install_windows.bat`
   - Wait for installation to complete

4. **Run the application**:
   - Double-click `run_app.bat`
   - The application window will appear

### Mac Users

1. **Download the repository**:
   ```bash
   git clone https://github.com/geosampson/gasclip-certificates.git
   cd gasclip-certificates
   ```

2. **Install Python** (if not already installed):
   ```bash
   brew install python3
   ```

3. **Install the application**:
   ```bash
   ./install_unix.sh
   ```

4. **Run the application**:
   ```bash
   ./run_app.sh
   ```

### Linux Users

1. **Download the repository**:
   ```bash
   git clone https://github.com/geosampson/gasclip-certificates.git
   cd gasclip-certificates
   ```

2. **Install Python** (if not already installed):
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip python3-tk
   ```

3. **Install the application**:
   ```bash
   ./install_unix.sh
   ```

4. **Run the application**:
   ```bash
   ./run_app.sh
   ```

## Detailed Installation Instructions

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **Disk Space**: At least 50 MB
- **RAM**: Minimum 2 GB

### Manual Installation

If the automated scripts don't work, you can install manually:

1. **Install Python**:
   - Ensure Python 3.8+ is installed
   - Verify with: `python --version` or `python3 --version`

2. **Install dependencies**:
   ```bash
   pip install PyPDF2==3.0.1
   pip install reportlab==4.0.7
   pip install Pillow==10.1.0
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```
   or
   ```bash
   python3 app.py
   ```

## Troubleshooting

### "Python is not recognized"

**Problem**: Command prompt says "Python is not recognized as an internal or external command"

**Solution**:
1. Reinstall Python and check "Add Python to PATH"
2. Or manually add Python to PATH:
   - Search for "Environment Variables" in Windows
   - Edit "Path" variable
   - Add Python installation directory (e.g., `C:\Python311`)

### "No module named tkinter"

**Problem**: Error about missing tkinter module

**Solution** (Linux):
```bash
sudo apt-get install python3-tk
```

**Solution** (Mac):
```bash
brew install python-tk
```

### Permission Denied (Mac/Linux)

**Problem**: Can't run shell scripts

**Solution**:
```bash
chmod +x install_unix.sh run_app.sh
```

### Application Window Doesn't Appear

**Problem**: Script runs but no window appears

**Solution**:
1. Check if there are error messages in the terminal
2. Ensure all dependencies are installed
3. Try running with: `python app.py` directly to see error messages

## Verifying Installation

After installation, verify everything works:

1. Run the application
2. Select a product from the dropdown
3. Try entering sample data:
   - Serial: `123456`
   - Activation Date: `01012025`
   - Lot Number: `TEST123`
   - Gas Production Date: `01012025`
   - Calibration Date: `01012025`
4. Click "Generate Certificate"
5. Check the `output` folder for the generated PDF

## Uninstallation

To remove the application:

1. Delete the application folder
2. (Optional) Uninstall Python packages:
   ```bash
   pip uninstall PyPDF2 reportlab Pillow
   ```

## Getting Help

If you encounter issues:

1. Check the [USER_GUIDE.md](USER_GUIDE.md) for usage instructions
2. Review the [Troubleshooting](#troubleshooting) section above
3. Open an issue on [GitHub](https://github.com/geosampson/gasclip-certificates/issues)

## Next Steps

Once installed, read the [USER_GUIDE.md](USER_GUIDE.md) for detailed usage instructions.
