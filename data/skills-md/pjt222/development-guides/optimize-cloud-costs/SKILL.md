---
name: optimize-cloud-costs
description: >
  Implement cloud cost optimization strategies for Kubernetes workloads using tools like
  Kubecost for visibility, right-sizing recommendations, horizontal and vertical pod
  autoscaling, spot/preemptible instances, and resource quotas. Covers cost allocation,
  showback reporting, and continuous optimization practices. Use when cloud costs are
  growing without proportional business value, when resource requests are misaligned with
  actual usage, when manual scaling leads to over-provisioning, or when implementing
  showback and chargeback for internal cost accountability.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: cost-optimization, kubecost, hpa, vpa, spot-instances, resource-management, kubernetes
---

# Optimize Cloud Costs

Implement comprehensive cost optimization strategies for Kubernetes clusters to reduce cloud spending.

## When to Use

- Cloud infrastructure costs growing without corresponding business value increase
- Need visibility into cost allocation by team, application, or environment
- Resource requests/limits not aligned with actual usage patterns
- Manual scaling leading to over-provisioning and waste
- Want to leverage spot/preemptible instances for non-critical workloads
- Need to implement showback or chargeback for internal cost allocation
- Seeking to establish FinOps culture with cost awareness and accountability

## Inputs

- **Required**: Kubernetes cluster with workloads running
- **Required**: Cloud provider billing API access
- **Required**: Metrics server or Prometheus for resource metrics
- **Optional**: Historical usage data for trend analysis
- **Optional**: Cost allocation requirements (by namespace, label, team)
- **Optional**: Service level objectives (SLOs) for performance constraints
- **Optional**: Budget limits or cost reduction targets

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Deploy Cost Visibility Tools

Install Kubecost or OpenCost for cost monitoring and allocation.

**Install Kubecost:**
```bash
# Add Kubecost Helm repository
helm repo add kubecost https://kubecost.github.io/cost-analyzer/
helm repo update

# Install Kubecost with Prometheus integration
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set kubecostToken="your-token-here" \
  --set prometheus.server.global.external_labels.cluster_id="production-cluster" \
  --set prometheus.nodeExporter.enabled=true \
  --set prometheus.serviceAccounts.nodeExporter.create=true

# For existing Prometheus, configure Kubecost to use it
helm install kubecost kubecost/cost-analyzer \
  --namespace kubecost \
  --create-namespace \
  --set prometheus.enabled=false \
  --set global.prometheus.fqdn="http://prometheus-server.monitoring.svc.cluster.local" \
  --set global.prometheus.enabled=true

# Verify installation
kubectl get pods -n kubecost
kubectl get svc -n kubecost

# Access Kubecost UI
kubectl port-forward -n kubecost svc/kubecost-cost-analyzer 9090:9090
# Open http://localhost:9090
```

**Configure cloud provider integration:**
```yaml
# kubecost-cloud-integration.yaml
apiVersion: v1
kind: Secret
metadata:
  name: cloud-integration
  namespace: kubecost
type: Opaque
stringData:
  # For AWS
  cloud-integration.json: |
    {
      "aws": [
        {
          "serviceKeyName": "AWS_ACCESS_KEY_ID",
          "serviceKeySecret": "AWS_SECRET_ACCESS_KEY",
          "athenaProjectID": "cur-query-results",
          "athenaBucketName": "s3://your-cur-bucket",
          "athenaRegion": "us-east-1",
          "athenaDatabase": "athenacurcfn_my_cur",
          "athenaTable": "my_cur"
        }
      ]
    }
---
# For GCP
apiVersion: v1
kind: Secret
metadata:
  name: gcp-key
  namespace: kubecost
type: Opaque
data:
  key.json: <base64-encoded-service-account-key>
---
# For Azure
apiVersion: v1
kind: ConfigMap
metadata:
  name: azure-config
  namespace: kubecost
data:
  azure.json: |
    {
      "azureSubscriptionID": "your-subscription-id",
      "azureClientID": "your-client-id",
      "azureClientSecret": "your-client-secret",
      "azureTenantID": "your-tenant-id",
      "azureOfferDurableID": "MS-AZR-0003P"
    }
```

