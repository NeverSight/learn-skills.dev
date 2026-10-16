---
name: security-and-hardening
description: 加固代码以防漏洞。用于审计某个输入处理函数是否存在漏洞、处理用户输入、认证、数据存储或外部集成时，或用于检查登录流程是否安全、是否符合 OWASP Top Ten 时。用于构建任何接受不可信数据、管理用户会话或与第三方服务交互的功能时。用于审计依赖中的已知漏洞、分诊包管理器的 audit 结果，或评估新包的供应链风险时。当涉及个人数据或隐私合规（GDPR、CCPA）时也使用。
---

# 安全和加固

## 概览

面向 Web 应用的 security-first 开发实践。把每一个外部输入都当作敌意的，把每一个 secret 都当作神圣的，把每一次 authorization 检查都当作强制的。Security 不是一个阶段，它是对每一行接触用户数据、认证或外部系统的代码的约束。

## 何时使用

- 构建任何接受用户输入的东西
- 实现 authentication 或 authorization
- 存储或传输敏感数据
- 集成外部 API 或服务
- 添加文件上传、webhooks 或 callbacks
- 处理支付或 PII 数据

## 流程：威胁建模优先

没有 threat model 就往上堆 controls，那只是猜测。在做加固之前，先花五分钟像攻击者一样思考：

1. **画出 trust boundaries。** 不可信数据在哪些位置进入你的系统？HTTP 请求、表单字段、文件上传、webhooks、第三方 API、消息队列，以及 **LLM 输出**；还包括那些因为由 OS 交给你而看起来是内部的本地值：另一个进程的命令行或环境变量、共享卷上的文件名、job payload 里的路径。信任跟随的是*写入*某个值的人，而不是传送它的通道。每一条边界都是攻击面。
2. **点名资产。** 有什么值得偷或值得破坏？Credentials、PII、支付数据、admin 操作、资金流转。
3. **对每条边界跑一遍 STRIDE** —— 它是一个快速视角，不是仪式：

| 威胁 | 要问的问题 | 典型 mitigation |
|---|---|---|
| **S**poofing（假冒） | 有人能冒充某个用户/服务吗？ | 认证、签名验证 |
| **T**ampering（篡改） | 数据能在传输中或静态存储时被篡改吗？ | 完整性检查、参数化查询、HTTPS |
| **R**epudiation（否认） | 某个行为事后能被否认吗？ | 对安全事件做审计日志 |
| **I**nformation disclosure（信息泄露） | 数据会泄露吗？ | 加密、字段 allowlist、通用错误信息 |
| **D**enial of service（拒绝服务） | 它会被打垮吗？ | 限流、输入大小上限、超时 |
| **E**levation of privilege（提权） | 用户能获得本不该有的权限吗？ | Authorization 检查、最小权限 |

4. **在每个 use case 旁边写下 abuse case。** 对每个功能问自己："我会怎么滥用它？" 然后把那答案变成你的第一个测试。

如果你说不出某个功能的 trust boundaries，你就还没准备好保护它。这就是 OWASP 的 **A04: Insecure Design** —— 大多数 breaches 始于设计，而不是代码。

## 三层边界系统

### Always Do（没有例外）

- **在所有系统边界（API routes、form handlers）校验全部外部输入**
- **参数化所有数据库查询** —— 绝不把用户输入拼接进 SQL
- **对输出做编码** 以防 XSS（使用框架的自动转义，不要绕过它）
- **所有外部通信使用 HTTPS**
- **用 bcrypt/scrypt/argon2 对密码做 hash**（绝不存明文）
- **设置安全 headers**（CSP、HSTS、X-Frame-Options、X-Content-Type-Options）
- **对 session 使用 httpOnly、secure、sameSite cookies**
- **每次发布前，用检测到的包管理器的原生 audit 针对已提交的 lockfile 跑一遍**

### Ask First（需要人工批准）

