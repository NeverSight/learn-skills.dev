---
name: error-handling
description: 处理错误与异常时使用。不吞异常、不裸抛、给出可恢复信息。
category: backend
tags: [错误处理, 异常]
---

# 错误处理

## 何时用

- 写任何涉及 IO、网络、数据库、外部 SDK 调用的代码时。
- 在函数/方法中加 try-catch/try-except，需要确定该怎么处理时。
- 联调时前端反馈"不知道哪里出错了"或日志里找不到报错原因时。
- code review 发现 catch 块为空、或者只有 `console.log(e)` 时。

## 核心规则

### 1. 不吞异常：catch 块必须有实质处理

**规则：** `catch`/`except` 块里必须有真正的处理动作——记录日志、触发回滚、重新抛出或转换为业务错误；禁止空 catch 块，禁止仅打印后继续正常流程假装没发生过。

**为什么：** AI 生成代码时，"先写个 try-catch 让它跑起来"是最常见的反模式——`catch (e) {}` 或 `except: pass`。空 catch 会把真实的数据库连接失败、磁盘写入错误、第三方 API 超时全部静默吞掉，函数返回"成功"，上层完全感知不到异常，日志里没有任何线索，用户看到的是数据没有保存但页面显示"操作成功"。定位这类 bug 通常要花几倍时间，因为所有的证据都被主动销毁了。

**怎么做：**
- 能处理就处理（重试、降级、返回默认值），并记录 warn 级日志。
- 不能处理就重新抛出（`throw`/`raise`），让上层决定。
- 需要转换语义时，把底层异常包裹成业务异常再抛：`throw new PaymentFailedException("支付网关超时", cause=e)`。
- `finally` 块做资源清理，不要把清理逻辑写在 catch 里然后 return 提前跳出。

---

### 2. 错误分类：可预期错误与意外错误分开处理

**规则：** 明确区分两类错误——可预期的业务错误（用户输入非法、资源不存在、权限不足）和意外的系统错误（空指针、数据库宕机、bug）；前者用业务异常类表达，后者进入全局 handler 并触发告警。

**为什么：** AI 生成的代码经常把所有异常一律 `catch (Exception e)` 然后返回 500——校验失败返回 500、资源不存在返回 500、真正的 bug 也是 500。监控告警全是噪音，用户看到的错误信息毫无意义，oncall 工程师不知道哪些 500 需要紧急处理、哪些是正常的业务错误被错误分类了。错误分类是可观测性的基础，混在一起会让整个告警体系失效。

**怎么做：**
```python
# 业务异常基类（可预期，映射到 4xx）
class AppError(Exception):
    def __init__(self, code: str, message: str, http_status: int = 400):
        self.code = code
        self.message = message
        self.http_status = http_status

class ResourceNotFoundError(AppError):
    def __init__(self, resource: str, resource_id):
        super().__init__("RESOURCE_NOT_FOUND", f"{resource} {resource_id} 不存在", 404)

# 意外错误不捕获，让全局 handler 接管，触发告警
def get_user(user_id: int) -> User:
    user = db.query(User).get(user_id)
    if user is None:
        raise ResourceNotFoundError("User", user_id)  # ✅ 业务错误，明确分类
    return user
```
- 业务异常：校验失败、资源不存在、权限不足、业务规则冲突 → 映射到 4xx，记录 info/warn，不触发 PagerDuty。
- 系统异常：数据库连接失败、空指针、未捕获异常 → 5xx，记录 error，触发告警，保留完整堆栈。

---

### 3. 错误信息带上下文，但不泄露敏感数据

**规则：** 错误日志必须包含"哪个操作、哪个输入、在哪一步失败"的上下文；但对外返回的错误信息不能包含数据库表名、SQL 语句、堆栈、密钥、用户密码等敏感内容。

**为什么：** AI 有两种相反的倾向：要么日志只有 `"操作失败"` 一句话，查问题像盲人摸象；要么直接把框架抛出的原始异常（含 SQL 语句、文件路径、变量值）直接序列化返回给前端，攻击者可以从中提取数据库结构、推断内部逻辑。两种极端都在真实生产事故中反复出现。

**怎么做：**
- 日志（内部）：`logger.error("创建订单失败 user_id=%s product_id=%s amount=%s", uid, pid, amt, exc_info=True)` — 带参数、带堆栈。
- 响应（外部）：`{"code": "ORDER_CREATE_FAILED", "message": "订单创建失败，请稍后重试"}` — 友好文案，无内部细节。
- 生产环境关闭框架的 debug 模式（`DEBUG=False`、`NODE_ENV=production`），避免默认暴露堆栈。
- 日志脱敏：手机号、邮箱、身份证、密码、token 在写入日志前做掩码处理（`1380***8888`）。

---

### 4. 失败要清理：避免半完成态

**规则：** 操作失败时必须清理已完成的副作用：回滚数据库事务、删除已创建的临时文件、释放已获取的锁、取消已发出的可撤销请求；不能让系统停留在"一半成功一半失败"的中间状态。

**为什么：** AI 在处理多步操作时极容易只写成功路径：第一步写数据库成功，第二步发消息失败，然后 catch 里只打了一行日志——数据库里有了这条记录，但消息没发出去，系统进入不一致状态。这类 bug 不会立刻报错，会在后续的业务流程里以奇怪的方式暴露（重复处理、数据对不上），且很难复现和修复。

