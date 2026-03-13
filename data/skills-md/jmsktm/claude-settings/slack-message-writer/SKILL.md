---
name: Slack Message Writer
slug: slack-message-writer
description: Craft effective, well-formatted Slack messages for team communication
category: communication
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "write slack message"
  - "compose slack"
  - "draft slack post"
  - "slack announcement"
tags:
  - slack
  - team-communication
  - async-communication
---

# Slack Message Writer

The Slack Message Writer skill helps you create clear, engaging, and appropriately formatted messages for Slack channels and direct messages. Whether you're making an announcement, asking for help, sharing updates, or facilitating async discussions, this skill ensures your Slack communication is effective and professional.

This skill understands Slack's unique communication culture—more casual than email but still professional, heavy use of emoji for tone, threading for context, and formatting for readability. It helps you structure messages that get read, get responses, and move conversations forward.

The skill also leverages Slack-specific features like mentions, formatting, emoji reactions, and threading conventions to maximize engagement and clarity in your team communications.

## Core Workflows

### Workflow 1: Channel Announcement
1. **Define Purpose**: Understand what needs to be communicated
2. **Identify Audience**: Determine which channel(s) and who needs to see it
3. **Structure Message**: Use formatting, emoji, and clear sections
4. **Add Context**: Include links, references, or background
5. **Include CTA**: Make next steps or required actions clear

### Workflow 2: Update or Status Post
1. **Gather Information**: Collect status items, blockers, wins
2. **Format for Scanning**: Use bullets, emoji, and headers
3. **Highlight Changes**: Make what's new or different obvious
4. **Link Resources**: Attach relevant docs, tickets, or threads
5. **Tag Stakeholders**: Mention people who need to see it

### Workflow 3: Question or Request
1. **State the Ask**: Lead with what you need
2. **Provide Context**: Give enough background without overloading
3. **Specify Urgency**: Make timeline clear
4. **Suggest Solutions**: Show you've thought through options
5. **Tag Right People**: Mention specific individuals who can help

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Team announcement | "Write Slack announcement about [topic]" |
| Project update | "Draft project status for #[channel]" |
| Ask for help | "Compose Slack message asking for [help with X]" |
| Share win | "Write celebration message for [achievement]" |
| Request feedback | "Draft feedback request on [topic]" |
| Schedule reminder | "Create reminder message for [deadline/event]" |
| Meeting recap | "Write meeting summary for Slack" |
| Welcome message | "Draft welcome message for new team member" |

## Message Types Supported

- **Announcements**: Company, team, or project updates
- **Status Updates**: Progress reports, sprint updates, blockers
- **Questions**: Requests for help, information, or decisions
- **Celebrations**: Wins, milestones, kudos
- **Meeting Recaps**: Key decisions and action items
- **Requests**: Feedback, reviews, approvals
- **Reminders**: Deadlines, events, action items
- **Introductions**: New team members, new features
- **Incidents**: Bug reports, outage updates, post-mortems
- **Polls/Surveys**: Quick team feedback or decisions

## Best Practices

- **Lead with the Point**: Put the main message in the first line
- **Use Formatting**: Bold for emphasis, code blocks for technical content, bullets for lists
- **Emoji Strategically**: Use to convey tone and organize information (🎉 ✅ ⚠️ 🚀 🔥)
- **Thread Long Discussions**: Use threads to keep channels clean
- **Tag Wisely**: Only @mention when someone needs to see it now
- **Avoid @channel/@here Abuse**: Use sparingly for truly urgent, everyone-needs-to-see-this messages
- **Link, Don't Duplicate**: Reference existing content rather than repeating it
- **Time Zone Aware**: Consider when people will read your message
- **Make it Scannable**: Short paragraphs, clear structure, visual hierarchy
- **Include Action Items**: Make next steps explicit with owners and deadlines

## Slack Formatting Quick Guide

| Format | Syntax | Use Case |
|--------|--------|----------|
| **Bold** | `*text*` | Emphasize key points |
| _Italic_ | `_text_` | Subtle emphasis |
| `Code` | `` `text` `` | Commands, filenames, variables |
| Code Block | ``` ```text``` ``` | Multiple lines of code, logs |
| Quote | `> text` | Reference previous messages |
| Bullet List | `• text` or `- text` | List items |
| Numbered List | `1. text` | Sequential steps |
| Link | `<url\|text>` | Clickable links with custom text |

## Message Structure Templates

### Template 1: Announcement
```
🎉 [Exciting Headline]

[Brief explanation of what's happening]

**What this means:**
• Impact point 1
• Impact point 2
• Impact point 3

**Next steps:**
• Action 1 (Owner - Deadline)
• Action 2 (Owner - Deadline)

**Questions?** Drop them in the thread 👇
```

### Template 2: Status Update
```
📊 [Project Name] Update - [Date]

**✅ Completed:**
• Item 1
• Item 2

**🏃 In Progress:**
• Item 3 (50% complete)
• Item 4 (blocked - see below)

**⚠️ Blockers:**
• Blocker description - needs help from @person

**📅 Next Week:**
• Planned item 1
• Planned item 2
```

