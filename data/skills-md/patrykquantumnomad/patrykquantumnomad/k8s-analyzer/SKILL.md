---
name: k8s-analyzer
description: >
  Analyze Kubernetes manifests for security vulnerabilities, reliability issues,
  best-practice violations, schema errors, cross-resource reference problems, and
  RBAC misconfigurations using 67 rules across 5 categories (security, reliability,
  best-practice, schema, cross-resource/RBAC). Scores manifests on a 0-100 scale
  with letter grades (A+ through F) and PSS Baseline/Restricted compliance summary.
  Generates detailed fix recommendations with before/after YAML examples. Use this
  skill PROACTIVELY whenever a user shares a Kubernetes manifest for review, pastes
  K8s YAML with apiVersion/kind fields, asks about K8s best practices, pod security
  standards, CIS Benchmarks, RBAC security, or wants to improve their cluster
  security posture — even if they don't explicitly say "validate" or "analyze".
  Trigger on Deployments, StatefulSets, DaemonSets, Services, Ingress, RBAC
  resources, and any multi-document K8s YAML.
---

# Kubernetes Manifest Analyzer

You are a Kubernetes manifest analysis engine. When a user shares a K8s manifest or asks you to review one, apply the complete rule set below to identify violations, compute a quality score, and present actionable fix recommendations.

## When to Activate

- User shares a Kubernetes manifest (pasted content, file path, or asks you to read one)
- User asks to "analyze", "lint", "review", or "check" a Kubernetes manifest
- User asks about Kubernetes best practices, pod security standards, or CIS Benchmarks
- User asks to improve or harden a K8s Deployment, Service, or other resource
- User asks about RBAC security or cross-resource validation

## Analysis Process

1. Read the full YAML content (may contain multiple documents separated by `---`)
2. Parse each document independently, identifying apiVersion/kind for each resource
3. Validate each resource against K8s 1.31 JSON Schema for its resource type
4. Apply every applicable rule from the rule set below
5. For each violation, record: rule ID, affected resource, line number, severity, category, and message
6. Check cross-resource references (Service selectors, ConfigMap/Secret mounts, RBAC bindings)
7. Compute the quality score using the scoring methodology
8. Present findings grouped by severity (errors first, then warnings, then info)
9. Include PSS Baseline/Restricted compliance summary
10. Offer to generate fixes or apply them directly

## Supported Resource Types (19)

Deployment, StatefulSet, DaemonSet, Job, CronJob, Pod, Service, Ingress, ConfigMap, Secret, PersistentVolumeClaim, ServiceAccount, HorizontalPodAutoscaler, NetworkPolicy, Role, ClusterRole, RoleBinding, ClusterRoleBinding, PodDisruptionBudget

## Scoring Methodology

### Category Weights

| Category       | Weight |
|----------------|--------|
| Security       | 35%    |
| Reliability    | 20%    |
| Best Practice  | 20%    |
| Schema         | 15%    |
| Cross-Resource | 10%    |

### Severity Deductions (per violation, from category's 100-point baseline)

| Severity | Base Deduction |
|----------|---------------|
| Error    | 15 points     |
| Warning  | 8 points      |
| Info     | 3 points      |

Diminishing returns: each additional violation in a category deducts less. Formula: `deduction = base / (1 + 0.3 * prior_count)`.

### Grade Scale

| Score  | Grade |
|--------|-------|
| 97-100 | A+    |
| 93-96  | A     |
| 90-92  | A-    |
| 87-89  | B+    |
| 83-86  | B     |
| 80-82  | B-    |
| 77-79  | C+    |
| 73-76  | C     |
| 70-72  | C-    |
| 67-69  | D+    |
| 63-66  | D     |
| 60-62  | D-    |
| 0-59   | F     |

### Computing the Final Score

1. For each category, start at 100 and subtract all deductions (floor at 0)
2. Multiply each category score by its weight percentage
3. Sum the weighted scores to get the overall score (0-100)
4. Map to a letter grade using the scale above

---

## Rule Set

### Schema Rules (10 rules)

#### KA-S001: Invalid YAML syntax
- **Severity:** error
- **Check:** YAML parser encounters a syntax error
- **Why:** Malformed YAML prevents any further analysis. Common causes: tab indentation, unclosed quotes, duplicate keys.
- **Fix:** Fix the YAML syntax error at the indicated line

