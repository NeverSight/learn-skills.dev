---
name: maven-profile-selector
description: Helps users select Maven Profile for its network.
---

# Maven Profile Selector

This skill helps you select and manage Maven profiles for different network configurations.

## When to Use This Skill

Use this skill when the user:

- Switch between different network environments (e.g., development, staging, production) that require different Maven profiles.

## Workflow
1. Ensure `mvn` is installed and available in the system PATH.
2. Check the `settings.xml` file for available profiles relative to `mvn`, such as `mvn`'s `conf` directory.
3. Present the user with a list of available profiles and their descriptions.
4. Allow the user to select a profile.
5. Ask the user whether to change profile, and if confirmed, set the selected profile as the active profile for Maven commands.
6. For all subsequent Maven commands, use the selected profile until the user decides to switch again. Replace './mvnw' with `mvn` and add `-P <selected_profile>`.

## Example
User: I need to switch environment for my Maven project.
Assistant: Sure! Here are the available Maven profiles in your `settings.xml`:
1. Home - Profile for Home environment
2. Stuff - Profile for Stuff environment
3. Trip - Profile for Trip environment
Please select the profile you want to use (1, 2, or 3).