---
name: xata-postgres-platform
description: Expert skill for Xata open-source cloud-native Postgres platform with copy-on-write branching, scale-to-zero, and Kubernetes deployment
triggers:
  - set up xata postgres platform
  - create postgres branch with copy on write
  - self-host xata on kubernetes
  - xata scale to zero postgres
  - xata cli project and branch management
  - deploy xata postgres platform locally
  - xata branching preview environments
  - xata tilt kind cluster setup
---

# Xata Postgres Platform

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Xata is an open-source, cloud-native Postgres platform built on Kubernetes that provides copy-on-write (CoW) branching, scale-to-zero, auto-scaling, high-availability, PITR backups, and a serverless SQL driver. It sits on top of [CloudNativePG](https://github.com/cloudnative-pg/cloudnative-pg) and [OpenEBS](https://github.com/openebs/openebs).

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Xata Platform                      │
│  CLI ──► REST API (clusters/projects services)       │
│  SQL Gateway (routing, scale-to-zero wakeup)         │
│  Branch Operator (manages K8s resources per branch)  │
│  Auth Service (Keycloak-based, RBAC API keys)        │
├─────────────────────────────────────────────────────┤
│  CloudNativePG (HA, failover, backups, pooling)      │
│  OpenEBS (local NVMe or Mayastor replicated storage) │
└─────────────────────────────────────────────────────┘
```

## Prerequisites

- Docker
- [Kind](https://github.com/kubernetes-sigs/kind)
- [Tilt](https://github.com/tilt-dev/tilt)
- `kubectl`

## Local Development Setup

### Step 1: Create Kind Cluster

```bash
kind create cluster --wait 10m
```

### Step 2: Deploy with Tilt

```bash
tilt up
```

Wait for all resources to become ready. First run downloads images and takes longer; subsequent runs are fast.

### Step 3: Install and Authenticate the CLI

```bash
# Install Xata CLI
curl -fsSL https://xata.io/install.sh | bash

# Authenticate to local profile
# Default credentials: email=dev@xata.tech, password=Xata1234!
xata auth login --profile local --env local --force

# Switch to the local profile
xata auth switch local
```

### Step 4: Create Project and Branch

```bash
# Create a new project
xata project create --name my-project

# Create the main branch (done automatically with project)
# Create a child branch (CoW copy of parent)
xata branch create
```

## CLI Reference

### Authentication

```bash
# Login to Xata Cloud
xata auth login

# Login to self-hosted local instance
xata auth login --profile local --env local --force

# Switch between profiles
xata auth switch local
xata auth switch default

# List profiles
xata auth list
```

### Projects

```bash
# Create a project
xata project create --name my-project

# List projects
xata project list

# Get project details
xata project get <project-id>

# Delete a project
xata project delete <project-id>
```

### Branches

```bash
# Create a branch (CoW snapshot of parent, completes in seconds even for TB of data)
xata branch create

# Create a named branch from a specific parent
xata branch create --name feature-xyz --from main

# List branches
xata branch list

# Get branch details
xata branch get <branch-id>

# Delete a branch
xata branch delete <branch-id>
```

### Connecting to a Branch

```bash
# Get connection string for a branch
xata branch connection-string <branch-id>

# Connect via psql
psql "$(xata branch connection-string <branch-id>)"
```

## Configuration

### Environment Variables

```bash
# Xata API endpoint (for self-hosted)
export XATA_API_URL=http://localhost:8080

# API key for authentication
export XATA_API_KEY=your_api_key_here

# Default project ID
export XATA_PROJECT_ID=your_project_id
```

### API Key Management (RBAC)

```bash
# Create an API key with specific permissions
xata apikey create --name ci-key --role branch:read,branch:write

# List API keys
xata apikey list

# Revoke an API key
xata apikey delete <key-id>
```

## Serverless SQL Driver (SQL over HTTP/WebSockets)

Xata exposes a serverless driver for executing SQL over HTTP or WebSockets, useful for edge functions and environments without persistent TCP connections.

### HTTP SQL Query (Go)

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
)

type SQLRequest struct {
    Query  string `json:"query"`
    Params []any  `json:"params,omitempty"`
}

type SQLResponse struct {
    Records []map[string]any `json:"records"`
    Error   string           `json:"error,omitempty"`
}

func queryXata(query string, params ...any) (*SQLResponse, error) {
    apiURL := os.Getenv("XATA_API_URL")
    apiKey := os.Getenv("XATA_API_KEY")
    branchID := os.Getenv("XATA_BRANCH_ID")

    reqBody := SQLRequest{Query: query, Params: params}
    data, err := json.Marshal(reqBody)
    if err != nil {
        return nil, err
    }

    url := fmt.Sprintf("%s/branches/%s/sql", apiURL, branchID)
    req, err := http.NewRequest("POST", url, bytes.NewReader(data))
    if err != nil {
        return nil, err
    }
    req.Header.Set("Authorization", "Bearer "+apiKey)
    req.Header.Set("Content-Type", "application/json")

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var sqlResp SQLResponse
    if err := json.NewDecoder(resp.Body).Decode(&sqlResp); err != nil {
        return nil, err
    }
    return &sqlResp, nil
}

func main() {
    result, err := queryXata("SELECT id, name FROM users WHERE active = $1", true)
    if err != nil {
        panic(err)
    }
    for _, record := range result.Records {
        fmt.Printf("User: %v\n", record)
    }
}
```

### Direct Postgres Connection (Go)

```go
package main

import (
    "context"
    "fmt"
    "os"

    "github.com/jackc/pgx/v5"
)

func main() {
    connStr := os.Getenv("XATA_DATABASE_URL")
    // e.g. postgresql://user:pass@sql-gateway-host:5432/dbname

    conn, err := pgx.Connect(context.Background(), connStr)
    if err != nil {
        fmt.Fprintf(os.Stderr, "Unable to connect: %v\n", err)
        os.Exit(1)
    }
    defer conn.Close(context.Background())

    rows, err := conn.Query(context.Background(), "SELECT id, name FROM users LIMIT 10")
    if err != nil {
        panic(err)
    }
    defer rows.Close()

    for rows.Next() {
        var id int
        var name string
        if err := rows.Scan(&id, &name); err != nil {
            panic(err)
        }
        fmt.Printf("id=%d name=%s\n", id, name)
    }
}
```

## Common Patterns

### Preview Environment Workflow (CI/CD)

Create a per-PR branch for isolated testing, then destroy it after merge:

```bash
#!/usr/bin/env bash
# create-preview.sh
set -euo pipefail

PR_NUMBER="${1:?PR number required}"
BRANCH_NAME="pr-${PR_NUMBER}"

# Create a CoW branch from main (completes in seconds, even for TB of data)
BRANCH_ID=$(xata branch create --name "$BRANCH_NAME" --from main --output json | jq -r '.id')
echo "Created branch: $BRANCH_ID"

# Get connection string for tests
CONN_STR=$(xata branch connection-string "$BRANCH_ID")
echo "::set-output name=database_url::${CONN_STR}"
echo "::set-output name=branch_id::${BRANCH_ID}"
```

```bash
#!/usr/bin/env bash
# cleanup-preview.sh
BRANCH_ID="${1:?Branch ID required}"
xata branch delete "$BRANCH_ID"
echo "Deleted branch $BRANCH_ID"
```

### GitHub Actions Integration

```yaml
name: Preview Environment
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  create-preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Xata CLI
        run: curl -fsSL https://xata.io/install.sh | bash

      - name: Authenticate
        env:
          XATA_API_KEY: ${{ secrets.XATA_API_KEY }}
        run: xata auth login --api-key "$XATA_API_KEY"

      - name: Create Preview Branch
        id: branch
        run: |
          BRANCH_ID=$(xata branch create \
            --name "pr-${{ github.event.number }}" \
            --from main \
            --output json | jq -r '.id')
          echo "branch_id=$BRANCH_ID" >> "$GITHUB_OUTPUT"
          CONN=$(xata branch connection-string "$BRANCH_ID")
          echo "database_url=$CONN" >> "$GITHUB_OUTPUT"

      - name: Run Tests
        env:
          DATABASE_URL: ${{ steps.branch.outputs.database_url }}
        run: go test ./...

  cleanup:
    runs-on: ubuntu-latest
    needs: create-preview
    if: always()
    steps:
      - name: Delete Preview Branch
        env:
          XATA_API_KEY: ${{ secrets.XATA_API_KEY }}
        run: |
          xata auth login --api-key "$XATA_API_KEY"
          xata branch delete "${{ needs.create-preview.outputs.branch_id }}"
```

### Programmatic Branch Management (Go)

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "os"
    "strings"
)

