---
name: k8s-query
description: Query Kubernetes resources (pods, deployments, services, events). Use when checking cluster state and resource status.
---

# Query Kubernetes Resources

Check status of Kubernetes pods, deployments, services, and events.

## When to Use

- Checking if pods are running
- Viewing pod/deployment status
- Investigating pod failures or restarts
- Checking resource events and logs

## Pre-flight Checks

### Authentication and Context
```bash
# Check kubectl context
kubectl config current-context || {
  echo "No kubectl context. Run: kubectl config use-context <context>"
  exit 1
}

# Show current context and namespace
CURRENT_CONTEXT=$(kubectl config current-context)
CURRENT_NAMESPACE=$(kubectl config view --minify -o jsonpath='{..namespace}' || echo 'default')
echo "K8s Context: $CURRENT_CONTEXT"
echo "Namespace: $CURRENT_NAMESPACE"

# If context suggests different environment, prompt to switch
# Example: User mentions "production namespace" but current context is "staging-cluster"
# Detect from query context and prompt:
# echo "Query mentions 'production' but current context is '$CURRENT_CONTEXT'"
# echo "Switch to production context? Run: kubectl config use-context prod-cluster"
# read -p "Continue with current context? (y/n) " -n 1 -r
```

## Query Strategy

Follow this approach for effective Kubernetes debugging:

1. **Check pod status first**: `kubectl get pods -n <namespace>`
2. **Check events if pod failing**: `kubectl describe pod <pod-name> -n <namespace>` (events at bottom)
3. **Check logs if pod running**: `kubectl logs <pod-name> -n <namespace>`
4. **Check previous logs if crashed**: `kubectl logs <pod-name> --previous -n <namespace>`
5. **Correlate with GCP logs**: Save K8s events/logs to /tmp, check GCP for service logs

### Example Workflow

```bash
# Step 1: Check pod status
kubectl get pods -n production -l app=api-gateway

# Step 2: If pod is failing, describe for events
kubectl describe pod api-gateway-abc123 -n production
# Look at Events section at bottom for errors

# Step 3: If pod running but misbehaving, check logs
kubectl logs api-gateway-abc123 -n production --tail=200

# Step 4: If pod crashed/restarted, check previous logs
kubectl logs api-gateway-abc123 --previous -n production

# Step 5: Check namespace events for broader context
kubectl get events -n production --sort-by='.lastTimestamp' | tail -20
```

## Output Management

For large outputs or correlation with other tools, save to tmp file:

```bash
# Save pod list to tmp file
kubectl get pods -n production -o json > /tmp/k8s-pods-$(date +%Y%m%d-%H%M%S).json

# Save logs for offline analysis
kubectl logs api-gateway-xyz -n production --tail=1000 > /tmp/api-gateway-logs-$(date +%Y%m%d-%H%M%S).log

# Save events for correlation
kubectl get events -n production --sort-by='.lastTimestamp' > /tmp/k8s-events-$(date +%Y%m%d-%H%M%S).txt

# Then analyze or correlate with GCP logs
grep -i error /tmp/api-gateway-logs-*.log
```

**Benefits**:
- Correlate Kubernetes events with GCP logs using timestamps
- Share debugging context with team
- Preserve state for investigation

## Common Patterns

For detailed command reference, see:
- [kubectl command patterns](references/COMMANDS.md) - Get, describe, logs, events, metrics

### Quick Reference

```bash
# Get pods in namespace
kubectl get pods -n <namespace>

# Describe pod (includes events)
kubectl describe pod <pod-name> -n <namespace>

# Get pod logs
kubectl logs <pod-name> -n <namespace> --tail=200

# Get previous logs (after crash)
kubectl logs <pod-name> --previous -n <namespace>

# Get events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

## Tips

- Use `-n <namespace>` for all commands or set default: `kubectl config set-context --current --namespace=<namespace>`
- Use `--all-namespaces` or `-A` to search across all namespaces
- Use `-l` for label selectors: `-l app=api,tier=frontend`
- Use `--field-selector` for field-based filtering (e.g., `status.phase=Failed`)
- Check pod events with describe before checking logs (events show scheduling/startup issues)
- For debugging sessions, save logs/events to /tmp for correlation with GCP logs
- Use `-o wide` for additional columns (pod IP, node name)
- Use `-o json` or `-o yaml` for full resource definitions