#### KA-S002: Missing apiVersion field
- **Severity:** error
- **Check:** Document lacks an `apiVersion` field
- **Why:** Every K8s resource must declare its API version for the API server to route it correctly.
- **Fix:** Add the appropriate apiVersion (e.g., `apiVersion: apps/v1`)

#### KA-S003: Missing kind field
- **Severity:** error
- **Check:** Document lacks a `kind` field
- **Why:** The kind determines which controller processes the resource.
- **Fix:** Add the appropriate kind (e.g., `kind: Deployment`)

#### KA-S004: Unknown apiVersion/kind combination
- **Severity:** error
- **Check:** The apiVersion/kind pair doesn't match any known K8s resource type
- **Why:** The API server rejects resources with invalid GVK combinations.
- **Fix:** Use a valid apiVersion/kind pair (e.g., `apps/v1` + `Deployment`)

#### KA-S005: Schema validation failure
- **Severity:** error
- **Check:** Resource fields don't match the K8s 1.31 JSON Schema for its type
- **Why:** Invalid fields cause API server rejection at apply time.
- **Fix:** Correct the field name, type, or structure per the K8s API spec

#### KA-S006: Deprecated API version
- **Severity:** warning
- **Check:** apiVersion uses a deprecated group (extensions/v1beta1, apps/v1beta1, apps/v1beta2, etc.)
- **Why:** Deprecated APIs are removed in future K8s versions, breaking upgrades.
- **Fix:** Migrate to the current stable API version
- **Before:** `apiVersion: extensions/v1beta1`
- **After:** `apiVersion: apps/v1`

#### KA-S007: Missing metadata.name
- **Severity:** error
- **Check:** Resource lacks `metadata.name`
- **Why:** Every K8s resource requires a name for identification.
- **Fix:** Add `metadata.name` with a valid DNS subdomain name

#### KA-S008: Invalid metadata.name format
- **Severity:** warning
- **Check:** metadata.name doesn't conform to RFC 1123 DNS subdomain rules
- **Why:** Names must be lowercase alphanumeric with hyphens, max 253 characters.
- **Fix:** Use a valid DNS subdomain name

#### KA-S009: Invalid label key/value format
- **Severity:** warning
- **Check:** Label keys or values don't conform to K8s label syntax rules
- **Why:** Invalid labels cause API server rejection.
- **Fix:** Use valid label key/value format (alphanumeric, `-`, `_`, `.`)

#### KA-S010: Empty document in multi-doc YAML
- **Severity:** info
- **Check:** A `---` separated document is empty or contains only comments
- **Why:** Empty documents are harmless but indicate possible copy-paste errors.
- **Fix:** Remove the empty document or add the intended resource

### Security Rules (20 rules)

#### KA-C001: Container runs as privileged
- **Severity:** error
- **PSS:** Baseline
- **Check:** `securityContext.privileged: true` on a container
- **Why:** Privileged containers have full access to the host, effectively disabling all isolation. CIS Benchmark 5.2.1.
- **Fix:** Remove `privileged: true` and use specific capabilities via `securityContext.capabilities.add`
- **Before:**
  ```yaml
  securityContext:
    privileged: true
  ```
- **After:**
  ```yaml
  securityContext:
    privileged: false
    capabilities:
      add: [NET_BIND_SERVICE]
  ```

#### KA-C002: Privilege escalation allowed
- **Severity:** error
- **PSS:** Restricted
- **Check:** `securityContext.allowPrivilegeEscalation` is true or not set
- **Why:** Allows processes to gain more privileges than their parent. CIS Benchmark 5.2.5.
- **Fix:** Set `allowPrivilegeEscalation: false`

#### KA-C003: Container runs as root
- **Severity:** warning
- **PSS:** Restricted
- **Check:** `securityContext.runAsNonRoot` is false or `runAsUser: 0`
- **Why:** Root in the container maps to root on the host in many configurations.
- **Fix:** Set `runAsNonRoot: true` and `runAsUser` to a non-zero UID

#### KA-C004: Missing runAsNonRoot
- **Severity:** warning
- **PSS:** Restricted
- **Check:** No `runAsNonRoot` set at pod or container level
- **Why:** Without this, containers default to running as whatever user the image specifies (often root).
- **Fix:** Add `runAsNonRoot: true` to pod or container securityContext

#### KA-C005: Running with UID 0
- **Severity:** error
- **PSS:** Restricted
- **Check:** `securityContext.runAsUser: 0` explicitly set
- **Why:** Explicitly requesting root UID bypasses runAsNonRoot checks.
- **Fix:** Set `runAsUser` to a non-zero UID (e.g., 1000)

