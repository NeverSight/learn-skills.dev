---
name: configure-ingress-networking
description: >
  Configure Kubernetes Ingress networking with NGINX Ingress Controller, cert-manager
  for automated TLS certificate management, path-based routing, rate limiting, and
  multi-domain hosting with SSL termination and load balancing. Use when exposing multiple
  Kubernetes services via a single load balancer, implementing path-based or host-based
  routing, automating TLS certificate issuance with Let's Encrypt, or setting up blue-green
  and canary deployments with traffic splitting.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: devops
  complexity: intermediate
  language: multi
  tags: ingress, nginx, cert-manager, tls, networking
---

# Configure Ingress Networking

Set up production-grade Kubernetes Ingress with NGINX controller, automated TLS certificates, and advanced routing capabilities.

## When to Use

- Exposing multiple Kubernetes services via single load balancer
- Implementing path-based or host-based routing for microservices
- Automating TLS certificate issuance and renewal with Let's Encrypt
- Implementing rate limiting, authentication, and WAF policies
- Setting up blue-green or canary deployments with traffic splitting
- Configuring custom error pages and request/response modification

## Inputs

- **Required**: Kubernetes cluster with LoadBalancer support or MetalLB
- **Required**: DNS records pointing to cluster LoadBalancer IP
- **Optional**: Existing TLS certificates or Let's Encrypt account
- **Optional**: OAuth2 provider for authentication
- **Optional**: WAF rules (ModSecurity)
- **Optional**: Prometheus for metrics collection

## Procedure

> See [Extended Examples](references/EXAMPLES.md) for complete configuration files and templates.


### Step 1: Install NGINX Ingress Controller

Deploy NGINX Ingress Controller with Helm and configure cloud provider integration.

```bash
# Add NGINX Ingress Helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

# Create namespace
kubectl create namespace ingress-nginx

# Install for cloud providers (AWS, GCP, Azure)
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.service.type=LoadBalancer \
  --set controller.metrics.enabled=true \
  --set controller.metrics.serviceMonitor.enabled=true \
  --set controller.podAnnotations."prometheus\.io/scrape"=true \
  --set controller.podAnnotations."prometheus\.io/port"=10254

# Or install for bare-metal with NodePort
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.service.type=NodePort \
  --set controller.service.nodePorts.http=30080 \
  --set controller.service.nodePorts.https=30443

# AWS-specific configuration with NLB
helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-type"=nlb \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-backend-protocol"=tcp \
  --set controller.service.annotations."service\.beta\.kubernetes\.io/aws-load-balancer-cross-zone-load-balancing-enabled"=true

# Verify installation
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx

# Wait for LoadBalancer external IP
kubectl get svc ingress-nginx-controller -n ingress-nginx -w

# Get external IP/hostname
INGRESS_IP=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
INGRESS_HOST=$(kubectl get svc ingress-nginx-controller -n ingress-nginx -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "Ingress IP: $INGRESS_IP"
echo "Ingress Hostname: $INGRESS_HOST"

# Test controller
curl http://$INGRESS_IP
# Should return 404 (no backend configured yet)
```

**Expected:** NGINX Ingress Controller pods running in ingress-nginx namespace. LoadBalancer service has external IP assigned. Metrics endpoint accessible on port 10254. Health check at `/healthz` returns 200 OK.

**On failure:** For pending LoadBalancer, verify cloud provider integration and service quotas. For CrashLoopBackOff, check controller logs with `kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller`. For webhook errors, verify admission webhook certificate is valid. For no external IP on bare-metal, install MetalLB or use NodePort service type.

### Step 2: Install cert-manager for Automated TLS

Deploy cert-manager and configure Let's Encrypt ClusterIssuer.

```bash
# Install cert-manager CRDs
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.crds.yaml

# Add cert-manager Helm repository
helm repo add jetstack https://charts.jetstack.io
helm repo update

# Install cert-manager
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.13.0 \
  --set prometheus.enabled=true \
  --set webhook.timeoutSeconds=30

# Verify installation
kubectl get pods -n cert-manager
kubectl get apiservice v1beta1.webhook.cert-manager.io -o yaml

# Create Let's Encrypt staging issuer (for testing)
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-staging
spec:
  acme:
    server: https://acme-staging-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-staging-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Create Let's Encrypt production issuer
cat <<EOF | kubectl apply -f -
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@example.com
    privateKeySecretRef:
      name: letsencrypt-prod-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
    - dns01:
        route53:
          region: us-east-1
          hostedZoneID: Z1234567890ABC
          # IAM role for EKS with IRSA
          role: arn:aws:iam::123456789012:role/cert-manager
EOF

# Verify ClusterIssuer ready
kubectl get clusterissuer
kubectl describe clusterissuer letsencrypt-prod
```

