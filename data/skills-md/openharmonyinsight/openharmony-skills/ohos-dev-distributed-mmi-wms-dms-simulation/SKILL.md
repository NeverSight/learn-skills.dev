---
name: ohos-dev-distributed-mmi-wms-dms-simulation
description: Use when testing OpenHarmony input features that depend on window/display state without running real WMS/DMS. Builds requested simulation scenarios from display groups, users, main/extended/mirror displays, per-display focus windows, z-order window stacks, hot areas, dynamic focus switching, pointer style, capture mode, scroll wheel, and device binding.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: wms-dms-simulation
  version: 0.2.0
  status: draft
  tags:
    - multimodalinput
    - wms-simulation
    - display-group
    - window-management
    - z-order
  related-skills:
    - ohos-dev-distributed-mmi-device-test-harness
    - ohos-dev-distributed-mmi-uinput-virtual-device
---

# WMS/DMS 模拟

测试进程直接通过 InputManager IPC 构造显示组和窗口，替代 WMS（窗口管理服务）和 DMS（显示管理服务），实现输入子系统的独立功能验证。

**前置 skill**: 权限获取、server 绕过、编译部署、hidumper 捕获等基础设施见 `ohos-dev-distributed-mmi-device-test-harness`；虚拟设备创建和事件注入见 `ohos-dev-distributed-mmi-uinput-virtual-device`。

## When to Use

- 按测试要求模拟显示组、用户、主屏、扩展屏、镜像屏和窗口栈
- 测试依赖显示组/窗口状态的输入功能（设备绑定、光标路由、焦点分发、命中测试）
- 验证单显示组多屏、多显示组多用户、镜像屏比例不一致、前台用户切换等场景
- 不想或不能启动完整 WMS/DMS 栈时

## 已验证能力摘要

DAYU200 真机 `dual_group_interleave_test` 已覆盖双显示组构造、多窗口注入、per-group
光标/按钮/键盘/焦点/captureMode/滚轮隔离、热拔插绑定清理、跨绑定按键状态和 per-window
光标外观。详细步骤、dump 证据和 PARTIAL 项见 `evals/test-results.md`，不要把长篇实测表格复制到
`SKILL.md` 主流程。

## Scenario-First 建模流程

不要从固定 demo 出发。先把用户要求归一成这张模型表，再生成 `UserScreenInfo` 和窗口注入：

| 维度 | 必填内容 | 关键约束 |
|------|---------|----------|
| User | `userId`、是否前台/ACTIVE | 只模拟前台用户时，所有目标 `UserScreenInfo` 都应可写入 active display group 状态 |
| DisplayGroup | `groupId`、`type`、`mainDisplayId`、`focusWindowId` | 必须有一个 `GROUP_DEFAULT` 且 id=0；其他组用 `GROUP_SPECIAL` |
| Display | 主屏/扩展屏/镜像屏的 `displayId`、位置、尺寸、dpi、direction | `screenArea` 必须和 display 坐标/尺寸一致；扩展屏坐标不能无意重叠 |
| Mirror | 镜像源 display、镜像 display、缩放比例或 letterbox/crop 策略 | 镜像屏比例和主屏不一致时要显式建模坐标映射，不能假设 1:1 |
| Screen | 与每个 display 对应的 `ScreenInfo` | `screens` 数量和 id 必须覆盖所有 displays |
| Window | 每屏焦点窗口、背景窗口、浮窗、遮挡窗口、hotArea | `win.groupId`/`displayId` 必须匹配目标 display；zOrder 必须体现层叠关系 |
| Focus | 每个 display 的焦点窗口，以及 group 级键盘焦点 | `DisplayGroupInfo.focusWindowId` 是键盘路由关键；每屏焦点窗口也要体现在窗口栈中 |

输出模拟方案时，先给出模型表，再给出 C++ helper 或伪代码。不要只贴单一固定 `SetupDualDisplayGroups()`。

