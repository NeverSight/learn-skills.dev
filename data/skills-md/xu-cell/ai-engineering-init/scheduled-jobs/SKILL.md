---
name: scheduled-jobs
description: |
  通用定时任务开发指南。涵盖 @Scheduled、Quartz、XXL-Job 等方案的概念对比与实现模式。
  触发场景：
  - 每日数据汇总、定期清理等周期性任务
  - 分布式任务调度、失败重试
  - 任务分片、广播任务
  - 可视化任务管理和监控
  触发词：定时任务、任务调度、@Scheduled、Quartz、XXL-Job、Cron、重试、分片任务、广播任务、分布式任务
  注意：如果项目有专属技能（如 `leniu-java-task`），优先使用专属版本。
---

# 定时任务开发指南

> 通用模板。如果项目有专属技能（如 `leniu-java-task`），优先使用。

## 设计原则

1. **幂等性**：任务重复执行不会产生副作用。考虑任务被重试、多次调度的情况。
2. **可观测**：任务执行结果必须可追踪（日志、监控、告警）。
3. **故障隔离**：单个任务失败不应影响其他任务的调度。
4. **超时控制**：设置合理的执行超时时间，避免任务无限阻塞。

---

## 方案对比

| 维度 | @Scheduled | Quartz | XXL-Job | 其他（SnailJob 等） |
|------|-----------|--------|---------|-------------------|
| 学习成本 | 极低 | 中等 | 低 | 低-中 |
| 分布式支持 | 无 | 支持（数据库锁） | 原生支持 | 原生支持 |
| 可视化管理 | 无 | 无（需自建） | Web 控制台 | Web 控制台 |
| 失败重试 | 无 | 支持 | 支持 | 支持 |
| 任务分片 | 不支持 | 不支持 | 支持 | 支持 |
| 广播模式 | 不支持 | 不支持 | 支持 | 支持 |
| 工作流编排 | 不支持 | 不支持 | 子任务依赖 | 部分支持 |
| 依赖 | Spring 内置 | quartz jar | 独立服务 | 独立服务 |
| 适用场景 | 简单周期任务 | 中等复杂度 | 生产级分布式 | 生产级分布式 |

### 选型决策树

```
需要分布式调度？
├── 否 → @Scheduled（简单定时）
└── 是 → 需要可视化管理？
        ├── 否 → Quartz + 数据库（中等规模）
        └── 是 → XXL-Job / SnailJob / PowerJob（生产推荐）
```

---

## 实现模式

### 方案一：@Scheduled（Spring 内置）

```java
@Component
@EnableScheduling
public class SimpleScheduledTasks {

    // 固定频率：每30秒执行一次
    @Scheduled(fixedRate = 30000)
    public void heartbeat() {
        log.info("心跳检测");
    }

    // 固定延迟：上次执行完成后等10秒再执行
    @Scheduled(fixedDelay = 10000)
    public void cleanTempFiles() {
        log.info("清理临时文件");
    }

    // Cron 表达式：每天凌晨2点执行
    @Scheduled(cron = "0 0 2 * * ?")
    public void dailyReport() {
        log.info("生成日报");
    }

    // 使用配置文件中的 Cron
    @Scheduled(cron = "${task.cleanup.cron:0 0 3 * * ?}")
    public void configuredTask() {
        log.info("可配置的定时任务");
    }
}
```

**注意事项**：
- 默认单线程执行，需配置线程池避免任务阻塞
- 多实例部署时每个实例都会执行，需分布式锁控制

```java
@Configuration
public class SchedulingConfig implements SchedulingConfigurer {
    @Override
    public void configureTasks(ScheduledTaskRegistrar registrar) {
        registrar.setScheduler(Executors.newScheduledThreadPool(5));
    }
}
```

### 方案二：Quartz

```java
// 1. 定义 Job
public class OrderCleanupJob implements Job {
    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        JobDataMap dataMap = context.getMergedJobDataMap();
        int days = dataMap.getInt("retentionDays");
        // 业务逻辑...
    }
}

// 2. 配置调度
@Configuration
public class QuartzConfig {

    @Bean
    public JobDetail orderCleanupJobDetail() {
        return JobBuilder.newJob(OrderCleanupJob.class)
            .withIdentity("orderCleanup", "maintenance")
            .usingJobData("retentionDays", 30)
            .storeDurably()
            .build();
    }

    @Bean
    public Trigger orderCleanupTrigger() {
        return TriggerBuilder.newTrigger()
            .forJob(orderCleanupJobDetail())
            .withIdentity("orderCleanupTrigger", "maintenance")
            .withSchedule(CronScheduleBuilder.cronSchedule("0 0 2 * * ?"))
            .build();
    }
}
```

