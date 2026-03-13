---
name: eks
description: |
  Deploy Phase Console on AWS EKS. Triggers: "deploy Phase on EKS", "set up EKS cluster for Phase",
  "install Phase Console on AWS", "Phase EKS deployment", "deploy Phase to Kubernetes on AWS",
  "set up Phase on AWS", "Phase Helm EKS setup"
---

# Deploy Phase Console on AWS EKS

This skill autonomously deploys Phase Console on AWS EKS using the Phase Helm chart. The agent handles all file creation, kubectl, helm, aws, and eksctl commands directly. The user only handles things that require their own secrets.

## Important Principles

- **Autopilot by default.** The agent creates files and runs commands without asking permission at each step. Show a preview of generated files once before writing, then proceed.
- **Never handle secrets directly.** Write the Kubernetes secret as a shell script (`create-secret.sh`) with `$(openssl rand -hex 32)` for auto-generated values and `EDIT_ME` placeholders for values the user must supply. Keep `--from-literal` lines flush with no unnecessary leading indentation — this makes the script easy to read and edit. Tell the user to fill in the `EDIT_ME` values and run the script. Never ask the user to type secret values into the chat.
- **Agent runs eksctl.** Do not ask the user to run `eksctl create cluster`. Run it directly and poll until completion.
- **License key is not a secret.** If the user has a Phase Enterprise license key, ask them to paste it directly into the chat.
- **Reference files for details.** See `refs/eks-deployment.md` for exact commands and YAML templates, and `refs/troubleshooting.md` for diagnosing issues.

## Workflow

### Phase 1 — Prerequisites

Run these checks automatically without asking:

1. `which aws` — if missing, point to https://aws.amazon.com/cli/ and stop
2. `which eksctl` — if missing, show the install command from references and stop
3. `which kubectl` — if missing, point to https://kubernetes.io/docs/tasks/tools/ and stop
4. `which helm` — if missing, show the install command from references and stop
5. `aws sts get-caller-identity` — if it fails, say: "Please run `aws configure` or `aws sso login` in your terminal to authenticate, then let me know when you're done." Do not run these — they require interactive input.

Once all checks pass, proceed to Phase 2 without waiting for the user to say "continue".

### Phase 2 — Configuration Questions

Ask all questions in a single conversational message. Do not ask one at a time.

1. **AWS region** — e.g., `us-east-1`, `eu-central-1`. Default: `us-east-1`
2. **EKS cluster name** — Default: `phase-eks-cluster`. Do they have an existing cluster to reuse?
3. **Domain name** — The FQDN where Phase Console will be accessible (e.g., `phase.example.com`). Required.
4. **Email for Let's Encrypt** — Used for certificate expiry notifications.
5. **SSO provider** — Which identity provider to use for login:
   - `google` — Google OAuth 2.0
   - `github` — GitHub OAuth 2.0
   - `gitlab` — GitLab OAuth 2.0
   - `google-oidc`, `jumpcloud-oidc`, `entra-id-oidc`, `okta-oidc` — OIDC providers
   - `authentik` — Authentik OAuth 2.0
   - `github-enterprise` — GitHub Enterprise
6. **Database mode**:
   - **In-cluster** (default) — PostgreSQL and Redis inside the cluster on EBS. Simpler, suitable for dev/small deployments.
   - **External (RDS + ElastiCache)** — Managed AWS databases. Recommended for production.
7. **AWS Secrets Manager integration** — Will Phase need to sync secrets to AWS Secrets Manager? (yes/no)
8. **SMTP / email notifications** — Does the user have an existing SMTP gateway for Phase email notifications (invites, alerts)?
   - If **yes**: ask for SMTP host, port, sender address, and username. Tell them the password will be added to the secret script — do not ask for it in chat.
   - If **no**: offer to provision AWS SES SMTP credentials automatically. If they accept, the agent will create everything and inject the password into the secret.