## 标准场景模板

### 单显示组：主屏 + 扩展屏 + 主屏镜像屏

用于验证一个用户/一个 display group 内的多屏路由、每屏焦点窗口、镜像屏坐标映射和多窗口层叠：

| 对象 | 建议建模 |
|------|----------|
| group | `groupId=0`, `GROUP_DEFAULT`, `mainDisplayId=0` |
| 主屏 | `displayId=0`, `screenArea={0,0,720,1280}` |
| 扩展屏 | `displayId=1`, `screenArea={720,0,1920,1080}`，与主屏横向拼接 |
| 镜像屏 | `displayId=2`, `screenArea={2640,0,1024,768}`，镜像主屏但比例不同 |
| 焦点窗口 | 每个 display 至少一个 focus window，例如 1000/1100/1200 |
| 层叠窗口 | 每屏背景窗口、状态栏/系统层、浮窗，使用不同 zOrder |
| hotArea | 镜像屏和扩展屏都要配置 `pointerHotAreas`，用于命中测试 |

镜像屏比例不一致时，必须在测试说明中写清楚期望坐标策略：

- **fit/letterbox**：保持主屏比例，镜像屏部分区域无有效 hotArea。
- **stretch**：主屏坐标按 X/Y 独立比例映射到镜像屏。
- **crop**：镜像屏只覆盖主屏裁剪区域。

MMI 的窗口命中只看注入的 display/window 几何信息；如果要验证镜像坐标换算，测试代码必须把源屏坐标转换为镜像屏 display 坐标后再注入事件或验证目标窗口。

### 多显示组多用户：每组都是主屏 + 扩展屏 + 镜像屏

用于验证不同前台用户或并行前台场景下的显示组隔离：

| 对象 | 建议建模 |
|------|----------|
| user A group | `userId=100`, `groupId=0`, `GROUP_DEFAULT` |
| user B group | `userId=101`, `groupId=10`, `GROUP_SPECIAL` 或按被测模型分配非 0 group |
| 每个 group | 都包含 main/extended/mirror 三类 display |
| displayId | 全局唯一，不同 group 不能复用同一 displayId |
| windowId | 全局唯一，建议按 group/display 分段编号 |
| focus | 每个 group 设置 group 级 focusWindowId；每个 display 都有自己的可命中焦点窗口 |
| mirror mismatch | 每组至少一个镜像屏比例不同，用来验证坐标和命中隔离 |

如果底层 `UserScreenInfo` 一次只表达一个 user，则按用户分别调用 `UpdateDisplayInfo`，并在报告中说明“多用户均为前台/ACTIVE”的模拟假设。不要把多个用户的窗口混到同一个 group 后声称验证了多用户隔离。

## 构造显示组（替代 DMS）

下面是最小构造片段。真实测试应按上面的 scenario model 生成多个 display、screen 和 group。

