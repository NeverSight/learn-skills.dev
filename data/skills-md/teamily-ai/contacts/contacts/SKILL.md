---
name: contacts
description: Smart contact management with profiles, phone numbers, and emails. Add, search, update, and organize your contacts with detailed information and notes.
---

# Contacts Skill

An intelligent contact management skill that stores and manages contact information including names, phone numbers, emails, and detailed profiles.

## 🚀 Quick Usage

**For AI Agents calling this skill:**

```bash
# Add a new contact
python scripts/contacts.py add \
  --name "John Smith" \
  --phone "+1-555-0123" \
  --email "john@example.com" \
  --profile "CTO at TechCorp, loves coffee, met at conference 2024"

# Search contacts
python scripts/contacts.py search "John"

# List all contacts
python scripts/contacts.py list

# Get contact details
python scripts/contacts.py get "John Smith"

# Update contact
python scripts/contacts.py update "John Smith" --email "john.smith@newcompany.com"

# Delete contact
python scripts/contacts.py delete "John Smith"
```

**What it does:**
- ✅ Store contact information persistently
- ✅ Search contacts by name, phone, or email
- ✅ Add detailed profiles and notes
- ✅ Update contact information
- ✅ List all contacts with formatting
- ✅ Delete contacts when needed

**Output:** Clear success messages and formatted contact information.

---

## Core Capabilities

This skill provides **complete contact management**:

1. ✅ **Add Contacts** - Store new contacts with comprehensive information
2. ✅ **Search & Filter** - Find contacts quickly by any field
3. ✅ **View Details** - Display complete contact information
4. ✅ **Update Information** - Modify existing contact details
5. ✅ **Delete Contacts** - Remove contacts when no longer needed
6. ✅ **List All** - View all contacts in organized format

## When to Use This Skill

Use this skill when the user wants to:
- Save someone's contact information
- Look up a phone number or email
- Add notes or profile information about a contact
- Update contact details
- Search through their contacts
- Organize contact information
- Keep track of people they meet

## Complete Workflow

### 1. Understand User Request

When the user wants to manage contacts, identify the action:

**Possible Actions:**
- **Add**: Save new contact information
- **Search**: Find a specific contact
- **List**: Show all contacts
- **Update**: Modify existing information
- **Delete**: Remove a contact
- **Get**: View complete contact details

**Example User Requests:**
- "Save John's contact: +1-555-0123, john@example.com"
- "What's Sarah's email?"
- "Add a note about Mike: he prefers meetings in the morning"
- "Show me all my contacts"
- "Update Lisa's phone number"

**What YOU Must Do:**
- Identify the action type
- Extract all relevant information
- Confirm details before proceeding

### 2. Add New Contact

To add a new contact, gather:

**Required Information:**
- **Name**: Full name of the contact

**Optional Information:**
- **Phone**: Phone number (with country code recommended)
- **Email**: Email address
- **Profile**: Detailed description, notes, tags, or context
- **Company**: Where they work
- **Title**: Their job title
- **Tags**: Categories or labels

**Example:**
```bash
python scripts/contacts.py add \
  --name "Alice Johnson" \
  --phone "+1-555-0199" \
  --email "alice@techstartup.com" \
  --profile "Product Manager at StartupXYZ, expert in AI/ML, met at Tech Summit 2024"
```

### 3. Search Contacts

Search by any field:

```bash
# Search by name
python scripts/contacts.py search "Alice"

# Search by phone (partial match)
python scripts/contacts.py search "555-0199"

# Search by email domain
python scripts/contacts.py search "@techstartup.com"

# Search by profile keywords
python scripts/contacts.py search "Product Manager"
```

**Search Features:**
- Case-insensitive matching
- Partial string matching
- Searches across all fields
- Returns all matching contacts

### 4. View Contact Details

Get complete information:

```bash
python scripts/contacts.py get "Alice Johnson"
```

**Output Format:**
```
📇 Contact Details

Name: Alice Johnson
Phone: +1-555-0199
Email: alice@techstartup.com

Profile:
Product Manager at StartupXYZ, expert in AI/ML, met at Tech Summit 2024

Created: 2024-02-09 10:30:45
Updated: 2024-02-09 10:30:45
```

### 5. Update Contact Information

Modify any field:

```bash
# Update phone number
python scripts/contacts.py update "Alice Johnson" --phone "+1-555-0200"

# Update email
python scripts/contacts.py update "Alice Johnson" --email "alice@newcompany.com"

# Update profile (appends to existing)
python scripts/contacts.py update "Alice Johnson" --profile "Now working at BigTech Inc."

# Replace profile completely
python scripts/contacts.py update "Alice Johnson" --profile "New profile" --replace
```

### 6. List All Contacts

View all saved contacts:

```bash
python scripts/contacts.py list
```

