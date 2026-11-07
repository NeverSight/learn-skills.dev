---
name: huawei-cloud-gallery-publish
description: "一键创建简单网页并发布到华为云开发者作品展览馆（CodeArts ACP 生成页面 → 开发隧道 → GitCode 仓库 → 封面/简介/详情 → 投递进行中活动）。用于用户提到华为云开发者作品展览馆、华为云发布作品、gallery 投稿、闯关活动投递、CodeArts ACP 生成网页并上架、把 demo 页发布到华为云陈列馆时。全程自动执行，仅在 GitCode OAuth 授权时需要用户打开一次浏览器链接。Triggers: 华为云作品展览馆, 华为云发布作品, gallery 发布, 闯关活动, CodeArts 网页, hcloud STS, gitcode 发布."
---

# 一键发布简单网页到华为云开发者作品展览馆

本 Skill 封装了「从零生成一个 Hello World 级简单网页 → 托管 → 投递到华为云开发者作品展览馆（默认投递进行中的闯关活动）」的完整流程。AI 全程自动执行，仅在 **GitCode OAuth 授权** 时需要用户打开一次浏览器链接；**Step 7 选活动** 由用户确认序号。

## 前置依赖（运行环境内必须已存在）

- `huawei-cloud-ext-coding` skill（CodeArts ACP，监听 `127.0.0.1:19300`）
- `huawei-cloud-publish-work-to-gallery` skill，位于 `/root/workspace/.agents/skills/huawei-cloud-publish-work-to-gallery`
- `huawei-cloud-jobenv-devbridge-tunnel` skill（开发隧道 db_* 命令）
- `/root/job-envs/registry.json` 中 id=`codearts` 的 jobenv
- `/usr/local/bin/hcloud` CLI（已登录）

以上均在目标沙箱/宿主机环境内，本包不带脚本实现，只做编排。

## 分享给非技术用户

如果对方没有装 skill 体系、只想拿到一段可复制的提示词直接喂给 AI，把 [`references/shareable-prompt.md`](references/shareable-prompt.md) 的「提示词正文」整段发过去即可 —— 这是与本 SKILL.md 等价的原始可复用提示词，含完整分享包装。

## 阶段一：创建网页（CodeArts ACP）

1. 加载 `huawei-cloud-ext-coding` skill，`curl -s --max-time 3 http://127.0.0.1:19300/healthz` 确认 ACP 可用。
2. 从 `/root/job-envs/registry.json` 读 id=`codearts` 的 `cwd`，在其下建子目录 `simple-webpage`。
3. 建 acpx session，发 prompt 让 CodeArts 生成单个 `index.html`（居中标题 "Hello World" + 欢迎文字 + 浅色背景 + flexbox 居中），后台启动 `python3 -m http.server 8000 --bind 0.0.0.0`。**不写测试，不加额外文件**。
4. 轮询日志到 `[done]`，确认 8000 返回 200。

## 阶段二：准备宿主机工作目录

- 先建宿主机目录，再拷贝（沙箱文件在 bwrap mount namespace 内，外层 `ls` 看不到，必须用 http.server 进程的 `/proc` 路径访问）：

```bash
mkdir -p /root/workspace/simple-webpage
HTTP_PID=$(pgrep -f "http.server 8000" | head -1)
cp /proc/$HTTP_PID/cwd/index.html /root/workspace/simple-webpage/index.html
```

- 提前创建 `README.md`（scan-projects 靠它识别项目根，没有会扫不到）：标题 `# Simple Webpage` + 一句项目说明 + 预览命令。

## 阶段三：发布（加载 huawei-cloud-publish-work-to-gallery skill）

```bash
export SKILL_DIR=/root/workspace/.agents/skills/huawei-cloud-publish-work-to-gallery
chmod +x "$SKILL_DIR/scripts/"*
```

### Step 1 账号

`check-version.mjs`（status=ok）→ `resolve-domain.mjs --hcloud /usr/local/bin/hcloud` 拿 domainID → `gen_sts.py --account <domainID> --hcloud /usr/local/bin/hcloud --creds-out ./sts-creds.json --sh-out ./sts-creds.sh`。

### Step 2 隧道

`detect-env.mjs` 确认 tunnel=true → 加载 `huawei-cloud-jobenv-devbridge-tunnel` skill：`db_init` → `db_auth_status` → `db_create <name> "开发隧道" 72` → `db_port_create <id> 8000 auto true` → `db_host <id>` → `db_tunnel_url <id>` 得 envUrl → `curl -sf <envUrl>/index.html` 验证 200。

### Step 3 Git 仓库