**怎么做：**
- 多步写操作首选数据库事务，异常时自动回滚所有步骤。
- 事务外的副作用（发邮件、上传文件、调外部 API）要么放在事务提交后执行，要么使用 Saga/补偿事务模式。
- 资源获取用 `with`/`using`/RAII 模式，保证无论正常还是异常路径都会释放：
```python
# ✅ 正例：即使中途抛异常，文件也会被关闭
with open("report.csv", "w") as f:
    write_report(f)   # 若此处抛异常，with 保证 f.close() 被调用

# ❌ 反例：异常发生后 f.close() 不会执行，文件句柄泄漏
f = open("report.csv", "w")
write_report(f)
f.close()
```
- 分布式场景：调用外部服务前记录"进行中"状态，失败时通过补偿接口或消息撤销已执行步骤。

---

### 5. 边界统一兜底，向用户返回友好信息，向日志留全栈

**规则：** 在应用最外层（HTTP 中间件、消息消费入口、定时任务入口）设置全局异常 handler，统一兜住所有漏网异常；对用户返回固定的友好提示，同时保证完整的错误信息（含堆栈）被记录到日志系统。

**为什么：** AI 生成的服务代码经常没有全局兜底——未处理的异常直接导致 Node.js 进程崩溃、Python Flask 返回裸 HTML 500 页面、Go 的 panic 泄露 goroutine 堆栈给客户端。每加一个新接口都需要记住加 try-catch，一旦有人忘了，对外就是 500 裸崩。设置全局兜底等于给整个系统加了安全气囊，不依赖每个开发者都记得处理所有异常。

**怎么做：**
```python
# FastAPI 全局异常处理示例
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    # 业务错误：记录 warn，返回 4xx
    logger.warning("业务错误 path=%s code=%s", request.url.path, exc.code)
    return JSONResponse(status_code=exc.http_status,
                        content={"code": exc.code, "message": exc.message})

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    # 意外错误：记录 error + 完整堆栈，触发告警，返回 500
    logger.error("未捕获异常 path=%s", request.url.path, exc_info=True)
    alert_oncall(exc)  # 触发告警
    return JSONResponse(status_code=500,
                        content={"code": "INTERNAL_ERROR", "message": "服务暂时异常，请稍后重试"})
```
- 全局 handler 是最后防线，不替代局部处理：能在业务层处理的错误应该在业务层处理完，全局 handler 只接住漏网的。
- 定时任务和消息消费者同样需要全局兜底，不能因为"不是 HTTP"就忘记。

---

## 正例 / 反例

### 反例：空 catch + 吞异常

```python
# 反例 — 吞掉了数据库异常，函数返回 None 假装成功
def save_order(order: Order) -> bool:
    try:
        db.session.add(order)
        db.session.commit()
        return True
    except Exception:
        pass   # ❌ 什么都没做：日志没有，回滚没有，调用方不知道失败了
    return False  # 调用方收到 False 但不知道是哪类错误，也没法重试

# 调用方
if not save_order(order):
    print("保存失败")  # ❌ 但没有任何错误信息可以定位问题
```

```python
# 正例 — 明确回滚 + 记录 + 重抛
def save_order(order: Order) -> None:
    try:
        db.session.add(order)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()                          # ✅ 清理：回滚事务
        logger.error("保存订单失败 order_id=%s", order.id, exc_info=True)  # ✅ 记录完整堆栈
        raise OrderPersistenceError("订单保存失败") from e  # ✅ 转换语义后重抛
```

---

### 反例：把原始异常直接返回给前端

```python
# 反例 — 内部 SQL 错误暴露给客户端
@app.route("/users/<int:user_id>")
def get_user(user_id):
    try:
        return jsonify(db.get_user(user_id))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        # ❌ str(e) 可能包含:
        # "column 'passwrd' does not exist in table 'users'"
        # 暴露了表名、字段名，攻击者可以利用这些信息
```

```python
# 正例 — 内外信息分离
@app.route("/users/<int:user_id>")
def get_user(user_id):
    try:
        return jsonify(db.get_user(user_id))
    except ResourceNotFoundError as e:
        return jsonify({"code": e.code, "message": e.message}), 404  # ✅ 业务错误，友好提示
    except Exception as e:
        logger.error("获取用户失败 user_id=%s", user_id, exc_info=True)  # ✅ 完整堆栈写日志
        return jsonify({"code": "INTERNAL_ERROR", "message": "服务异常"}), 500  # ✅ 对外不暴露细节
```

---

## 自查清单

- [ ] 代码中没有空 catch 块，也没有只打印后继续正常流程的 catch。
- [ ] 业务异常（校验失败、资源不存在）和系统异常（bug、宕机）已区分，分别用不同类型表达。
- [ ] 日志中包含足够的上下文（操作类型、关键参数、堆栈），可以在不重现的情况下定位问题。
- [ ] 对外的错误响应不包含数据库结构、SQL、堆栈、密钥等敏感信息。
- [ ] 多步操作失败时有清理逻辑（事务回滚、临时文件删除、锁释放），不存在半完成态。
- [ ] 资源（文件、连接、锁）用 `with`/`using`/RAII 模式管理，异常路径也能保证释放。
- [ ] 应用最外层有全局异常 handler，兜住所有未处理异常，向用户返回友好提示，向日志写完整堆栈。
