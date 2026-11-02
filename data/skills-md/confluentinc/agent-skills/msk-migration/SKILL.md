---
name: msk-migration
description: Use this skill to assess and plan a migration from AWS MSK (Managed Streaming for Apache Kafka) to Confluent Cloud. Triggers on user intent like "migrate MSK to Confluent Cloud", "move off MSK", "MSK to CC cutover", "Zero-Cut migration from MSK", "kcp scan my MSK", or any discussion of MSK-to-CC assessment, planning, cluster sizing, Cluster Linking setup, Gateway-based switchover, or post-cutover validation. Do NOT trigger for non-MSK Kafka sources (open-source Kafka, Aiven, Confluent Platform, Redpanda) — this skill is MSK-only. Do NOT trigger for greenfield Confluent Cloud projects with no existing Kafka source. Do NOT trigger for general Kafka programming questions (producer/consumer code, Kafka Streams) unrelated to migration.
metadata:
  version: "1.0.1"
---

# AWS MSK Migration to Confluent Cloud

## Scope

This skill helps with **AWS MSK to Confluent Cloud migrations.** Three things it does:

1. **Answer general migration questions** about MSK and Confluent Cloud — concepts (Cluster Linking, the KCP Gateway / Zero-Cut for no-restart cutovers, Schema Linking), feature comparisons (auth, networking, cluster types), tooling (KCP, the cost estimator), and process. Grounded in the skill's references and live-fetched docs.
2. **Produce an Assessment** of an MSK environment — Red Flags audit, Environment Summary, Topic-Level Readiness — from a KCP state file or a manual intake profile.
3. **Produce a Technical Plan** for the migration — cluster type, sizing, networking, auth, switchover approach, schema and connector migration paths, pre-migration workstream, risks.

When the user signals intent for target-cluster provisioning, Cluster Linking setup, client cutover, or post-cutover monitoring, redirect to [docs.confluent.io](https://docs.confluent.io) and the Confluent account team rather than fabricating coverage. Plan-stage decisions about networking, auth, switchover, schemas, and connectors feed those downstream stages — the user carries them out with Confluent's documented tooling and account-team support.

**Do NOT pre-enumerate out-of-scope stages in the opening or anywhere else in user-facing copy.** Phrases like "MVP", "next iteration", "future version", "scoped for later", and proactive lists of stages-this-skill-does-not-cover are roadmap leakage — implementation details about the skill's development that have no place in the conversation with a migration practitioner. State scope positively (what the skill helps with). Handle out-of-scope intent only when the user actually signals it; do not preemptively warn them about what's missing.

## Skill Conduct

These principles govern how the skill engages with the user. They override default assistant behavior.

- **Voice.** Talk to the user about their migration, not about how the skill works. Instructions in this file (reference files, mode detection, stage routing, internal flags, scope boundaries, development roadmap) are implementation detail — do not describe them to the user. Keep skill mechanics invisible. Do NOT use MVP-style framing (e.g., "this is an MVP", "in this iteration", "future version", "scoped for later") or preemptively enumerate stages this skill doesn't cover. State scope positively when asked, and handle out-of-scope intent only when the user signals it.
- **Default opening = stage menu; direct-route only on signal.** When the user's intent clearly signals a specific stage ("we haven't started" → Assess; "ready to cut over" → Switchover; "monitor post-cutover" → Monitor), route directly into that stage's intake or questions. When intent is unclear or the user has just loaded the skill without describing their situation, open with the Mode Detection stage menu and ask where they are in the migration. **Do NOT jump to intake path selection (KCP vs manual) without the user first signaling they're at Assess.** Intake path selection is Assess-stage logic — assuming the user is at Assess before they've said so is a routing error.
- **Stage discipline.** At each stage, address only that stage's decisions and immediate red flags. Do not front-load concerns from downstream stages unless they're red flags at the current stage (e.g., IAM auth is flagged in Assess because it requires pre-migration *before* Zero-Cut is even viable; specific KCP version requirements for Zero-Cut belong at Switchover, not Assess).
- **Command execution requires user approval — except for read-only operations on user-provided files.** Mutating or environment-touching commands (KCP scans, Terraform, AWS CLI writes, Confluent CLI writes, anything that contacts an external system) require approval: present the command and ask whether the user wants to run it or have the skill run it. Do not auto-execute mutating commands without explicit approval. **Read-only operations against files the user has explicitly pointed at — file reads, `jq` queries, structured parsing of state files / profiles / configs — auto-run with no approval prompt.** Those are parsing, not executing, and asking permission to parse a file the user just provided breaks flow. The user is the migration practitioner and stays in control of their environment via the approval rule for mutating commands; read-only file parsing is not an environment-control concern.
- **One command per Bash tool call.** When the skill does run shell commands (with user approval), issue each command as its own Bash tool call. Do NOT batch commands into compound shell expressions — variable assignments with chained invocations (`F=/path; jq '...' "$F"; jq '...' "$F"`), `cmd1 && cmd2`, subshells, loops over collections, heredocs. Reason: Claude Code's built-in safety check matches the allowlist on the first command word; compound expressions don't match cleanly and trigger a permission prompt regardless of the allowlist, even when every individual command is harmless. Single-command invocations match the allowlist and run without prompting. Applies across every stage — scan-coverage audits, `kcp` CLI invocations, `jq` query sequences, Terraform steps, inspection loops. Batching saves no meaningful time and disrupts the user's flow with unnecessary approvals.
- **Ask before acting on branching decisions.** When a stage has multiple paths (intake method, switchover pattern, connector migration approach, etc.), present the options and ask which the user wants before committing to a path.
- **Foundational inputs — ask, never fabricate.** Three inputs are load-bearing for the Plan's core recommendations: topics/partitions/scale, auth posture, and networking accessibility (private/public plus VPC topology). When one is missing, ask — route the user to a re-scan or manual intake — and hold the dependent sections rather than inventing a value. Throughput is foundational-but-degradable: no metrics at all → ask; peak present but P95 missing → use the existing peak fallback with the overestimation flag (do not hard-block). Everything else (EOS/transactions, Kafka Streams, connector detail, costs, client inventory, SR version, IBP, the finer reachability route) is peripheral — assume, label the working assumption, and capture an Open Question per the never-hedge behavior. The discriminator: if the assumption would invent a load-bearing recommendation (cluster type, sizing, networking, auth, switchover), ask; if it fills a peripheral unknown, assume and label. Do not trust a tool's success exit over the data: when a KCP state file shows `kafka_admin_client_information.topics.details` empty across all clusters while `msk_cluster_config` is populated, the deep scan did not complete (almost always private-network unreachability) — this is not a zero-topic cluster. Verify the state file actually contains topic data before proceeding.
- **Avoid temporal claims.** No "as of Q1 2026," no release-date stamps, no "recent changes." Route version and availability facts to live sources; cite version floors (e.g., "v0.7.0+") without dates.
- **Full URLs in citation link text — strict.** Every doc citation in skill output must render the full URL visibly in the rendered text, not just behind the markdown href. The link text `[migrate-cc.md](https://...)` fails this rule — readers who copy the Plan to plaintext, print it, paste it into Slack, or view it in a non-rendering tool see only the filename with no way to navigate to the doc. Three acceptable formats: (1) **bare URL (preferred):** `Per Confluent docs, see https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/migrate-cc.md.` Most markdown renderers auto-link bare URLs; plaintext readers still see the full path. (2) **URL as link text:** `[https://docs.confluent.io/cloud/current/clusters/cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md)` — verbose but explicit. (3) **Short descriptive label + bare URL in surrounding prose:** `Per the cluster types doc (https://docs.confluent.io/cloud/current/clusters/cluster-types.md)`. (These examples show the `.md` form as written in this skill; when you emit the citation to the user, swap the extension to `.html` per the fetch/cite rule in Sources of Truth.) **Forbidden:** filename-only or filename-shorthand link text where the href carries the full URL — `[cluster-types.md](https://...)`, `[migrate-cc.md](https://...)`, `[aws-pni.md](https://...)`, `See [private-networking.md](https://...)`. **Also forbidden:** bare bracketed shorthand with no link at all (e.g., `([cluster-types.html])` in table cells). **Also forbidden:** filename mentions in prose with no URL (e.g., "per private-networking.html"). The href being correct is not sufficient — the URL must be visible. Applies to all doc citations in Plan output, Assess output, and any other artifact the skill produces. Does not apply to KCP repo links where the repo name is the canonical identifier (e.g., `confluentinc/kcp`).

## Mode Detection

This stage menu is the default opening when the user's intent is unclear. Present the three in-scope stages — Explore, Assess, Plan — let the user pick, and route from there. When intent is already clear (explicit stage signal in the user's first message), skip the menu and route directly per the Skill Conduct principles above.

