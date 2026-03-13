---
name: meetings
description: "Coordinate meetings using calendar and email integration. Find mutual availability, send invites, create calendar events, and manage meeting agendas with prep documents."
version: 1.0.0
author: OpenClaw
entry: ./dist/cli.js
type: script
---

# Meetings Skill

Coordinate meetings seamlessly using calendar and email integration. Schedule meetings, find mutual availability, manage agendas, and send invites all from your agent.

## Features

- **Schedule Meetings**: Find available time slots and create meetings
- **Email Invites**: Automatically send meeting invitations
- **Agenda Management**: Structured agendas with time allocations
- **Prep Documents**: Attach and share pre-meeting materials
- **Meeting Templates**: Pre-defined templates for common meeting types
- **Calendar Integration**: Syncs with Google Calendar

## Installation

```bash
npm install
npm run build
```

## Prerequisites

The meetings skill requires both calendar and email to be connected:

```bash
# Connect Google account with Calendar and Gmail scopes
node ../google-oauth/dist/cli.js connect default calendar email
```

## CLI Usage

### Check Status

```bash
# Check connection status
node dist/cli.js status
```

### Health Check

```bash
node dist/cli.js health
```

### Schedule a Meeting

```bash
# Basic meeting
node dist/cli.js schedule --title "Team Sync" --attendees "alice@example.com,bob@example.com"

# With all options
node dist/cli.js schedule \
  --title "Project Review" \
  --attendees "alice@example.com,bob@example.com,carol@example.com" \
  --duration 90 \
  --description "Quarterly project review" \
  --location "Conference Room A" \
  --days 14 \
  --prep

# With agenda items
node dist/cli.js schedule \
  --title "Sprint Planning" \
  --attendees "dev-team@example.com" \
  --duration 120 \
  --agenda-0 "Review previous sprint" --agenda-0-duration 20 \
  --agenda-1 "Story estimation" --agenda-1-duration 60 \
  --agenda-2 "Sprint commitment" --agenda-2-duration 20 \
  --prep
```

### Quick Schedule

```bash
# Quick 30-minute meeting (minimal options)
node dist/cli.js quick --title "Quick Sync" --attendees "bob@example.com"

# With duration
node dist/cli.js quick --title "Code Review" --attendees "dev@example.com" --duration 60
```

### Use a Template

```bash
# List available templates
node dist/cli.js templates

# Schedule from template
node dist/cli.js template "Standup" --attendees "team@example.com"

# With custom title
node dist/cli.js template "1-on-1" --title "1-on-1 with Alice" --attendees "alice@example.com"
```

### List Meetings

```bash
# List upcoming meetings
node dist/cli.js list

# List more meetings
node dist/cli.js list --days 30 --limit 50

# Filter by status
node dist/cli.js list --status scheduled
```

### Get Meeting Details

```bash
node dist/cli.js get meeting_abc123
```

### Cancel a Meeting

```bash
# Cancel and notify attendees
node dist/cli.js cancel meeting_abc123

# Cancel without notifications
node dist/cli.js cancel meeting_abc123 --no-notify
```

### Delete a Meeting

```bash
node dist/cli.js delete meeting_abc123
```

### Find Available Time

```bash
# Find 60-minute slots in next 7 days
node dist/cli.js free

# Find 30-minute slots in next 3 days
node dist/cli.js free --duration 30 --days 3
```

### Send Invites

```bash
# Re-send invites for a meeting
node dist/cli.js invite meeting_abc123
```

### Send Prep Email

```bash
# Send agenda and prep materials
node dist/cli.js prep meeting_abc123
```

## JavaScript/TypeScript API

### Initialize

```typescript
import { MeetingsSkill } from '@openclaw/meetings';

// Create skill for default profile
const meetings = new MeetingsSkill();

// Or for specific profile
const workMeetings = MeetingsSkill.forProfile('work');
```

### Check Status