**Expected:** cert-manager pods running in cert-manager namespace. ClusterIssuers created with Ready status. ACME account registered with Let's Encrypt. Webhook responding to certificate requests.

**On failure:** For webhook timeout errors, increase `webhook.timeoutSeconds` or check network policies blocking cert-manager to API server. For ACME registration failures, verify email is valid and server URL correct. For DNS01 failures, check Route53 IAM permissions allow route53:ChangeResourceRecordSets. Test DNS propagation with `dig +short _acme-challenge.example.com TXT`.

### Step 3: Create Basic Ingress with TLS

Deploy application and expose via Ingress with automatic certificate issuance.

```bash
# Deploy sample application
kubectl create deployment web --image=nginx:alpine
kubectl expose deployment web --port=80 --target-port=80

# Create Ingress resource with TLS
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-staging"  # Use staging for testing
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - web.example.com
    secretName: web-tls-secret  # cert-manager will create this
  rules:
  - host: web.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 80
EOF

# Watch certificate creation
kubectl get certificate -w
kubectl describe certificate web-tls-secret

# Verify certificate issued
kubectl get secret web-tls-secret
kubectl get secret web-tls-secret -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout

# Check cert-manager logs if issues
kubectl logs -n cert-manager -l app=cert-manager -f

# Test HTTP to HTTPS redirect
curl -I http://web.example.com
# Should return 308 Permanent Redirect to https://

# Test HTTPS
curl -v https://web.example.com
# Should return 200 OK with valid certificate

# Once tested successfully, switch to production issuer
kubectl patch ingress web-ingress -p '{"metadata":{"annotations":{"cert-manager.io/cluster-issuer":"letsencrypt-prod"}}}'
kubectl delete certificate web-tls-secret
kubectl delete secret web-tls-secret
# cert-manager will recreate with production certificate
```

**Expected:** Ingress resource created. cert-manager detects annotation and creates Certificate resource. HTTP-01 challenge completes successfully. TLS secret created with valid certificate. HTTPS requests succeed with trusted certificate. HTTP redirects to HTTPS.

**On failure:** For challenge failures, verify DNS resolves to Ingress LoadBalancer IP with `dig web.example.com`. For rate limit errors, use staging issuer until configuration correct. For certificate not issued, check events with `kubectl describe certificate web-tls-secret` and `kubectl get challenges`. For "too many certificates" error, hit Let's Encrypt rate limits (50 certs/domain/week); wait or use staging.

### Step 4: Implement Advanced Routing and Load Balancing

Configure path-based routing, header-based routing, and traffic splitting.

```bash
# Deploy multiple services
kubectl create deployment api --image=hashicorp/http-echo --replicas=3 -- -text="API Service"
kubectl create deployment admin --image=hashicorp/http-echo --replicas=2 -- -text="Admin Service"
kubectl expose deployment api --port=5678
kubectl expose deployment admin --port=5678

# Create Ingress with path-based routing
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rewrite-target: /\$2
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - app.example.com
    secretName: app-tls
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port:
              number: 80
      - path: /api(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: api
            port:
              number: 5678
      - path: /admin(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: admin
            port:
              number: 5678
EOF

# Canary deployment with traffic splitting
kubectl create deployment api-v2 --image=hashicorp/http-echo -- -text="API Service v2"
kubectl expose deployment api-v2 --port=5678

cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "20"  # 20% traffic to v2
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-v2
            port:
              number: 5678
EOF

# Header-based canary routing (for testing)
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-canary-header
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-by-header: "X-Canary"
    nginx.ingress.kubernetes.io/canary-by-header-value: "always"
spec:
  ingressClassName: nginx
  rules:
  - host: app.example.com
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: api-v2
            port:
              number: 5678
EOF

# Test routing
curl https://app.example.com/            # -> web service
curl https://app.example.com/api/        # -> 80% api, 20% api-v2
curl https://app.example.com/admin/      # -> admin service
curl -H "X-Canary: always" https://app.example.com/api/  # -> api-v2 (100%)
```

