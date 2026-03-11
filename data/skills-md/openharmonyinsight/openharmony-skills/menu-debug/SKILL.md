---
name: menu-debug
description: This skill should be used when user asks to "Menu宽度为0", "Menu宽度问题", "Menu显示异常", "Menu子窗口问题", "Menu layout异常", "recreate subwindow", "快速打开Menu问题", "Menu闪退", "Menu位置错误", "子窗口recreate", "Menu崩溃", "Menu打印recreate", "点击无响应", "点击菜单关闭", "菜单位置左上角", "菜单方向不对", "菜单避让坑", "宽度高度为0", or mentions any Menu component issues like Menu width being 0, Menu display problems, Menu subwindow issues, Menu layout exceptions, positioning errors, crashes, click response issues, menu closing immediately, incorrect positioning, direction issues, safe area issues, or zero width/height problems. Provides systematic debugging guidance for Menu component issues including width problems, subwindow recreation, layout exceptions, positioning errors, crash analysis, click issues, menu positioning, and dimension problems with automatic log enhancement patch generation.
version: 0.2.0
---

# Menu Component Debugging Skill

Systematic debugging and problem diagnosis for Menu component issues in OpenHarmony ACE Engine. This skill provides structured troubleshooting guidance for Menu-related problems with automatic log enhancement patch generation.

## Overview

Menu component debugging requires analyzing multiple layers:
- **Subwindow lifecycle** - Window creation, recreation, and destruction
- **Menu layout algorithm** - Width calculation, positioning, and constraint handling
- **Menu pattern** - State management, menu wrapper, and menu items
- **Pipeline context** - Window rect info, theme settings, and display configuration
- **Event handling** - Click detection, state transitions, and gesture processing

**Critical Requirements**:
- ⚠️ **All log patches MUST be based on actual code analysis** - no speculation
- ⚠️ **Log patches MUST follow OpenHarmony logging standards** (TAG_LOGI/W/E macros)
- ⚠️ **Always provide context** - include relevant variable values in log statements
- ⚠️ **Use existing log tags** - ACE_MENU, ACE_SUB_WINDOW, ACE_OVERLAY

## Problem Categories

### 1. Menu Width Issues
**Symptoms**:
- Menu width displays as 0
- Menu appears too narrow or wide
- Menu width calculation errors

**Common Causes**:
- `displayWindowRectInfo.Width()` returns 0 (async initialization not complete)
- PipelineContext source issues (subwindow vs main window)
- Menu parameter configuration Errors
- Theme settings problems

### 2. Subwindow Recreation Issues
**Symptoms**:
- Frequent "recreate subwindow" logs
- Menu fails to show on rapid open
- Window state transitions (ATTACHING/DETACHING)
- Menu displays blank or delayed

**Common Causes**:
- Quick Menu opening (DETACHING state conflict)
- Display ID changes
- Menu wrapper state mismatches

### 3. Menu Layout Issues
**Symptoms**:
- Menu positioned incorrectly
- Menu overlaps with target
- Menu clipped or truncated
- Menu displays on wrong screen side

**Common Causes**:
- Window rect calculation errors
- Offset calculation problems
- Device type issues (foldable phones)
- Safe area not considered

### 4. Menu Crash/Instability
**Symptoms**:
- Menu crashes when opening
- Menu disappears unexpectedly
- Menu interaction failures

**Common Causes**:
- Null pointer dereferences
- Menu pattern lifecycle issues
- State management errors

### 5. Click Response Issues
**Symptoms**:
- Click on menu trigger has no response
- Menu fails to open when clicked
- Delayed response to menu interaction

**Common Causes**:
- Event hub not properly initialized
- Gesture event not registered
- Menu state prevents click handling

### 6. Menu Auto-Close Issues
**Symptoms**:
- Menu closes immediately after opening
- Menu disappears when clicked
- Menu closes without user interaction

**Common Causes**:
- State machine issues in menu wrapper
- Touch event handling conflicts
- HideMenu called incorrectly

### 7. Menu Positioning Issues
**Symptoms**:
- Menu positioned at screen top-left corner
- Menu appears at wrong screen position
- Menu placement calculation errors

