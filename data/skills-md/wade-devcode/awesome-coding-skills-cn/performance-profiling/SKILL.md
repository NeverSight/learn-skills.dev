---
name: performance-profiling
description: 优化性能时使用。先测量定位再优化,不凭感觉。
category: performance
tags: [性能,profiling,优化]
---

# 性能调优

## 何时用

- 系统出现明显变慢、延迟升高、资源使用异常时。
- 接到"优化这段代码"的任务,准备动手之前。
- 发现自己想"感觉这里可以缓存一下"但没有数据支撑时——这是需要先测量的信号。
- 在 code review 里看到未经测量的性能优化改动时。

## 核心规则

### 1. 先测量:用 profiler/benchmark 找真实瓶颈,不靠猜

**规则：** 任何优化动作之前,必须先用工具(profiler、benchmark、APM 追踪)找出真实的热点函数或慢路径,再决定优化什么。

**为什么：** AI 在"优化性能"任务中常先凭直觉下手:把字典查找换成数组遍历"因为听说数组快"、把 for 循环改成列表推导"因为更 Pythonic"。但实际瓶颈往往在完全不同的地方——90% 的时间花在一个数据库查询上,而 AI 在优化内存里的字符串拼接。没有数据的优化不仅收益不明,还可能引入新 bug 或降低可读性。

**怎么做：**
- Python 用 `cProfile`/`py-spy`,Node.js 用 `--prof` 或 Chrome DevTools,Go 用 `pprof`。
- APM(Datadog、New Relic、Sentry)看生产慢请求的 trace,定位到具体函数调用。
- 先得到一份"热点函数列表"(火焰图或 top-N),再决定优化哪里。

---

### 2. 优化热点,不过早优化冷路径;有数据支撑再改

**规则：** 只优化 profiler 确认的高频/高耗时路径,忽略执行频率低的冷路径;每次优化决策都要有性能数据作为依据。

**为什么：** AI 在生成代码时常做"预防性优化"——在一个每天调用 10 次的管理接口里用位运算替代普通算术,因为"更高效"。这些优化降低了代码可读性,却对实际用户体验毫无影响。真实的性能收益来自于优化那些每秒调用上千次或每次耗时数百毫秒的路径,而不是散落各处的"感觉更快"的改写。

**怎么做：**
- 只处理 profiler 报告中占总耗时前 80% 的函数。
- 改之前记录基准数字(当前 P99 延迟、QPS 上限、内存峰值)。
- 对于冷路径,优先选择可读性好的实现,留注释说明"此处不是瓶颈,无需优化"。

---

### 3. 关注算法复杂度与 I/O(N+1、同步阻塞、无缓存),常比微优化收益大

**规则：** 先检查 O(n²) 算法、N+1 查询、同步阻塞 I/O、无缓存的重复计算这类结构性问题,再考虑微观层面的优化。

**为什么：** AI 进行性能优化时容易去做微优化(内联函数、减少对象分配、换更快的序列化库),却忽视结构性问题。常见事故:一个列表页接口产生 N+1 查询——每条记录触发一次独立 DB 查询,100 条记录 = 101 次查询。把 JSON 序列化从 `json` 换成 `orjson` 节省了 1ms,但 N+1 查询吃掉了 500ms。结构性优化(改成一次 JOIN 查询)的收益是微优化的 100 倍。

**怎么做：**
- 用数据库慢查询日志或 `EXPLAIN` 检查是否有 N+1、缺失索引、全表扫描。
- 检查热路径上是否有阻塞 I/O 可以改为异步或批量处理。
- 检查计算密集型结果是否有合适的缓存层(内存缓存/Redis),减少重复计算。
- 对循环内的数据库查询、HTTP 调用保持警惕。

---

### 4. 改完再测量对比,确认真变快且没破坏正确性

**规则：** 优化完成后必须重新运行 benchmark/profiler,与基准数字对比,确认性能确实提升;同时运行测试套件确认正确性没有回归。

**为什么：** AI 实施优化后常缺失验证步骤——直接提交,相信"理论上更快"。实际中常见结果:优化后 benchmark 数字基本没变(瓶颈在别处),或者"优化"引入了竞态条件、缓存不一致、精度损失等正确性问题。没有前后对比数字的优化 PR 无法让 reviewer 判断是否值得合并。