```cpp
#include "input_manager.h"

UserScreenInfo screenInfo;
screenInfo.userId = 100;

// Group 0: 默认组（主屏）
DisplayGroupInfo group0;
group0.id = 0;
group0.name = "default";
group0.type = GroupType::GROUP_DEFAULT;
group0.mainDisplayId = 0;
group0.focusWindowId = 1000;

DisplayInfo disp0;
disp0.id = 0;
disp0.x = 0; disp0.y = 0;
disp0.width = 720; disp0.height = 1280;
disp0.dpi = 240;
disp0.name = "main";
disp0.direction = DIRECTION0;
disp0.displayDirection = DIRECTION0;
disp0.screenArea = { .id = 0, .area = { 0, 0, 720, 1280 } };
group0.displaysInfo.push_back(disp0);

// Group 1: 特殊组（另一个显示组；单组多屏时可改为给 group0 增加 display1/display2）
DisplayGroupInfo group1;
group1.id = 1;
group1.name = "secondary";
group1.type = GroupType::GROUP_SPECIAL;
group1.mainDisplayId = 1;
group1.focusWindowId = 2000;

DisplayInfo disp1;
disp1.id = 1;
disp1.x = 0; disp1.y = 0;
disp1.width = 1920; disp1.height = 1080;
disp1.dpi = 160;
disp1.name = "secondary";
disp1.direction = DIRECTION0;
disp1.displayDirection = DIRECTION0;
disp1.screenArea = { .id = 1, .area = { 0, 0, 1920, 1080 } };
group1.displaysInfo.push_back(disp1);

// 单组多屏时，扩展屏/镜像屏也可以 push 到同一个 group：
// group0.displaysInfo.push_back(extendedDisplay);
// group0.displaysInfo.push_back(mirrorDisplay);

screenInfo.displayGroups.push_back(group0);
screenInfo.displayGroups.push_back(group1);

// 物理屏幕信息（必须与 displaysInfo 对应）
ScreenInfo screen0;
screen0.id = 0;
screen0.uniqueId = "default0";
screen0.width = 720; screen0.height = 1280;
screen0.physicalWidth = 62; screen0.physicalHeight = 110;
screen0.dpi = 240; screen0.ppi = 295;
screen0.tpDirection = DIRECTION0;
screenInfo.screens.push_back(screen0);

ScreenInfo screen1;
screen1.id = 1;
screen1.uniqueId = "secondary1";
screen1.width = 1920; screen1.height = 1080;
screen1.physicalWidth = 531; screen1.physicalHeight = 299;
screen1.dpi = 160; screen1.ppi = 92;
screen1.tpDirection = DIRECTION0;
screenInfo.screens.push_back(screen1);

InputManager::GetInstance()->UpdateDisplayInfo(screenInfo);
```

### 关键约束

| 字段 | 约束 | 后果 |
|------|------|------|
| `group0.type` | 必须有一个 `GROUP_DEFAULT` | `InitDisplayGroupInfo` 校验 groupId==MAIN_GROUPID |
| `group0.id` | DEFAULT 组 id 必须为 0 | 非 0 会被拒绝 |
| `focusWindowId` | 必须在 DisplayGroupInfo 中预设 | 键盘事件路由依赖此值，不设则为 -1 导致键盘事件无法分发 |
| `screenArea` | 必须与 width/height 一致 | 光标边界夹紧依赖此值 |
| `screens` 数量和 ID | 必须与 displaysInfo 对应 | 屏幕信息用于 DPI/PPI 计算 |
| `userState` | 默认 `USER_ACTIVE`，无需设置 | 非 ACTIVE 时 displayGroupInfoMap_ 不写入 |
| `displayId` | 全局唯一 | 多组/多用户复用 displayId 会导致路由和 dump 解释混乱 |
| 镜像屏比例 | 必须显式说明映射策略 | 不同比例镜像屏不能直接用主屏坐标断言命中 |

### 返回码

`UpdateDisplayInfo` 返回 -201 是正常的 — 这是 `UpdateUIExtensionInfo` 的错误码，不影响显示组数据的写入。

## 注入虚拟窗口（替代 WMS）

每个 display 至少需要一个可命中的窗口。复杂场景应为每个 display 注入自己的背景窗口、焦点窗口和需要验证的层叠窗口：

```cpp
WindowGroupInfo wgi0;
wgi0.focusWindowId = 1000;
wgi0.displayId = 0;

WindowInfo win0;
win0.id = 1000;
win0.pid = getpid();
win0.uid = getuid();
win0.area = { 0, 0, 720, 1280 };
win0.defaultHotAreas = { { 0, 0, 720, 1280 } };
win0.pointerHotAreas = { { 0, 0, 720, 1280 } };
win0.agentWindowId = -1;
win0.flags = 0;
win0.action = WINDOW_UPDATE_ACTION::ADD;
win0.displayId = 0;
win0.groupId = 0;
win0.zOrder = 1.0f;
wgi0.windowsInfo.push_back(win0);

InputManager::GetInstance()->UpdateWindowInfo(wgi0);
```

