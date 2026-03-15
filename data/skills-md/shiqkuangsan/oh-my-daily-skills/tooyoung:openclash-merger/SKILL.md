---
name: tooyoung:openclash-merger
description: "将 vless+reality 等新协议配置转换为带 ACL4SSR Full NoAuto 规则的配置文件，支持分组+分流，可直接上传 OpenClash 使用。触发词：合并 OpenClash、转换订阅、Clash 配置"
metadata:
  version: "1.0.0"
---

# OpenClash 订阅配置合并

将提供商的代理节点与 ACL4SSR Full NoAuto 规则合并，生成可用于 OpenClash 的完整配置。

## 前置依赖

- **Node.js** - 脚本使用 Node.js 处理 YAML

## 为什么需要这个工具

- 部分提供商仅提供完整配置，不提供原始订阅链接
- vless+reality 等新协议无法被 subconverter 解析
- 需要使用 ACL4SSR 等高质量规则集替换提供商规则

## 使用方法

```bash
# 进入 skill 目录
cd /path/to/openclash-merger

# 从订阅链接生成
./scripts/merge.sh "https://xxx.com/sub/xxx/clash"

# 从本地文件生成
./scripts/merge.sh /path/to/provider.yaml

# 指定输出文件
./scripts/merge.sh "订阅链接" ~/Downloads/my-config.yaml
```

默认输出到 `~/Downloads/openclash_merged.yaml`

## 目录结构

```
openclash-merger/
├── SKILL.md              # 本文件
├── scripts/
│   └── merge.sh          # 合并脚本
└── assets/
    ├── template.yaml     # ACL4SSR proxy-groups 模板
    └── rules.yaml        # ACL4SSR Full NoAuto 规则 (~10400 条)
```

## 工作原理

1. **获取配置** - 从订阅链接下载或读取本地文件
2. **提取节点** - 从 `proxies:` 部分提取所有代理节点
3. **分类节点** - 按地区关键字分类（香港/日本/美国/新加坡/台湾/韩国/其他）
4. **填充模板** - 将节点填入 ACL4SSR 模板的占位符
5. **合并规则** - 附加完整的 ACL4SSR 分流规则
6. **输出文件** - 生成可直接导入 OpenClash 的配置

## 策略组

| 策略组      | 说明                  |
| ----------- | --------------------- |
| 🚀 节点选择 | 主选择，默认香港      |
| 🚀 手动切换 | 包含所有节点          |
| 📲 电报消息 | Telegram              |
| 💬 Ai平台   | ChatGPT/Claude/Gemini |
| 📹 油管视频 | YouTube               |
| 🎥 奈飞视频 | Netflix               |
| 📺 哔哩哔哩 | B站                   |
| Ⓜ️ 微软Bing | Bing + Copilot        |
| 🎯 全球直连 | 直连                  |
| 🛑 广告拦截 | 广告                  |
| 🐟 漏网之鱼 | 未匹配流量            |

## 地区节点组（url-test 自动测速）

🇭🇰 香港 | 🇯🇵 日本 | 🇺🇲 美国 | 🇸🇬 狮城 | 🇨🇳 台湾 | 🇰🇷 韩国

## 节点分类规则

按节点名中的关键字匹配：

| 地区   | 关键字                      |
| ------ | --------------------------- |
| 香港   | 香港, HK, Hong Kong         |
| 日本   | 日本, JP, Japan             |
| 美国   | 美国, US, USA, America      |
| 新加坡 | 新加坡, SG, Singapore, 狮城 |
| 台湾   | 台湾, TW, Taiwan            |
| 韩国   | 韩国, KR, Korea             |

未匹配的节点归入"其他"，会包含在"手动切换"组中。

## 故障排查

### 配置加载失败

检查 OpenClash 日志：

- `proxy [xxx] not found` → 策略组名不匹配
- 节点 `not found` → 节点组引用了不存在的节点

### 节点分类异常

节点名需包含地区关键字才能正确分类。不含关键字的节点会归入"其他"。

## 自定义

### 修改模板

编辑 `assets/template.yaml` 可自定义策略组结构。占位符：

- `{{PROXIES}}` - proxies 部分
- `{{ALL_NODES}}` - 所有节点
- `{{HK_NODES}}` / `{{JP_NODES}}` / ... - 各地区节点

### 更新规则

替换 `assets/rules.yaml` 可使用其他规则集。
