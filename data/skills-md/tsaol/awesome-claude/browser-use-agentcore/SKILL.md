---
name: browser-use-agentcore
description: >
  AWS AgentCore Browser skill for automated web testing and screenshot capture.
  Use this skill when the user asks to:
  - Test if a website works / 测试网站是否正常
  - Take a screenshot of a webpage / 截取网页截图
  - Check for JavaScript errors or console errors
  - Verify API health endpoints
  - Open a URL in a cloud browser
  - Debug website loading issues
  This skill uses AWS Bedrock AgentCore Browser (cloud-based, no local browser needed).
license: MIT
---

# Browser Use AgentCore Skill

## Overview

This skill uses **AWS Bedrock AgentCore Browser** to perform automated web testing in the cloud. No local browser or display required - tests run on AWS infrastructure.

## Features

- Test any URL with a real browser
- Capture full-page screenshots
- Check for JavaScript console errors
- Verify API health endpoints
- View live browser session in AWS Console

## Prerequisites

1. AWS credentials configured
2. IAM permissions for AgentCore Browser
3. Python 3.10+

### Required IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:StartBrowserSession",
        "bedrock-agentcore:StopBrowserSession",
        "bedrock-agentcore:GetBrowserSession"
      ],
      "Resource": "*"
    }
  ]
}
```

## Quick Start

### Install Dependencies

```bash
pip install bedrock-agentcore playwright boto3 nest-asyncio
```

### Basic Usage

```bash
# Test a URL
python scripts/browser_test.py https://example.com

# Test with screenshot
python scripts/browser_test.py https://example.com --screenshot screenshot.png

# Test with API health check
python scripts/browser_test.py https://example.com --check-api

# Full test with JSON output
python scripts/browser_test.py https://example.com -s screenshot.png -a --json
```

## Python API

### Simple Test

```python
from browser_test import test_url

# test_url is a synchronous function
results = test_url(
    url="https://example.com",
    screenshot_path="screenshot.png",
    check_api=True
)

print(f"Status: {results['status']}")
print(f"Title: {results['title']}")
print(f"Errors: {results['errors']}")
```

### Advanced Usage with Playwright

```python
from bedrock_agentcore.tools.browser_client import BrowserClient
from playwright.async_api import async_playwright

async def custom_test():
    client = BrowserClient(region="us-west-2")

    session = await client.start_browser_session(
        session_name="my-test",
        timeout=300,
        viewport={"width": 1920, "height": 1080}
    )

    ws_url, headers = await client.generate_ws_headers()

    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(ws_url, headers=headers)
        page = browser.contexts[0].pages[0]

        # Your custom test logic
        await page.goto("https://example.com")
        await page.click("button#submit")
        await page.wait_for_selector(".result")

        content = await page.content()
        await browser.close()

    await client.stop_browser_session()
    return content
```

## Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| `url` | - | URL to test (required) |
| `--screenshot` | `-s` | Path to save screenshot |
| `--check-api` | `-a` | Check /api/health endpoint |
| `--region` | `-r` | AWS region (default: us-west-2) |
| `--json` | `-j` | Output results as JSON |

## Output Format

### Console Output

```
🚀 Starting browser session in us-west-2...
✅ Browser session started: sess-abc123
🔗 Connecting to remote browser...
🌐 Navigating to https://example.com...
📄 Page title: Example Domain
📊 HTTP status: 200
📸 Screenshot saved: screenshot.png

==================================================
📋 Test Results
==================================================
URL: https://example.com
Status: 200
Title: Example Domain
Errors: 0

✅ All checks passed!
```

### JSON Output

```json
{
  "url": "https://example.com",
  "status": 200,
  "title": "Example Domain",
  "errors": [],
  "api_check": {
    "url": "https://example.com/api/health",
    "status": 200,
    "body": "{\"status\":\"healthy\"}"
  },
  "screenshot": "screenshot.png"
}
```

## Live View

While tests are running, you can watch the browser in real-time:

1. Open [AWS Console - AgentCore Browser](https://us-west-2.console.aws.amazon.com/bedrock-agentcore/builtInTools)
2. Navigate to **Built-in tools**
3. Find your active session
4. Click **View live session**

## Troubleshooting

### Session Timeout

If tests timeout, increase the session timeout:

```python
session = await client.start_browser_session(
    session_name="long-test",
    timeout=600  # 10 minutes
)
```

### Permission Denied

Ensure your IAM role/user has the required permissions for AgentCore Browser.

### Network Errors

Check that the target URL is accessible from AWS infrastructure. Internal/private URLs may not be reachable.

## Regional Availability

AgentCore Browser is available in:
- us-east-1 (N. Virginia)
- us-west-2 (Oregon)

## Pricing

AgentCore Browser uses consumption-based pricing with no upfront costs. See [AWS Pricing](https://aws.amazon.com/bedrock/agentcore/pricing/) for details.