**Common Causes**:
- Offset calculation problems
- Anchor point configuration errors
- MenuWindowRect calculation incorrect

### 8. Safe Area/Navigation Bar Issues
**Symptoms**:
- Menu overlaps with navigation bar
- Menu covers status bar
- Menu doesn't avoid system UI

**Common Causes**:
- Safe area insets not applied
- Window rect doesn't account for system UI
- Display cutout settings ignored

### 9. Menu Dimension Issues
**Symptoms**:
- Menu width is 0
- Menu height is 0
- Menu size calculations return 0

**Common Causes**:
- Async initialization timing
- Pipeline context not ready
- DisplayWindowRectInfo not properly initialized

## Debugging Workflow

### Step 1: Identify Problem Category

Based on symptoms, identify which problem category:

**Width/Dimension Issues** → Look for:
```
Menu width is 0
menuMaxWidth = 0
displayWindowRectInfo.Width() = 0
```

**Subwindow Issues** → Look for:
```
recreate subwindow
DETACHING state
MenuWindowRect
```

**Layout Issues** → Look for:
```
MenuOffset incorrect
position calculation error
menuWindowRect
```

**Crash Issues** → Look for:
```
Segmentation fault
Null pointer
CHECK_NULL_*
```

**Click/Auto-Close Issues** → Look for:
```
HideMenu called
state transition
gesture event not received
```

**Positioning Issues** → Look for:
```
anchorPoint calculation
MenuWindowRect values
offset errors
```

### Step 2: Locate Key Code Locations

**For Width/Dimension Issues**:
- `menu_layout_algorithm.cpp:941` - UpdateChildConstraintByDevice
- `menu_layout_algorithm.cpp:3618` - GetMenuWindowRectInfo
- `menu_layout_algorithm.cpp:931` - Pipeline context source
- `menu_pattern.cpp` - Menu wrapper initialization

**For Subwindow Issues**:
- `subwindow_manager.cpp:1954` - GetOrCreateMenuSubWindow
- `subwindow_manager.cpp:1965` - Recreate log
- `menu_wrapper_pattern.cpp` - Menu wrapper lifecycle

**For Layout Issues**:
- `menu_layout_algorithm.cpp:3611-3659` - GetMenuWindowRectInfo
- `menu_pattern.cpp` - Menu positioning
- `multi_menu_layout_algorithm.cpp` - Multi-menu layout

**For Click/Auto-Close Issues**:
- `menu_wrapper_pattern.cpp` - OnDetach/OnAttach
- `menu_pattern.cpp` - Menu state management
- `menu_view.cpp` - Event handling

**For Positioning Issues**:
- `menu_layout_algorithm.cpp` - GetMenuWindowRectInfo
- `menu_pattern.cpp` - Offset calculation
- `subwindow_manager.cpp` - Window rect calculation

### Step 3: Collect Existing Logs

**Key log tags to filter**:
```bash
# Menu-related logs
cat xxx.log | grep "ACE_MENU"
cat xxx.log | grep "ACE_SUB_WINDOW"
cat xxx.log | grep "ACE_OVERLAY"

# Specific issues
cat xxx.log | grep "recreate subwindow"
cat xxx.log | grep "DisplayWindowRectInfo"
cat xxx.log | grep "MenuWindowRect"
cat xxx.log | grep "HideMenu"
cat xxx.log | grep "OnClick"
```

**Critical log patterns**:
- `recreate subwindow` → Subwindow recreation occurred
- `DisplayWindowRectInfo width is 0` → Width initialization problem
- `DETACHING` → Window state transition
- `MenuWindowRect` → Window rect calculation
- `HideMenu` → Menu hide operation

## New Problem Analysis (v0.2.0)

### Problem 1: 点击无响应/点击弹不出来菜单 (Click No Response)

**Symptoms**:
- 点击菜单触发器没有反应
- 点击后菜单不弹出
- 没有任何错误日志
- 点击事件似乎被忽略

**Possible Causes**:
1. **事件中心未正确初始化**
   - GestureEventHub 没有获取或创建
   - Pan event 没有注册到菜单组件

2. **菜单状态不正确**
   - MenuWrapper 处于 DETACHING 状态
   - MenuPattern 的状态机阻止了新事件

