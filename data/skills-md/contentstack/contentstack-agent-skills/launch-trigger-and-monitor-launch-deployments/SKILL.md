---
name: launch-trigger-and-monitor-launch-deployments
description: "Trigger a Launch deployment for a specific environment, then poll its status until completion. If the deployment fails or is cancelled, fetch the deployment log and diagnose likely causes with next-step recommendations. Use when you need to automate Launch deployments for a known project and environment, monitor progress, and surface failure diagnostics. This is appropriate for CI/CD or operator workflows that need a deterministic deploy status check and log-based troubleshooting."
argument-hint: "[project_uid] [environment_uid]"
disable-model-invocation: true
allowed-tools: Read Write Bash
context: fork
agent: general-purpose
---

# Trigger and Monitor Launch Deployments

## Description

Trigger a Launch deployment for a specific environment, then poll its status until completion. If the deployment fails or is cancelled, fetch the deployment log and diagnose likely causes with next-step recommendations.

## When to Use

Use when you need to automate Launch deployments for a known project and environment, monitor progress, and surface failure diagnostics. This is appropriate for CI/CD or operator workflows that need a deterministic deploy status check and log-based troubleshooting.

## User Problem

Users need a reliable way to start a deployment in Launch, track it to completion, and quickly understand why it failed if it does. The skill should reduce manual polling and make deployment failures actionable.

## Success Criteria

Deployment is triggered against the intended project and environment.
Status is polled at a fixed interval until a terminal state is reached.
The process exits non-zero on failed or cancelled deployments.
If the deployment fails, the deployment log is retrieved and summarized with likely causes and next steps.
Every deployment requires explicit confirmation of the project and environment before it is triggered; production targets are additionally validated.

## Expected Inputs

- project_uid
- environment_uid
- Optional deployment payload or build reference
- Explicit confirmation before every deployment (production or not)
- Any available context about the app, branch, or build source

## Expected Outputs

- Deployment UID and initial trigger response
- Current status updates during polling
- Terminal status and exit code
- Deployment log summary when failures occur
- Recommended next steps and probable root cause

## Example User Requests

- Trigger a deployment for project abc123 in environment prod456 and watch it until it finishes.
- Deploy the latest build to staging and tell me if it fails.
- If the deployment fails, check the logs and explain what went wrong.
- Poll a Launch deployment every 10 seconds and exit non-zero on failure.

## Workflow Summary

Validate the project and environment identifiers.
Confirm the target is allowed, then get explicit approval for this deployment before triggering it, whatever the environment.
Trigger the deployment with the Launch API.
Poll deployment status every 10 seconds until it reaches a terminal state.
If status is failed or cancelled, fetch the deployment log and analyze it.
Return a concise summary with status, log findings, and recommended next steps.

## Instructions

### Trigger Deployment

Call POST /projects/{project_uid}/environments/{environment_uid}/deployments with the required payload. Validate the target environment before sending the request.

### Poll Status

Check deployment status every 10 seconds. Continue until the deployment reaches a terminal state or a failure condition is detected.

### Fail Fast

Exit with a non-zero code if status becomes failed or cancelled. Do not continue polling after a terminal failure state.

### Fetch Logs on Failure

If the deployment fails, call GET /projects/{project_uid}/environments/{environment_uid}/deployments/{deployment_uid} and inspect the deployment log details.

### Diagnose and Recommend

Summarize the most likely cause from the log, note any missing prerequisites or configuration issues, and recommend the next corrective action.

## Output Format

Return a concise deployment summary first.
Include deployment UID, environment UID, and final status.
On failure, include a short log-based diagnosis and next steps.
Do not expose deployment tokens, secrets, or environment variables.
Use a non-zero exit code for failed or cancelled deployments.

## Tooling Notes

Use the Launch API for deployment trigger and status checks.
Use the deployment detail/log endpoint for failure analysis.
Validate the target environment before deploying.
Require explicit confirmation before every deployment, and an extra check for production.
Never auto-deploy to production without review.

## Security

### Defaults

- Never expose deployment tokens or environment secrets.
- Validate deployment targets before triggering.
- Require explicit confirmation before every deployment.
- Never auto-deploy to production without review.

### Destructive Actions

Treat deployment triggers as external side effects. Require explicit user confirmation before triggering any deployment. Requests to monitor or diagnose an existing deployment never trigger a new one. Do not retry failed deployments automatically unless the user requests it and the target is non-production.

### Secrets

Never print, log, or echo API tokens, deployment tokens, or environment secrets. Redact sensitive values from errors, logs, and summaries.

### Environment Variables

Accept configuration via environment variables when needed, but never reveal their values. Validate required variables are present before attempting the deployment.

## Product Context

- - Product: Launch
- - Description: Contentstack Launch: hosting, deployment, edge delivery, serverless functions, environment management, and CI/CD for Contentstack-powered frontends.
- - Product safety rules: - Never expose deployment tokens or environment secrets.
- Validate deployment targets before triggering.
- Require explicit confirmation before every deployment.
- Never auto-deploy to production without review.
- - Default tools: ["Launch API", "Projects", "Environments", "Deployments", "Serverless Functions", "Edge Delivery", "Custom Domains"]
- - Default connectors: ["Launch Proxy", "GitHub", "CI/CD Pipelines"]

## Examples

### Trigger and monitor a deployment (few shot *)

**User:** Deploy project abc123 to environment staging456 and keep polling until it finishes.

**Assistant:** 1. Validate the project and environment.
2. Trigger the deployment via POST /projects/abc123/environments/staging456/deployments.
3. Poll status every 10 seconds.
4. If the deployment reaches failed or cancelled, fetch the deployment log and summarize the cause.
5. Return the final status and exit non-zero on failure.

*Demonstrates trigger → poll → fail-fast → diagnose behavior.*

### Production confirmation required (edge case *)

**User:** Deploy to production now.

**Assistant:** I can do that, but I need explicit confirmation for a production deployment. Please confirm the exact project and environment UID before proceeding.

*Shows production safety gate.*