```typescript
const status = await meetings.getStatus();
console.log('Connected:', status.connected);
console.log('Calendar:', status.calendarConnected);
console.log('Email:', status.emailConnected);
```

### Schedule a Meeting

```typescript
const result = await meetings.schedule({
  title: 'Team Standup',
  description: 'Daily team sync',
  duration: 30,
  attendees: ['alice@example.com', 'bob@example.com'],
  timeMin: new Date().toISOString(),
  timeMax: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  location: 'Conference Room A',
  agenda: [
    { title: 'What did you do yesterday?', duration: 10 },
    { title: 'What will you do today?', duration: 10 },
    { title: 'Any blockers?', duration: 10 },
  ],
  sendInvites: true,
  sendPrepEmail: true,
});

if (result.success) {
  console.log('Meeting scheduled:', result.meeting?.id);
  console.log('Time:', result.meeting?.startTime);
} else {
  console.error('Failed:', result.error);
}
```

### Schedule from Template

```typescript
const result = await meetings.scheduleFromTemplate('Standup', {
  title: 'Daily Standup',
  attendees: ['team@example.com'],
  timeMin: new Date().toISOString(),
  timeMax: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  sendInvites: true,
});
```

### Find Availability

```typescript
const availability = await meetings.findAvailability({
  attendees: ['alice@example.com', 'bob@example.com'],
  duration: 60,
  timeMin: new Date().toISOString(),
  timeMax: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
});

for (const slot of availability.availableSlots) {
  console.log(`Available: ${slot.start} - ${slot.end}`);
}
```

### List Meetings

```typescript
const meetingList = await meetings.listMeetings({
  status: 'scheduled',
  from: new Date().toISOString(),
  to: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
  limit: 50,
});

for (const meeting of meetingList) {
  console.log(`${meeting.title}: ${meeting.startTime}`);
}
```

### Get Meeting Details

```typescript
const meeting = await meetings.getMeeting('meeting_abc123');

console.log('Title:', meeting?.title);
console.log('Attendees:', meeting?.attendees.map(a => a.email));
console.log('Agenda:', meeting?.agenda.map(item => item.title));
```

### Update a Meeting

```typescript
const updated = await meetings.updateMeeting('meeting_abc123', {
  title: 'Updated Title',
  startTime: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
  endTime: new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString(),
});
```

### Cancel a Meeting

```typescript
// Cancel and notify attendees
await meetings.cancelMeeting('meeting_abc123', true);

// Cancel without notifications
await meetings.cancelMeeting('meeting_abc123', false);
```

### Send Invites

```typescript
const meeting = await meetings.getMeeting('meeting_abc123');
if (meeting) {
  await meetings.sendMeetingInvite(meeting);
}
```

### Send Prep Email

```typescript
const meeting = await meetings.getMeeting('meeting_abc123');
if (meeting) {
  await meetings.sendPrepEmail(meeting);
}
```

## Meeting Templates

### Default Templates

The meetings skill includes several pre-defined templates:

#### Standup
- Duration: 15 minutes
- Agenda: Yesterday's work, Today's plan, Blockers

#### Sprint Planning
- Duration: 2 hours
- Agenda: Review, Goal discussion, Estimation, Commitment

#### 1-on-1
- Duration: 30 minutes
- Agenda: Updates, Priorities, Challenges, Career development

#### Retrospective
- Duration: 1 hour
- Agenda: What went well, Improvements, Action items

#### Review
- Duration: 1 hour
- Agenda: Status overview, Demo, Feedback

### Create Custom Template

```typescript
const template = await meetings.createTemplate({
  name: 'Architecture Review',
  title: 'Architecture Review: {topic}',
  description: 'Review proposed architecture changes',
  duration: 90,
  agenda: [
    { id: '1', title: 'Problem statement', duration: 10 },
    { id: '2', title: 'Proposed solution', duration: 30 },
    { id: '3', title: 'Discussion', duration: 40 },
    { id: '4', title: 'Decision', duration: 10 },
  ],
  prepDocuments: [
    { id: '1', name: 'Architecture Doc', type: 'link', required: true },
  ],
});
```

