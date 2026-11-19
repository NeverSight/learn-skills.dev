---
name: modbus-template-upload
description: 将用户指定的 Modbus Connector 模板 JSON 上传到 WebDAV 模板目录，保留其他模板并创建版本快照。首次上传地址必须由用户手动输入，配置持久化在技能目录之外；用于上传、发布模板或修改上传目标，不用于生成模板或同步工作区。
---

# 上传 Modbus 模板

使用 `scripts/upload_templates.py`。脚本复用 Modbus Connector 的无 Qt WebDAV
客户端，兼容应用的 `.catalog.json` 与 `.versions/` 历史格式，不只是上传孤立文件。
技能可以独立安装，但运行脚本的 Python 环境需有本项目的 `modbus_connector` 包。
优先使用用户现有的项目虚拟环境；若没有，在独立虚拟环境安装此仓库的 headless 包
（`python -m pip install 'git+https://github.com/sytuacmdyh/modbus_connector.git@v0.16.0'`），
无需 Python GUI 依赖。不要把依赖或用户配置装入技能目录。

下列 `<script>` 指本 SKILL.md 同目录下的 `scripts/upload_templates.py`。

## 上传地址由用户提供

先运行 `python <script> config-show`。

- 未配置时，询问用户完整的 **WebDAV 模板目录 URL** 和用户名（若需要认证）。
  地址必须由用户手动输入，例如用户提供 `https://host/dav/templates` 后，
  该 URL 就是目标目录，不再自动附加 `templates`。
- 不从源码、其他应用设置、云缓存、历史日志或环境变量中猜测/复制上传地址。
  不把示例地址当作真实配置。用户修改地址时同样只接受其明确输入。
- 保存后可跨项目复用，无需每次重填。上传前说明当前目标与将上传的模板；
  用户已明确要求上传这些文件时直接执行，不重复要求批准。

保存配置（使用用户实际输入，正确进行 shell 引用）：

```bash
python <script> configure --url '<用户输入的模板目录URL>' --username '<用户名或空字符串>'
```

默认配置文件为 `~/.modbus_connector/skills/template-upload/config.json`。
`MODBUS_TEMPLATE_UPLOAD_HOME` 可指定外部配置目录；它不能位于当前技能目录内
（包括软链接解析后的路径）。技能升级/重装不修改这个文件。它与 Flutter 的
`cloud.json`、工作区设置和模板缓存互相独立，不提交到 Git，不作为上传内容。
默认只保存 URL、用户名和超时。认证密码通过 `MODBUS_TEMPLATE_UPLOAD_PASSWORD`
环境变量提供，或由用户在交互终端隐藏输入。用户明确要求保存凭据时，可为 configure
添加 `--remember-password`：从环境变量或隐藏输入获取密码，明文保存在同一外部配置文件，
文件权限设为 0600（Windows 原生环境还受目录 ACL 控制）。不在技能目录保存凭据。
读取优先级为环境变量、已保存密码、交互输入；`config-show` 只显示是否已保存密码。
再次 configure 不加该选项会移除旧密码，避免更换账号时沿用旧凭据。
不要要求用户把密码发在聊天中，也不要把密码拼进命令行、URL 或显示在输出中。

## 选择文件、预览与发布

只选用户请求的模板 JSON，不包含 `.sources.md`、工作区、个人模板历史或配置文件。
输入应按 `<Manufacturer>/<Device>.json` 放置，父目录名和文件名构成远端资源键。
只有一个文件且目录结构不符时，用 `--resource 'Manufacturer/Device.json'` 明确资源键。
若同名资源已经存在，上传将替换这个模板，预览会标为 replace。

脚本在任何远端读取前校验所选文件中的可选概览：`overview_id` 唯一性、区块引用、
旧式 row 下标、宽度比例和数值颜色规则；重复 JSON 键也会拒绝。引用无效时先修复本地文件，
不靠发布后客户端忽略错误。支持顶层 `draft` 及旧式 `registers_options.flutter.draft`，
后者浅合并覆盖前者。生成或修改配置时按目标版本的加载实现核对；概览颜色仅支持 red/yellow。

上传完整保留寄存器 ID、区块和内容顺序、颜色规则以及已有表格偏好，不重建 ID、不迁移
draft、不补默认布局字段；缺失的概览、`rules` 和隐藏列配置保持缺失，显式空数组保持为空。
只改概览也属于模板替换，版本快照和回读均核对完整 JSON。对其他远端模板只做原有目录格式
检查，保留其内容，不因新增概览规范擅自改写或阻止发布无关模板。

```bash
python <script> upload /path/Manufacturer/Device.json
python <script> upload /path/Manufacturer/Device.json --publish
```

无 `--publish` 时只验证文件、读取远端目录并打印新增/替换/未变化清单，不执行远端写入。
实际上传前先运行预览；如果发现目标文件或同名替换超出用户授权范围，再澄清。
每次 publish 都重新读取远端，只合并指定模板，保留其他模板；没有变化时不创建版本。
目录不存在时允许在其已存在的 WebDAV 父目录下创建，父目录不会递归补建。

脚本先写完整版本快照，再更新 `.catalog.json`，最后回读核验。
只有旧式文件目录时会先读取旧模板，随后发布统一索引。不会删除旧文件或历史版本，
也不会更改本地应用云缓存。应用下载时优先读取新索引。

## 故障与交付

- 本地文件无效、远端索引损坏、认证失败、连接失败或重定向时停止，不把错误当空目录。
  HTTPS 使用默认证书校验，不跟随重定向传递凭据。
- 发布步骤报错时不要自动反复重试写入。先只读核对远端：索引写入可能已经成功，
  或仅留下未激活的历史快照。说明实际可确认的状态，再按用户原始授权处理。
- 现有发布协议没有 ETag 条件更新，不保证多个发布者同时写入时的原子合并。
  同一目录应串行发布；若用户要求并发发布，先解决服务端条件更新再使用。
- 完成后报告目标 URL、资源键、新增/替换数量、版本号和回读结果；不要展示密码。
  此技能本身的创建/安装不是上传授权，未获得用户提供的地址时不访问实际服务器。