Apply cloud integration:
```bash
kubectl apply -f kubecost-cloud-integration.yaml

# Verify cloud costs are being imported
kubectl logs -n kubecost -l app=cost-analyzer -c cost-model --tail=100 | grep -i "cloud"

# Check Kubecost API for cost data
kubectl port-forward -n kubecost svc/kubecost-cost-analyzer 9090:9090 &
curl http://localhost:9090/model/allocation\?window\=7d | jq .
```

**Expected:** Kubecost pods running successfully. UI accessible showing cost breakdown by namespace, deployment, pod. Cloud provider costs importing (may take 24-48 hours for initial sync). API returning allocation data.

**On failure:**
- Check Prometheus is running and accessible: `kubectl get svc -n monitoring prometheus-server`
- Verify cloud credentials have billing API access
- Review cost-model logs: `kubectl logs -n kubecost -l app=cost-analyzer -c cost-model`
- Ensure metrics-server or Prometheus node-exporter collecting resource metrics
- Check for network policies blocking access to cloud billing APIs

### Step 2: Analyze Current Resource Utilization

Identify over-provisioned resources and optimization opportunities.

**Query resource utilization:**
```bash
# Get resource requests vs usage for all pods
kubectl top pods --all-namespaces --containers | \
  awk 'NR>1 {print $1,$2,$3,$4,$5}' > current-usage.txt

# Compare requests to actual usage
cat <<'EOF' > analyze-utilization.sh
#!/bin/bash
echo "Pod,Namespace,CPU-Request,CPU-Usage,Memory-Request,Memory-Usage"
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}'); do
  kubectl get pods -n $ns -o json | jq -r '
    .items[] |
    select(.status.phase == "Running") |
    {
      name: .metadata.name,
      namespace: .metadata.namespace,
      containers: [
        .spec.containers[] |
        {
          name: .name,
          cpuReq: .resources.requests.cpu,
          memReq: .resources.requests.memory
        }
      ]
    } |
    "\(.name),\(.namespace),\(.containers[].cpuReq // "none"),\(.containers[].memReq // "none")"
  ' 2>/dev/null
done
EOF

chmod +x analyze-utilization.sh
./analyze-utilization.sh > resource-requests.csv

# Get actual usage from metrics server
kubectl top pods --all-namespaces --containers > actual-usage.txt
```

**Use Kubecost recommendations:**
```bash
# Get right-sizing recommendations via API
curl "http://localhost:9090/model/savings/requestSizing?window=7d" | jq . > recommendations.json

# Extract top wasteful resources
jq '.data[] | select(.totalRecommendedSavings > 10) | {
  cluster: .clusterID,
# ... (see EXAMPLES.md for complete configuration)
```

**Create utilization dashboard:**
```yaml
# grafana-utilization-dashboard.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: utilization-dashboard
  namespace: monitoring
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Clear view of current resource requests vs actual usage. Identification of pods with <30% utilization (over-provisioned). List of optimization opportunities with estimated savings. Dashboard showing utilization trends over time.

**On failure:**
- Ensure metrics-server is running: `kubectl get deployment metrics-server -n kube-system`
- Check if Prometheus has node-exporter metrics: `curl http://prometheus:9090/api/v1/query?query=node_cpu_seconds_total`
- Verify pods have been running long enough for meaningful data (at least 24 hours)
- Check for gaps in metrics collection: review Prometheus retention and scrape intervals
- For Kubecost, ensure it has collected at least 48 hours of data

### Step 3: Implement Horizontal Pod Autoscaling (HPA)

Configure automatic scaling based on CPU, memory, or custom metrics.

**Create HPA for CPU-based scaling:**
```yaml
# hpa-cpu.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-server-hpa
  namespace: production
# ... (see EXAMPLES.md for complete configuration)
```

**Deploy and verify HPA:**
```bash
kubectl apply -f hpa-cpu.yaml

# Check HPA status
kubectl get hpa -n production
kubectl describe hpa api-server-hpa -n production

# Monitor scaling events
kubectl get events -n production --field-selector involvedObject.kind=HorizontalPodAutoscaler --watch

# Generate load to test autoscaling
kubectl run load-generator --rm -it --image=busybox -- /bin/sh -c \
  "while true; do wget -q -O- http://api-server.production.svc.cluster.local; done"

# Watch replicas scale
watch kubectl get hpa,deployment -n production
```

