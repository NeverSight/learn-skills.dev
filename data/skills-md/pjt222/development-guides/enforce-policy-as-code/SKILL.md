---
name: enforce-policy-as-code
description: >
  Implement policy-as-code enforcement using OPA Gatekeeper or Kyverno to validate and mutate
  Kubernetes resources according to organizational policies. Covers constraint templates,
  admission control, audit mode, reporting violations, and integrating with CI/CD pipelines
  for shift-left policy validation. Use when enforcing resource configuration standards,
  preventing security misconfigurations such as privileged containers, ensuring compliance
  before deployment, standardizing naming conventions, or auditing existing cluster resources
  against policies.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: opa, gatekeeper, kyverno, policy, admission-control, compliance, kubernetes
---

# Enforce Policy as Code

Implement declarative policy enforcement using OPA Gatekeeper or Kyverno for Kubernetes resource validation and mutation.

## When to Use

- Enforce organizational standards for resource configuration (labels, annotations, limits)
- Prevent security misconfigurations (privileged containers, host namespaces, insecure images)
- Ensure compliance requirements are met before resources deployed
- Standardize resource naming conventions and metadata
- Implement automated remediation through mutation policies
- Audit existing cluster resources against policies without blocking
- Integrate policy validation into CI/CD pipelines for shift-left approach

## Inputs

- **Required**: Kubernetes cluster with admin access
- **Required**: Choice of policy engine (OPA Gatekeeper or Kyverno)
- **Required**: List of policies to enforce (security, compliance, operational)
- **Optional**: Existing resources to audit
- **Optional**: Exemption/exclusion patterns for specific namespaces or resources
- **Optional**: CI/CD pipeline configuration for pre-deployment validation

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Install Policy Engine

Deploy OPA Gatekeeper or Kyverno as admission controller.

**For OPA Gatekeeper:**
```bash
# Install Gatekeeper using Helm
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm repo update

# Install with audit enabled
helm install gatekeeper gatekeeper/gatekeeper \
  --namespace gatekeeper-system \
  --create-namespace \
  --set audit.replicas=2 \
  --set replicas=3 \
  --set validatingWebhookFailurePolicy=Fail \
  --set auditInterval=60

# Verify installation
kubectl get pods -n gatekeeper-system
kubectl get crd | grep gatekeeper

# Check webhook configuration
kubectl get validatingwebhookconfigurations gatekeeper-validating-webhook-configuration -o yaml
```

**For Kyverno:**
```bash
# Install Kyverno using Helm
helm repo add kyverno https://kyverno.github.io/kyverno/
helm repo update

# Install with HA setup
helm install kyverno kyverno/kyverno \
  --namespace kyverno \
  --create-namespace \
  --set replicaCount=3 \
  --set admissionController.replicas=3 \
  --set backgroundController.replicas=2 \
  --set cleanupController.replicas=2

# Verify installation
kubectl get pods -n kyverno
kubectl get crd | grep kyverno

# Check webhook configurations
kubectl get validatingwebhookconfigurations kyverno-resource-validating-webhook-cfg
kubectl get mutatingwebhookconfigurations kyverno-resource-mutating-webhook-cfg
```

Create namespace exclusions:
```yaml
# gatekeeper-config.yaml
apiVersion: config.gatekeeper.sh/v1alpha1
kind: Config
metadata:
  name: config
  namespace: gatekeeper-system
spec:
  match:
    - excludedNamespaces:
      - kube-system
      - kube-public
      - kube-node-lease
      - gatekeeper-system
      processes:
      - audit
      - webhook
  validation:
    traces:
      - user: system:serviceaccount:gatekeeper-system:gatekeeper-admin
        kind:
          group: ""
          version: v1
          kind: Namespace
```

**Expected:** Policy engine pods running with multiple replicas. CRDs installed (ConstraintTemplate, Constraint for Gatekeeper; ClusterPolicy, Policy for Kyverno). Validating/mutating webhooks active. Audit controller running.

**On failure:**
- Check pod logs: `kubectl logs -n gatekeeper-system -l app=gatekeeper --tail=50`
- Verify webhook endpoints reachable: `kubectl get endpoints -n gatekeeper-system`
- Check for port conflicts or certificate issues in webhook logs
- Ensure cluster has sufficient resources (policy engines need ~500MB per replica)
- Review RBAC permissions: `kubectl auth can-i create constrainttemplates --as=system:serviceaccount:gatekeeper-system:gatekeeper-admin`

### Step 2: Define Constraint Templates and Policies

Create reusable policy templates and specific constraints.

**OPA Gatekeeper Constraint Template:**
```yaml
# required-labels-template.yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8srequiredlabels
  annotations:
# ... (see EXAMPLES.md for complete configuration)
```