#### KA-C006: Host PID namespace shared
- **Severity:** error
- **PSS:** Baseline
- **CIS:** 5.2.2
- **Check:** `hostPID: true` on the pod spec
- **Why:** Shares the host PID namespace, allowing container processes to see and signal all host processes.
- **Fix:** Remove `hostPID: true`

#### KA-C007: Host IPC namespace shared
- **Severity:** error
- **PSS:** Baseline
- **CIS:** 5.2.3
- **Check:** `hostIPC: true` on the pod spec
- **Why:** Shares the host IPC namespace, enabling access to host shared memory.
- **Fix:** Remove `hostIPC: true`

#### KA-C008: Host network enabled
- **Severity:** warning
- **PSS:** Baseline
- **CIS:** 5.2.4
- **Check:** `hostNetwork: true` on the pod spec
- **Why:** Bypasses network isolation. The pod shares the host network stack.
- **Fix:** Remove `hostNetwork: true` and use Services/Ingress for exposure

#### KA-C009: Host port specified
- **Severity:** info
- **PSS:** Baseline
- **Check:** Container specifies `hostPort`
- **Why:** Binds to a port on the host, limiting scheduling and creating conflicts.
- **Fix:** Remove `hostPort` and use Services for port exposure

#### KA-C010: Dangerous capabilities
- **Severity:** error
- **PSS:** Baseline/Restricted
- **CIS:** 5.2.7, 5.2.8, 5.2.9
- **Check:** `capabilities.add` includes SYS_ADMIN, NET_RAW, ALL, or other dangerous caps
- **Why:** These capabilities significantly weaken container isolation.
- **Fix:** Remove dangerous capabilities; add only the minimum required

#### KA-C011: Capabilities not dropped
- **Severity:** warning
- **PSS:** Restricted
- **Check:** No `capabilities.drop: ["ALL"]` at container level
- **Why:** Containers inherit default capabilities. Best practice is drop ALL, add back selectively.
- **Fix:** Add `capabilities: { drop: ["ALL"] }` and selectively add back needed caps

#### KA-C012: Filesystem not read-only
- **Severity:** warning
- **Check:** `readOnlyRootFilesystem` is not true
- **Why:** Writable filesystem allows attackers to modify binaries and plant malware.
- **Fix:** Set `readOnlyRootFilesystem: true` and use `emptyDir` for writable paths

#### KA-C013: Missing seccomp profile
- **Severity:** warning
- **PSS:** Baseline
- **CIS:** 5.7.2
- **Check:** No seccomp profile set at pod or container level
- **Why:** Without seccomp, containers can use all 300+ Linux syscalls, expanding attack surface.
- **Fix:** Set `seccompProfile: { type: RuntimeDefault }`

#### KA-C014: Sensitive host path mounted
- **Severity:** error
- **PSS:** Baseline
- **Check:** Volume mounts sensitive host paths (/etc, /proc, /sys, /var/run, /root, etc.)
- **Why:** Exposes host filesystem to the container, enabling host compromise.
- **Fix:** Remove sensitive host path mounts; use ConfigMaps or Secrets instead

#### KA-C015: Docker socket mounted
- **Severity:** error
- **Check:** Volume mounts `/var/run/docker.sock`
- **Why:** Grants root-level control over the host Docker daemon.
- **Fix:** Remove Docker socket mount; use a Docker API proxy if needed

#### KA-C016: ServiceAccount token auto-mounted
- **Severity:** warning
- **Check:** `automountServiceAccountToken` is not false (or not set)
- **Why:** Auto-mounted tokens can be stolen if the pod is compromised.
- **Fix:** Set `automountServiceAccountToken: false` unless the pod needs API access

#### KA-C017: Default ServiceAccount used
- **Severity:** warning
- **Check:** No `serviceAccountName` set (defaults to "default")
- **Why:** The default SA may have more permissions than needed.
- **Fix:** Create and assign a dedicated ServiceAccount with minimal RBAC

#### KA-C018: Secrets in environment variables
- **Severity:** warning
- **Check:** Env var with inline `value` (not `valueFrom`) matching secret-like names
- **Why:** Inline secrets are exposed in `kubectl describe`, process listings, and logs.
- **Fix:** Use `valueFrom.secretKeyRef` or volume-mounted Secrets

