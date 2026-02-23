---
name: ansible-coder
description: This skill guides writing Ansible playbooks for server configuration. Use when hardening servers, installing packages, or automating post-provisioning tasks that cloud-init cannot handle.
allowed-tools: Read Write Edit Grep Glob Bash
---

# Ansible Coder

## ⚠️ SIMPLICITY FIRST - Default to Flat Structure

**ALWAYS start with the simplest approach. Only add complexity when explicitly requested.**

### Simple (DEFAULT) vs Overengineered

| Aspect | ✅ Simple (Default) | ❌ Overengineered |
|--------|---------------------|-------------------|
| Playbooks | 1 playbook with inline tasks | Multiple playbooks + custom roles |
| Roles | Use Galaxy roles (geerlingguy.*) | Write custom roles for simple tasks |
| Inventory | Single `hosts.ini` | Multiple inventories + group_vars hierarchy |
| Variables | Inline in playbook or single vars file | Scattered across group_vars/host_vars |
| File count | ~3-5 files total | 20+ files in nested directories |

### When to Use Simple Approach (90% of cases)

- Setting up 1-5 servers
- Standard stack (Docker, nginx, fail2ban, ufw)
- Single environment or identical servers
- No complex conditional logic per host

### When Complexity is Justified (10% of cases)

- Large fleet with divergent configurations
- Multi-team requiring role isolation
- Complex orchestration with dependencies
- User explicitly requests modular structure

**Rule: If you can fit everything in one 200-line playbook, DO IT.**

## When to Use Ansible vs Cloud-Init

| Use Cloud-Init When | Use Ansible When |
|---------------------|------------------|
| First boot only | Re-running config on existing servers |
| Simple package install | Complex multi-step configuration |
| Basic user creation | Role-based configuration |
| Immutable infrastructure | Mutable servers needing updates |

**Rule of thumb:** Cloud-init for initial provisioning, Ansible for ongoing management.

## Directory Structure

### Simple Structure (DEFAULT)

```
infra/ansible/
├── playbook.yml          # Single playbook with all tasks inline
├── requirements.yml      # Galaxy dependencies (geerlingguy.*, etc.)
├── hosts.ini             # Inventory (git-ignored)
└── hosts.ini.example     # Inventory template
```

### Complex Structure (only when justified)

```
infra/ansible/
├── playbook.yml          # Main playbook
├── requirements.yml      # Galaxy dependencies
├── hosts.ini             # Inventory (git-ignored)
├── hosts.ini.example     # Inventory template
├── group_vars/
│   └── all.yml           # Shared variables
└── roles/
    └── custom_role/
        ├── tasks/main.yml
        ├── handlers/main.yml
        └── templates/
```

## Inventory

### Static Inventory

```ini
# hosts.ini
[web]
192.168.1.1 ansible_user=root

[db]
192.168.1.2 ansible_user=root

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### Dynamic from Terraform

```bash
# Generate inventory from Terraform output
SERVER_IP=$(cd infra && tofu output -raw server_ip)
cat > infra/ansible/hosts.ini << EOF
[web]
$SERVER_IP ansible_user=root
EOF
```

## Playbook Structure

### Basic Playbook

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  vars:
    timezone: "UTC"
    swap_size_mb: "2048"

  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

    - name: Install packages
      ansible.builtin.apt:
        name:
          - docker.io
          - fail2ban
          - ufw
        state: present
```

### With Roles

```yaml
---
- name: Configure web servers
  hosts: web
  become: true

  vars:
    security_autoupdate_reboot: true
    security_autoupdate_reboot_time: "03:00"

  roles:
    - role: geerlingguy.swap
      when: ansible_swaptotal_mb < 1
    - role: geerlingguy.docker
    - role: security
```

## Common Tasks

### Package Management

```yaml
- name: Install required packages
  ansible.builtin.apt:
    name:
      - curl
      - ca-certificates
      - gnupg
      - fail2ban
      - ufw
      - ntp
    state: present
    update_cache: true
```

### Docker Installation

