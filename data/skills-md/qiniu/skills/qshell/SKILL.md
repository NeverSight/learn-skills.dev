---
name: qshell
description: >
  Operate Qiniu Cloud KODO object storage via qshell CLI. Covers file CRUD,
  batch operations, CDN refresh/prefetch, data processing, file sharing,
  M3U8 operations, and sandbox management.
type: tool
best_for:
  - "Managing Qiniu Cloud KODO object storage resources"
  - "Batch file operations (upload, download, copy, move, delete)"
  - "CDN cache refresh and prefetch"
  - "Cloud sandbox environment management"
  - "File sharing and private link generation"
scenarios:
  - "Upload local files to a Qiniu bucket"
  - "List and query files in a bucket with prefix filtering"
  - "Batch delete expired files from storage"
  - "Refresh CDN cache after updating resources"
  - "Create and manage sandbox environments"
  - "Generate private download links for restricted files"
  - "Migrate data from AWS S3 or Alibaba Cloud OSS to Qiniu"
---

# 七牛 KODO 资源操作 (qshell)

通过 `qshell` CLI 操作七牛云 KODO 对象存储及沙箱计算资源。

## 前置条件

qshell 通过系统 PATH 查找，直接使用 `qshell` 命令调用。

### 使用策略

**不要提前检查 qshell 是否安装。** 直接执行用户请求的 qshell 命令。仅当命令执行失败（如 `command not found`、`no such file or directory`、exit code 127）时，告知用户 qshell 未安装，并询问是否需要自动安装。获得用户同意后，执行 `references/install.sh` 安装（如需了解脚本细节可阅读 `references/install.md`），然后重新执行命令。

### 账号未配置时

如果命令返回 `bad token` / `unauthorized` / `401` 错误，提示用户运行：
```bash
qshell account <AccessKey> <SecretKey> <Name>
```

> **安全规则：** 当执行 `qshell account` 设置凭据时，**必须** 在命令前加一个空格，以防止 AccessKey 和 SecretKey 被记录在 shell 历史中。例如：` qshell account <AK> <SK> <Name>`

### 沙箱功能鉴权

沙箱相关命令需要配置环境变量：
- `QINIU_API_KEY` 或 `E2B_API_KEY`：API 密钥（必填）
- `QINIU_SANDBOX_API_URL` 或 `E2B_API_URL`：API 服务地址（可选）

优先级：`QINIU_*` > `E2B_*`

---

## 命令速查

### 1. 账号与 Bucket 管理

```bash
# 设置/查看当前账号
qshell account                                    # 查看当前账号
qshell account <AccessKey> <SecretKey> <Name>     # 设置账号

# 用户管理
qshell user ls                                    # 列出所有已配置账号
qshell user cu <Name>                             # 切换当前账号
qshell user current                               # 查看当前用户
qshell user lookup <Name>                         # 查看指定账号详情

# 列出所有 bucket
qshell buckets
qshell buckets --detail                           # 带详情
qshell buckets --region z0                        # 指定区域

# 查看 bucket 信息
qshell bucket <Bucket>

# 创建 bucket
qshell mkbucket <Bucket> --region z0              # 华东
qshell mkbucket <Bucket> --region z1              # 华北
qshell mkbucket <Bucket> --region z2              # 华南
qshell mkbucket <Bucket> --region na0             # 北美
qshell mkbucket <Bucket> --region as0             # 东南亚
qshell mkbucket <Bucket> --region z0 --private    # 创建私有 bucket

# 查看 bucket 绑定的域名
qshell domains <Bucket>
qshell domains <Bucket> --detail
```

### 2. 文件查询