- 新增 authentication 流程或修改 auth 逻辑
- 存储新类别的敏感数据（PII、支付信息）
- 新增外部服务集成
- 修改 CORS 配置
- 添加文件上传处理器
- 修改 rate limiting 或 throttling
- 授予更高权限或角色

### 绝不执行

- **绝不把 secrets 提交**到版本控制（API keys、密码、tokens）
- **绝不在日志里记录敏感数据**（密码、tokens、完整信用卡号）
- **绝不把客户端校验当作安全边界**
- **绝不为图省事而禁用安全 headers**
- **绝不对用户提供的数据使用 `eval()` 或 `innerHTML`**
- **绝不把 sessions 存放在客户端可访问的存储里**（用 localStorage 存 auth tokens）
- **绝不向用户暴露 stack traces** 或内部错误细节

## OWASP Top 10 防护模式

这些是预防模式，不是排名。2021 年的排序见 `../../references/security-checklist.md` 中的速查表。

### Injection（SQL、NoSQL、OS Command）

```typescript
// BAD: SQL injection via string concatenation
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD: Parameterized query
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);

// GOOD: ORM with parameterized input
const user = await prisma.user.findUnique({ where: { id: userId } });
```

### Broken Authentication

```typescript
// Password hashing
import { hash, compare } from 'bcrypt';

const SALT_ROUNDS = 12;
const hashedPassword = await hash(plaintext, SALT_ROUNDS);
const isValid = await compare(plaintext, hashedPassword);

// Session management
app.use(session({
  secret: process.env.SESSION_SECRET,  // From environment, not code
  resave: false,
  saveUninitialized: false,
  cookie: {
    httpOnly: true,     // Not accessible via JavaScript
    secure: true,       // HTTPS only
    sameSite: 'lax',    // CSRF protection
    maxAge: 24 * 60 * 60 * 1000,  // 24 hours
  },
}));
```

### Cross-Site Scripting (XSS)

```typescript
// BAD: Rendering user input as HTML
element.innerHTML = userInput;

// GOOD: Use framework auto-escaping (React does this by default)
return <div>{userInput}</div>;

// If you MUST render HTML, sanitize first
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(userInput);
```

### Broken Access Control

```typescript
// Always check authorization, not just authentication
app.patch('/api/tasks/:id', authenticate, async (req, res) => {
  const task = await taskService.findById(req.params.id);

  // Check that the authenticated user owns this resource
  if (task.ownerId !== req.user.id) {
    return res.status(403).json({
      error: { code: 'FORBIDDEN', message: 'Not authorized to modify this task' }
    });
  }

  // Proceed with update
  const updated = await taskService.update(req.params.id, req.body);
  return res.json(updated);
});
```

### Security Misconfiguration

```typescript
// Security headers (use helmet for Express)
import helmet from 'helmet';
app.use(helmet());

// Content Security Policy
app.use(helmet.contentSecurityPolicy({
  directives: {
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'"],
    styleSrc: ["'self'", "'unsafe-inline'"],  // Tighten if possible
    imgSrc: ["'self'", 'data:', 'https:'],
    connectSrc: ["'self'"],
  },
}));

// CORS — restrict to known origins
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3000',
  credentials: true,
}));
```

### Sensitive Data Exposure

```typescript
// Never return sensitive fields in API responses
function sanitizeUser(user: UserRecord): PublicUser {
  const { passwordHash, resetToken, ...publicFields } = user;
  return publicFields;
}

// Use environment variables for secrets
const API_KEY = process.env.STRIPE_API_KEY;
if (!API_KEY) throw new Error('STRIPE_API_KEY not configured');
```

### Server-Side Request Forgery (SSRF)

只要服务器去抓取一个受用户影响的 URL —— webhooks、"从 URL 导入"、图片代理、链接预览 —— 攻击者就能把它指向内部服务（cloud metadata、`localhost`、私有 IP）。

