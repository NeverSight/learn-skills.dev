---
name: calendar-event-manager
description: Create macOS Calendar events with sound alarms and paired Reminders. TRIGGERS - add event, calendar event, create reminder, birthday party, schedule event, RSVP, don't miss, set reminder
allowed-tools: Bash, Read, AskUserQuestion
---

# Calendar Event Manager

Create macOS Calendar events with **tiered sound alarms** and **paired Reminders** so events are never missed across Mac and iOS.

## CRITICAL RULES (Hard-Learned Truths 2026-02-12)

> **These rules are NON-NEGOTIABLE. Violating any of them defeats the purpose of this skill.**

### 1. Calendar + Reminders ALWAYS Together

Every event MUST create BOTH:

- **Calendar event** with multiple `sound alarm` entries (custom sound per tier)
- **Reminders** (3 minimum) as a separate notification channel

Never create one without the other.

### 2. Use `sound alarm`, NOT `display alarm`

```applescript
-- CORRECT: audible alert with custom sound
make new sound alarm at end of sound alarms with properties {trigger interval:-60, sound name:"Glass"}

-- WRONG: silent visual banner only
make new display alarm at end of display alarms with properties {trigger interval:-60}
```

Each alarm supports its own `sound name` property. Use DIFFERENT sounds for different tiers so the user knows which alert level it is by sound alone.

### 3. ONLY Long Sounds (>= 1.4 seconds)

Short sounds get missed and ignored. NEVER use sounds under 1.4 seconds.

**APPROVED sounds only:**

| Sound     | Duration | Use For                   |
| --------- | -------- | ------------------------- |
| Funk      | 2.16s    | At event time (loudest)   |
| Glass     | 1.65s    | 1 hour before             |
| Pop       | 1.63s    | Morning-of / 3 hrs before |
| Sosumi    | 1.54s    | Day-before                |
| Ping      | 1.50s    | 30 min before             |
| Submarine | 1.49s    | Alternative               |
| Blow      | 1.40s    | Gentle early reminder     |

**BANNED sounds:** Hero, Basso, Bottle, Purr, Frog, Morse, Tink (all < 1.4s)

### 4. Multiple Early Reminders Are Mandatory

Minimum alarm tiers for any event:

| Tier            | Trigger   | Calendar Sound | Reminder          |
| --------------- | --------- | -------------- | ----------------- |
| 1 day before    | -1440 min | Blow           | "TOMORROW: ..."   |
| Morning-of 9 AM | Absolute  | Sosumi         | "TODAY: ..."      |
| 3 hours before  | -180 min  | Pop            | (via Calendar)    |
| 1 hour before   | -60 min   | Glass          | (via Calendar)    |
| 30 min before   | -30 min   | Ping           | (via Calendar)    |
| At event time   | 0 min     | Funk           | Due-time reminder |

### 5. macOS Notification Settings Prerequisite

Calendar notifications must be enabled in System Settings:

- System Settings > Notifications > Calendar > Allow Notifications = ON
- Alert style = Banners or Alerts
- Play sound = ON

Open with: `open "x-apple.systempreferences:com.apple.Notifications-Settings.extension"`

---

## TodoWrite Task Templates

### Template A: Create Event from Invitation

```
1. Extract event details (title, date, time, location, notes, RSVP)
2. Create Calendar event with 6-tier sound alarms (Blow, Sosumi, Pop, Glass, Ping, Funk)
3. Create 3 Reminders (TOMORROW, TODAY morning, due-time)
4. Verify event and reminders created
5. Report full schedule to user
```

### Template B: Create Event from User Description

```
1. Ask user for: event name, date/time, duration, location
2. Create Calendar event with 6-tier sound alarms
3. Create 3 Reminders
4. Verify event and reminders created
5. Report full schedule to user
```

### Template C: Test Notification Setup

```
1. Create test Calendar event 3 min in future with sound alarms (1 min, 2 min tiers)
2. Create test Reminder 2 min in future
3. Wait for user confirmation of notifications
4. Clean up test event and reminders
```

---

## AppleScript Patterns

### Full Event Creation (Copy-Paste Ready)

```applescript
tell application "Calendar"
    tell calendar "Calendar"
        set newEvent to make new event with properties {summary:"EVENT_NAME", start date:date "DATE_STRING", end date:date "DATE_STRING", location:"LOCATION", description:"NOTES"}
        tell newEvent
            -- 1 day before: gentle
            make new sound alarm at end of sound alarms with properties {trigger interval:-1440, sound name:"Blow"}
            -- 3 hours before: noticeable
            make new sound alarm at end of sound alarms with properties {trigger interval:-180, sound name:"Pop"}
            -- 1 hour before: clear
            make new sound alarm at end of sound alarms with properties {trigger interval:-60, sound name:"Glass"}
            -- 30 min before: time to go
            make new sound alarm at end of sound alarms with properties {trigger interval:-30, sound name:"Ping"}
            -- At event time: loudest
            make new sound alarm at end of sound alarms with properties {trigger interval:0, sound name:"Funk"}
        end tell
    end tell
    reload calendars
end tell
```

### Paired Reminders Creation

```applescript
tell application "Reminders"
    set defaultList to default list
    -- Due-time reminder
    make new reminder in defaultList with properties {name:"EVENT_NAME", due date:EVENT_DATE, body:"LOCATION\nNOTES"}
    -- Day-before
    make new reminder in defaultList with properties {name:"TOMORROW: EVENT_NAME", due date:(EVENT_DATE - 1 * days), body:"Event tomorrow! LOCATION"}
    -- Morning-of at 9 AM
    set morningDate to date "DATE_STRING"
    set time of morningDate to 9 * hours
    make new reminder in defaultList with properties {name:"TODAY: EVENT_NAME", due date:morningDate, body:"Today! LOCATION"}
end tell
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Sound reference table matches [sound-reference.md](./references/sound-reference.md)
2. [ ] All 6 alarm tiers documented with correct sounds
3. [ ] BANNED sounds list is complete
4. [ ] Hook file (`hooks/calendar-reminder-sync.ts`) aligned with skill rules
5. [ ] AppleScript examples use `sound alarm` not `display alarm`

---

## References

- [Sound Reference](./references/sound-reference.md) - Full sound duration data and approved/rejected lists
- [Apple Calendar Scripting Guide](https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/CalendarScriptingGuide/Calendar-AddanAlarmtoanEvent.html)
