---
name: manage-kubernetes-secrets
description: >
  Implement secure secrets management in Kubernetes using SealedSecrets for GitOps,
  External Secrets Operator for cloud secret managers, and rotation strategies. Handle
  TLS certificates, API keys, and credentials with encryption at rest and RBAC controls.
  Use when storing sensitive configuration for Kubernetes applications, implementing GitOps
  where secrets must be version-controlled, integrating with AWS Secrets Manager or Azure
  Key Vault, rotating credentials without downtime, or migrating from plaintext Secrets to
  encrypted solutions.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: kubernetes, secrets, sealedsecrets, external-secrets, security
---

# Manage Kubernetes Secrets

Implement production-grade secrets management for Kubernetes with encryption, rotation, and integration with external secret stores.

## When to Use

- Storing sensitive configuration (API keys, passwords, tokens) for Kubernetes applications
- Implementing GitOps workflows where secrets must be committed to version control
- Integrating Kubernetes with AWS Secrets Manager, Azure Key Vault, GCP Secret Manager
- Rotating credentials and certificates without application downtime
- Enforcing least-privilege access to secrets across namespaces and teams
- Migrating from plaintext Secrets to encrypted or externally managed solutions

## Inputs

- **Required**: Kubernetes cluster with admin access
- **Required**: Secrets to manage (database credentials, API keys, TLS certificates)
- **Optional**: Cloud secret manager (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- **Optional**: Certificate authority for TLS certificate generation
- **Optional**: GitOps repository for SealedSecrets
- **Optional**: Key management service (KMS) for encryption at rest

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Enable Kubernetes Secrets Encryption at Rest

Configure encryption at rest for Secrets using KMS or local encryption.

```bash
# For AWS EKS, enable secrets encryption with KMS
cat > encryption-config.yaml <<EOF
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
  - resources:
      - secrets
    providers:
      - aescbc:
          keys:
            - name: key1
              secret: $(head -c 32 /dev/urandom | base64)
      - identity: {}
EOF

# For self-hosted clusters, configure API server
# Add to kube-apiserver flags:
# --encryption-provider-config=/etc/kubernetes/encryption-config.yaml

# Verify encryption status
kubectl get secrets -A -o json | jq '.items[] | select(.metadata.name != "default-token") | .metadata.name'

# Encrypt existing secrets by reading and rewriting
kubectl get secrets --all-namespaces -o json | kubectl replace -f -

# Verify a secret is encrypted at rest
# Check etcd directly (requires etcd access)
ETCDCTL_API=3 etcdctl get /registry/secrets/default/my-secret --print-value-only | hexdump -C
```

For cloud-managed Kubernetes:

```bash
# AWS EKS - Create KMS key
aws kms create-key --description "EKS secrets encryption"
KMS_KEY_ARN=$(aws kms describe-key --key-id alias/eks-secrets --query 'KeyMetadata.Arn' --output text)

# Enable encryption on EKS cluster
aws eks associate-encryption-config \
  --cluster-name my-cluster \
  --encryption-config "resources=secrets,provider={keyArn=$KMS_KEY_ARN}"

# GKE - Enable application-layer secrets encryption
gcloud container clusters update my-cluster \
  --database-encryption-key projects/PROJECT_ID/locations/LOCATION/keyRings/RING_NAME/cryptoKeys/KEY_NAME

# AKS - Encryption enabled by default with platform-managed keys
# Optionally use customer-managed keys
az aks update \
  --name my-cluster \
  --resource-group my-rg \
  --enable-azure-keyvault-secrets-provider
```

**Expected:** Secrets encrypted at rest in etcd. Hexdump shows encrypted data, not plaintext. KMS integration configured for cloud-managed clusters. Re-encryption of existing secrets completes without errors.

**On failure:** For API server startup failures, verify encryption-config.yaml syntax and key format (must be base64-encoded 32-byte key). For KMS errors, check IAM permissions allow kms:Decrypt and kms:Encrypt. For etcd access issues, use backup/restore procedure to recover if encryption misconfigured.

### Step 2: Install and Configure Sealed Secrets for GitOps

Deploy Bitnami Sealed Secrets controller to encrypt secrets for Git storage.

```bash
# Install Sealed Secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/controller.yaml

# Verify controller is running
kubectl get pods -n kube-system -l name=sealed-secrets-controller

# Install kubeseal CLI
wget https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.24.0/kubeseal-0.24.0-linux-amd64.tar.gz
tar xfz kubeseal-0.24.0-linux-amd64.tar.gz
sudo install -m 755 kubeseal /usr/local/bin/kubeseal

# Fetch public key for offline sealing
kubeseal --fetch-cert \
  --controller-namespace=kube-system \
  --controller-name=sealed-secrets-controller \
  > pub-cert.pem

# Create a regular Secret (NOT applied to cluster yet)
kubectl create secret generic mysecret \
  --from-literal=username=admin \
  --from-literal=password='sup3rs3cr3t!' \
  --dry-run=client \
  -o yaml > mysecret.yaml

# Seal the secret
kubeseal --format=yaml --cert=pub-cert.pem < mysecret.yaml > mysealedsecret.yaml

# Inspect sealed secret (safe to commit to Git)
cat mysealedsecret.yaml
```

The sealed secret will look like:

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: default
spec:
  encryptedData:
    username: AgA8V7f3q2... (encrypted data)
    password: AgBkXp9n1h... (encrypted data)
  template:
    metadata:
      name: mysecret
      namespace: default
```

Apply and verify:

```bash
# Apply sealed secret to cluster
kubectl apply -f mysealedsecret.yaml

# Verify regular Secret was created automatically
kubectl get secret mysecret -o yaml

# Decode secret to verify values
kubectl get secret mysecret -o jsonpath='{.data.username}' | base64 -d

# Commit sealed secret to Git (safe, encrypted)
git add mysealedsecret.yaml
git commit -m "Add database credentials as sealed secret"
```

**Expected:** Sealed Secrets controller running in kube-system namespace. Public certificate fetched. Kubeseal encrypts Secrets using public key. Sealed Secrets applied to cluster automatically create decrypted Secrets. Only controller can decrypt (has private key).

**On failure:** For encryption errors, verify controller is running and pub-cert.pem is valid. For decryption failures, check controller logs with `kubectl logs -n kube-system -l name=sealed-secrets-controller`. For namespace mismatch errors, sealed secrets are namespace-scoped by default; use `--scope cluster-wide` for cross-namespace secrets. If private key lost, sealed secrets cannot be decrypted; backup controller key with `kubectl get secret -n kube-system sealed-secrets-key -o yaml > sealed-secrets-backup.yaml`.

### Step 3: Deploy External Secrets Operator for Cloud Secret Managers

Integrate Kubernetes with AWS Secrets Manager, Azure Key Vault, or GCP Secret Manager.

```bash
# Install External Secrets Operator via Helm
helm repo add external-secrets https://charts.external-secrets.io
helm repo update

helm install external-secrets \
  external-secrets/external-secrets \
  --namespace external-secrets-system \
  --create-namespace

# Verify operator is running
kubectl get pods -n external-secrets-system

# Create IAM role for AWS Secrets Manager (EKS with IRSA)
cat > trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/oidc.eks.REGION.amazonaws.com/id/OIDC_ID"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.REGION.amazonaws.com/id/OIDC_ID:sub": "system:serviceaccount:default:external-secrets-sa"
        }
      }
    }
  ]
}
EOF