**Kyverno ClusterPolicy:**
```yaml
# kyverno-policies.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-labels
  annotations:
# ... (see EXAMPLES.md for complete configuration)
```

Apply policies:
```bash
# Apply Gatekeeper templates and constraints
kubectl apply -f required-labels-template.yaml

# Apply Kyverno policies
kubectl apply -f kyverno-policies.yaml

# Verify constraint/policy status
kubectl get constraints
kubectl get clusterpolicies

# Check for any policy errors
kubectl describe k8srequiredlabels require-app-labels
kubectl describe clusterpolicy require-labels
```

**Expected:** ConstraintTemplates/ClusterPolicies created successfully. Constraints show status "True" for enforcement. No errors in policy definitions. Webhook begins evaluating new resources against policies.

**On failure:**
- Validate Rego syntax (Gatekeeper): Use `opa test` locally or check constraint status
- Check policy YAML syntax: `kubectl apply --dry-run=client -f policy.yaml`
- Review constraint status: `kubectl get constraint -o yaml | grep -A 10 status`
- Test with simple policy first, then add complexity
- Verify match criteria (kinds, namespaces) are correct

### Step 3: Test Policy Enforcement

Validate policies block non-compliant resources and allow compliant ones.

Create test manifests:
```yaml
# test-non-compliant.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-no-labels
  namespace: production
# ... (see EXAMPLES.md for complete configuration)
```

Test policies:
```bash
# Attempt to create non-compliant resource (should fail)
kubectl apply -f test-non-compliant.yaml
# Expected: Error with policy violation message

# Create compliant resource (should succeed)
kubectl apply -f test-compliant.yaml
# Expected: deployment.apps/test-compliant created

# Test with dry-run for validation
kubectl apply -f test-non-compliant.yaml --dry-run=server
# Shows policy violations without actually creating resource

# Clean up
kubectl delete -f test-compliant.yaml
```

Test with policy reporting (Kyverno):
```bash
# Check policy reports
kubectl get policyreports -A
kubectl get clusterpolicyreports

# View detailed report
kubectl get policyreport -n production -o yaml

# Check policy rule results
kubectl get policyreport -n production -o jsonpath='{.items[0].results}' | jq .
```

**Expected:** Non-compliant resources rejected with clear violation messages. Compliant resources created successfully. Policy reports show pass/fail results. Dry-run validation works without creating resources.

**On failure:**
- Check if policy is in audit mode instead of enforce: `validationFailureAction: audit`
- Verify webhook is processing requests: `kubectl logs -n gatekeeper-system -l app=gatekeeper`
- Check for namespace exclusions that might exempt test namespace
- Test webhook connectivity: `kubectl run test --rm -it --image=busybox --restart=Never`
- Review webhook failure policy (Ignore vs Fail)

### Step 4: Implement Mutation Policies

Configure automatic remediation through mutation.

**Gatekeeper mutation:**
```yaml
# gatekeeper-mutations.yaml
apiVersion: mutations.gatekeeper.sh/v1beta1
kind: Assign
metadata:
  name: add-default-labels
spec:
# ... (see EXAMPLES.md for complete configuration)
```

**Kyverno mutation policies:**
```yaml
# kyverno-mutations.yaml
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: add-default-labels
spec:
# ... (see EXAMPLES.md for complete configuration)
```

Apply and test mutations:
```bash
# Apply mutation policies
kubectl apply -f gatekeeper-mutations.yaml
# OR
kubectl apply -f kyverno-mutations.yaml

# Test mutation with a deployment
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Mutations automatically add labels, resources, or modify images. Deployed resources show mutated values. Mutations logged in policy engine logs. No errors during mutation application.

**On failure:**
- Check mutation webhook is enabled: `kubectl get mutatingwebhookconfiguration`
- Verify mutation policy syntax: especially JSON paths and conditions
- Review logs: `kubectl logs -n kyverno deploy/kyverno-admission-controller`
- Test mutations don't conflict (multiple mutations on same field)
- Ensure mutation applied before validation (order matters)

### Step 5: Enable Audit Mode and Reporting

Configure audit to identify violations in existing resources without blocking.

**Gatekeeper audit:**
```bash
# Audit runs automatically based on auditInterval setting
# Check audit results
kubectl get constraints -o json | \
  jq '.items[] | {name: .metadata.name, violations: .status.totalViolations}'

# Get detailed violation information
# ... (see EXAMPLES.md for complete configuration)
```

**Kyverno audit and reporting:**
```bash
# Generate policy reports for existing resources
kubectl create job --from=cronjob/kyverno-cleanup-controller -n kyverno manual-report-gen