type XataClient struct {
    BaseURL string
    APIKey  string
    Project string
    http    *http.Client
}

func NewXataClient() *XataClient {
    return &XataClient{
        BaseURL: os.Getenv("XATA_API_URL"),
        APIKey:  os.Getenv("XATA_API_KEY"),
        Project: os.Getenv("XATA_PROJECT_ID"),
        http:    &http.Client{},
    }
}

type Branch struct {
    ID           string `json:"id"`
    Name         string `json:"name"`
    ParentID     string `json:"parentId"`
    State        string `json:"state"`
    ConnectionURL string `json:"connectionUrl"`
}

type CreateBranchRequest struct {
    Name     string `json:"name"`
    ParentID string `json:"parentId"`
}

func (c *XataClient) CreateBranch(ctx context.Context, name, parentID string) (*Branch, error) {
    payload := CreateBranchRequest{Name: name, ParentID: parentID}
    data, _ := json.Marshal(payload)

    url := fmt.Sprintf("%s/projects/%s/branches", c.BaseURL, c.Project)
    req, err := http.NewRequestWithContext(ctx, "POST", url, strings.NewReader(string(data)))
    if err != nil {
        return nil, err
    }
    req.Header.Set("Authorization", "Bearer "+c.APIKey)
    req.Header.Set("Content-Type", "application/json")

    resp, err := c.http.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()

    var branch Branch
    if err := json.NewDecoder(resp.Body).Decode(&branch); err != nil {
        return nil, err
    }
    return &branch, nil
}