```typescript
// BAD: fetch whatever the user gives you
await fetch(req.body.webhookUrl);

// GOOD: allowlist scheme + host, reject if ANY resolved IP is private, forbid redirects
import { lookup } from 'node:dns/promises';
import ipaddr from 'ipaddr.js';

const ALLOWED_HOSTS = new Set(['hooks.example.com']);

async function assertSafeUrl(raw: string): Promise<URL> {
  const url = new URL(raw);
  if (url.protocol !== 'https:') throw new Error('https only');
  if (!ALLOWED_HOSTS.has(url.hostname)) throw new Error('host not allowed');
  // Resolve ALL records; a single private/reserved address fails the check.
  const addrs = await lookup(url.hostname, { all: true });
  if (addrs.some((a) => ipaddr.parse(a.address).range() !== 'unicast')) {
    throw new Error('private/reserved IP');
  }
  return url;
}

await fetch(await assertSafeUrl(req.body.webhookUrl), { redirect: 'error' });
```

`range() !== 'unicast'` 这个检查覆盖了 loopback、link-local `169.254.169.254`（cloud metadata，SSRF 的头号目标）、private 和 unique-local 范围，IPv4 与 IPv6 都适用。

**注意 —— 这里仍然存在一个 TOCTOU gap。** `fetch` 会在检查之后重新解析 DNS，所以攻击者用一条短 TTL 的记录，就能在校验和建立连接之间把域名 rebind 到内部 IP。对高风险场景，要么解析一次并连接固定（pinned）的 IP，要么在前面放一个过滤代理（`request-filtering-agent` / `ssrf-req-filter`）。

## 输入校验模式

### 在边界进行 Schema Validation

```typescript
import { z } from 'zod';

const CreateTaskSchema = z.object({
  title: z.string().min(1).max(200).trim(),
  description: z.string().max(2000).optional(),
  priority: z.enum(['low', 'medium', 'high']).default('medium'),
  dueDate: z.string().datetime().optional(),
});

// Validate at the route handler
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: 'Invalid input',
        details: result.error.flatten(),
      },
    });
  }
  // result.data is now typed and validated
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

### 文件上传安全

```typescript
// Restrict file types and sizes
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];
const MAX_SIZE = 5 * 1024 * 1024; // 5MB

function validateUpload(file: UploadedFile) {
  if (!ALLOWED_TYPES.includes(file.mimetype)) {
    throw new ValidationError('File type not allowed');
  }
  if (file.size > MAX_SIZE) {
    throw new ValidationError('File too large (max 5MB)');
  }
  // Don't trust the file extension — check magic bytes if critical
}
```

### 对派生路径的破坏性操作

一次 delete、move 或 overwrite，其安全性只取决于命名目标的那个值的安全性。从 kernel、job payload 或兄弟服务读取这个值，只能证明它*从哪里来*，不能证明是谁*写入*的 —— 另一个进程的命令行和表单字段一样受攻击者控制。一个形状检查（"绝对路径、至少一层目录深"）只能证明格式良好，却常被误当成授权；清理脚本删掉根目录而不是叶子目录，就是这么发生的。

在发起破坏性调用之前，三个条件缺一不可：解析后的目标位于某个 **allowlisted root** 之下（在解析 symlink 之后比较，绝不在原始字符串上比较）；它至少在该 root 之下**一层**，因此 root 本身永远不会成为目标；并且它带有**属于你**的证据，这份证据要在操作*之前*、在任何会移除它的 teardown 之前读取 —— 否则"不存在"和"不是我的"无法区分。拒绝执行时，记下被拒绝的目标然后停止：一个回退到更宽默认路径的清理脚本，正是这套检查要防的事故。完整示例见 `../../references/security-checklist.md`。

有两个局限，因为这个检查看起来比实际更强。树内部的标记文件是自我声明 —— 任何能往那里写的东西都能写这个标记 —— 所以期望的 owner 必须来自已认证的状态，而且标记本身需要完整性保护（严格的 ownership 或一个 MAC）才算得上授权。另外，先解析路径再对*名字*执行操作，只要有一个不可信进程能换掉某个祖先目录，就存在 check/use race：在共享卷上，用文件 descriptor 持有目标，并使用不跟随 symlink、限定在 root 之下的操作，或者确保这段时间内目录层级不会变化。

## 分流依赖审计结果

包管理器的 audit 报告的是已知 advisories；它既不证明一个包值得信任，也不证明易受攻击的代码是可达的。用这棵决策树：

```
The native package-manager audit reports a vulnerability
├── Severity: critical or high
│   ├── Is the vulnerable code reachable in runtime, build, test, or deployment paths?
│   │   ├── YES --> Fix immediately (update, patch, or replace the dependency)
│   │   └── NO (confirmed unused across those paths) --> Fix soon, but not a blocker
│   └── Is a fix available?
│       ├── YES --> Update to the patched version
│       └── NO --> Check for workarounds, consider replacing the dependency, or add to allowlist with a review date
├── Severity: moderate
│   ├── Reachable in production? --> Fix in the next release cycle
│   └── Dev-only? --> Fix when convenient, track in backlog
└── Severity: low
    └── Track and fix during regular dependency updates
