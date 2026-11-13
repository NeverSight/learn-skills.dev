---
name: ansible-convert
description: Use when converting shell scripts to Ansible playbooks. Use when migrating bash automation, manual procedures, or Dockerfiles to idempotent Ansible tasks.
---

# Shell to Ansible Conversion

## Overview

Shell scripts execute commands imperatively; Ansible declares desired state. Conversion means rethinking operations as state declarations, not translating commands line-by-line. The goal is idempotency: running twice produces identical results.

## When to Use

- Converting existing shell scripts to playbooks
- Migrating manual server setup procedures
- Replacing bash automation with Ansible
- Converting Dockerfile RUN commands

## Core Principle

**Don't wrap shell commands in Ansible's `shell` module.** Find the module that achieves the same end state declaratively.

```bash
# Shell: imperative
mkdir -p /opt/app
chown app:app /opt/app
```

```yaml
# Ansible: declarative
- ansible.builtin.file:
    path: /opt/app
    state: directory
    owner: app
    group: app
    mode: '0755'
```

## Conversion Table

| Shell Command | Ansible Module | Notes |
|---------------|----------------|-------|
| `mkdir -p` | `ansible.builtin.file` | `state: directory` |
| `cp` | `ansible.builtin.copy` | Static files |
| `cp` with variables | `ansible.builtin.template` | Use `.j2` templates |
| `rm -rf` | `ansible.builtin.file` | `state: absent` |
| `ln -s` | `ansible.builtin.file` | `state: link` |
| `chmod`, `chown` | Include in file/copy/template | `mode`, `owner`, `group` params |
| `apt-get install` | `ansible.builtin.apt` | `update_cache: yes` |
| `yum install` | `ansible.builtin.yum` | Or use `package` for cross-platform |
| `pip install` | `ansible.builtin.pip` | Specify `executable` if needed |
| `useradd` | `ansible.builtin.user` | Handles home, shell, groups |
| `systemctl start` | `ansible.builtin.service` | `state: started` |
| `systemctl enable` | `ansible.builtin.service` | `enabled: yes` |
| `curl -O` | `ansible.builtin.get_url` | Use `checksum` for verification |
| `tar -xzf` | `ansible.builtin.unarchive` | `remote_src: yes` if already on target |
| `echo >> file` | `ansible.builtin.lineinfile` | Ensures line exists |
| `cat > file` | `ansible.builtin.copy` | `content:` parameter |

## Control Flow Conversion

### Conditionals

```bash
# Shell
if [ -f /etc/debian_version ]; then
    apt-get install nginx
fi
```

```yaml
# Ansible
- ansible.builtin.apt:
    name: nginx
  when: ansible_os_family == "Debian"
```

### Loops

```bash
# Shell
for user in alice bob; do
    useradd $user
done
```

```yaml
# Ansible
- ansible.builtin.user:
    name: "{{ item }}"
  loop:
    - alice
    - bob
```

## When Shell Module is Necessary

Use `command` or `shell` only when no module exists. Always add proper change detection:

```yaml
- name: Run custom installer
  ansible.builtin.shell: /opt/app/install.sh
  args:
    creates: /opt/app/.installed  # Skip if file exists
  register: install_result
  changed_when: "'Installed' in install_result.stdout"
  failed_when: install_result.rc != 0 and 'already installed' not in install_result.stderr
```

## Variable Extraction

Identify values to parameterize:
- Version numbers → `app_version: "1.2.3"`
- Paths → `app_dir: "/opt/app"`
- Usernames → `app_user: "appuser"`
- Ports → `app_port: 8080`

Place in `defaults/main.yml` for easy override.

## Conversion Workflow

1. Read entire script, identify major phases
2. Map each command to Ansible module
3. Extract hardcoded values as variables
4. Order tasks for dependencies (dirs before files)
5. Add handlers for service restarts
6. Test with `--check --diff`
7. Verify idempotency: second run shows no changes
