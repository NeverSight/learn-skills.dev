---
name: xiaohongshu-search-summarizer
description: Searches Xiaohongshu(小红书) for a given keyword, extracts the top N posts (including texts, images, and user comments), and then synthesizes a comprehensive final analytical report. Use this skill whenever the user wants to search Xiaohongshu for a specific topic, compile research seamlessly combining text and images, or needs an aggregated thematic summary of social media posts, comments, and visual data on a given subject.
---

# Xiaohongshu Search and Summarize

This skill automates the process of extracting high-quality multi-modal content (text + images) from Xiaohongshu (小红书) and actively assists you in generating a deeply integrated, analytical final report for the user. Due to Xiaohongshu's aggressive anti-scraping mechanisms, direct HTTP requests or naive scraping often result in 404s or blocks. This skill natively bypasses these by simulating a real user through the `playwright-cli` in a headed browser window.

It operates in two distinct phases:

### Phase 1: Subagent Data Collection
1. Simulate a search for the keyword on Xiaohongshu in a headed browser.
2. Advance through image sliders to fully load all lazy pictures from the top N posts.
3. Extract titles, descriptions, top comments, and all high-resolution images.
4. Download those images to a local directory and generate a raw data document (`[keyword]_raw_data.md`).

### Phase 2: AI Multi-Modal Synthesis (Your Job)
5. **You** MUST use your file reading capabilities to read the `[keyword]_raw_data.md` file.
6. Inside the raw data markdown, you will find paths to image files. **You MUST use your file reading / vision capabilities on these image file paths** to actually ingest and "see" their visual content. If you skip this step, you are only reading file names, not the images themselves!
7. **You** analyze the texts, summarize the genuinely useful comments (discarding noise like "pm me"), and interpret the semantic content of the images you just viewed (e.g. diagrams, guidelines, step-by-step UI flows).
8. **You** compile everything into a beautifully synthesized, single comprehensive report rather than just a linear list of posts. 

### Dependencies
- `playwright-cli` (Must be available on the path)
- `python3` (Required to download images and stitch the raw data markdown)

---

## Usage Instructions

### Step 1: Run the Extraction Script

Execute the wrapper script in `scripts/run.sh`. It accepts the following arguments:

```bash
/bin/bash <skill_dir>/scripts/run.sh "YOUR KEYWORD" <MAX_POSTS> <OUTPUT_DIRECTORY>
```

- **`YOUR KEYWORD`**: The search term to look up on Xiaohongshu.
- **`<MAX_POSTS>`**: (Optional, default = 10) The number of top posts to scan.
- **`<OUTPUT_DIRECTORY>`**: (Optional, default = `./`) Directory where the raw data and images will be saved.

**Example execution**:

```bash
/bin/bash ~/.claude/skills/xiaohongshu-search-summarizer/scripts/run.sh "openclaw使用场景" 10 "./xhs_report_openclaw_scenarios"
```

### Step 2: Read Raw Data & Images

Once the bash script finishes successfully, navigate to the `OUTPUT_DIRECTORY` and use your file reading capabilities to ingest the generated `[keyword]_raw_data.md` file.

Inside this file, you will find descriptions, comments, and file paths pointing to `post_X_img_Y.webp` or `post_X_img_Y.jpg`. 

### Step 3: Synthesis & Summarization

**This is the most critical step.** Do not just return the raw markdown file to the user. Instead, write a polished comprehensive markdown report that reorganizes the information logically, while retaining a high level of detail.

Follow these strict compilation rules:
- **Do not list posts individually** (e.g. avoid "Post 1: ... Post 2: ...").  
- **Read the Images:** You MUST use your file reading and vision capabilities on the `.webp` or `.jpg` image files found in the raw data directory to interpret their contents.
- **Detailed & Comprehensive Synthesis:** Provide a highly detailed summary that includes diverse viewpoints, nuances, and specific examples found across different posts. Avoid over-summarizing or losing important context; preserve the richness and diversity of the information.
- **Extract and merge themes:** Group ideas by concepts, steps, recurring themes, or pros/cons.  
- **Evaluate comments:** Merge insights from valuable comments directly into the core narrative. Skip useless or repetitive comments, but preserve diverse opinions or helpful counter-arguments from the comments section.
- **Integrate images contextually:** Embed the most relevant and high-quality images directly into the flow of your final report to support the analytical points being made. Describe their visual meaning based on what you saw with your vision capabilities.
- **Save to OUTPUT_DIRECTORY:** Save your beautifully compiled final Markdown report using your file writing capabilities directly into the same `<OUTPUT_DIRECTORY>` as the raw data (e.g., `<OUTPUT_DIRECTORY>/[keyword]_synthesis.md`), and give the user the path to it. 

### Error Handling

If you encounter `404 Not Found` or "element not visible" errors during the browser invocation:
- Keep in mind that Xiaohongshu may demand a login challenge. If the site pauses waiting for a login, instruct the user to verify the `playwright-cli` browser window and perform necessary authentication manually, then try the script again.
