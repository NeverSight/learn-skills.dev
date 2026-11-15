---
name: awesome-bug-bounty
description: Use when doing bug bounty hunting, vulnerability research, security report writing/analysis, payload or WAF-bypass selection, business logic / IDOR / race / API testing, recon methodology, tool choice (Burp vs Caido vs ZAP, AI pentest agents, MCP security testing, headless browsers), or looking up writeups/programs — e.g. "find XSS payload", "business logic checklist", "SSRF bypass", "HackerOne top reports", "bug bounty methodology", "which tools to install". Merges curated knowledge with source-repo fallbacks; authorized testing only.
license: MIT
---

# Awesome Bug Bounty

Distilled knowledge base for bug bounty hunting and authorized security research. **Paths below are relative to this skill's directory.** Prefer them; only fetch source repos (Fallback table) when deeper detail is needed.

## Operating rules

1. Read extended detail from `knowledge/*.md` before improvising:
   - `knowledge/vuln-types.md` — per-vuln hunt focus + example patterns
   - `knowledge/payloads.md` — payload/bypass cheat sheet by context
   - `knowledge/business-logic.md` — business logic + race condition playbooks
   - `knowledge/methodology.md` — recon/API methodology, best practices, non-duplicated engagement path, report template, wordlists
   - `knowledge/tools.md` — tool-choice matrix: proxies, AI-native hunters, Obscura, MCP stack, authz/API/bizlogic tools
   - `knowledge/install.md` — install commands + post-install setup (API keys, proxy CA, MCP registration)
2. For writeup links, full payload lists, or tool internals: fall back to source repos via registered opencode references (`@awesome-bb-writeups`, `@bug-bounty-reference`, `@payloads-all-the-things`, `@hack-skills`, `@bizlogic`, `@aw-junaid-bug-bounty`, `@hackerone-reports`, `@autorizepro`, `@burp-api-security-suite`, `@awesome-bugbounty-tools`, `@obscura`, `@caido-skills`) or the Fallback table URLs. If a reference isn't registered, use the GitHub URL.
3. **Authorized testing only.** Stay inside program scope and rules of engagement.
4. Evidence standard for reports: clear impact, minimal repro steps, PoC request-response, severity justification, fix guidance.

## Operating profile gate (ask before acting)

**When:** at the first action-taking turn of a session/engagement — **skip entirely** if the user already stated preferences/rules in this conversation, or if `engagements/<target>/profile.yaml` (or an equivalent profile the user pointed to) already exists. Never re-ask within a session after answers are given.

**How:** ask **once**, using the `question` tool, a single question call containing the full set below as multiple sub-questions:

> **"Operating profile for this engagement?"**
> - `Defaults — Stealth (Recommended)` — in-place/Ollama LLM, no cloud keys, scope taken as-given (no expansion), focus = broad recon, recon + verify layers, **install only what scope needs**, MCP: pd-tools & obscura, **no GitHub push**. Applied immediately, no further prompts.
> - `Configure…` — answer the full set below (one `question` call, all items together).

Full set (only when `Configure…`):