**Output Format:**
```
📇 All Contacts (3 total)

1. Alice Johnson
   Phone: +1-555-0199
   Email: alice@techstartup.com

2. Bob Wilson
   Phone: +1-555-0234
   Email: bob@example.com

3. Carol Davis
   Phone: +1-555-0567
   Email: carol@company.org
```

### 7. Delete Contact

Remove a contact:

```bash
python scripts/contacts.py delete "Alice Johnson"
```

**Note:** This action is permanent and cannot be undone.

## Environment Setup

### 1. Install Dependencies

```bash
cd contacts-skill
pip install -r requirements.txt
```

### 2. Test Installation

```bash
# Add a test contact
python scripts/contacts.py add \
  --name "Test User" \
  --phone "+1-555-9999" \
  --email "test@example.com"

# Verify it was added
python scripts/contacts.py list
```

**No external dependencies required** - All data stored locally in JSON format.

## Data Storage

Contacts are stored in: `~/.claude/skills/contacts/contacts.json`

**Data Format:**
```json
{
  "contacts": [
    {
      "id": "uuid-string",
      "name": "Alice Johnson",
      "phone": "+1-555-0199",
      "email": "alice@techstartup.com",
      "profile": "Product Manager at StartupXYZ...",
      "created_at": "2024-02-09T10:30:45.123Z",
      "updated_at": "2024-02-09T10:30:45.123Z"
    }
  ]
}
```

## Usage Examples

### Example 1: Quick Contact Save

**User:** "Save John's contact: +1-555-0123, john@example.com"

**Agent Actions:**
1. Extract information: name="John", phone="+1-555-0123", email="john@example.com"
2. Run: `python scripts/contacts.py add --name "John" --phone "+1-555-0123" --email "john@example.com"`
3. Confirm success

**Agent Response:**
```
✅ Contact saved successfully!

Name: John
Phone: +1-555-0123
Email: john@example.com
```

### Example 2: Contact Lookup

**User:** "What's Sarah's phone number?"

**Agent Actions:**
1. Search for "Sarah"
2. Run: `python scripts/contacts.py search "Sarah"`
3. Extract and display phone number

**Agent Response:**
```
📇 Found Sarah Miller

Phone: +1-555-0456
Email: sarah@company.com
```

### Example 3: Adding Detailed Profile

**User:** "Add a note about Mike: he prefers morning meetings and loves discussing AI"

**Agent Actions:**
1. Search for "Mike" to find existing contact
2. Update with profile information
3. Run: `python scripts/contacts.py update "Mike" --profile "Prefers morning meetings, loves discussing AI"`

**Agent Response:**
```
✅ Updated Mike's profile

Profile now includes:
- Prefers morning meetings
- Loves discussing AI
```

## Best Practices

### For AI Agents

**When Adding Contacts:**
- Always ask for at least name and one contact method (phone or email)
- Encourage users to add profile information for context
- Use consistent phone number formats (include country code)
- Validate email format before saving

**When Searching:**
- Try multiple search terms if first attempt fails
- Search by partial names if full name doesn't match
- Suggest alternatives if no results found

**When Updating:**
- Confirm which contact to update if multiple matches
- Show before/after comparison
- Preserve existing information unless replacing

**Profile Information Ideas:**
- Where you met them
- Their role/company
- Special interests or preferences
- Communication preferences
- Important dates (birthday, anniversary)
- Conversation topics they enjoy

## Troubleshooting

### Issue: Contact Not Found

**Problem:** "No contact found with name 'John'"

**Solutions:**
- List all contacts to see exact names: `python scripts/contacts.py list`
- Search with partial name: `python scripts/contacts.py search "Joh"`
- Check for typos in the name

### Issue: Duplicate Contacts

**Problem:** Multiple contacts with similar names

**Solution:**
- View all contacts and identify duplicates
- Merge information manually
- Delete the duplicate entry
- Use more specific names (add last name or company)

### Issue: Data File Corrupted

**Problem:** JSON parsing errors

**Solution:**
```bash
# Backup current file
cp ~/.claude/skills/contacts/contacts.json ~/.claude/skills/contacts/contacts.backup.json

# Reset with empty contacts
echo '{"contacts":[]}' > ~/.claude/skills/contacts/contacts.json
```

## Security & Privacy

**Important Considerations:**
- All data stored locally on your machine
- No cloud sync or external transmission
- Backup contacts.json regularly for safety
- Keep sensitive information secure
- Be mindful of profile details you store

## Advanced Features

### Batch Import (Coming Soon)
- Import from CSV
- Import from vCard
- Sync with phone contacts

### Export Options (Coming Soon)
- Export to CSV
- Export to vCard
- Generate contact cards

## Technical Support

- GitHub Issues: Report bugs or request features
- Documentation: See README.md for detailed setup

## License

MIT License - See LICENSE file for details
