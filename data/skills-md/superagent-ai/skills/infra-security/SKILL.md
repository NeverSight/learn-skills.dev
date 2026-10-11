---
name: infra-security
description: Audit Infrastructure-as-Code for security misconfigurations before it ships — Terraform (.tf/.tfvars/.hcl), CloudFormation/SAM (YAML/JSON), Kubernetes & Helm manifests, and Docker / Docker Compose. Reads the IaC offline and reports each misconfiguration at file:line with a severity (P0–P3) and a corrected snippet. A dependency-free scanner does the high-recall first pass; the model adds blast-radius and cross-resource judgment. No cloud credentials, no terraform apply, no pip install. Trigger when reviewing a Terraform plan before apply, auditing K8s/Helm manifests or a Dockerfile before deploy, checking CloudFormation for public S3 buckets or open security groups, doing a pre-deployment or compliance (SOC-2 / PCI-DSS / ISO-27001) security review, or when the user asks "audit this Terraform", "is this S3 bucket public?", "is this security group open to the internet?", "is this container running as root?", "what's the blast radius if this infra is wrong?", or "run an IaC security scan".
---

# Infrastructure-as-Code Security Scanner

This skill turns the model into a cloud security auditor. Read the IaC, find the dangerous misconfigurations, and report each one with a severity and a concrete fix. The analysis runs entirely against files on disk — no live cloud, no credentials, no `apply`.

The rules encode the consensus from the CIS Benchmarks, AWS Well-Architected, the Kubernetes Pod Security Standards, and the checks that tools like `tfsec`/`trivy`, `checkov`, `kube-score`, and `cfn-nag` ship — applied as a source read rather than another scanner to wire up.

## How it works: two stages

This skill is deliberately split, the same way `skill-security` is.

- **Stage 1 — the scanner (deterministic, mechanical).** `scripts/scan.py` does the fast, high-recall work: it walks the target, classifies each file by format, and runs line-oriented detectors for the misconfigurations that are unambiguous in text (`0.0.0.0/0` on port 22, `Action: "*"`, `privileged: true`, `runAsUser: 0`, a public-read S3 ACL). It is offline and **dependency-free** — pure Python standard library, no `pip install`, no `hcl2`, no `pyyaml`. It emits findings with `file:line` and a CI-friendly exit code.
- **Stage 2 — you (semantic, judgment).** The scanner cannot reason about *blast radius* or *compensating controls*. You can. You read the flagged resources alongside the rest of the IaC and decide what the scanner cannot: is that `0.0.0.0/0` actually reachable, or fronted by a WAF? Does that wildcard IAM policy attach to an internet-facing instance, turning a P1 into a P0? Is the "missing" encryption set by a default elsewhere in the module? Stage 1 finds candidates; you confirm impact, suppress false positives, and catch the judgment-only misconfigs (least-privilege gaps, a *missing* resource, cross-resource chains) that no regex can see.

The scanner is high-recall, not high-precision on purpose. Trust its `file:line` anchors; apply your own judgment to severity and validity.

## Mental model

Misconfiguration risk is **exposure × blast radius**, not a checklist tick.

- **Exposure** — can an attacker reach it? Internet-facing (`0.0.0.0/0`, public ACL, public subnet) is the top of the funnel. Internal-only, behind a private subnet or an authn proxy, is far lower.
- **Blast radius** — if reached, what falls? A wildcard IAM policy on a bastion is bad; the same policy on a role assumed by every Lambda is a takeover. Encryption-off on a scratch bucket is P3; on the bucket holding PII it is P1.

The same literal pattern can be P0 or P3 depending on these two axes — which is exactly why the scanner proposes and you decide. When you genuinely cannot tell the blast radius from the IaC alone, say so and rate conservatively with the assumption stated.

## Workflow

Three phases, in order.

### Phase 1 — Discover and ingest

Run the scanner over the target to get the candidate findings and a file inventory:

```bash
python3 scripts/scan.py <target-dir> --format markdown
```

It classifies files by extension and a content peek:

- **Terraform** — `.tf`, `.tfvars`, `.hcl`
- **CloudFormation / SAM** — `.yaml`/`.yml`/`.json` with `AWSTemplateFormatVersion` or a `Resources:` map of `AWS::*` types
- **Kubernetes / Helm** — `.yaml`/`.yml` with `apiVersion:` and `kind:` (multi-document streams split on `---`)
- **Docker** — `Dockerfile*`, `docker-compose*.yml`

Use `--format json` when you want to fold the findings into your own reasoning programmatically; `--severity P0,P1` to focus; the scanner exits `1` when any P0/P1 is present (so it gates a pipeline) and `0` otherwise.

### Phase 2 — Evaluate by category

Take the scanner's candidates and read the surrounding IaC. Walk the categories in `references/controls.md`, confirming impact and looking for the judgment-only gaps the scanner can't:

- **Identity & Access (IAM)** — wildcard `Action`/`Resource`, `*` principals in resource policies, over-broad roles attached to compute, missing least privilege, hardcoded credentials.
- **Network & Firewall** — `0.0.0.0/0` to sensitive ports (22, 3389, 3306, 5432, 6379, 27017, 9200), databases in public subnets, unnecessary open egress, missing WAF on internet-facing endpoints.
- **Storage & Data** — public S3 ACLs/policies, encryption-at-rest disabled (S3/EBS/RDS/DynamoDB), versioning/logging off on sensitive buckets, public snapshots.
- **Compute & Containers** — privileged containers, running as root, no `readOnlyRootFilesystem`, `hostNetwork`/`hostPID`/`hostIPC`, the Docker socket mounted in, missing resource limits.
- **Secrets & Encryption** — plaintext secrets in variables/env/ConfigMaps, missing TLS, wildcard KMS key policies.
- **Logging & Monitoring** — CloudTrail/Config/VPC Flow Logs disabled, missing log retention or encryption.
- **Supply chain** — images on `:latest` or from untrusted registries, Terraform modules from unpinned git/HTTP sources.