```

**关键问题：**
- 易受攻击的那个函数在你的代码路径里真的被调用吗？
- 这个依赖是 runtime dependency 还是仅开发使用？
- 结合你的部署上下文，这个漏洞可被利用吗（例如一个仅客户端应用里的 server-side 漏洞）？

当你推迟一个修复时，记录原因并设定一个复查日期。

### 供应链卫生

不要假设是 npm，也不要把最近的 manifest 当作 install root。按这个顺序执行：

1. **找到 installation boundary 和 manager。** 使用拥有 lockfile 的 workspace 根目录；只有在独立嵌套项目位于该 workspace 之外时才使用它。在那里，交叉验证 `packageManager`（存在时）、lockfile 和 CI；出现分歧或互相竞争的 lockfile 时停下。固定 manager 版本，并使用 `../../references/security-checklist.md` 中的对照矩阵。
2. **在首次执行前阻断依赖脚本。** 以禁用脚本的方式 bootstrap，或采用一个有文档的 fail-closed 策略；检查待执行脚本的源码，只批准最低限度必需的包，提交这个策略，然后用一次干净的 frozen/immutable install 验证。绝不无差别批准脚本。

Audit 只能发现已知 advisories，抓不到新出现的恶意包或 typosquatting 包。因此：

- **绝不自动应用强制的 audit 修复**（`npm audit fix --force` 或等价命令）。先预览修复内容、阅读 changelogs，并逐一测试产生的升级；强制修复可能越过声明的依赖范围。
- **在支持的地方验证 registry 签名和 provenance**（`npm audit signatures`、`pnpm audit signatures`），把"缺失"当作需要调查的信号，而不是自动认定为被攻破。
- **把新依赖、lockfile diff 和 script-policy 变更放在一起 review** —— ownership、维护状况、发布时长、provenance、传递依赖图，以及 typosquats，如 `cross-env` 对比 `crossenv`（OWASP **A06**、**LLM03**）。

## Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// General API rate limit
app.use('/api/', rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100,                   // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
}));

// Stricter limit for auth endpoints
app.use('/api/auth/', rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,  // 10 attempts per 15 minutes
}));
```

**一旦进程数超过一个，就用共享存储来计数。** `express-rate-limit` 默认把计数器放在进程内存里。在 load balancer 后面，每个实例各自计数，实际限额是 `max × instances`；在 serverless 或 edge 运行时，每次新调用都从零开始，所以上面那个 auth 限额可能永远不会触发。传入一个共享 `store`（通过 `rate-limit-redis` 用 Redis），或使用一个在不适合长连接 TCP 的地方也能工作的 HTTP-based limiter（例如 `@upstash/ratelimit`）：