### 关键约束

| 字段 | 约束 |
|------|------|
| `win.groupId` | 必须匹配目标显示组 ID |
| `win.displayId` | 必须匹配显示组内的 display ID |
| `win.pid` | 用 `getpid()` — 权限检查需要 |
| `win.action` | 首次用 `ADD`，更新用 `CHANGE` |
| `wgi.focusWindowId` | 对 MAIN_GROUPID 生效；非主组从 displayGroupInfoMap_ 读取 |
| `pointerHotAreas` | 鼠标事件命中测试依赖此区域 |
| `win.id` | 全局唯一 | 多屏/多组复用 windowId 会让 dump 和分发结果不可审计 |
| `zOrder` | 按业务层级显式区分 | 所有窗口同 zOrder 时命中顺序不可作为证据 |

### 每屏窗口栈模式

为每个 display 建议至少构造：

| 窗口 | zOrder | 作用 |
|------|-------:|------|
| background/app | 10 | 默认命中目标 |
| panel/status/system | 100 | 验证系统层优先级 |
| popup/floating | 200+ | 验证重叠命中和 DEL 后回退 |

每屏焦点窗口可以是 background，也可以是专门的输入窗口；需要在模型表中标明。

## 增量窗口操作

单个窗口的 ADD/CHANGE/DEL，无需重新注入全部窗口：

```cpp
static void InjectSingleWindow(int32_t winId, int32_t groupId, int32_t displayId,
    Rect area, float zOrder, WINDOW_UPDATE_ACTION action, int32_t focusWinId = -1)
{
    WindowGroupInfo wgi;
    wgi.focusWindowId = focusWinId;
    wgi.displayId = displayId;
    WindowInfo win;
    win.id = winId;
    win.pid = getpid();
    win.uid = getuid();
    win.area = area;
    win.defaultHotAreas = { area };
    win.pointerHotAreas = { area };
    win.agentWindowId = -1;
    win.flags = 0;
    win.action = action;
    win.displayId = displayId;
    win.groupId = groupId;
    win.zOrder = zOrder;
    wgi.windowsInfo.push_back(win);
    InputManager::GetInstance()->UpdateWindowInfo(wgi);
}
```

`UpdateDisplayInfoByIncrementalInfo` 处理：`ADD` 追加（已存在则替换），`CHANGE` 就地替换，`DEL` 从列表移除。

## 动态焦点切换

### 主组 (groupId=0)

`UpdateWindowInfo` 使用传入的 `wgi.focusWindowId`，直接生效。

### 非主组 (groupId!=0)

`UpdateWindowInfo` 忽略传入的 `focusWindowId`，始终从 `displayGroupInfoMap_` 读取。**必须通过 `UpdateDisplayInfo` 更新焦点：**

```cpp
SetupDualDisplayGroups(1000, 2002);  // 重新调用 UpdateDisplayInfo
sleep(1s);
InjectVirtualWindows();               // 重新注入窗口（同步 focusWinId 全局变量）
sleep(1s);
```

多屏场景里要区分：

- **group 级键盘焦点**：由 `DisplayGroupInfo.focusWindowId` 决定。
- **每屏期望焦点窗口**：由测试窗口栈和命中坐标体现，不要误认为 MMI 会为每个 display 自动维护独立键盘焦点。
- 如果需求声称“每个屏幕都有自己的焦点窗口”，测试应明确这是窗口栈/命中目标焦点，还是输入框架实际键盘焦点。两者不能混写。

**实现模式**：使用全局变量跟踪焦点，`SetupDualDisplayGroups` 和 `InjectVirtualWindows` 共享：