```bash
# 查看单个文件信息
qshell stat <Bucket> <Key>

# 列举 bucket 中的文件
qshell listbucket2 <Bucket>                                # 列出所有文件
qshell listbucket2 <Bucket> -p <Prefix>                    # 按前缀列举
qshell listbucket2 <Bucket> -p <Prefix> --limit 100        # 限制数量
qshell listbucket2 <Bucket> -o result.txt                  # 输出到文件
qshell listbucket2 <Bucket> -r                             # 人类可读的文件大小
qshell listbucket2 <Bucket> -s 2024-01-01-00-00-00         # 起始时间
qshell listbucket2 <Bucket> -e 2024-12-31-23-59-59         # 结束时间
qshell listbucket2 <Bucket> --file-types 0,1               # 按存储类型过滤
qshell listbucket2 <Bucket> --min-file-size 1048576         # 最小文件大小 (1MB)
qshell listbucket2 <Bucket> --show-fields Key,FileSize,PutTime  # 指定显示字段

# 旧版列举（兼容）
qshell listbucket <Bucket> <OutputFile>

# 批量查看文件信息（从文件或 stdin 读取 key 列表）
qshell batchstat <Bucket> -i <KeyListFile>

# 校验本地文件与云端文件是否一致
qshell match <Bucket> <Key> <LocalFile>

# 批量校验
qshell batchmatch <Bucket> -i <KeyLocalFile>               # 每行: Key\tLocalPath
```

**listbucket2 输出格式（默认 tab 分隔）：**
```
Key    FileSize    Hash    PutTime    MimeType    FileType    EndUser
```

**存储类型 FileType：**
- 0: 标准存储 (STANDARD)
- 1: 低频存储 (IA)
- 2: 归档存储 (ARCHIVE)
- 3: 深度归档 (DEEP_ARCHIVE)
- 4: 归档直读 (ARCHIVE_IR)
- 5: 智能分层 (INTELLIGENT_TIERING)

### 3. 文件上传

**选择策略：** 文件 < 100MB 使用 `fput`（表单上传），>= 100MB 使用 `rput`（分片上传）。

```bash
# 表单上传（适合 < 100MB 的文件）
qshell fput <Bucket> <Key> <LocalFile>
qshell fput <Bucket> <Key> <LocalFile> --overwrite            # 覆盖同名
qshell fput <Bucket> <Key> <LocalFile> --file-type 1          # 上传为低频存储
qshell fput <Bucket> <Key> <LocalFile> -t image/png           # 指定 MIME 类型

# 分片上传（>= 100MB 的文件，支持断点续传）
qshell rput <Bucket> <Key> <LocalFile>
qshell rput <Bucket> <Key> <LocalFile> --overwrite
qshell rput <Bucket> <Key> <LocalFile> --resumable-api-v2     # 使用 v2 分片
qshell rput <Bucket> <Key> <LocalFile> -c 10                  # 10 个并发分片

# 批量上传目录
qshell qupload2 --src-dir <LocalDir> --bucket <Bucket>
qshell qupload2 --src-dir <LocalDir> --bucket <Bucket> --key-prefix "dir/" --overwrite
qshell qupload2 --src-dir <LocalDir> --bucket <Bucket> --thread-count 10
qshell qupload2 --src-dir <LocalDir> --bucket <Bucket> --skip-suffixes .tmp,.log
qshell qupload2 --src-dir <LocalDir> --bucket <Bucket> --check-exists   # 跳过已存在

# 旧版批量上传（使用配置文件）
qshell qupload <UploadConfigFile>
```

### 4. 文件下载

```bash
# 下载单个文件
qshell get <Bucket> <Key>
qshell get <Bucket> <Key> -o <LocalFile>                      # 指定保存路径
qshell get <Bucket> <Key> --domain <Domain>                   # 指定下载域名
qshell get <Bucket> <Key> --check-hash                        # 下载后校验 hash
qshell get <Bucket> <Key> --enable-slice                      # 分片下载大文件

# 批量下载
qshell qdownload2 --bucket <Bucket> --dest-dir <LocalDir>
qshell qdownload2 --bucket <Bucket> --dest-dir <LocalDir> --prefix "logs/"
qshell qdownload2 --bucket <Bucket> --dest-dir <LocalDir> -c 10     # 10 并发
qshell qdownload2 --bucket <Bucket> --dest-dir <LocalDir> --domain <Domain>
qshell qdownload2 --bucket <Bucket> --dest-dir <LocalDir> --key-file <KeyFile>

# 旧版批量下载（使用配置文件）
qshell qdownload <DownloadConfigFile>
```

### 5. 文件操作

