---
name: singbox-config
description: "Generate, modify, migrate, and debug version-aware sing-box client configuration files for v1.13 and v1.14. Covers TUN and system proxy modes for end-user devices (SFM/SFA/SFI/CLI), RealIP vs FakeIP TUN templates, DNS/routing split rules, remote rule-set downloads, Clash API selectors, and node conversion for VLESS/VMess/Shadowsocks/Trojan/Hysteria2/TUIC/ShadowTLS/AnyTLS. Use when the user mentions sing-box, singbox, SFM/SFA/SFI, TUN/system proxy setup, split routing, DNS hijack, FakeIP, selector behavior, per-app routing, network strategy, TLS fragment/ECH, proxy chaining, or asks to create, update, migrate, or troubleshoot a client config. Does not cover server-side proxy inbound setup."
---

# sing-box 客户端配置生成器

生成适用于中国用户的生产级 sing-box **客户端**配置，包含分流路由。本 skill 必须按目标版本生成配置，默认版本由版本表维护，避免跨版本字段误用导致警告、启动失败或网络完全瘫痪。

**覆盖范围：** 客户端（连接到代理服务器的终端设备）— TUN/VPN、system proxy、manual mixed/socks/http、SFM/SFA/SFI 图形客户端、命令行 `sing-box run`。

**不覆盖：** 服务端配置（搭建代理服务器）、服务端 inbound 监听、服务端 TLS/ACME/Reality、透明代理网关服务端部署。服务端问题应提示本 skill 只覆盖客户端，并参考官方 inbound 文档。

## Reference 路由

先按任务读取最小必要 reference，不要一次加载全部：

| 任务 | 读取 |
|------|------|
| 生成新配置、选择版本/模板、默认值、摘要格式 | `references/workflow.md` |
| TUN、system proxy、manual mixed/http、platform.http_proxy、平台行为 | `references/network-modes.md` |
| DNS hijack、RealIP、FakeIP、DNS 延迟、IPv6 策略 | `references/dns-routing.md` |
| Clash/V2Ray 节点转换到 sing-box outbound | `references/node-conversion.md` |
| geosite/geoip、rule-set URL、自定义分流规则 | `references/rule-sets.md` |
| 字段、版本矩阵、schema 级兼容性 | `references/config-schema.md` |
| 机制排查、连接生命周期、常见陷阱、源码验证 | `references/cookbook.md` |
| 1.13 TUN RealIP 模板（默认） | `references/templates/config-1.13-tun.json` |
| 1.13 TUN FakeIP 模板 | `references/templates/config-1.13-tun-fakeip.json` |
| 1.14 TUN RealIP 模板 | `references/templates/config-1.14-tun-realip.json` |
| 1.14 TUN FakeIP 模板 | `references/templates/config-1.14-tun-fakeip.json` |

`references/template.json` 必须等价于当前默认版本模板；截至 2026-07-03 为 `references/templates/config-1.13-tun.json`。

## 生成入口流程

生成**新配置**时，读取 `references/workflow.md`，按“入口判断 + 最少问题”执行：

- 只有生成意图、无节点信息：询问生成方案。
- 已提供节点信息、无方案：解析节点，默认使用 `1.13 TUN RealIP` 和模板内置规则。
- 已提供节点信息和方案：不要重复询问方案。
- 已提供分流/规则诉求：进入自定义规则流程，并按需读取 `references/rule-sets.md`。
- 修改已有配置：不要启动完整向导，只询问当前变更缺失的信息。
- 节点格式无法识别：只询问节点格式或缺失协议字段，不展开其它问题。

如果当前运行时支持结构化选择控件且允许使用，优先用控件提问；否则使用简短文本问题。不要在 skill 中承诺任何特定 UI 形态。

生成前必须回显摘要；用户已明确要求生成时，摘要后直接生成，不额外确认。

## 默认值

- 默认方案：`1.13 TUN RealIP`（兼容性优先）
- 默认运行方式：TUN/VPN
- 默认 DNS/IP 策略：IPv4-only
- `1.13 TUN` 和 `1.14 TUN` 默认模板：RealIP 模板（兼容性优先）
- 默认规则：模板内置规则（国内直连、广告拦截、常见海外服务代理、已有服务 selector）
- 默认启用 Clash API 和服务 selector
- 默认不配置平台包名排除
- 默认输出：直接返回 JSON；只有用户要求写文件时才写文件

如果用户主要诉求是 DNS 延迟，不要推荐 FakeIP；优先使用版本可用的 DNS 缓存/乐观缓存策略。

## 版本表

版本选项按版本号倒序展示：