3. **点击区域被遮挡**
   - 其他组件覆盖了菜单的点击区域
   - Window z-order 问题

4. **事件被消费**
   - 其他组件拦截了点击事件
   - Touch event 没有传递到菜单

**Debug Steps**:

1. **检查事件注册**
   ```bash
   # 查找菜单事件相关日志
   cat xxx.log | grep "OnClick"
   cat xxx.log | grep "GestureEventHub"
   ```

2. **检查菜单状态**
   ```bash
   # 查找菜单状态
   cat xxx.log | grep "MenuWrapper"
   cat xxx.log | grep "MenuState"
   ```

3. **检查 window 状态**
   ```bash
   # 查找子窗口状态
   cat xxx.log | grep "ACE_SUB_WINDOW"
   cat xxx.log | grep "MenuWindowRect"
   ```

**Code Locations**:
- `menu_wrapper_pattern.cpp:OnDetach()` - 状态转换
- `menu_pattern.cpp:OnClick` - 点击处理
- `menu_view.cpp:Create()` - 菜单创建流程

**Solutions**:
1. **确保事件正确注册**
   - 检查 GestureEventHub 初始化
   - 验证 Pan event 注册
   - 确认 event hub 传递正确

2. **检查菜单状态机**
   - 验证 OnModifyDone 时机
   - 确保 Menu 不在阻止状态
   - 检查 isShowing_ 状态

3. **验证点击区域**
   - 检查是否有组件遮挡
   - 验证 hitTestStack 配置
   - 确认触摸事件传递

4. **添加调试日志**
   ```cpp
   // 在点击处理中添加日志
   TAG_LOGI(AceLogTag::ACE_MENU, "OnClick called: menuId=%{public}d", menuId);
   ```

---

### Problem 2: 点击菜单立马就关闭了 (Menu Closes Immediately)

**Symptoms**:
- 菜单打开后立即关闭
- 点击菜单后菜单消失
- 菜单闪现后消失
- 看到 "HideMenu" 日志紧接着 "ShowMenu"

**Possible Causes**:
1. **状态机错误**
   - MenuWrapper 状态在 ATTACHING 和 DETACHED 间快速切换
   - OnDetach 被意外调用
   - 状态转换逻辑有缺陷

2. **触摸事件冲突**
   - 点击事件触发两次
   - Hide 和 Show 事件冲突
   - Touch down 和 touch up 事件处理错误

3. **Window 焦点问题**
   - Window 失去焦点导致菜单关闭
   - Focus change event 触发隐藏

4. **超时配置错误**
   - Menu 超时时间设置为 0
   - Duration 太短导致立即关闭

**Debug Steps**:

1. **检查状态转换日志**
   ```bash
   # 查找快速的状态变化
   cat xxx.log | grep -E "ATTACHING|DETACHING" | head -20
   ```

2. **检查 HideMenu 调用**
   ```bash
   # 查找谁调用了 HideMenu
   cat xxx.log | grep "HideMenu" | grep -B 5 "ShowMenu"
   ```

3. **检查触摸事件**
   ```bash
   # 查找触摸事件
   cat xxx.log | grep "Touch"
   cat xxx.log | grep "Click"
   ```

4. **检查窗口生命周期**
   ```bash
   # 查找子窗口创建和销毁
   cat xxx.log | grep "GetOrCreateMenuSubWindow"
   cat xxx.log | grep "RemoveMenuSubWindow"
   ```

**Code Locations**:
- `menu_wrapper_pattern.cpp:OnDetach()` - 状态管理
- `menu_wrapper_pattern.cpp:HideMenu()` - 隐藏逻辑
- `menu_pattern.cpp` - 状态机实现

**Solutions**:
1. **修复状态转换逻辑**
   - 添加状态转换日志
   - 添加转换条件检查
   - 防止非法状态转换

2. **优化事件处理**
   - 添加事件去重逻辑
   - 防止 Show/Hide 冲突
   - 添加事件处理延迟

3. **检查焦点管理**
   - 验证窗口焦点设置
   - 确认 focus 事件处理
   - 添加焦点状态日志

