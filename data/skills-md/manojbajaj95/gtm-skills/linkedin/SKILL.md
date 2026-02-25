---
name: linkedin
description: Enables Claude to manage LinkedIn posts, profile, and professional networking through browser automation
version: 1.0.0
author: Canifi
category: social
---

# LinkedIn Skill

## Overview
Automates LinkedIn operations including posting content, managing professional profile, engaging with network, and building professional connections through browser automation.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/linkedin/install.sh | bash
```

Or manually:
```bash
cp -r skills/linkedin ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set LINKEDIN_EMAIL "your-email@example.com"
canifi-env set LINKEDIN_PASSWORD "your-password"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities
- Create and publish posts
- Share articles and documents
- Like, comment, and share content
- Send connection requests
- Update profile sections
- Search for people and jobs
- Manage company pages
- View post analytics

## Usage Examples

### Example 1: Create a Post
```
User: "Post on LinkedIn about our company milestone"
Claude: I'll create that LinkedIn post.
- Navigate to linkedin.com
- Click Start a post
- Write milestone announcement
- Add relevant hashtags
- Publish post
- Confirm posted
```

### Example 2: Share Article
```
User: "Share this article on LinkedIn with my thoughts"
Claude: I'll share that article.
- Click share article
- Paste article URL
- Add commentary
- Select visibility
- Post
- Confirm shared
```

### Example 3: Update Profile
```
User: "Update my LinkedIn headline"
Claude: I'll update your headline.
- Navigate to profile
- Click edit profile
- Update headline section
- Save changes
- Confirm updated
```

### Example 4: Engage with Network
```
User: "Like and comment on posts from my connections today"
Claude: I'll engage with your network.
- Navigate to feed
- Review recent posts from connections
- Like relevant content
- Add thoughtful comments
- Track engagement
```

## Authentication Flow
1. Navigate to linkedin.com/login via Playwright MCP
2. Enter email and password from canifi-env
3. Handle CAPTCHA if presented (notify user)
4. Complete 2FA if enabled (notify user via iMessage)
5. Verify feed access
6. Maintain session cookies

## Error Handling
- **Login Failed**: Clear cookies, verify credentials
- **Session Expired**: Re-authenticate automatically
- **CAPTCHA Required**: Notify user to complete
- **2FA Required**: iMessage for verification code
- **Rate Limited**: Pause and implement backoff
- **Connection Limit**: Notify of weekly limits
- **Post Failed**: Check content guidelines
- **Profile Restriction**: Notify user of issues

## Self-Improvement Instructions
When encountering new LinkedIn features:
1. Document new UI elements
2. Add support for new post types
3. Log successful networking patterns
4. Update for LinkedIn updates

## Notes
- LinkedIn has strict automation detection
- Premium features require subscription
- Connection limits enforced weekly
- Company pages need admin access
- Post timing affects engagement
- Sales Navigator has different features
- LinkedIn Learning is separate platform
