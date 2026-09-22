---
name: ohos-dev-distributed-mmi-device-test-harness
description: Use when building or running multimodal input system tests on a real DAYU200 device. Covers NativeToken permission setup, server-side bypass, test binary compile/deploy/run pipeline, phase-based hidumper capture, device discovery polling, and dump field reference.
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: mmi
  capability: device-test-harness
  version: 0.2.0
  status: draft
  tags:
    - multimodalinput
    - device-testing
    - hidumper
    - nativetoken
  related-skills:
    - ohos-dev-distributed-mmi-wms-dms-simulation
    - ohos-dev-distributed-mmi-uinput-virtual-device
---

# 多模输入真机测试脚手架

在 DAYU200 (RK3568) 真机上运行多模输入子系统测试二进制的完整基础设施。

## When to Use

- 新建多模输入系统测试二进制时，需要权限获取、编译部署、dump 捕获等基础能力
- 已有测试需要在真机上运行和验证
- 需要理解 hidumper dump 输出的含义

## 设备连接拓扑

优先按实际连接方式选择命令形态，不要默认所有环境都有 Windows 跳板机。

### 直连设备

本机能直接访问 USB 设备时，只需要参数化设备序列号：

```bash
export DEVICE="<device_serial>"
export HDC="hdc -t $DEVICE"
```

### Windows 跳板机

设备接在 Windows 测试机、当前环境只能通过 SSH 访问时，再使用跳板机变量。所有命令必须参数化，避免硬编码凭据：

```bash
# 设置一次，全 session 复用（根据实际环境替换占位符；不要提交真实值）
export DEVICE="<device_serial>"                    # hdc 设备序列号
export WIN_SSH="ssh <ssh_options> -p <port> <user>@<host>"
export WIN_SCP="scp <scp_options> -P <port>"
export WIN_SCP_DST="<user>@<host>:Desktop"         # SCP 目标（跳板机桌面）
export WIN_HOME='C:\Users\<user>'                  # Windows 用户主目录
export HDC="hdc -t $DEVICE"
```

后续文档中的 `$WIN_SSH`、`$WIN_SCP`、`$WIN_SCP_DST`、`$WIN_HOME`、`$HDC` 均引用这些变量。直连场景下去掉 `$WIN_SSH` 包装，直接运行 `$HDC ...`。
SSH 认证方式由环境决定，可使用 SSH key、CI secret 或其他跳板机机制。Skill 输出和 eval 结果中不得包含真实密码、主机名、用户名或设备 serial。

## 设备状态修改安全门槛

以下操作会改变真机系统状态，执行前必须先取得用户明确授权：

- server bypass 代码改动对应的 `.so` 部署
- `mount -o rw,remount /`
- 替换 `/system/lib/*.so`
- `kill $(pidof multimodalinput)` 或其他服务重启命令
- `setenforce 0` / `setenforce 1`
- 设备重启、系统分区写入或清理备份文件

授权前先向用户列出：

- 要修改的设备和目标进程
- 要备份、替换、还原的文件路径
- 备份保存位置和校验方式
- 预期还原状态
- 最终验证命令

报告中必须记录备份结果、替换结果、还原结果和最终验证结果。没有授权时，只能生成命令计划和检查清单，不得直接执行会改设备状态的命令。

## 权限获取

测试进程调用 InputManager IPC 需要系统权限：

```cpp
#include "accesstoken_kit.h"
#include "nativetoken_kit.h"
#include "token_setproc.h"

static void InitNativeToken() {
    const char *perms[] = {
        "ohos.permission.INPUT_DEVICE_CONFIGURATOR",
        "ohos.permission.INPUT_MONITORING",
    };
    NativeTokenInfoParams info = {
        .dcapsNum = 0,
        .permsNum = sizeof(perms) / sizeof(perms[0]),
        .aclsNum = 0,
        .dcaps = nullptr,
        .perms = perms,
        .acls = nullptr,
        .processName = "YourTestName",
        .aplStr = "system_basic",
    };
    uint64_t tokenId = GetAccessTokenId(&info);
    SetSelfTokenID(tokenId);
    OHOS::Security::AccessToken::AccessTokenKit::ReloadNativeTokenInfo();
}
```

