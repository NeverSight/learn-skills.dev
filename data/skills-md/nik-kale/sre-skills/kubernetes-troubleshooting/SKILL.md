---
name: kubernetes-troubleshooting
description: Systematic debugging workflows for Kubernetes issues including pod failures, resource problems, and networking. Use when debugging CrashLoopBackOff, OOMKilled, ImagePullBackOff, pod not starting, k8s issues, or any Kubernetes troubleshooting.
---

# Kubernetes Troubleshooting

Systematic approach to debugging Kubernetes issues.

## When to Use This Skill

- Pod stuck in CrashLoopBackOff
- OOMKilled errors
- ImagePullBackOff failures
- Pod not starting or scheduling
- Service connectivity issues
- Resource constraint problems

## Quick Diagnostic Commands

Start with these commands to understand the current state:

```bash
# Cluster overview
kubectl get nodes
kubectl get pods -A | grep -v Running

# Specific namespace
kubectl get pods -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Resource usage
kubectl top nodes
kubectl top pods -n <namespace>
```

## Pod Debugging Workflow

### Step 1: Check Pod Status

```bash
kubectl get pod <pod-name> -n <namespace> -o wide
kubectl describe pod <pod-name> -n <namespace>
```

Look for:

- **Status**: What state is the pod in?
- **Conditions**: Ready, ContainersReady, PodScheduled
- **Events**: Recent events at the bottom of describe output

### Step 2: Identify the Problem Category