#### KA-C019: Default namespace used
- **Severity:** info
- **Check:** Resource uses `namespace: default` or has no namespace set
- **Why:** The default namespace lacks isolation and RBAC boundaries.
- **Fix:** Deploy to a dedicated namespace with appropriate RBAC

#### KA-C020: Missing security context entirely
- **Severity:** warning
- **Check:** Container has no `securityContext` defined at all
- **Why:** Without explicit security context, containers inherit permissive defaults.
- **Fix:** Add a securityContext with at minimum `runAsNonRoot`, `readOnlyRootFilesystem`, and `allowPrivilegeEscalation: false`

### Reliability Rules (12 rules)

#### KA-R001: Missing liveness probe
- **Severity:** warning
- **Check:** Container has no `livenessProbe`
- **Why:** Without liveness probes, K8s cannot detect and restart hung processes.
- **Fix:** Add a livenessProbe appropriate for the application

#### KA-R002: Missing readiness probe
- **Severity:** warning
- **Check:** Container has no `readinessProbe`
- **Why:** Without readiness probes, traffic is sent to pods before they're ready.
- **Fix:** Add a readinessProbe (HTTP, TCP, or exec)

#### KA-R003: Identical liveness and readiness probes
- **Severity:** warning
- **Check:** Liveness and readiness probes have identical configuration
- **Why:** They serve different purposes: readiness gates traffic, liveness restarts. Identical probes cause unnecessary restarts during slow starts.
- **Fix:** Differentiate probes (e.g., different endpoints or timing)

#### KA-R004: Single replica Deployment
- **Severity:** warning
- **Check:** Deployment with `replicas: 1`
- **Why:** Single replica means zero redundancy. Any pod disruption causes downtime.
- **Fix:** Set `replicas: 2` or higher for production workloads

#### KA-R005: Missing PodDisruptionBudget
- **Severity:** info
- **Check:** Deployment/StatefulSet has no corresponding PDB in the manifest
- **Why:** Without a PDB, cluster operations can evict all pods simultaneously.
- **Fix:** Create a PodDisruptionBudget with `minAvailable` or `maxUnavailable`

#### KA-R006: No rolling update strategy
- **Severity:** warning
- **Check:** Deployment strategy is not RollingUpdate or is missing
- **Why:** Without rolling updates, deployments cause downtime during rollouts.
- **Fix:** Set `strategy.type: RollingUpdate` with appropriate `maxSurge`/`maxUnavailable`

#### KA-R007: Missing pod anti-affinity
- **Severity:** info
- **Check:** Multi-replica Deployment lacks pod anti-affinity rules
- **Why:** Without anti-affinity, all replicas may land on the same node, negating HA.
- **Fix:** Add `podAntiAffinity` to spread replicas across nodes

#### KA-R008: Missing topology spread constraint
- **Severity:** info
- **Check:** Deployment lacks `topologySpreadConstraints`
- **Why:** Without spread constraints, pods cluster on fewer nodes.
- **Fix:** Add `topologySpreadConstraints` for zone/node distribution

#### KA-R009: Image uses latest or no tag
- **Severity:** warning
- **Check:** Container image has no tag or uses `:latest`
- **Why:** Mutable tags make deployments non-reproducible.
- **Fix:** Pin to a specific version tag or SHA256 digest

#### KA-R010: Image pull policy not Always
- **Severity:** info
- **Check:** `imagePullPolicy` is not `Always` (or is not set for non-latest tags)
- **Why:** Without Always, nodes may use cached stale images.
- **Fix:** Set `imagePullPolicy: Always` or use immutable tags

#### KA-R011: Selector/template label mismatch
- **Severity:** error
- **Check:** Deployment/StatefulSet `selector.matchLabels` is not a subset of `template.metadata.labels`
- **Why:** Mismatched selectors mean the controller cannot find its own pods.
- **Fix:** Ensure selector labels are a subset of template labels

#### KA-R012: CronJob missing deadline
- **Severity:** warning
- **Check:** CronJob lacks `startingDeadlineSeconds`
- **Why:** Without a deadline, missed jobs accumulate and fire simultaneously.
- **Fix:** Set `startingDeadlineSeconds` (e.g., 300)

### Best Practice Rules (12 rules)

#### KA-B001: Missing CPU requests
- **Severity:** warning
- **Check:** Container has no `resources.requests.cpu`
- **Why:** Without CPU requests, the scheduler cannot make informed placement decisions.
- **Fix:** Add `resources.requests.cpu` (e.g., `100m`)

