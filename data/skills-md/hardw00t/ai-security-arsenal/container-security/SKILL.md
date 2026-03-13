---
name: container-security
description: "Container and Kubernetes security assessment skill for Docker, Kubernetes, and container orchestration platforms. This skill should be used when scanning container images for vulnerabilities, auditing Kubernetes cluster security, testing container escape scenarios, reviewing Docker configurations, or performing container runtime security analysis. Triggers on requests to scan Docker images, audit Kubernetes security, test container configurations, or assess container orchestration security."
---

# Container Security Assessment

This skill enables comprehensive security testing of containerized environments including Docker image scanning, Kubernetes cluster security auditing, container runtime analysis, and orchestration security assessment using tools like Trivy, Grype, Kubescape, kube-bench, and Falco.

## When to Use This Skill

This skill should be invoked when:
- Scanning Docker/OCI images for vulnerabilities
- Auditing Kubernetes cluster security posture
- Testing container runtime configurations
- Reviewing Dockerfile security practices
- Checking CIS benchmarks for Docker/Kubernetes
- Analyzing container escape possibilities
- Implementing container security monitoring

### Trigger Phrases
- "scan this Docker image for vulnerabilities"
- "audit Kubernetes cluster security"
- "check container configuration"
- "test container escape"
- "review Dockerfile security"
- "run kube-bench"

---

## Prerequisites

### Required Tools

| Tool | Purpose | Installation |
|------|---------|--------------|
| Trivy | Image/IaC vulnerability scanner | `brew install trivy` |
| Grype | Image vulnerability scanner | `brew install grype` |
| Syft | SBOM generator | `brew install syft` |
| Kubescape | K8s security platform | `curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh \| /bin/bash` |
| kube-bench | CIS K8s benchmark | `brew install kube-bench` |
| kube-hunter | K8s penetration testing | `pip install kube-hunter` |
| Falco | Runtime security | Helm chart or binary |
| Docker Bench | Docker CIS benchmark | `git clone https://github.com/docker/docker-bench-security.git` |

---

## Container Image Security

### Trivy Image Scanning

```bash
# Scan image from registry
trivy image nginx:latest

# Scan local image
trivy image --input ./image.tar

# Filter by severity
trivy image --severity HIGH,CRITICAL nginx:latest

# Output formats
trivy image -f json -o results.json nginx:latest
trivy image -f sarif -o results.sarif nginx:latest
trivy image -f table nginx:latest

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed nginx:latest

# Scan specific vulnerability types
trivy image --vuln-type os,library nginx:latest

# With SBOM
trivy image --format cyclonedx nginx:latest > sbom.json

# Exit code on findings
trivy image --exit-code 1 --severity CRITICAL nginx:latest

# Scan filesystem (for built images)
trivy fs --security-checks vuln,secret,config /path/to/project
```

### Grype Scanning

```bash
# Scan image
grype nginx:latest

# Output formats
grype nginx:latest -o json > grype.json
grype nginx:latest -o table
grype nginx:latest -o cyclonedx > sbom.xml

# Fail on severity
grype nginx:latest --fail-on high

# Scan SBOM
syft nginx:latest -o json > sbom.json
grype sbom:./sbom.json

# Scan local directory
grype dir:/path/to/project

# Scan tarball
grype docker-archive:./image.tar
```

### SBOM Generation with Syft

```bash
# Generate SBOM
syft nginx:latest

# Output formats
syft nginx:latest -o json > sbom.json
syft nginx:latest -o cyclonedx-json > sbom-cyclonedx.json
syft nginx:latest -o spdx-json > sbom-spdx.json

# Scan filesystem
syft dir:/app

# Include file metadata
syft nginx:latest -o json --file-metadata
```

### Image Analysis Checklist

```markdown
### Base Image
- [ ] Official/verified base image
- [ ] Minimal base (alpine, distroless, scratch)
- [ ] Pinned version (no :latest)
- [ ] Recently updated
- [ ] Known CVE status

### Vulnerabilities
- [ ] No CRITICAL vulnerabilities
- [ ] HIGH vulnerabilities remediated or accepted
- [ ] OS packages updated
- [ ] Application dependencies current

### Secrets
- [ ] No hardcoded credentials
- [ ] No API keys in layers
- [ ] No private keys
- [ ] Environment variables reviewed

### Configuration
- [ ] Non-root user defined
- [ ] Read-only filesystem where possible
- [ ] Minimal capabilities
- [ ] No unnecessary packages
```

---

## Dockerfile Security

### Dockerfile Best Practices