### List Templates

```typescript
const templates = await meetings.listTemplates();

for (const template of templates) {
  console.log(`${template.name}: ${template.duration} min`);
}
```

## Data Types

### Meeting

```typescript
interface Meeting {
  id: string;
  title: string;
  description?: string;
  startTime: string; // ISO datetime
  endTime: string;   // ISO datetime
  timeZone: string;
  location?: string;
  videoLink?: string;
  attendees: MeetingAttendee[];
  agenda: AgendaItem[];
  prepDocuments: PrepDocument[];
  calendarEventId?: string;
  status: 'draft' | 'scheduled' | 'cancelled' | 'completed';
  notes?: string;
  createdAt: string;
  updatedAt: string;
}
```

### MeetingAttendee

```typescript
interface MeetingAttendee {
  email: string;
  name?: string;
  optional?: boolean;
  responseStatus?: 'needsAction' | 'declined' | 'tentative' | 'accepted';
}
```

### AgendaItem

```typescript
interface AgendaItem {
  id: string;
  title: string;
  duration: number; // in minutes
  presenter?: string;
  description?: string;
}
```

### PrepDocument

```typescript
interface PrepDocument {
  id: string;
  name: string;
  url?: string;
  content?: string;
  type: 'link' | 'file' | 'note';
  required: boolean;
}
```

## Storage

Meeting data is stored in:
```
~/.openclaw/skills/meetings/meetings.db
```

Tables:
- `meetings` - Meeting records
- `templates` - Meeting templates

## Multi-Profile Support

Manage meetings for different accounts:

```typescript
import { MeetingsSkill } from '@openclaw/meetings';

// Work account
const work = MeetingsSkill.forProfile('work');

// Personal account
const personal = MeetingsSkill.forProfile('personal');

// Schedule independently
await work.schedule({ /* work meeting */ });
await personal.schedule({ /* personal meeting */ });
```

Each profile needs separate authentication:
```bash
node ../google-oauth/dist/cli.js connect work calendar email
node ../google-oauth/dist/cli.js connect personal calendar email
```

## Error Handling

```typescript
try {
  const result = await meetings.schedule({
    title: 'Team Meeting',
    duration: 60,
    attendees: ['team@example.com'],
    timeMin: new Date().toISOString(),
    timeMax: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
  });
  
  if (!result.success) {
    console.log('Could not schedule:', result.error);
    console.log('Alternative slots:', result.suggestedSlots);
  }
} catch (error) {
  console.error('Error:', error.message);
}
```

## Testing

```bash
# Type checking
npm run typecheck

# Build
npm run build

# Check status
npm run status

# List templates
npm run cli -- templates

# Schedule a meeting
npm run cli -- quick --title "Test Meeting" --attendees "you@example.com"

# List meetings
npm run cli -- list --days 30
```

## Troubleshooting

### "Not connected" error

Authenticate with google-oauth first:
```bash
node ../google-oauth/dist/cli.js connect default calendar email
```

### Calendar or email not working

Check health of dependencies:
```bash
node ../calendar/dist/cli.js health
node ../email/dist/cli.js health
```

### No available slots found

Expand your search window:
```bash
node dist/cli.js schedule --title "Meeting" --attendees "email@example.com" --days 14
```

## Dependencies

- `@openclaw/calendar`: Calendar integration
- `@openclaw/email`: Email integration
- `@openclaw/google-oauth`: Authentication (via calendar/email)
- `@openclaw/auth-provider`: Base authentication
- `sqlite3`: Local storage

## Security Notes

- OAuth tokens stored encrypted by auth-provider
- Meeting database has 0600 permissions
- Email communications use Gmail API
- Calendar events use Google Calendar API
