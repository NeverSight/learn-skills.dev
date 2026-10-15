---
name: meishe-effect-kit-android
description: 在已有 Android 工程中接入、扩展、排障或辅助验收 NveEffectKit，以及把该工程现有 NVE 管线的最终输出纹理录制到系统相册。用于首次集成或新增完整/单项美肤、美型、微整形、美妆、滤镜、人脸道具、自定义特效、NVE 处理后画面录制，以及处理 AAR/授权/模型/素材、CameraX/Camera2/自定义 GL、生命周期、黑屏/闪退/卡死、预览或效果不生效、方向镜像、音画同步和性能/UI 验证问题；不用于没有 NVE 最终输出管线的通用相机录制。
---

# NveEffectKit Android 接入

只修改客户已有工程，保持其模块、相机、GL、线程和 UI 所有权。以目标 AAR 为接口事实；
不复制未经授权的 Activity/AAR/lic/模型/素材/UUID，不猜版本敏感 API。

## 首次版本提示

每个新任务首次使用本 skill 时，先输出一次以下提示；同一任务后续响应不重复。
不要求用户确认，提示后继续执行本次需求：

> 版本提示：当前 Skill 基于美摄 SDK 3.16.1，并向后兼容；若目标项目使用更高版本 SDK，可能存在效果差异，请从[美摄官网开发者中心](https://www.meishesdk.com/downloads/)获取对应版本的 Skill。

## 固定五步

### 1. 解析范围

```text
python -B -X utf8 <skill-dir>/scripts/feature_contract.py --features <csv>
```

只传逗号分隔的功能词组，不传整句需求。未知 feature 立即停止；存在
`scope_selection_required` 时按 `selection_requests` 让用户选择并等待。选择完成前，
展开的 `implementation_features` 只是候选全集，不得实施。资源路径只授权读取，不代表
选择功能；滤镜和美妆范围解析按对应 reference 执行。

`recording` 只表示消费既有 NVE 最终输出纹理，不扩成通用相机录制、素材或特效功能。

### 2. 盘点并通过前置门禁

首次接入、新增能力或 AAR/ABI/资源/渲染契约变化时，开始写代码前运行：

```text
python -B -X utf8 <skill-dir>/scripts/inspect_android_project.py <project-root> \
  --variant <variant> --features <csv> [--resource-path <authorized-path>] \
  [--asset-map <feature-to-path.json>] --json --gate
```

按 [前置条件](references/prerequisites.md) 确认唯一 AAR、基线 hash、模块/ABI、资源、
渲染接入点和现有 UI；输入未变化时不重复盘点。非零时停止受影响功能。只检查最终所选项，
只读取用户授权的工程外路径。

仅为已有 NVE 最终输出管线增加 `recording` 时报告必须为 `host-only`；不重复校验既有
NVE AAR/lic/模型/素材，但必须发现取得、消费并回收 `renderEffect` 最终纹理的闭环。
缺少该闭环时停止，且不转为通用相机录制；混合请求仍对新增 NVE 功能执行资源门禁。

### 3. 按需读取

- 美颜：[beauty.md](references/beauty.md)
- 美妆：[makeup.md](references/makeup.md)
- 滤镜、道具、自定义特效：[effects.md](references/effects.md)
- NVE 最终输出录制：[recording.md](references/recording.md)
- Gradle、ABI、相机接入：[project-integration.md](references/project-integration.md)
- 帧、GL、线程、方向和生命周期：[lifecycle-rendering.md](references/lifecycle-rendering.md)
- Camera2 OES + NV21：[camera2-oes-nv21.md](references/camera2-oes-nv21.md)
- 模型、素材和安装：[assets-and-models.md](references/assets-and-models.md)
- UI 接入与默认面板：[ui-integration.md](references/ui-integration.md)
- AAR 基线和版本契约：[compatibility-contracts.md](references/compatibility-contracts.md)
- 登记模板与宿主适配：[golden-templates.md](references/golden-templates.md)
- 故障定位：[troubleshooting.md](references/troubleshooting.md)
- 构建和设备验收：[verification.md](references/verification.md)

单功能任务只读取相关 reference，不加载无关配方。

### 4. 完成纵向闭环

实施前按场景加载以下最小 reference 集，不得凭通用经验跳过：

| 场景 | 必读 reference |
| --- | --- |
| 稳定桥上新增效果 | 所选功能文档、golden-templates；涉及模型/素材时追加 assets-and-models，改 UI 时追加 ui-integration |
| 首次 NVE 接入 | 所选功能文档、project-integration、lifecycle-rendering、assets-and-models、compatibility-contracts、golden-templates、verification |
| Camera2 OES + NV21 | 首次接入集合追加 camera2-oes-nv21 |
| 改相机、帧、GL、方向或输出消费 | 首次接入集合，并按 verification 逐阶段取证 |
| 仅新增最终输出录制 | recording、verification |

首次或高风险接入按阶段推进。有可用设备时逐阶段运行轻量门禁，观察未通过就停止；没有设备不等同于
阶段失败：标准路径可继续单个纵向切片、必要 UI 和最小编译并标记运行时未验证，高风险相机/GL 路径
不得继续批量扩展多个效果模块：

- 原始预览：非黑屏，方向、镜像、宽高比和 crop/viewport 正确。
- 无效果：真实输入输出闭环，确认输出 type/size、raw fallback、GL 恢复和单次回收，无闪烁或几何跳变。
- 单效果：0/默认/明显值或选择/移除可见且能恢复原始画面。
- 选定范围与恢复：只实现最终 leaf feature；前后台、页面重进和 GLContext 重建后状态一致。

登记 AAR 命中 catalog hash 时才使用版本化 NVE 模板；复用使用 `controllers`，首次接入或
改变相机、帧、GL、方向、输出消费时使用 `all`：

```text
python -B -X utf8 <skill-dir>/scripts/materialize_baseline_templates.py <project-root> \
  --aar <confirmed-aar> --baseline 3.16.1 --layer <controllers|all> \
  --source-dir <relative-java-dir> --package <java-package> --features <csv> \
  [--profile camera2-oes-nv21] [--ui-profile <profile>] [--test-source-dir <dir>] \
  [--makeup-catalog-report <inspect-makeup-json>] --dry-run
```

美妆范围必须先把 `inspect_makeup_catalog.py --json` 的零错误、零警告、无待选择报告保存到
目标工程或临时目录，并传 `--makeup-catalog-report`。dry-run 必须检查
`missing_gradle_dependencies` 和 `compatibility_issues`；未清零不得执行实际落地。

只为既有 NVE 最终输出增加录制时使用版本无关模板：

```text
python -B -X utf8 <skill-dir>/scripts/materialize_recording_templates.py <project-root> \
  --source-dir <relative-java-dir> --package <java-package> [--test-source-dir <dir>] --dry-run
```

两个落地器都先检查 dry-run，再执行且不得覆盖已有文件。录制模板只接既有最终纹理，禁止
接原始相机纹理或再次调用 `renderEffect`。其余适配和运行时硬约束以对应 reference 为准。

登记基线在 GL 就绪后由 Android 主线程 `initialize`；渲染线程消费并仅回收一次每个输出，
在旧 EGLContext 有效时释放宿主 GL，最后 `cleanUp`。安装和对象创建不得进入每帧或参数
回调。效果无效时按 troubleshooting reference 的固定顺序排查。

UI 优先级为用户明确提供的设计 → 用户工程已有设计体系 → skill 登记默认 UI；只有前两者都不存在
时才使用第三级，且不访问、不搜索、不依赖未经授权的工程外资源。

### 5. 验证和交付

每次修改运行严格静态校验和目标模块最小编译：

```text
python -B -X utf8 <skill-dir>/scripts/validate_nve_integration.py <project-root> \
  --profile <profile> --features <csv> --strict
<gradle-wrapper> :<module>:compile<Variant>JavaWithJavac
```

有可用设备时，首次/高风险 NVE 接入把 `assets/stage-evidence.example.json` 复制到目标工程或临时
目录，只更新副本，再用 `verify_nve_stages.py` 逐阶段验证；观察失败即停止扩展。无设备时不伪造
阶段证据，按第 4 步限制继续并保留运行时未验证项。
首次/高风险接入检测到可用设备时，交付回答前还必须执行目标 APK 安装和冷启动门禁；不因用户
未再次要求“完整验收”而跳过。使用 `verify_nve_delivery.py --device <serial>`，至少确认异步
模型/素材准备窗口后目标进程仍在前台且目标进程日志无崩溃。

仅接入 `recording` 不执行上述 NVE 特效阶段门禁，改按录制 reference 验证相册、音画同步、
压力丢帧、前后台和回滚。

仅在用户要求完整交付验收时运行：

```text
python -B -X utf8 <skill-dir>/scripts/verify_nve_delivery.py <project-root> \
  --module <module> --variant <variant> --features <csv> --profile <profile>
```

只使用 `BLOCKED`、`STATIC_READY`、`DEVICE_VERIFIED`。任何自动状态都不证明视觉效果或
发布通过；最终只报告实际命令、通过项、阻塞项和未覆盖风险。
