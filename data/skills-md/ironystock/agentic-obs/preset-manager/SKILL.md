---
name: preset-manager
description: Activate this skill when users need help with scene preset operations including saving, applying, organizing, or managing source visibility configurations. Triggers include requests like "save this layout", "apply my gaming preset", "switch to BRB mode", "create a preset", "list my presets", "rename preset", or managing saved configurations. This skill orchestrates preset tools for efficient scene state management.
---

# Preset Manager

Expert guidance for managing scene presets in OBS Studio, enabling quick switching between saved source visibility configurations.

## When to Use This Skill

Activate the **preset-manager** skill when users request help with:

- **Creating presets**
  - "Save this layout"
  - "Create a preset for my current setup"
  - "Remember these source settings"
  - "Save my gaming configuration"

- **Applying presets**
  - "Apply my BRB preset"
  - "Switch to gaming mode"
  - "Load my starting configuration"
  - "Use my interview preset"

- **Listing and viewing presets**
  - "What presets do I have?"
  - "Show my saved presets"
  - "What's in my gaming preset?"
  - "Preview preset changes"

- **Managing presets**
  - "Rename my preset"
  - "Delete old presets"
  - "Organize my presets"
  - "Update my preset"

- **Preset workflows**
  - "Set up quick switching"
  - "Create presets for my stream"
  - "Automate scene changes"

## Core Responsibilities

As the **preset-manager**, your role is to:

1. **Create presets** from current scene configurations
2. **Apply presets** to restore saved source visibility states
3. **List presets** with filtering by scene
4. **Preview presets** before applying
5. **Rename presets** for better organization
6. **Delete presets** that are no longer needed
7. **Guide preset strategy** for efficient workflows

## Available Tools

### Preset Operations
- `save_scene_preset` - Save current scene's source visibility as a preset
- `apply_scene_preset` - Apply a saved preset to restore source visibility
- `get_preset_details` - View what a preset contains before applying
- `list_scene_presets` - List all presets, optionally filtered by scene
- `rename_scene_preset` - Rename an existing preset
- `delete_scene_preset` - Remove a preset permanently

### Supporting Tools
- `list_scenes` - View available scenes
- `list_sources` - View sources in a scene
- `toggle_source_visibility` - Manually adjust visibility if needed

## What Presets Store

A preset captures:
- **Scene name**: Which scene the preset belongs to
- **Source visibility states**: For each source, whether it's visible or hidden
- **Creation timestamp**: When the preset was saved

A preset does NOT store:
- Source positions or transforms
- Source settings or configurations
- Audio levels or mute states
- Scene order or structure

## Preset Naming Conventions

### Recommended Format
```
[Scene]-[Purpose]-[Variant]
```

### Examples
```
Gaming-Stream-Full        # Gaming scene, all sources visible
Gaming-Focus-NoChat       # Gaming scene, chat hidden
Starting-Countdown-5min   # Starting scene with 5-min countdown
BRB-Quick                 # Quick BRB with minimal elements
Interview-TwoCamera       # Interview with both cameras
```

### Good Naming Practices
- Include scene name for clarity
- Describe the configuration purpose
- Use consistent naming patterns
- Avoid special characters
- Keep names reasonably short

## Preset Creation Workflow

### Step 1: Verify Current State

```
Before saving:
1. Use list_sources to see current visibility
2. Confirm this is the desired configuration
3. Note any sources that need adjustment
```

### Step 2: Adjust if Needed

```
If changes needed:
1. Use toggle_source_visibility to show/hide sources
2. Verify final state with list_sources
```

### Step 3: Save the Preset

```
1. Use save_scene_preset with:
   - preset_name: Descriptive name
   - scene_name: Current scene
2. Confirm save with list_scene_presets
```

### Example: Creating a Gaming Preset

```
User: "Save my current gaming layout"

1. Verify scene:
   - Use list_scenes to confirm current scene is "Gaming"

2. Check current sources:
   - Use list_sources for "Gaming" scene
   - Report:
     - Webcam: Visible
     - Game Capture: Visible
     - Chat Overlay: Hidden
     - Alerts: Visible

3. Confirm with user:
   - "Your Gaming scene has: Webcam, Game Capture, and Alerts visible. Chat is hidden."
   - "Save this as a preset?"

4. Save preset:
   - save_scene_preset:
     - preset_name: "Gaming-Stream-NoChat"
     - scene_name: "Gaming"

5. Confirm:
   - "Saved preset 'Gaming-Stream-NoChat' with current source visibility"
```

## Preset Application Workflow

### Step 1: Preview the Preset

```
Before applying:
1. Use get_preset_details to see what will change
2. Report visibility changes to user
3. Confirm they want to proceed
```

### Step 2: Apply the Preset

```
1. Use apply_scene_preset with preset name
2. Report what changed
```

### Step 3: Verify Application

```
1. Use list_sources to confirm new state
2. Report final visibility status
```

### Example: Applying a Preset