For each candidate, the deciding question is the mental model: *what is the exposure, and what is the blast radius?* That is what turns a raw pattern match into a rated finding.

### Phase 3 — Report and remediate

For every confirmed finding, produce:

- **Severity** (P0–P3, see `references/severity-rubric.md`)
- **Resource** and **`file:line`**
- **Current code** — the verbatim bad snippet
- **Fixed code** — the corrected snippet (patterns in `references/remediation-playbook.md`)
- **Rationale** — the exposure and blast radius, in one or two sentences
- **Compliance mapping** — SOC-2 / PCI-DSS / ISO-27001 control IDs where applicable
- **Effort** — Quick Fix / Moderate / Complex

Assemble these into the report in `references/report-template.md`. Default save path: `./infra-audit-report-<timestamp>.md`.

## Finding format

When reporting inline (not the full document), use this structure. Group by severity, P0 first.

```
[P0] network-ssh-world-open in infra/sg.tf:24
  aws_security_group.web allows 0.0.0.0/0 to port 22. Any host on the
  internet can reach SSH; combined with the public subnet on this SG,
  the blast radius is full shell access to the instance.

  Current:
    ingress {
      from_port   = 22
      to_port     = 22
      cidr_blocks = ["0.0.0.0/0"]
    }

  Fix (scope to the bastion / VPN CIDR, or use SSM Session Manager):
    ingress {
      from_port   = 22
      to_port     = 22
      cidr_blocks = [var.admin_cidr]   # e.g. ["10.0.0.0/16"]
    }
```

If the user pastes a snippet without a path, refer to "the resource" and use line numbers within the snippet. Always name the exposure and the blast radius — that pair is the justification for the severity.

## Severity scale

Summary only — full criteria, the deployment risk rating, and the effort scale are in `references/severity-rubric.md`.

- **P0 Critical** — exploitable now from the internet with high blast radius: unauthenticated data exposure or infrastructure takeover. Blocks deployment.
- **P1 High** — privilege escalation, lateral movement, or significant data exposure (often one precondition away from P0). Requires owner review before merge.
- **P2 Medium** — defense-in-depth gap; exploitable under specific conditions. Tracked as tech debt.
- **P3 Low** — best-practice deviation or compliance gap with no direct exploit.
- **Informational** — architectural recommendation or documentation note; no security impact on its own.

## When it looks clean

After walking all categories, if nothing fires:

1. Say so explicitly. "No findings against the standard control set."
2. Note what was **not** checked: live cloud state and drift (the deployed resource may differ from this IaC), evaluated IAM permissions (the scanner reads policy *documents*, not the effective access graph), runtime container behavior, secrets injected outside the IaC, and anything in modules/charts not present in the scanned tree.
3. Recommend the user confirm against the deployed environment — a clean IaC read does not prove the running infrastructure is safe.

## Safety and guardrails

1. **Read-only against files.** Never run `terraform apply`/`plan -out`, `kubectl apply`, `helm install`, `aws cloudformation deploy`, or `docker build/run` to "validate" a finding. This skill reasons about the IaC text, nothing more.
2. **No credentialed access.** Do not read `~/.aws/credentials`, `~/.kube/config`, environment secrets, or call any cloud API to confirm a finding.
3. **Deterministic rules first.** Severity decisions trace back to `references/controls.md`. Model judgment is for blast radius, false-positive suppression, and rationale — not for inventing rules.
4. **False-positive reduction.** Flag a finding only when the bad pattern is present **and** no compensating control is visible in the same scope (e.g. an explicit `aws_s3_bucket_public_access_block`, a default that sets encryption, a WAF in front of the open port). When a compensating control might exist outside the scanned tree, note the assumption.
5. **Redact secrets.** If the IaC contains live secrets, redact them in the report rather than echoing them.

## Trigger phrases

```
Audit this Terraform for security issues: <dir>
Review these Kubernetes manifests before deploy: <dir>
Check this CloudFormation for public S3 buckets: <file>
Is this security group open to the internet?
Is this container running as root / privileged?
Pre-deployment security review of this IaC: <dir>
What's the blast radius if this Terraform is wrong?
```

## Reference files

- `references/controls.md` — the control catalog: every rule with a stable id, category, severity, the bad and good pattern, and SOC-2/PCI-DSS/ISO-27001 mapping. Read it during Phase 2 to know what to check and how to rate it.
- `references/severity-rubric.md` — the P0–P3 + Informational definitions, how to choose between adjacent levels, the deployment risk rating, and the effort scale. Read it when scoring.
- `references/remediation-playbook.md` — bad→good fixes for the most common misconfigurations, each with a rationale and the looks-right-but-isn't pitfall. Read it when writing the fix, not just naming the gap.
- `references/report-template.md` — the structure of the output audit report. Read it when assembling the final document.

## What this skill won't do

- It won't run `terraform apply`, `kubectl apply`, or deploy anything, and it won't read cloud credentials. The audit is the model reading the IaC plus a stdlib scanner.
- It won't require `pip install`, Docker, or network access. The scanner is standard-library only; if a format needs a real parser to disambiguate, the model reads the file directly.
- It won't rate a finding on the literal pattern alone — severity comes from exposure and blast radius, so the same pattern can land anywhere from P0 to P3.
- It won't replace a runtime posture tool (CSPM) or a live IAM access analyzer. It checks the IaC before it ships; it cannot see drift or the effective permission graph of the deployed account.
- It won't claim "secure" — only "no findings against this control set, and here is what a file read cannot cover."
