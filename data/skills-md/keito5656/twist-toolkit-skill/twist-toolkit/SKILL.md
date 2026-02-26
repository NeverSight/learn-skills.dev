---
name: twist-toolkit
description: Full interaction with Doist's Twist app. Manage workspaces, users, groups, channels, threads, comments, DMs, search, and attachments.
---

# Twist Toolkit Skill

This skill provides a comprehensive set of commands to interact with the Twist API v3. It supports a default workspace ID to simplify common tasks and ensures secure local credential management.

## Requirements

No additional installation is required. Node.js is needed to run the core script.

## Onboarding (First-time use)

1. **Login:** `node scripts/twist_api.js login` (Opens browser)
2. **Auth:** `node scripts/twist_api.js auth <code>`
3. **Set Default Workspace:** `node scripts/twist_api.js set_workspace <id>`

## Available Commands

### 1. User & Workspace Management
- **Workspaces:** `node scripts/twist_api.js workspaces`
- **Users:** `node scripts/twist_api.js users [workspace_id]`
- **Set Default Workspace:** `node scripts/twist_api.js set_workspace <workspace_id>`
- **Add User:** `node scripts/twist_api.js add_workspace_user [workspace_id] <email>`
- **Search User by Email:** `node scripts/twist_api.js get_user_by_email <email>`
- **Get User Info:** `node scripts/twist_api.js get_user_info [workspace_id] <user_id>`
- **Update Profile:** `node scripts/twist_api.js update_user <new_name>`

### 2. Channel Management
- **List Channels:** `node scripts/twist_api.js channels [workspace_id]`
- **Add Channel:** `node scripts/twist_api.js add_channel [workspace_id] "Name"`
- **Update Channel:** `node scripts/twist_api.js update_channel <channel_id> "New Name"`
- **Favorite:** `node scripts/twist_api.js favorite_channel <channel_id>`
- **Archive/Unarchive:** `node scripts/twist_api.js archive_channel <channel_id>` / `unarchive_channel`
- **Remove:** `node scripts/twist_api.js remove_channel <channel_id>`
- **Add User:** `node scripts/twist_api.js add_user_to_channel <channel_id> <user_id>`
- **Remove User:** `node scripts/twist_api.js remove_user_from_channel <channel_id> <user_id>`

### 3. Thread & Comment Operations
- **List Threads:** `node scripts/twist_api.js threads <channel_id>`
- **Unread Threads:** `node scripts/twist_api.js unread_threads [workspace_id]`
- **Create Thread:** `node scripts/twist_api.js add_thread <channel_id> "Title" "Content"`
- **Star/Unstar:** `node scripts/twist_api.js star_thread <thread_id>` / `unstar_thread`
- **Close/Reopen:** `node scripts/twist_api.js close_thread <thread_id>` / `reopen_thread`
- **Read Comments:** `node scripts/twist_api.js comments <thread_id>`
- **Post Reply:** `node scripts/twist_api.js reply <thread_id> "Message"`
- **Add Reaction:** `node scripts/twist_api.js add_reaction <comment_id> "👍"`

### 4. Inbox Management (Archiving/Completing)
- **Get Inbox:** `node scripts/twist_api.js inbox [workspace_id]`
- **Inbox Count:** `node scripts/twist_api.js get_inbox_count [workspace_id]`
- **Complete/Archive:** `node scripts/twist_api.js complete_thread <thread_id>` (Alias for archive)
- **Unarchive:** `node scripts/twist_api.js unarchive_inbox_thread <thread_id>`
- **Archive All:** `node scripts/twist_api.js archive_all_inbox [workspace_id]`
- **Mark All Read:** `node scripts/twist_api.js mark_all_inbox_read [workspace_id]`

### 5. Direct Messages (Conversations)
- **List DMs:** `node scripts/twist_api.js conversations [workspace_id]`
- **Get/Create DM:** `node scripts/twist_api.js get_or_create_conversation [workspace_id] "[user_id1,user_id2]"`
- **History:** `node scripts/twist_api.js messages <conv_id>`
- **Add Message:** `node scripts/twist_api.js add_message <conv_id> "Content"`
- **Archive/Mute:** `node scripts/twist_api.js archive_conversation <conv_id>` / `mute_conversation <conv_id> [minutes]`

### 6. Search & Attachments
- **Search Workspace:** `node scripts/twist_api.js search [workspace_id] "Query"`
- **Search In Thread:** `node scripts/twist_api.js search_in_thread <thread_id> "Query"`
- **Notification Settings:** `node scripts/twist_api.js notification_settings [workspace_id]`
- **Upload File:** `node scripts/twist_api.js upload_attachment <attachment_id> <file_path>`

## Tip: Default Workspace
For commands marked with `[workspace_id]`, the parameter is optional if you have set a default via `set_workspace`.