aws iam create-role \
  --role-name external-secrets-role \
  --assume-role-policy-document file://trust-policy.json

aws iam attach-role-policy \
  --role-name external-secrets-role \
  --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite

# Create SecretStore referencing AWS Secrets Manager
cat <<EOF | kubectl apply -f -
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secretsmanager
  namespace: default
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: external-secrets-sa
  namespace: default
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::ACCOUNT_ID:role/external-secrets-role
EOF

# Create secret in AWS Secrets Manager
aws secretsmanager create-secret \
  --name myapp/database \
  --secret-string '{
    "username":"dbadmin",
    "password":"dbpass123",
    "endpoint":"db.example.com:5432",
    "database":"myapp"
  }'

# Create ExternalSecret to sync from AWS
cat <<EOF | kubectl apply -f -
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: myapp-database
  namespace: default
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager
    kind: SecretStore
  target:
    name: myapp-db-secret
    creationPolicy: Owner
  data:
  - secretKey: username
    remoteRef:
      key: myapp/database
      property: username
  - secretKey: password
    remoteRef:
      key: myapp/database
      property: password
  - secretKey: endpoint
    remoteRef:
      key: myapp/database
      property: endpoint
EOF

# Verify ExternalSecret synced
kubectl get externalsecret myapp-database
kubectl get secret myapp-db-secret -o yaml

# Check synchronization status
kubectl describe externalsecret myapp-database
```

For Azure Key Vault:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: azure-keyvault
  namespace: default
spec:
  provider:
    azurekv:
      authType: ManagedIdentity
      vaultUrl: "https://my-keyvault.vault.azure.net"
      tenantId: "tenant-id"
```

**Expected:** External Secrets Operator running. SecretStore configured with cloud provider credentials. ExternalSecret resources automatically create Kubernetes Secrets by pulling from cloud secret managers. Secrets refresh hourly. Changes in cloud secret manager propagate to cluster.

**On failure:** For authentication errors, verify IAM role/service account annotations and trust policy allows assume role. For sync failures, check ExternalSecret status with `kubectl describe externalsecret`. For missing secrets in cloud, verify secret names and JSON property paths match. Test AWS credentials with `aws secretsmanager get-secret-value --secret-id myapp/database`.

### Step 4: Implement Certificate Management with cert-manager

Automate TLS certificate provisioning and renewal using cert-manager.

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Verify installation
kubectl get pods -n cert-manager

# ... (see EXAMPLES.md for complete configuration)
```

For ingress annotation-based certificate issuance:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: myapp-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** cert-manager obtains certificate from Let's Encrypt. TLS secret created with valid certificate and private key. Certificate auto-renews before expiration. Ingress uses certificate for HTTPS termination.

**On failure:** For ACME challenge failures, verify DNS points to Ingress LoadBalancer IP for http01, or Route53 IAM permissions for dns01. For rate limit errors, use `letsencrypt-staging` issuer for testing. For renewal failures, check cert-manager logs with `kubectl logs -n cert-manager deployment/cert-manager`. Test certificate with `curl -v https://myapp.example.com`.