| Symptom               | Likely Cause         | Go To Section                           |
| --------------------- | -------------------- | --------------------------------------- |
| Pending               | Scheduling issue     | [Scheduling Issues](#scheduling-issues) |
| CrashLoopBackOff      | Application crash    | [CrashLoopBackOff](#crashloopbackoff)   |
| ImagePullBackOff      | Image/registry issue | [Image Pull Issues](#image-pull-issues) |
| OOMKilled             | Memory exhaustion    | [OOMKilled](#oomkilled)                 |
| Running but not Ready | Health check failing | [Readiness Issues](#readiness-issues)   |
| Error                 | Container error      | [Container Errors](#container-errors)   |

## Common Issues

### Scheduling Issues

Pod stuck in **Pending** state.

**Diagnostic**:

```bash
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Events
```

**Common Causes**:

| Event Message                   | Cause                | Fix                              |
| ------------------------------- | -------------------- | -------------------------------- |
| Insufficient cpu/memory         | Not enough resources | Add nodes or reduce requests     |
| node(s) had taints              | Node taints          | Add tolerations or remove taints |
| no nodes available              | No matching nodes    | Check node selector/affinity     |
| persistentvolumeclaim not found | PVC missing          | Create the PVC                   |

**Fix Resource Issues**:

```bash
# Check resource requests vs available
kubectl describe nodes | grep -A 5 "Allocated resources"

# Check pending pod requests
kubectl get pod <pod> -o yaml | grep -A 10 resources
```

---

### CrashLoopBackOff

Container keeps crashing and restarting.

**Diagnostic**:

```bash
# Check container logs (current)
kubectl logs <pod-name> -n <namespace>

# Check previous container logs
kubectl logs <pod-name> -n <namespace> --previous

# Check exit code
kubectl describe pod <pod-name> -n <namespace> | grep -A 3 "Last State"
```

**Common Exit Codes**:

| Exit Code | Meaning           | Common Cause                                        |
| --------- | ----------------- | --------------------------------------------------- |
| 0         | Success           | Process completed (might be wrong for long-running) |
| 1         | Application error | Check application logs                              |
| 137       | SIGKILL (OOM)     | Memory limit exceeded                               |
| 139       | SIGSEGV           | Segmentation fault                                  |
| 143       | SIGTERM           | Graceful termination                                |

**Common Fixes**:

- Check application logs for startup errors
- Verify environment variables and secrets
- Check if dependencies are available
- Verify resource limits aren't too restrictive

---

### Image Pull Issues

**ImagePullBackOff** or **ErrImagePull**.

**Diagnostic**:

```bash
kubectl describe pod <pod-name> -n <namespace> | grep -A 5 Events
```

**Common Causes**:

| Error                     | Cause                | Fix                    |
| ------------------------- | -------------------- | ---------------------- |
| repository does not exist | Wrong image name     | Fix image name/tag     |
| unauthorized              | Auth failure         | Check imagePullSecrets |
| manifest unknown          | Tag doesn't exist    | Verify tag exists      |
| connection refused        | Registry unreachable | Check network/firewall |

**Fix Registry Auth**:

```bash
# Create image pull secret
kubectl create secret docker-registry regcred \
  --docker-server=<registry> \
  --docker-username=<user> \
  --docker-password=<password> \
  -n <namespace>

# Reference in pod spec
spec:
  imagePullSecrets:
  - name: regcred
```

---

### OOMKilled

Container killed due to memory exhaustion.

**Diagnostic**:

```bash
kubectl describe pod <pod-name> -n <namespace> | grep -i oom
kubectl get pod <pod-name> -n <namespace> -o yaml | grep -A 5 lastState
```

**Fix Options**:

1. **Increase memory limit** (if available):

```yaml
resources:
  limits:
    memory: '512Mi' # Increase this
  requests:
    memory: '256Mi'
```

2. **Profile memory usage**:

```bash
kubectl top pod <pod-name> -n <namespace> --containers
```

3. **Check for memory leaks** in application code

---

### Readiness Issues

Pod is Running but not Ready.

**Diagnostic**:

```bash
# Check readiness probe
kubectl describe pod <pod-name> -n <namespace> | grep -A 10 Readiness

# Check probe endpoint manually
kubectl exec <pod-name> -n <namespace> -- wget -qO- localhost:<port>/health
```

**Common Causes**:

- Application not listening on expected port
- Readiness endpoint returning non-200
- Probe timeout too short
- Dependencies not available

**Fix Readiness Probe**:

```yaml
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 10 # Give app time to start
  periodSeconds: 5
  timeoutSeconds: 3 # Increase if needed
  failureThreshold: 3
```

---

### Container Errors

**Diagnostic**:

```bash
# Get detailed container status
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.status.containerStatuses[*]}'

# Check init containers
kubectl logs <pod-name> -n <namespace> -c <init-container-name>
```

---

## Networking Troubleshooting

### Service Not Reachable

```bash
# Check service endpoints
kubectl get endpoints <service-name> -n <namespace>

# Check service selector matches pod labels
kubectl get svc <service-name> -n <namespace> -o yaml | grep selector -A 5
kubectl get pods -n <namespace> --show-labels

# Test connectivity from another pod
kubectl run debug --rm -it --image=busybox -- wget -qO- <service>:<port>
```

### DNS Issues

```bash
# Check DNS resolution from pod
kubectl exec <pod> -n <namespace> -- nslookup <service-name>
kubectl exec <pod> -n <namespace> -- nslookup <service-name>.<namespace>.svc.cluster.local

# Check CoreDNS is running
kubectl get pods -n kube-system -l k8s-app=kube-dns
```

---

## Resource Analysis

### Node Pressure

```bash
# Check node conditions
kubectl describe nodes | grep -A 5 Conditions

# Check node resource usage
kubectl top nodes

# Find resource-heavy pods
kubectl top pods -A --sort-by=memory | head -20
```

### PVC Issues

```bash
# Check PVC status
kubectl get pvc -n <namespace>

# Check PV status
kubectl get pv

# Describe for events
kubectl describe pvc <pvc-name> -n <namespace>
```

---

## Quick Reference Commands

```bash
# Pod debugging
kubectl logs <pod> -n <ns>                    # Current logs
kubectl logs <pod> -n <ns> --previous         # Previous container logs
kubectl logs <pod> -n <ns> -c <container>     # Specific container
kubectl logs <pod> -n <ns> --tail=100 -f      # Follow logs

# Interactive debugging
kubectl exec -it <pod> -n <ns> -- /bin/sh     # Shell into container
kubectl exec <pod> -n <ns> -- env             # Check environment
kubectl exec <pod> -n <ns> -- cat /etc/hosts  # Check DNS

# Resource inspection
kubectl get pod <pod> -n <ns> -o yaml         # Full pod spec
kubectl describe pod <pod> -n <ns>            # Events and status
kubectl get events -n <ns> --sort-by='.lastTimestamp'

# Cluster-wide
kubectl get pods -A | grep -v Running         # Non-running pods
kubectl top pods -A --sort-by=cpu             # CPU usage
kubectl top pods -A --sort-by=memory          # Memory usage
```

## Additional Resources

- [Error Message Decoder](references/error-decoder.md)
- [kubectl Cheat Sheet](references/kubectl-cheatsheet.md)
