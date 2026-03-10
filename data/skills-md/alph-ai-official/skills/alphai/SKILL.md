---
name: alphai
description: Alph.ai API 主导航 - 帮助查找合适的 API 模块、生成调用代码、提供 API 使用建议。当用户不确定使用哪个模块或需要 API 总览时使用。
argument-hint: [你的问题或需求]
---

# Alph.ai API 导航中心

欢迎使用 Alph.ai API Skills！本系统包含 **208 个 API**，分为 6 个功能模块。

## 🔑 认证与连接（必读）

使用任何 API 前，你需要先了解认证方式。完整说明见 [auth-guide.md](auth-guide.md)，核心流程：

```
1. 浏览器登录 alph.ai
2. DevTools → Application → Cookies → alph.ai → 复制 dex_cookie
3. 所有请求 Header 携带: Cookie: dex_cookie=<value>     （有效期14天）
4. 需要 WebSocket 时: POST /smart-web-gateway/ws/listenkey → 获取 listenKey
5. 连接: wss://ws.alph.ai/stream/ws?listenKey=<listen_key>
6. listenKey 默认1小时过期，需要自动续期
```

---

## 📦 可用模块

### 1. `/alphai-trading` - 交易模块 (54 个 API)
**功能**：买卖交易、挂单、跟单、订单查询、手续费
**使用场景**：
- 下单、撤单、改单
- 设置买单/卖单参数
- 挂单管理
- 跟单功能
- 订单查询和统计

**示例**：
```
/alphai-trading 查询下单接口
/alphai-trading 如何设置止损止盈？
```

---

### 2. `/alphai-market` - 行情模块 (41 个 API)
**功能**：币种详情、实时行情、热门币种、市场数据、WebSocket 推送
**使用场景**：
- 查询币价和行情
- 获取热门币种
- 实时数据推送
- 扫链数据
- Gas 费查询

**示例**：
```
/alphai-market 查询 ETH 实时价格接口
/alphai-market WebSocket 如何订阅行情？
```

---

### 3. `/alphai-user` - 用户模块 (67 个 API)
**功能**：注册登录、账户管理、钱包、活动、分销
**使用场景**：
- 用户注册和登录
- 账户安全设置
- 钱包管理
- 空投和 VIP 活动
- 邀请返佣

**示例**：
```
/alphai-user 查询注册登录接口
/alphai-user 如何管理用户钱包？
```

---

### 4. `/alphai-twitter` - 社媒推特(X) (7 个 API)
**功能**：X 账户监控、热门监控、关注管理、监控配置、翻译
**使用场景**：
- 监控 KOL 推特动态（转发、引用、头像更新）
- 查看热门监控列表
- 关注/取消关注 X 账户
- 自定义推特监控配置
- 推特内容翻译

**示例**：
```
/alphai-twitter 如何监控某个 KOL？
/alphai-twitter 查看热门监控列表接口
```

---

### 5. `/alphai-smart` - 智能功能 (31 个 API)
**功能**：聪明钱包、Tracker 追踪、信号源、Bot 机器人
**使用场景**：
- 智能钱包分析
- 链上地址追踪
- 交易信号监控
- 机器人自动化

**示例**：
```
/alphai-smart 查询聪明钱包接口
/alphai-smart 如何追踪特定地址？
```

---

### 6. `/alphai-common` - 公共模块 (8 个 API)
**功能**：公共接口、黑名单、SEO、分享
**使用场景**：
- 通用配置接口
- 黑名单管理
- SEO 优化
- 分享功能

**示例**：
```
/alphai-common 查询公共配置接口
```

---

## 💡 使用建议

### 如果你知道要什么
直接使用具体模块：
```
/alphai-trading 下单接口
/alphai-market 获取 BTC 价格
```

### 如果你不确定
使用本导航 skill：
```
/alphai 我想做交易
/alphai 如何获取币价？
/alphai 用户注册怎么实现？
```

### 如果让 Claude 自动选择
直接提问，Claude 会自动调用合适的模块：
```
帮我查询下单的 API
我想获取 ETH 的实时价格
用户注册需要哪些接口？
```

---

## 🔧 通用功能

所有模块都支持：
1. **查询 API**：搜索和浏览 API 列表
2. **查看详情**：查看完整的请求参数和响应格式
3. **生成代码**：自动生成 Python、JavaScript、TypeScript 等语言的调用代码
4. **使用建议**：提供最佳实践和注意事项

---

## 📚 工作流程

当你提问时，我会：
1. 理解你的需求
2. 推荐合适的模块
3. 调用对应的 skill 获取详细信息
4. 生成可用的代码示例
5. 提供集成建议

---

**需要帮助？** 告诉我你想做什么，我会帮你找到合适的 API！

当前问题：$ARGUMENTS