**必须在 main() 最开始、其他 InputManager 调用之前执行。**

权限列表按测试需要调整：
- `INPUT_DEVICE_CONFIGURATOR` — 设备绑定/解绑
- `INPUT_MONITORING` — 事件监听

## Server 端绕过

测试进程不是 WMS/DMS 进程，server 端会校验调用方 token 类型。只有本地验证确实无法通过 NativeToken/权限配置完成时，才允许临时 server-side bypass。

这些绕过只允许用于本地开发验证。提交产品代码、PR 或测试报告前必须还原，且不得把绕过作为正式测试能力描述。

**收窄原则**：

- 首选 test-only 编译宏、测试进程名白名单或本地 patch 名称限制，不要提交“允许所有 token 类型”的通用绕过。
- patch 中必须标记 `[TEST BYPASS]`、目标测试名和还原方式。
- 测试报告只能说明“本地验证使用临时 bypass”，不能把绕过当作产品行为或长期测试能力。
- 如果必须短暂放开 token 检查，报告中要明确这是最宽松 fallback，并记录还原验证。

### 1. OnDisplayInfo — 允许测试进程调 UpdateDisplayInfo

**文件**: `service/message_handle/src/server_msg_handler.cpp`

```cpp
int32_t ServerMsgHandler::OnDisplayInfo(SessionPtr sess, NetPacket &pkt) {
    // [TEST BYPASS] prefer a test-only macro or process whitelist.
    // Avoid broad "allow all token types" changes except as a last-resort local fallback.
}
```

### 2. OnWindowGroupInfo — 允许测试进程调 UpdateWindowInfo

**文件**: `service/message_handle/src/server_msg_handler.cpp`

```cpp
int32_t ServerMsgHandler::OnWindowGroupInfo(SessionPtr sess, NetPacket &pkt) {
    // [TEST BYPASS] same narrow local-only rule as OnDisplayInfo.
}
```

### 3. CheckBindDevicePermission — 允许测试进程绑定设备

**文件**: `service/module_loader/src/mmi_service.cpp`

```cpp
// [TEST BYPASS] prefer allowing only the named local test process.
// Avoid unconditional return RET_OK except as a last-resort local fallback.
```

### 部署绕过后的 .so

```bash
# 备份原始 .so
$WIN_SSH "$HDC shell mount -o rw,remount /"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-server.z.so /system/lib/libmmi-server.z.so.bak"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-service.z.so /system/lib/libmmi-service.z.so.bak"

# 推送修改后的 .so（从编译产物）
$WIN_SCP libmmi-server.z.so "$WIN_SCP_DST/libmmi-server.z.so"
$WIN_SSH "$HDC file send $WIN_HOME\\Desktop\\libmmi-server.z.so /system/lib/libmmi-server.z.so"
$WIN_SCP libmmi-service.z.so "$WIN_SCP_DST/libmmi-service.z.so"
$WIN_SSH "$HDC file send $WIN_HOME\\Desktop\\libmmi-service.z.so /system/lib/libmmi-service.z.so"

# 重启 multimodalinput 服务
$WIN_SSH "$HDC shell kill \$(pidof multimodalinput)"
```

**注意**：.so 在 `/system/lib/`，不是 `/system/lib/platformsdk/` 或 `/system/lib/chipset-pub-sdk/`。

### 还原

```bash
$WIN_SSH "$HDC shell mount -o rw,remount /"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-server.z.so.bak /system/lib/libmmi-server.z.so"
$WIN_SSH "$HDC shell cp /system/lib/libmmi-service.z.so.bak /system/lib/libmmi-service.z.so"
$WIN_SSH "$HDC shell kill \$(pidof multimodalinput)"
```

**测试完成后必须还原。** 绕过会降低系统安全性。

## 编译部署流水线

### 编译

测试二进制通过 `compile_test.py` 编译（使用 OpenHarmony 工具链交叉编译）：

