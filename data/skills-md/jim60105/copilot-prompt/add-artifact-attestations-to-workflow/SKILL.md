---
name: add-artifact-attestations-to-workflow
description: Add SLSA build-provenance attestations to existing GitHub Actions workflows. Use when the user wants to add artifact attestations, build provenance, or SLSA attestations to Docker container image builds in GitHub Actions CI/CD pipelines.
metadata:
  original-prompt: add-artifact-attestations-to-workflow.prompt.md
---

# Add Artifact Attestations to Workflow

Add SLSA build-provenance attestations to existing GitHub Actions workflows for Docker container images.

## Steps

0. Find existing workflow files in `.github/workflows/` that contain `docker/build-push-action` or similar steps. Note that composite actions may be used — read both the composite action and the calling workflow simultaneously.

1. **Enable OIDC & Attestations permissions**
   In each workflow's top-level `permissions:` block, grant both the OIDC token and attestations write privileges:

   ```yaml
   permissions:
     id-token: write
     attestations: write
     contents: read       # (existing)
     packages: write      # (existing)
   ```

2. **Log in to container registries**
   Ensure authentication steps exist for each registry you'll attest against. Judge whether there are omissions based on the implemented content, rather than always logging into all registries.

   ```yaml
   - name: Login to GHCR
     uses: docker/login-action@v3
     with:
       registry: ghcr.io
       username: ${{ github.actor }}
       password: ${{ secrets.GITHUB_TOKEN }}

   - name: Login to Docker Hub
     uses: docker/login-action@v3
     with:
       registry: index.docker.io
       username: ${{ secrets.DOCKERHUB_USERNAME }}
       password: ${{ secrets.DOCKERHUB_TOKEN }}

   - name: Login to Quay
     uses: docker/login-action@v3
     with:
       registry: quay.io
       username: ${{ secrets.QUAY_USERNAME }}
       password: ${{ secrets.QUAY_TOKEN }}
   ```

3. **Build & push image, capturing the digest**
   Use `docker/build-push-action@v*` with an `id` to reference its output. Judge tags based on implemented content.

   ```yaml
   - name: Build and push image
     id: build_push
     uses: docker/build-push-action@v5
     with:
       context: .
       push: true
       tags: |
         ghcr.io/${{ github.repository }}:latest
         index.docker.io/${{ secrets.DOCKERHUB_USERNAME }}/your-repo:latest
         quay.io/${{ github.repository_owner }}/your-repo:latest
   ```

4. **Add attestation steps**
   After the `build_push` step, insert one `actions/attest-build-provenance@v3` invocation per registry. The `subject-name` is the full image name without a tag. The `subject-digest` comes from the build step's output. Judge which registries to use based on implemented content.

   ```yaml
   - name: Attest GHCR image
     uses: actions/attest-build-provenance@v3
     with:
       subject-name: ghcr.io/${{ github.repository }}
       subject-digest: ${{ steps.build_push.outputs.digest }}

   - name: Attest Docker Hub image
     uses: actions/attest-build-provenance@v3
     with:
       subject-name: index.docker.io/${{ secrets.DOCKERHUB_USERNAME }}/your-repo
       subject-digest: ${{ steps.build_push.outputs.digest }}

   - name: Attest Quay image
     uses: actions/attest-build-provenance@v3
     with:
       subject-name: quay.io/${{ github.repository_owner }}/your-repo
       subject-digest: ${{ steps.build_push.outputs.digest }}
   ```

5. **Commit changes**
   Write the git commit message in English.

   ```bash
   git add .github/workflows/docker_publish.yml # or whatever files you modified
   git commit --signoff -m "ci: add build-provenance attestations for container images"
   ```

6. **Ask the user to push**
   Tell the user to manually push the changes and verify attestations are created successfully. DO NOT perform a git push.