```typescript
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const authLimiter = new Ratelimit({
  redis: Redis.fromEnv(),                       // UPSTASH_REDIS_REST_URL + _TOKEN
  limiter: Ratelimit.slidingWindow(10, '15 m'), // 10 attempts per 15 minutes, across all instances
});
const { success } = await authLimiter.limit(`login:${req.ip}`);
if (!success) return res.status(429).end();
```

## Secrets 管理

```
.env files:
  ├── .env.example  → Committed (template with placeholder values)
  ├── .env          → NOT committed (contains real secrets)
  └── .env.local    → NOT committed (local overrides)

.gitignore must include:
  .env
  .env.local
  .env.*.local
  *.pem
  *.key
```

**提交前务必检查：**
```bash
# Check for accidentally staged secrets
git diff --cached | grep -i "password\|secret\|api_key\|token"
```

**如果一个 secret 已经被提交，立刻轮换它。** 删掉那一行或重写 history 都不够 —— 只要它到达过 remote 就当作已泄露。先吊销并重新签发 key，再从 history 中清除它。

## 数据隐私与合规

保护数据问的是"攻击者能读到它吗？"。Privacy 问的是"我们*该*持有它吗，该持有多久？" —— 这是加固回答不了的另一个问题。最好保护、最不会泄露、最省合规成本的数据，是你从未收集过的数据。把个人数据当作要最小化的负债，而不是要囤积的资产。

**知道你持有什么。** 你无法保护或删除你找不到的数据。在添加字段时就做好分类：

| 类别 | 示例 | 处理方式 |
|---|---|---|
| **非个人** | 聚合数据、匿名计数 | 常规处理 |
| **个人（PII）** | 姓名、邮箱、IP、设备/用户 ID | 最小化、访问控制、纳入导出/删除 |
| **敏感** | 健康、财务、位置、生物特征、政府 ID、任何关于未成年人的信息 | 收集需要额外依据、更严格的访问、通常需要加密 + 审计日志 |

**操作规则：**
- **最小化并设定目的。** 只在有明确用途时才收集某个字段。"以后可能用得上"不是目的，那是潜在的 breach 范围。不要把 PII 写进 telemetry 日志（`observability-and-instrumentation` skill 从 ops 角度表达了同一个观点）。
- **事先设定保留期限，并且真的去删除。** 每个人个人数据存储都需要一个 TTL 和一条可用的删除路径 —— 包括备份、缓存、搜索索引和分析副本。没有到期时间的数据，就是一张预约在未来发生的 breach。
- **支持你所在司法辖区要求的数据主体权利**（GDPR/CCPA 及同类法规）：按请求导出、更正和删除。这些是工程特性 —— 设计 schema 时要让用户的数据*可查找*、*可擦除*，而不是不可逆地抹散在各个系统里。
- **在收集或第三方共享之前取得同意**，并让同意可审计。把 PII 发给分析/广告/LLM 厂商就属于"共享" —— 由用户的选择决定放行，且厂商需要签一份数据处理协议。
- **默认值要本地化，不要硬编码某一个地区的法律。** 数据驻留和规则随用户所在地不同；把策略做成可配置的边界，而不是一个假设。

当数据跨越 trust boundary 时，按不可信数据处理并校验它（见上文 Input Validation）；当 privacy 事件暴露了个人数据时，breach-notification 的倒计时是 postmortem 的一部分 —— 遵循 `debugging-and-error-recovery` skill。

## AI / LLM 功能安全

如果你的应用调用 LLM —— chatbots、摘要器、agents、RAG —— 它就继承了一个新的攻击面。把它映射到 [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/)：

