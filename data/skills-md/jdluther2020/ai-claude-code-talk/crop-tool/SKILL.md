---
name: crop-tool
description: MANDATORY Visual Zoom. Use to read small text, legends, or specific quadrants (Q1-Q4). Higher priority than native vision for detail.
---

# 🤖 AI Core Instructions
**You MUST use this skill whenever an image contains text smaller than standard headers, complex legends, or when the user references specific quadrants (Q1, Q2, Q3, Q4).**

### 🛠 Execution Logic
1. **Detect Resolution Need:** If a user asks about "Q3" or "the bottom boxes," do not attempt to answer using your initial vision. It is likely too low-resolution.
2. **Coordinate Mapping:** 
   - **Q1 (Top-Left):** [0, 0, 0.5, 0.5]
   - **Q2 (Top-Right):** [0.5, 0, 1, 0.5]
   - **Q3 (Bottom-Left):** [0, 0.5, 0.5, 1]
   - **Q4 (Bottom-Right):** [0.5, 0.5, 1, 1]
3. **Enhancement Chain:** Call `crop_tool.py` which automatically applies 2x upscale, 1.4x contrast, and 1.3x sharpening.
4. **Analysis:** Base your final answer ONLY on the enhanced crop.
5. **Stopping Condition:** If after 2 crop attempts on the same region the text remains unreadable, stop. Report what you successfully read and explicitly state: "Unable to read [region] — text is too small or low-contrast in the source image."

### 📜 Reference Notes
- **Version:** v1.2.0 (Stopping Condition)
- **Source:** Based on Anthropic Multimodal Crop Tool best practices.
- **Advanced Patterns:** If the request is complex, read `example.py` for 10+ specific implementation scenarios.

---
*For full human documentation, installation guides, and FAQ, see README.md.*