# View policy reports
kubectl get policyreport -A
kubectl get clusterpolicyreport
# ... (see EXAMPLES.md for complete configuration)
```

Create dashboard for policy compliance:
```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: policy-alerts
  namespace: monitoring
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Audit identifies violations in existing resources without blocking deployments. Policy reports generated with pass/fail counts. Violations exportable for review. Metrics exposed for monitoring. Alerts fire on increasing violations.

**On failure:**
- Verify audit controller running: `kubectl get pods -n gatekeeper-system -l gatekeeper.sh/operation=audit`
- Check audit interval setting in installation
- Review audit logs for errors: `kubectl logs -n gatekeeper-system -l gatekeeper.sh/operation=audit`
- Ensure RBAC permissions allow reading all resource types for audit
- Verify CRD status field being populated: `kubectl get constraint -o yaml | grep -A 20 status`

### Step 6: Integrate with CI/CD Pipeline

Add pre-deployment policy validation to shift-left policy enforcement.

**CI/CD integration script:**
```bash
#!/bin/bash
# validate-policies.sh

set -e

echo "=== Policy Validation for CI/CD ==="
# ... (see EXAMPLES.md for complete configuration)
```

**GitHub Actions workflow:**
```yaml
# .github/workflows/policy-validation.yaml
name: Policy Validation

on:
  pull_request:
    paths:
# ... (see EXAMPLES.md for complete configuration)
```

**Pre-commit hook:**
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate Kubernetes manifests against policies
if git diff --cached --name-only | grep -E 'manifests/.*\.yaml$'; then
  echo "Validating Kubernetes manifests against policies..."
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** CI/CD pipeline validates manifests before deployment. Policy violations fail pipeline with clear messages. Policy reports attached to PR. Pre-commit hooks catch violations early. Developers notified of policy issues before reaching cluster.

**On failure:**
- Verify CLI tools installed and in PATH
- Check kubeconfig credentials valid for fetching policies
- Test policy validation locally first: `kyverno apply policy.yaml --resource manifest.yaml`
- Ensure policies synced from cluster are complete
- Review policy CLI logs for specific validation errors

## Validation

- [ ] Policy engine pods running with HA configuration
- [ ] Validating and mutating webhooks active and reachable
- [ ] Constraint templates and policies created without errors
- [ ] Non-compliant resources rejected with clear violation messages
- [ ] Compliant resources deploy successfully
- [ ] Mutation policies automatically remediate resources
- [ ] Audit mode identifies violations in existing resources
- [ ] Policy reports generated and accessible
- [ ] Metrics exposed for policy compliance monitoring
- [ ] CI/CD pipeline validates manifests pre-deployment
- [ ] Pre-commit hooks prevent policy violations
- [ ] Namespace exclusions configured appropriately

## Common Pitfalls

- **Webhook Failure Policy**: `failurePolicy: Fail` blocks all resources if webhook unavailable. Use `Ignore` for non-critical policies, but understand security implications. Test webhook availability before enforcing.

- **Too Restrictive Initial Policies**: Starting with enforcement mode on strict policies breaks existing workloads. Begin with audit mode, review violations, communicate with teams, then enforce gradually.

- **Missing Resource Specifications**: Policies must specify API groups, versions, and kinds correctly. Use `kubectl api-resources` to find exact values. Wildcards (`*`) convenient but can cause performance issues.

- **Mutation Order**: Mutations applied before validations. Ensure mutations don't conflict and that validations account for mutated values. Test mutation+validation together.

- **Namespace Exclusions**: Excluding system namespaces necessary, but be careful not to over-exclude. Review exclusions regularly as policies mature.

- **Rego Complexity (Gatekeeper)**: Complex Rego policies difficult to debug. Start simple, test with `opa test` locally, add logging with `trace()`, use gator for offline testing.

- **Performance Impact**: Policy evaluation adds latency to admission. Keep policies efficient, use appropriate matching criteria, monitor webhook latency metrics.

- **Policy Conflicts**: Multiple policies modifying same field cause issues. Coordinate policies across teams, use policy libraries for common patterns, test combinations.

- **Background Scanning**: Background audit scans entire cluster. Can be resource-intensive in large clusters. Adjust audit interval based on cluster size and policy count.

- **Version Compatibility**: Policy CRD versions change. Gatekeeper v3 uses `v1beta1` constraints, Kyverno v1.11 uses `kyverno.io/v1`. Check docs for your version.

## Related Skills

- `manage-kubernetes-secrets` - Secret validation policies
- `security-audit-codebase` - Complementary security scanning
- `deploy-to-kubernetes` - Application deployment with policy validation
- `setup-service-mesh` - Service mesh authorization policies complement admission policies
- `configure-api-gateway` - Gateway policies work alongside admission policies
- `implement-gitops-workflow` - GitOps with policy validation in pipeline