4. **增加状态保护**
   ```cpp
   // 添加状态检查
   if (menuWrapperPattern->GetState() != MenuWrapperState::DETACHING) {
       TAG_LOGW(AceLogTag::ACE_MENU,
           "Invalid HideMenu call, current state=%{public}d",
           static_cast<int>(state));
       return;
   }
   ```

---

### Problem 3: 弹出菜单位置在屏幕左上角 (Menu Positioned at Top-Left)

**Symptoms**:
- 菜单位置在屏幕左上角 (0,0)
- 菜单位置明显错误
- 菜单没有跟随触发器
- offset 计算错误

**Possible Causes**:
1. **Offset 计算错误**
   - targetOffset 计算为 0
   - PositionOffset 未正确设置
   - 初始位置使用默认值

2. **锚点配置错误**
   - anchorPoint 未设置
   - anchorPosition 使用默认值
   - 菜单锚到错误位置

3. **MenuWindowRect 计算错误**
   - GetMenuWindowRectInfo 返回错误值
   - displayWindowRect 信息错误
   - 子窗口尺寸计算失败

4. **Placement 配置未生效**
   - UpdateMenuPlacement 没有被调用
   - placement 属性被忽略
   - AlignRule 配置错误

**Debug Steps**:

1. **检查位置相关日志**
   ```bash
   # 查找菜单位置计算
   cat xxx.log | grep "MenuOffset"
   cat xxx.log | grep "MenuPosition"
   cat xxx.log | grep "targetOffset"
   ```

2. **检查窗口 Rect 信息**
   ```bash
   # 查找窗口矩形
   cat xxx.log | grep "MenuWindowRect"
   cat xxx.log | grep "DisplayWindowRectInfo"
   ```

3. **检查 placement 配置**
   ```bash
   # 查找 placement 配置
   cat xxx.log | grep "placement"
   cat xxx.log | grep "anchor"
   ```

**Code Locations**:
- `menu_layout_algorithm.cpp:3611-3659` - GetMenuWindowRectInfo
- `menu_layout_algorithm.cpp` - Offset 计算
- `menu_pattern.cpp` - PositionOffset 更新
- `menu_view.cpp:1627` - UpdateMenuPlacement

**Solutions**:
1. **验证 Offset 计算**
   - 检查 targetOffset 是否正确
   - 验证 positionOffset 来源
   - 添加 offset 计算日志

2. **检查锚点配置**
   - 验证 anchorPoint 设置
   - 检查 anchorPosition 属性
   - 确认锚点计算逻辑

3. **验证 Placement**
   - 确保 UpdateMenuPlacement 被调用
   - 检查 AlignRule 配置
   - 验证 placement 类型

4. **添加位置调试日志**
   ```cpp
   // 添加位置日志
   TAG_LOGI(AceLogTag::ACE_MENU,
       "Menu position: offset=(%{public}f,%{public}f), target=(%{public}f,%{public}f)",
       offsetX, offsetY, targetOffsetX, targetOffsetY);
   ```

---

### Problem 4: 菜单弹出方向不对 (Menu Direction Incorrect)

**Symptoms**:
- 菜单方向错误（应上弹却下弹）
- 菜单与触发器方向不匹配
- 子菜单展开方向错误
- 菜单在错误侧弹出

**Possible Causes**:
1. **Direction 参数错误**
   - fontSize 或 direction 参数配置错误
   - menuDirection 枚举值不正确
   - 箭头绘制方向错误

2. **Placement 计算错误**
   - placement 类型判断错误
   - Top/Bottom/Left/Right 混淆
   - AlignRule 应用不正确

3. **Target 位置计算错误**
   - 触发器位置获取错误
   - TargetOffset 使用错误值
   - 相对位置计算符号错误

4. **布局算法方向错误**
   - Column/Row 方向设置错误
   - crossAxis 配置错误
   - mainAxisSize 设置错误

**Debug Steps**:

1. **检查方向相关配置**
   ```bash
   # 查找方向配置
   cat xxx.log | grep -E "direction|font|arrow"
   ```

2. **检查 placement 配置**
   ```bash
   cat xxx.log | grep "placement"
   cat xxx.log | grep "AlignDirection"
   ```

