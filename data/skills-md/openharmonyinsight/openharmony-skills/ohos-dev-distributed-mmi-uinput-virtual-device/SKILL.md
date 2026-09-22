---
name: ohos-dev-distributed-mmi-uinput-virtual-device
description: Use when testing OpenHarmony input subsystem features (mouse/keyboard/touchpad event flow, device binding, display group isolation) on a real device without physical peripherals. Covers /dev/uinput device creation, event injection, InputManager device discovery, and hot-plug simulation.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: uinput-virtual-device
  version: 0.2.0
  status: draft
  tags:
    - multimodalinput
    - uinput
    - virtual-device
    - event-injection
    - hot-plug
  related-skills:
    - ohos-dev-distributed-mmi-device-test-harness
    - ohos-dev-distributed-mmi-wms-dms-simulation
---

# uinput 虚拟设备测试

通过 `/dev/uinput` 创建虚拟 HID 设备，注入精确事件序列，验证输入子系统行为。

## When to Use

- 验证输入事件流（鼠标移动、按键、触控板）在真机上的行为
- 测试设备绑定（BindDeviceToDisplayGroupByDisplay）和状态隔离
- 模拟热拔插场景
- 不需要或没有物理外设时

## 设备创建

### 关键约束

- **bustype 必须用 `BUS_USB`**（0x03）。`BUS_VIRTUAL` 会被 MMI 过滤，不触发设备发现回调
- **vendor/product 需唯一**，避免与真实设备冲突。推荐 vendor=0x93a，product 自定义
- 鼠标必须同时注册 `EV_KEY`+`EV_REL`，否则不被识别为 pointer 设备

### 鼠标

```cpp
int fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
ioctl(fd, UI_SET_EVBIT, EV_KEY);
ioctl(fd, UI_SET_EVBIT, EV_REL);
ioctl(fd, UI_SET_KEYBIT, BTN_LEFT);
ioctl(fd, UI_SET_KEYBIT, BTN_RIGHT);   // 可选
ioctl(fd, UI_SET_KEYBIT, BTN_MIDDLE);  // 可选
ioctl(fd, UI_SET_RELBIT, REL_X);
ioctl(fd, UI_SET_RELBIT, REL_Y);
ioctl(fd, UI_SET_RELBIT, REL_WHEEL);   // 可选

struct uinput_user_dev ud = {};
strncpy(ud.name, "TestMouseA", UINPUT_MAX_NAME_SIZE - 1);
ud.id.bustype = BUS_USB;  // 必须
ud.id.vendor  = 0x93a;
ud.id.product = 0xAA01;   // 每个虚拟设备用不同值
ud.id.version = 1;
write(fd, &ud, sizeof(ud));
ioctl(fd, UI_DEV_CREATE);
```

### 键盘

```cpp
int fd = open("/dev/uinput", O_WRONLY | O_NONBLOCK);
ioctl(fd, UI_SET_EVBIT, EV_KEY);
// 不注册 EV_REL —— 确保被识别为键盘而非鼠标
for (int k = KEY_ESC; k <= KEY_RIGHTMETA; k++) {
    ioctl(fd, UI_SET_KEYBIT, k);
}
// ... 同上构造 uinput_user_dev, bustype=BUS_USB
```

## 事件注入

每个事件序列必须以 `SYN_REPORT` 结尾：

```cpp
// 鼠标相对移动
void InjectMotion(int fd, int dx, int dy) {
    struct input_event ev = {};
    ev.type = EV_REL; ev.code = REL_X; ev.value = dx;
    write(fd, &ev, sizeof(ev));
    ev.code = REL_Y; ev.value = dy;
    write(fd, &ev, sizeof(ev));
    ev.type = EV_SYN; ev.code = SYN_REPORT; ev.value = 0;
    write(fd, &ev, sizeof(ev));
}

// 按键/按钮（鼠标按钮和键盘按键共用）
void InjectKey(int fd, int code, int pressed) {
    struct input_event ev = {};
    ev.type = EV_KEY; ev.code = code; ev.value = pressed;
    write(fd, &ev, sizeof(ev));
    ev.type = EV_SYN; ev.code = SYN_REPORT; ev.value = 0;
    write(fd, &ev, sizeof(ev));
}

// code: BTN_LEFT, BTN_RIGHT (鼠标按钮)
//       KEY_A, KEY_LEFTCTRL, KEY_LEFTSHIFT (键盘按键)
// pressed: 1=按下, 0=释放
```

## InputManager 设备发现

`GetDeviceIds` / `GetDevice` 是异步回调。创建 uinput 设备后需要等待 MMI 枚举：