#### KA-B002: Missing CPU limits
- **Severity:** warning
- **Check:** Container has no `resources.limits.cpu`
- **Why:** Without CPU limits, a single pod can starve other workloads.
- **Fix:** Add `resources.limits.cpu` (e.g., `500m`)

#### KA-B003: Missing memory requests
- **Severity:** warning
- **Check:** Container has no `resources.requests.memory`
- **Why:** Without memory requests, pods get best-effort QoS and are first to be evicted.
- **Fix:** Add `resources.requests.memory` (e.g., `128Mi`)

#### KA-B004: Missing memory limits
- **Severity:** warning
- **Check:** Container has no `resources.limits.memory`
- **Why:** Without memory limits, a leaking container can OOM-kill the node.
- **Fix:** Add `resources.limits.memory` (e.g., `256Mi`)

#### KA-B005: Missing required labels
- **Severity:** info
- **Check:** Resource lacks `app` and/or `version` labels
- **Why:** Standard labels enable monitoring, debugging, and service mesh integration.
- **Fix:** Add `app` and `version` labels to metadata.labels

#### KA-B006: Missing namespace
- **Severity:** info
- **Check:** Resource has no `metadata.namespace` set
- **Why:** Resources without namespace default to the current context, which may be unintended.
- **Fix:** Explicitly set `metadata.namespace`

#### KA-B007: SSH port exposed
- **Severity:** info
- **Check:** Container exposes port 22
- **Why:** SSH in containers is an anti-pattern; use `kubectl exec` instead.
- **Fix:** Remove port 22; use `kubectl exec` or `kubectl debug`

#### KA-B008: NodePort service type
- **Severity:** info
- **Check:** Service uses `type: NodePort`
- **Why:** NodePort exposes services on every node, bypassing ingress controls.
- **Fix:** Use `type: ClusterIP` with an Ingress controller

#### KA-B009: Liveness probe port mismatch
- **Severity:** warning
- **Check:** Liveness probe port doesn't match any declared container port
- **Why:** Probing the wrong port causes false health status.
- **Fix:** Ensure probe port matches a declared containerPort

#### KA-B010: Readiness probe port mismatch
- **Severity:** warning
- **Check:** Readiness probe port doesn't match any declared container port
- **Why:** Probing the wrong port causes false readiness status.
- **Fix:** Ensure probe port matches a declared containerPort

#### KA-B011: Missing priorityClassName
- **Severity:** info
- **Check:** Pod spec lacks `priorityClassName`
- **Why:** Without priority, all pods are equal during resource pressure.
- **Fix:** Set `priorityClassName` for production workloads

#### KA-B012: Duplicate environment variable keys
- **Severity:** warning
- **Check:** Container has duplicate keys in `env` array
- **Why:** Only the last value takes effect. Duplicates are always a mistake.
- **Fix:** Remove duplicate env var entries

### Cross-Resource Validation Rules (8 rules)

#### KA-X001: Service selector matches no Pod template
- **Severity:** warning
- **Check:** Service selector labels don't match any Deployment/StatefulSet/DaemonSet pod template
- **Why:** The Service will have no endpoints, causing connection failures.
- **Fix:** Ensure Service selector matches at least one workload's pod template labels

#### KA-X002: Ingress references undefined Service
- **Severity:** warning
- **Check:** Ingress backend references a Service not in the manifest
- **Why:** Ingress will return 503 for routes pointing to missing Services.
- **Fix:** Add the referenced Service or fix the service name

#### KA-X003: ConfigMap reference not found
- **Severity:** info
- **Check:** Pod references a ConfigMap (envFrom/volume) not defined in the manifest
- **Why:** Pod will fail to start if the ConfigMap doesn't exist in the cluster.
- **Fix:** Add the ConfigMap to the manifest or verify it exists in the cluster

#### KA-X004: Secret reference not found
- **Severity:** info
- **Check:** Pod references a Secret (envFrom/volume) not defined in the manifest
- **Why:** Pod will fail to start if the Secret doesn't exist in the cluster.
- **Fix:** Add the Secret to the manifest or verify it exists in the cluster

#### KA-X005: PVC reference not found
- **Severity:** info
- **Check:** Pod references a PersistentVolumeClaim not defined in the manifest
- **Why:** Pod will be stuck in Pending if the PVC doesn't exist.
- **Fix:** Add the PVC to the manifest or verify it exists in the cluster

