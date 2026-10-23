---
name: jenkins-agent-l3-deploy
disable-model-invocation: true
description: >
  Deploy a docker-compose app via a Jenkins INBOUND AGENT running on the target
  server (no SSH from controller), with Docker-secrets "L3" hardening — runtime
  secrets live on tmpfs and never appear in `docker inspect` nor in `.env`.
  Use when the user wants: "deploy via jenkins agent", "no-ssh deploy", "agent
  thay vì ssh", "docker secrets L3", "ẩn secret khỏi docker inspect", "secret
  không nằm trên đĩa", or is wiring a Jenkins pipeline that deploys docker-compose
  to a Linux host. Encodes the gotchas learned from a real 1:1 run (Java 21,
  0444 secret perms, 0400 file-credential, agent user needs docker+sudo).
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: orchestrate
  requires:
    bin: [curl, docker, python3]
---

# Jenkins-agent L3 deploy (no SSH)

Deploy a docker-compose stack where **a Jenkins inbound agent on the target host
runs `deploy.py` + `docker compose` locally**. The controller never SSHes in.
Runtime secrets are written to **tmpfs `/run/payroll-sec` (file 0444, dir 0700)**,
mounted as Docker secrets at `/run/secrets/<name>`, and a tiny entrypoint shim
exports them to env at container start — so they are absent from `docker inspect`
and from `.env`.

## WHAT

### Purpose và context
- **Purpose:** dựng/chạy pipeline Jenkins deploy một stack docker-compose QUA inbound agent trên chính target (controller không SSH vào), với secret L3: chỉ nằm trên tmpfs, mount làm Docker secret, không có trong `docker inspect` lẫn `.env`.
- **Trigger (when to use vs the SSH variant):**
  - **Agent (this skill, preferred):** an inbound agent runs on the target → `sh`
    steps execute locally; only a `Secret file` credential (the cred bundle) is
    needed. Controller opens no SSH outbound.
  - **SSH variant:** controller `ssh/scp/rsync` into the target (needs an
    `SSH Username with private key` credential). Use only when you cannot run an
    agent on the target.
  - User nói "deploy via jenkins agent", "no-ssh deploy", "agent thay vì ssh", "docker secrets L3", "ẩn secret khỏi docker inspect", "secret không nằm trên đĩa", hoặc đang nối pipeline Jenkins deploy docker-compose lên host Linux.
- **Non-goals:** không dựng biến thể SSH (chỉ khi không chạy được agent); không sửa code ứng dụng để đọc secret (shim entrypoint lo); không cài Jenkins controller.

### Mental model
Architecture (L3):
```
secret source (cred bundle)
   → deploy provisioner writes 7 files to tmpfs /run/payroll-sec  (file 0444, dir 0700 root)
   → docker-compose `secrets:` mounts each at /run/secrets/<name> (tmpfs, ro)
   → secrets-entrypoint.sh in each image: for f in /run/secrets/*; export $(UPPER basename)=$(cat f); exec "$@"
   ⇒ secret NOT in `docker inspect` (set at runtime), NOT on disk (RAM only)
```
`postgres` uses the official `POSTGRES_PASSWORD_FILE`; app containers use the
entrypoint shim so **no application code changes** (avoids the Edge-runtime `fs`
trap if a framework imports the secret module in middleware).

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | Jenkins controller reachable `:8080` + `:50000` từ target | có | agent phải kết nối được |
| In | target Linux: Java 21, user thuộc docker group + sudo NOPASSWD | có | xem Gotchas 1, 4 |
| In | `Secret file` credential (cred bundle) | có | không cần SSH credential |
| In | repo app có `docker-compose.yml`, `deploy.py(.example)`, Dockerfile + `secrets-entrypoint.sh` | có | qua SCM checkout hoặc workspace có sẵn |
| In | tick chọn service (WEB/ETL/DB/NGINX/ALL) | không | selective deploy; mặc định full |
| Out | stack chạy trên target | có | build console `Running on <target>` |
| Out | tín hiệu verify | có | `CLEAN <c>` + `MOUNT <c>` mọi container, smoke 200, cred bundle đã shred |

