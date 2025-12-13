# GasClip Certificate Coordinate Calibrator Guide

## Overview

The Coordinate Calibrator is a visual tool that helps you set the exact positions where text should appear on your certificate PDFs. This eliminates the need to guess coordinates manually!

## How It Works

1. **Load a Product Template**: Select a product and load its PDF template
2. **Click on the PDF**: Click exactly where each field should be placed
3. **Save Coordinates**: The tool saves the exact coordinates to a JSON file
4. **Use in Main App**: The main certificate generator uses these coordinates automatically

## Step-by-Step Instructions

### 1. Start the Calibrator

```bash
python3 coordinate_calibrator.py
```

### 2. Select a Product

- Choose a product from the dropdown (e.g., "D4PQ: MGC-S+ (MGC-SIMPLEPLUS)")
- Click "Load PDF"

### 3. Calibrate Each Field

The tool will guide you through 6 fields:

**Page 1 (5 fields):**
1. **Serial Number** - Click where "D4PQ236599" should appear (top right)
2. **Activation Date** - Click where "01/04/2026" should appear (below serial)
3. **Lot Number** - Click where "25-3348" should appear (middle section)
4. **Gas Production Date** - Click where "29/05/2025" should appear
5. **Calibration Date** - Click where "01/10/2025" should appear (bottom section)

**Page 2 (1 field):**
6. **Serial Number** - Click where "D4PQ236599" should appear (after "sn:")

### 4. Navigation

- **Next Field ▶**: Move to the next field
- **◀ Previous Field**: Go back to the previous field
- **Page 1 / Page 2**: Switch between pages manually
- The tool automatically switches pages when needed

### 5. Visual Feedback

- Red crosshairs show where you've clicked
- Field names appear above each marker
- Current field is shown at the top

### 6. Save Your Work

- Click "Save Coordinates" when done
- Coordinates are saved to `calibrated_coordinates.json`
- You can reload them later with "Load Saved"

### 7. Repeat for All Products

Calibrate all 5 products:
- D4PQ (MGC-S+)
- SOSP (SGC-O)
- SCSQ (SGC-C)
- D4SQ (MGC-S)
- SHSP (SGC-H)

## Tips for Accurate Placement

1. **Zoom In**: The PDF is displayed at a good size for accuracy
2. **Click Precisely**: Click exactly where the LEFT edge of the text should start
3. **Check Your Work**: Red markers show where you clicked
4. **Redo if Needed**: Just click again to update a coordinate
5. **Test**: Generate a test certificate to verify placement

## Output File

The calibrator creates `calibrated_coordinates.json` with this structure:

```json
{
  "D4PQ": {
    "serial_p1": {"x": 395.92, "y": 647.58, "page": 1},
    "activation": {"x": 447.71, "y": 638.03, "page": 1},
    "lot": {"x": 95.75, "y": 411.58, "page": 1},
    "gas_production": {"x": 169.46, "y": 394.64, "page": 1},
    "calibration": {"x": 167.08, "y": 320.42, "page": 1},
    "serial_p2": {"x": 382.82, "y": 682.62, "page": 2}
  },
  ...
}
```

## Integration with Main App

The main certificate generator (`app.py`) automatically reads `calibrated_coordinates.json` if it exists. If not, it falls back to the default coordinates in `product_coordinates.py`.

## Troubleshooting

**PDF won't load:**
- Make sure the template PDF exists in the `templates/` folder
- Check that the filename matches exactly

**Coordinates seem off:**
- The tool accounts for PDF coordinate system (bottom-left origin)
- Test with the main app to verify placement
- Re-calibrate if needed

**Can't click on the PDF:**
- Make sure the PDF is loaded (you should see the image)
- Try clicking in a different area to test

## Benefits of This Approach

✅ **Visual**: See exactly where you're clicking
✅ **Accurate**: No manual coordinate calculation needed
✅ **Flexible**: Easy to adjust if templates change
✅ **Reusable**: Save and load coordinates anytime
✅ **Professional**: Keeps your original PDF templates with logos and formatting

## Next Steps

After calibrating all products:
1. Test certificate generation with the main app
2. Verify text placement is perfect
3. Adjust if needed by re-calibrating specific fields
4. Start generating certificates!