**怎么做：**
- 固定测试环境(同一机器、同一数据量、预热后再测)保证对比公平。
- 同时记录优化前后的延迟(P50/P95/P99)和吞吐量,不只看平均值。
- 运行完整测试套件,包括边界用例和并发测试。
- 在 PR 描述里贴出"优化前 vs 优化后"的数字对比。

---

### 5. 记录基准与取舍,避免可读性为微小收益让路

**规则：** 性能优化产生的代码复杂度提升,必须伴随明确的数字收益记录;若收益小于可读性代价,优先选择清晰实现。

**为什么：** AI 做性能优化时常引入晦涩写法——位运算替代乘除、手动内联展开循环、复杂的预分配逻辑——并声称"性能更好"。但没有记录收益是多少,也没有说明这段复杂代码将来是否还需要人工维护。三个月后下一个维护者看到这段代码完全不懂,但也不敢改,因为不知道它到底优化了什么、优化幅度多大。

**怎么做：**
- 对引入复杂度的优化,在代码注释里记录:`// 性能优化:此处用 bitmap 替代 Set,基准测试显示 P99 延迟从 12ms 降至 3ms (见 bench/user_lookup.go)`。
- 若基准测试显示收益小于 5%,优先保留可读性较好的原始写法。
- 复杂的优化单独提一个 PR,附完整 benchmark 结果,不要混在功能 PR 里。

---

## 正例 / 反例

### 反例:无数据支撑,优化了错误的地方

```python
# 反例 — 凭感觉把字典查找"优化"成列表,实际上字典查找是 O(1) 更快
# 而真正的瓶颈在下面那个 N+1 查询,完全没动

def get_user_roles(user_id: int) -> list[str]:
    # "优化":把 set 改成 list,因为 list 占内存更少?
    role_names = []                         # ❌ 没有 profiler 数据支撑
    roles = Role.objects.filter(user=user_id)  # ❌ 真正的问题:循环外还有 N+1
    for role in roles:
        if role.name not in role_names:     # ❌ 现在查找变成 O(n) 了
            role_names.append(role.name)
    return role_names
```

```python
# 正例 — profiler 定位到 N+1 查询是瓶颈,用 prefetch 消除

# 优化前:N+1 查询,100 个用户 = 101 次 SQL,P99 = 480ms
# 优化后:1+1 次查询,P99 = 18ms (benchmark: tests/bench/test_user_roles.py)
def get_users_with_roles(user_ids: list[int]) -> dict[int, list[str]]:
    users = (
        User.objects
        .filter(id__in=user_ids)
        .prefetch_related("roles")          # ✅ 消除 N+1,一次 JOIN 取全部
    )
    return {user.id: [r.name for r in user.roles.all()] for user in users}
```

---

### 反例:优化完不测量,只靠理论判断

```typescript
// 反例 — 宣称"更快"但没有 benchmark 数字,且没跑测试
// PR 描述写:"使用 Map 替代对象字面量,理论上查找更快"

function findUser(users: Record<string, User>, id: string): User | undefined {
  return users[id];
}

// 改成了 Map 版本,没有前后性能对比数据
function findUser(users: Map<string, User>, id: string): User | undefined {
  return users.get(id);  // ❌ 没有 benchmark 验证,签名破坏了所有调用方
}
```

```typescript
// 正例 — 有基准测试,确认收益,测试通过
// benchmark 结果:10万次查找,Object: 8ms vs Map: 6ms,提升 25%
// 调用方已全部迁移,回归测试全绿 (npm run bench -- user-lookup)

function findUser(users: Map<string, User>, id: string): User | undefined {
  return users.get(id); // ✅ 有数据支撑,调用方已更新,测试已过
}
```

---

## 自查清单

- [ ] 优化之前已运行 profiler/benchmark,拿到热点函数列表或慢路径数据。
- [ ] 本次优化针对的是 profiler 确认的热点,不是凭感觉选的目标。
- [ ] 已检查是否存在 N+1 查询、同步阻塞 I/O、无缓存的重复计算等结构性问题。
- [ ] 优化完成后重新运行 benchmark,有"优化前 vs 优化后"的具体数字对比。
- [ ] 优化后运行了完整测试套件,正确性没有回归。
- [ ] 引入代码复杂度的优化,有注释记录性能收益数字和 benchmark 位置。
- [ ] 若收益不显著(< 5%),已选择保留可读性更好的原始写法。
