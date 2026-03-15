---
name: leniu-code-patterns
description: |
  leniu-tengyun-core 项目代码规范速查。基于 pigx-framework 框架的后端代码禁令和编码规范。

  触发场景：
  - 查看项目禁止事项（leniu 后端代码）
  - 命名规范速查
  - Git 提交规范
  - 避免过度工程
  - 代码风格检查

  触发词：代码禁令、代码规范、命名规范、代码风格、Git提交规范、包结构、禁止写法、审计字段规范、delFlag、crby/crtime
---

# leniu-tengyun-core 代码规范速查

## leniu 项目特征

| 项目特征 | 说明 |
|----------|------|
| **包名前缀** | `net.xnzn.core.*` |
| **JDK 版本** | 21 |
| **Validation** | `jakarta.validation.*` |
| **工具库** | Hutool (CollUtil, ObjectUtil, BeanUtil) |
| **分页组件** | PageHelper (PageMethod) |
| **对象转换** | `BeanUtil.copyProperties()` |
| **异常类** | `LeException` |
| **国际化** | `I18n` |
| **租户上下文** | `TenantContextHolder` |

## 与 RuoYi-Vue-Plus 对比

| 特征 | RuoYi-Vue-Plus | leniu-tengyun-core |
|---------|----------------|-------------------|
| **包名前缀** | `org.dromara.*` | `net.xnzn.core.*` |
| **JDK 版本** | 17 | 21 |
| **Validation** | `jakarta.validation.*` | `jakarta.validation.*` |
| **工具库** | 自定义工具类 | Hutool |
| **分页** | `TableDataInfo<T>` | `Page<T>` |
| **对象转换** | `MapstructUtils.convert()` | `BeanUtil.copyProperties()` |
| **异常类** | `ServiceException` | `LeException` |
| **国际化** | `MessageUtils.message()` | `I18n.getMessage()` |
| **审计字段** | create_by/create_time/update_by/update_time | crby/crtime/upby/uptime |
| **逻辑删除** | 0=正常, 2=删除 | 1=删除, 2=正常 |

## 后端禁令速查表

> **快速查表**：一眼定位所有后端代码禁止写法

| 禁止项 | ❌ 禁止写法 | ✅ 正确写法 | 原因 |
|--------|-----------|-----------|------|
| 包名规范 | `org.dromara.*` | `net.xnzn.core.*` | 包名统一标准 |
| 完整引用 | `org.dromara.xxx.Xxx` | `import` + 短类名 | 代码整洁 |
| Map 封装业务数据 | `Map<String, Object>` | 创建 VO 类 | 类型安全 |
| Service 继承基类 | `extends ServiceImpl<>` | `implements XxxService` | 三层架构 |
| 查询构建位置 | Controller 层 | **Service 层** | 职责分离 |
| 对象转换工具 | `MapstructUtils` | `BeanUtil.copyProperties()` | 项目统一规范 |
| 审计字段命名 | create_by/create_time | crby/crtime | 项目规范 |
| 逻辑删除值 | 0=正常, 2=删除 | 2=正常, 1=删除 | 项目规范 |
| 异常类 | `ServiceException` | `LeException` | 项目规范 |
| 国际化工具 | `MessageUtils` | `I18n` | 项目规范 |

## 后端禁令详解

### 1. 包名必须是 `net.xnzn.core.*`

```java
// ✅ 正确
package net.xnzn.core.order.service;
package net.xnzn.core.marketing.handler;

// ❌ 错误
package org.dromara.system.service;
package plus.ruoyi.business.service;
```

### 2. 禁止使用完整类型引用

```java
// ✅ 正确：先 import 再使用
import net.xnzn.core.common.response.LeResponse;
public LeResponse<XxxVo> getXxx(Long id) { ... }

// ❌ 错误：直接使用完整包名
public net.xnzn.core.common.response.LeResponse<XxxVo> getXxx(Long id) { ... }
```

### 3. 禁止使用 Map 封装业务数据

```java
// ✅ 正确：创建 VO 类
public XxxVo getXxx(Long id) {
    XxxEntity entity = mapper.selectById(id);
    return BeanUtil.copyProperties(entity, XxxVo.class);
}

// ❌ 错误：使用 Map
public Map<String, Object> getXxx(Long id) {
    XxxEntity entity = mapper.selectById(id);
    Map<String, Object> result = new HashMap<>();
    result.put("id", entity.getId());
    return result;
}
```

### 4. Service 禁止继承 ServiceImpl 基类

```java
// ✅ 正确：不继承任何基类，直接注入 Mapper
@Service
public class XxxServiceImpl implements XxxService {
    @Autowired
    private XxxMapper mapper;
}

// ❌ 错误：继承 ServiceImpl
public class XxxServiceImpl extends ServiceImpl<XxxMapper, Xxx> {
}
```

