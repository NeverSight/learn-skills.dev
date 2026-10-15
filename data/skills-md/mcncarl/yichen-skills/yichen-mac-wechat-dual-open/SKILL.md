---
name: yichen-mac-wechat-dual-open
description: Create, inspect, repair, and polish a second WeChat app on macOS by copying WeChat, changing the bundle identifier, ad-hoc re-signing, preparing it for the user to open manually, setting Chinese language preferences, and recoloring only the copied app icon from WeChat green to blue. Use when the user asks whether Mac WeChat dual-open methods from X/Twitter or scripts are reliable, asks to prepare a second WeChat app, fix WeChat-2 language/icon/cache issues, or make the copied app visually distinct without installing third-party injection tools. Never launch or control WeChat.
---

# Mac WeChat Dual Open

## Core Judgment

Prefer the copy + bundle id + ad-hoc signing method over injection/tweak tools when the user wants a cleaner second WeChat:

1. Copy `/Applications/WeChat.app` to a user-owned app such as `~/Applications/WeChat-2.app`.
2. Change only the copy's `CFBundleIdentifier`, usually to `com.tencent.xin2`.
3. Re-sign the copy with `codesign --force --deep --sign -`.
4. Stop and have the user open the prepared copy manually. The agent never launches WeChat.

This is generally workable, but not permanent. Updates, push notifications, keychain isolation, Gatekeeper/signing policy, and Tencent-side app checks can break or degrade it. Read `references/reliability-and-risks.md` when evaluating a public tutorial or explaining tradeoffs.

## Prerequisites

- macOS 12+ with WeChat installed at `/Applications/WeChat.app`
- Python 3.10+ (system python works)
- Pillow: required for `recolor-icon`. Install with `pip3 install Pillow` if missing.
- Xcode Command Line Tools: `xcode-select --install` provides `codesign`, `iconutil`, `sips`.

## Locating the Script

This skill contains a helper script at `scripts/wechat_dual_open.py` relative to the skill directory. Different agents install skills to different paths:

- Claude Code: `~/.claude/skills/yichen-mac-wechat-dual-open/scripts/wechat_dual_open.py`
- Codex CLI: `~/.codex/skills/yichen-mac-wechat-dual-open/scripts/wechat_dual_open.py`
- Others: locate the skill directory by finding `SKILL.md` for `yichen-mac-wechat-dual-open`

When executing commands, construct the script path dynamically:

```bash
# Auto-detect: find the script regardless of agent platform
SKILL_DIR="$(dirname "$(find ~ -path '*/yichen-mac-wechat-dual-open/SKILL.md' -maxdepth 4 2>/dev/null | head -1)")"
SCRIPT="$SKILL_DIR/scripts/wechat_dual_open.py"
python3 "$SCRIPT" status
```

Or if you know your skill path, use it directly:

```bash
SCRIPT="<skill-dir>/scripts/wechat_dual_open.py"
python3 "$SCRIPT" status
```

## Quick Commands

```bash
python3 "$SCRIPT" status
python3 "$SCRIPT" create
python3 "$SCRIPT" set-language --languages zh-Hans en
python3 "$SCRIPT" recolor-icon --blue "#1296db"
# The user opens ~/Applications/WeChat-2.app manually; the agent never runs launch.
```

Default paths:

- Source app: `/Applications/WeChat.app`
- Second app: `~/Applications/WeChat-2.app`
- Second bundle id: `com.tencent.xin2`

Pass `--source-app`, `--target-app`, or `--bundle-id` when the user's setup differs.

## Workflow

1. Run `status` first. Confirm the source version, target path, bundle ids, active processes, and whether an existing `WeChat-2.app` is already present.
2. If no second app exists, run `create`. If it exists, avoid deleting it. Use `repair` to re-apply bundle id, language preference, signing, registration, and cache refresh.
3. If the second instance appears in English, run `set-language --languages zh-Hans en`, then restart the second WeChat.
4. If the user wants a blue icon, run `recolor-icon`. This extracts the original WeChat icon, changes green pixels to blue in HSV/HLS space, preserves white chat bubbles and shape, replaces both outer and embedded icon files, removes `CFBundleIconName` to avoid stale `Assets.car` green icons, clears Finder custom-icon detritus before signing, re-signs, adds a Finder custom icon back, and refreshes caches. If the Finder custom icon tools (`DeRez`, `Rez`, `SetFile`) are unavailable on newer macOS, the script skips that step gracefully — icns replacement alone is usually sufficient.
5. Stop before launch. Tell the user to open `~/Applications/WeChat-2.app` manually. If Dock still shows the old icon, the user may quit and reopen it; the agent must not control either WeChat app.

## Icon Pitfalls

Do not stop after replacing only `Contents/Resources/AppIcon.icns`. WeChat also has:

- `Contents/MacOS/WeChatAppEx.app/Contents/Resources/app.icns`
- `Contents/Resources/Assets.car` with `AppIcon` renditions
- Finder/Dock/LaunchServices icon caches

For reliable Finder "Applications" display, the script also writes a Finder custom icon to `WeChat-2.app/Icon\r` and sets the Custom Icon attribute. If the user says "Finder still shows green," inspect the real selected path with Finder or `open -R ~/Applications/WeChat-2.app`; they may be looking at `/Applications/WeChat.app` or a cached Dock/Launchpad tile.

Important ordering: `codesign` must run before adding the Finder custom icon, or after clearing it. Otherwise macOS can reject the bundle with `resource fork, Finder information, or similar detritus not allowed`.

## Safety

Do not modify `/Applications/WeChat.app` unless the user explicitly asks. Keep all changes scoped to the second app.

Before deleting/replacing an existing second app, ask for action-time confirmation because deleting local files is risky. Prefer repair-in-place.

Do not run pasted one-line shell scripts from social media. Recreate the simple operations locally or use the bundled script so the exact changes are inspectable.

Never launch, open, quit, click, or otherwise control either WeChat app. The bundled `launch` command is disabled; opening the prepared copy is always a user-only step.