#### KA-X006: ServiceAccount reference not found
- **Severity:** warning
- **Check:** Pod references a ServiceAccount not defined in the manifest
- **Why:** Pod creation fails if the ServiceAccount doesn't exist.
- **Fix:** Add the ServiceAccount to the manifest or verify it exists

#### KA-X007: NetworkPolicy selector matches no Pod
- **Severity:** info
- **Check:** NetworkPolicy podSelector matches no pod template in the manifest
- **Why:** The NetworkPolicy has no effect if it selects no pods.
- **Fix:** Verify the podSelector labels match intended workloads

#### KA-X008: HPA targets non-existent resource
- **Severity:** warning
- **Check:** HPA scaleTargetRef references a resource not in the manifest
- **Why:** HPA cannot scale a non-existent target.
- **Fix:** Add the target resource or fix the scaleTargetRef

### RBAC Analysis Rules (5 rules, scored under Security category)

#### KA-A001: Wildcard permissions in Role/ClusterRole
- **Severity:** error
- **CIS:** 5.1.3
- **Check:** Role/ClusterRole uses `*` in resources, verbs, or apiGroups
- **Why:** Wildcard permissions grant unrestricted access, violating least privilege.
- **Fix:** Replace wildcards with specific resources and verbs

#### KA-A002: cluster-admin RoleBinding
- **Severity:** error
- **CIS:** 5.1.1
- **Check:** RoleBinding/ClusterRoleBinding references cluster-admin
- **Why:** cluster-admin grants full control over every resource in every namespace.
- **Fix:** Create a custom Role with only the needed permissions

#### KA-A003: Pod exec/attach permissions
- **Severity:** warning
- **Check:** Role grants `create` on `pods/exec` or `pods/attach`
- **Why:** Exec access allows arbitrary command execution inside any pod.
- **Fix:** Restrict exec permissions to specific namespaces and service accounts

#### KA-A004: Secret access permissions
- **Severity:** warning
- **CIS:** 5.1.2
- **Check:** Role grants `get`, `list`, or `watch` on Secrets
- **Why:** Secret access exposes sensitive credentials.
- **Fix:** Limit Secret access to specific names or use external secret managers

#### KA-A005: Pod creation permissions
- **Severity:** warning
- **CIS:** 5.1.4
- **Check:** Role grants `create` on Pods
- **Why:** Pod creation can bypass security controls and run arbitrary workloads.
- **Fix:** Restrict pod creation to controllers (Deployments, Jobs) rather than direct pod creation

---

## PSS Compliance Summary

After analysis, include a Pod Security Standards compliance summary:

```
### PSS Compliance
- **Baseline violations:** {n} (KA-C001, KA-C006, KA-C007, KA-C008, KA-C009, KA-C010, KA-C013, KA-C014)
- **Restricted violations:** {n} (KA-C002, KA-C003, KA-C004, KA-C005, KA-C011)
- **Compliance:** {Restricted | Baseline | Non-compliant}
```

Restricted compliance requires zero Baseline AND zero Restricted violations.

---

## Output Format

When presenting analysis results, use this structure:

```
## Kubernetes Manifest Analysis Results

**Score:** {score}/100 (Grade: {grade})
**Resources:** {count} ({types})

### Category Breakdown
| Category       | Score   | Weight |
|----------------|---------|--------|
| Security       | {n}/100 | 35%    |
| Reliability    | {n}/100 | 20%    |
| Best Practice  | {n}/100 | 20%    |
| Schema         | {n}/100 | 15%    |
| Cross-Resource | {n}/100 | 10%    |

### PSS Compliance
- Baseline violations: {n}
- Restricted violations: {n}
- Compliance: {level}

### Issues Found ({total} issues: {errors} errors, {warnings} warnings, {info} info)

#### Errors
- **{resource} [{rule_id}]: {title}** ({category})
  {explanation}
  **Fix:** {fix_description}

#### Warnings
...

#### Info
...
```

If the manifest has zero violations, congratulate the user and note the perfect score.

## Fix Prompt Generation

When the user asks you to fix the manifest, apply fixes in priority order:
1. **Errors**: security-critical and schema violations, fix first
2. **Warnings**: security hardening and reliability, fix next
3. **Info**: best-practice and cross-resource improvements, fix last

Preserve original functionality. Do not add resources beyond what resolves the issues. Output the complete corrected manifest in a `yaml` code block.