### 5. 查询条件必须在 Service 层构建

```java
// ✅ 正确：在 Service 层构建查询条件
@Service
public class XxxServiceImpl implements XxxService {

    @Autowired
    private XxxMapper mapper;

    private LambdaQueryWrapper<Xxx> buildWrapper(XxxParam param) {
        return Wrappers.lambdaQuery()
            .eq(param.getStatus() != null, Xxx::getStatus, param.getStatus());
    }

    public List<XxxVo> list(XxxParam param) {
        return mapper.selectList(buildWrapper(param));
    }
}

// ❌ 错误：在 Controller 层构建查询条件
@RestController
public class XxxController {
    @GetMapping("/list")
    public LeResponse<List<XxxVo>> list(XxxParam param) {
        LambdaQueryWrapper<Xxx> wrapper = new LambdaQueryWrapper<>();  // 禁止！
    }
}
```

### 6. 使用正确的对象转换工具

```java
// ✅ 正确：使用 BeanUtil
import cn.hutool.core.bean.BeanUtil;

XxxVo vo = BeanUtil.copyProperties(entity, XxxVo.class);
List<XxxVo> voList = BeanUtil.copyToList(entities, XxxVo.class);

// ❌ 错误：使用 MapstructUtils（RuoYi 的工具类）
import org.dromara.common.core.utils.MapstructUtils;

XxxVo vo = MapstructUtils.convert(entity, XxxVo.class);
```

### 7. 使用正确的审计字段命名

```java
// ✅ 正确：leniu 审计字段
@Data
public class XxxEntity {
    private String crby;      // 创建人
    private LocalDateTime crtime; // 创建时间
    private String upby;      // 更新人
    private LocalDateTime uptime; // 更新时间
    private Integer delFlag;   // 删除标识（1=删除，2=正常）
}

// ❌ 错误：RuoYi 审计字段
@Data
public class XxxEntity {
    private String createBy;   // ❌
    private LocalDateTime createTime; // ❌
    private String updateBy;   // ❌
    private LocalDateTime updateTime; // ❌
}
```

### 8. 使用正确的逻辑删除值

```java
// ✅ 正确：leniu 使用 2 表示正常
wrapper.eq(XxxEntity::getDelFlag, 2);

// ❌ 错误：RuoYi 使用 0 表示正常
wrapper.eq(XxxEntity::getDelFlag, 0);
```

### 9. 使用正确的异常类

```java
// ✅ 正确：使用 leniu 的异常
import net.xnzn.core.common.exception.LeException;

throw new LeException("订单不存在");
throw new LeException(I18n.getMessage("order.not.exists"));

// ❌ 错误：使用 RuoYi 的异常
import org.dromara.common.core.exception.ServiceException;

throw new ServiceException("订单不存在");
```

### 10. 使用正确的国际化工具

```java
// ✅ 正确：使用 leniu 的国际化
import net.xnzn.core.common.i18n.I18n;

throw new LeException(I18n.getMessage("order.not.exists"));
throw new LeException(I18n.getMessage("user.password.retry.limit.exceed", maxRetryCount));

// ❌ 错误：使用 RuoYi 的国际化
import org.dromara.common.core.utils.MessageUtils;

throw new ServiceException(MessageUtils.message("order.not.exists"));
```

## 命名规范速查

### 后端命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 包名 | 小写，点分隔 | `net.xnzn.core.order` |
| 类名 | 大驼峰 | `OrderServiceImpl` |
| 方法名 | 小驼峰 | `pageList`, `getById` |
| 变量名 | 小驼峰 | `userName`, `crtime` |
| 常量 | 全大写下划线 | `MAX_PAGE_SIZE` |
| 表名 | 小写下划线 | `order_table` |
| 字段名 | 小写下划线 | `order_amount`, `crby` |

### 类命名后缀

| 类型 | 后缀 | 示例 |
|------|------|------|
| 实体类 | 无/Entity | `Order`, `OrderEntity` |
| VO | XxxVO | `OrderVO` |
| DTO | XxxDTO | `OrderDTO` |
| Param | XxxParam/XxxQueryParam | `OrderQueryParam` |
| Service 接口 | XxxService | `OrderService` |
| Service 实现 | XxxServiceImpl | `OrderServiceImpl` |
| Controller | XxxController | `OrderController` |
| Mapper | XxxMapper | `OrderMapper` |
| Enum | XxxEnum | `OrderStatusEnum` |
| Handler | XxxHandler | `OrderHandler` |

### 方法命名

| 操作 | Service 方法 | Mapper 方法 |
|------|-------------|-------------|
| 分页查询 | `pageXxx` | `pageXxx` |
| 查询列表 | `listXxx` | `listXxx` |
| 查询单个 | `getXxx` | `selectById` |
| 新增 | `save` / `add` / `create` | `insert` |
| 更新 | `update` / `modify` | `updateById` |
| 删除 | `delete` / `remove` | `deleteById` |