### Rules và capabilities
- RULE-01 (MUST): Don't pass secrets via compose `environment:` (visible in `docker inspect`, written to `.env`).
- RULE-02 (MUST): Don't store the secret files 0600 (non-root container can't read) — use 0444 + dir 0700.
- RULE-03 (MUST): Don't rely on the SSH variant if you can run an agent — agent keeps SSH closed and runs locally.
- RULE-04 (MUST): Don't point a `file://` SCM URL at a path the controller can't see — use a network git URL.
- RULE-05 (MUST): Gotchas 1–5 (mỗi cái đã làm hỏng một lần chạy thật) phải được bake vào setup/pipeline.
- Capabilities: cấu hình node/credential/job trên Jenkins; chạy shell + docker + sudo trên target; đọc git repo (SCM). Không mở SSH outbound từ controller.

### Failure boundaries
- Không chạy được agent trên target → ngoài phạm vi, dùng biến thể SSH (**blocked** cho skill này).
- Stage Verify in `LEAK <c>` hoặc `NOMOUNT <c>` → pipeline **failed** (exit 1), không coi là deploy xong.
- Agent chết `UnsupportedClassVersionError` / permission denied docker-sudo / secret 0600 → **failed**, sửa theo bảng Gotchas rồi chạy lại.
- Repo private chưa có deploy key / known_hosts → **blocked** ở checkout.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | hạ tầng target | Chọn agent (ưu tiên) hay SSH variant | quyết định | không chạy được agent → dừng, SSH variant |
| W02 | effect | Jenkins + target | Setup inbound agent (once): node, Java 21, agent.jar, user docker+sudo, `Secret file` credential | agent online | gotcha 1/4 → sửa, lặp |
| W03 | effect | repo app | Bake `secrets-entrypoint.sh` vào mỗi image (ENTRYPOINT trước CMD); provisioner ghi secret 0444/0700 | image + provisioner | — |
| W04 | effect | job | Pipeline template (Sync → Deploy → Verify), code từ SCM | job chạy | checkout lỗi → B02 |
| W05 | deterministic | build | Verify success (real signals) | `Running on <target>`, `CLEAN`, `MOUNT`, smoke 200, cred shredded | LEAK/NOMOUNT → failed |

Chi tiết từng bước (nguồn chân lý cho W01–W05):

#### Setup the inbound agent (once)
1. Jenkins → Manage Jenkins → Nodes → New Node: Permanent Agent, label = `<target>`,
   Remote root = `/home/<user>/jenkins-agent`, Launch = **inbound (JNLP)**; copy the secret.
2. On the target (agent must reach controller `:8080` + `:50000`):
   ```bash
   sudo apt-get install -y openjdk-21-jre-headless          # Java 21 — NOT 17 (see gotcha 1)
   J21=$(ls /usr/lib/jvm/java-21-openjdk-*/bin/java | head -1)
   mkdir -p ~/jenkins-agent && cd ~/jenkins-agent
   curl -sO http://<CONTROLLER>:8080/jnlpJars/agent.jar
   nohup "$J21" -jar agent.jar -url http://<CONTROLLER>:8080/ \
     -secret <AGENT_SECRET> -name <target> -workDir ~/jenkins-agent > agent.log 2>&1 &
   ```
   Run the agent as a user that is in the **docker group** AND has **sudo NOPASSWD**.
   For production replace `nohup` with a systemd unit (`Restart=always`).
3. Credential: one `Secret file` credential (the cred bundle). No SSH credential.

