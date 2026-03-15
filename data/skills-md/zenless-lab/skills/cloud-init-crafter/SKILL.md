---
name: cloud-init-crafter
description: Expert assistant for creating, modifying, and debugging cloud-init scripts. Supports multiple formats (YAML, shell, MIME archives), Jinja templating with instance-data, and multi-platform validation.
---
# Cloud-init Crafter

This skill provides a structured framework for generating and maintaining `cloud-init` configurations. It utilizes a library of baseline templates, localized reference guides, and automated validation scripts to ensure production-ready deployments.

## Core Principles

1. **Plan Before Execution:** Always define a concise implementation plan (listing target modules, target format, baseline templates, and validation logic) before generating code.
2. **Format Awareness:** Recognize that `cloud-init` accepts multiple formats. Default to `#cloud-config` (YAML 1.1) but proactively suggest shell scripts, boothooks, or MIME archives when the user's operational timing requires it.
3. **Security by Default:** Prohibit plaintext passwords. Use `ssh_authorized_keys` or `hashed_passwd` exclusively. Ensure sensitive `instance-data` is accessed securely.
4. **Idempotency:** Ensure all `runcmd`, `bootcmd`, and custom scripts are idempotent to allow safe re-execution.

## Local References (Load On-Demand)

Load these reference documents on-demand when specific technical details, formats, or troubleshooting steps are required to save token context.

### Format Guides
Load these when defining the structure of the user-data payload or combining multiple execution types:
* [Cloud Config Format](references/formats/cloud-config.md) - Standard YAML configurations.
* [Cloud Boothook Format](references/formats/cloud-boothook.md) - Early-boot shell scripts (Network stage).
* [User-data Script Format](references/formats/user-data-script.md) - Late-boot standard shell scripts.
* [Include File Format](references/formats/include-file.md) - Referencing external URLs.
* [Jinja Template Format](references/formats/jinja-template.md) - Header requirements for Jinja rendering.
* [Gzip Compressed Content](references/formats/gzip.md) - Handling binary compressed payloads.
* [Cloud Config Archive](references/formats/cloud-config-archive.md) - YAML-based multi-part alternatives.
* [MIME Multi-part Archive](references/formats/mime-archive.md) - Combining multiple formats into a single payload.

### Data & Templating
* [Instance Data](references/instance-data.md) - Standardized `v1` keys, JSON structure, and Jinja templating usage for dynamic, environment-aware configurations.

### Core Concepts & Guidelines
* [Concepts and Boot Stages](references/concepts_and_boot_stages.md) - Overview of cloud-init principles and the five boot stages (Detect, Local, Network, Config, Final).
* [Cloud-config API](references/cloud_config_api.md) - Detailed syntax, configuration schema, and examples for common configuration modules.
* [Best Practices](references/best_practices.md) - Strategic guidelines for writing robust, idempotent, and maintainable cloud-init scripts.
* [Security Guidelines](references/security_guidelines.md) - Critical security hardening, credential management, and SSH host key verification.
* [CLI Reference](references/cli_reference.md) - Comprehensive command-line interface guide for `cloud-init` and `cloud-init-per`.
* [Error Cheatsheet](references/error_cheatsheet.md) - Troubleshooting workflows, log paths, status codes, and common failure modes.

### Platform Launching Guides
* [QEMU Launching](references/launching/qemu.md) - Guide for local instance testing using QEMU and the NoCloud datasource.
* [LXD Launching](references/launching/lxd.md) - Guide for testing with LXD containers.
* [Multipass Launching](references/launching/multipass.md) - Guide for launching VMs on Linux, Windows, or macOS.
* [Libvirt Launching](references/launching/libvirt.md) - Automating seed image creation and deployment.
* [WSL Launching](references/launching/wsl.md) - Requirements for Ubuntu 24.04+ on Windows Subsystem for Linux.

## Assets (Baseline Templates)

Use these templates as a starting point for new configurations:
* [Minimal Template](assets/minimal_template.yaml) - Essential SSH-only access with password authentication disabled.
* [Default Template](assets/default_template.yaml) - Standard baseline for production including users, SSH keys, and package updates.
* [Complete Template](assets/complete_template.yaml) - Comprehensive setup including disk partitioning, file writing, and complex orchestration.

## Validation Tools
* [Config Validator](scripts/validate_config.py) - A Python script (PEP 723) to offline validate YAML syntax and mandatory headers.

## Official Documentation
Refer to these external resources for the most granular specifications:
* [Official Documentation](https://docs.cloud-init.io/en/latest/index.html)
* [Cloud-config Modules Reference](https://docs.cloud-init.io/en/latest/reference/modules.html)
* [Datasources Reference](https://docs.cloud-init.io/en/latest/reference/datasources.html)

## Standard Operating Procedure (SOP)

1. **Discovery & Planning:** Analyze the user's requirements. Determine the correct Boot Stage needed (early network vs. final execution) and select the appropriate format (e.g., `#cloud-config`, `#cloud-boothook`, or MIME). Decide if dynamic `instance-data` via Jinja is required. Output a concise plan.
2. **Context Loading:** Silently load the relevant format guide from `references/formats/` and `references/instance-data.md` if templating is needed.
3. **Execution:** Generate or modify the configuration block. Ensure strict adherence to the loaded format's specific headers, syntax, and security constraints.
4. **Validation:** Recommend validation via `cloud-init schema -c <file> --annotate` or the provided `scripts/validate_config.py` tool.