```bash
# 复制文件
qshell copy <SrcBucket> <SrcKey> <DestBucket> -k <DestKey>
qshell copy <SrcBucket> <SrcKey> <DestBucket>                 # key 不变
qshell copy <SrcBucket> <SrcKey> <DestBucket> -k <DestKey> --overwrite

# 移动文件
qshell move <SrcBucket> <SrcKey> <DestBucket> -k <DestKey>
qshell move <Bucket> <OldKey> <Bucket> -k <NewKey>            # 同 bucket 重命名

# 重命名文件
qshell rename <Bucket> <OldKey> <NewKey>

# 删除文件
qshell delete <Bucket> <Key>

# 抓取远程资源到 bucket（大文件建议使用 sync 命令）
qshell fetch <RemoteURL> <Bucket> -k <Key>

# 同步远程大文件到 bucket（使用分片上传，支持断点续传，适合大文件）
qshell sync <SrcResUrl> <Bucket> -k <Key>
qshell sync <SrcResUrl> <Bucket> -k <Key> --overwrite
qshell sync <SrcResUrl> <Bucket> -k <Key> --file-type 1      # 指定存储类型

# 镜像更新（从源站重新拉取覆盖旧文件）
qshell mirrorupdate <Bucket> <Key>
qshell prefetch <Bucket> <Key>                     # 同 mirrorupdate

# 批量操作（从文件或 stdin 读取列表）
qshell batchcopy <SrcBucket> <DestBucket> -i <MapFile>        # 每行: SrcKey\tDestKey
qshell batchmove <SrcBucket> <DestBucket> -i <MapFile>
qshell batchdelete <Bucket> -i <KeyListFile>                   # 每行一个 key
qshell batchrename <Bucket> -i <OldNewKeyMapFile>              # 每行: OldKey\tNewKey
qshell batchfetch <Bucket> -i <URLKeyMapFile>                  # 每行: URL\tKey
```

> **安全提示：** 批量删除/移动操作默认需要输入验证码确认，可加 `-y` 跳过确认直接执行。执行前务必确认操作范围。
> 建议先用 `--success-list` 和 `--failure-list` 记录结果。

### 6. 文件属性修改

```bash
# 修改 MIME 类型
qshell chgm <Bucket> <Key> <NewMimeType>

# 修改存储类型
qshell chtype <Bucket> <Key> <FileType>   # 0/1/2/3/4/5

# 设置文件过期时间（天数，0 表示取消过期）
qshell expire <Bucket> <Key> <DeleteAfterDays>

# 禁用/启用文件访问
qshell forbidden <Bucket> <Key>              # 禁用
qshell forbidden <Bucket> <Key> -r           # 取消禁用

# 解冻归档文件（FreezeAfterDays: 1~7 天）
qshell restorear <Bucket> <Key> <FreezeAfterDays>

# 修改文件生命周期（转存储类型、过期删除）
qshell chlifecycle <Bucket> <Key> \
  --to-ia-after-days 30 \
  --to-archive-ir-after-days 60 \
  --to-archive-after-days 120 \
  --to-deep-archive-after-days 180 \
  --delete-after-days 365
# 设为 -1 表示取消对应的生命周期规则

# 批量操作
qshell batchchgm <Bucket> -i <KeyMimeFile>          # 每行: Key\tMimeType
qshell batchchtype <Bucket> -i <KeyTypeFile>         # 每行: Key\tFileType
qshell batchexpire <Bucket> -i <KeyDaysFile>         # 每行: Key\tDays
qshell batchforbidden <Bucket> -i <KeyListFile>
qshell batchrestorear <Bucket> -i <KeyDaysFile>      # 每行: Key\tFreezeAfterDays
qshell batchchlifecycle <Bucket> -i <LifecycleFile>  # 批量修改生命周期
```

### 7. CDN 操作

```bash
# 刷新 URL 缓存（从文件读取 URL 列表，每行一个 URL）
qshell cdnrefresh -i <URLListFile>
qshell cdnrefresh -i <URLListFile> -r          # 刷新目录

# 预取 URL（从文件读取 URL 列表）
qshell cdnprefetch -i <URLListFile>

# 也可以从 stdin 输入
echo "http://example.com/path/file.jpg" | qshell cdnrefresh
echo "http://example.com/path/file.jpg" | qshell cdnprefetch
```

### 8. 数据处理 (pfop)

```bash
# 触发持久化数据处理
qshell pfop <Bucket> <Key> <FopCommand>
qshell pfop <Bucket> <Key> <FopCommand> -p <Pipeline>         # 指定队列
qshell pfop <Bucket> <Key> <FopCommand> -u <NotifyURL>         # 通知 URL

# 查询处理状态
qshell prefop <PersistentId>
```

