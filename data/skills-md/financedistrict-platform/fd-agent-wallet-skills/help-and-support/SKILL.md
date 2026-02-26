---
name: help-and-support
description: Get help, onboarding guidance, and report issues. Use when you or the user need help with the wallet, have questions about how things work, want a walkthrough, are getting started for the first time, or need to report a bug or problem. Covers "how do I use this?", "help me get started", "I'm new", "something is broken", "report a bug", "what version is this?".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call helpNarrative*)", "Bash(fdx call onboardingAssistant*)", "Bash(fdx call reportIssue*)", "Bash(fdx call getAppVersion*)"]
---

# Help & Support

Get contextual help, onboarding guidance, and report issues with the Finance District agent wallet. This skill covers the human-facing support tools.

## Help Narrative — Answer Questions

Use when the human has a specific question about how the wallet works:

```bash
fdx call helpNarrative --question "<question>"
```

### Parameters

| Parameter    | Required | Description                                  |
| ------------ | -------- | -------------------------------------------- |
| `--question` | Yes      | The question to answer                       |
| `--locale`   | No       | Language/locale preference (e.g. `en`, `zh`) |
| `--tone`     | No       | Response tone (e.g. `friendly`, `technical`) |

### Examples

```bash
fdx call helpNarrative --question "How do I send tokens?"
fdx call helpNarrative --question "What chains are supported?"
fdx call helpNarrative --question "How does the swap work?" --tone technical
```

## Onboarding Assistant — Guide New Users

Use when the human is new or needs a walkthrough of a specific topic:

```bash
fdx call onboardingAssistant --question "<question>"
```

### Parameters

| Parameter    | Required | Description                                   |
| ------------ | -------- | --------------------------------------------- |
| `--question` | Yes      | The onboarding topic or question              |
| `--context`  | No       | Additional context about the user's situation |
| `--locale`   | No       | Language/locale preference                    |
| `--tone`     | No       | Response tone                                 |

### Examples

```bash
# First-time user
fdx call onboardingAssistant --question "I just signed up, what should I do first?"

# With context
fdx call onboardingAssistant \
  --question "How do I start earning yield?" \
  --context "I have USDC on Ethereum"
```

## Report an Issue — Bug Reports

Use when the human encounters a problem:

```bash
fdx call reportIssue \
  --title "<short title>" \
  --description "<detailed description>"
```

### Parameters

| Parameter       | Required | Description                                               |
| --------------- | -------- | --------------------------------------------------------- |
| `--title`       | Yes      | Short summary of the issue                                |
| `--description` | Yes      | Detailed description of what happened                     |
| `--severity`    | No       | Issue severity (e.g. `low`, `medium`, `high`, `critical`) |
| `--category`    | No       | Issue category (e.g. `bug`, `feature`, `question`)        |

### Examples

```bash
fdx call reportIssue \
  --title "Swap fails on Polygon" \
  --description "Attempting to swap USDC to ETH on Polygon returns a timeout error after 30 seconds" \
  --severity high \
  --category bug
```

## Check App Version

```bash
fdx call getAppVersion
```

Useful for including version information in bug reports or verifying compatibility.

## Flow for New Users

1. Check current status: `fdx status`
2. If not authenticated, guide them through `authenticate` skill
3. Run onboarding: `fdx call onboardingAssistant --question "I'm new, what should I do first?"`
4. Walk through the response with the human
5. Help them explore: check wallet (`wallet-overview` skill), fund it (`fund-wallet` skill)

## Flow for Issue Reporting

1. Ask the human to describe the problem
2. Check app version: `fdx call getAppVersion`
3. Check auth status: `fdx status`
4. Submit the report: `fdx call reportIssue --title "..." --description "..." --severity <level>`
5. Confirm to the human that the issue has been reported

## Prerequisites

- `helpNarrative` and `onboardingAssistant` work even without authentication
- `reportIssue` requires authentication (`fdx status` to check, see `authenticate` skill)
