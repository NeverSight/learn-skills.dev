---
name: requirements-gathering
description: Systematic requirements gathering through AskUserQuestion. Use when starting development to clarify app specifications.
---

# Requirements Gathering Skill

Systematically gather requirements through AskUserQuestion to ensure clear specifications before implementation.

## Trigger Conditions

Apply this skill when:
- User invokes `/start-development` command
- Starting development of a new feature or app
- Requirements are unclear and need clarification

## Gathering Process

### Phase 1: Basic Information

**Question 1: App Purpose**
```
Header: "Purpose"
Question: "What is the main purpose of this app?"
Options:
- "Productivity/Task management"
- "E-commerce/Shopping"
- "Social/Communication"
- "Entertainment/Media"
(User can also provide custom answer)
```

**Question 2: Target Users**
```
Header: "Users"
Question: "Who are the target users?"
Options:
- "General consumers (B2C)"
- "Business users (B2B)"
- "Internal company use"
- "Specific community/group"
```

**Question 3: Platform**
```
Header: "Platform"
Question: "Which platforms do you want to support?"
Options:
- "iOS only"
- "Android only"
- "Both iOS and Android"
- "iOS, Android, and Web"
multiSelect: true
```

### Phase 2: Feature Requirements

**Question 4: Core Features**
```
Header: "Features"
Question: "What are the 3-5 main features you need? (Select all that apply)"
Options:
- "User authentication (login/signup)"
- "Data listing and detail views"
- "Create/Edit/Delete operations"
- "Search and filtering"
multiSelect: true
```

**Question 5: MVP Scope**
```
Header: "MVP"
Question: "For the initial release (MVP), which feature is most critical?"
Options:
- "Core functionality working end-to-end"
- "Beautiful UI/UX design"
- "Performance and speed"
- "Comprehensive feature set"
```

**Question 6: Data Storage**
```
Header: "Storage"
Question: "How should data be stored?"
Options:
- "Local only (offline first)"
- "Cloud/Server (Firebase, Supabase, etc.)"
- "Hybrid (local + cloud sync)"
- "No persistent storage needed"
```

### Phase 3: Screen Design

**Question 7: Screen Count**
```
Header: "Screens"
Question: "How many main screens do you expect?"
Options:
- "1-3 screens (simple app)"
- "4-6 screens (medium complexity)"
- "7-10 screens (complex app)"
- "10+ screens (large app)"
```

**Question 8: Navigation Pattern**
```
Header: "Navigation"
Question: "What navigation pattern do you prefer?"
Options:
- "Bottom navigation bar"
- "Drawer/Side menu"
- "Tab bar at top"
- "Simple stack navigation"
```

### Phase 4: Technical Requirements

**Question 9: External APIs**
```
Header: "APIs"
Question: "Do you need external API integrations?"
Options:
- "No external APIs"
- "REST APIs"
- "GraphQL"
- "Third-party services (maps, payment, etc.)"
multiSelect: true
```

**Question 10: Authentication**
```
Header: "Auth"
Question: "What authentication method do you need?"
Options:
- "No authentication needed"
- "Email/Password"
- "Social login (Google, Apple, etc.)"
- "Phone number/OTP"
multiSelect: true
```

**Question 11: Offline Support**
```
Header: "Offline"
Question: "How important is offline functionality?"
Options:
- "Not needed (online only)"
- "Basic offline viewing"
- "Full offline support with sync"
- "Offline-first architecture"
```

### Phase 5: Confirmation

After gathering all responses, compile a summary and confirm with the user.

**Question 12: Requirements Summary**
```
Header: "Confirm"
Question: "Does this requirements summary look correct?"
Options:
- "Yes, proceed with planning"
- "No, I need to modify some requirements"
```

## Output: REQUIREMENTS.md

Generate a `REQUIREMENTS.md` file in the project root with the gathered information:

```markdown
# Project Requirements

## Overview
- **App Name**: [To be determined]
- **Purpose**: [From Question 1]
- **Target Users**: [From Question 2]
- **Platforms**: [From Question 3]

## Features

### Core Features
[From Question 4]

### MVP Scope
[From Question 5]

## Data & Storage
- **Storage Method**: [From Question 6]
- **Offline Support**: [From Question 11]

## Screens & Navigation
- **Expected Screens**: [From Question 7]
- **Navigation Pattern**: [From Question 8]

## Technical Requirements

### Authentication
[From Question 10]

### External Integrations
[From Question 9]

## Next Steps
1. Review and approve this requirements document
2. Enter Plan Mode to design implementation
3. Begin feature-by-feature development

---
Generated on: [Date]
```

## Integration with Workflow

After requirements gathering:

1. Save REQUIREMENTS.md
2. Transition to Plan Mode (EnterPlanMode)
3. Design implementation based on requirements
4. User approves plan
5. Begin implementation with TodoWrite tracking

## Tips for Effective Gathering

1. **Be Specific**: Ask for concrete details, not vague descriptions
2. **Prioritize**: Help users identify MVP features vs nice-to-have
3. **Validate**: Confirm understanding before proceeding
4. **Iterate**: Allow users to modify answers as they think through requirements

## Sample Workflow

```
1. User: "I want to build a todo app"
2. Claude: Invokes requirements-gathering skill
3. Claude: Asks Question 1-12 using AskUserQuestion
4. Claude: Compiles responses into REQUIREMENTS.md
5. Claude: Shows summary and asks for confirmation
6. User: Confirms or requests modifications
7. Claude: Saves REQUIREMENTS.md
8. Claude: Enters Plan Mode for implementation design
```