### 9. 私有链接与签名

```bash
# 生成私有资源访问链接
qshell privateurl <PublicURL>                      # 默认有效期
qshell privateurl <PublicURL> <Deadline>           # 指定 Unix 时间戳

# 生成带数据处理 + saveas 的 URL
qshell saveas <PublicUrlWithFop> <SaveBucket> <SaveKey>

# 批量签名（从文件读取 URL 列表）
qshell batchsign -i <URLListFile>

# 生成各类七牛 Token（交互式，AI 助手无法直接调用，需提示用户手动运行）
qshell token
```

### 10. 工具命令

```bash
# 解码七牛 reqid
qshell reqid <ReqId>

# 计算本地文件的 qetag
qshell qetag <LocalFilePath>

# Base64 编解码（URL 安全）
qshell b64encode <String>
qshell b64decode <EncodedString>

# RPC 编解码
qshell rpcencode <String>
qshell rpcdecode <EncodedString>

# URL 编解码
qshell urlencode <String>
qshell urldecode <EncodedString>

# 时间工具
qshell d2ts <Seconds>                    # N 秒后的时间戳
qshell tms2d <TimestampInMs>             # 毫秒时间戳转日期
qshell tns2d <TimestampInNs>             # 纳秒时间戳转日期
qshell ts2d <TimestampInSec>             # 秒级时间戳转日期

# IP 查询
qshell ip <IPAddress>

# 目录缓存（用于批量上传前生成文件列表）
qshell dircache <DirPath> -o <OutputFile>

# 解压 zip 文件（兼容 GBK/UTF8 文件名）
qshell unzip <ZipFilePath> --dir <UnzipToDir>

# Go 模板函数（验证模板格式）
qshell func <ParamsJson> <FuncTemplate>

# 查看版本
qshell version
```

### 11. 异步抓取与云迁移

```bash
# 异步批量抓取远程资源
qshell abfetch -i <URLKeyFile> <Bucket>

# 查询异步抓取状态
qshell acheck <Bucket> <Id> --zone <Zone>

# 从 AWS S3 列举
qshell awslist -A <AwsID> -S <AwsSecretKey> <AwsBucket> <AwsRegion>

# 从 AWS S3 迁移到七牛
qshell awsfetch -A <AwsID> -S <AwsSecretKey> <AwsBucket> <AwsRegion> <QiniuBucket>

# 从阿里云 OSS 列举
qshell alilistbucket <DataCenter> <Bucket> <AccessKeyId> <AccessKeySecret> [Prefix] <ListBucketResultFile>
```

### 12. 文件分享

```bash
# 创建分享链接
qshell create-share kodo://<Bucket>/<Prefix>
qshell create-share kodo://<Bucket>/<Prefix> --extract-code <Code>
qshell create-share kodo://<Bucket>/<Prefix> --validity-period 1h
qshell create-share kodo://<Bucket>/<Prefix> --output share.json

# 列举分享内容
qshell share-ls <ShareLink>                        # 使用分享链接
qshell share-ls share.json                         # 使用输出文件
qshell share-ls <ShareLink> --prefix <Prefix>      # 按前缀过滤
qshell share-ls <ShareLink> --limit 100            # 限制数量
qshell share-ls <ShareLink> --extract-code <Code>  # 指定提取码

# 从分享下载文件
qshell share-cp <ShareLink> --to <LocalDir>        # 下载文件
qshell share-cp <ShareLink> --to <LocalDir> -r     # 递归下载目录
qshell share-cp share.json --from <Path> --to <LocalDir>  # 下载指定文件
```

### 13. M3U8 操作

```bash
# 删除 M3U8 播放列表及其所有切片文件
qshell m3u8delete <Bucket> <M3u8Key>

# 替换/清除 M3U8 播放列表中的切片域名
qshell m3u8replace <Bucket> <M3u8Key>                         # 清除域名（相对路径）
qshell m3u8replace <Bucket> <M3u8Key> <NewDomain>             # 替换为新域名
```

### 14. 沙箱管理

需要配置 `QINIU_API_KEY` 或 `E2B_API_KEY` 环境变量。

别名：`sandbox` = `sbx`

