---
name: product-catalog-downloader
description: This skill explains how to download semiconductor product catalog (usually a spreadsheet with product information) from a webpage that contains "Download" or "Export" button, using Playwright CLI.
allowed-tools: Bash(playwright-cli:*)
---

# Download prodcut catalog with playwright-cli

This skill describe how to use playwright-cli to automate download product catalog process from a specific webpage that contains "Download" or "Export" button.

## When to Use

- **Scenario 1**: User provides a webpage Url and ask agent to download product catalog.
- **Scenario 2**: User provides a file that has a list of webpages and ask agent to go to each page to download product catalogs. 

## Quick Start

Basic usage example or workflow:

```bash
# open webpage url provided by user
playwright-cli open https://www.ti.com/product-category/amplifiers/products.html
# grep "Download" to find the "Download" button from playwright-cli snapshot that was automatically taken when open the webpage
grep "Download" .playwright-cli/page-2026-03-29T02-00-52-610Z.yml 
# run playwright code to handel download. Save file using url and timestamp as file name
playwright-cli run-code "async page => {
                                const downloadPromise = page.waitForEvent('download');
                                await page.getByRole('button', { name: 'Download Excel' }).click();
                                const download = await downloadPromise;
                                await download.saveAs('./www.ti.com-product-category-amplifiers_2026-03-28-13-10-56.xlsx');
                                return download.suggestedFilename();
                              }"
# check download file
ls www.ti.com-product-category-amplifiers_2026-03-28-13-10-56.xlsx
# close browser
playwright-cli close
# delete .playwright-cli directory if download success
rm -rf .playwright-cli
```

## Workflows

Step-by-step process for a common task:

1. **Step 1**: Open webpage with url provided by user using playwright-cli 
2. **Step 2**: Find the download/export link/button etc. from the playwright-cli snapshot *.yml.
3. **Step 3**: Use "playwright-cli run-code" to download file.
4. **Step 4**: Check file existance.
4. **Step 5**: Close browser.


## Best Practices

- **Do**:
  1. We have validated the webpage do have Download/Export link/button. If you don't see it, stop and report current status and error.
  2. Make a check list if downloading from multiple urls. Use the check list to validate if all urls are processed before quit.
  3. Always use playwright-cli run-code to download file. This is the most stable way.
  4. When using url in the "downlaod.saveAs" file name, replace illegal chars like "/" with "-"
  5. Check if there is any dialog window like "Cookie Settings". Dismiss it and snapshot again.
  6. Always close browser
  7. Clean .playwright-cli directory if download is successful. Leave it for debugging if there is any error occurs.

- **Do Not**:
  1. Try to find the Download/Export link/button if you don't see it. Stop and Report error.
  2. Question the url. It is correct.
  3. Use any other methods to download file.

## Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Found the Download button but can not click it| Check if there is a dialog/modal window covering the webpage.|
| playwright-cli is not installed | It is installed globally, try "nvm use lts" to activate it|