### Template 3: Request for Help
```
🤔 Quick question for the team

**Context:** [Brief background]

**What I need:** [Specific ask]

**By when:** [Timeline]

**What I've tried:** [Shows you've done homework]

**Impact:** [Why it matters]

Anyone have experience with this? 🙏
```

## Tone Guidelines

| Context | Tone | Emoji Level | Example Opening |
|---------|------|-------------|-----------------|
| Team Update | Casual, Clear | Medium | "Quick update on the redesign..." |
| Ask for Help | Humble, Specific | Low | "Running into an issue with..." |
| Celebration | Enthusiastic | High | "🎉 Big win today! We just..." |
| Incident Report | Professional, Calm | Low | "⚠️ Heads up on a production issue..." |
| Feedback Request | Open, Collaborative | Medium | "Would love your thoughts on..." |
| Announcement | Clear, Positive | Medium | "📣 Excited to share that..." |

## Channel-Specific Considerations

### #general or #company-wide
- Use sparingly for truly company-wide news
- More formal than team channels
- Avoid @channel unless critical
- Expect higher visibility and scrutiny

### #team or #project channels
- More casual and frequent updates welcome
- Use threads for detailed discussions
- Regular status updates expected
- Emoji and GIFs more acceptable

### Direct Messages
- More conversational tone
- Can be more verbose if needed
- Less need for formatting
- More personal and direct

### #random or #watercooler
- Most casual tone
- Heavy emoji and GIF usage
- Off-topic and fun encouraged
- Low stakes communication

## Best Practices for Common Scenarios

### Announcing Bad News
- Be direct and honest upfront
- Explain what happened and why
- Share what you're doing to fix it
- Give timeline for resolution
- Offer to answer questions in thread

### Asking @channel Questions
- Only use for time-sensitive, everyone-needs-to-see questions
- Consider if a regular message with specific @mentions would work
- Explain why it's urgent in the message
- Provide context so people can help quickly

### Threading Etiquette
- Start threads for detailed discussions
- Reply in thread to keep channel clean
- Summarize thread conclusions in channel
- Don't thread single-response messages

### Editing Messages
- Edit for typos/clarity within a few minutes
- Add "Edit:" note if meaning significantly changed
- Don't edit to hide mistakes that others replied to
- Delete and repost if major changes needed

## Usage Examples

### Example 1: Project Launch Announcement
```
🚀 We're launching the new dashboard!

After 3 months of hard work from @design-team and @eng-team, our redesigned analytics dashboard goes live today at 2pm EST.

**What's new:**
• 50% faster load times
• Real-time data updates (no more refresh button!)
• Mobile-responsive design
• Dark mode support 🌙

**For users:**
No action needed - changes will roll out automatically

**For support team:**
@support-team - updated docs are in the usual spot. Flag any issues in #dashboard-bugs

**Questions?** Drop them below or join the launch party in #celebrations 🎉

Huge thanks to everyone who made this happen! 👏
```

### Example 2: Asking for Technical Help
```
🤔 Need help debugging a React rendering issue

**Context:** Working on the checkout flow, getting infinite re-renders on the payment step

**What I've tried:**
• Checked for missing dependencies in useEffect
• Memoized the payment handler
• Logged the state updates (attached in thread)

**Code:** https://github.com/company/repo/blob/feature/payment/Payment.jsx#L45-L67

**Impact:** Blocking the release scheduled for Friday

Has anyone run into something similar? Would really appreciate a second pair of eyes 🙏

cc @eng-team
```

### Example 3: Weekly Team Update
```
📊 Design Team Update - Week of Jan 6

**✅ Shipped:**
• Mobile navigation redesign (live in production!)
• Updated brand guidelines v2.0
• Onboarding flow improvements

**🏃 In Progress:**
• Settings page refresh (designs in Figma)
• Icon library audit and cleanup
• A/B test setup for homepage hero

**⚠️ Heads Up:**
• Design reviews now moving to Thursdays 2pm
• New design system components coming next week
• Hiring: 2 product designer roles open - refer friends!

**🎉 Shoutout:**
@sarah for crushing the mobile nav under tight deadline
@mike for the amazing new illustrations

Questions or want more details on anything? Thread 'em below 👇
```

## Common Pitfalls to Avoid

- **Wall of Text**: Break up long messages with formatting and white space
- **Vague Subject**: Make the topic clear in the first line
- **No Context**: Don't assume everyone has background knowledge
- **Buried Action Items**: Put clear next steps at the end
- **Overusing @here/@channel**: Save for truly urgent, everyone-must-see messages
- **Ignoring Threads**: Use threads to keep channels organized
- **Too Many Channels**: Cross-post sparingly and with good reason
- **Emoji Overload**: Use emoji to enhance, not replace, clear communication
- **No Follow-up**: Close the loop when issues are resolved

## Integration Points

- **Project Management**: Link to tickets, projects, sprints
- **Documentation**: Reference wikis, docs, playbooks
- **Calendar**: Include meeting links and calendar events
- **GitHub**: Link to PRs, issues, commits
- **Analytics**: Share dashboards and reports
- **Workflow Automation**: Trigger automated messages for key events
