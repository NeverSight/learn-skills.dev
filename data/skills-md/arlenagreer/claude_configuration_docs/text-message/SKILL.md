---
name: text-message
description: Send text messages via Apple Messages app with automatic contact lookup and attachment support. This skill should be used when sending SMS/iMessage to contacts. Supports name-based recipient lookup via Google Contacts integration, image/file attachments, and handles missing recipient/message prompts. CRITICAL - Messages are ALWAYS sent individually to each recipient, NEVER as group messages. REQUIRES E.164 phone format (+1XXXXXXXXXX) for reliable delivery. Integrates Arlen's writing style guide for authentic messaging.
category: communication
version: 1.4.0
---

# Text Message Agent Skill

## 🔴 CRITICAL MESSAGE DELIVERY RULE

**MANDATORY: ALL text messages MUST be sent INDIVIDUALLY to each recipient**

- ✅ **CORRECT**: Send same message to Rob → Send same message to Julie → Send same message to Mark
- ❌ **FORBIDDEN**: Send message to Rob, Julie, and Mark in a group chat
- **NO EXCEPTIONS**: This applies to ALL text message requests, regardless of how many recipients

**Why This Matters**:
- Email skill CAN send to multiple recipients simultaneously
- Text-message skill MUST NEVER create group conversations
- Each recipient receives an individual 1-on-1 message
- This is a fundamental behavioral difference between email and text messaging

## Purpose

Send text messages (SMS/iMessage) via Apple Messages app on behalf of Arlen Greer with:
- Automatic contact lookup via Google Contacts for mobile numbers
- **Accent-insensitive name matching** (e.g., "Zoe" matches "Zoë", "Jose" matches "José")
- **Image and file attachment support** (photos, videos, documents, audio, etc.)
- Interactive prompts for missing recipient or message
- Support for both name-based and direct phone number recipients
- Integration with existing contacts skill
- **Individual delivery to each recipient (never group messages)**
- Read existing message threads and retrieve unread messages

## When to Use This Skill

Use this skill when:
- User requests to send a text message or SMS
- Keywords detected: "text", "message", "SMS", "iMessage", "send to", "tell"
- User mentions contacting someone via text
- Mobile communication needs
- User asks to check messages, view unread messages, or read message threads

**Trigger Patterns**:
- "Text [name] [message]"
- "Send [name] a text saying [message]"
- "Message [name] that [message]"
- "Tell [name] [message]" ← NEW: Natural conversation pattern
- "iMessage [name] [message]"
- "Send [name] this photo/image/file" ← NEW: Attachment pattern
- "Text [name] [message] with attachment [path]" ← NEW: Message + attachment

## Core Workflow

### 1. Recipient Resolution

**🔴 CRITICAL - Multiple Recipients Handling**:
When user specifies multiple recipients (e.g., "Text Rob, Julie, and Mark"):
1. Parse and identify ALL recipients from the request
2. Resolve each recipient to a phone number (via contact lookup or direct number)
3. Send the SAME message INDIVIDUALLY to EACH recipient (sequential sends)
4. Confirm completion: "✅ Message sent individually to Rob, Julie, and Mark"
5. **NEVER** create a group message or group chat

**Single Recipient Flow**:

**Name-Based Recipients**:
```bash
# Look up mobile number via contacts skill
~/.claude/skills/contacts/scripts/contacts_manager.rb --search "John Smith"
```

Extract mobile phone number from results:
- Prioritize phone numbers with type "mobile"
- Fall back to any phone number if no mobile type found
- Prompt user if no phone number exists

**Direct Phone Number Recipients**:
- Accept phone numbers in any format: (555) 123-4567, 555-123-4567, 5551234567
- Normalize to E.164 format if needed for Messages app

**Missing Recipient**:
- If no recipient specified, prompt user: "Who would you like to send a text message to?"
- Accept either name or phone number in response
- Process name through contact lookup
- If multiple names provided, prepare to send individually to each

### 2. Message Content

**Missing Message**:
- If no message specified, prompt user: "What message would you like to send?"
- Wait for user response before proceeding

**Message Validation**:
- No length restrictions (Messages app handles SMS vs iMessage)
- Preserve formatting and emoji
- No modifications to user's message content