func (c *XataClient) DeleteBranch(ctx context.Context, branchID string) error {
    url := fmt.Sprintf("%s/projects/%s/branches/%s", c.BaseURL, c.Project, branchID)
    req, err := http.NewRequestWithContext(ctx, "DELETE", url, nil)
    if err != nil {
        return err
    }
    req.Header.Set("Authorization", "Bearer "+c.APIKey)
    _, err = c.http.Do(req)
    return err
}

func main() {
    client := NewXataClient()
    ctx := context.Background()

    branch, err := client.CreateBranch(ctx, "feature-test", "main-branch-id")
    if err != nil {
        panic(err)
    }
    fmt.Printf("Created branch %s, connect at: %s\n", branch.ID, branch.ConnectionURL)

    // ... run migrations, tests, etc. ...

    if err := client.DeleteBranch(ctx, branch.ID); err != nil {
        panic(err)
    }
    fmt.Println("Branch cleaned up")
}
```

## Scale-to-Zero

Branches automatically hibernate after inactivity and wake up on the next connection. The SQL Gateway handles the wakeup transparently — clients may experience a short delay (~seconds) on the first connection after hibernation.

```bash
# Manually hibernate a branch
xata branch hibernate <branch-id>

# Wake a branch
xata branch wake <branch-id>

# Check branch state (running, hibernated, starting)
xata branch get <branch-id> --output json | jq '.state'
```

## Troubleshooting

### Tilt/Kind Issues

```bash
# Check all pods are running
kubectl get pods -A

# Check Xata-specific pods
kubectl get pods -n xata

# View logs for a specific component
kubectl logs -n xata -l app=sql-gateway --tail=100
kubectl logs -n xata -l app=branch-operator --tail=100
kubectl logs -n xata -l app=clusters --tail=100

# Restart tilt if resources are stuck
tilt down && tilt up
```

### Branch Stuck in Provisioning

```bash
# Check branch operator logs
kubectl logs -n xata -l app=branch-operator -f

# Check CloudNativePG cluster status
kubectl get clusters -A
kubectl describe cluster <cluster-name> -n <namespace>

# Check OpenEBS storage
kubectl get pvc -A
kubectl describe pvc <pvc-name> -n <namespace>
```

### Connection Refused to SQL Gateway

```bash
# Verify SQL gateway is running
kubectl get svc -n xata sql-gateway

# Port-forward for local testing
kubectl port-forward -n xata svc/sql-gateway 5432:5432

# Test connection
psql "postgresql://$DB_USER:$DB_PASS@localhost:5432/$DB_NAME"
```

### CLI Authentication Failures

```bash
# Re-authenticate
xata auth login --profile local --env local --force

# Verify current profile
xata auth whoami

# Check API key validity
xata apikey list
```

### Checking Scale-to-Zero Plugin

```bash
# Verify CNPG plugin is installed
kubectl get plugins -A | grep scale-to-zero

# Check hibernation annotations on a cluster
kubectl get cluster <name> -n <namespace> -o jsonpath='{.metadata.annotations}'
```

## Key Components Reference

| Component | Role |
|---|---|
| SQL Gateway | Connection routing, scale-to-zero wakeup, HTTP/WS serverless driver |
| Branch Operator | Kubernetes resource lifecycle per branch |
| clusters service | REST API for cluster management |
| projects service | REST API for project management |
| Auth service | Keycloak-based auth, RBAC API keys |
| CloudNativePG | HA Postgres, failover, backups, connection pooling |
| OpenEBS | Cloud-native storage (local NVMe or Mayastor replicated) |

## Use Case Decision Guide

| Scenario | Use Xata OSS? |
|---|---|
| Internal Postgres-as-a-Service | ✅ Yes |
| Preview/testing/dev environments with CoW | ✅ Yes |
| Single Postgres instance | ❌ Use plain Postgres or managed service |
| Public PGaaS for end customers | ⚠️ Contact Xata for BYOC offering |