```dockerfile
# Use specific version, not latest
FROM python:3.11-slim-bookworm

# Set labels for tracking
LABEL maintainer="security@company.com" \
      version="1.0" \
      description="Secure application container"

# Create non-root user early
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Set working directory
WORKDIR /app

# Copy dependency files first (layer caching)
COPY requirements.txt .

# Install dependencies with no cache, minimal packages
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        package1 \
        package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY --chown=appuser:appgroup . .

# Remove unnecessary files
RUN rm -rf tests/ docs/ *.md

# Switch to non-root user
USER appuser

# Set read-only where possible
# Use HEALTHCHECK
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Expose only necessary ports
EXPOSE 8080

# Use exec form for signals
ENTRYPOINT ["python", "app.py"]
```

### Dockerfile Linting with Hadolint

```bash
# Install
brew install hadolint

# Lint Dockerfile
hadolint Dockerfile

# Ignore specific rules
hadolint --ignore DL3008 --ignore DL3009 Dockerfile

# Output formats
hadolint -f json Dockerfile > hadolint.json
hadolint -f sarif Dockerfile > hadolint.sarif

# Strict mode
hadolint --strict Dockerfile
```

### Dockerfile Security Checklist

```markdown
### User & Permissions
- [ ] USER instruction present (non-root)
- [ ] Files owned by non-root user (COPY --chown)
- [ ] No sudo/su usage
- [ ] Minimal file permissions

### Base Image
- [ ] Official/trusted base image
- [ ] Pinned digest or specific version
- [ ] Minimal base (alpine, slim, distroless)
- [ ] Multi-stage build for smaller image

### Package Management
- [ ] Package versions pinned
- [ ] Package cache cleaned (rm -rf /var/lib/apt/lists/*)
- [ ] --no-install-recommends used
- [ ] pip --no-cache-dir used

### Secrets
- [ ] No secrets in build args
- [ ] No secrets COPY'd into image
- [ ] .dockerignore excludes secrets
- [ ] Multi-stage build hides build secrets

### Network
- [ ] Only required ports EXPOSE'd
- [ ] No SSH server installed
- [ ] No unnecessary network tools

### Runtime
- [ ] HEALTHCHECK defined
- [ ] Exec form for ENTRYPOINT/CMD
- [ ] Signal handling correct
- [ ] Logging to stdout/stderr
```

---

## Kubernetes Cluster Security

### Kubescape Assessment

```bash
# Full cluster scan
kubescape scan

# Scan with specific framework
kubescape scan framework nsa
kubescape scan framework mitre
kubescape scan framework cis-v1.23-t1.0.1

# Scan specific namespace
kubescape scan --include-namespaces production

# Scan manifest files
kubescape scan *.yaml

# Output formats
kubescape scan -f json -o results.json
kubescape scan -f sarif -o results.sarif

# Compliance score threshold
kubescape scan --compliance-threshold 80

# Exception handling
kubescape scan --exceptions exceptions.json

# List available frameworks
kubescape list frameworks
```

### kube-bench CIS Benchmark

```bash
# Run all checks (run inside cluster)
kube-bench run

# Target specific component
kube-bench run --targets master
kube-bench run --targets node
kube-bench run --targets etcd
kube-bench run --targets policies

# Output formats
kube-bench run --json > kube-bench.json
kube-bench run --junit > kube-bench.xml

# Specific version
kube-bench run --version 1.27

# As Kubernetes job
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml
kubectl logs -l app=kube-bench
```

### kube-hunter Penetration Testing

```bash
# Remote scanning
kube-hunter --remote <cluster-ip>

# Pod scanning (run as pod in cluster)
kube-hunter --pod

# Active hunting (exploitation attempts)
kube-hunter --active

# Report formats
kube-hunter --report json > kube-hunter.json
kube-hunter --report yaml > kube-hunter.yaml

# Interface mode
kube-hunter --interface

# Specific CIDR
kube-hunter --cidr 10.0.0.0/8
```

### Kubernetes Security Checklist

```markdown
### Control Plane
- [ ] API server authentication enabled
- [ ] RBAC enabled (no ABAC)
- [ ] Admission controllers configured
- [ ] Audit logging enabled
- [ ] etcd encrypted and authenticated
- [ ] API server TLS configured

### Node Security
- [ ] Nodes hardened (CIS benchmark)
- [ ] kubelet authentication enabled
- [ ] kubelet authorization not AlwaysAllow
- [ ] Read-only port disabled (10255)
- [ ] Container runtime hardened

### Network
- [ ] Network policies enforced
- [ ] Pod-to-pod encryption (service mesh)
- [ ] Ingress TLS configured
- [ ] External access restricted
- [ ] Egress policies defined

### Workload Security
- [ ] Pod Security Standards enforced
- [ ] No privileged containers
- [ ] Read-only root filesystem
- [ ] Resource limits set
- [ ] Service account tokens managed

### RBAC
- [ ] Least privilege roles
- [ ] No cluster-admin for workloads
- [ ] Service accounts per workload
- [ ] Regular access review
```