```bash
cd <openharmony-source-root>
python3 <compile_test_script>
```

`compile_test.py` 的关键配置：
- `SOURCE` — 测试 .cpp 源文件路径
- `BUILD_DIR` — `<oh_root>/code/out/rk3568`
- `OUTPUT_DIR` — 编译产物子目录（如 `multimodalinput/input`）
- 产物位于 `$BUILD_DIR/$OUTPUT_DIR/<target_name>`

### 部署到设备

```bash
BINARY="<oh_root>/code/out/rk3568/<output_dir>/<target>"
```

直连设备：

```bash
$HDC file send "$BINARY" /data/local/tmp/<target>
```

Windows 跳板机：

```bash
$WIN_SCP "$BINARY" "$WIN_SCP_DST/<target>"
$WIN_SSH "$HDC file send $WIN_HOME\\Desktop\\<target> /data/local/tmp/<target>"
```

**路径注意**：只有 hdc 在 Windows 跳板机上运行时，`file send` 的源路径才是 Windows 路径（`C:\\...`）。

### 运行

```bash
$HDC shell chmod 755 /data/local/tmp/<target>
$HDC shell /data/local/tmp/<target>

# Windows 跳板机时：
# $WIN_SSH "$HDC shell chmod 755 /data/local/tmp/<target>"
# $WIN_SSH "$HDC shell /data/local/tmp/<target>"
```

**hdc shell 引号陷阱**：不要在 hdc shell 后用单引号包裹命令（`hdc shell 'cmd1 && cmd2'`），会报 `no closing quote`。拆成多条 hdc 命令。

## Phase-Based Dump 捕获

### 原理

测试二进制通过写 phase 文件通知外部脚本当前阶段，外部脚本检测到新 phase 后执行 hidumper 捕获。

### C++ 端 — DumpPhase()

```cpp
static void DumpG(const char *label)
{
    std::cout << "\n===== " << label << " =====" << std::endl;
    std::cout.flush();
    FILE *f = fopen("/data/local/tmp/dual_group_phase.txt", "w");
    if (f) { fprintf(f, "%s\n", label); fclose(f); }
    std::this_thread::sleep_for(std::chrono::seconds(3));  // 等外部脚本捕获
}
```

3 秒 sleep 是关键 — 外部脚本 1 秒轮询一次，需要留出足够时间。

### Shell 端 — 后台捕获脚本

```bash
#!/system/bin/sh
DUMP=/data/local/tmp/dump.txt
PHASE=/data/local/tmp/dual_group_phase.txt
TEST=/data/local/tmp/<test_binary>
rm -f "$DUMP" "$PHASE"
chmod 755 "$TEST"
$TEST &
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
echo "TEST_DONE" >> "$DUMP"
```

**关键**：PHASE 文件路径必须与 C++ 端一致。之前出过 `phase.txt` vs `dual_group_phase.txt` 不匹配导致整个 dump 为空的 bug。

### 拉取 dump 到本地

```bash
# 直连设备
$HDC file recv /data/local/tmp/dump.txt ./dump.txt

# Windows 跳板机
$WIN_SSH "$HDC file recv /data/local/tmp/dump.txt $WIN_HOME\\Desktop\\dump.txt"
$WIN_SCP "$WIN_SCP_DST/../Desktop/dump.txt" /tmp/dump.txt
```

## 设备发现轮询

uinput `UI_DEV_CREATE` 后设备需要被 libinput 扫描到才能通过 InputManager 发现。轮询模式：

```cpp
static int FindDevice(const std::string &targetName) {
    struct FindState {
        std::mutex mtx;
        std::condition_variable cv;
        int foundId = -1;
        int pending = 0;
        bool done = false;
    };
    for (int attempt = 0; attempt < 30; ++attempt) {
        auto state = std::make_shared<FindState>();
        InputManager::GetInstance()->GetDeviceIds([state, targetName](std::vector<int32_t> &ids) {
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
                    [state, id, targetName](std::shared_ptr<InputDevice> dev) {
                        bool notify = false;
                        {
                            std::lock_guard<std::mutex> lock(state->mtx);
                            if (dev && dev->GetName() == targetName && state->foundId < 0) {
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
        state->cv.wait_for(lock, std::chrono::milliseconds(500), [&] { return state->done; });
        if (state->foundId >= 0) return state->foundId;
        std::this_thread::sleep_for(std::chrono::milliseconds(500));
    }
    return -1;
}
```