**When describing Assess in the opening, introduce KCP at the first mention of "scan."** Beginners don't know what "scan" means in an MSK migration context — naming the tool grounds it. KCP is Confluent's open-source command-line tool for planning and executing Kafka migrations to Confluent Cloud ([github.com/confluentinc/kcp](https://github.com/confluentinc/kcp)). Acceptable opening phrasing for the Assess row: *"Assess — scan your MSK environment with KCP (Confluent's open-source migration tool at github.com/confluentinc/kcp), or describe it manually if you don't have KCP installed yet. Surfaces red flags and builds an environment profile."* Adjust phrasing for tone, but the load-bearing piece is that "scan" is paired with the tool that does the scanning. A bare "scan your MSK environment" without the KCP intro is not enough for a user who hasn't seen the skill before.

**Explore is the lowest-commitment entry point.** Many users open the skill with general questions before they're ready to scan or plan. Present Explore as a valid path — they don't have to start with Assess. Acceptable opening phrasing for the Explore row: *"Explore — ask general questions about MSK and Confluent Cloud migration. Concepts (Cluster Linking, the KCP Gateway / Zero-Cut for no-restart cutovers, Schema Linking), feature comparisons, tooling, process. I'll cite sources from docs.confluent.io and the KCP repo."* Gloss switchover-pattern jargon (Zero-Cut, Gateway, Dual-write, Manual CL) in plain English on first use, even in this menu — a first-time user does not know these terms. Lead with Cluster Linking, since plain Cluster Linking is the recommended default and the Gateway is the large/complex escalation.

| User Intent | Stage | Read |
|---|---|---|
| "I just have questions" / "what is X?" / "how does Y work?" / "explain Z" / "compare A vs B" / browsing-stage intent | Explore | This file's "Explore stage" section below |
| "scan my MSK clusters" / "assess my environment" / "starting fresh" | Assess | references/assess.md |
| "what cluster type should I use" / "plan my migration" | Plan | references/plan.md |
| "set up Cluster Linking" / "switch my clients over" / "monitor post-cutover" / "provision target cluster" | Out of scope (Provision / Migrate / Switchover / Monitor) | Decline and redirect to docs.confluent.io and the Confluent account team. Still offer Assess or Plan if useful. |

If the user asks about KCP commands or MCP tools directly, use `references/kcp-commands.md` or `references/mcp-integration.md` respectively — reference material, not user-facing stages.

If overall intent is still unclear, start at Explore — let the user ask whatever they want, then route to Assess or Plan when they signal readiness. When the user signals an intent for downstream execution stages (Provision, Migrate, Switchover, Monitor) — for example "set up Cluster Linking", "switch my clients over", "monitor post-cutover" — acknowledge that those are out of scope for this skill and redirect to docs.confluent.io and the Confluent account team. Still complete an Assess or Plan if the user wants those, since Plan's switchover-approach and pre-migration-workstream decisions inform downstream execution.

## Explore stage

Conversational Q&A about MSK-to-CC migration. No artifact produced. The user asks questions; the skill answers grounded in its references and live-fetched docs. Exit conditions: user signals readiness for Assess ("let's scan my environment", "I have a state file"), or signals readiness for Plan ("I have an environment profile already"), or ends the conversation.

**What Explore covers (in scope):**

- **Concepts:** Cluster Linking (mirror-then-cutover, the recommended default), the KCP Gateway / Zero-Cut (a proxy that cuts clients over with no restart, for large/complex environments), Schema Linking, mTLS vs API Keys vs OAuth, PNI vs PrivateLink vs VPC peering vs Transit Gateway, eCKU vs CKU sizing, tiered storage, MSK Connect vs self-managed Connect, Debezium migration paths.
- **Comparisons:** MSK Provisioned vs Confluent Cloud Enterprise/Dedicated, MSK Serverless vs Enterprise, IAM auth on MSK vs CC auth methods, MSK Glue Schema Registry vs CC Schema Registry.
- **Tooling:** What KCP is and what it does, what the KCP commands produce, what CMU is, what the public cost estimator is for, what `kcp create-asset migrate-acls iam` does vs `migrate-acls kafka`.
- **Process:** What a typical migration looks like, what stages exist, what pre-migration work is involved (IAM → SCRAM, schema migration order), what Zero-Cut prereqs are.
- **Specific feature questions:** "Does CC Enterprise support mTLS on Azure?", "What's the Enterprise eCKU cap on PNI?", "What's the CL source Kafka version floor?" — answer by fetching the relevant docs.confluent.io page (using the `.md` URL pattern from the Fetch tool directive) and citing the value with the source.

**What Explore does NOT cover:**

- **Customer-specific recommendations without source data.** "Should I use Enterprise or Dedicated for my cluster?" requires Assess (sizing math depends on throughput, partitions, ACLs from the source). Redirect: "That's an Assess question — I need your MSK environment details first. Want to scan with KCP or describe it manually?"
- **Non-MSK Kafka sources.** The skill is MSK-only. Open-source Kafka / Confluent Platform / Aiven / Redpanda migrations are not in scope.
- **Greenfield Confluent Cloud setup.** Migration only.
- **General Kafka programming questions** unrelated to migration (producer/consumer code, Kafka Streams app development, schema design).
- **Pricing dollars.** Per SKILL.md commercial-signals row — direct to the public cost estimator and the Confluent account team. Feature comparisons are fine; specific dollar figures are not.

**Conduct in Explore:**

- **Answer with citations.** Every claim ties to a specific source — docs.confluent.io page (cite the URL), KCP repo file (cite the GitHub URL), this skill's reference files. Don't answer from training data alone — the migration product surface evolves; live sources are authoritative.
- **One question at a time.** Answer what was asked. Don't pre-emptively dump the full reference file. If the user asks "what is Cluster Linking?", answer that — don't also explain Schema Linking and Zero-Cut unless they ask.
- **Offer the natural next step at the end of each answer.** Examples: *"Want me to walk through how Cluster Linking applies to your environment specifically? Tell me about your MSK setup and we can move to Assess."* / *"Curious about how this would look in your cutover? Once you've scanned with KCP, I can produce a Plan."* Optional, low-pressure — the user may just want more questions answered.
- **Stay in scope.** If the user asks about something outside MSK→CC migration (e.g., "how do I use Flink?"), acknowledge briefly and redirect — don't pull them out of the migration context unless they explicitly want to leave.
- **Honest about limits.** "I don't have access to live customer data — Confluent's account team can confirm specifics for your org" is preferable to fabricating a customer-specific answer.

**Routing out of Explore:**

- User signals scan readiness ("I have a state file at X" / "let's run a scan" / "ready to assess") → load `references/assess.md` and proceed.
- User signals planning readiness ("I have an environment profile already" / "let's build a plan from this data") → load `references/plan.md` and proceed.
- User asks an Assess-shaped question (cluster-type recommendation, sizing math, networking choice for their environment) → say so, offer to start Assess: "That depends on your environment. Want to scan with KCP or describe your setup manually?"

## Intake Path Selection

Present both paths to the user and ask which they want. Do NOT auto-detect tool availability by running bash — per the command-execution principle, user approval is required before any command runs. Present the two options, let the user choose, and then proceed.

**Path 1 — KCP deep scan.** KCP is Confluent's open-source migration tool ([github.com/confluentinc/kcp](https://github.com/confluentinc/kcp)) for assessing AWS MSK environments and generating migration assets (Terraform, mirror-topic configs, migration orchestration) for Confluent Cloud. If you have it installed and AWS credentials for your MSK account, it can scan your environment and produce a `kcp-state.json` file that becomes the canonical profile for every downstream stage. Richest path when available.

**Path 2 — Manual intake.** For users who don't have KCP installed, don't have AWS credentials available, or are in a restricted AWS account / pre-engagement context. We walk through ~11 question groups and populate `assets/migration-profile.yaml`, which serves the same role downstream as a KCP state file — less detailed but workable.

**If the user already has a KCP state file**, treat that as completed KCP path output — skip directly to parsing it.

Once the user picks a path, load `references/assess.md` and follow that stage's reference for the next steps. Do not ask auxiliary questions or run any commands before the user has chosen.

**First-mention reminder:** whenever KCP is introduced in a conversation (including downstream stages), include the brief intro — who built it, that it's open source, the GitHub URL, what it does in the migration context. Don't assume the user knows.

## Stage Workflow

Each stage has entry criteria, an exit artifact, and a reference file. Each stage validates its own work before handoff.

| Stage | Entry | Exit Artifact (validation for this stage) | Reference |
|---|---|---|---|
| Explore | User has questions about MSK-to-CC migration concepts, comparisons, tooling, or process | No artifact — conversational Q&A grounded in skill references and live-fetched docs. Exit when user signals readiness for Assess or Plan, or ends the conversation. | SKILL.md "Explore stage" section |
| Assess | User starts migration | Environment profile with required fields populated; red flags surfaced; when a KCP state file is provided with `topics.details[]` populated, a Topic-Level Readiness section classifies user topics into four buckets (Skip / Manual / Needs Config / Moves Cleanly) — see references/assess.md "Topic-Level Readiness" section | references/assess.md |
| Plan | Environment profile exists | Technical Plan output starts with the "About this Technical Plan" boilerplate from references/plan.md; architecture decisions documented; pre-migration requirements identified | references/plan.md |

Users may enter at any of the three stages. Explore is often the entry point for users who are still learning; Assess is the entry point for users who have an MSK environment to scan or describe; Plan is the entry point for users who already have an environment profile. The Plan exit artifact is the handoff for downstream execution stages (Provision, Migrate, Switchover, Monitor), which the user carries out with their Confluent account team using docs.confluent.io as the reference.

## Cross-Stage Decision Logic

### Cluster type: default to Enterprise, escalate to Dedicated only on hard limits

Enterprise is the recommended target for every migration. It is elastic, supports private networking (PrivateLink and PNI on AWS), supports mTLS on AWS, supports BYOK on all clouds, supports client quotas, and covers the vast majority of migration scenarios without the operational overhead of CKU sizing. Recommend Dedicated **only** when the source environment triggers one of the hard limits below.

**How to use the hard-limits table:**

- **ROUTE rows require a live fetch before answering.** Do not answer an escalation question from memory. Fetch the cited doc section, extract the value, and cite the URL in the response.
- **HARDCODED row protocol.** A HARDCODED row encodes a fact the skill could not route to a structured live source at design time. Treat the cached value as a working assumption, not a verified fact. Two sub-categories:
  - **Doc-cited HARDCODED** — a doc URL is given, but the fact lives in prose rather than a structured row. Before recommending, fetch the cited URL and check whether a structured representation now exists (table row, bullet list, version matrix). If yes, use the doc's value and tell the user "Skill's cached value was X; doc now says Y; using the doc value." If no structured representation exists, present the recommendation **conditionally on the cached assumption** — phrase it as "If [cached condition] still holds (the docs do not currently publish a structured matrix to confirm — see [URL]), then [recommendation]; otherwise [alternative]." Do NOT date-stamp the cached value to the user; the cited URL is the live-verification signal.
  - **Uncited HARDCODED** — no public doc URL exists for this fact (e.g., "no canonical public doc found"). Keep the "last verified YYYY-MM-DD" stamp on these rows. Without a URL the user can verify against, the date stamp is the only staleness signal they have. Still apply the conditional framing in the recommendation.
- **Multi-trigger profiles.** When more than one row applies, apply each independently and cite every trigger. Do not stop at the first match.
- **Maintenance for uncited HARDCODED rows.** Uncited rows have no public URL to drift-check against, so the date stamp is the only staleness signal. Review uncited HARDCODED rows on a quarterly cadence: confirm cached values with the relevant Confluent product team (Cluster Linking, Networking, Schema Registry, etc.) or internal product docs. Update both the cached value and the "last verified YYYY-MM-DD" stamp when reviewed. If a structured public doc emerges that exposes the fact, convert the row from HARDCODED to ROUTE.

| Trigger Category | Escalation Condition | Source |
|---|---|---|
| Projected eCKU exceeds Enterprise cap | Any of three capacity checks fails (see Row 1 sub-bullets below) | **ROUTE:** cluster-types.html — fetch per-eCKU ingress, per-eCKU egress, per-eCKU partition rate, Enterprise eCKU cap from the Enterprise column |
| ACL count exceeds Enterprise cap | Source scan ACL count ≥ Enterprise cap | **ROUTE:** cluster-types.html — fetch the ACLs row of the comparison table for the relevant cluster type (Enterprise / Dedicated) |
| Networking requires VPC Peering or Transit Gateway | Hub-and-spoke or direct peering topology | **HARDCODED (doc-cited)** — cached assumption: Enterprise supports PrivateLink + PNI only; VPC Peering and TGW are Dedicated-only. cluster-types.html prose only, no structured row. Apply HARDCODED protocol. |
| Broker-side schema ID validation required | `confluent.value.schema.validation=true` on source or stated requirement | **ROUTE:** [broker-side-schema-validation.md](https://docs.confluent.io/cloud/current/sr/broker-side-schema-validation.md), Prerequisites section |
| mTLS required, target cluster type doesn't support it on the chosen cloud | Source uses mTLS AND target cluster type × cloud combination doesn't support mTLS | **ROUTE:** [cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md) — fetch the mTLS row of the feature comparison table to verify support before recommending escalation. |
| High-throughput Kafka REST Produce v3 | REST-based producers with non-trivial throughput | **ROUTE:** cluster-types.html, "Kafka REST Produce v3 - Max throughput" row |
| 99.95% single-zone SLA required | Explicit contractual SLA requirement | **ROUTE:** cluster-types.html, "Uptime service level agreement options" table. Legal SLA PDF is not programmatically routable. |

**Row 1 escalation check (compound capacity math):**

- Fetch four facts from the `.md` variant of cluster-types: `https://docs.confluent.io/cloud/current/clusters/cluster-types.md` (the `.html` page truncates the comparison table; the `.md` variant returns clean data). Cite it in user-facing output as the `.html` form (swap the `.md` extension per the fetch/cite rule in Sources of Truth). Values to extract from the Enterprise column: per-eCKU ingress (MBps), per-eCKU egress (MBps), per-eCKU partition rate (use "Partitions (pre-replication)" row, not "Compactable partitions"), Enterprise eCKU cap.
- **Verify the fetch before computing.** Per the verification protocol in `references/plan.md` Capacity Sizing Procedure step 5a: each value must be a concrete number AND must be cited with a row label that names the dimension explicitly (e.g., "Ingress (MBps)", "Partitions (pre-replication)"). If any value is missing, unparseable, or extracted from an unexpected row, STOP — do not produce a cluster-type verdict. Mark as blocked on cluster-types fetch failure and ask the user to verify manually. Falling back to remembered values from training data is not permitted — wrong per-eCKU values produce a wrong cluster-type call that downstream readers cannot detect.
- Compute three divisions against the user's profile:
  - peak ingress ÷ per-eCKU ingress
  - peak egress ÷ per-eCKU egress
  - partition count ÷ per-eCKU partition rate
- If **any** of the three exceeds the Enterprise eCKU cap, escalate to Dedicated and cite which check triggered.

**Soft triggers — operational and compliance signals the skill decides on:**

| Condition | Recommendation | Why |
|---|---|---|
| Strict change-control around capacity | Dedicated | Dedicated capacity changes only via explicit CKU change. Enterprise's elastic scaling happens automatically, which can violate change-control policies. |
| Regulatory requirement for dedicated infrastructure | Dedicated | Some compliance regimes require isolation guarantees elastic multi-tenant offerings don't provide. |

**Commercial signals — flag to Sales, don't decide:**

| Signal | Skill Behavior |
|---|---|
| Customer prefers fixed predictable billing | Keep Enterprise default. Flag: "Billing-model preference is a commercial decision. Sales can walk through CKU vs. eCKU pricing implications." |
| Very large steady-state workload with sustained high utilization | Keep Enterprise default. Flag: "Workloads like this are a common case where customers evaluate Dedicated for pricing efficiency at scale. Worth a Sales conversation." |
| Direct pricing question ("what will this cost?", "TCO", "savings vs. MSK") | Decline to produce a dollar figure. Route to the **public [cost estimator](https://www.confluent.io/pricing/cost-estimator/)** as the first-line self-service handoff (user enters their own throughput, retention, networking inputs and gets list-price ranges). Frame as "pricing is a Sales conversation by design — the cost estimator is the right entry point." If the customer needs a deal quote rather than list-price math, escalate to the Confluent account team. Do NOT compute synthetic estimates from scan data. |

**Source-to-target mapping:**

| Source | Default | Escalate if |
|---|---|---|
| MSK Serverless | **Enterprise** | Any hard limit above applies (rare — both are elastic) |
| MSK Provisioned (any size) | **Enterprise** | Any hard limit above applies |

Non-MSK Kafka sources are not handled by this skill. Freight is a documented cluster-type option ([cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md)); if a user asks, route them to the live doc rather than asserting guidance.

### Auth migration mapping (MSK-supported auth types)

Auth migration is a two-step decision: (1) handle any source-side pre-migration requirements, then (2) pick the target CC auth method based on the customer's identity-model preference. The source-side step is determined by the source MSK auth type; the target-side step cascades from `target_context.target_identity_model` (a Plan-stage customer input).

**Source-side handling by MSK auth type:**

| Source Auth (MSK) | Plain Cluster Linking (default) | If the Gateway is chosen (large/complex) |
|---|---|---|
| SASL/SCRAM-SHA-512 | No change — CL authenticates with SCRAM. | Supported (SCRAM client/transit auth). |
| mTLS | No change — CL authenticates with mTLS. | Supported. |
| Unauthenticated (plaintext) | CL leg needs no change, but those clients have no CC equivalent and break at cutover — move them to a CC-supported method before cutover (see Red Flags: unauthenticated listener). | Same client move required. |
| AWS IAM — MSK Provisioned | No client change. Add a SASL/SCRAM listener for the cluster link only, OR use a KCP jump cluster. | Gateway does not accept IAM — reshape clients off IAM to SCRAM/mTLS first. |
| AWS IAM — MSK Serverless | KCP jump cluster only (Serverless is IAM-only; you cannot add a listener). | Not applicable. |

**Always cite the CL security doc (https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/security-cloud.md) in the Plan's Auth Approach source-side handling — for every source auth type (SCRAM, mTLS, IAM, unauthenticated), not just IAM.** It is the source of truth for which source auth methods CC Cluster Linking supports; emit the URL, do not leave it as an unstated "verify live." Verify current support against it live. SASL/SCRAM is a valid CL **source** auth and a valid Gateway **transit/client** auth, but is NOT a Confluent Cloud **target/client** auth method — never recommend SCRAM as a CC target.

MSK clusters may run multiple listeners/auth methods at once; reason over the full set. An unauthenticated listener has no CC target — those clients must move to a CC-supported method before cutover.

**Step 0 — preserve a CC-supported source method.** If the source already authenticates with a method Confluent Cloud supports for clients (mTLS or OAuth/OIDC), default the target to that same method and state "preserving source auth method — already Confluent-supported." The customer can override. The identity-model cascade below applies only when the source method has no CC equivalent (SASL/SCRAM, AWS IAM, unauthenticated) or the customer wants to change. Default-to-API-Keys is the fallback for non-preservable source methods and the undecided case — not the universal default.

**Target auth options (cascade from `target_context.target_identity_model`):**

| `target_identity_model` | CC target auth method | Notes |
|---|---|---|
| `oauth` | SASL/OAUTHBEARER | Integrates with enterprise IDP. Requires IDP integration setup on the CC side. |
| `api_keys` | SASL/PLAIN (CC-managed API keys on service accounts) | Service-account credentials managed by CC. Default when customer is undecided. |
| `mtls` | SSL with client certs | Customer-managed PKI. Verify cluster-type / cloud availability live against [cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md). |
| `undecided` | Default to API Keys (SASL/PLAIN); flag as Open Question to close before Provision | Working assumption keeps Plan unblocked; customer can override. |
| `other` (SAML-only, federated assertion not fitting OAuth/IDP integration, custom identity proxy) | Defer to Confluent account team | CC's published identity models don't cover all enterprise scenarios. |

**Sources of truth:** [CC auth overview](https://docs.confluent.io/cloud/current/security/authenticate/overview.md) for CC auth methods and identity models; [cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md) for the live auth × cluster-type matrix (including mTLS cloud availability — fetch the mTLS row of the feature comparison table before recommending mTLS as a target auth method); [KCP zero-cut guide](https://confluentinc.github.io/kcp/latest/getting-started-with-zero-cut-migrations/) for Gateway auth-swap matrix. When starting-point guidance and live sources disagree, the live source wins.

### Switchover approach selection

Confluent recommends a straight **Cluster Linking** migration (mirror the source, then cut clients over) for most environments — it is the simplest path. Cluster Linking mirrors the source byte-for-byte and syncs consumer offsets; you cut clients over to Confluent Cloud once mirrors are caught up. This can be done incrementally (promote mirror topics in batches by team or criticality) or in a single window. Incremental vs. single-window is a scoping choice inside plain CL, not a separate recommended mechanism.

The **KCP Gateway (Zero-Cut)** (a proxy flips clients over with no restart) is for genuinely large or complex environments where a per-group atomic flip with no client restarts is worth the additional gateway infrastructure and licensing. Recommend it when a no-restart/minimal-downtime requirement, a high client-coordination burden, or high blast radius makes a coordinated client cutover impractical.

| Approach | When to recommend | What the Plan emits |
|---|---|---|
| **Cluster Linking — RECOMMENDED (most migrations)** | Default. The straightforward path for the large majority of environments. | Destination-initiated CL; mirror-then-cutover; consumer offset sync; incremental (batch promotion) or single-window. See https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/migrate-cc.md. |
| **Cluster Linking + KCP Gateway (Zero-Cut)** | Large or complex environments where per-group atomic cutover with no client restarts justifies the gateway overhead. | KCP groups by ownership/criticality; per-group lag-check + execute + validate; per-group rollback. Gateway prereqs fetched live. |
| **Dual-write (blue-green)** | Avoid unless the customer's architecture already requires it (write to both clusters in parallel during validation). | Generic CL for mirroring; rest is customer-owned. No Confluent-specific tooling; double infrastructure cost; operationally complex. |

**Switchover-mechanism selection — default plain CL; recommend the Gateway when any signal fires.** This is a separate axis from the Enterprise-vs-Dedicated capacity rule. Both primary signals are intake-driven, so the trigger does not depend on the optional client-inventory scan. Default to "cutover window acceptable / coordination manageable" → plain CL (matching most migrations). State the reasoning visibly in the Plan: "few clients, window acceptable → plain CL; Gateway warranted if you need zero client restarts or can't coordinate a single window."

| Signal | Tier | Source | Drives Gateway because |
|---|---|---|---|
| No-restart / minimal-downtime requirement (clients can't restart or take a cutover window) | Primary | Intake (`target_context.downtime_tolerance`) | This is the Gateway's defining use case — atomic flip, no restart. |
| Client-coordination burden too high for a single window (many distinct client apps and/or many owning teams) | Primary | Intake (`target_context.client_coordination_burden`; or distinct-app count from `discovered_clients` if client-inventory ran) | A coordinated re-point + restart across many teams in one window is impractical. |
| High blast radius (very high partition/topic counts — e.g., the Row 5 >10k-partition flag — or many clusters) | Secondary | State file | All-at-once manual cutover carries unacceptable risk; per-group rollback has real value. |

**Consumer continuity.** On a destination-initiated Cluster Link, consumer offsets sync from source to destination, so consumers resume from their previous position. Migrate consumers before promoting mirror topics (`consumer.offset.sync.enable=true`); after promotion, source consumers lose offset sync. This is the default plain-CL behavior. On the Gateway path (large/complex), producers and consumers on the same route flip together atomically per group, so there is no producers-first/consumers-later window to manage. This is not a bidirectional-link scenario — bidirectional Cluster Linking is unavailable for an MSK source (see Cluster Linking direction below). A deliberate producers-first, consumers-much-later cutover with a long gap is not a documented MSK migration pattern — defer to the Confluent account team.

**Gateway/Zero-Cut prerequisites — fetch live only when the Plan recommends the Gateway.** Plain Cluster Linking carries no Gateway prerequisites. When the Plan recommends the Gateway for a large/complex environment, its required components (Kubernetes distribution, CP licensing, CL state, minimum KCP version, auth compatibility) evolve as Zero-Cut matures — fetch the current prerequisite list from the [KCP zero-cut guide](https://confluentinc.github.io/kcp/latest/getting-started-with-zero-cut-migrations/) before telling a user whether the Gateway fits. Do not rely on cached prerequisites.

### Cluster Linking direction

**For an MSK source, Cluster Linking is destination-initiated only (`link.mode=DESTINATION`).** There is no direction decision to make. `SOURCE` (source-initiated) and `BIDIRECTIONAL` both require a cluster-link object on the source — a Confluent Server / Confluent Cloud capability. MSK is open-source Apache Kafka, which bidirectional explicitly excludes (https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/cluster-links-cc.md), so neither mode is available. Always emit destination-initiated.

What varies is not the direction but HOW Confluent Cloud reaches a private MSK source. That is a networking question. When `target_networking` is PNI (the AWS-to-AWS private default), ask `target_context.cc_reaches_source` to learn whether the destination VPC has a direct route to the MSK VPC. Either answer still resolves to a destination-initiated link — the difference is whether an additive Egress PrivateLink Endpoint is needed for Confluent Cloud to reach back to the source.

| `target_networking` | How CC reaches the private MSK source | Setup path (always destination-initiated) |
|---|---|---|
| VPC peering | Existing peering provides the route | KCP generates the cluster-link resources once reachability exists. |
| Transit Gateway | TGW provides the route (assumes MSK on the TGW) | KCP generates the cluster-link resources once reachability exists. |
| Public + MSK public | CC reaches MSK over the public endpoint | KCP generates the cluster-link resources once reachability exists. |
| PNI, direct route exists (`cc_reaches_source: true`) | Existing peering / TGW between the CC networking VPC and the MSK VPC | KCP generates the cluster-link resources once reachability exists. |
| PNI, no direct route (`cc_reaches_source: false`) | Add an **Egress PrivateLink Endpoint** — an additive, environment-scoped resource. The cluster stays PNI for ingress. | Set up the egress endpoint per https://docs.confluent.io/cloud/current/networking/aws-egress-privatelink-esku.md; KCP generates the cluster-link resources once reachability exists. |

When `target_context.cc_reaches_source` is needed but unknown, default to "assume a direct route" as a working assumption and flag as an Open Question to close before Provision.

KCP does not provision the networking (PNI or the Egress PrivateLink Endpoint). The egress endpoint is set up per docs.confluent.io and the `confluentinc/cc-terraform-module-clusterlinking-outbound-private` module as a Provision-stage / account-team activity. Verify current requirements live against [aws-egress-privatelink-esku.md](https://docs.confluent.io/cloud/current/networking/aws-egress-privatelink-esku.md) and [cluster-links-cc.md](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/cluster-links-cc.md) before committing the Technical Plan.

### Networking selection

For private AWS-to-AWS migrations, **PNI is the recommended default** (cost-preferred when prereqs are met — PNI charges only for cross-AZ traffic, while PrivateLink adds data processing fees and hourly endpoint fees). PNI is the ingress networking type for every private-MSK-on-AWS case. The cluster flips off PNI only when the PNI gateway limit is reached (≥2 per environment) or the target cloud is Azure/GCP (PNI is AWS-only). Two additive needs do NOT flip the cluster off PNI: when Confluent Cloud has no direct route to the private MSK source, and when `target_context.cc_egress_required` is true (CC managed connectors reaching customer-hosted systems), the Plan adds an Egress PrivateLink Endpoint while the cluster stays PNI for ingress.

**Lay out both options in plain English — most enterprises do not know what PNI is.** Wherever PNI is recommended (in skill answers and in the Plan's Networking Decision), explain both:

- **PNI (Private Network Interface):** Confluent places network interfaces directly in your VPC. AWS-only. Cheapest at steady state because you pay only for cross-AZ traffic. Requires customer-side ENI setup.
- **PrivateLink:** AWS-managed private connectivity via endpoint services. Works on AWS, Azure, and GCP. Adds per-endpoint hourly fees plus data-processing fees, so typically costlier at steady state. Lower setup burden.
- **When to pick each:** PNI for AWS-to-AWS steady-state cost; PrivateLink when the target is Azure/GCP, when the PNI gateway limit (2 per environment) is hit, or when the customer prefers lower setup effort over steady-state cost.

Actual savings are workload-dependent — validate with the Confluent account team. Do not quote a percentage.

| Source Accessibility | Target Cloud | CC Networking | Cluster Type |
|---|---|---|---|
| Private (VPC-internal), direct route to MSK exists | AWS | **PNI** (default — cost-preferred when prereqs met) | **Enterprise** |
| Private (VPC-internal), no direct route to MSK (`target_context.cc_reaches_source: false`) | AWS | **PNI** ingress + additive Egress PrivateLink Endpoint for the CL replication pull | **Enterprise** |
| Private (VPC-internal) + CC egress required (`target_context.cc_egress_required: true`) | AWS | **PNI** ingress + additive Egress PrivateLink Endpoint for outbound | **Enterprise** |
| Private (VPC-internal) + PNI gateway limit reached (≥2 PNI gateways in environment) | AWS | PrivateLink | **Enterprise** |
| Private (VPC-internal) | Azure / GCP | PrivateLink (PNI not available) | **Enterprise** |
| Private (multi-VPC, hub-and-spoke) | AWS | Transit Gateway | Dedicated |
| Private (direct VPC peering existing) | AWS / Azure / GCP | VPC Peering | Dedicated |
| Public | Any | Public endpoint | Enterprise (non-prod only) |

PNI prerequisites and the egress-not-supported constraint: see [aws-pni.md](https://docs.confluent.io/cloud/current/networking/aws-pni.md) for current customer-side setup (ENI count, network interface permissions). PNI does not support egress, so when Confluent Cloud must reach back to the source (no direct route to a private MSK) or out to customer-hosted systems, the documented substitute is an additive Egress PrivateLink Endpoint — see [aws-egress-privatelink-esku.md](https://docs.confluent.io/cloud/current/networking/aws-egress-privatelink-esku.md). The endpoint is additive and environment-scoped; it does not change the cluster's PNI ingress type. PNI cap and gateway limit: aws-pni.html. Networking feature availability by cluster type: [networking/overview.md](https://docs.confluent.io/cloud/current/networking/overview.md) + [cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md).

Compliance, organizational-policy, latency-sensitivity, or substrate-constraint cases that fall outside the three citable exceptions are not published as structured Confluent doc — defer to the Confluent account team.

## Environment Profile

Produced during Assess, consumed by all subsequent stages.

| Field Group | Key Fields | Used In |
|---|---|---|
| Source platform | platform, cloud_provider, kafka_version | Plan (CL compatibility), Migrate (CL setup) |
| Clusters | brokers, topics, partitions, throughput, auth, networking | Plan (sizing, cluster type, networking), Provision (Terraform) |
| Schema Registry | type, subject_count | Plan (migration path), Migrate (Schema Linking vs REST API) |
| Connectors | managed_count, self_managed_count, types | Plan (CMU scope), Migrate (connector migration) |
| Costs | monthly_total, breakdown | Plan (business justification) |

Full schema: `assets/migration-profile.yaml`. Field details: `references/assess.md`.

## Invariants

Non-negotiable defaults for every migration, regardless of user input.

1. **If schemas are in scope, schema migration completes before data migration.** Source-has-SR migrations: migrate schemas via the path chosen in Plan (Schema Linking, REST API, etc.) before CL mirrors carry data. Source-has-no-SR migrations where the user opts to adopt SR during migration: provision CC SR and register initial schemas before data migration. If the user opts to migrate without schemas, record the choice explicitly and skip the schema steps.
2. Private networking for production clusters. Never use public endpoints for production.
3. Cluster Linking source must meet the **migration-use-case** version floor in the [CL source requirements doc](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/index.md) — Kafka 2.4.0+ (or Confluent Platform 5.4.0+ for on-prem sources), NOT the general Kafka 3.0+ floor. This skill is MSK-only and always operates in the migration-exception path, so an MSK cluster on Kafka 2.4–2.9 is CL-eligible for migration on the product-version floor. The source must ALSO meet the `inter.broker.protocol` (IBP) floor — a **separate, general non-Confluent-Cloud-source requirement stated independently of the migration exception.** The migration exception relaxes only the Kafka/CP product version, NOT IBP. Fetch both live — do not cache either cutoff. When extracting, the migration-use-case product floor lives in Footnote [1] under "Supported cluster types" — a footnote, not a prominent table — so fetch the `index.md` variant and read the footnotes; the IBP requirement is stated separately on the same page. Do NOT assume the IBP floor equals the 2.4.0 binary floor (a customer on a newer Kafka binary can still have a stale IBP that fails the requirement, and because IBP can never exceed the running binary version, a binary too old to support the required IBP is ineligible until upgraded). Do not use the general Kafka 3.0+ product floor.
4. Consumer offset sync configured per current [CL offset-sync guidance](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/index.md). Flag names and defaults are product facts — verify live.
5. Maintain source cluster throughout migration. No decommissioning until Monitor stage rollback window has elapsed and stakeholder sign-off is in hand.
6. For Zero-Cut: verify `kcp migration lag-check` shows zero lag before executing. For manual CL: test with canary consumer before switchover.
7. Rollback plan documented before switchover begins. Zero-Cut rollback is clean before promotion; manual after.
8. AWS IAM is an MSK/AWS-proprietary auth method with no Confluent Cloud equivalent. Plain Cluster Linking (the default) handles an IAM-authenticated MSK source **without changing client auth**: for MSK Provisioned, either add a SASL/SCRAM listener used only by the cluster link, or use a KCP jump cluster that bridges IAM; for MSK Serverless (IAM-only, cannot add listeners), the KCP jump cluster is the path. The KCP Gateway does NOT accept IAM — reshape clients off IAM only if the Gateway path is chosen. Verify current CL source-auth support against the [CL security doc](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/security-cloud.md) live.
9. NEVER display or log credentials, API keys, bootstrap server secrets, or .env file contents.
10. NEVER apply Terraform without user reviewing the plan (`terraform plan` before `terraform apply`).
11. All auth credentials created as service accounts, not user accounts.
12. The KCP Gateway (Zero-Cut) is reserved for large or complex environments and has prerequisite infrastructure and licensing requirements. When the Plan recommends the Gateway, fetch the current prerequisites from the [KCP zero-cut guide](https://confluentinc.github.io/kcp/latest/getting-started-with-zero-cut-migrations/) — do not cache. Plain Cluster Linking is the default and carries no Gateway prerequisites.

## Tool Routing

| Operation | Preferred | Fallback |
|---|---|---|
| Discover MSK clusters | KCP CLI `kcp discover` | Conversational intake |
| Scan cluster details | KCP CLI `kcp scan clusters` | Conversational intake |
| Scan Schema Registry | KCP CLI `kcp scan schema-registry` | Conversational intake |
| Scan client inventory | KCP CLI `kcp scan client-inventory` | Conversational intake |
| Cost analysis | KCP CLI `kcp report costs` | Conversational intake |
| Metrics analysis | KCP CLI `kcp report metrics` | Conversational intake |
| Verify CC environment | Local Confluent MCP (`list-environments`, `list-clusters`) | Confluent CLI |
| Verify CC topics / schemas / connectors | Local Confluent MCP (`list-topics`, `list-schemas`, `list-connectors`) | Confluent CLI |
| Generate Terraform | KCP CLI `kcp create-asset ...` | Manual Terraform |
| Zero-Cut cutover | KCP CLI `kcp migration {init,list,lag-check,execute}` | Manual CL + client switchover |

MCP write operations (`create-`, `alter-`, `delete-`) require explicit user confirmation per DTX `destructiveHint`.

## Sources of Truth

The skill encodes judgment, not product facts. Decision frameworks, trigger categories, stage handoffs, and routing logic stay in this skill. Specific numbers, version cutoffs, feature availability, command surfaces, and mapping matrices live in external sources and are fetched live.

**Live-fetch protocol:**

- Before recommending a KCP command, flag, or procedure, fetch the KCP repo.
- Before quoting a cluster-type capacity, version cutoff, or feature-availability state, fetch docs.confluent.io.
- Before claiming Gateway or Zero-Cut support for a given configuration **(only relevant when the Plan recommends the Gateway for a large/complex environment)**, fetch the KCP zero-cut guide.
- **The live source always wins.** If it disagrees with anything cached in this skill, use the live value and tell the user the cached value was stale.
- **Failure handling.** If a ROUTE URL returns a 404 or the page structure has changed materially, surface this to the user, fall back to the HARDCODED value with conditional framing if available, and flag the URL for update.

**Fetch tool — use `WebFetch`, not shell.** `WebFetch` is the only tool to use for every live source in the map below. Do NOT use `curl`, `wget`, `python3 -c`, `python3 <<EOF`, `node -e`, or any shell-based HTML stripping. `WebFetch` handles HTML→markdown conversion and targeted extraction in one call. Pass a focused prompt (e.g., "Extract per-eCKU ingress MBps, egress MBps, partition rate, and eCKU cap from the Enterprise column") rather than fetching raw content and parsing. For GitHub-hosted sources (KCP repo, zero-cut guide), `WebFetch` against the rendered URL works; the `gh` CLI is also acceptable for KCP repo reads. No Confluent MCP tool exposes a `fetch-docs` capability — `WebFetch` is the only fetch path.

**docs.confluent.io URLs in this skill are written with the `.md` extension.** The Confluent docs site publishes LLM-friendly markdown at the same path with a `.md` extension instead of `.html`. The `.md` variant returns clean structured data with all rows intact; the `.html` rendered page truncates wide comparison tables (e.g., the eCKU/CKU comparison on cluster-types) when WebFetched, leading to missing or hallucinated values. **Fetch these `.md` URLs as-is with `WebFetch`** — no extension change is needed for machine extraction.

**When you surface a doc link to the user — swap the trailing `.md` to `.html`.** This applies to every citation in the Plan or Assessment artifact and every link in a chat answer. The `.html` page is what a human renders in a browser; the `.md` variant serves raw markdown that reads badly in a browser. So:

- URL as written in this skill (fetch form): `https://docs.confluent.io/cloud/current/clusters/cluster-types.md`
- Same URL surfaced to the user (citation form): the identical path with the extension changed to `.html`

If a `.md` URL returns 404 (the markdown variant doesn't exist for that page), fetch the `.html` form instead and report the truncation risk in any extracted value. Query-string variants like `?format=markdown` do NOT work — they return the same truncated content as `.html`.

**Source map:**

| Topic | Live Source | Fetch When |
|---|---|---|
| KCP CLI commands, flags, subcommand behavior | [KCP Command Reference](https://confluentinc.github.io/kcp/latest/command-reference/) (structured CLI reference, generated from Cobra definitions) + [github.com/confluentinc/kcp](https://github.com/confluentinc/kcp) (README, repo context). Hub-page note: meta-refresh redirect; WebFetch may return redirect message — surface to user or navigate to current version per the failure-handling protocol. | Before recommending any command or flag |
| KCP state file schema | [github.com/confluentinc/kcp](https://github.com/confluentinc/kcp) (internal/types/state.go) | When parsing a state file |
| Zero-Cut prerequisites, flow, auth support | [KCP zero-cut guide](https://confluentinc.github.io/kcp/latest/getting-started-with-zero-cut-migrations/) | Switchover; any Gateway or Zero-Cut question |
| Gateway auth-swap scenarios (source-auth × target-auth matrix) | [KCP Gateway Switchover hub](https://confluentinc.github.io/kcp/latest/gateway-switchover/) — 8 documented scenarios (none/mTLS/SCRAM source × SASL-PLAIN/OAuth/mTLS target). Hub-page note: meta-refresh redirect; navigate from hub to specific scenario pages. | Auth target derivation in Plan stage; any question about specific source → target auth migration through Gateway |
| Cluster types, eCKU caps, per-eCKU throughput, partition rates, REST throughput, SLA | [cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md) | Plan; whenever capacity, throughput, or partitioning matters |
| CC per-topic config defaults and limits (retention.ms, retention.bytes, segment.bytes, max.message.bytes, min.insync.replicas, compression.type, replication factor) | [topics/manage.md](https://docs.confluent.io/cloud/current/topics/manage.md) — fetch the `.md` variant per the fetch rule above. The `.html` config table truncates after `num.partitions` when WebFetched, dropping the `retention.*` and `segment.bytes` rows, so `.md` is required for these thresholds. cluster-types.html does NOT carry per-topic config defaults — do not route topic configs there. | Topic-Level Readiness bucketing in Assess; any per-topic config threshold comparison |
| Cluster Linking source requirements and compatibility | [cluster-linking index](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/index.md) (fetch the `index.md` variant; the migration-use-case floor is in Footnote [1] under "Supported cluster types") plus the "Cluster linking capabilities" sub-table on [cluster-types.md](https://docs.confluent.io/cloud/current/clusters/cluster-types.md) for which cluster types can act as CL source vs destination. **When fetching the CL source floor for this skill, extract the migration-use-case exception** (Kafka 2.4.0+ / CP 5.4.0+) for the product-version floor, **and separately extract the current `inter.broker.protocol` (IBP) floor** — a general non-CC-source requirement independent of the migration exception (fetch the IBP value live; do not cache it and do not assume it equals the product-version floor). Do not use the general Kafka 3.0+ product floor — this skill is MSK-only and always operates in the migration-exception path for the product version. | Any CL-related question or version compatibility check, and whenever the Plan references CL availability for a specific target cluster type |
| Cluster Linking direction config (`link.mode`); bidirectional excludes open-source Apache Kafka, so MSK is destination-initiated only | [cluster-links-cc.md](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/cluster-links-cc.md) | Any CL-direction question; confirming MSK supports only `link.mode=DESTINATION` |
| CC Cluster Linking source-auth support (supported source SASL mechanisms; IAM not among them) | [security-cloud.md](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/security-cloud.md) | Any IAM-source or CL-source-auth question |
| Egress PrivateLink Endpoint for the Cluster Linking replication pull (additive, environment-scoped, Enterprise; the documented substitute when PNI must reach back to a private source) | [aws-egress-privatelink-esku.md](https://docs.confluent.io/cloud/current/networking/aws-egress-privatelink-esku.md) | Whenever `target_context.cc_reaches_source: false` or `cc_egress_required: true` on a PNI cluster |
| Manual CL-based migration flow (big-bang fallback when Zero-Cut prereqs not met) | [migrate-cc.md](https://docs.confluent.io/cloud/current/multi-cloud/cluster-linking/migrate-cc.md) | Switchover; whenever the Plan emits a Big-bang + Manual CL cell or otherwise needs to describe the manual-CL cutover flow |
| CC authentication options and CL auth compatibility | [authenticate docs](https://docs.confluent.io/cloud/current/security/authenticate/overview.md) | Auth mapping for each source auth type |
| mTLS availability by cloud | [mTLS overview](https://docs.confluent.io/cloud/current/security/authenticate/workload-identities/identity-providers/mtls/overview.md) and CC release notes | mTLS + Azure/GCP questions |
| Broker-side schema ID validation availability | [broker-side-schema-validation.md](https://docs.confluent.io/cloud/current/sr/broker-side-schema-validation.md) | When source uses schema ID validation |
| Schema Linking support matrix | [docs.confluent.io](https://docs.confluent.io) Schema Registry / Schema Linking pages | Schema migration path selection |
| Schema Linking version floor and edition requirement | **HARDCODED (doc-cited)** — cached value: source SR must be on Confluent Platform 7.0 and later, Enterprise edition only (Community does not support Schema Linking even at 7.0+). Drift-check: fetch [schema-linking-cp.md](https://docs.confluent.io/platform/current/schema-registry/schema-linking-cp.md) Prerequisites section and verify the page still names "Confluent Platform 7.0" as the floor. On miss (version bumped or wording changed), fall back to a "verify live" prompt and tell the user the cached value may be stale. | Any Plan where source SR is Confluent SR — confirm version meets the floor and edition is Enterprise before recommending Schema Linking |
| Schema Linking exporter mechanism (one-directional source → destination push; source SR's outbound reachability to CC SR is the gating constraint) | [schema-linking.md](https://docs.confluent.io/cloud/current/sr/schema-linking.md) | B2 Schema Migration Path Selection cascade; whenever source SR is Confluent SR meeting SL floor and `target_context.source_sr_can_push_to_cc_sr` is being evaluated |
| Schema ID in Kafka Headers wire format (GA March 2026 — supports non-disruptive SR adoption on existing topics) | [Confluent Cloud serdes wire format docs](https://docs.confluent.io/cloud/current/sr/fundamentals/serdes-develop/index.md#wire-format) | When customer is considering adopt-SR-during-migration path for an existing schemaless source |
| Connector catalog (managed connector availability) | [connectors docs](https://docs.confluent.io/cloud/current/connectors/index.md) | Connector migration path decisions |
| CMU usage | [github.com/confluentinc/connect-migration-utility](https://github.com/confluentinc/connect-migration-utility) | Self-managed or MSK Connect connector migration |
| CC networking availability by cluster type | docs.confluent.io networking + cluster-types.html | Networking selection |
| Networking option availability by cloud + cluster type (PNI / PrivateLink / Peering / TGW) | [networking/overview.md](https://docs.confluent.io/cloud/current/networking/overview.md) | Networking selection; B6 PNI-default cascade |
| PNI specifics (cluster types, customer-side ENI setup, egress limitation, gateway limit of 2 per environment) | [aws-pni.md](https://docs.confluent.io/cloud/current/networking/aws-pni.md) | Whenever PNI is recommended or a PrivateLink exception case is being evaluated |
| Terraform provider resource schemas | [registry.terraform.io/providers/confluentinc/confluent](https://registry.terraform.io/providers/confluentinc/confluent) | Any Terraform generation or review |

Hardcoded values in this skill are labeled explicitly. The HARDCODED protocol in the hard-limits section applies: fetch the cited source each session, detect drift, prefer the live value if found.

## Reference File Index

One-line description of each reference file with when to read it:

- `references/assess.md` — Tool selection logic and red flag identification. Read when starting a migration.
- `references/plan.md` — Sizing, migration path selection for schemas and connectors, risk identification. Read after assessment.
- `references/kcp-commands.md` — When to use each KCP command and what to look for in the output. Read when user needs KCP guidance.
- `references/mcp-integration.md` — When to prefer MCP over CLI and how to interpret results. Read when MCP tools are available.