```cpp
static int FindDevice(const std::string &name) {
    struct FindState {
        std::mutex mtx;
        std::condition_variable cv;
        int foundId = -1;
        int pending = 0;
        bool done = false;
    };
    for (int attempt = 0; attempt < 30; ++attempt) {
        auto state = std::make_shared<FindState>();
        InputManager::GetInstance()->GetDeviceIds([state, name](std::vector<int32_t> &ids) {
            {
                std::lock_guard<std::mutex> lock(state->mtx);
                state->pending = static_cast<int>(ids.size());
                if (state->pending == 0) {
                    state->done = true;
                    state->cv.notify_one();
                    return;
                }
            }
            for (auto id : ids) {
                InputManager::GetInstance()->GetDevice(id,
                    [state, id, name](std::shared_ptr<InputDevice> dev) {
                        bool notify = false;
                        {
                            std::lock_guard<std::mutex> lock(state->mtx);
                            if (dev && dev->GetName() == name && state->foundId < 0) {
                                state->foundId = id;
                            }
                            if (--state->pending == 0) {
                                state->done = true;
                                notify = true;
                            }
                        }
                        if (notify) {
                            state->cv.notify_one();
                        }
                    });
            }
        });
        std::unique_lock<std::mutex> lock(state->mtx);
        state->cv.wait_for(lock, std::chrono::milliseconds(500), [&]{ return state->done; });
        if (state->foundId >= 0) return state->foundId;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
    return -1;
}
```

**创建后至少等 3 秒**再调 `FindDevice`，给 libinput 和 MMI 枚举的时间。

## 热拔插模拟

```cpp
ioctl(fd, UI_DEV_DESTROY);
close(fd);
// MMI 的 OnInputDeviceRemoved 会自动清理绑定
// 等 2 秒后 dump 验证 RuntimeBindings 已清理
```

## 状态隔离验证模式

测试 per-group 隔离时的标准模式：

```
1. 创建 2 个虚拟设备，绑定到不同 group
2. warm-up：每个设备注入 2-3 个事件触发懒初始化
3. 对设备 A 注入值 X（如 +20,+10 移动），对设备 B 注入值 Y（如 -15,-8）
4. dump → 验证 group0 反映 X，group1 反映 Y，互不影响
```

**warm-up 必要性**：绑定后首次事件触发 `EnsureGroupState` 和 `cursorPosMap_` 初始化。跳过 warm-up 会导致 dump 中 group 状态为空。

## Phase-marker + hidumper 状态快照

测试代码写 marker，后台脚本捕获 hidumper：

```cpp
// 测试代码中
static void DumpPhase(const char *label) {
    FILE *f = fopen("/data/local/tmp/phase.txt", "w");
    if (f) { fprintf(f, "%s\n", label); fclose(f); }
    std::this_thread::sleep_for(std::chrono::seconds(3));
}
```

```bash
#!/system/bin/sh
# run_with_dump.sh — 后台捕获 hidumper
DUMP=/data/local/tmp/dump.txt
PHASE=/data/local/tmp/phase.txt
rm -f "$DUMP" "$PHASE"
$TEST_BIN &
PID=$!
LAST=""
while kill -0 $PID 2>/dev/null; do
    if [ -f "$PHASE" ]; then
        CUR=$(cat "$PHASE" 2>/dev/null)
        if [ "$CUR" != "$LAST" ] && [ -n "$CUR" ]; then
            echo "===== DUMP: $CUR =====" >> "$DUMP"
            hidumper -s MultimodalInput -a '-G' >> "$DUMP" 2>&1
            LAST="$CUR"
        fi
    fi
    sleep 1
done
wait $PID 2>/dev/null
```

## 清理

```cpp
// 必须在测试退出前销毁所有虚拟设备
ioctl(fd, UI_DEV_DESTROY);
close(fd);
```

不销毁的虚拟设备会在进程退出时自动清理，但 MMI 的设备移除通知可能延迟。

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| `bustype = BUS_VIRTUAL` | 设备不被 MMI 识别 | 用 `BUS_USB` |
| 缺少 `SYN_REPORT` | 事件不被处理 | 每个事件序列末尾加 SYN_REPORT |
| 创建后立即 FindDevice | 找不到设备 | 等 3 秒 |
| 跳过 warm-up 事件 | per-group 状态未初始化 | 绑定后注入 2-3 个移动事件 |
| 鼠标不注册 `EV_REL` | 不被识别为 pointer 设备 | 同时注册 EV_KEY + EV_REL |
| 多个设备用同一 product ID | 可能混淆设备发现 | 每个设备用不同 product |