**Expected:** Single Ingress routes to multiple services based on path. Rewrite-target strips path prefix. Canary Ingress splits traffic by weight. Header-based routing sends specific requests to canary. TLS terminates at Ingress, backends use HTTP.

**On failure:** For 404 errors, verify service names and ports match. For rewrite issues, test regex with `nginx.ingress.kubernetes.io/rewrite-target` debugger. For canary not working, verify only one Ingress has `canary: "false"` (main) and others have `canary: "true"`. For traffic imbalance, check backend pod counts and readiness probes.

### Step 5: Configure Rate Limiting and Authentication

Implement rate limiting, basic auth, and OAuth2 authentication.

```bash
# Rate limiting by IP
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ratelimit
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Rate limiting blocks excessive requests with 503 Service Temporarily Unavailable. Basic auth prompts for credentials, rejects unauthorized requests. OAuth2 redirects to provider login page, sets authentication cookies.

**On failure:** For rate limit not working, verify annotation syntax and restart Ingress controller pods. For basic auth 500 errors, check secret format with `kubectl get secret basic-auth -o yaml | grep auth:`. For OAuth2 failures, verify client ID/secret and callback URL registered with provider. Check oauth2-proxy logs for detailed errors.

### Step 6: Implement Custom Error Pages and Request Modification

Configure custom error pages, CORS, and request/response headers.

```bash
# Create ConfigMap with custom error pages
kubectl create configmap custom-errors --from-file=404.html --from-file=503.html -n ingress-nginx

# Configure NGINX to use custom error pages
cat <<EOF | kubectl apply -f -
apiVersion: v1
# ... (see EXAMPLES.md for complete configuration)
```

**Expected:** Custom 404 and 503 pages display instead of default NGINX pages. CORS headers allow specified origins and methods. Security headers protect against XSS and clickjacking. Request body size limit allows large file uploads. Timeout settings prevent premature connection closes.

**On failure:** For custom error pages not showing, verify ConfigMap mounted to controller pods and default backend deployed. For CORS preflight failures, check OPTIONS requests allowed in backend service. For 413 Request Entity Too Large, increase `proxy-body-size` annotation. For timeout errors, increase all three timeout annotations together.

## Validation

- [ ] NGINX Ingress Controller running with external IP assigned
- [ ] cert-manager issues certificates automatically via Let's Encrypt
- [ ] HTTPS redirects enforce SSL for all Ingresses
- [ ] Path-based routing directs requests to correct backend services
- [ ] Canary Ingresses split traffic according to weight annotations
- [ ] Rate limiting blocks excessive requests from single IP
- [ ] Authentication (basic auth or OAuth2) protects admin routes
- [ ] Custom error pages display on 404/503 errors
- [ ] CORS headers allow cross-origin requests from specified domains
- [ ] Metrics endpoint exposes Prometheus metrics for monitoring

## Common Pitfalls

- **No ingressClassName**: Ingress not picked up by controller. Always specify `ingressClassName: nginx` in Kubernetes 1.19+.

- **Certificate challenges fail**: DNS doesn't point to Ingress LoadBalancer. Verify with `dig yourdomain.com` before requesting certificate.

- **HTTP-01 challenge timeout**: Firewall blocks port 80. Let's Encrypt must reach `http://domain/.well-known/acme-challenge/` for validation.

- **Rate limit applies globally**: `limit-rps` annotation applies per Ingress, not per path. Create separate Ingresses for different rate limits.

- **Rewrite-target regex wrong**: Captures don't match path pattern. Test with `echo "/api/users" | sed 's|/api(/\|$)\(.*\)|/\2|'`.

- **Canary weight ignored**: Multiple canary Ingresses for same host/path conflict. Only create one canary Ingress per route.

- **Auth bypass via IP**: Authentication only on Ingress, backend services accessible via ClusterIP. Implement network policies or service mesh.

- **Configuration-snippet injection risk**: User input in configuration-snippet allows NGINX config injection. Validate and sanitize all annotations.

## Related Skills

- `deploy-to-kubernetes` - Creating Services that Ingress routes to
- `manage-kubernetes-secrets` - Managing TLS certificates as Secrets
- `implement-gitops-workflow` - Declarative Ingress management with Argo CD
- `setup-service-mesh` - Advanced traffic management with Istio/Linkerd
- `build-ci-cd-pipeline` - Automated Ingress updates in CI/CD