**Expected:** HPA created and showing current/target metrics. Pods scale up under load. Pods scale down when load decreases (after stabilization window). Scaling events logged. No thrashing (rapid scale up/down cycles).

**On failure:**
- Verify metrics-server is running: `kubectl get apiservice v1beta1.metrics.k8s.io`
- Check if deployment has resource requests set (HPA requires this)
- Review HPA events: `kubectl describe hpa api-server-hpa -n production`
- Ensure target deployment is not at max replicas
- For custom metrics, verify metrics adapter installed and configured
- Check HPA controller logs: `kubectl logs -n kube-system -l app=kube-controller-manager | grep horizontal-pod-autoscaler`

### Step 4: Configure Vertical Pod Autoscaling (VPA)

Automatically adjust resource requests based on actual usage patterns.

**Install VPA:**
```bash
# Clone VPA repository
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler

# Install VPA
./hack/vpa-up.sh

# Verify installation
kubectl get pods -n kube-system | grep vpa

# Check VPA CRDs
kubectl get crd | grep verticalpodautoscaler
```

**Create VPA policies:**
```yaml
# vpa-policies.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: api-server-vpa
  namespace: production
# ... (see EXAMPLES.md for complete configuration)
```

**Deploy and monitor VPA:**
```bash
kubectl apply -f vpa-policies.yaml

# Check VPA recommendations
kubectl get vpa -n production
kubectl describe vpa api-server-vpa -n production

# View detailed recommendations
kubectl get vpa api-server-vpa -n production -o jsonpath='{.status.recommendation}' | jq .

# Monitor VPA-initiated pod updates
kubectl get events -n production --field-selector involvedObject.kind=VerticalPodAutoscaler --watch

# Compare recommendations to current requests
kubectl get deployment api-server -n production -o json | \
  jq '.spec.template.spec.containers[].resources.requests'
```

**Expected:** VPA providing recommendations or automatically updating resource requests. Recommendations based on percentile usage patterns (typically P95). Pods restarted with new requests when using Auto/Recreate mode. No conflicts between HPA and VPA (use HPA for replicas, VPA for resources per pod).

**On failure:**
- Ensure metrics-server has sufficient data (VPA needs several days for accurate recommendations)
- Check VPA components running: `kubectl get pods -n kube-system | grep vpa`
- Review VPA admission controller logs: `kubectl logs -n kube-system -l app=vpa-admission-controller`
- Verify webhook is registered: `kubectl get mutatingwebhookconfigurations vpa-webhook-config`
- Don't use VPA and HPA on same metric (CPU/memory) - causes conflicts
- Start with "Off" mode to review recommendations before enabling automatic updates

### Step 5: Leverage Spot/Preemptible Instances

Configure workload scheduling on cost-effective spot instances.

**Create node pools with spot instances:**
```yaml
# For AWS (via Karpenter)
apiVersion: karpenter.sh/v1alpha5
kind: Provisioner
metadata:
  name: spot-provisioner
spec:
# ... (see EXAMPLES.md for complete configuration)
```

**Configure workloads for spot instances:**
```yaml
# spot-workload.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: batch-processor
  namespace: production
# ... (see EXAMPLES.md for complete configuration)
```

**Deploy and monitor spot usage:**
```bash
kubectl apply -f spot-workload.yaml

# Monitor spot node allocation
kubectl get nodes -l node-type=spot

# Check workload distribution
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Workloads scheduled on spot nodes successfully. Significant cost reduction (typically 60-90% vs on-demand). Graceful handling of spot interruptions with pod rescheduling. Monitoring shows spot interruption rate and successful recovery.

**On failure:**
- Verify spot instance availability in your region/zones
- Check node labels and taints match workload tolerations
- Review Karpenter logs: `kubectl logs -n karpenter -l app.kubernetes.io/name=karpenter`
- Ensure workloads are stateless or have proper state management for interruptions
- Test interruption handling: manually cordon and drain spot node
- Monitor interruption rate - if too high, consider fallback to on-demand nodes

### Step 6: Implement Resource Quotas and Budget Alerts

Set hard limits and alerting for cost control.

**Create resource quotas:**
```yaml
# resource-quotas.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
# ... (see EXAMPLES.md for complete configuration)
```

**Configure budget alerts:**
```yaml
# kubecost-budget-alerts.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: budget-alerts
  namespace: kubecost
