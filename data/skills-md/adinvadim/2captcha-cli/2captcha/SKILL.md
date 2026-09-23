---
name: 2captcha
description: Solve CAPTCHAs with 2Captcha from the command line during browser automation.
version: 2.0.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
      config:
        - ~/.config/2captcha/api-key
    primaryEnv: TWOCAPTCHA_API_KEY
    envVars:
      - name: TWOCAPTCHA_API_KEY
        required: false
        description: Optional 2Captcha API key; config file works too.
    homepage: https://github.com/adinvadim/2captcha-cli
---

# 2Captcha Skill

Solve CAPTCHAs programmatically using the 2Captcha human-powered service.

Source and feedback: https://github.com/adinvadim/2captcha-cli

## Privacy and Authorized Use

This skill sends CAPTCHA images, page URLs, sitekeys, challenge IDs, and task metadata to 2Captcha for processing by the 2Captcha service and its human solvers. Use it only for authorized automation, and do not submit sensitive, regulated, internal, or third-party user data unless you have approval.

## Installation

```bash
# Install this agent skill with skills.sh
npx skills add adinvadim/2captcha-cli

# Or install with ClawHub/OpenClaw
openclaw skills install 2captcha

# Install the CLI after reviewing the source
git clone https://github.com/adinvadim/2captcha-cli.git
cd 2captcha-cli
python3 solve-captcha --version
mkdir -p ~/.local/bin
ln -sf "$PWD/solve-captcha" ~/.local/bin/solve-captcha

# Verify
solve-captcha --version
```

## Configuration

```bash
# Save your 2Captcha API key
mkdir -p ~/.config/2captcha
echo "YOUR_API_KEY" > ~/.config/2captcha/api-key

# Or use environment variable
export TWOCAPTCHA_API_KEY="your-key"
```

Get your API key at https://2captcha.com/enterpage

The CLI reads credentials only from the `--api-key` flag, `TWOCAPTCHA_API_KEY`, `~/.config/2captcha/api-key`, or `~/.2captcha-api-key`.

## Quick Reference

### Check Balance First
```bash
solve-captcha balance
```

### Image CAPTCHA
```bash
# From file
solve-captcha image /path/to/captcha.png

# From URL  
solve-captcha image "https://site.com/captcha.jpg"

# With options
solve-captcha image captcha.png --numeric 1 --math
solve-captcha image captcha.png --comment "Enter red letters only"
```

### reCAPTCHA v2
```bash
solve-captcha recaptcha2 --sitekey "6Le-wvk..." --url "https://example.com"
```

### reCAPTCHA v3
```bash
solve-captcha recaptcha3 --sitekey "KEY" --url "URL" --action "submit" --min-score 0.7
```

### hCaptcha
```bash
solve-captcha hcaptcha --sitekey "KEY" --url "URL"
```

### Cloudflare Turnstile
```bash
solve-captcha turnstile --sitekey "0x4AAA..." --url "URL"
```

### FunCaptcha (Arkose)
```bash
solve-captcha funcaptcha --public-key "KEY" --url "URL"
```

### GeeTest
```bash
# v3
solve-captcha geetest --gt "GT" --challenge "CHALLENGE" --url "URL"

# v4
solve-captcha geetest4 --captcha-id "ID" --url "URL"
```

### Text Question
```bash
solve-captcha text "What color is the sky?" --lang en
```

## Finding CAPTCHA Parameters

### reCAPTCHA sitekey
Look for:
- `data-sitekey` attribute in HTML
- `k=` parameter in reCAPTCHA iframe URL
- Network request to `google.com/recaptcha/api2/anchor`

### hCaptcha sitekey
Look for:
- `data-sitekey` in hCaptcha div
- Network requests to `hcaptcha.com`

### Turnstile sitekey
Look for:
- `data-sitekey` in Turnstile widget
- `cf-turnstile` class elements

## Workflow for Browser Automation

1. **Detect CAPTCHA** - Check if page has captcha element
2. **Extract params** - Get sitekey/challenge from page source
3. **Solve via CLI** - Call solve-captcha with params
4. **Inject token** - Set `g-recaptcha-response` or callback

### Example: Inject reCAPTCHA Token
```javascript
// After getting token from solve-captcha
document.getElementById('g-recaptcha-response').value = token;
// Or call callback if defined
___grecaptcha_cfg.clients[0].callback(token);
```

## Cost Awareness

- Check balance before heavy automation
- Image: ~$0.001 per solve
- reCAPTCHA/hCaptcha/Turnstile: ~$0.003 per solve

## Error Handling

Common errors:
- `ERROR_ZERO_BALANCE` - Top up account
- `ERROR_NO_SLOT_AVAILABLE` - Retry in few seconds
- `ERROR_CAPTCHA_UNSOLVABLE` - Bad image or impossible captcha
- `ERROR_WRONG_CAPTCHA_ID` - Invalid task ID

## Notes

- Solving takes 10-60 seconds depending on type
- reCAPTCHA v3 may need multiple attempts for high scores
- Some sites detect automation - use carefully
- Tokens expire! Use within 2-5 minutes