---

## Docker Host Security

### Docker Bench for Security

```bash
# Clone and run
git clone https://github.com/docker/docker-bench-security.git
cd docker-bench-security
sudo sh docker-bench-security.sh

# With specific checks
sudo sh docker-bench-security.sh -c container_images

# Output to file
sudo sh docker-bench-security.sh -l /tmp/docker-bench.log

# JSON output
sudo sh docker-bench-security.sh -j > docker-bench.json
```

### Docker Daemon Configuration

```json
// /etc/docker/daemon.json
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "seccomp-profile": "/etc/docker/seccomp-profile.json",
  "storage-driver": "overlay2",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "live-restore": true,
  "userland-proxy": false,
  "tls": true,
  "tlscacert": "/etc/docker/ca.pem",
  "tlscert": "/etc/docker/server-cert.pem",
  "tlskey": "/etc/docker/server-key.pem",
  "tlsverify": true
}
```

### Docker Security Checklist

```markdown
### Daemon
- [ ] TLS enabled for remote access
- [ ] User namespaces enabled
- [ ] Live restore enabled
- [ ] Default ulimits configured
- [ ] Inter-container communication disabled
- [ ] Content trust enabled (DOCKER_CONTENT_TRUST=1)

### Images
- [ ] Base images from trusted registries
- [ ] Image signing verified
- [ ] Vulnerability scanning in place
- [ ] No secrets in image layers

### Containers
- [ ] Non-root user
- [ ] Read-only root filesystem
- [ ] No privileged containers
- [ ] Capabilities dropped
- [ ] Seccomp profile applied
- [ ] AppArmor/SELinux enabled
- [ ] Resource limits set
- [ ] Health checks defined

### Network
- [ ] User-defined networks (not default bridge)
- [ ] No --network=host
- [ ] Port mapping minimal
- [ ] Sensitive ports protected

### Storage
- [ ] No sensitive host mounts
- [ ] Read-only mounts where possible
- [ ] No /var/run/docker.sock mount
- [ ] Volume driver security reviewed
```

---

## Container Runtime Security

### Falco Runtime Monitoring

```bash
# Install via Helm
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --set driver.kind=modern_ebpf \
  --set tty=true

# View alerts
kubectl logs -l app.kubernetes.io/name=falco -f

# Custom rules
# /etc/falco/rules.d/custom_rules.yaml
```

### Falco Custom Rules

```yaml
# custom_rules.yaml
- rule: Shell Spawned in Container
  desc: Detect shell spawned in container
  condition: >
    spawned_process and
    container and
    proc.name in (bash, sh, zsh, ksh, csh)
  output: >
    Shell spawned in container
    (user=%user.name command=%proc.cmdline container=%container.name
     image=%container.image.repository)
  priority: WARNING
  tags: [container, shell]

- rule: Sensitive File Access
  desc: Detect access to sensitive files
  condition: >
    open_read and
    container and
    fd.name pmatch (/etc/shadow, /etc/passwd, /etc/kubernetes/*)
  output: >
    Sensitive file accessed
    (user=%user.name file=%fd.name container=%container.name)
  priority: CRITICAL
  tags: [container, filesystem]

- rule: Unexpected Outbound Connection
  desc: Detect outbound connections from container
  condition: >
    outbound and
    container and
    not (fd.sip.name in (allowed.destinations))
  output: >
    Unexpected outbound connection
    (container=%container.name dest=%fd.sip.name port=%fd.sport)
  priority: WARNING
  tags: [container, network]

- rule: Container Escape Attempt
  desc: Detect potential container escape
  condition: >
    container and
    (evt.type in (ptrace, process_vm_readv, process_vm_writev) or
     fd.name startswith /proc/1/ or
     fd.name = /proc/sys/kernel/core_pattern)
  output: >
    Potential container escape attempt
    (user=%user.name command=%proc.cmdline container=%container.name)
  priority: CRITICAL
  tags: [container, escape]
```

### Seccomp Profiles