## 避免过度工程

### 不要做的事

1. **不要创建不必要的抽象**
   - 只有一处使用的代码不需要抽取
   - 三处以上相同代码才考虑抽取

2. **不要添加不需要的功能**
   - 只实现当前需求
   - 不要"以防万一"添加功能

3. **不要过早优化**
   - 优先使用简单直接的方案
   - 复杂方案需要有明确理由

4. **不要添加无用注释**
   - 不要给显而易见的代码加注释
   - 只在逻辑复杂处添加注释

5. **不要保留废弃代码**
   - 删除不用的代码，不要注释保留
   - Git 有历史记录

## Git 提交规范

### 格式

```
<type>(<scope>): <description>
```

### 类型

| type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | 修复 Bug |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响逻辑） |
| `refactor` | 重构（不是新功能或修复） |
| `perf` | 性能优化 |
| `test` | 测试 |
| `chore` | 构建/工具 |

### 示例

```bash
feat(order): 新增订单创建功能
fix(order): 修复订单状态显示错误
docs(readme): 更新安装说明
refactor(common): 重构分页查询工具类
perf(order): 优化订单列表查询性能
```

## Hutool 工具类速查

```java
import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.ObjectUtil;
import cn.hutool.core.util.StrUtil;
import cn.hutool.core.bean.BeanUtil;

// 集合判空
if (CollUtil.isEmpty(list)) { }
if (CollUtil.isNotEmpty(list)) { }

// 对象判空
if (ObjectUtil.isNull(obj)) { }
if (ObjectUtil.isNotNull(obj)) { }

// 字符串判空
if (StrUtil.isBlank(str)) { }
if (StrUtil.isNotBlank(str)) { }

// 对象拷贝
Target target = BeanUtil.copyProperties(source, Target.class);
List<Target> targets = BeanUtil.copyToList(sources, Target.class);
```

## 包结构规范

```
net.xnzn.core
├── [module]/
│   ├── controller/         # 控制器层（按端分：web/mobile/android）
│   ├── business/impl/      # 业务编排层
│   ├── service/impl/       # 服务层
│   ├── mapper/             # 数据访问层（含 XML 同目录）
│   ├── model/              # 数据模型（Entity）
│   ├── vo/                 # 视图对象（返回前端）
│   ├── dto/                # 数据传输对象（服务间/MQ）
│   ├── param/              # 请求参数对象
│   ├── constants/          # 常量和枚举
│   ├── config/             # 配置类
│   ├── mq/                 # 消息队列监听器
│   ├── task/               # 定时任务
│   ├── handle/             # 业务处理器（策略模式）
│   └── util/               # 工具类
```

## 依赖注入规范

```java
// 推荐：字段注入
@Autowired
private OrderService orderService;

// 解决循环依赖
@Resource
@Lazy
private ProductService productService;
```

## 类注释规范

```java
/**
 * 类功能描述
 *
 * @author xujiajun
 * @date 2026-02-20
 */
public class OrderService {
}
```

## 数据类型规范

### 布尔字段命名

```java
// ❌ 错误：前缀冗余、类型错误
private Integer ifNarrow;
private Integer isEnabled;

// ✅ 正确：Boolean 类型，无前缀
private Boolean narrow;     // getter → isNarrow()
private Boolean enabled;    // getter → isEnabled()
```

### 枚举字段标注

```java
// ❌ 错误：只靠注释 @see
/** @see AccTradeTypeEnum */
private Integer tradeType;

// ✅ 方案一：VO/DTO 用枚举类型（配合 @JsonValue）
private AccTradeTypeEnum tradeType;

// ✅ 方案二：@ApiModelProperty 标注合法值
@ApiModelProperty(value = "操作类型：1-充值 2-消费 3-退款", allowableValues = "1,2,3")
private Integer tradeType;
```

## MyBatis-Plus 安全规范

### selectOne 必须有唯一保障

```java
// ❌ 危险：多条记录时抛 TooManyResultsException
Entity entity = mapper.selectOne(wrapper);

// ✅ 方案一：LIMIT 1
Entity entity = mapper.selectOne(wrapper.last("LIMIT 1"));

// ✅ 方案二：selectList 取第一条
List<Entity> list = mapper.selectList(wrapper);
Entity entity = CollUtil.isNotEmpty(list) ? list.get(0) : null;

// ✅ 方案三：确保有唯一索引（注释说明）
// 唯一索引：UNIQUE KEY (order_no, del_flag)
Entity entity = mapper.selectOne(wrapper);
```

### 存在性判断用 EXISTS，禁用 selectCount