9. **Phase Enterprise license** — Do they have a Phase Enterprise license key? If yes, ask them to paste it here.

Store all answers. Proceed to Phase 3 once answered.

### Phase 3 — Credential Setup

#### SSO OAuth Application

Tell the user the exact callback URL to register when creating their OAuth app:

- Pattern: `https://{domain}/api/auth/callback/{provider_slug}`
- Examples: `/callback/google`, `/callback/github`, `/callback/gitlab` — see `refs/eks-deployment.md` for all providers

Tell them where to create the OAuth app (Google Cloud Console, GitHub Settings > Developer settings > OAuth Apps, etc.) and ask them to share their **Client ID** (not secret — safe to share in chat) once created.

#### Secret Script

Once you have the Client ID, write `create-secret.sh`. Use no unnecessary leading indentation on `--from-literal` lines. Mark every value the user must supply with an `# EDIT_ME` comment on the same line.

**For in-cluster databases:**

```bash
#!/bin/bash
kubectl create secret generic phase-console-secret \
--from-literal=NEXTAUTH_SECRET=$(openssl rand -hex 32) \
--from-literal=SECRET_KEY=$(openssl rand -hex 32) \
--from-literal=SERVER_SECRET=$(openssl rand -hex 32) \
--from-literal=DATABASE_PASSWORD=$(openssl rand -hex 32) \
--from-literal=REDIS_PASSWORD=$(openssl rand -hex 32) \
--from-literal={SSO_CLIENT_ID_KEY}={client_id_value} \
--from-literal={SSO_CLIENT_SECRET_KEY}=EDIT_ME_CLIENT_SECRET # EDIT_ME: your {Provider} OAuth Client Secret
```

**For external databases (RDS + ElastiCache):**

```bash
#!/bin/bash
kubectl create secret generic phase-console-secret \
--from-literal=NEXTAUTH_SECRET=$(openssl rand -hex 32) \
--from-literal=SECRET_KEY=$(openssl rand -hex 32) \
--from-literal=SERVER_SECRET=$(openssl rand -hex 32) \
--from-literal=DATABASE_PASSWORD=$(openssl rand -hex 32) \
--from-literal=REDIS_PASSWORD=$(openssl rand -hex 32) \
--from-literal={SSO_CLIENT_ID_KEY}={client_id_value} \
--from-literal={SSO_CLIENT_SECRET_KEY}=EDIT_ME_CLIENT_SECRET # EDIT_ME: your {Provider} OAuth Client Secret
```

For external databases, `DATABASE_PASSWORD` and `REDIS_PASSWORD` are auto-generated here. The agent reads them back from the secret after it's created and uses them when provisioning RDS and ElastiCache — the user never needs to see or manage those passwords.

If the user provided SMTP credentials, append:

```bash
--from-literal=EMAIL_HOST_PASSWORD=EDIT_ME_SMTP_PASSWORD # EDIT_ME: your SMTP password
```

If using SES-provisioned SMTP, leave this line out — the agent will patch the secret after generating credentials.

If the user has an Enterprise license key, append:

```bash
--from-literal=LICENSE_KEY={license_key_value}
```

Substitute `{SSO_CLIENT_ID_KEY}`, `{SSO_CLIENT_SECRET_KEY}`, and `{client_id_value}` with the actual values from the SSO table in `refs/eks-deployment.md`. Add any extra variables required by the provider (e.g., `AUTHENTIK_URL`, `OKTA_OIDC_ISSUER`) — see "Additional SSO Provider Variables" in references.

Write the file and `chmod +x create-secret.sh`. Tell the user: "Edit the `# EDIT_ME` lines in `create-secret.sh`, then run it after the cluster is up — I'll let you know exactly when."

### Phase 4 — Infrastructure Provisioning

#### 4a. EKS Cluster (skip if user has an existing cluster)