1. **Target + scope source** — `Program URL (HackerOne/Bugcrowd/Intigriti/YesWeHack page)` · `Domain / wildcard list pasted` · `scope.yaml / scope.txt file path` · `Just a name — I'll paste scope next`
2. **Scope discovery** — `Use scope as-given (Recommended for Stealth)` (never touch out-of-scope; no expansion crawling) · `Fetch program scope from platform page` (parse in-scope/out-of-scope, rules, bounty table into `scope.yaml`) · `Passive expansion` (crt.sh, subfinder passive, GitHub dorks — no active touch, then filter to scope) · `Full attack-surface map` (passive + httpx/katana live probe on in-scope only)
3. **Vuln focus** (multiple) — `Broad recon` · `XSS` · `SQLi` · `IDOR / BOLA / API` · `Auth / ATO / JWT / OAuth` · `SSRF / XXE / OAST` · `Subdomain takeover / misconfig` · `Secrets / exposure` · `Business logic / race` · `MCP / LLM / prompt-injection`
4. **Mode** — `Stealth / no API keys (Recommended)` (local/offline tools only; `HEXSTRIKE_API_KEY` and proxy CA are local auth, allowed) · `Balanced` (in-place LLM + read-only keys like `GITHUB_TOKEN`, no paid LLM APIs) · `Full` (cloud API keys per tool)
5. **LLM backend** — `In-place (opencode session model)` · `Ollama (http://localhost:11434/v1)` · `Cloud API keys` · `None — deterministic only`
6. **Tool layers** (multiple) — `Proxy (Burp/Caido/ZAP)` · `Recon stack` · `Verify (sqlmap/dalfox/interactsh)` · `Obscura browser` · `bizlogic` · `AI hunter` · `MCP/LLM-offensive suite`
7. **Install policy** — `Install only what scope/focus needs (Recommended)` (health-check → `knowledge/install.md` section for focus only; nothing extra) · `Install core now` (one-shot §9 block + proxy/Obscura/MCP per layers) · `Don't install — use system as-is` (health-check, report gaps, continue with whatever is on PATH; never run install commands)
8. **MCP surface** (multiple) — `pd-tools` · `hexstrike` · `obscura` · `ptai` · `mcp-bb` · `none`
9. **GitHub persistence** — `No push (Recommended)` (local `engagements/<target>/` only) · `Push workspace to GitHub (private)` · `Push workspace to GitHub (public)` — when push is chosen, account selection is via `gh auth switch` (interactive account picker, never a pasted token), then `gh repo create` + push.

**Scope → minimal-tool map** (used when Install = `scope-needs` — install/read only these sections of `knowledge/install.md`):

| Focus / scope | Install only |
|---|---|
| Broad recon / unknown | §1 recon (subfinder, httpx, dnsx, katana, nuclei, ffuf) + §10 health check |
| XSS | httpx, katana, dalfox, obscura (§4 for DOM XSS) |
| SQLi | httpx, katana, nuclei, sqlmap (§2) |
| IDOR / BOLA / API | httpx, katana, arjun, nuclei, AutorizePro/BurpAPISecuritySuite (§3 proxy) |
| Auth / ATO / JWT | proxy (§3 Caido/Burp) + AutorizePro, nuclei, gitleaks |
| SSRF / XXE / OAST | httpx, katana, interactsh-client (§2), ZAP/Burp Collaborator (§3) |
| Takeover / misconfig | subfinder, dnsx, nuclei (+ takeover templates) |
| Secrets / exposure | gitleaks, trufflehog binary (§2) |
| Business logic / race | proxy (§3) + bizlogic (§5) + Turbo Intruder / Caido Automate |
| MCP / LLM | obscura (§4) + §8 MCPScan/mcpsec/mcpwn + AI Scanner (§7) |

**After answers:** write them to `engagements/<target>/profile.yaml` (keys: `target`, `scope_source`, `scope_expand`, `focus[]`, `mode`, `llm`, `layers[]`, `install`, `mcp[]`, `github{push, visibility}`; env names only, never secrets), then obey for the rest of the engagement:

| Profile choice | Enforced behavior |
|---|---|
| Scope `as-given` | Never expand beyond provided hosts; no platform fetch, no passive enum outside scope; write `scope.yaml` verbatim then filter once |
| Scope `fetch from platform` | Fetch program page / API, extract in-scope, out-of-scope, rules, rate limits into `scope.yaml`; ask before testing if scope parse is ambiguous |
| Scope `passive expansion` / `full map` | crt.sh / subfinder-passive only first (archive pullers like gau/wayback rarely return usable data — skip them); active probe (httpx/katana) only against confirmed in-scope; everything filtered to `scope.yaml` before fan-out |
| Focus set | Install + run only rows matching focus in Scope → minimal-tool map; other vuln classes are out-of-scope for tooling this engagement |
| Mode `Stealth` | Never suggest/export cloud API keys; Caido AI plugins, Burp AI, AutorizePro AI **off** unless backend = Ollama; prefer offline/zero-dep tools (`nuclei -duc`, crt.sh/subfinder passive); hexstrike/Obscura only as **local stdio** MCP; active scanning rate-capped |
| Mode `Balanced` | In-place/Ollama only for LLM; read-only GitHub PAT allowed; no paid API suggest |
| Mode `Full` | Per-tool keys from `knowledge/install.md` §11 as needed; AI hunters may use cloud LLMs |
| LLM `In-place` | All AI features pointed at the session agent — zero key setup |
| LLM `Ollama` | Point tools at `http://localhost:11434/v1`; verify reachable before starting |
| LLM `None` | Deterministic only: `ptai --no-llm`, no AI triage steps in playbooks |
| Layer unchecked | Do not install, run, or mention that layer as a next step this engagement |
| Install `scope-needs` | `knowledge/install.md` §10 health check first, then install **only** binaries for the chosen focus/layers (map above); report skipped sections as out-of-scope, not missing |
| Install `core` | One-shot `knowledge/install.md` §9 block + selected layers (§3/§4/§6/§7); then §10 health check |
| Install `Don't install — use system as-is` | Health-check (`knowledge/install.md` §10) and report gaps, then **continue with whatever is on PATH** — adapt playbooks to available tools, never run install commands |
| MCP `none` / unchecked | Leave servers `enabled: false` in `opencode.jsonc`; drive tools via shell instead |
| GitHub `No push` | Keep everything local in `engagements/<target>/`; never run `gh`/`git push` |
| GitHub `Push (private/public)` | At engagement end (or on demand): sanitize workspace (strip secrets/tokens/PII from PoCs, ensure `.gitignore` covers `findings/raw/`, sessions, cookies), then account-pick + create + push per Push flow below |

Declining the gate or saying "use defaults" = **Defaults / Stealth** above, recorded without further prompting.

### GitHub push flow (only when `github.push: true`)

Never paste tokens. Account selection is always via `gh`:

```bash
# 1) pick account interactively (pre-authed accounts only)
gh auth status
gh auth switch   # user selects account in terminal picker

# 2) init + sanitize (run inside engagements/<target>/)
git init -b main
cat > .gitignore <<'EOF'
findings/raw/
*.har
*.cookies
.env
*token*
*secret*
EOF

# 3) create + push (visibility from profile: private|public)
gh repo create <owner>/<repo> --private|--public --source=. --push
# existing repo instead:
# git remote add origin git@github.com:<owner>/<repo>.git && git push -u origin main
```

Rules: private by default; public only if profile says `visibility: public`. Never push secrets, raw cookies, or unredacted PoCs — review `git status` + `git diff` before `gh repo create`. If `gh auth status` shows no account, run `gh auth login` first, then `gh auth switch`.

## Engage flow (impact-first)

0. **Profile gate** — once per engagement as above; persist `profile.yaml`; all later steps obey it.
1. **Scope** — resolve scope per profile (`as-given` vs `fetch from platform` vs `passive expansion`): write the scope manifest (`knowledge/methodology.md` → non-duplicated path): in-scope hosts, exclusions, rate limits, test windows. Every tool consumes this one file.
2. **Install (scoped)** — `knowledge/install.md` §10 health check, then per install policy: `scope-needs` = only focus/layer binaries, `core` = §9 block, `Don't install` = adapt to system as-is and continue.
3. **Recon / attack-surface map** — single deduped workspace: assets → live hosts → site/API/auth surfaces (union + `uro`/`sort -u`, no per-tool re-enumeration); render SPAs with Obscura/Playwright; note in-scope MCP/LLM features.
4. **Route by surface** — highest-impact path first (auth bypass > ATO > RCE > SSRF/IDOR > XSS > info leaks), filtered to chosen focus[].
5. **Deep playbooks** — read matching `knowledge/*.md` section; escalate to fallback repos only if uncovered. Fan-out tools **read** the shared surfaces, never re-scan them.
6. **Report** — dedupe findings by `METHOD+host+path+param+class`; impact-first writeup per template; one submission per issue.
7. **Push (optional)** — only if `github.push: true`: sanitize, `gh auth switch` account pick, `gh repo create --private|--public --source=. --push` per Push flow above.

## Category router (symptom → knowledge → fallback)

