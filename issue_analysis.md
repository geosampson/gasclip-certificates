# Issue Analysis - D4PQ321312.pdf

## Problems Identified

### Page 1 Issues:
1. **Old serial number still visible**: "D4PQ236599" (template) is still showing, new "D4PQ321312" is overlaid on top right
2. **Old activation date visible**: "Activate before: 01/04/2026" (template) still showing
3. **Old dates overlapping**: 
   - "29/10/2025" (template) visible with new date overlaid
   - "22/06/2025" (template) visible with new date overlaid
4. **Old lot number visible**: Template lot number still showing with new one overlaid
5. **Old gas production date**: Template date still showing
6. **Old calibration date**: "01/10/2025" (template) still showing

### Page 2 Issues:
1. **Old serial number visible**: "D4PQ236599" (template) still showing, new "D4PQ321312" overlaid
2. **Date boxes have extra zeros**: 
   - "1 0 0 2 2 0 2 0" instead of "1 0 0 2 2 0 2 0" (looks like there's a "0" after formatting)
   - The issue is the date "10/02/2020" is being split incorrectly

## Root Cause

**Problem 1: Text Overlay Instead of Replacement**
- The current approach uses `page.merge_page()` which OVERLAYS the new text ON TOP of the existing content
- PDFs don't have "editable text fields" - the text is baked into the page
- We need to either:
  - A) Cover the old text with white rectangles first, then add new text
  - B) Recreate the entire page from scratch
  - C) Use a different PDF library that can remove/edit text

**Problem 2: Date Formatting Issue**
- When splitting date "10/02/2020" by removing slashes, we get "10022020"
- But the code is adding an extra "0" somewhere in the process
- Need to check the date splitting logic

## Solution Approach

### For Problem 1 (Old Text Visible):
Use white rectangles to cover old text before overlaying new text:
```python
# Draw white rectangle over old text area
can.setFillColor(white)
can.rect(x, y, width, height, fill=1, stroke=0)

# Then draw new text
can.setFillColor(black)
can.drawString(x, y, new_text)
```

### For Problem 2 (Extra Zero):
Fix the date splitting logic:
```python
# Current (wrong):
activation_digits = data['activation'].replace('/', '')  # "10/02/2020" → "10022020"

# Should be:
activation_digits = data['activation'].replace('/', '')  # Already correct
# But need to ensure we're not adding extra characters
```

## Next Steps

1. Add white rectangle overlays to cover old text
2. Fix date digit extraction to remove extra zeros
3. Test with the same data to verify fixes
4. Adjust coordinates if needed
