#!/usr/bin/env python3
"""
Send the 10 most recently discovered skills to a Discord webhook.

Reads:  data/skills_index.json
Sends:  skill id + GitHub repo URL for each of the 10 newest entries
        (sorted by firstSeenAt descending).

Usage:
  DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/... python scripts/notify_discord_top_skills.py
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = REPO_ROOT / "data" / "skills_index.json"

TOP_N = 10
WEBHOOK_ENV = "DISCORD_WEBHOOK_URL"


def github_url_from_source(source: str | None) -> str:
    if not source:
        return ""
    return f"https://github.com/{source.strip('/')}"


def main() -> None:
    webhook_url = os.environ.get(WEBHOOK_ENV, "").strip()
    if not webhook_url:
        sys.exit(f"Error: environment variable {WEBHOOK_ENV} is not set.")

    if not INDEX_PATH.exists():
        sys.exit(f"Error: {INDEX_PATH} not found. Run the crawler first.")

    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    items: list[dict] = index.get("items") or []

    # Keep only items with a firstSeenAt timestamp, sort newest first.
    with_ts = [it for it in items if isinstance(it, dict) and it.get("firstSeenAt")]
    newest = sorted(with_ts, key=lambda x: x["firstSeenAt"], reverse=True)[:TOP_N]

    if not newest:
        print("No skills with firstSeenAt found; skipping Discord notification.")
        return

    lines = [f"**Newly Discovered {TOP_N} Skills**\n"]
    for i, skill in enumerate(newest, start=1):
        skill_id = skill.get("id") or skill.get("skillId") or "unknown"
        gh_url = github_url_from_source(skill.get("source"))
        first_seen = skill.get("firstSeenAt", "")[:10]  # keep date part only
        lines.append(f"{i}. `{skill_id}` — <{gh_url}>  *({first_seen})*")

    content = "\n".join(lines)

    payload = json.dumps({"content": content}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SkillsFeed-Bot/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"Discord webhook returned HTTP {exc.code}: {body}")
    except urllib.error.URLError as exc:
        sys.exit(f"Discord webhook request failed: {exc.reason}")

    print(f"Discord notification sent (HTTP {status}). Latest {TOP_N} skills posted.")


if __name__ == "__main__":
    main()