- **把所有模型输出当作不可信输入（LLM05: Improper Output Handling）。** 绝不把 LLM 输出直接传进 `eval`、SQL、shell、`innerHTML` 或文件路径。像校验原始用户输入一样校验并编码它。
- **假设 prompts 可能被劫持（LLM01: Prompt Injection）。** context window 里的任何不可信文本 —— 用户消息、抓取的网页、PDF —— 都可能携带指令。system prompt 不是安全边界；权限要在代码里强制执行，而不是写在 prompt 里。
- **让 secrets 和其他用户的数据远离 prompts（LLM02 / LLM07）。** context 里的任何东西都可能被回显出来。不要把 API keys、跨租户数据或完整 system prompt 放在模型能重复出来的位置。
- **约束工具和 agent 的权限（LLM06: Excessive Agency）。** 把工具限定到最小范围，对破坏性或不可逆操作要求确认，并校验每一个工具参数。
- **限制消耗（LLM10: Unbounded Consumption）。** 给 tokens、请求速率、循环/递归深度设上限，让精心构造的输入无法刷高成本或挂死系统。
- **隔离检索数据（LLM08: Vector and Embedding Weaknesses）。** 在 RAG 中，把 vector store 当作 trust boundary：按租户分区 embeddings，让一个用户检索不到另一个人的数据；在索引文档前先校验它们，让被投毒的内容无法左右答案。

```typescript
// BAD: trusting model output as a command or as markup
const sql = await llm.generate(`Write SQL for: ${userQuestion}`);
await db.query(sql);                                   // arbitrary query execution
container.innerHTML = await llm.reply(userMessage);   // stored XSS, via the model

// GOOD: model output is data — parse defensively, then validate, then encode
let intent;
try {
  intent = CommandSchema.parse(JSON.parse(await llm.replyJson(userMessage)));
} catch {
  throw new ValidationError('unexpected model output'); // JSON.parse or schema failed
}
await runAllowlistedAction(intent.action, intent.params);
container.textContent = await llm.reply(userMessage);
```

## 安全审查检查清单

```markdown
### Authentication
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (salt rounds ≥ 12)
- [ ] Session tokens are httpOnly, secure, sameSite
- [ ] Login has rate limiting
- [ ] Password reset tokens expire

### Authorization
- [ ] Every endpoint checks user permissions
- [ ] Users can only access their own resources
- [ ] Admin actions require admin role verification

### Input
- [ ] All user input validated at the boundary
- [ ] SQL queries are parameterized
- [ ] HTML output is encoded/escaped
- [ ] Server-side URL fetches are allowlisted (no SSRF to internal services)
- [ ] Delete/move/overwrite targets built from data are checked against an allowlisted root, a minimum depth, and ownership evidence read before the operation

### Data
- [ ] No secrets in code or version control
- [ ] Sensitive fields excluded from API responses
- [ ] PII encrypted at rest (if applicable)
- [ ] Personal data is classified, collected against a stated purpose, and minimized
- [ ] Personal data has a retention limit and a working deletion path (incl. backups/indexes)
- [ ] Export/delete (data-subject) requests are supported where required; sharing with third parties has consent

### Infrastructure
- [ ] Security headers configured (CSP, HSTS, etc.)
- [ ] CORS restricted to known origins
- [ ] Dependencies audited for vulnerabilities
- [ ] Error messages don't expose internals

### Supply Chain
- [ ] One authoritative lockfile committed; CI uses that manager's frozen/immutable install
- [ ] Native audit triaged by reachability and fix risk; dependency install scripts blocked unless explicitly approved
- [ ] New dependencies reviewed (ownership, provenance, release age, transitive graph)

### AI / LLM (if used)
- [ ] Model output treated as untrusted (no eval/SQL/innerHTML/shell)
- [ ] Secrets and other users' data kept out of prompts
- [ ] Tool/agent permissions scoped; destructive actions require confirmation
```
## 另请参阅

详细的 security checklists 和 pre-commit 验证步骤见 `../../references/security-checklist.md`。

## 常见合理化借口