### 3. Attachment Handling (NEW)

**Attachment Support**:
- **Supported formats**: Images (JPG, PNG, GIF, HEIC, etc.), Videos (MP4, MOV, etc.), Audio (MP3, M4A, etc.), Documents (PDF, DOC, etc.), Archives (ZIP, etc.)
- **Path requirements**: Provide absolute or relative file path
- **Validation**: Script validates file exists, is readable, and checks format
- **Optional message**: Can send attachment with or without text message

**Attachment-only message**:
```bash
~/.claude/skills/text-message/scripts/send_message.sh "PHONE_NUMBER" "" "/path/to/photo.jpg"
```

**Message with attachment**:
```bash
~/.claude/skills/text-message/scripts/send_message.sh "PHONE_NUMBER" "Check out this photo!" "/path/to/photo.jpg"
```

### 4. Send Message

**Use AppleScript via Messages app**:
```bash
# Text-only message
~/.claude/skills/text-message/scripts/send_message.sh "PHONE_NUMBER" "MESSAGE_TEXT"

# Message with attachment
~/.claude/skills/text-message/scripts/send_message.sh "PHONE_NUMBER" "MESSAGE_TEXT" "/path/to/file"

# Attachment-only (no text)
~/.claude/skills/text-message/scripts/send_message.sh "PHONE_NUMBER" "" "/path/to/file"
```

**🔴 CRITICAL - Phone Number Format for Delivery**:
For maximum delivery reliability, ALWAYS use **E.164 format** (`+1XXXXXXXXXX`) when sending via AppleScript:
- ✅ **CORRECT**: `+17604199142` (full international format)
- ⚠️ **RISKY**: `7604199142` (may fail delivery, especially for SMS)
- ❌ **WRONG**: `(760) 419-9142` (formatted numbers may be rejected)

**Why This Matters**:
- AppleScript `send to buddy` requires consistent phone number format
- Missing `+1` country code can cause "Not Delivered" errors
- Formatted numbers with parentheses/dashes may fail silently
- E.164 format works for both iMessage AND SMS delivery

**Format Conversion**:
```bash
# Remove all non-digits and add +1 for US numbers
PHONE=$(echo "$PHONE" | sed 's/[^0-9]//g' | sed 's/^1*//')
PHONE="+1${PHONE}"
```