1. Generate `cluster-config.yaml` from the template in references, substituting the user's cluster name and region.
2. Show the file content as a preview, then write it.
3. Run the cluster creation directly — do not ask the user to run it:
   ```bash
   eksctl create cluster -f cluster-config.yaml
   ```
   This takes 15–20 minutes. The command blocks until complete — wait for it.
4. After it completes, verify kubectl connectivity:
   ```bash
   kubectl get pods -A
   ```
   If this fails with a connection error, update the kubeconfig and retry:
   ```bash
   aws eks update-kubeconfig --name {cluster_name} --region {region}
   kubectl get pods -A
   ```
   If still failing, consult `refs/troubleshooting.md`.
5. Once kubectl is confirmed working, tell the user: "Cluster is up and kubectl is connected. Now run `./create-secret.sh` (fill in the `# EDIT_ME` values first). Let me know when it's done."
6. Wait for the user to confirm the secret was created before proceeding.

#### 4b. cert-manager

Run automatically without asking:

```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.2/cert-manager.yaml
kubectl wait --for=condition=Ready pods -l app.kubernetes.io/instance=cert-manager -n cert-manager --timeout=120s
```

#### 4c. ClusterIssuer

Generate `cluster-issuer.yaml` from the template in references, substituting the user's email. Write and apply:

```
kubectl apply -f cluster-issuer.yaml
```

#### 4d. Databases

**If in-cluster:**

Generate `storage-class.yaml` from the template in references. Write and apply:

```
kubectl apply -f storage-class.yaml
```

**If external (RDS + ElastiCache):**

Run security group and subnet group setup automatically (see references). Tag all resources with `project=phase` and `cluster={cluster_name}`.

Note: eksctl clusters use subnets tagged with `kubernetes.io/role/internal-elb` for private subnets. Use this tag to filter them — do NOT rely on the CloudFormation logical ID pattern `SubnetPrivate*`, which may not match in all regions. Get IDs with:

```bash
SUBNET_IDS=$(aws ec2 describe-subnets \
  --filters "Name=vpc-id,Values=$VPC_ID" \
            "Name=tag:kubernetes.io/role/internal-elb,Values=1" \
  --query 'Subnets[*].SubnetId' --output text \
  --region {region} | tr '\t' ' ')
```

Then provision RDS and ElastiCache by reading passwords directly from the Kubernetes secret — no user involvement needed:

```bash
DB_PASSWORD=$(kubectl get secret phase-console-secret -o jsonpath='{.data.DATABASE_PASSWORD}' | base64 -d)
REDIS_PASSWORD=$(kubectl get secret phase-console-secret -o jsonpath='{.data.REDIS_PASSWORD}' | base64 -d)
```

Pass `$DB_PASSWORD` as `--master-user-password` for RDS and `$REDIS_PASSWORD` as `--auth-token` for ElastiCache. See references for the full commands.

Poll until both databases are `available`, checking every 60 seconds. Note the endpoint addresses for the values file.

**If provisioning SES SMTP:**

Run automatically — see references for full commands. After creating the IAM user and access key, compute the SES SMTP password and patch it into the secret:

```bash
kubectl patch secret phase-console-secret \
  --type merge \
  -p "{\"data\":{\"EMAIL_HOST_PASSWORD\":\"$(echo -n $SMTP_PASSWORD | base64)\"}}"
```

#### 4e. NGINX Ingress Controller

Run automatically (see references for full command):

```
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx --create-namespace ...
```

#### 4f. Get LoadBalancer Endpoint

Run automatically and report the result to the user:

```
kubectl get svc -n ingress-nginx ingress-nginx-controller \
  -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```

Extract and display the `EXTERNAL-IP` value.

### Phase 5 — Deployment

#### 5a. DNS Setup

Tell the user to point their domain to the LoadBalancer endpoint from step 4f:
- If EXTERNAL-IP is a **hostname** (typical for NLB): create a **CNAME** record
- If EXTERNAL-IP is an **IP address**: create an **A** record

