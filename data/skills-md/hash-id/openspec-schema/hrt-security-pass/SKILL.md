---
name: hrt-security-pass
description: Trust-boundary gate for tempa-spec's `specs`, `design`, and `apply` review. If the change touches a trust boundary, it points to the method and the OWASP and MITRE reference lists to use. Run the gate first; stop there if it does not fire.
---

# hrt-security-pass

Run the gate per capability in `specs`, per change in `design`, and on the diff in `apply`'s review. A trust boundary is touched if any of these hold:

- Authentication, authorization, or privileges are added or changed.
- Input comes from an untrusted source: a user, a file, a webhook, another service, or LLM output.
- Sensitive data (credentials, tokens, personal data) is stored, exposed, or logged.
- A secret is handled, a third-party service is integrated, or a third-party package is added or upgraded (Odoo `external_dependencies` included; Odoo module `depends`, and a lockfile regenerated with no direct version change, are not).
- An LLM or agent is given tools or untrusted text.

**If none hold:** in `design`, write `Security pass: skipped - <reason>` under Risks / Trade-offs; in `specs` and in `apply`'s review, write nothing. Stop. Do not read anything else.

**If any hold:** read `references/method.md` and follow the sections for your phase. It picks the reference lists to read (OWASP Top 10 lists, MITRE CWE Top 25, framework hints) from what the change touches, and sets the `[Threat T<n>: <category>, <High|Medium|Low>] → Mitigation (<source>)` line for `design.md`.
