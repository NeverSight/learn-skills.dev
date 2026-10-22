---
name: rivet-deploy-image
description: Deploy a Docker image to a Rivet Cloud cluster through the Rivet MCP server, or roll a cluster back to an earlier build. Use when asked to deploy, ship, release, or roll back an app on a Rivet cluster and a shell with Docker is available.
metadata:
  rivet-requires: rivet.deploy.prepare rivet.deploy.rollout
---

# Deploy an image to a Rivet cluster

A deploy is a local build, one upload, and two Code Mode operations run through the `execute` tool. It needs Docker and a shell. It does not need the Rivet CLI or any other login.

## Before starting

1. Confirm the session can deploy. If `search` does not list `rivet.deploy.prepare`, the session is read-only or is pinned to a project or namespace, and the deploy cannot run from here. Say so instead of retrying.
2. Pick the cluster. Run `return (await rivet.cloud.v2.clusters.list()).items;` in `execute` and use the `cluster` field of the one to deploy to, which is its name. On a connection pinned to a cluster, `rivet.context()` reports it, and `cluster` is left out of every call below.

## Steps

1. Build and measure the image in the shell. The platform must be `linux/amd64`.

   ```sh
   docker build --platform linux/amd64 -t app .
   docker image save app -o image.tar
   wc -c < image.tar                        # content_length
   openssl md5 -binary image.tar | base64   # content_md5
   ```

   The tarball must be 5 GiB or smaller. Measure the exact file that will be uploaded, because the build fails verification when either value differs.

2. Register the build.

   ```js
   return await rivet.deploy.prepare({
   	cluster: "my-cluster",
   	image: "app:latest",
   	content_length: 48213504,
   	content_md5: "1B2M2Y8AsgTpgAmY7PhCfg==",
   });
   ```

   `content_length` is a number, not a string. Pass `file` when the tarball is not named `image.tar`. Keep the returned `build_id`.

3. Run the returned `upload` command in the shell, unchanged. It is a curl command against a presigned URL that is good for that one tarball until `expires_at`, so it carries no Rivet credentials.

4. Roll out, repeating until `done` is `true`.

   ```js
   return await rivet.deploy.rollout({ cluster: "my-cluster", build_id: "<build_id>" });
   ```

   Each call advances one step and returns immediately, so call it again while `done` is `false`. See `references/rollout.md` for each step, the errors, and how to roll back.

5. Report the `build_id` and the `endpoints` from the final result to the user. The `build_id` is what a later rollback needs.

## Rules

- Never rebuild or re-upload to retry a rollout. Call `rivet.deploy.rollout` again with the same `build_id`.
- Use `rivet.deploy.*` for the whole deploy. Do not drive `rivet.cloud.v2.builds.*` or `rivet.cloud.v2.runnerPools.upsert` by hand, because an upsert replaces the pool's settings wholesale and would drop its allowlist.
- Do not guess a `cluster`, `region`, or `pool` name. List them first.
