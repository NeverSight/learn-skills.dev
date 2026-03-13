---
name: clash-meta-proxy
description: Update clash-meta proxy configuration. Use when updating proxy nodes for clash-meta service, editing config.yaml with new proxies from .proxies.yaml, or maintaining proxy-groups consistency. Use the provided Python script with uv for automated backup, proxy update, and proxy-groups review.
---

# Clash-Meta 配置更新

更新服务器的 clash-meta 代理配置。

## 环境信息

- **默认工作目录**: `./`
- **现配置文件**: `config.yaml`
- **新代理配置**: `.proxies.yaml`

## 使用脚本自动化（推荐）

提供 PEP 723 内联元数据脚本，支持 `uv run` 直接运行，无需手动安装依赖。

### 运行方式

**方式一：直接运行（推荐）**
```bash
# In the work_dir
uv run scripts/update_clash_config.py
```

**方式二：指定工作目录运行**
```bash
uv run --cwd ./ scripts/update_clash_config.py
```

脚本自动完成：
- 文件备份（`config.yaml.bak` + 时间戳备份 + `config.yaml.editing`）
- 读取 `.proxies.yaml` 并完整覆盖 `proxies`
- 核验 `proxy-groups`，注释失效代理
- 生成 diff 到控制台和 `.update.diff`

## 人工确认与生效（关键步骤）

脚本**不会**自动重命名文件，需人工确认后执行：

1. **检查 diff 输出**
```bash
cat ./.update.diff
```

2. **确认无误后生效**
```bash
mv ./config.yaml.editing ./config.yaml
```

## 手动操作流程

若脚本无法使用，按以下步骤手动操作：

1. **备份配置**
   - 复制 `config.yaml` 为 `config.yaml.bak`
   - 复制 `config.yaml` 为 `config.yaml.editing`

2. **更新 proxies 配置**
   - 读取 `.proxies.yaml` 获取新代理节点
   - 用新代理列表完整覆盖 `config.yaml.editing` 中的 `proxies` 字段

3. **核验 proxy-groups**
   - 检查 `proxy-groups[*].proxies` 引用的 name 是否存在于 `proxies` 列表
   - 若发现失效代理，注释掉而非删除

4. **diff 确认并重命名**
   - 执行 `diff config.yaml.bak config.yaml.editing` 对比
   - 确认无误后，将 `config.yaml.editing` 重命名为 `config.yaml`

## 配置示例

### .proxies.yaml 结构

```yaml
proxies:
  - name: hy2.node.proxychain.top
    type: hysteria2
    server: IP
    port: PORT
    password: PASSWORD
    sni: hy2.node.proxychain.top
    skip-cert-verify: false
```

### proxy-groups 结构

```yaml
proxy-groups:
  - name: G-SELECT
    type: select
    proxies:
      # - 失效节点名    # 已失效，需注释
      - hy2.node.proxychain.top   # 有效节点
```

## 注意事项

- `proxy-groups[*].proxies` 引用的 name 必须与 `proxies[*].name` 严格对应
- 仅注释失效代理名，保留配置结构完整
- 始终保留 `config.yaml.bak` 以便回滚
- 最终重命名操作必须由人工确认后执行