- **git init 前先写 .gitignore**（排除 `sts-creds.json` / `sts-creds.sh`，否则凭证会被提交）：

```bash
printf 'sts-creds.json\nsts-creds.sh\n' > .gitignore
git init -b main
git add -A
git -c user.email=agent@local -c user.name=agent commit -m "Initial commit"
```

- **提交只做一次，且只在本步执行**；Step 4 起的产物（cover.png / diagram.png / detail.zip / resources/）一律写 `/tmp`，不落 workDir，避免后续 `git add -A` 把二进制带进仓。
- GitCode OAuth：`ensure-gitcode-credential.mjs` → missing 则 `gitcode-oauth.ensure.mjs --start` 拿 login_url → **立即醒目展示链接给用户并提示"请现在打开浏览器授权"**，马上 `--wait session_1 --timeout 300`。**超时则重新 `--start` 生成新链接再等**。
- 建仓库 + push：**GitCode API POST 用 `private_token` query param，不是 Authorization header**。从 `/root/.gitcode/auth.toml` 读 `access_token` 字段（不是 `token`）：
  - `GET /api/v5/user?private_token=<tok>` 拿 login
  - `POST /api/v5/user/repos?private_token=<tok>` body `{"name":"simple-webpage","private":false}`
  - `git remote add origin https://<login>:<tok>@gitcode.com/<login>/simple-webpage.git`
  - `git push -u origin main` → `git remote set-url origin` 去掉 token
- `read-git-info.mjs` 确认 gitUrl + gitBranch=main；`extract-workname.mjs` 拿 workName。

### Step 4 封面

并行执行 `preflight.sh`（后台，轮询 `/tmp/font-gate-ok`，首次 2-5 分钟）+ `ensure-utf8.mjs`，然后：

```bash
build-cover.mjs --url http://127.0.0.1:8000 --project-dir <workDir> \
  --title "<workName>" --tagline "<短tagline>" --description "<1-3句>" \
  --out /tmp/cover.png --quiet
verify-glyphs.py /tmp/cover.png --quiet
```

### Step 5 简介

直接用这句（29 字符，一次通过，不要先写长版再裁剪）：

```text
极简Hello World网页，单文件居中布局，浅色背景。
```

写入 `/tmp/intro.txt`，`count-cjk.mjs --file /tmp/intro.txt` 验证。

### Step 6 详情

写架构图 HTML → `generate_diagram.py --html /tmp/diagram.html --out /tmp/diagram.png --width 1280` → `verify-glyphs.py` → 写详情 README.md（500-1500 字，引用架构图）→ `build-detail-zip.mjs --readme <md> --resources <workDir>/resources --out /tmp/detail.zip`。

### Step 7 选活动（用户确认）

`api.mjs GET /v1/gallery/camps --creds-file ./sts-creds.json`（**401 则先刷新 STS**）→ 列可投稿活动（`startsAt ≤ 今天 ≤ endsAt` 且 `status=published`），让用户回序号。默认推荐「闯关活动」。

### Step 8 发布

- **发布前刷新 STS**（全流程可能超过 900s 有效期）：重跑 `gen_sts.py`。
- `check-gates.mjs --cover /tmp/cover.png --detail /tmp/detail.zip --strict --max-age 3600 --quiet`。
- 构建 params JSON（key: `idempotencyKey, accessKeyId, secretAccessKey, securityToken, trainingCampId, workName, introduction, coverImage, detailZip, gitUrl, gitBranch, envUrl, _refresh`）→ `publish-work.mjs /tmp/publish-params.json --max-age 3600` → 期望 `#status=201`，取 `workId` / `workUrl`。
- 清理临时文件。返回陈列馆链接给用户。

## 防坑清单（务必遵守）

1. **OAuth 链接一生成就立刻展示给用户并开始等待**，不要耽搁；超时重新 `--start` 生成新链接。
2. 简介直接用上面 29 字符短版，不要先写长再裁。
3. **发布前刷新 STS**（900s 有效期容易被全流程超掉）。
4. `git init` 前先写 `.gitignore` 排除 STS 凭证。
5. GitCode API POST 用 `private_token` query param，不是 Authorization header；读 `access_token` 字段。
6. 沙箱文件用 `/proc/<pid>/cwd/` 访问（bwrap mount namespace 隔离）。
7. workDir 提前放 `README.md`（scan-projects 识别项目根）。
8. 发布结束后**不要自动清理隧道**，留给用户验证。
9. 宿主机目录先 `mkdir -p` 再 `cp`；**提交只做一次**，Step 4 起产物一律落 `/tmp`，不落 workDir。