| Symptom / surface | Knowledge | Primary fallback |
|---|---|---|
| XSS, SQLi, SSTI, RCE, LFI/upload, SSRF, CSRF/CORS, smuggling, takeover, cache, host header, 401/403, SAML, most vuln classes | `knowledge/vuln-types.md` (+ `knowledge/payloads.md` for injection/WAF contexts) | PayloadsAllTheThings, Awesome-Bugbounty-Writeups, bug-bounty-reference, hackerone-reports `docs/tops_*` |
| IDOR/BOLA, API recon, GraphQL, mass assignment | `knowledge/vuln-types.md`, `knowledge/methodology.md`, `knowledge/tools.md` | AutorizePro, BurpAPISecuritySuite, hack-skills api-sec |
| Auth bypass, 2FA/MFA, OAuth/JWT, ATO | `knowledge/vuln-types.md` | bug-bounty-reference, hack-skills auth-sec |
| Business logic, race conditions | `knowledge/business-logic.md` | hack-skills, bizlogic, PayloadsAllTheThings, hackerone-reports TOPRACECONDITION |
| Recon, wordlists, engagement workspace, report template, SPA browsing | `knowledge/methodology.md` + `knowledge/tools.md` (Obscura) | aw-junaid/bug-bounty, obscura |
| Proxy / scanner / AI hunter / MCP tool choice, agent orchestration | `knowledge/tools.md` | awesome-bugbounty-tools, caido-skills, hexstrike-ai, pd-tools-mcp |
| Install commands, API keys, proxy CA, MCP registration | `knowledge/install.md` | upstream repo README |
| Mode / LLM / layers / MCP / scope / install / GitHub | Operating profile gate → `profile.yaml` | `knowledge/install.md` §10–12 |
| MCP server or LLM app testing (prompt injection, tool poisoning) | `knowledge/tools.md`, `knowledge/payloads.md` | MCPScan, mcpsec, mcpwn, AI Scanner |

Covered classes are indexed in `knowledge/vuln-types.md` (XSS → MCP abuse).

## Fallback repositories

| Reference alias | Repository | Role |
|---|---|---|
| `@awesome-bb-writeups` | [devanshbatham/Awesome-Bugbounty-Writeups](https://github.com/devanshbatham/Awesome-Bugbounty-Writeups) | Writeups indexed by bug type |
| `@bug-bounty-reference` | [ngalongc/bug-bounty-reference](https://github.com/ngalongc/bug-bounty-reference) | Writeups by bug nature (XSSI, OAuth, money, business logic) |
| `@payloads-all-the-things` | [swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings) | 64+ vuln categories: payloads, bypasses, methodology |
| `@hack-skills` | [yaklang/hack-skills](https://github.com/yaklang/hack-skills) | 100+ agent skills; master/category routers |
| `@bizlogic` | [ekomsSavior/bizlogic](https://github.com/ekomsSavior/bizlogic) | Business-logic heuristic scanner (9 checks) |
| `@aw-junaid-bug-bounty` | [aw-junaid/bug-bounty](https://github.com/aw-junaid/bug-bounty) | Methodologies, cheatsheets, wordlists, report templates |
| `@hackerone-reports` | [reddelexc/hackerone-reports](https://github.com/reddelexc/hackerone-reports) | Top disclosed HackerOne reports by bug type + program |
| `@autorizepro` | [WuliRuler/AutorizePro](https://github.com/WuliRuler/AutorizePro) | Burp authz-enforcement tester + AI FP reduction |
| `@burp-api-security-suite` | [Teycir/BurpAPISecuritySuite](https://github.com/Teycir/BurpAPISecuritySuite) | Burp API suite: recon, 15 attack types, BOLA/IDOR |
| `@awesome-bugbounty-tools` | [vavkamil/awesome-bugbounty-tools](https://github.com/vavkamil/awesome-bugbounty-tools) | Curated tool index by phase (incl. AI Agents) |
| `@obscura` | [h4ckf0r0day/obscura](https://github.com/h4ckf0r0day/obscura) | Rust headless browser for AI agents: CDP + MCP, stealth, SPA rendering |
| `@caido-skills` | [caido/skills](https://github.com/caido/skills) | Caido Client SDK + AI skill (AI-native Burp alternative) |

Deep research: fetch the corresponding reference path (e.g. `@payloads-all-the-things` → `SQL Injection/README.md`) rather than guessing payloads.