| 自我合理化 | 现实 |
|---|---|
| "这是内部工具，security 不重要" | 内部工具也会被攻破。攻击者专挑最弱的环节。 |
| "我们以后再加安全" | 事后补安全比一开始就构建难 10 倍。现在就加。 |
| "没人会来 exploiting 这个" | 自动化扫描器会找到它。靠隐蔽来保证安全不是安全。 |
| "框架会处理安全" | 框架提供工具，不提供保证。你还是得正确使用它们。 |
| "这只是个原型" | 原型会上生产。安全习惯从第一天开始。 |
| "这里搞 threat modeling 太过了" | 五分钟思考"我会怎么攻击它"，能防住那些事后任何 control 都补不回来的设计缺陷。 |
| "只是 LLM 输出，不过是文本而已" | 那"文本"可能是一条 SQL 语句、一个 script 标签或一条 shell 命令。像对待任何不可信输入一样对待它。 |
| "audit 通过了，所以依赖是安全的" | Audit 匹配的是已知 advisories。它检测不出新出现的恶意包，也不会让未经 review 的 install 脚本变得安全可执行。 |
| "先收集起来，以后可能用得上" | 你没有持有的数据不会被 breach、被传票调取或被误删。"可能用得上"是 breach 范围，不是目的。 |
| "删除请求我们手动处理" | 手动擦除会漏掉备份、缓存和分析副本。如果 schema 找不出某个用户的数据，你就无法兑现删除请求 —— 要为它做设计。 |
| "合规是法务的问题，不是我们的" | 导出、删除、保留和同意都是 schema 和代码的事。等你把 PII 抹散到十个系统之后，法务没法再补上去。 |

## 危险信号

- 用户输入直接传入数据库查询、shell 命令或 HTML 渲染
- delete、move 或 overwrite 的目标来自 payload、配置值或另一个进程的命令行，只靠一个路径形状检查来防护
- 源码或 commit history 里有 secrets
- API endpoints 没有 authentication 或 authorization 检查
- 缺少 CORS 配置，或使用了通配符（`*`）origins
- 认证 endpoints 没有 rate limiting，或者多个实例前面放了一个内存态 limiter
- 向用户暴露 stack traces 或内部错误
- 依赖存在已知 critical 漏洞、同一 installation boundary 有互相竞争的 lockfiles、install 不可复现、脚本被无差别批准
- 服务端在没有 allowlist 的情况下抓取用户提供的 URLs（SSRF）
- LLM/模型输出被传进查询、DOM、shell 或 `eval`
- Secrets、PII 或完整 system prompt 被放进 LLM context window
- 收集个人数据时没有声明目的、保留期限或删除路径
- 在没有同意或数据处理协议的情况下把 PII 发给分析/广告/LLM 厂商
- "删除我的账号"只翻了个标志位，个人数据仍留在各个存储和备份里

## 验证

实现安全相关代码之后：

- [ ] 原生 audit 没有未缓解且可达的 critical/high findings；CI 保留 authoritative lockfile 并阻断未经 review 的依赖脚本
- [ ] 源码和 git history 中没有 secrets
- [ ] 所有用户输入都在系统边界做了校验
- [ ] 破坏性文件系统操作先解析 symlinks，再在执行前验证 allowlisted root、最小深度和 ownership
- [ ] 每个受保护 endpoint 都检查了 authentication 和 authorization
- [ ] 响应中存在安全 headers（用浏览器 DevTools 检查）
- [ ] 错误响应不暴露内部细节
- [ ] auth endpoints 启用了 rate limiting，且当有多个实例服务流量时由共享存储支撑
- [ ] 服务端 URL 抓取按 allowlist 校验过（无 SSRF）
- [ ] LLM/模型输出在使用前经过校验和编码（如果使用了 AI 功能）
- [ ] 个人数据已分类、按声明目的最小化收集，并设有保留期限
- [ ] 删除和导出请求端到端可用（包括备份、缓存和分析副本）