```
User: "Switch to my BRB setup"

1. Find the preset:
   - Use list_scene_presets
   - Locate: "BRB-Quick"

2. Preview changes:
   - Use get_preset_details for "BRB-Quick"
   - Report:
     - Scene: BRB
     - Sources to show: BRB Screen, Background Music
     - Sources to hide: Webcam, Game Capture

3. Confirm:
   - "Applying 'BRB-Quick' will show BRB Screen and Background Music, hide Webcam and Game Capture. Proceed?"

4. Apply:
   - Use apply_scene_preset: "BRB-Quick"

5. Confirm:
   - "Applied 'BRB-Quick' preset"
   - "BRB Screen and Background Music now visible"
```

## Preset Management

### Listing Presets

```
User: "What presets do I have?"

1. Use list_scene_presets (no filter for all)
2. Report:
   - Gaming-Stream-Full (Gaming scene)
   - Gaming-Focus-NoChat (Gaming scene)
   - BRB-Quick (BRB scene)
   - Starting-Countdown (Starting Soon scene)
   - Ending-Credits (Ending scene)
```

### Filtering by Scene

```
User: "Show presets for my Gaming scene"

1. Use list_scene_presets with scene_name: "Gaming"
2. Report:
   - Gaming-Stream-Full
   - Gaming-Focus-NoChat
   - Gaming-Commentary
```

### Renaming Presets

```
User: "Rename 'Gaming-Stream-Full' to 'Gaming-Everything'"

1. Use rename_scene_preset:
   - old_name: "Gaming-Stream-Full"
   - new_name: "Gaming-Everything"

2. Confirm:
   - "Renamed 'Gaming-Stream-Full' to 'Gaming-Everything'"
```

### Deleting Presets

```
User: "Delete my old 'Test-Preset'"

1. Confirm:
   - "Are you sure you want to delete 'Test-Preset'? This cannot be undone."

2. If confirmed, use delete_scene_preset:
   - preset_name: "Test-Preset"

3. Confirm:
   - "Deleted preset 'Test-Preset'"
```

## Preset Strategy for Streamers

### Recommended Preset Collection

#### Per-Scene Presets
```
For each scene, consider:
1. [Scene]-Full - All sources visible
2. [Scene]-Minimal - Only essential sources
3. [Scene]-Focused - Key content only (no overlays)
```

#### Workflow Presets
```
Streaming workflow:
1. Starting-Countdown - Pre-stream state
2. Gaming-Stream - Active gaming setup
3. Just-Chatting - Conversation mode
4. BRB-Quick - Brief away state
5. Ending-Credits - End-of-stream state
```

#### Special Purpose Presets
```
For specific moments:
1. Sponsor-Spotlight - Sponsor visibility
2. Raid-Welcome - Raid celebration overlay
3. Giveaway-Active - Giveaway overlay visible
4. Technical-Difficulty - Error/issue screen
```

### Preset Organization Tips

```
1. Use consistent naming conventions
2. Group by scene name prefix
3. Indicate purpose in name
4. Delete unused presets regularly
5. Test presets before going live
```

## Example Workflows

### Example 1: Complete Preset Setup for New Streamer

**User Request**: "Help me set up presets for my stream"

**Response Pattern**:
```
1. "Let me help you create a preset system..."

2. Inventory scenes:
   - list_scenes
   - Report: "You have 4 scenes: Starting Soon, Gaming, Just Chatting, Ending"

3. For each scene, create presets:

   Starting Soon:
   - Set up countdown visible, chat hidden
   - save_scene_preset: "Starting-Countdown"
   - "Created 'Starting-Countdown' preset"

   Gaming:
   - Full setup with all overlays
   - save_scene_preset: "Gaming-Full"
   - Focused setup without chat
   - Toggle chat visibility off
   - save_scene_preset: "Gaming-Focused"
   - "Created 'Gaming-Full' and 'Gaming-Focused' presets"

   Just Chatting:
   - save_scene_preset: "Chatting-Standard"
   - "Created 'Chatting-Standard' preset"

   Ending:
   - save_scene_preset: "Ending-Credits"
   - "Created 'Ending-Credits' preset"

4. Summary:
   - "Created 5 presets for your stream workflow:"
   - "Starting-Countdown, Gaming-Full, Gaming-Focused, Chatting-Standard, Ending-Credits"
   - "Use 'apply [preset-name]' to switch between them"
```

### Example 2: Quick Scene Transition with Preset

**User Request**: "I'm taking a break, switch to BRB"

**Response Pattern**:
```
1. Check for BRB preset:
   - list_scene_presets
   - Found: "BRB-Quick"

2. Preview:
   - get_preset_details: "BRB-Quick"
   - "This will switch to BRB scene and show: BRB Screen, Chill Music"

3. Apply:
   - apply_scene_preset: "BRB-Quick"

4. Confirm:
   - "You're now in BRB mode"
   - "BRB screen is showing with background music"
   - "Say 'apply Gaming-Full' when you're back"
```

### Example 3: Creating a New Preset from Modified Scene

**User Request**: "I like this layout, save it as a new preset"

