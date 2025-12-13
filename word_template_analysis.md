# Word Template Analysis

## What I see in D4PQ236599_clean.docx:

### Page 1:
- **Serial Number**: "D4PQ236599" (needs to be replaced)
- **Activation Date**: "01/04/2026" (needs to be replaced)
- **Lot Number**: "25-3348" (needs to be replaced)
- **Gas Production**: "29/05/2025" (needs to be replaced)
- **Calibration Date**: "01/10/2025" (needs to be replaced)
- **Detector Life**: "36" (needs to be replaced - 36 for D4PQ/D4SQ, 24 for others)

### Page 2:
- **Serial Number**: "D4PQ236599" (needs to be replaced)
- **Detector Life**: "36" (needs to be replaced)
- **Calibration Days**: "1095" (needs to be replaced - 1095 for D4PQ/D4SQ, 730 for others)

## Replacement Strategy:

I'll use the `python-docx` library to:
1. Open the Word template
2. Search for specific text strings (like "D4PQ236599", "01/04/2026", etc.)
3. Replace them with user-provided values
4. Save the modified Word file
5. Convert to PDF using `docx2pdf` or LibreOffice

## Text to Replace:

### D4PQ (MGC-S+):
- "D4PQ236599" → User's serial number
- "01/04/2026" → User's activation date
- "25-3348" → User's lot number
- "29/05/2025" → User's gas production date
- "01/10/2025" → User's calibration date
- "36" → 36 (detector life months)
- "1095" → 1095 (calibration days)

### SOSP, SCSQ, SHSP (SGC products):
- Similar replacements but with:
- "24" → 24 (detector life months)
- "730" → 730 (calibration days)

### D4SQ (MGC-S):
- Similar to D4PQ:
- "36" → 36 (detector life months)
- "1095" → 1095 (calibration days)

## Benefits of Word-based approach:
1. ✅ No coordinate positioning issues
2. ✅ Perfect alignment automatically
3. ✅ Easy to maintain and update templates
4. ✅ Can export to PDF after filling
5. ✅ Much more reliable than PDF overlay
