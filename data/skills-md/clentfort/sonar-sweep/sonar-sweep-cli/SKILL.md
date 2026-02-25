---
name: sonar-sweep-cli
description: Inspect and triage SonarQube Cloud pull request findings
---

# sonar-sweep-cli

## Purpose

Use this skill when a user wants to inspect SonarQube Cloud PR status, review
issues with code context, identify low-coverage files, and optionally accept
issues after review.

## When to use

- User asks to check Sonar status for a PR.
- User asks why a quality gate failed.
- User asks for issue details (rule, file, line, message).
- User asks which files are below coverage threshold in Sonar.
- User asks to accept Sonar issues after triage.

## Common workflows

### 1) PR triage (recommended default)

Run summary, coverage, and issue review in sequence:

```bash
npx sonar-sweep pr-report <pullRequest>
npx sonar-sweep pr-coverage <pullRequest> --threshold 80
npx sonar-sweep pr-review <pullRequest> --context 3
```

Notes:

- `pr-*` commands auto-detect `sonar.projectKey` from `sonar-project.properties`
  in the current git root.
- Override auto-detection with `--projectKey` when needed.

### 2) Agent-friendly JSON output

```bash
npx sonar-sweep pr-report <pullRequest> --json
npx sonar-sweep pr-issues <pullRequest> --json
npx sonar-sweep pr-coverage <pullRequest> --json
npx sonar-sweep pr-review <pullRequest> --json
```

### 3) Accept issues after review

```bash
npx sonar-sweep issue-accept <issueKey> --comment "Reviewed and accepted"
```

For multiple issues:

```bash
npx sonar-sweep issue-accept <issueKeyA> --comment "Reviewed and accepted"
npx sonar-sweep issue-accept <issueKeyB> --comment "Reviewed and accepted"
```

## Suggested assistant behavior

1. Start with `pr-report` to determine gate state and failing conditions.
2. If gate fails on coverage, run `pr-coverage` before proposing test work.
3. If issues exist, run `pr-review` to inspect snippets and issue URLs.
4. Prefer fixing code issues when practical; use acceptance only when the user
   explicitly chooses that path.
5. If accepting issues, include a short rationale in `--comment`.
6. Re-run `pr-report` and/or `pr-issues` after changes to confirm outcome.

## Safety

- `issue-accept` changes Sonar state. Never run it without explicit user intent.
- Avoid any non-read Sonar actions unless the user asked for them.

## Troubleshooting checklist

- Missing token: ensure `SONAR_TOKEN` is set or pass `--token`.
- Wrong project detected: pass `--projectKey` explicitly.
- No project auto-detection: verify `sonar-project.properties` exists at git root.
- No open issues but gate fails: inspect `pr-report` conditions and `pr-coverage`.

## Expected output style

- Execute requested checks instead of only suggesting commands.
- Return concise triage output: gate status, issue count, coverage hotspots.
- When mutating issue state, confirm which issue keys were transitioned.
