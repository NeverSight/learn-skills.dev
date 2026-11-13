---
name: ansible-debug
description: Use when playbooks fail with UNREACHABLE, permission denied, MODULE FAILURE, or undefined variable errors. Use when SSH connections fail or sudo password is missing.
---

# Ansible Debugging

## Overview

Ansible errors fall into four categories: connection, authentication, module, and syntax. Systematic diagnosis starts with identifying the category, then isolating the specific cause.

## When to Use

- UNREACHABLE errors (SSH/network issues)
- Permission denied or sudo password errors
- MODULE FAILURE messages
- Undefined variable errors
- Template rendering failures
- Slow playbook execution

## Error Categories

| Category | Symptoms | First Check |
|----------|----------|-------------|
| Connection | UNREACHABLE | `ssh -v user@host` |
| Authentication | Permission denied, Missing sudo password | SSH keys, sudoers config |
| Module | MODULE FAILURE | Module parameters, target state |
| Syntax | YAML parse error | Line number in error, indentation |

## Quick Diagnosis

### Connection Errors

```bash
# Test SSH directly
ssh -v -i /path/to/key user@hostname

# Test port connectivity
nc -zv hostname 22

# Verify inventory parsing
ansible-inventory --host hostname
```

**Common causes:**
- Wrong IP/hostname in inventory
- Firewall blocking port 22
- SSH key permissions (must be 600)

### Authentication Errors

```bash
# Test with explicit options
ansible hostname -m ping -u user --private-key /path/to/key

# For sudo password issues, either:
ansible-playbook playbook.yml --ask-become-pass
# Or configure NOPASSWD in /etc/sudoers
```

### Module Errors

```bash
# Check module documentation
ansible-doc ansible.builtin.copy

# Verify module parameters match your Ansible version
ansible --version
```

### Variable Errors

```yaml
# Use default filter for optional variables
{{ my_var | default('fallback') }}

# Debug variable values
- ansible.builtin.debug:
    var: problematic_variable
```

## Verbosity Levels

| Flag | Shows |
|------|-------|
| `-v` | Task results |
| `-vv` | Task input parameters |
| `-vvv` | SSH connection details |
| `-vvvv` | Full plugin internals |

Start with `-v`, increase only if needed.

## Debugging Commands

```bash
# Syntax check only
ansible-playbook --syntax-check playbook.yml

# Dry run
ansible-playbook --check playbook.yml

# Step through tasks
ansible-playbook --step playbook.yml

# Start at specific task
ansible-playbook --start-at-task "Task Name" playbook.yml

# Limit to specific host
ansible-playbook --limit hostname playbook.yml
```

## Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| `Permission denied (publickey)` | SSH key not accepted | Check key permissions, verify authorized_keys |
| `Missing sudo password` | become=true without password | Use `--ask-become-pass` or configure NOPASSWD |
| `No such file or directory` | Path doesn't exist | Create parent directories first |
| `Unable to lock` (apt/yum) | Package manager locked | Wait for other process, remove stale lock |
| `undefined variable` | Variable not defined | Check spelling, use `default()` filter |

## Performance Debugging

```ini
# ansible.cfg
[defaults]
callback_whitelist = profile_tasks  # Show task timing

[ssh_connection]
pipelining = True                   # Faster SSH
```

```yaml
# Skip fact gathering if not needed
- hosts: all
  gather_facts: no
```