| 版本 | 默认状态 | 模板 |
|------|----------|------|
| `1.14` | 可选 | `config-1.14-tun-realip.json` 或 `config-1.14-tun-fakeip.json` |
| `1.13` | **默认** | `config-1.13-tun.json` 或 `config-1.13-tun-fakeip.json` |

截至 2026-07-03，默认版本为 `1.13`；1.14 按 alpha/preview 线处理。未来版本状态变化时，只更新版本表和默认模板指向，不要把“推荐”硬编码到正文其它位置。

## 模板选择

### 1.13 TUN RealIP

默认正式版本模板。使用 `references/templates/config-1.13-tun.json`。无 FakeIP，启用 `dns.reverse_mapping: true`，并保留 1.13 可用字段如 `independent_cache`、`store_rdrc`、remote rule-set `download_detour`。

1.13 已支持 RealIP 所需的 `reverse_mapping`。1.14 的优势是 `dns.optimistic`、`store_dns`、HTTP client 与 DNS rule 新能力，不是 RealIP 从无到有。

`reverse_mapping` 只记录已返回的真实 IP -> domain，帮助路由阶段匹配域名规则；它本身不防 DNS 污染。RealIP 模板必须用 DNS rule 将明确代理/海外域名送到 remote DNS。

### 1.13 TUN FakeIP

仅在用户明确需要更确定的连接 IP -> 域名恢复或 legacy FakeIP 行为时使用。使用 `references/templates/config-1.13-tun-fakeip.json`。不要因为普通 DNS 延迟单独选择 FakeIP。

### 1.14 TUN RealIP

默认 1.14 TUN 模板。使用 `references/templates/config-1.14-tun-realip.json`。无 FakeIP，启用 `dns.reverse_mapping: true`、`store_dns`，并使用 1.14 HTTP client 配置。

### 1.14 TUN FakeIP

仅在用户明确需要更确定的连接 IP -> 域名恢复时使用。使用 `references/templates/config-1.14-tun-fakeip.json`。不要因为普通 DNS 延迟单独选择 FakeIP。

## 必须遵守的硬规则

### 路由顺序

所有 TUN 模板的路由前两条必须保持：

```json
{ "action": "sniff" },
{
  "type": "logical",
  "mode": "or",
  "rules": [{ "protocol": "dns" }, { "port": 53 }],
  "action": "hijack-dns"
}
```

不要只用 `"protocol": "dns"` 做 DNS 劫持；需要 `protocol dns OR port 53`。

### v1.13+ 新模板避免的 legacy/special 用法

新模板避免以下 legacy/special 用法：

- `"type": "dns"` outbound；1.13 已移除，改用 `"action": "hijack-dns"`。
- `"type": "block"` outbound；当前仍可用，但普通阻断优先用 `"action": "reject"`，只有 selector 需要一个可选阻断出站时才使用 `type: "block"`。
- `"outbound": "any"` DNS 规则；改用 outbound `domain_resolver` 或 route `default_domain_resolver`。

### v1.14 模板字段门控

1.14 模板不要使用：

- `independent_cache`
- `store_rdrc`
- remote rule-set `download_detour`

1.14 remote rule-set 必须显式使用 `http_client` 或 `route.default_http_client`，不要依赖隐式默认 HTTP client。

### IPv6 默认

除非用户确认真实网络 IPv6 可用并要求完整 IPv6 TUN，否则：

- DNS 使用 `"strategy": "ipv4_only"`。
- TUN inbound 只配置 IPv4 地址。
- 不给 TUN 配 IPv6 地址。

IPv6 机制和 HTTPDNS 绕过原因见 `references/dns-routing.md`。

### 防泄漏

在 `ip_is_private -> direct` 后拒绝 DoT 和 STUN；不要全局拒绝 UDP 443/QUIC。

## 路由决策原则

- 从路由语义出发，不要从 DNS 语义出发。
- 用户说“域名必须走代理”：在 CN/直连兜底规则前添加显式 route 规则；RealIP 且默认 DNS 是国内 DNS 时，同时添加 remote DNS 规则。
- 用户说“域名必须直连”：同时添加 DNS 规则和 route 规则，放在 CN/代理兜底前。
- 不根据站点语言、品牌或 TLD 猜测 `geosite-cn` 成员关系；需要时查官方或可信 rule-set。
- GUI / Clash API 当前 selector 状态是运行时事实，不要假设 JSON 中 `"default"` 就是当前选择。

## 验证

完成文档或模板变更后至少运行：

```bash
jq empty references/template.json references/templates/*.json
python3 /Users/shpirt/skills/.system/skill-creator/scripts/quick_validate.py /Users/shpirt/playground/singbox-config
```

如果本机 Python 缺少 PyYAML，可用临时 `PYTHONPATH` 安装目录运行，不要把依赖写入 skill 仓库。
