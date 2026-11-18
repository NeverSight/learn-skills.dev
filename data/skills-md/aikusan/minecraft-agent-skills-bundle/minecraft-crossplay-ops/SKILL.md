---
name: minecraft-crossplay-ops
description: "Operate Java-to-Bedrock crossplay for Minecraft 1.21.x servers with Geyser and Floodgate. Use for proxy placement, online/offline authentication choices, Bedrock client connection triage, resource-pack delivery, converted-pack placement, plugin compatibility checks, port/firewall issues, and safe rollout/rollback of crossplay access."
---

# Minecraft Crossplay Operations Skill

## Scope

Use this skill for Java servers that allow Bedrock Edition clients through Geyser,
optionally with Floodgate authentication.

### Routing Boundaries
- `Use when`: the task is crossplay setup, Bedrock client access to a Java server, Geyser/Floodgate operations, crossplay resource-pack delivery, or compatibility triage.
- `Do not use when`: the task is pure Java server administration (`minecraft-server-admin`), pure BDS administration (`minecraft-bedrock-server-admin`), pack conversion itself (`minecraft-resource-pack-conversion`), or Java plugin implementation (`minecraft-plugin-dev`).
- `Do not use when`: the task is a bot playthrough from a Bedrock or Java client (`minecraft-bot-qa`).

## Architecture Choices

Common placements:

- Geyser as a standalone proxy in front of a Java server.
- Geyser as a Velocity/Bungee plugin in a proxy network.
- Geyser as a Paper plugin for small single-server setups.

Prefer proxy placement when the network already uses Velocity or when multiple
backend servers need shared access.

## Rollout Checklist

1. Confirm Java server version and Geyser build compatibility.
2. Decide whether Bedrock users must own Java accounts.
3. If using Floodgate, install matching Floodgate components on the proxy/server.
4. Open the Bedrock UDP listener port.
5. Test with one Bedrock client before advertising support.
6. Document username prefix/suffix policy for permission and moderation tools.

## Authentication Modes

Use online-mode Java auth when Bedrock players will sign in with Java accounts.
Use Floodgate when Bedrock players should join with Bedrock identities.

Operational guardrails:

- Keep Floodgate key files private.
- Align permission plugin contexts with Bedrock-prefixed names.
- Test staff commands against a Bedrock account before granting broad access.

## Resource Pack Delivery

For Java packs served to Bedrock clients:

1. Convert the Java pack with `minecraft-resource-pack-conversion`.
2. Place the converted Bedrock pack where Geyser expects packs for the chosen
   deployment mode.
3. Restart or reload Geyser as documented by the local install.
4. Join with a Bedrock client and confirm download, UI, item, and block visuals.

Keep the Java pack and converted Bedrock pack versioned together.

## Compatibility Triage

For login failures:

- Check Bedrock client version support.
- Check UDP firewall rules.
- Check Geyser startup logs for bind or remote-address errors.
- Check Floodgate key and forwarding configuration.

For gameplay differences:

- Identify whether the issue is protocol translation, plugin behavior, or pack
  conversion.
- Reproduce with a vanilla Java account and a Bedrock account.
- Disable optional plugins in staging to isolate plugin compatibility.

For permission problems:

- Confirm the exact Bedrock username shown to the Java server.
- Check LuckPerms user records and inherited groups.
- Avoid wildcard staff grants to Bedrock test users.

## Rollback

Rollback should be a reversible config change:

- Disable public Bedrock port exposure.
- Stop or unload Geyser.
- Leave Java server data untouched.
- Keep converted pack artifacts for post-incident review.
