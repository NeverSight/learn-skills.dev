---
name: verify
description: Verify any change, fix, behavior, deploy, or external state with current evidence from its real surface. Use when the user asks to verify, prove, check, test, or demonstrate that something works.
argument-hint: "<thing to verify or expected outcome>"
---

Prove the claim (or, when none is given, the latest user request) from current evidence on its real surface.

1. Define observable pass criteria.
2. Exercise the real user-facing or authoritative surface: open the page in a browser, call the endpoint, run the command, read back the provider (Stripe, Convex, Cloudflare, Lumail). Static checks (typecheck, lint, build, tests) support runtime proof; they do not replace it.
3. Capture current evidence:
   - Visual: a screenshot of the page or state, shown in the chat.
   - Non-visual: the command or request, its output, errors, status, and the authoritative read-back.
4. Mark each criterion `PASS` or `NOT PROVEN`.

Keep these proof layers distinct: local or static checks, provider read-back, deployed or public artifact, authenticated live behavior.

After any later change, rerun the affected criteria and replace the evidence.

Finish with `PASS` only when every criterion has current evidence. Otherwise `BLOCKED: NOT PROVEN` with the exact blocker.