```java
// ❌ 低效：100万行表 ~200ms
Long count = mapper.selectCount(wrapper);
if (count > 0) { ... }

// ✅ 高效：~2ms（MyBatis-Plus 3.5.4+）
boolean exists = mapper.exists(wrapper);

// ✅ 或 selectList + LIMIT 1
boolean exists = CollUtil.isNotEmpty(mapper.selectList(wrapper.last("LIMIT 1")));
```

### Wrapper 嵌套不超过 2 层

```java
// ❌ 过于复杂的 Wrapper
wrapper.and(w -> w.eq(A::getType, type)
    .or(q -> q.eq(A::getType, 0))
    .or(!PersonTypeEnum.LABOUR.getKey().equals(type),
        q -> q.eq(A::getType, PSN_TYPE_SHARED)));

// ✅ 复杂查询写到 XML 中
List<Entity> list = mapper.selectByTypeCondition(type, isLabour);
```

### 禁止 SELECT *

```xml
<!-- ❌ 禁止 -->
<select id="selectAll">SELECT * FROM t_order WHERE del_flag = 2</select>

<!-- ✅ 明确列出字段 -->
<select id="selectAll">SELECT id, order_no, amount, status, crtime FROM t_order WHERE del_flag = 2</select>
```

## Redis 使用规范

### 禁止 KEYS 命令

```java
// ❌ 严禁：KEYS 阻塞 Redis
Set<Object> keys = keysByPattern(pattern);
Set<Object> keys = redisTemplate.keys(pattern);

// ✅ 使用 Redisson deleteByPattern（内部 SCAN + UNLINK）
RedissonClient redisson = SpringUtil.getBean(RedissonClient.class);
redisson.getKeys().deleteByPattern(keyPattern);
```

## Optional 使用规范

```java
// ❌ 错误：of() 不接受 null
Optional.of(value).orElse(defaultValue);

// ✅ 正确：ofNullable()
Optional.ofNullable(value).orElse(defaultValue);

// ✅ 链式安全转换
Optional.ofNullable(model.getReserveRate())
    .map(BigDecimal::new)
    .orElse(BigDecimal.ZERO);

// ❌ 禁止作为方法参数或类字段
// ✅ 允许作为方法返回值
```

## @Transactional 规范

```java
// ❌ 默认只回滚 RuntimeException
@Transactional
public void createOrder() { ... }

// ✅ 显式指定 rollbackFor
@Transactional(rollbackFor = Exception.class)
public void createOrder() { ... }
```

- 事务方法不要 try-catch 吞掉异常
- 只读查询不加 `@Transactional`

## 业务逻辑分层规范

```java
// ❌ 错误：业务判断混在数据操作中
public void processOrder(Long orderId) {
    OrderInfo order = orderMapper.selectById(orderId);
    if (order.getStatus() == 1 && order.getPayTime() != null
        && ChronoUnit.HOURS.between(order.getPayTime(), LocalDateTime.now()) < 24) {
        order.setStatus(2);
        orderMapper.updateById(order);
        accWalletService.deduct(order.getCustId(), order.getAmount());
    }
}

// ✅ 正确：分层清晰
public void processOrder(Long orderId) {
    OrderInfo order = orderMapper.selectById(orderId);
    if (ObjectUtil.isNull(order)) {
        throw new LeException(I18n.getMessage("order_not_found"));
    }
    checkCanProcess(order);           // 业务校验（独立方法）
    order.markAsProcessed();          // 状态变更（Entity 方法封装）
    orderMapper.updateById(order);
    afterOrderProcessed(order);       // 后续动作（独立方法）
}
```

| 层 | 职责 | 不应做的 |
|----|------|---------|
| Controller | 参数接收、格式转换 | 不含业务判断 |
| Business | 业务编排、跨 Service 协调 | 不直接操作 Mapper |
| Service | 单表 CRUD、单表事务 | 不含跨表业务逻辑 |
| Mapper | SQL 映射 | 不含业务逻辑 |

## TODO 管理规范

```java
// ❌ 错误
// TODO 修改一下

// ✅ 正确
// TODO(@陈沈杰, 2026-03-20, #TASK-1234): 移动端 AppId 赋值逻辑待产品确认
```

- 不用的代码直接删除，不要注释保留

## 通用代码规范

1. **禁止使用 `SELECT *`**：明确指定字段
2. **使用参数化查询**：`#{}` 而非 `${}`
3. **异常必须处理**：不能吞掉异常
4. **日志使用占位符**：`log.info("msg: {}", value)`
5. **敏感信息脱敏**：不记录密码、身份证等
6. **集合判空**：使用 `CollUtil.isEmpty()` 或类似方法
7. **空指针防护**：使用 `ObjectUtil.isNull()`

## 参考文档

详见：[leniu-tengyun-core 源码](/Users/xujiajun/Developer/gongsi_proj/core/leniu-tengyun-core)