### 方案三：分布式任务调度平台（XXL-Job 等）

```java
// 通用模式：注解标记任务处理器
@Component
public class OrderCleanupJobHandler {

    @Autowired
    private OrderService orderService;

    // 具体注解取决于所选平台
    // XXL-Job: @XxlJob("orderCleanupHandler")
    // SnailJob: @JobExecutor(name = "orderCleanupJob")
    public void execute(String params) {
        log.info("开始清理过期订单");
        try {
            int days = StringUtils.isBlank(params) ? 30 : Integer.parseInt(params);
            int count = orderService.cleanupExpiredOrders(days);
            log.info("清理完成，删除 {} 条", count);
        } catch (Exception e) {
            log.error("清理失败: {}", e.getMessage());
            throw e;  // 抛出异常触发平台重试
        }
    }
}
```

### 执行模式

| 模式 | 特点 | 适用场景 |
|------|------|---------|
| **集群/随机** | 多节点竞争，只有一个执行 | 订单处理、数据汇总 |
| **广播** | 所有节点都执行 | 清理本地缓存、刷新配置 |
| **分片** | 按规则分片，每节点处理部分数据 | 大数据量批处理 |
| **MapReduce** | 动态分片 + 结果汇总 | 分布式计算、统计 |

---

## 最佳实践

### 标准任务模板

```java
@Component
public class [你的任务类] {

    private static final Logger log = LoggerFactory.getLogger([你的任务类].class);

    @Autowired
    private [你的业务Service] bizService;

    public void execute(String params) {
        long startTime = System.currentTimeMillis();
        log.info("[任务开始] 参数: {}", params);

        try {
            // 1. 解析参数
            int days = parseParams(params);

            // 2. 幂等检查
            if (bizService.isAlreadyProcessed(today())) {
                log.info("[任务跳过] 今日已执行");
                return;
            }

            // 3. 执行业务逻辑
            int count = bizService.process(days);

            // 4. 记录结果
            long cost = System.currentTimeMillis() - startTime;
            log.info("[任务完成] 处理 {} 条，耗时 {} ms", count, cost);

        } catch (Exception e) {
            log.error("[任务失败] {}", e.getMessage(), e);
            throw e;  // 抛出异常触发重试
        }
    }
}
```

### 重试策略对比

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| 固定间隔 | 每次间隔相同（如 30s） | 网络抖动、临时故障 |
| 指数退避 | 间隔逐倍增加（1s, 2s, 4s, 8s...） | 服务恢复中 |
| Cron 重试 | 按 Cron 表达式重试 | 定点重试 |
| 最大次数 | 限制最大重试次数 | 防止无限重试 |

### Cron 表达式速查

| 表达式 | 含义 |
|--------|------|
| `0 0 2 * * ?` | 每天凌晨 2:00 |
| `0 0/30 * * * ?` | 每 30 分钟 |
| `0 0 9-18 * * MON-FRI` | 工作日 9-18 点每小时 |
| `0 0 0 1 * ?` | 每月 1 号零点 |
| `0 0 0 L * ?` | 每月最后一天零点 |

---

## 常见错误

```java
// 1. @Scheduled 任务中抛出异常但不处理
@Scheduled(fixedRate = 60000)
public void task() {
    service.process();  // 异常后任务停止调度！
}
// 应捕获异常
@Scheduled(fixedRate = 60000)
public void task() {
    try {
        service.process();
    } catch (Exception e) {
        log.error("任务执行失败", e);
    }
}

// 2. @Scheduled 默认单线程，长任务阻塞其他任务
// 应配置线程池（见上文 SchedulingConfig）

// 3. 多实例部署未做互斥
// @Scheduled 每个实例都执行 -> 数据重复处理
// 应使用分布式锁（Redis / 数据库）或分布式调度平台

// 4. 任务非幂等
public void syncData() {
    insertAll(fetchData());  // 重复执行会插入重复数据
}
// 应先检查是否已处理

// 5. 任务内开启大事务
@Transactional
public void processAllOrders() {
    // 处理百万条数据在一个事务中 -> 内存溢出、锁超时
}
// 应分批处理，每批独立事务
```