3. **检查布局方向**
   ```bash
   cat xxx.log | grep "mainAxisSize"
   cat xxx.log | grep "crossAxis"
   ```

**Code Locations**:
- `menu_pattern.cpp` - Direction 配置
- `menu_layout_algorithm.cpp` - Placement 计算
- `menu_item/` - 菜单项布局

**Solutions**:
1. **验证 Direction 参数**
   - 检查 fontSize API 调用
   - 验证方向枚举值
   - 检查箭头绘制逻辑

2. **修正 Placement 计算**
   - 确保 placement 类型正确
   - 检查 Top/Bottom 判断逻辑
   - 验证对齐规则

3. **检查目标位置**
   - 验证 trigger 组件位置
   - 检查 targetOffset 计算
   - 确认相对位置方向

4. **添加方向调试日志**
   ```cpp
   TAG_LOGI(AceLogTag::ACE_MENU,
       "Menu direction: placement=%{public}d, direction=%{public}d",
       placement, direction);
   ```

---

### Problem 5: 菜单没有避让挖坑/导航条 (Menu Overlaps System UI)

**Symptoms**:
- 菜单被导航栏遮挡
- 菜单覆盖状态栏
- 菜单没有考虑系统 UI 安全区域
- 菜单部分在屏幕外

**Possible Causes**:
1. **SafeArea 未应用**
   - GetSafeArea() 没有被调用
   - SafeArea insets 没有传递到布局
   - system_safe_area 属性未设置

2. **Window Rect 计算错误**
   - displayWindowRect 没有考虑 safe area
   - Window 位置和尺寸计算错误
   - Cutout state 未应用

3. **Z-Order 问题**
   - 菜单 window 层级错误
   - Window type 不是 PANEL 类型
   - Z-order 配置不正确

4. **Maximize 设置错误**
   - LayoutFullScreen 使用错误
   - Window mode 设置为 FULLSCREEN 而非 FLOATING
   - 布局约束配置错误

**Debug Steps**:

1. **检查 SafeArea 相关日志**
   ```bash
   cat xxx.log | grep -i "safe|safeArea"
   ```

2. **检查 Window Mode**
   ```bash
   cat xxx.log | grep "LayoutFullScreen"
   cat xxx.log | grep "WindowMode"
   ```

3. **检查 Window Rect**
   ```bash
   cat xxx.log | grep "DisplayWindowRectInfo"
   ```

**Code Locations**:
- `subwindow_manager.cpp` - Window 创建
- `menu_layout_algorithm.cpp` - SafeArea 应用
- Menu wrapper - Window 模式设置

**Solutions**:
1. **应用 SafeArea 约束**
   - 确保 GetSafeArea() 被调用
   - 将 safe area 传递给布局算法
   - 设置 system_safe_area 属性

2. **调整 Window Mode**
   - 使用 FLOATING 或 PANEL 类型
   - 避免 FULLSCREEN 模式
   - 设置合适的窗口属性

3. **修正 Window Rect 计算**
   - 在窗口 rect 中减去 safe area
   - 确保菜单在可见区域内
   - 验证 cutout 处理

4. **验证 Z-Order**
   - 检查 window type 配置
   - 确保菜单在正确层级
   - 验证与系统 UI 的关系

---

### Problem 6: 菜单弹出宽度为0/高度为0 (Menu Width/Height is 0)

**Symptoms**:
- 菜单宽度计算为 0
- 菜单高度计算为 0
- Menu 显示异常窄或不显示
- displayWindowRectInfo 返回 0 值

**Possible Causes**:
1. **异步初始化未完成**
   - GetDisplayWindowRectInfo 在 pipeline ready 前调用
   - displayWindowRect 还未初始化
   - 异步获取 display 信息时机错误

2. **Pipeline Context 来源错误**
   - 使用了 subwindow 的 context 而非 main window
   - Context 类型判断错误
   - PipelineContext 初始化时机问题

3. **MenuParam 配置错误**
   - fontSize 参数未解析
   - MenuParam 传递错误
   - 属性值未正确设置

4. **计算公式错误**
   - menuMaxWidthRatio 计算为 0
   - displayWidth 乘以错误系数
   - theme 返回值使用错误

**Debug Steps**:

1. **检查 displayWidth 相关日志**
   ```bash
   # 查找宽度计算
   cat xxx.log | grep "displayWidth"
   cat xxx.log | grep "displayWindowRect.Width"
   cat xxx.log | grep "menuMaxWidthRatio"
   ```

2. **检查 MenuParam**
   ```bash
   cat xxx.log | grep "MenuParam"
   cat xxx.log | grep "fontSize"
   ```

3. **检查 Pipeline Context**
   ```bash
   cat xxx.log | grep "PipelineContext"
   cat xxx.log | grep "GetMainPipelineContext"
   ```

**Code Locations**:
- `menu_layout_algorithm.cpp:920-966` - UpdateChildConstraintByDevice
- `menu_layout_algorithm.cpp:3618` - GetMenuWindowRectInfo
- `menu_pattern.cpp` - MenuParam 处理
- Theme 相关 - menuMaxWidthRatio 配置

**Solutions**:
1. **添加初始化检查**
   ```cpp
   // 在 GetMenuWindowRectInfo 中添加检查
   auto displayWidth = displayWindowRectInfo.Width();
   if (displayWidth <= 0.0f) {
       TAG_LOGE(AceLogTag::ACE_MENU,
           "Invalid displayWidth=%{public}f, waiting for async init",
           displayWidth);
       return menuWindowRect;
   }
   ```

2. **验证 Context 来源**
   - 检查是否应该使用 main window context
   - 验证 PipelineContext 类型
   - 添加 context 来源日志

3. **延迟宽度计算**
   - 在异步初始化完成前使用默认宽度
   - 添加 ready 状态检查
   - 防止使用未初始化的值

4. **添加异步初始化日志**
   ```cpp
   TAG_LOGI(AceLogTag::ACE_MENU,
       "Async display init: displayWidth=%{public}f, ready=%{public}d",
       displayWidth, IsDisplayReady());
   ```

---

## Log Enhancement Reference

### Key Logging Patterns

**1. State Transition Logging**
```cpp
TAG_LOGI(AceLogTag::ACE_SUB_WINDOW,
    "Subwindow state transition: %{public}d -> %{public}d",
    static_cast<int>(oldState), static_cast<int>(newState));
```

**2. Value Context Logging**
```cpp
TAG_LOGI(AceLogTag::ACE_MENU,
    "Calculation: displayWidth=%{public}f, menuMaxWidthRatio=%{public}f, result=%{public}f",
    displayWidth, menuMaxWidthRatio, menuMaxWidth);
```

**3. Code Path Logging**
```cpp
TAG_LOGI(AceLogTag::ACE_MENU,
    "GetMenuWindowRectInfo: host=%{public}p, menuId=%{public}d, targetTag=%{public}d, targetNodeId=%{public}d",
    host.Get(), menuPattern->GetMenuId(), targetTag_, targetNodeId_);
```

**4. Error Context Logging**
```cpp
if (displayWidth <= 0.0f) {
    TAG_LOGE(AceLogTag::ACE_MENU,
        "Invalid displayWidth=%{public}f, expected>%{public}f",
        displayWidth, expectedWidth);
    return;
}
```

### Critical Variables to Log

**For Width/Height Issues**:
- `displayWindowRectInfo.Width()` / `Height()`
- `menuMaxWidth` / `menuMaxHeight`
- `menuMaxWidthRatio` / `menuMaxHeightRatio`
- `theme->GetMenuMaxWidthRatio()`
- `pipeline->GetDisplayWindowRectInfo()`

**For Subwindow Issues**:
- `subwindow->GetDetachState()`
- `subwindow->GetShown()`
- `subwindow->GetRect().GetSize()`
- `instanceId` / `searchKey.ToString()`

**For Layout Issues**:
- `menuWindowRect` (all fields)
- `targetOffset_` / `targetSize_`
- `GetMenuWindowRectInfo()` return value
- `placement` / `anchorPosition`

## Quick Reference Code Locations