### Step 5: Implement Secret Rotation Strategy

Automate secret rotation with version management and application restarts.

```bash
# Enable automatic Pod restarts on Secret changes with Reloader
kubectl apply -f https://raw.githubusercontent.com/stakater/Reloader/master/deployments/kubernetes/reloader.yaml

# Annotate Deployment to watch Secrets
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
# ... (see EXAMPLES.md for complete configuration)
```

Verify rotation workflow:

```bash
# Manually trigger rotation
kubectl create job --from=cronjob/secret-rotation manual-rotation-$(date +%s)

# Watch for Secret update
kubectl get secret myapp-db-secret -w

# Verify Reloader triggered Pod restart
kubectl get events --sort-by='.lastTimestamp' | grep Reloader

# Check new Pods are using updated secret
kubectl get pods -l app=myapp
kubectl exec -it <pod-name> -- env | grep DB_PASSWORD
```

**Expected:** Reloader watches Secrets/ConfigMaps and restarts Pods on changes. Secret rotation updates AWS Secrets Manager, External Secrets Operator syncs to Kubernetes, Reloader triggers rolling restart. Application picks up new credentials without manual intervention.

**On failure:** For Reloader not triggering, verify annotation syntax and Reloader is running with `kubectl get pods -n default -l app=reloader-reloader`. For External Secrets sync delays, decrease refreshInterval or manually trigger with `kubectl annotate externalsecret myapp-database force-sync="$(date +%s)" --overwrite`. For application connection failures during rotation, implement graceful secret reload in application code or use connection pooling with retry logic.

### Step 6: Implement RBAC for Secrets Access Control

Restrict secret access using Kubernetes RBAC with least-privilege principle.

```yaml
# Create namespace for sensitive workloads
apiVersion: v1
kind: Namespace
metadata:
  name: production
---
# ... (see EXAMPLES.md for complete configuration)
```

Test RBAC:

```bash
# Apply RBAC resources
kubectl apply -f rbac.yaml

# Test as application service account
kubectl auth can-i get secret myapp-db-secret --as=system:serviceaccount:production:myapp -n production
# Should return "yes"
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Service accounts have read-only access to specific secrets via resourceNames. Developers cannot view secrets in production namespace. Only secret-admins group can create/update/delete secrets. RBAC denials logged in audit logs.

**On failure:** For access denied errors, verify RoleBinding subjects match ServiceAccount name and namespace. For overly permissive roles, remove wildcard verbs and add resourceNames restriction. For audit log gaps, enable Kubernetes audit logging at API server level. Test with `kubectl auth can-i` before deploying changes.

## Validation

- [ ] Secrets encrypted at rest in etcd (verify with etcdctl or KMS)
- [ ] Sealed Secrets controller running and public certificate fetched
- [ ] External Secrets Operator syncing from cloud secret managers
- [ ] TLS certificates issued by cert-manager and auto-renewing
- [ ] Secret rotation automated with application restarts via Reloader
- [ ] RBAC policies enforce least-privilege access to secrets
- [ ] No plaintext secrets in Git repositories or container images
- [ ] Backup/restore procedure tested for sealed-secrets private key
- [ ] Monitoring alerts configured for secret sync failures and expiration

## Common Pitfalls

- **Secrets in Git history**: Committing plaintext secrets then later removing them doesn't purge Git history. Use git-filter-repo or BFG to rewrite history, rotate compromised secrets.

- **Overly broad RBAC**: Granting `get secrets` on all secrets in namespace. Use resourceNames to restrict access to specific secrets only.

- **No rotation strategy**: Secrets never rotated, increasing blast radius of compromise. Implement automated rotation with External Secrets Operator or CronJobs.

- **Missing encryption at rest**: Secrets stored in plaintext in etcd. Enable encryption provider or KMS integration before storing sensitive data.

- **Application caching secrets**: App reads secret once at startup and never reloads. Implement signal handling (SIGHUP) or file watcher for secret file changes.

- **External Secrets refresh too slow**: Default 1h refresh means secrets changes take up to an hour to propagate. Lower refreshInterval for critical secrets, use webhooks for immediate updates.

- **No backup of sealed-secrets key**: Controller private key lost, all sealed secrets unrecoverable. Backup with `kubectl get secret -n kube-system sealed-secrets-key -o yaml > backup.yaml` and store securely.

- **Certificate renewal failures**: cert-manager unable to renew due to DNS/firewall changes. Monitor certificate expiry with Prometheus metrics and alerts.

## Related Skills

- `deploy-to-kubernetes` - Using secrets in Deployments and StatefulSets
- `enforce-policy-as-code` - OPA policies for secret access validation
- `security-audit-codebase` - Detecting hardcoded secrets in application code
- `configure-ingress-networking` - TLS certificate usage in Ingress resources
- `implement-gitops-workflow` - Sealed Secrets in ArgoCD/Flux pipelines