```bash
# 列出沙箱
qshell sandbox list                                # 列出运行中的沙箱
qshell sbx ls                                      # 使用别名
qshell sandbox list -s running,paused              # 按状态过滤
qshell sandbox list -m key=value                   # 按元数据过滤
qshell sandbox list -f json                        # JSON 格式输出

# 创建沙箱（默认自动连接终端）
# ⚠ AI 助手应始终使用 -d（分离模式），避免交互式终端阻塞
qshell sandbox create <TemplateID> -d
qshell sbx cr <TemplateID> -d
qshell sandbox create <TemplateID> -d -t 300          # 设置超时 300 秒
qshell sandbox create <TemplateID> -d -m env=dev      # 添加元数据

# 连接到已有沙箱终端
qshell sandbox connect <SandboxID>
qshell sbx cn <SandboxID>

# 在沙箱中执行命令
qshell sandbox exec <SandboxID> -- <Command>
qshell sbx ex <SandboxID> -- ls -la
qshell sandbox exec <SandboxID> -b -- python server.py    # 后台运行
qshell sandbox exec <SandboxID> -c /app -- npm install    # 指定工作目录
qshell sandbox exec <SandboxID> -e PORT=3000 -- node app.js  # 设置环境变量

# 终止沙箱
qshell sandbox kill <SandboxID>
qshell sbx kl <SandboxID>
qshell sandbox kill -a                             # 终止所有
qshell sandbox kill -a -m user=alice               # 按元数据过滤终止

# 暂停/恢复沙箱
qshell sandbox pause <SandboxID>
qshell sbx ps <SandboxID>
qshell sandbox pause -a                            # 暂停所有
qshell sandbox resume <SandboxID>
qshell sandbox resume -a                           # 恢复所有

# 查看沙箱日志
qshell sandbox logs <SandboxID>
qshell sbx lg <SandboxID>

# 查看沙箱资源指标
qshell sandbox metrics <SandboxID>
qshell sbx mt <SandboxID>
```

### 15. 沙箱模板管理

别名：`sandbox template` = `sbx tpl`

```bash
# 列出模板
qshell sandbox template list
qshell sbx tpl ls

# 查看模板详情
qshell sandbox template get <TemplateID>
qshell sbx tpl gt <TemplateID>

# 删除模板
qshell sandbox template delete <TemplateID> -y
qshell sbx tpl dl <TemplateID> -y

# 构建模板
qshell sandbox template build --name <Name> --from-image ubuntu:22.04 --wait
qshell sbx tpl bd --name <Name> --from-image ubuntu:22.04 --wait

# 查看构建状态
qshell sandbox template builds <TemplateID> <BuildID>
qshell sbx tpl bds <TemplateID> <BuildID>

# 发布/取消发布模板
qshell sandbox template publish <TemplateID> -y
qshell sandbox template unpublish <TemplateID> -y

# 初始化模板项目脚手架
qshell sandbox template init
qshell sandbox template init --name my-template --language go
qshell sandbox template init --name my-api --language typescript --path ./my-api
```

**支持的语言：** go, typescript, python

---

## 用户意图到操作的映射

下表仅列出存在歧义或需要判断的场景，简单的一对一映射请参考命令速查部分。

| 用户说 | 操作 | 判断依据 |
|--------|------|----------|
| "上传文件到七牛" | `qshell fput`（< 100MB）/ `qshell rput`（>= 100MB） | 根据文件大小选择 |
| "批量上传" | `qshell qupload2` | 上传整个目录 |
| "从远程 URL 抓取文件" | `qshell fetch`（小文件） / `qshell sync`（大文件或需断点续传） | fetch 适合小文件，sync 支持分片和断点续传 |
| "同步文件到七牛" | `qshell sync` | 大文件或需断点续传时优先 |
| "从 S3 迁移" | `qshell awsfetch` | 需要 AWS 凭据 |
| "从阿里云迁移" | `qshell alilistbucket` + `qshell batchfetch` | 先列举再批量抓取 |
| "刷新 CDN" | `qshell cdnrefresh` | URL 刷新 |
| "预热 CDN" | `qshell cdnprefetch` | URL 预取 |
| "改一下存储类型" | `qshell chtype`（单文件） / `qshell batchchtype`（批量） | 根据操作规模选择 |
| "设置文件生命周期" | `qshell chlifecycle`（单文件） / `qshell batchchlifecycle`（批量） | 根据操作规模选择 |
| "移动文件" / "重命名文件" | `qshell rename`（同 bucket）/ `qshell move`（跨 bucket） | 根据是否跨 bucket 选择 |
| "删除 m3u8" | `qshell m3u8delete` | 会同时删除所有切片文件 |
| "创建沙箱" | `qshell sandbox create <TemplateID> -d` | AI 助手必须使用 -d 分离模式 |
| "生成 token" | `qshell token` | 交互式命令，提示用户手动运行 |