# ... (see EXAMPLES.md for complete configuration)
```

Apply and monitor:
```bash
kubectl apply -f resource-quotas.yaml
kubectl apply -f kubecost-budget-alerts.yaml

# Check quota usage
kubectl get resourcequota -n production
kubectl describe resourcequota production-quota -n production
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Resource quotas enforcing limits per namespace. Pod creation blocked when quota exceeded. Budget alerts firing when thresholds breached. Cost spike detection working. Regular reports sent to stakeholders.

**On failure:**
- Verify ResourceQuota and LimitRange applied correctly: `kubectl get resourcequota,limitrange -A`
- Check for pods failing due to quota: `kubectl get events -n production | grep quota`
- Review Kubecost alert configuration: `kubectl logs -n kubecost -l app=cost-analyzer | grep alert`
- Ensure Prometheus has Kubecost metrics: `curl http://prometheus:9090/api/v1/query?query=kubecost_monthly_cost`
- Test alert routing: verify email/Slack webhook configuration

## Validation

- [ ] Kubecost or OpenCost deployed and showing accurate cost data
- [ ] Cloud provider billing integration working (costs match actual bills)
- [ ] Resource utilization analysis identifies over-provisioned workloads
- [ ] HPA scaling pods based on load (verified with load test)
- [ ] VPA providing recommendations or auto-adjusting resource requests
- [ ] Spot instances handling interruptions gracefully
- [ ] Resource quotas enforcing limits per namespace
- [ ] Budget alerts firing when thresholds exceeded
- [ ] Monthly cost trending downward or staying within budget
- [ ] Showback reports generated for teams/projects
- [ ] No performance degradation from cost optimizations
- [ ] Documentation updated with optimization practices

## Common Pitfalls

- **Aggressive Right-Sizing**: Don't immediately apply VPA recommendations. Start with "Off" mode, review suggestions for a week, then gradually apply. Sudden changes can cause OOMKills or CPU throttling.

- **HPA + VPA Conflict**: Never use HPA and VPA on same metric (CPU/memory). Use HPA for horizontal scaling, VPA for per-pod resource tuning, or HPA on custom metrics + VPA on resources.

- **Spot Without Fault Tolerance**: Only run fault-tolerant, stateless workloads on spot. Never databases, stateful services, or single-replica critical services. Always use PodDisruptionBudgets.

- **Insufficient Monitoring Period**: Cost optimization decisions need historical data. Wait at least 7 days before making changes, 30 days for VPA recommendations, 90 days for trend analysis.

- **Ignoring Burst Requirements**: Setting limits too low based on average usage causes throttling during traffic spikes. Use P95 or P99 percentiles, not average, for capacity planning.

- **Network Egress Costs**: Compute costs visible in Kubecost, but egress (data transfer) can be significant. Monitor cross-AZ traffic, use topology-aware routing, consider data transfer costs in architecture.

- **Storage Overlooked**: PersistentVolume costs often forgotten. Audit unused PVCs, right-size volumes, use volume expansion instead of over-provisioning, implement PV cleanup policies.

- **Quota Too Restrictive**: Setting quotas too low blocks legitimate growth. Review quota usage monthly, adjust based on actual needs, communicate limits to teams before enforcement.

- **False Savings from Wrong Metrics**: Using CPU/memory as sole optimization metric misses I/O, network, storage costs. Consider total cost of ownership, not just compute.

- **Chargeback Before Trust**: Implementing chargeback before teams understand and trust cost data causes friction. Start with showback (informational), build culture of cost awareness, then move to chargeback.

## Related Skills

- `deploy-to-kubernetes` - Application deployment with appropriate resource requests
- `setup-prometheus-monitoring` - Monitoring infrastructure for cost metrics
- `plan-capacity` - Capacity planning based on cost and performance
- `setup-local-kubernetes` - Local development to avoid cloud costs
- `write-helm-chart` - Templating resource requests and limits
- `implement-gitops-workflow` - GitOps for cost-optimized configurations