| Problem Type | File | Line(s) | Function | Key Variables |
|-------------|------|----------|----------|---------------|
| Click issues | `menu_wrapper_pattern.cpp` | - | `OnDetach` / `OnAttach` | `state_` |
| Auto-close | `menu_pattern.cpp` | - | State machine | `isShowing_` |
| Position (top-left) | `menu_layout_algorithm.cpp` | 3611-3659 | `GetMenuWindowRectInfo` | `menuWindowRect` |
| Direction | `menu_pattern.cpp` | - | `direction_` / `placement` | - |
| Safe area | `subwindow_manager.cpp` | - | Window creation params | - |
| Width=0/Height=0 | `menu_layout_algorithm.cpp` | 920-966 | `UpdateChildConstraintByDevice` | `displayWidth` |

## Log Filtering Commands

**Extract all Menu-related logs**:
```bash
# Comprehensive Menu logs
grep -E "ACE_MENU|ACE_SUB_WINDOW|ACE_OVERLAY" xxx.log > menu_debug.log

# Width-specific logs
grep -E "DisplayWindowRectInfo|menuMaxWidth|displayWidth" xxx.log

# Subwindow recreation logs
grep -E "recreate subwindow|DETACHING|MenuWindowState" xxx.log

# Positioning logs
grep -E "MenuOffset|MenuPosition|targetOffset|placement" xxx.log

# Click/Event logs
grep -E "OnClick|TouchEvent|GestureEvent" xxx.log
```

**Filter by specific instance**:
```bash
# For specific container ID
grep "instanceId: 123" xxx.log

# For specific menu node
grep "menuId: 456" xxx.log
```

## Best Practices

### Log Enhancement Principles

**DO**:
- ✅ Add context - log relevant variable values
- ✅ Log state transitions - old → new
- ✅ Use appropriate log level - INFO for normal, WARN for unexpected, ERROR for failures
- ✅ Include identifiers - node IDs, instance IDs
- ✅ Log calculations - input values and results
- ✅ Minimal changes - Only add logging, don't modify logic
- ✅ Use existing macros - TAG_LOGI/W/E with correct tags
- ✅ Test compilation - Verify syntax before applying
- ✅ Document changes - Note what and why for each log

**DON'T**:
- ❌ Log without context - just "entered function"
- ❌ Over-log - excessive logging in loops
- ❌ Log sensitive data - user information, tokens
- ❌ Speculate - log actual values only
- ❌ Modify logic - Only add logging statements

### Patch Generation Guidelines

1. **Minimal Changes** - Only add logging, don't modify logic
2. **Preserve Formatting** - Follow existing code style
3. **Use Existing Macros** - TAG_LOGI/W/E with correct tags
4. **Test Compilation** - Verify syntax before applying
5. **Document Changes** - Note what and why for each log
6. **Contextual Logging** - Include surrounding code state in logs

### Analysis Workflow

1. **Gather baseline** - Collect logs without issue if possible
2. **Apply patch** - Add targeted logging
3. **Reproduce issue** - Trigger problem with enhanced logging
4. **Extract relevant logs** - Filter specific log tags
5. **Trace execution flow** - Follow log sequence through code
6. **Identify root cause** - Find where unexpected behavior occurs
7. **Implement fix** - Address identified issue
8. **Verify resolution** - Confirm fix works, remove debug logs if needed

## Integration with Other Skills

This skill complements:
- **compile-analysis** - For performance issues in Menu code
- **build-error-analyzer** - If Menu changes cause build failures
- **xts-component-test** - For writing Menu test cases

## Version History

- **0.2.0** (2026-02-12): 新增6个常见问题分析
  - 💫 添加点击无响应问题分析
  - 💫 添加菜单自动关闭问题分析
  - 💫 添加菜单位置左上角问题分析
  - 💫 添加菜单方向不对问题分析
  - 💫 添加菜单避让导航条问题分析
  - 💫 添加宽度/高度为0问题分析
  - 📝 为每个问题提供详细调试步骤和解决方案
  - 🎯 扩展触发关键词覆盖常见用户问题

- **0.1.0** (2026-02-12): 初始版本
  - ✨ 完整的 Menu 组件调试 skill
  - 📝 覆盖宽度、子窗口、布局、崩溃等4大类问题
  - 🔧 提供系统化调试工作流程
  - 📊 包含关键代码位置和变量参考
  - 🎯 自动化日志增强补丁生成