**🔴 CRITICAL - Special Character Handling**:
Messages with ANY apostrophes or single quotes can cause AppleScript failures:
- ✅ **SAFE**: "We just get hot, hotter, and why did I move here"
- ✅ **SAFE**: "I will not be there" (no contractions)
- ⚠️ **FAILS**: "We just get 'hot,' 'hotter,' and 'why did I move here again?'" (nested quotes)
- ⚠️ **FAILS**: "I won't be there" (contractions with apostrophes)
- ⚠️ **FAILS**: "It's time to go" (possessives and contractions)
- **Solution**: Remove ALL apostrophes - no contractions, no possessives, no nested quotes
- **Root Cause**: AppleScript string escaping fails with ANY apostrophe/single quote character, even after sed escaping
- **Recommendation**: Convert contractions to full words (won't → will not, it's → it is, can't → cannot)

The script will:
1. Validate phone number format and convert to E.164 if needed
2. Validate attachment file if provided (exists, readable, supported format)
3. Open Messages app if not running
4. Send message and/or attachment via AppleScript with proper phone format
5. Return status confirmation with attachment info if applicable
6. **Note**: May fail with ANY apostrophes/single quotes - remove all contractions and possessives if send fails

### 4. Read Messages (NEW)

**Read existing message threads and unread messages**:
```bash
~/.claude/skills/text-message/scripts/read_messages.sh [OPTIONS]
```

**Common Operations**:
```bash
# Get unread messages
~/.claude/skills/text-message/scripts/read_messages.sh --unread

# Get last 20 messages
~/.claude/skills/text-message/scripts/read_messages.sh --limit 20

# Get messages from specific contact
~/.claude/skills/text-message/scripts/read_messages.sh --from "Rob"

# Get unread messages from Julie
~/.claude/skills/text-message/scripts/read_messages.sh --unread --from "Julie"
```

**Returns JSON** with message text, sender phone number/iMessage ID, timestamp, read status, and conversation identifier.

**🔴 CRITICAL - Sender Name Resolution Required**:
When presenting messages to the user, you MUST:
1. Extract the phone number or iMessage ID from the `from` field in the JSON response
2. Look up the sender's name via contacts skill: `~/.claude/skills/contacts/scripts/contacts_manager.rb --search "PHONE_NUMBER"`
3. Display both the **sender name** (if found in contacts) and phone number/ID
4. Format: "**From: [Name]** ([phone/ID]) - [timestamp]"
5. If contact not found: "**From: [phone/ID]** *(Unknown contact)* - [timestamp]"

**Example workflow**:
```bash
# 1. Get messages
MESSAGES=$(~/.claude/skills/text-message/scripts/read_messages.sh --limit 3)

# 2. For each message, look up sender by phone number
PHONE=$(echo $MESSAGES | jq -r '.messages[0].from')
CONTACT=$(~/.claude/skills/contacts/scripts/contacts_manager.rb --search "$PHONE")
NAME=$(echo $CONTACT | jq -r '.contacts[0].name.display_name')

# 3. Present to user with name AND number
echo "From: $NAME ($PHONE) - Message text here"
```

**Permission Required**: Full Disk Access for Terminal in System Settings > Privacy & Security

## Writing Style Integration

**Arlen's Authentic Voice** - This skill integrates Arlen's personal writing style for authentic text messaging.

**Style Guide Reference**: `~/.claude/skills/email/references/writing_style_guide.md`

**Key Texting Adaptations** (adapted from email style guide):
- **Conversational but clear** - Texts are more casual than emails, but still professional
- **Direct and brief** - Get to the point quickly, texting favors brevity
- **Natural contractions** - Use "I'm", "I'll", "we're" freely in texts (BUT see apostrophe handling below)
- **Friendly tone** - Warm and approachable, less formal than email
- **Emoji usage** - Appropriate in texting contexts for tone and friendliness

**Text Message Adaptations**:
```
Email: "Hi Mark, I've successfully integrated the database connection..."
Text: "Hey! Got the database integrated 👍"

Email: "Let me know if you run into any issues."
Text: "Let me know if any issues come up"

Email: "Thank you, -Arlen"
Text: "Thanks!" or just the message without signature
```

**🔴 CRITICAL - Apostrophe Handling Conflict**:
While Arlen's natural writing style uses contractions (I'm, I'll, won't, can't), AppleScript messaging has a technical limitation that causes ALL apostrophes to fail message delivery.

**Resolution Strategy**:
1. **First Priority**: Natural voice preservation when possible
2. **Technical Constraint**: Remove ALL apostrophes if send fails
3. **Adaptive Approach**:
   - Attempt natural message first (with contractions if user wrote them)
   - If send fails, automatically remove apostrophes and retry
   - Expand contractions: won't → will not, I'm → I am, can't → cannot
   - Rephrase possessives: Tait's → the one Tait has

**Best Practice**: For critical or time-sensitive messages, proactively avoid apostrophes. For casual messages, attempt natural style first and adapt if needed.

## Bundled Resources

### Scripts

**`scripts/send_message.sh`**
- Send text message via Apple Messages app using AppleScript
- Handles phone number validation and normalization
- Opens Messages app if needed
- Returns JSON status response

**`scripts/read_messages.sh`** (NEW)
- Read existing message threads from Messages database
- Filter by read/unread status
- Filter by sender name or number
- Limit results and retrieve conversation history
- Returns JSON with message details

**Usage**:
```bash
~/.claude/skills/text-message/scripts/send_message.sh "+15551234567" "Hello, this is a test message"
```

**Output**:
- Success: `{"status": "success", "recipient": "+15551234567", "message": "Hello..."}`
- Error: `{"status": "error", "code": "ERROR_CODE", "message": "..."}`

**Exit Codes**:
- 0: Success
- 1: Invalid arguments
- 2: Messages app error
- 3: AppleScript execution error

### References

**`references/phone_number_formats.md`**
- Supported phone number formats
- Normalization rules
- International number handling

**`references/contact_integration.md`**
- Integration patterns with contacts skill
- Mobile number extraction logic
- Fallback strategies

**`references/reading_messages.md`** (NEW)
- Reading message threads from Messages database
- Filtering and querying messages
- Database schema reference
- Permission setup and troubleshooting

## Integration with Contacts Skill

The text-message skill leverages the contacts skill for recipient lookup:

```bash
# 1. Search for contact by name
CONTACT=$(~/.claude/skills/contacts/scripts/contacts_manager.rb --search "Rob")

# 2. Extract mobile number (prioritize "mobile" type)
PHONE=$(echo $CONTACT | jq -r '.contacts[0].phones[] | select(.type == "mobile") | .value')

# 3. Fall back to first available phone if no mobile
if [ -z "$PHONE" ]; then
  PHONE=$(echo $CONTACT | jq -r '.contacts[0].phones[0].value')
fi

# 4. Send message
~/.claude/skills/text-message/scripts/send_message.sh "$PHONE" "Your message here"
```

## Workflow Examples

### Example 1: Send to Named Contact
```
User: "Send Rob a text saying I'm running 10 minutes late"

Steps:
1. Look up "Rob" in contacts
2. Extract mobile number
3. Send message: "I'm running 10 minutes late"
4. Confirm: "✅ Message sent to Rob (+1-555-123-4567)"
```

### Example 2: Multiple Recipients (Individual Sends)
```
User: "Text Rob, Julie, and Mark that the meeting is postponed"

🔴 CRITICAL WORKFLOW - Individual sends only:

Steps:
1. Parse recipients: ["Rob", "Julie", "Mark"]
2. Look up each contact and extract mobile numbers:
   - Rob: +1-555-123-4567
   - Julie: +1-555-234-5678
   - Mark: +1-555-345-6789
3. Send INDIVIDUALLY to each recipient (one-by-one):
   a. Send to Rob: "The meeting is postponed"
   b. Send to Julie: "The meeting is postponed"
   c. Send to Mark: "The meeting is postponed"
4. Confirm: "✅ Message sent individually to Rob, Julie, and Mark"

❌ FORBIDDEN: Creating group chat with all three recipients
✅ REQUIRED: Three separate 1-on-1 conversations
```

### Example 3: Missing Recipient
```
User: "Send a text message"

Steps:
1. Prompt: "Who would you like to send a text message to?"
2. User responds: "Julie Whitney"
3. Look up Julie in contacts
4. Prompt: "What message would you like to send?"
5. User responds: "Meeting confirmed for tomorrow at 2pm"
6. Send message
7. Confirm: "✅ Message sent to Julie Whitney"
```

### Example 4: Direct Phone Number
```
User: "Text (555) 123-4567 to confirm the appointment"

Steps:
1. Normalize phone number: +15551234567
2. Prompt: "What message would you like to send?"
3. User responds: "Confirming appointment"
4. Send message
5. Confirm: "✅ Message sent to (555) 123-4567"
```

### Example 5: No Contact Found
```
User: "Send a text to John"

Steps:
1. Search contacts for "John"
2. No match found (or no phone number)
3. Prompt: "I couldn't find a phone number for John. Please provide a phone number."
4. User responds: "555-123-4567"
5. Send message with provided number
```

### Example 5a: Send Image to Contact (NEW)
```
User: "Send Rob this photo: ~/Desktop/vacation.jpg"

Steps:
1. Look up "Rob" in contacts
2. Extract mobile number: +1-555-123-4567
3. Validate attachment file exists and is readable
4. Prompt: "What message would you like to include with the photo?" (or send without message)
5. User responds: "Check out our vacation!" (or "" for no message)
6. Send message with attachment:
   ~/.claude/skills/text-message/scripts/send_message.sh "+15551234567" "Check out our vacation!" "/Users/user/Desktop/vacation.jpg"
7. Confirm: "✅ Message and photo sent to Rob (+1-555-123-4567)"
```

### Example 5b: Send Attachment Only (NEW)
```
User: "Text Julie this PDF: ~/Documents/report.pdf"

Steps:
1. Look up "Julie" in contacts
2. Extract mobile number: +1-555-234-5678
3. Validate PDF file exists
4. Send attachment without text message:
   ~/.claude/skills/text-message/scripts/send_message.sh "+15552345678" "" "/Users/user/Documents/report.pdf"
5. Confirm: "✅ PDF attachment sent to Julie (+1-555-234-5678)"
```

### Example 5c: Send Video with Message (NEW)
```
User: "Send Mark this video with a message: ~/Movies/demo.mp4 - 'Here's the demo video we discussed'"

Steps:
1. Look up "Mark" in contacts
2. Extract mobile number: +1-555-345-6789
3. Validate video file exists and is readable
4. Send message with video attachment:
   ~/.claude/skills/text-message/scripts/send_message.sh "+15553456789" "Here's the demo video we discussed" "/Users/user/Movies/demo.mp4"
5. Confirm: "✅ Message and video sent to Mark (+1-555-345-6789)"
```

### Example 6: Check Unread Messages
```
User: "Do I have any unread text messages?"

Steps:
1. Run: ~/.claude/skills/text-message/scripts/read_messages.sh --unread
2. Parse JSON response to extract phone numbers for each message
3. Look up each sender's name via contacts skill:
   - Contact lookup for +15551234567 → Rob Lopez
   - Contact lookup for +15552345678 → Julie Whitney
   - Contact lookup for +15553456789 → Mark Davis
4. Display with names AND phone numbers:
   "📱 You have 3 unread messages:
   - **Rob Lopez** ((555) 123-4567): 'Hey, are you free for lunch?'
   - **Julie Whitney** ((555) 234-5678): 'Meeting confirmed for 2pm'
   - **Mark Davis** ((555) 345-6789): 'Thanks for the update'"
```

### Example 7: Read Recent Conversation
```
User: "Show me my recent messages with Rob"

Steps:
1. Run: ~/.claude/skills/text-message/scripts/read_messages.sh --from "Rob" --limit 10
2. Parse JSON response
3. Display conversation thread with timestamps:
   "💬 Recent conversation with Rob:
   [2:30 PM] You: 'Sure! What time?'
   [2:28 PM] Rob: 'Want to grab lunch?'
   [11:45 AM] You: 'Thanks, see you then'
   [11:42 AM] Rob: 'Meeting at 2pm confirmed'"
```

### Example 8: Check and Reply to Unread
```
User: "Check my unread messages and reply to Rob"

Steps:
1. Run: ~/.claude/skills/text-message/scripts/read_messages.sh --unread --from "Rob"
2. Extract phone number from JSON and look up contact name
3. Display with name AND phone: "📱 Unread from **Rob Lopez** ((555) 123-4567): 'Are you free for lunch?'"
4. Prompt: "What would you like to reply?"
5. User responds: "Yes, 12:30 works for me"
6. Look up Rob's mobile number via contacts (if not already retrieved)
7. Send reply: ~/.claude/skills/text-message/scripts/send_message.sh "$PHONE" "Yes, 12:30 works for me"
8. Confirm: "✅ Reply sent to Rob Lopez"
```

## Error Handling

**Contact Lookup Fails**:
1. **STOP** messaging workflow immediately
2. Display error: "❌ Contact lookup failed: No contact found for '[Name]'"
3. **PROMPT** user: "Please provide a phone number for [Name] to continue."
4. **WAIT** for user response - do not assume or guess
5. Only proceed once valid phone number provided

**No Phone Number in Contact**:
1. Display: "❌ [Name] doesn't have a phone number in contacts"
2. **PROMPT** user: "Please provide a phone number to send the message."
3. Wait for user response
4. Proceed with provided number

**Messages App Not Available**:
1. Check if Messages app exists on system
2. If not available, display: "❌ Apple Messages app not found. This skill requires macOS with Messages app."
3. Offer alternative: "Would you like me to help draft an email instead?"

**AppleScript Permission Denied**:
1. Display: "❌ Permission denied to control Messages app"
2. Instruct: "Please grant System Events permission in System Settings > Privacy & Security > Automation"
3. Wait for user to grant permission before retrying

**Attachment File Not Found** (NEW):
1. Display: "❌ Attachment file not found: [path]"
2. **PROMPT** user: "Please verify the file path and try again."
3. Wait for corrected path or user decision to proceed without attachment

**Attachment File Not Readable** (NEW):
1. Display: "❌ Cannot read attachment file: [path]"
2. Check file permissions
3. Instruct: "Please check file permissions or try a different file."

**Unsupported File Format** (NEW):
1. Display warning: "⚠️ File type '[extension]' may not be supported by Messages app"
2. Ask user: "Would you like to try sending anyway?"
3. Proceed based on user confirmation

**Special Characters Causing Send Failure** (NEW):
When send_message.sh fails with SEND_FAILED error code:

1. **Common Cause**: ANY apostrophes or single quotes in message text
   - Nested quotes: 'hot,' 'hotter,' or 'why did I move here?'
   - Contractions: won't, can't, it's, don't, shouldn't
   - Possessives: Tait's, Grace's, user's

2. **Solution**: Remove ALL apostrophes
   - Remove nested quotes: 'hot' → hot
   - Expand contractions: won't → will not, it's → it is, can't → cannot
   - Rephrase possessives: Tait's candy → the candy Tait has, Grace's bag → the bag Grace has
   - Keep emoji and other characters intact

3. **Testing Strategy**:
   - First attempt with original message
   - If fails, scan for ANY apostrophes (contractions, possessives, quotes)
   - Remove/replace all apostrophes and retry
   - Inform user of simplification made

4. **Examples**:
   ```bash
   # Original (FAILS - nested quotes):
   "We get 'hot,' 'hotter,' and 'why did I move here again?'"
   # Fixed:
   "We get hot, hotter, and why did I move here again?"

   # Original (FAILS - contraction):
   "I won't be there at 2pm"
   # Fixed:
   "I will not be there at 2pm"

   # Original (FAILS - multiple apostrophes):
   "It's Grace's candy and she won't share"
   # Fixed:
   "It is the candy Grace has and she will not share"
   ```

**Message Not Delivered** (NEW):
When Messages app shows "Not Delivered" with red exclamation mark:

1. **Immediate Diagnosis**:
   - Check if message appears in Messages app conversation with "Not Delivered" indicator
   - Verify phone number format used in failed attempt

2. **Root Causes**:
   - **Phone Number Format**: Most common cause - missing `+1` or improper formatting
   - **iMessage/SMS Routing**: Recipient's iMessage temporarily offline, SMS fallback failed
   - **Network Connectivity**: Temporary cellular/internet connection issue
   - **Messages Service**: Apple's messaging service experiencing issues

3. **Resolution Steps**:
   ```bash
   # Step 1: Retry with E.164 format (fixes 80% of issues)
   osascript -e 'tell application "Messages"
       send "MESSAGE TEXT" to buddy "+1PHONENUMBER"
   end tell'

   # Step 2: If still fails, verify Messages app connectivity
   osascript -e 'tell application "Messages"
       get properties of service 1
   end tell'

   # Step 3: Check for multiple delivery attempts in database
   ~/.claude/skills/text-message/scripts/read_messages.sh --limit 5
   ```

4. **Manual Fallback**:
   - If automated retry fails, instruct user to manually tap red exclamation mark in Messages app
   - Select "Try Again" from the popup menu
   - Or delete failed message and manually type/send

5. **Success Indicators**:
   - Message shows "Delivered" (iMessage) or no error indicator (SMS)
   - Message timestamp appears in conversation
   - No red exclamation mark present

## Pre-Send Checklist

**🔴 CRITICAL - Multiple Recipients Check**:
- ✅ If multiple recipients detected, verified they will receive INDIVIDUAL messages
- ✅ Confirmed NO group message will be created
- ✅ Each recipient will receive separate 1-on-1 message

**Recipient Validation**:
- ✅ All recipients resolved (name → phone number OR direct phone number)
- ✅ All phone numbers format validated
- ✅ Confirmation that recipients are correct

**Message Validation**:
- ✅ Message content provided (or intentionally empty for attachment-only)
- ✅ No modifications to user's intended message (except removing ALL apostrophes)
- ✅ Emoji and formatting preserved
- ✅ **CRITICAL**: ALL apostrophes removed (won't → will not, it's → it is, Grace's → the one Grace has)

**Attachment Validation** (NEW):
- ✅ File path validated if attachment provided
- ✅ File exists and is readable
- ✅ File format checked (warning given for unsupported types)
- ✅ Absolute path resolved for AppleScript

**System Validation**:
- ✅ Messages app available on system
- ✅ AppleScript permissions granted
- ✅ Script execution successful for each recipient

## Quick Reference

**Contact Lookup**:
```bash
~/.claude/skills/contacts/scripts/contacts_manager.rb --search "First Last"
```

**Send Message**:
```bash
# Text only
~/.claude/skills/text-message/scripts/send_message.sh "PHONE" "MESSAGE"

# With attachment (NEW)
~/.claude/skills/text-message/scripts/send_message.sh "PHONE" "MESSAGE" "/path/to/file"

# Attachment only (NEW)
~/.claude/skills/text-message/scripts/send_message.sh "PHONE" "" "/path/to/file"
```

**Read Messages**:
```bash
# Get unread messages
~/.claude/skills/text-message/scripts/read_messages.sh --unread

# Get recent messages from specific contact
~/.claude/skills/text-message/scripts/read_messages.sh --from "Name" --limit 20

# Get all unread from specific contact
~/.claude/skills/text-message/scripts/read_messages.sh --unread --from "Name"
```

**Phone Number Extraction** (from contact JSON):
```bash
# Prioritize mobile
jq -r '.contacts[0].phones[] | select(.type == "mobile") | .value'

# Fall back to first phone
jq -r '.contacts[0].phones[0].value'
```

## Best Practices

1. **Individual Messages Always**: When multiple recipients, send individually (never group messages)
2. **Always Resolve Sender Names**: When reading messages, ALWAYS look up sender names via contacts and display both name and phone/ID
3. **Always Confirm Recipients**: Before sending, confirm all recipients with user
4. **Preserve Message Intent**: Don't modify user's message unless asked (except removing ALL apostrophes to prevent failures)
5. **Handle Missing Info Gracefully**: Use interactive prompts rather than assumptions
6. **Respect Privacy**: Don't log message contents beyond what's needed for confirmation
7. **Error Recovery**: Provide clear next steps when errors occur
8. **Rate Limiting**: Add small delay between messages when sending to multiple recipients
9. **Attachment Validation** (NEW): Always validate file exists and is readable before sending
10. **File Path Resolution** (NEW): Convert relative paths to absolute paths for reliability
11. **Format Warnings** (NEW): Warn users about potentially unsupported file formats
12. **Remove ALL Apostrophes** (NEW): Remove contractions, possessives, and quotes to prevent AppleScript failures

## Limitations

- **macOS Only**: Requires Apple Messages app (macOS)
- **Contacts Access**: Requires Google Contacts integration for name lookup
- **Messages App Permissions**: User must grant automation permissions
- **iMessage vs SMS**: Messages app determines delivery method (iMessage or SMS)
- **No Group Messages**: By design, cannot create group chats (individual messages only)

## Version History

- **1.4.0** (2025-11-01) - **WRITING STYLE INTEGRATION**: Added comprehensive integration with Arlen's personal writing style guide from email skill. New "Writing Style Integration" section documents how to adapt email communication patterns to text messaging context. Includes key texting adaptations (conversational, brief, natural contractions), text message examples, and critical apostrophe handling conflict resolution strategy. Balances natural voice preservation with AppleScript technical limitations. Reference: `~/.claude/skills/email/references/writing_style_guide.md`
- **1.3.3** (2025-11-01) - **CRITICAL UPDATE - ALL APOSTROPHES**: Discovered AppleScript fails with ANY apostrophes/single quotes, not just nested ones. Updated documentation throughout to reflect that ALL apostrophes must be removed including: contractions (won't → will not, it's → it is, can't → cannot), possessives (Grace's → the one Grace has, Tait's → the one Tait has), and nested quotes ('hot' → hot). Updated Special Character Handling section, Error Handling examples, Pre-Send Checklist, and Best Practices #4 and #12. Root cause: AppleScript string escaping completely fails with ANY apostrophe character, even after sed escaping. Solution: Expand all contractions, rephrase all possessives, remove all quotes.
- **1.3.2** (2025-11-01) - **SPECIAL CHARACTER HANDLING**: Documented AppleScript failure when messages contain nested single quotes/apostrophes (e.g., 'hot,' 'hotter,'). Added error handling guidance, troubleshooting steps, and best practice to simplify punctuation in messages. Updated Pre-Send Checklist, Error Handling section with new "Special Characters Causing Send Failure" guidance, and Best Practices with recommendation #12. Root cause: AppleScript string escaping struggles with nested quotes even after sed escaping. Solution: Remove or replace nested quotes before sending. Includes example workflows and testing strategy.
- **1.3.1** (2025-11-01) - **CRITICAL DELIVERY FIX**: Added comprehensive phone number format requirements and delivery troubleshooting guidance. Documented that AppleScript `send to buddy` REQUIRES E.164 format (`+1XXXXXXXXXX`) for reliable delivery to both iMessage and SMS recipients. Missing `+1` country code or formatted numbers with parentheses/dashes can cause "Not Delivered" errors. Added troubleshooting section for delivery failures with diagnosis steps, root cause analysis, resolution workflow, and manual fallback procedures. Includes format conversion examples and success indicators. This addresses 80% of message delivery failures.
- **1.3.0** (2025-11-01) - **MAJOR FEATURE**: Added comprehensive attachment support for images, videos, audio, documents, and other file types. Enhanced `send_message.sh` to accept optional third parameter for file attachments. Includes file validation (existence, readability, format checking), absolute path resolution, and support for sending attachments with or without text messages. Updated SKILL.md with attachment workflows, error handling, and usage examples. Supports all common media formats supported by Apple Messages app.
- **1.2.4** (2025-11-01) - **CRITICAL FIX**: Fixed SMS delivery issue. Previously, messages would only send successfully to iMessage users (iPhone/Mac). Updated AppleScript to allow Messages app to auto-route to either iMessage or SMS based on recipient capability. Now works correctly for both Apple users (iMessage) and non-Apple users (SMS). Changed from explicitly selecting iMessage service to using `send to buddy` which lets Messages app choose the appropriate delivery method.
- **1.2.3** (2025-11-01) - **CRITICAL UPDATE**: Added mandatory sender name resolution when reading messages. When presenting messages to users, skill MUST look up sender names via contacts script and display both the contact name and phone number/iMessage ID. Updated workflow examples and best practices to enforce this requirement. Format: "**From: [Name]** ([phone/ID]) - [timestamp]" or "**From: [phone/ID]** *(Unknown contact)* - [timestamp]".
- **1.2.2** (2025-11-01) - Added accent-insensitive contact name matching to contacts script. Names with diacritics (ë, ñ, é, etc.) can now be searched without accents. For example, "Zoe" will match "Zoë", "Jose" matches "José", etc. Uses Unicode NFD normalization to decompose characters and strip combining marks for matching.
- **1.2.1** (2025-11-01) - Enhanced contacts script phone number search to support multiple formats including `+1` country code prefix. Phone numbers are now normalized by removing all non-digit characters and stripping leading `1` for US numbers, enabling searches with formats like `+1 (619) 846-1019`, `+16198461019`, `(619) 846-1019`, or `6198461019` to all match contacts with `619-846-1019`.
- **1.2.0** (2025-11-01) - Added ability to read existing message threads and retrieve unread messages via `read_messages.sh` script. Includes SQLite database access to Messages chat.db, filtering by read/unread status, sender-based filtering, and conversation history retrieval. Added comprehensive reading_messages.md reference documentation and workflow examples for checking unread messages and replying to conversations.
- **1.1.0** (2025-11-01) - **CRITICAL UPDATE**: Added mandatory individual message delivery for multiple recipients. Messages are NEVER sent as group chats. Each recipient receives a separate 1-on-1 message. Updated workflow examples, pre-send checklist, and best practices to enforce this behavior.
- **1.0.0** (2025-11-01) - Initial text-message skill creation with contact integration, interactive prompts, and AppleScript-based message sending

---

*This skill enables seamless text messaging via Apple Messages with intelligent contact lookup and user-friendly prompts for missing information.*