**Response Pattern**:
```
1. Capture current state:
   - list_sources for current scene
   - Report: "Gaming scene with: Webcam (visible), Game Capture (visible),
     Chat Overlay (hidden), Alerts (visible), Sponsor Logo (visible)"

2. Ask for name:
   - "What would you like to name this preset?"

3. User: "Gaming with Sponsors"

4. Save:
   - save_scene_preset:
     - preset_name: "Gaming-with-Sponsors"
     - scene_name: "Gaming"

5. Confirm:
   - "Saved 'Gaming-with-Sponsors' preset"
   - "Includes: Webcam, Game Capture, Alerts, Sponsor Logo visible; Chat hidden"
```

### Example 4: Updating an Existing Preset

**User Request**: "Update my Gaming-Full preset with the new overlay"

**Response Pattern**:
```
1. Current preset:
   - get_preset_details: "Gaming-Full"
   - Shows current configuration

2. Explain approach:
   - "To update a preset, we'll save over it with the current configuration"
   - "First, let's verify your current sources are set correctly"

3. Verify:
   - list_sources
   - User confirms layout is correct

4. Save new version:
   - save_scene_preset:
     - preset_name: "Gaming-Full" (same name overwrites)
     - scene_name: "Gaming"

5. Confirm:
   - "Updated 'Gaming-Full' preset with current source visibility"
```

### Example 5: Preset Cleanup

**User Request**: "I have too many presets, help me clean up"

**Response Pattern**:
```
1. List all presets:
   - list_scene_presets
   - Report full list:
     - Gaming-Full
     - Gaming-Old
     - Gaming-Test1
     - Gaming-Test2
     - BRB-Quick
     - Test-Delete-Me

2. Identify candidates:
   - "I see some presets that might be outdated:"
   - "Gaming-Old, Gaming-Test1, Gaming-Test2, Test-Delete-Me"
   - "Would you like to review and delete these?"

3. For each candidate:
   - "Delete 'Gaming-Old'?"
   - If yes: delete_scene_preset: "Gaming-Old"
   - Confirm: "Deleted 'Gaming-Old'"

4. Final summary:
   - "Cleaned up 4 old presets"
   - "You now have 2 active presets: Gaming-Full, BRB-Quick"
```

## Best Practices

### Before Creating Presets
```
1. Set up your scene exactly as desired
2. Verify all source visibility
3. Test the configuration
4. Choose a descriptive name
```

### Before Applying Presets
```
1. Preview with get_preset_details
2. Confirm this is the right preset
3. Be aware of what will change
4. Have a fallback plan
```

### Preset Maintenance
```
1. Review presets periodically
2. Delete unused presets
3. Update presets when scenes change
4. Rename for clarity as needed
```

### Naming Discipline
```
1. Be consistent with naming format
2. Include scene name for context
3. Describe the purpose/state
4. Avoid cryptic abbreviations
```

## Troubleshooting

### Preset won't apply
```
Possible causes:
1. Preset references deleted sources - check preset details
2. Scene was renamed - preset may be orphaned
3. Typo in preset name - verify with list_scene_presets

Solution:
- If sources missing, create new preset
- If scene renamed, create new preset for new scene
- Use exact name from list
```

### Wrong sources affected
```
Possible causes:
1. Preset was saved with wrong visibility
2. Sources were added after preset creation
3. Applied to wrong scene

Solution:
- Preview with get_preset_details before applying
- Update preset by saving again with correct state
- New sources need explicit preset update
```

### Preset seems empty
```
Possible causes:
1. Scene had no sources when saved
2. Preset corrupted

Solution:
- Check scene has sources: list_sources
- Delete and recreate the preset
```

## Integration with Other Skills

The **preset-manager** skill may collaborate with:

- **streaming-assistant**: For preset-based scene transitions during streams
- **scene-designer**: After designing a layout, save it as a preset
- **audio-engineer**: Note that presets don't save audio states

**Handoff Pattern**:
```
User: "Design a new BRB scene and save it"

preset-manager: "Let me connect you with scene-designer
to create the layout first, then we'll save it as a preset..."

[Handoff to scene-designer, then return for preset save]
```

## Preset Limitations

Remember that presets only store **source visibility**:

```
Presets DO save:
- Which sources are visible/hidden
- The scene the preset belongs to

Presets DON'T save:
- Source positions/transforms
- Source settings (URLs, file paths, etc.)
- Audio levels or mute states
- Scene switching (they apply within a scene)
```

For complete state management, combine with:
- Manual source configuration
- Audio level presets (if implemented)
- Scene switching tools

## Summary

The **preset-manager** skill is your configuration efficiency expert for OBS Studio. It provides:

- Preset creation from current scene state
- Quick preset application for scene transitions
- Preset preview before applying
- Organization with listing, renaming, deletion
- Strategy guidance for preset systems

Use presets to enable instant switching between configurations, reducing manual source toggling during streams. Create a complete preset system during setup, then enjoy one-command configuration changes during live content.
