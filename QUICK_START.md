# Quick Start Guide - GasClip Certificates Generator

## Get Started in 5 Minutes! 🚀

### Step 1: Download (1 minute)

Visit: **https://github.com/geosampson/gasclip-certificates**

Click the green **"Code"** button → **"Download ZIP"**

Extract to a folder on your computer (e.g., `C:\GasClip`)

### Step 2: Install Python (2 minutes - skip if already installed)

**Windows**:
1. Download from: https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT**: Check **"Add Python to PATH"**
4. Click "Install Now"
5. Restart computer

**Mac**:
```bash
brew install python3
```

**Linux**:
```bash
sudo apt-get install python3 python3-pip python3-tk
```

### Step 3: Install Application (1 minute)

**Windows**:
- Double-click `install_windows.bat`
- Wait for completion

**Mac/Linux**:
```bash
./install_unix.sh
```

### Step 4: Run Application (30 seconds)

**Windows**:
- Double-click `run_app.bat`

**Mac/Linux**:
```bash
./run_app.sh
```

### Step 5: Create Your First Certificate (1 minute)

1. **Select Product**: Choose from dropdown (e.g., "SGC-H (Single Gas Clip H2S)")

2. **Enter Data**:
   - Serial Number: `085112` (digits only, no prefix)
   - Activation Date: `26022025` (no slashes)
   - Lot Number: `RR2310181807`
   - Gas Production Date: `19102023`
   - Calibration Date: `26022024`

3. **Click**: "✓ Generate Certificate"

4. **Done!** Certificate saved in `output` folder

## Common Questions

### Q: Where are my certificates?
**A**: In the `output` folder inside the application directory

### Q: How do I organize by invoice?
**A**: After generating all certificates:
1. Click "📁 Finish All Forms & Create Invoice Folder"
2. Enter invoice number
3. All certificates move to `output/Invoice_[number]`

### Q: What format for dates?
**A**: DDMMYYYY (no slashes)
- Example: 26/02/2025 → Type: `26022025`

### Q: What about the serial prefix?
**A**: Don't type it! Just the numbers.
- For D4PQ236599 → Type: `236599`
- The app adds the prefix automatically

### Q: Can I edit the PDF after?
**A**: Yes! Open with any PDF editor

### Q: Something not working?
**A**: Run `python test_app.py` to check your setup

## Input Cheat Sheet

| What You See | What You Type |
|--------------|---------------|
| D4PQ236599 | `236599` |
| 26/02/2025 | `26022025` |
| SHSP085112 | `085112` |
| 01/04/2026 | `01042026` |

## Workflow Example

```
1. Launch app
2. Select "MGC-S+" 
3. Enter: 236599, 01042026, 25-3348, 29052025, 01102025
4. Click "Generate"
5. Repeat for more certificates
6. Click "Finish All Forms"
7. Enter invoice number
8. Done! All organized.
```

## Need More Help?

- **Detailed Guide**: See `USER_GUIDE.md`
- **Installation Issues**: See `INSTALL.md`
- **Technical Details**: See `PROJECT_SUMMARY.md`
- **Problems**: Open issue on GitHub

## Tips for Speed

1. ⌨️ Use **Tab** to move between fields
2. 📋 Prepare data in Excel first
3. 📝 Copy-paste lot numbers
4. ✅ Generate all certificates before clicking "Finish"
5. 🔄 Keep the app open for multiple batches

---

**That's it! You're ready to go.** 🎉

For detailed instructions, see the full **USER_GUIDE.md**