#### Pipeline template (declarative)
```groovy
pipeline {
  agent { label '<target>' }                 // runs ON the target, no ssh
  environment { APP = '/home/<user>/<app-dir>' }
  stages {
    stage('Sync') { steps { sh '''
      set -e
      cp -f docker-compose.yml deploy.py.example "$APP/"
      cp -f web/Dockerfile web/secrets-entrypoint.sh "$APP/web/"
      cp -f etl/Dockerfile etl/secrets-entrypoint.sh "$APP/etl/"
      cd "$APP" && cp -f deploy.py.example deploy.py
    ''' } }
    stage('Deploy') { steps { withCredentials([file(credentialsId:'app-cred', variable:'CRED')]) { sh '''
      set -e
      mkdir -p /dev/shm/pl && chmod 700 /dev/shm/pl
      cp "$CRED" /dev/shm/pl/cred.txt && chmod 600 /dev/shm/pl/cred.txt   # gotcha 3
      cd "$APP" && ln -sf /dev/shm/pl/cred.txt cred.txt
      sudo python3 deploy.py --no-nginx --etl-url /etl
      rm -f cred.txt; shred -uf /dev/shm/pl/cred.txt 2>/dev/null || rm -f /dev/shm/pl/cred.txt
    ''' } } }
    stage('Verify') { steps { sh '''
      set -e
      for c in <containers>; do
        docker inspect "$c" --format "{{range .Config.Env}}{{println .}}{{end}}" \
          | grep -iqE "SESSION_SECRET=|AUTH_USERS=|PASSWORD=|DATABASE_URL=" && { echo "LEAK $c"; exit 1; } || echo "CLEAN $c"
        docker exec "$c" ls /run/secrets >/dev/null 2>&1 && echo "MOUNT $c" || { echo "NOMOUNT $c"; exit 1; }
      done
    ''' } }
  }
}
```
Provide the workspace code via SCM checkout, or pre-populate the agent workspace.

#### secrets-entrypoint.sh (baked into each app image; ENTRYPOINT before CMD)
```sh
#!/bin/sh
set -e
if [ -d /run/secrets ]; then
  for f in /run/secrets/*; do [ -f "$f" ] || continue
    name=$(basename "$f" | tr '[:lower:]' '[:upper:]'); export "$name=$(cat "$f")"
  done
fi
exec "$@"
```
The provisioner (e.g. `deploy.py`) writes the secret files to a tmpfs dir
**mode 0444 (files) / 0700 (dir)**, then `docker compose up -d`.

#### Gotchas (each cost a failed real run — bake these in)
| # | Symptom | Fix |
|---|---------|-----|
| 1 | Agent dies `UnsupportedClassVersionError: class 65.0 … up to 61.0` | Jenkins 2.5xx agent.jar needs **Java 21**, not 17. |
| 2 | App container crash-loops `Permission denied /run/secrets/*` | Compose non-swarm bind-mounts the source file's perms; write secret files **0444** (dir 0700) so the non-root container user can read. |
| 3 | `shred /dev/shm/.../cred: Permission denied` | Jenkins `file` credential is delivered **0400 (read-only)**; `cp` then `chmod 600`, and use `shred -uf … || rm -f`. |
| 4 | `docker`/`sudo` "permission denied" inside the pipeline | The agent process user must be in the **docker group** and have **sudo NOPASSWD**. |
| 5 | Reboot → containers fail to mount secret | `/run` is tmpfs → secrets cleared on reboot; re-run the deploy (or a boot hook) to re-materialize before `compose up`. |

#### Verify success (real signals)
- Build console shows `Running on <target>` (proves it ran on the agent, not controller).
- `CLEAN <c>` for every container (secret absent from `docker inspect`).
- `MOUNT <c>` (secret present at `/run/secrets`).
- App smoke (e.g. login) returns 200.
- The cred bundle is shredded from `/dev/shm` (not left on disk).


### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | chỉ deploy vài service (tick WEB/ETL/DB/NGINX thay ALL) | Selective deploy: `booleanParam` → `deploy.py --services "$SVC"` + `--no-deps`; NGINX thì `docker restart` proxy riêng | ALL → full; không tick gì → `none` = secrets only, no up | W05 |
| B02 | conditional_required | code lấy từ git (production: Pipeline script from SCM) | cấu hình SCM; repo private → SSH deploy key + known_hosts trên controller VÀ agent | lab không git server → agent `git clone file:///…/repo.git` | W04 |
| B03 | recovery | target reboot (`/run` tmpfs xoá secret) | chạy lại deploy (hoặc boot hook) để tái tạo secret trước `compose up` | — | W05 |

### Reference — Branch details

#### Selective deploy (deploy only some services, not full)
Expose `booleanParam` checkboxes (WEB/ETL/DB/NGINX/ALL) and pass the chosen compose
services to the provisioner. Use `--no-deps` so a tick rebuilds **only that service**
(not its dependency chain):
```sh
if [ "$ALL" = true ]; then SVC=""; else
  S=""; [ "$WEB" = true ] && S="$S web"; [ "$ETL" = true ] && S="$S etl"; [ "$DB" = true ] && S="$S postgres"
  [ -z "$(echo $S|xargs)" ] && SVC=none || SVC=$(echo $S|xargs)
fi
deploy.py --services "$SVC"        # "" = full ; "web etl" = those ; "none" = secrets only, no up
# provisioner runs: docker compose up -d --build --no-deps $SVC
[ "$NGINX" = true ] && docker restart <proxy-container>   # proxy is a separate container, not compose
```
**Dependency graph (depends_on) — document it** so operators know a fresh deploy needs the chain:
`web → etl → postgres` (proxy/nginx independent). With `--no-deps`, tick web = ONLY web; for a
clean first deploy tick the whole chain (or ALL). Verified: single ticks + combos all touch exactly
the chosen services.

#### Pulling code from git
Production: configure the job as **Pipeline script from SCM** (git repo + scriptPath); Jenkins
auto-`checkout scm` into the agent workspace, then the pipeline runs. The git URL must be reachable
by BOTH controller (fetch Jenkinsfile) and agent (checkout workspace) — `file://` only works on the
side that owns it; in a lab without a git server, have the agent `git clone file:///…/repo.git`.

**Private repo (tested with GitHub, build SUCCESS):**
- HTTPS anonymous clone fails for a private repo — needs auth.
- Use an **SSH deploy key** (read-only) on the repo; put the private key in a Jenkins
  `SSH Username with private key` credential (username `git`); SCM URL `git@github.com:owner/repo.git`
  with that credentialsId.
- **Host key gotcha:** add `github.com` to known_hosts on controller AND agent
  (`ssh-keyscan github.com >> ~/.ssh/known_hosts`) or set the git host-key strategy to
  "Accept first connection", else the SSH clone fails host-key verification.
- The deploy key's public part on GitHub must match the private key in Jenkins (compare
  `ssh-keygen -lf key.pub` fingerprint vs what GitHub shows).

### Validation và stopping
Stage Verify là cổng tất định: exit 1 khi có `LEAK`/`NOMOUNT`. Cần người xem: console `Running on <target>`, smoke login 200, `/dev/shm` không còn cred. Dừng khi đủ 5 tín hiệu ở "Verify success"; lỗi thuộc bảng Gotchas → sửa đúng dòng Fix rồi chạy lại build, không đoán ngoài bảng.

### Examples
- **Positive:** app payroll (web/etl/postgres) — agent label `<target>` Java 21, user trong docker group + sudo NOPASSWD, build tick ALL → console `Running on <target>`, `CLEAN`/`MOUNT` cho mọi container, login 200, cred bundle đã shred khỏi `/dev/shm`.
- **Boundary/failure:** secret ghi 0600 → container web crash-loop `Permission denied /run/secrets/*` (gotcha 2) → provisioner đổi sang 0444 + dir 0700, chạy lại; tick chỉ WEB lần deploy đầu → web lên một mình vì `--no-deps`, thiếu etl/postgres → tick cả chuỗi `web → etl → postgres` (hoặc ALL).