Example:
```
phase.example.com  CNAME  abc123.elb.us-east-1.amazonaws.com
```

After the user confirms the DNS record is created, verify propagation using multiple resolvers before proceeding — DNS issues will cause cert-manager's ACME challenge to fail:

```bash
dig @8.8.8.8 {domain} +short        # Google
dig @1.1.1.1 {domain} +short        # Cloudflare
dig @9.9.9.9 {domain} +short        # Quad9
dig @208.67.222.222 {domain} +short  # OpenDNS
```

All four should return the NLB hostname or an IP. If results are inconsistent or returning NXDOMAIN, wait and retry — do not proceed until at least 3 of 4 resolvers agree. Tell the user that propagation can take minutes to hours depending on TTL and their registrar.

#### 5b. Add Phase Helm Repository

Run automatically. If a `phase` repo already exists pointing to a different URL, remove and re-add it:

```bash
helm repo remove phase 2>/dev/null || true
helm repo add phase https://helm.phase.dev
helm repo update
```

#### 5c. Generate Values File

Build `phase-values.yaml` from the appropriate template in references (in-cluster or external), substituting all collected values: domain, SSO provider, RDS/ElastiCache endpoints if external, SMTP settings if configured, replica counts, etc. Write the file without showing a preview — proceed directly.

#### 5d. Install Phase

Run automatically:

```bash
helm install phase-console phase/phase -f phase-values.yaml
```

#### 5e. Enable Proxy Protocol (Client IP Forwarding)

Run automatically after installation:

```bash
helm upgrade ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.publishService.enabled=true \
  --set controller.service.type=LoadBalancer \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-scheme"=internet-facing \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-target-group-attributes"="proxy_protocol_v2.enabled=true" \
  --set controller.config.use-proxy-protocol="true"
```

See `refs/troubleshooting.md` for proxy protocol pitfalls.

### Phase 6 — Verification

Run all checks automatically and report results:

1. `kubectl get pods -A` — Phase pods (default ns) and ingress-nginx pods should be Running
2. `kubectl get ingress` — should show the domain with an address
3. `kubectl get certificate` — should show `True` for READY

If the certificate is not ready, check DNS propagation and cert-manager logs. Consult `refs/troubleshooting.md` for common issues and fixes.

Once everything is healthy, tell the user: "Your Phase Console is ready at `https://{domain}`."

### Phase 7 — AWS Secrets Manager Integration (IRSA)

Skip this phase if the user answered "no" to the AWS Secrets Manager question in Phase 2.

1. Write `phase-policy.json` with the Secrets Manager IAM policy from references.
2. Run automatically:
   ```bash
   aws iam create-policy \
     --policy-name PhaseConsolePolicy \
     --policy-document file://phase-policy.json \
     --tags Key=project,Value=phase Key=cluster,Value={cluster_name}
   ```
   Note the returned ARN.
3. Run automatically:
   ```bash
   eksctl create iamserviceaccount \
     --name phase-backend-sa \
     --namespace default \
     --cluster {cluster_name} \
     --attach-policy-arn {policy_arn} \
     --approve \
     --region {region}
   ```
4. Get the IAM role ARN from the service account annotation:
   ```bash
   kubectl get serviceaccount phase-backend-sa \
     -o jsonpath='{.metadata.annotations.eks\.amazonaws\.com/role-arn}'
   ```
5. Add the `serviceAccount` block to `phase-values.yaml` (see references) and upgrade:
   ```bash
   helm upgrade phase-console phase/phase -f phase-values.yaml
   ```
6. Confirm: "Phase will now use the IAM role automatically — no AWS credentials need to be configured in the application."

## Post-Deployment Notes

- **Upgrading:** `helm repo update && helm upgrade phase-console phase/phase -f phase-values.yaml`
- **Uninstalling:** `helm uninstall phase-console` (PVCs and external databases must be cleaned up separately)
