---
name: codeguard-cve
license: Apache-2.0
description: 编排 Maven、Node、Python 和 Rust 依赖的 CVE 扫描与门禁；未被原生扫描器覆盖的语言自动落 trivy 通用兜底（原生工具缺失时保持无法验证，不用兜底顶替）；当用户要求扫漏洞、依赖安全检查、发布前审查、解释 HIGH/CRITICAL 发现或设计抑制策略时使用。必须保留工具、阈值、依赖路径与复扫证据。
compatibility: 需要目标生态的锁文件、扫描工具及可用漏洞数据源；默认不升级依赖、不自动接受抑制。
---

# codeguard cve

## Capability Boundaries

### ✅ Strengths
1. 自动检测生态，编排对应扫描工具
2. 识别到语言但无原生生态映射 → 自动落 `universal`（trivy fs --scanners vuln）；原生生态存在时不并行兜底
3. `--severity` 为「该级别及以上」，在所有扫描器上同一语义（maven 按 CVSS 档位下界换算，HIGH⇒7）
4. 退出码：0 通过 / 1 无法验证 / 2 存在漏洞 / 3 参数错误（未声明 --ecosystem 在任何扫描前拒绝）
5. 阈值门禁（`--severity MEDIUM/HIGH/CRITICAL`）
6. `--fix` 自动修复（npm audit fix）；其余生态输出修复指引
7. 三态退出码：0=通过 / 1=无法验证（工具缺失）/ 2=发现漏洞

### ⚠️ Prerequisites
1. Maven：mvn + 网络（首跑下载 NVD 库，建议申请 NVD_API_KEY）
2. Node：npm + package-lock.json
3. Python：pip-audit（`pip install pip-audit`）
4. Rust：cargo-audit（`cargo install cargo-audit`）
5. 通用兜底：trivy（`brew install trivy`）——仅在检测到无原生扫描器的语言（Go/PHP/Ruby 等）时触发

### ❌ Out of Scope
1. 镜像内 OS 包 CVE → trivy image（可后续接入）
2. Dockerfile misconfig → codeguard-dockerfile
3. 豁免策略制定 → codeguard-security-code

## 命令

先判定引擎，两套命令面不同。Rust `codeguard` 组件的 `cve` 用位置参数选择生态，且没有 `--severity` / `--fix` / `--json`；它对质量路径固定返回未完成（退出码 3），不能用来签发"无漏洞"结论。

**Legacy Python 引擎：**

```bash
bin/codeguard cve                          # 全生态扫描
bin/codeguard cve --ecosystem node         # 只扫 node
bin/codeguard cve --fix                    # 扫描 + 自动修复 + 复扫
bin/codeguard cve --severity MEDIUM        # 门禁阈值调到中危（发版前）
bin/codeguard cve --json path/             # 结构化输出
```

**Rust 组件（局部原生观察，结论保持未完成）：**

```bash
codeguard cve typescript [path] --node-tool ABS_PATH --npm-entry ABS_PATH --npm-version VERSION
codeguard cve rust [path] --cargo-audit-tool ABS_PATH --db ABS_PATH
codeguard cve python [path] --pip-audit-tool ABS_PATH --pip-audit-version VERSION
```

引擎判定与两套命令面对照见 `codeguard` 技能的 `references/operations/engine-contract.md`。

## 三态语义（门禁必须遵守）

| 退出码 | 含义 | 门禁动作 |
|---|---|---|
| 0 | 全部通过 | 允许提交 |
| 1 | 无法验证（工具缺失/超时） | **不视为通过**——先装工具 |
| 2 | 发现漏洞 | 必须修复（升级/替换/登记缓解），禁止只报告不处理 |
| 3 | 检查未完成 | **不视为通过**——只能表述为未完成或局部观察 |

## Workflow

1. 扫描：`bin/codeguard cve`
2. 有发现 → 读报告定位受影响包与引入路径（`mvn dependency:tree` / `npm ls`）
3. 修复：优先升级版本；无法升级给出缓解措施（WAF/关闭暴露面）并登记注销日期
4. 复扫至零 HIGH/CRITICAL
5. 提交前再跑一次确认

## 不适用范围（什么时候不该用）

- 问题是容器基础镜像或操作系统包，而当前 Codeguard 还没有该 scanner 证据。
- 问题是源码密钥泄露、鉴权或数据安全；应转交对应安全技能。
- 没有 lockfile/依赖元数据却要求证明不存在漏洞。

## 数据与安全

依赖名、版本和锁文件可能被扫描工具发送到外部漏洞数据源。执行前需说明网络边界，不上传源码、凭据或私有包内容。报告不得回显 token/NVD key；本技能不会自动创建抑制或升级依赖。

## 证据化 Workflow

### Step 1：确定生态和范围

找到 lockfile、构建文件、workspace 边界和生产/dev/test 依赖分类。

### Step 2：探测扫描器

记录 scanner 版本、漏洞数据库时间和门禁阈值。数据源不可用时状态为 `UNVERIFIED`。

### Step 3：执行只读扫描

优先 `bin/codeguard cve --json <path>` 保存结构化证据，不在首次扫描时带 `--fix`。Rust 引擎下改用 `--format json` 的 `cve <生态>` 调用，并如实标注该结果为未完成。

### Step 4：确认可利用性与引入路径

核对 CVE/GHSA、受影响版本、已修复版本、直接/传递依赖与项目是否使用受影响功能。

### Step 5：选择处置

优先最小兼容升级，其次替换组件或关闭暴露面。抑制必须有误报依据、责任人和到期日。

### Step 6：回归测试

依赖改动后执行锁文件差异审查、编译、单测、集成测试和关键兼容性检查。

### Step 7：使用原阈值复扫

不能通过调高阈值把发现“修复”掉。报告必须列出已修复、已缓解、已抑制和尚未解决项。

## Rules

1. 无法访问漏洞数据源不等于零漏洞。
2. 不盲目运行 `npm audit fix --force` 或全量 latest 升级。
3. 不只复制 scanner 标题；必须确认依赖路径和可用修复版本。
4. 缓解不等于修复，必须写明残余风险与追踪日期。
5. 报告必须记录扫描日期和数据库新鲜度。
6. 必须写明本次扫描由哪个引擎签发；Rust 组件的未完成结果不得表述为零漏洞。

## 输出模板

```text
Codeguard CVE 结果
- 范围/生态：<workspace and lockfiles>
- 扫描器：<name/version/db timestamp>
- 阈值：<severity policy>
- 状态：PASS / FAIL / UNVERIFIED
- 发现：<CVE, dependency path, affected/fixed range>
- 处置：<upgrade/replace/mitigate/suppress with evidence>
- 回归：<build/test evidence>
- 复扫：<command and exit>
```

## Gotchas

1. **锁文件缺失**：基于声明版本的扫描可与真实解析版本不同。
2. **NVD/registry 限流**：首跑下载失败是 UNVERIFIED，不是 PASS。
3. **dev dependency 也可到达生产**：构建链供应链风险不能仅凭“非运行时”忽略。
4. **修复版本可破坏 API**：需根据 semver、changelog 和回归证据判断。
5. **同一漏洞多路径引入**：只升级一条直接依赖可能仍然残留传递路径。
6. **抑制会过期**：已抑制项需要到期日和重验条件。

## 按需加载资源

- 选择 scanner 和阈值时读取 `references/rules/scanner-matrix.md`。
- 设计修复/抑制证据时读取 `references/operations/remediation-playbook.md`。
- 只读取 `examples/` 中与当前生态或失败模式匹配的示例。