最多等 15 秒（30 次 x 500ms）。实测通常 1-3 秒内发现。

## hidumper Dump 字段参考

常用字段和解读细节见 `references/hidumper-dump-fields.md`。主流程只要求在报告中引用实际 dump 阶段、关键字段和结论，不要复制完整 dump 表。

## SELinux 注意

真机默认 SELinux Enforcing，测试前需要临时关闭：

```bash
$WIN_SSH "$HDC shell setenforce 0"   # Permissive
# 测试完成后还原：
$WIN_SSH "$HDC shell setenforce 1"   # Enforcing
```

不关闭 SELinux 时，`/dev/uinput` 访问和部分 IPC 会被拒绝。

## GN 构建目标配置

测试二进制的 `BUILD.gn` 配置要点：

```gn
ohos_executable("dual_group_interleave_test") {
  sources = [ "dual_group_interleave_test.cpp" ]
  deps = [
    "//foundation/multimodalinput/input/frameworks/proxy:libmmi-client",
    "//base/security/access_token/interfaces/innerkits/nativetoken:libnativetoken",
    "//base/security/access_token/interfaces/innerkits/accesstoken:libaccesstoken_sdk",
    "//base/security/access_token/interfaces/innerkits/token_setproc:libtoken_setproc",
  ]
  external_deps = [ "input:libmmi-client" ]
  testonly = true      # 测试专用，不参与正式构建
  part_name = "input"
  subsystem_name = "multimodalinput"
}
```

`testonly = true` 确保不会被正式产品构建拉入。

## 完整执行顺序

```
准备阶段：
  1. 获取用户明确授权，并记录备份/还原/验证计划
  2. 修改 server 端绕过 → 编译 .so
  3. 备份原 .so → 部署新 .so → 重启服务 → 记录替换验证
  4. SELinux permissive（如测试确需）

测试阶段：
  5. 编译测试二进制 (compile_test.py)
  6. 部署后台 dump 脚本 + 测试二进制到设备
  7. 运行后台 dump 脚本（启动测试 + hidumper 捕获）
  8. 拉取 dump 文件到本地分析

还原阶段：
  9. 还原 server 端 .so（从 .bak）
  10. SELinux enforcing（如果前面改成 permissive）
  11. 验证还原：重启服务 + 确认正常功能，并把结果写入报告
```

## Common Mistakes

| 错误 | 后果 | 修复 |
|------|------|------|
| Phase 文件路径不匹配 | dump 全程为空 | C++ 写的路径和 shell 读的路径必须完全一致 |
| hdc shell 用单引号包裹多命令 | `no closing quote` 错误 | 拆成多条独立 hdc 命令 |
| .so 推到错误路径 | 服务加载旧 .so，绕过不生效 | 路径是 `/system/lib/`，不是 platformsdk/ 或 chipset-pub-sdk/ |
| 忘记 mount -o rw,remount / | file send 到 /system/ 失败 | 先 remount |
| DumpG sleep 太短 | 外部脚本来不及捕获 | 至少 3 秒（脚本 1 秒轮询一次） |
| 忘记 testonly=true | 正式构建报错或拉入测试代码 | BUILD.gn 中加 testonly=true |
| 忘记还原 server 绕过 | 安全风险 | 测试完必须从 .bak 还原 |
| 未经授权直接 remount/替换 .so/关闭 SELinux | 改变真机系统状态且难以追责 | 先取得明确授权并记录备份、还原和最终验证 |
| SELinux 未关闭 | uinput/IPC 被拒绝，报权限错误 | `setenforce 0` |
| InitNativeToken 放在 InputManager 调用之后 | 权限检查失败 | 必须在 main() 最开始调用 |
