---
name: moodle-cli
description: Helps users run the right `moodle` CLI commands for interacting with Moodle LMS. Triggers when users ask about Moodle CLI usage, commands, workflows, or troubleshooting.
---

# Moodle CLI Skill

You are helping a user run `moodle` — a CLI tool for interacting with the Moodle Learning Management System API.

## Command Tree

```
moodle
├── auth                    # Manage authentication
│   ├── login               # Log in to a Moodle instance
│   ├── logout              # Log out of the Moodle instance
│   ├── status              # Show authentication status
│   └── token               # Print the authentication token
├── course                  # Manage courses
│   ├── list                # List enrolled courses
│   ├── get <id>            # Get course details
│   ├── search <query>      # Search courses
│   ├── content <id>        # Get course contents (sections, modules)
│   ├── module <id>         # Get course module details
│   ├── grades <id>         # View your course grades
│   └── download <id>       # Download module files
├── assignment              # Manage assignments
│   ├── list                # List assignments (--course to filter)
│   ├── get <id>            # Get assignment details
│   ├── status <id>         # Check submission status
│   ├── upload <id> <file>  # Upload files to an assignment
│   ├── submit <id>         # Submit assignment for grading
│   ├── text <id>           # View or update online text submission
│   └── download <id>       # Download submission files (-R for resources)
├── forum                   # Manage forums
│   ├── list                # List forums in a course (--course)
│   ├── discussions <id>    # List discussions in a forum
│   ├── read <id>           # Read a discussion thread
│   ├── post <id>           # Create a new discussion
│   ├── reply <id>          # Reply to a post
│   ├── edit <id>           # Edit a post
│   └── delete <id>         # Delete a post
├── user                    # Manage users
│   ├── whoami              # Show current user info
│   ├── list                # List users enrolled in a course (--course)
│   └── get <id>            # Get user by ID
├── config                  # Manage configuration
│   ├── list                # List all configuration settings
│   ├── get <key>           # Get a configuration value
│   └── set <key> <value>   # Set a configuration value
└── version                 # Print the version
```

## Global Flags

Every command supports these flags:

| Flag | Description |
|------|-------------|
| `-f, --format <fmt>` | Output format: `table`, `json`, `csv`, `yaml`, `plain` |
| `--no-color` | Disable color output |
| `-v, --verbose` | Enable verbose output |
| `-h, --help` | Help for the command |

## Guidelines

### Default to JSON output

When suggesting commands, prefer `-f json` for machine-readable output. Show users how to pipe to `jq` for filtering:

```bash
# List courses as JSON
moodle course list -f json

# Get a specific field
moodle course list -f json | jq '.[].fullname'

# Filter assignments by course
moodle assignment list --course 42 -f json | jq '.[] | {id, name, duedate}'
```

For quick human-readable output, the default `table` format works well — no flag needed.

### Common Workflows

**First-time setup:**
```bash
moodle auth login --url https://moodle.example.com
moodle auth status          # verify login
moodle course list          # see enrolled courses
```

**Assignment workflow:**
```bash
moodle assignment list --course 42          # find assignment ID
moodle assignment get 101                   # check details and due date
moodle assignment upload 101 report.pdf     # upload file
moodle assignment submit 101 --accept-statement  # submit for grading
moodle assignment status 101                # verify submission
```

**Forum workflow:**
```bash
moodle forum list --course 42               # find forum ID
moodle forum discussions 5                  # list discussions
moodle forum read 100                       # read a thread
moodle forum reply 200 --message "Thanks!"  # reply to a post
moodle forum post 5 --subject "Question" --message "Hello"  # new discussion
```

**Download assignment resources:**
```bash
moodle assignment get 101                   # see attached resources
moodle assignment download 101 --resources  # download instructor-attached files
moodle assignment download 101 -R -o ./resources  # download to a directory
```

**Download course files:**
```bash
moodle course content 42                    # browse course sections
moodle course download 500                  # download a module's files
```

### Filtering

- Use `--course <id>` to filter assignments, forums, and users by course
- Use positional `<id>` arguments for specific resources (courses, assignments, forums, users, modules)
- Chain with `jq` for advanced filtering on JSON output

### Configuration

Users can set defaults to avoid repeating flags:
```bash
moodle config set format json    # always output JSON
moodle config list               # see current settings
```

## Reference Documentation

For detailed information about a specific command (flags, options, examples), read the corresponding file in the `references/` directory:

- **Root command:** `references/moodle.md`
- **Auth group:** `references/moodle_auth.md`, `references/moodle_auth_login.md`, etc.
- **Course group:** `references/moodle_course.md`, `references/moodle_course_list.md`, etc.
- **Assignment group:** `references/moodle_assignment.md`, `references/moodle_assignment_list.md`, etc.
- **Forum group:** `references/moodle_forum.md`, `references/moodle_forum_list.md`, etc.
- **User group:** `references/moodle_user.md`, `references/moodle_user_whoami.md`, etc.
- **Config group:** `references/moodle_config.md`, `references/moodle_config_set.md`, etc.
- **Version:** `references/moodle_version.md`

The filename pattern is `references/moodle_<group>_<command>.md`. When the user asks about a specific command, read the reference file first to provide accurate flag names and usage details.
