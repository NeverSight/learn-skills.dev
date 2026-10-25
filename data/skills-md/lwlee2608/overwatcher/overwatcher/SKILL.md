---
name: overwatcher
description: Use when creating, configuring, or inspecting an Overwatcher deploy project with owctl — setting the compose file, mapping GitHub repos to compose services, or installing and binding a VM agent so pushes auto-deploy.
user-invocable: true
---

# Managing Overwatcher Projects

Overwatcher deploys Docker Compose services on a VM when a GitHub repo is pushed or its CI workflow succeeds. Use `owctl` for every API operation; do not hand-roll API calls or handle agent tokens.

## Rules

1. **Install owctl if missing.** If the installer fails, stop and report it; do not build from source unless asked.
   ```sh
   curl -fsSL "${OVERWATCHER_URL:-https://overwatcher-web-production.up.railway.app}/cli.sh" | sh
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **Use existing credentials.** owctl reads `OVERWATCHER_API_KEY` or a saved `owctl login`. If it reports no API key, ask the user to run `owctl login` in their terminal or set `OVERWATCHER_API_KEY` (create one under **user menu → API keys**). Never echo the key or pass it as an argument.

3. **Inspect the coordinator.** Use `--json`; stop on errors. Reuse a project with the same name instead of creating a duplicate.
   ```sh
   owctl project list --json
   owctl agent list --json
   owctl project get <project> --json
   ```

4. **Inspect the VM before asking anything else.** Ask only for the SSH target, resolve aliases with `ssh -G <target>`, then probe (read-only; `sh -s` avoids zsh glob errors on the VM):
   ```sh
   ssh -T -o BatchMode=yes <target> sh -s <<'EOF'
   echo "user: $(id -un)"
   sudo -n true 2>/dev/null && echo "sudo: passwordless" || echo "sudo: needs password"
   command -v systemctl >/dev/null && echo "systemd: ok" || echo "systemd: missing"
   command -v curl >/dev/null && echo "curl: ok" || echo "curl: missing"
   systemctl show -p LoadState -p ActiveState overwatcher-agent 2>/dev/null
   docker compose version 2>/dev/null || echo "compose v2: missing"
   docker compose ls --all 2>/dev/null || echo "docker: no access for $(id -un)"
   EOF
   ```
   Do not read `/etc/overwatcher-agent.env`; it holds the agent token. Then ask only what is still unknown, stating findings:
   - `LoadState=loaded`: an agent exists. If it is in `agent list` (match `name` or `remote_ip`), offer to bind it instead of reinstalling; otherwise ask the user.
   - Offer `docker compose ls` config files as the compose path. Without docker access, ask for the path; the installer adds the user to the `docker` group.
   - Missing sudo, systemd, curl, or Compose v2: stop until fixed.

5. **Create the project with a confirmed compose path.** The file must already exist on the VM (`ssh <target> test -r <path>`).
   ```sh
   owctl project create <project> --compose-file <path> --environment production --json
   ```

6. **Derive services from the app repo.** Take each field from the source, not defaults: `image` from the compose `image:` line, `workflow` from the CI file that pushes it, `tag` from the tags it pushes, `root_directory` from its build `context` (never `/` in a monorepo). Use existing projects as a pattern. `name` must equal the compose service key. `service set` replaces the whole list, so keep existing services.
   ```sh
   owctl service set <project> -f - --json <<'EOF'
   services:
     - name: web
       repo: acme/my-app
       image: ghcr.io/acme/my-app-web
       tag: main
       branch: main
       root_directory: services/web
       workflow: build.yml
   EOF
   ```
   Without `workflow`, deploys fire on push and may pull a stale image. If one workflow builds several images, every run redeploys all of them; tell the user.

7. **Bind or install the agent.** Binding moves an agent off its old project and replaces the project's current agent; ask before either.
   ```sh
   owctl agent bind <agent-id> <project> --json
   owctl agent install --ssh <target> --project <project> --json
   ```
   Install sets up a root-managed systemd service; get explicit approval before adding `--yes`. On failure owctl revokes the agent but VM files may remain; report and do not retry blindly. The agent runs as the SSH user, which needs registry login for private images.

8. **Check GitHub App access.** Without it, CI passes but nothing deploys. owctl cannot check this; use `gh` (needs the `read:user` scope; if missing, ask the user to run `gh auth refresh -h github.com -s read:user`):
   ```sh
   gh api user/installations --jq '.installations[] | select(.app_slug=="overwatcher-app") | {id, account: .account.login, repository_selection, events}'
   gh api user/installations/<id>/repositories --paginate --jq '.repositories[].full_name'
   ```
   The repo owner needs an installation whose `events` include `push` (and `workflow_run` when used). If `repository_selection` is `selected`, the repo must be listed. Otherwise send the user to the installation's **Configure → Repository access** and do not report setup as complete. GitHub does not resend earlier events; re-run the latest CI run after access is granted.

## Verification

1. `owctl project get <project> --json`: check `compose_file`, `enabled`, and each service's fields.
2. `owctl agent list --json`: the agent's `project_id` matches and `status` is `connected`.
3. The GitHub App check in rule 8 passes for every repo.
4. Report project ID, agent name, and trigger per service. This does not prove a deploy succeeded.