```cpp
static int32_t g_focusWin0 = 1000;
static int32_t g_focusWin1 = 2000;

static void SetupDualDisplayGroups(int32_t focusWin0 = 1000, int32_t focusWin1 = 2000)
{
    g_focusWin0 = focusWin0;
    g_focusWin1 = focusWin1;
    // ... UpdateDisplayInfo with focusWin0/focusWin1
}

static void InjectVirtualWindows()
{
    // wgi.focusWindowId = g_focusWin0;  // 不再硬编码
    // ...
}
```

## 多窗口 z-order 命中测试

### 基本模式：不同区域不同层级

```cpp
// Group 0: 3 个窗口
// win1000: 应用窗口(背景)  area={0,80,720,1200}   zOrder=10
// win1001: 状态栏          area={0,0,720,80}       zOrder=100
// win1002: 悬浮球          area={600,600,120,120}   zOrder=200
```

`SelectWindowInfo` 按 zOrder 降序遍历，第一个 `pointerHotAreas` 命中的窗口为目标。重叠区域 zOrder 高的优先。

### 全屏重叠模式：位置无关验证

ADD 多个全屏窗口（不同 zOrder），无需光标定位 — 全屏窗口在任意光标位置都命中：

```cpp
InjectSingleWindow(1005, 0, 0, {0,0,720,1280}, 50.0f, WINDOW_UPDATE_ACTION::ADD, g_focusWin0);
InjectSingleWindow(1006, 0, 0, {0,0,720,1280}, 150.0f, WINDOW_UPDATE_ACTION::ADD, g_focusWin0);
InjectSingleWindow(1007, 0, 0, {0,0,720,1280}, 250.0f, WINDOW_UPDATE_ACTION::ADD, g_focusWin0);
// 点击 → Cursor Info.windowId = 1007 (z=250 最高)
// DEL win1007 → 点击 → windowId 变为原有最高层（可能是 win1002=z200，不一定是 win1006=z150）
```

**注意**：DEL 全屏窗口后，命中目标取决于剩余所有窗口的 zOrder，包括原有非全屏窗口。上例中 DEL win1007(z=250) 后，如果光标位置在 win1002(z=200) 的 hotArea 内，则命中 win1002 而非 win1006(z=150)。

### 热区穿透

`area` 和 `pointerHotAreas` 可以不同。光标在 `area` 内但 `pointerHotAreas` 外时，点击穿透到下层窗口：

```cpp
// win1004: area 大于 hotArea
WindowInfo win;
win.area = { 100, 200, 400, 400 };
win.defaultHotAreas = { { 200, 300, 200, 200 } };  // hotArea 小于 area
win.pointerHotAreas = { { 200, 300, 200, 200 } };
// 点击 (150,250) — area 内但 hotArea 外 → 穿透到下层
// 点击 (350,450) — hotArea 内 → 命中此窗口
```

## 窗口生命周期 (ADD → CHANGE → DEL)

```cpp
// ADD: 新增弹窗
InjectSingleWindow(1003, 0, 0, {200,200,320,320}, 300.0f, WINDOW_UPDATE_ACTION::ADD, 1000);
// 点击 (360,360) → 命中 win1003

// CHANGE: 移动弹窗位置
InjectSingleWindow(1003, 0, 0, {400,800,320,320}, 300.0f, WINDOW_UPDATE_ACTION::CHANGE, 1000);
// 点击原位置 (360,360) → 穿透到 win1000

// DEL: 删除弹窗
InjectSingleWindow(1003, 0, 0, {0,0,0,0}, 0.0f, WINDOW_UPDATE_ACTION::DEL, 1000);
// 窗口列表恢复
```

## 可用的验证 API

