---
name: nextdns-cli
description:
  NextDNS CLI client best practices for installation, configuration, and management of
  DNS-over-HTTPS proxy. This skill should be used when installing NextDNS on routers, servers, or
  client devices, configuring DNS settings, managing the daemon, or troubleshooting DNS issues.
  Triggers on tasks involving NextDNS CLI installation, daemon control, system configuration, or DNS
  proxy setup.
license: MIT
metadata:
  author: tuanductran
  version: '1.0.0'
---

# NextDNS CLI Skills

## Capability Rules

| Rule                                                    | Keywords                                                 | Description                                |
| ------------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------ |
| [installation](rules/installation.md)                   | install, setup, curl, nextdns install                    | Install NextDNS CLI on various platforms   |
| [windows-installation](rules/windows-installation.md)   | Windows, GUI, CLI, installation, Systray, EXE            | Windows-specific installation methods      |
| [macos-installation](rules/macos-installation.md)       | macOS, Homebrew, App Store, installer                    | Install and configure NextDNS CLI on macOS |
| [daemon-control](rules/daemon-control.md)               | start, stop, restart, status, daemon                     | Control NextDNS daemon service             |
| [system-configuration](rules/system-configuration.md)   | activate, deactivate, DNS resolver                       | Configure system DNS settings              |
| [profile-configuration](rules/profile-configuration.md) | config, profile ID, settings                             | Configure NextDNS profile and settings     |
| [advanced-features](rules/advanced-features.md)         | conditional forwarder, MAC address, subnet               | Advanced routing and filtering             |
| [monitoring](rules/monitoring.md)                       | log, cache-stats, discovered clients                     | Monitor and debug DNS queries              |
| [platform-specific](rules/platform-specific.md)         | router, OpenWrt, pfSense, Synology                       | Platform-specific configurations           |
| [ddwrt-installation](rules/ddwrt-installation.md)       | DD-WRT, JFFS, NTP, router, time sync, dnsmasq            | DD-WRT router installation and setup       |
| [docker-deployment](rules/docker-deployment.md)         | docker, container, DockerHub, host network, port mapping | Deploy NextDNS CLI via Docker containers   |
| [troubleshooting](rules/troubleshooting.md)             | diagnostic, connection test, DNS leak                    | Troubleshoot DNS issues                    |
| [cache-configuration](rules/cache-configuration.md)     | cache-size, max-age, ttl, performance, optimization      | Optimize DNS performance with CLI caching  |
| [config-file-format](rules/config-file-format.md)       | nextdns.conf, automation, paths, structure               | Manage the nextdns.conf file format        |
| [split-horizon](rules/split-horizon.md)                 | internal dns, lan, forwarder, local resolution           | Resolve internal domains with NextDNS      |
| [Conditional Profiles](rules/conditional-profiles.md)   | cli, profile, conditional, subnet, mac-address           | Apply different profiles based on clients  |
| [Advanced Linux Support](rules/linux-advanced.md)       | linux, arch, alpine, aur, apk                            | Advanced Linux installation methods        |

## Efficiency Rules

| Rule                                            | Keywords                            | Description                   |
| ----------------------------------------------- | ----------------------------------- | ----------------------------- |
| [upgrade-uninstall](rules/upgrade-uninstall.md) | upgrade, uninstall, remove          | Upgrade or remove NextDNS CLI |
| [best-practices](rules/best-practices.md)       | performance, security, optimization | CLI best practices and tips   |