---

## 安全规则

### 危险操作（必须与用户确认后再执行）

- `qshell account <AK> <SK> <Name>` — 会覆盖当前账号配置，涉及凭据安全
- `qshell delete` / `qshell batchdelete` — 删除文件不可恢复
- `qshell move` / `qshell batchmove` — 源文件会被删除
- `qshell rename` / `qshell batchrename` — 重命名实质是移动
- `qshell forbidden` — 禁用文件访问
- `qshell batchexpire` — 批量设置过期可能导致数据丢失
- `qshell m3u8delete` — 删除 M3U8 及所有切片文件
- `qshell sandbox kill` / `qshell sandbox kill -a` — 终止沙箱
- `qshell sandbox connect` — 交互式终端，AI 助手无法操作，需提示用户手动执行
- `qshell sandbox template delete` — 删除模板
- 任何带 `--overwrite` 的上传/复制/同步操作
- `qshell token` — 交互式命令，AI 助手无法操作，需提示用户手动执行

### 安全操作（可直接执行）

- 所有查询类：`stat`、`listbucket2`、`buckets`、`bucket`、`domains`、`prefop`、`batchstat`
- 工具类：`reqid`、`qetag`、`match`、`b64encode`、`b64decode`、`urlencode`、`urldecode`、`rpcencode`、`rpcdecode`、`ip`、`d2ts`、`tms2d`、`tns2d`、`ts2d`、`func`、`dircache`、`unzip`、`version`
- 链接生成：`privateurl`、`saveas`、`batchsign`、`create-share`
- 分享查看：`share-ls`
- 沙箱查询：`sandbox list`、`sandbox logs`、`sandbox metrics`、`sandbox template list`、`sandbox template get`、`sandbox template builds`、`sandbox template init`

---

## 输出格式

### 文件信息 (stat)

```
## 文件信息: <Bucket>/<Key>

| 属性 | 值 |
|------|-----|
| Key | path/to/file.jpg |
| 大小 | 1.5 MB |
| Hash | Fh8... |
| MIME | image/jpeg |
| 存储类型 | 标准存储 |
| 上传时间 | 2024-03-01 10:30:00 |
```

### 文件列表 (listbucket2)

```
## <Bucket> 文件列表 (前缀: <Prefix>)

| Key | 大小 | MIME | 存储类型 | 上传时间 |
|-----|------|------|----------|----------|
| file1.jpg | 1.5 MB | image/jpeg | 标准 | 2024-03-01 |
| file2.pdf | 3.2 MB | application/pdf | 低频 | 2024-02-15 |

共 N 个文件，总大小 X MB
```

### 沙箱列表 (sandbox list)

```
## 沙箱列表

| SANDBOX ID | TEMPLATE ID | STATE | vCPUs | RAM MiB | STARTED AT |
|------------|-------------|-------|-------|---------|------------|
| sb-xxx | tmpl-xxx | running | 2 | 512 | 2024-03-01 10:00 |
```

---

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| `command not found` / exit 127 | qshell 未安装，执行 `references/install.sh` 安装 |
| `no such file or directory` | 检查本地文件路径 |
| `no such bucket` / `631` | 检查 bucket 名称，用 `qshell buckets` 列出可用 bucket |
| `no such file or key` / `612` | 检查文件 key 是否正确 |
| `bad token` / `unauthorized` / `401` | 账号配置问题，提示 `qshell account` 重新配置 |
| `bucket not match` | 操作的 bucket 与 key 不匹配 |
| `file exists` / `614` | 文件已存在，需要加 `--overwrite` 选项 |
| `403` | 权限不足 |
| `API key not configured` | 沙箱功能需设置 `QINIU_API_KEY` 环境变量 |
| `sandbox not found` | 检查沙箱 ID，用 `qshell sandbox list` 查看 |
| `template not found` | 检查模板 ID，用 `qshell sandbox template list` 查看 |
