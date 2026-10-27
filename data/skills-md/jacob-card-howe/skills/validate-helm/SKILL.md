---
name: validate-helm
description: Validate Helm chart rendering for apps in this k8s repo. Discovers chart source and version from ArgoCD appsets, runs helm template, and reports issues.
allowed-tools: Bash, Read, Glob, Grep
argument-hint: "<app-name> [values-file] (e.g., zot, zot custom-values.yaml)"
---

Validate a Helm-based app by discovering its chart source from the ArgoCD ApplicationSet and running `helm template` against the local values file, or a custom values file if provided.

## Process

Parse `$ARGUMENTS`: the first argument is the app name, the optional second argument is a custom values file path.

1. **Find the ApplicationSet** at `appsets/<app-name>.yaml`. Read it to extract:
   - `repoURL` — the Helm chart repository URL
   - `chart` — the chart name
   - `targetRevision` — the chart version
   - `valueFiles` — path(s) to values files (typically `apps/<app-name>/values.yaml`)

   If the appset doesn't use a Helm chart source (e.g., it's a plain manifest app), report that and stop.

2. **Ensure the Helm repo is added**:
   ```
   helm repo add <app-name> <repoURL> 2>/dev/null || true
   helm repo update <app-name>
   ```

3. **Determine the values file**:
   - If a custom values file was provided as the second argument, use it. Resolve relative paths from the repo root.
   - Otherwise, use the default values file from the appset's `valueFiles` (typically `apps/<app-name>/values.yaml`).

4. **Run `helm template`**:
   ```
   helm template <app-name> <app-name>/<chart> \
     --version <targetRevision> \
     -f <values-file> \
     --namespace <destination-namespace>
   ```
   The destination namespace is in `spec.template.spec.destination.namespace` of the appset.

   When using a custom values file, note which file is being used in the output so the user knows what they're validating.

5. **Check the output** for:
   - Template rendering errors (non-zero exit code)
   - Empty or missing resources that were expected
   - Secrets containing unexpected default values from the chart
   - ConfigMaps with malformed embedded config (e.g., invalid JSON)

6. **Report results**:
   - If clean: "Helm template rendered successfully. N resources generated."
   - If errors: show the error output and suggest fixes.
   - List the resource kinds and names that were rendered (brief summary, not full YAML).

## Notes

- If no app name is provided, list available Helm-based apps by scanning `appsets/*.yaml` for entries with a `chart:` field.
- Some apps use multiple values files or additional manifest directories — note these but only template the Helm chart portion.
- Do not modify any files. This skill is read-only validation.