```cpp
// 设备绑定（详见 ohos-dev-distributed-mmi-device-test-harness）
InputManager::GetInstance()->BindDeviceToDisplayGroupByDisplay(deviceId, displayId, msg);
InputManager::GetInstance()->UnbindDeviceFromDisplayGroup(deviceId, msg);

// 光标样式（per-window）
PointerStyle style;
style.id = 13;            // MOUSE_ICON::CROSS
style.size = 3;
style.color = 0xFF0000;   // red
InputManager::GetInstance()->SetPointerStyle(windowId, style);
InputManager::GetInstance()->GetPointerStyle(windowId, style);

// 全局光标大小/颜色
InputManager::GetInstance()->SetPointerSize(4);
InputManager::GetInstance()->SetPointerColor(0x00FF00);

// 捕获模式
InputManager::GetInstance()->EnterCaptureMode(windowId);
InputManager::GetInstance()->LeaveCaptureMode(windowId);
```

## 执行顺序

```
1. InitNativeToken()           — 权限 (见 ohos-dev-distributed-mmi-device-test-harness)
2. 建立 scenario model         — 用户、显示组、主/扩展/镜像屏、窗口栈、焦点
3. UpdateDisplayInfo()         — 注入 display group/screen 信息（等 1 秒）
4. UpdateWindowInfo() x N      — 每个 display 注入窗口栈（等 1 秒）
5. 创建虚拟设备 + FindDevice   — 见 ohos-dev-distributed-mmi-uinput-virtual-device
6. BindDeviceToDisplayGroupByDisplay()
7. warm-up 事件注入（2 次，初始化 group state）
8. 测试逻辑 + DumpPhase()     — dump 捕获见 ohos-dev-distributed-mmi-device-test-harness
9. 清理：解绑 → UI_DEV_DESTROY → close(fd)
```

## 已知限制

| 限制 | 原因 | 规避方案 |
|------|------|---------|
| 光标定位不精确 | libinput 鼠标加速导致 uinput 相对移动无法精确到绝对坐标 | 使用全屏窗口避免依赖光标位置 |
| `focusWindowId=-1` 在 DisplayGroups dump 中 | dump 读 `displayGroupInfoMap_`，MAIN_GROUPID 的焦点从 `UpdateWindowInfo` 传入 | 通过 `KeyboardStateByGroup` 或 `SequenceSnapshots` 验证实际焦点 |
| 非主组焦点切换 | `UpdateWindowInfo` 忽略非主组 focusWindowId | 必须通过 `UpdateDisplayInfo` 更新 |
| DEL 全屏后命中非预期窗口 | 剩余窗口中 zOrder 最高的命中，包括原有非全屏窗口 | 注意已有窗口的 zOrder 关系 |

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| 不设 `focusWindowId` | 键盘事件不分发到任何窗口 | 在 DisplayGroupInfo 中预设 |
| `groupId != 0` 的组用 `GROUP_DEFAULT` | `InitDisplayGroupInfo` 拒绝 | 非 0 组用 `GROUP_SPECIAL` |
| 窗口的 `groupId` 与显示组不匹配 | 事件路由到错误的组 | 确保一致 |
| 多屏/多组复用 displayId 或 windowId | dump 和路由证据不可审计 | 全局唯一编号 |
| 镜像屏比例不同但沿用主屏坐标 | 命中断言错误 | 先定义 fit/stretch/crop 映射策略 |
| 声称每屏独立键盘焦点但只设置 group focus | 结论不成立 | 区分 group 级键盘焦点和每屏窗口命中目标 |
| 非主组通过 UpdateWindowInfo 切焦点 | focusWindowId 被忽略 | 必须通过 UpdateDisplayInfo 切焦点 |
| 所有窗口用相同 zOrder | 命中顺序不确定 | 按业务层级分配不同 zOrder |
| 忘记注入窗口 | 鼠标事件无 hit test 目标 | 每组至少一个全屏窗口 |
| UpdateDisplayInfo 返回 -201 就认为失败 | 实际数据已写入 | -201 来自 UIExtension，可忽略 |
| InjectVirtualWindows 硬编码 focusWindowId | 动态焦点切换后被覆盖 | 使用全局变量同步焦点 |
| DEL 全屏窗口后假设次高全屏命中 | 原有非全屏窗口可能 zOrder 更高 | 检查所有窗口的 zOrder 关系 |