```yaml
- name: Check if Docker is installed
  ansible.builtin.command: docker --version
  register: docker_installed
  ignore_errors: true
  changed_when: false

- name: Install Docker via convenience script
  ansible.builtin.shell: curl -fsSL https://get.docker.com | sh
  when: docker_installed.rc != 0
  args:
    creates: /usr/bin/docker

- name: Ensure Docker is running
  ansible.builtin.systemd:
    name: docker
    state: started
    enabled: true
```

### SSH Hardening

```yaml
- name: Disable SSH password authentication
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "^#?PasswordAuthentication"
    line: "PasswordAuthentication no"
  notify: Restart ssh

- name: Disable SSH root login with password
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: "^#?PermitRootLogin"
    line: "PermitRootLogin prohibit-password"
  notify: Restart ssh

handlers:
  - name: Restart ssh
    ansible.builtin.systemd:
      name: ssh  # Ubuntu uses 'ssh', not 'sshd'
      state: restarted
```

### Fail2ban

```yaml
- name: Configure fail2ban for SSH
  ansible.builtin.copy:
    dest: /etc/fail2ban/jail.local
    content: |
      [sshd]
      enabled = true
      port = ssh
      filter = sshd
      logpath = /var/log/auth.log
      maxretry = 5
      bantime = 3600
      findtime = 600
    mode: "0644"
  notify: Restart fail2ban

- name: Ensure fail2ban is running
  ansible.builtin.systemd:
    name: fail2ban
    state: started
    enabled: true

handlers:
  - name: Restart fail2ban
    ansible.builtin.systemd:
      name: fail2ban
      state: restarted
```

### UFW Firewall

```yaml
- name: Set UFW default policies
  community.general.ufw:
    direction: "{{ item.direction }}"
    policy: "{{ item.policy }}"
  loop:
    - { direction: incoming, policy: deny }
    - { direction: outgoing, policy: allow }

- name: Allow specified ports through UFW
  community.general.ufw:
    rule: allow
    port: "{{ item }}"
    proto: tcp
  loop:
    - 22   # SSH
    - 80   # HTTP
    - 443  # HTTPS

- name: Enable UFW
  community.general.ufw:
    state: enabled
```

### Kernel Tuning

```yaml
- name: Configure sysctl for performance
  ansible.posix.sysctl:
    name: "{{ item.name }}"
    value: "{{ item.value }}"
    state: present
    reload: true
  loop:
    - { name: vm.swappiness, value: "10" }
    - { name: net.core.somaxconn, value: "65535" }
```

### Timezone

```yaml
- name: Set timezone
  community.general.timezone:
    name: "{{ timezone }}"
```

### Remove Snap (Ubuntu bloat)

```yaml
- name: Remove snapd
  ansible.builtin.apt:
    name: snapd
    state: absent
    purge: true
  ignore_errors: true

- name: Remove snap directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: absent
  loop:
    - /snap
    - /var/snap
    - /var/lib/snapd
```

## Galaxy Dependencies

### requirements.yml

```yaml
---
roles:
  - name: geerlingguy.swap
    version: 2.0.0
  - name: geerlingguy.docker
    version: 7.4.1

collections:
  - name: community.general
  - name: ansible.posix
```

### Installation

```bash
ansible-galaxy install -r requirements.yml --force
```

## Running Playbooks

### Basic Execution

```bash
ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i hosts.ini playbook.yml
```

### With Variables

```bash
ansible-playbook -i hosts.ini playbook.yml \
  -e "timezone=Europe/Berlin" \
  -e "swap_size_mb=4096"
```

### Dry Run

```bash
ansible-playbook -i hosts.ini playbook.yml --check --diff
```

### Limit to Specific Hosts

```bash
ansible-playbook -i hosts.ini playbook.yml --limit web
```

See [Kamal Server Preparation](references/kamal-playbook.md) for a complete Kamal deployment server playbook.

See [Integration with Terraform](references/provision-script.md) for the Terraform-Ansible-Kamal provisioning pipeline.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `ssh: connect refused` | Server not ready | Wait or check firewall |
| `Permission denied` | Wrong SSH key | Specify with `-i` |
| `sudo: password required` | User needs NOPASSWD | Use `become_method: sudo` |
| Handler not running | Task didn't change | Use `changed_when: true` |
| Module not found | Missing collection | Install from requirements.yml |