```json
// seccomp-profile.json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {
      "names": [
        "read", "write", "open", "close", "stat", "fstat",
        "mmap", "mprotect", "munmap", "brk", "ioctl",
        "access", "pipe", "select", "sched_yield",
        "dup", "dup2", "clone", "fork", "vfork",
        "execve", "exit", "wait4", "kill", "uname",
        "getcwd", "chdir", "getpid", "getuid", "getgid",
        "socket", "connect", "accept", "bind", "listen",
        "sendto", "recvfrom", "shutdown",
        "openat", "readlinkat", "newfstatat"
      ],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

---

## Container Escape Testing

### Common Escape Vectors

```markdown
### Privileged Container
```bash
# Check if privileged
cat /proc/self/status | grep CapEff
# CapEff: 0000003fffffffff = privileged

# Mount host filesystem
mkdir /mnt/host
mount /dev/sda1 /mnt/host
chroot /mnt/host
```

### Docker Socket Mount
```bash
# If /var/run/docker.sock is mounted
docker -H unix:///var/run/docker.sock run -v /:/host -it alpine chroot /host
```

### Kernel Exploits
- Check kernel version: uname -a
- Search for container escape CVEs
- CVE-2022-0185 (fsconfig)
- CVE-2022-0847 (Dirty Pipe)
- CVE-2020-15257 (containerd)

### Capabilities Abuse
```bash
# Check capabilities
capsh --print

# CAP_SYS_ADMIN - mount filesystems
# CAP_NET_ADMIN - network manipulation
# CAP_DAC_OVERRIDE - file permission bypass
```
```

### Escape Prevention Checklist

```markdown
- [ ] No privileged containers
- [ ] Capabilities dropped (--cap-drop=ALL)
- [ ] Only necessary capabilities added
- [ ] No Docker socket mount
- [ ] No host PID/network namespace
- [ ] Seccomp profile enabled
- [ ] AppArmor/SELinux enforcing
- [ ] User namespaces enabled
- [ ] Kernel patched and updated
- [ ] read-only root filesystem
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Container Security

on:
  push:
    branches: [main]
  pull_request:

jobs:
  trivy-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  grype-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t myapp:${{ github.sha }} .

      - name: Scan image with Grype
        uses: anchore/scan-action@v3
        with:
          image: myapp:${{ github.sha }}
          fail-build: true
          severity-cutoff: high

  hadolint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Lint Dockerfile
        uses: hadolint/hadolint-action@v3.1.0
        with:
          dockerfile: Dockerfile
          failure-threshold: error
```

### Kubernetes Admission Control

```yaml
# Gatekeeper constraint for image scanning
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sImageDigests
metadata:
  name: require-image-digests
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces: ["production"]
  parameters:
    exemptImages:
      - "gcr.io/distroless/*"
```

---

## Reporting Template

```markdown
# Container Security Assessment Report

## Executive Summary
- Assessment date: YYYY-MM-DD
- Scope: X images, Y clusters
- Critical vulnerabilities: X
- High vulnerabilities: Y
- Compliance score: Z%

## Image Scan Results

### Image: nginx:1.25
| CVE ID | Severity | Package | Fixed Version |
|--------|----------|---------|---------------|
| CVE-2023-XXXX | CRITICAL | openssl | 3.0.12 |

### Image: app:latest
| CVE ID | Severity | Package | Fixed Version |
|--------|----------|---------|---------------|
| CVE-2023-YYYY | HIGH | python | 3.11.6 |

## Kubernetes Findings

### CIS Benchmark Results
| Section | Pass | Fail | Score |
|---------|------|------|-------|
| Control Plane | 10 | 2 | 83% |
| Worker Nodes | 8 | 1 | 89% |
| Policies | 5 | 3 | 62% |

### Critical Findings
1. [CRITICAL] Privileged containers in production namespace
2. [HIGH] Missing network policies
3. [HIGH] Default service account used

## Recommendations
1. Update base images to patched versions
2. Implement Pod Security Standards
3. Enable network policies
4. Configure runtime monitoring with Falco
```

---

## Bundled Resources

### scripts/
- `scan_images.sh` - Batch image scanning automation
- `k8s_audit.sh` - Kubernetes security audit script
- `docker_bench_parser.py` - Parse Docker Bench results

### references/
- `escape_techniques.md` - Container escape methodology
- `cis_docker.md` - CIS Docker benchmark summary
- `cis_kubernetes.md` - CIS Kubernetes benchmark summary

### checklists/
- `image_security.md` - Image security checklist
- `k8s_hardening.md` - Kubernetes hardening checklist
- `docker_hardening.md` - Docker daemon hardening checklist
