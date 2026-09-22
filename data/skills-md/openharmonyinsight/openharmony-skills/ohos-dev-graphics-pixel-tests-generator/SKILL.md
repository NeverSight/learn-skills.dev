---
name: ohos-dev-graphics-pixel-tests-generator
metadata:
  author: openharmony
  scope: domain
  stage: development
  domain: cpp
  capability: pixel-tests-generator
  version: 0.1.0
  status: trial
  tags:
    - cpp
    - test case generator
description: 务必在创建、修改、评审或调试 OpenHarmony graphic_2d graphic_test 像素比对测试时使用；只要用户提到 RSGraphicTest、GRAPHIC_TEST、GRAPHIC_TESTS、GRAPHIC_N_TEST、Rosen 渲染测试、RSCanvasNode、RSSurfaceNode、Drawing::Canvas、PixelMap、截图测试、graphic_test 目录或 /data/local/graphic_test 图片，就必须使用。
---

# OpenHarmony 图形像素测试

使用本技能为 OpenHarmony Rosen 图形像素比对框架生成符合仓库风格的 C++ 测试，目标目录通常是 `graphic_test/test`。

生成用例不只是写一个测试函数。好的结果需要选对测试目录和 `RSGraphicTestType`，遵循相邻文件风格，正确使用框架生命周期，注册所有需要保活的渲染节点，并在新增 `.cpp` 时更新 `graphic_test/test/BUILD.gn`。

## 关键禁令

- 不要在 `GetRootNode()->AddChild(...)`、`AddChildToSubWindow(...)` 或创建自定义 surface 后忘记 `RegisterNode(...)`；节点可能提前释放，截图会空白或不稳定。
- 不要把独立测试误写成 `GRAPHIC_TESTS`；只有明确需要同一 fixture 的多个 test surface 聚合成一张网格截图时才使用。
- 不要为普通 graphic test 新建 `ohos_unittest` target；新增 `.cpp` 应加入 `graphic_test/test/BUILD.gn` 里现有的分类 sources 数组。
- 不要凭空发明 Drawing helper、测试 helper 或 RenderService API；先查相邻文件和 framework 头文件。
- 不要在自动截图测试里无脑添加 `FlushImplicitTransaction` 和 sleep；只有手动截图、立即查询渲染结果或相邻测试需要时才添加。
- 不要使用无法保证存在的图片资源路径；优先复用同目录已有 `/data/local/tmp/...` 路径，或在代码里生成 PixelMap。

## 开始步骤

1. 在工作区中定位真实的 `graphic_test` 根目录。
2. 先读 `graphic_test/graphic_test_framework/include/rs_graphic_test.h`、`rs_graphic_test_ext.h`，再读与需求最接近的现有测试文件。
3. 生成前先回答这些检查点：
   - Purpose：我要验证哪一个具体渲染行为或截图差异？
   - Existing：应该扩展已有测试文件，还是新建一个更合适？
   - Type：这个场景对应哪个 `RSGraphicTestType` 和哪个测试宏？
   - Pixels：截图中用什么颜色、图片、边框、网格或边界值让差异可见且稳定？
   - Build：如果新增文件，应加入 `test/BUILD.gn` 的哪个 sources 数组？
4. 确认场景后，只读取本技能中相关的参考文件：
   - `references/framework-lifecycle.md`：框架生命周期、宏、截图、节点生命周期。
   - `references/test-taxonomy-build.md`：测试放置位置和 `test/BUILD.gn` 更新规则。
   - `references/code-patterns.md`：节点、图片、Canvas、动画、手动截图、子窗口、PixelMap 的惯用写法。
   - `references/templates.md`：紧凑起始模板。
5. 优先沿用本地相邻文件风格。参考文件解释模式；现有代码才是 include、helper 名称和 API 可用性的权威。
6. 至少做文本级检查：宏名、namespace、include、`RegisterNode`、source list 入口，以及是否存在虚构 API。

## 生成流程

### 1. 判断测试归类

根据被测行为选择目录和 `RSGraphicTestType`：

| 场景 | 常用目录 | 常用类型 |
| --- | --- | --- |
| 节点外观、背景、前景、几何、内容显示 | `rs_display_effect/property_display` 或 `rs_display_effect/content_display` | `CONTENT_DISPLAY_TEST` |
| 动画协议、曲线、自定义 modifier 动画 | `rs_display_effect/animation` | `ANIMATION_TEST` |
| NG shader/filter/effect/mask/shape 视觉效果 | `rs_effect_feature/...` | `EFFECT_TEST` |
| PixelMap、font、symbol 等开放能力 API | `open_capability/...` | 通常是 `CONTENT_DISPLAY_TEST`，或沿用本地现有类型 |
| 脏区、HWC、GPU composer、hybrid render、性能相关渲染 | `rs_perform_feature/...` | 沿用本地现有类型，常见为 `CONTENT_DISPLAY_TEST`、`GPU_COMPOSER_TEST`、`HYBRID_RENDER_TEST` |
| surface capture、screen capture、多屏、无障碍、水印、render group | `rs_func_feature/...` | 通常是 `CONTENT_DISPLAY_TEST` |
| 框架 surface 行为 | `rs_framework/...` | 通常是 `CONTENT_DISPLAY_TEST` |
| Effect Kit NDK filter | `effect_kit/...` | `EFFECT_TEST` |

如果已有相关文件，优先扩展该文件；只有当新功能边界清晰、追加会让旧文件混乱时，才新增文件。

### 2. 选择测试宏

- 普通自动截图像素测试使用 `GRAPHIC_TEST(TestClass, TYPE, TestName)`。
- `GRAPHIC_TEST(TYPE, TestName)` 只适合很小的默认 fixture 测试；真实测试文件多数会定义派生 fixture。
- 多个测试函数需要拼成同一张网格截图时使用 `GRAPHIC_TESTS`。保持共享 `SetScreenSize`，并记住输出文件名不包含单个 test name。
- 只有当测试必须手动控制截图时机、调用自定义 `TestCaseCapture`、在 `FlushImplicitTransaction` 后 sleep，或要避开自动截图时，才使用 `GRAPHIC_N_TEST`。
- 除非任务明确涉及录制/回放，否则不要使用 `GRAPHIC_D_TEST`。当前测试语料主要使用自动和手动测试。

### 3. 构建 fixture

多数文件使用这种结构：

```cpp
class ExampleTest : public RSGraphicTest {
public:
    void BeforeEach() override
    {
        SetScreenSize(screenWidth, screenHeight);
    }

private:
    const int screenWidth = 1200;
    const int screenHeight = 2000;
};
```

只有当测试刻意捕获子区域或全屏显示行为时，才使用 `SetSurfaceBounds`。涉及特殊显示截图、子窗口、手动截图时，应对照同功能区域已有文件。

### 4. 创建可见且确定的像素输出

像素比对测试需要清晰、稳定的画面：

- 除非测试裁剪或越界行为，否则把节点放在配置的屏幕范围内。
- 参数矩阵使用网格布局：根据 `screenWidth`、`screenHeight`、行列计算 `sizeX`、`sizeY`、`x`、`y`。
- 使用对比明显的背景、边框、图片内容，让期望差异可见。
- 测试属性钳制时覆盖边界值：负数、0、中间值、1、大值、非法枚举值等。
- 如果每个取值应该生成独立图片，用多个 `GRAPHIC_TEST`；如果取值应该在同一张截图中对比，用单个测试内的网格。

### 5. 正确添加并保活节点

每个加入场景并需要渲染的节点都应这样处理：

```cpp
GetRootNode()->AddChild(testNode);
RegisterNode(testNode);
```

对于父子节点树，如果父节点或子节点的局部变量可能离开作用域，父子都要注册。对于子窗口，通过 `GetRootNode()->AddChildToSubWindow(subId, node)` 添加，并仍然调用 `RegisterNode(node)`。

### 6. 只在必要时 flush

自动测试通常依赖 `TearDown()` 统一 flush 和截图。当测试需要立即查询渲染结果、手动截图、提交节点后调用 surface/PixelMap API，或相邻测试已经采用显式提交模式时，再添加 `RSTransactionProxy::GetInstance()->FlushImplicitTransaction()`。

使用 `FlushImplicitTransaction` 时，需要 include `transaction/rs_interfaces.h`。

### 7. 新增文件时更新 BUILD.gn

新增 `.cpp` 时，必须更新 `graphic_test/test/BUILD.gn`，把相对路径插入匹配的 sources 数组，例如 `rs_display_effect_sources`、`rs_effect_feature_sources`、`open_capability_sources`、`rs_func_feature_sources`、`rs_perform_feature_sources`、`rs_framework_sources` 或 `effect_kit_sources`。

普通 graphic test 不要新建 `ohos_unittest` target。现有 `RSGraphicTest` target 已经汇总各分类 sources 数组。

## 完成前必要检查

声称完成前，至少运行快速文本检查：

```bash
rg -n "GRAPHIC_(N_)?TESTS?|RegisterNode|FlushImplicitTransaction" path/to/new_or_changed.cpp
rg -n "relative/path/to/new_file.cpp" graphic_test/test/BUILD.gn
```

然后确认：

- 文件有与相邻测试一致的 Apache copyright header。
- include 与实际 API 使用匹配，没有残留模板垃圾。
- 代码位于 `namespace OHOS::Rosen`。
- 每个测试宏都使用正确 fixture、类型和唯一测试名。
- 每个需要渲染的场景节点都已加入 root 或 sub-window，并调用 `RegisterNode`。
- 手动截图测试在 flush/wait 后调用截图 helper，并使用 `GRAPHIC_N_TEST`。
- 新文件已加入正确的 source array。
- 没有残留占位调用，例如 `DrawTextBlob(...)`、`paintSetColor` 或虚构 helper 名称。

## 常见失败模式

| 失败现象 | 原因 | 修复 |
| --- | --- | --- |
| 截图空白 | 节点未添加、未注册或没有可见属性 | 添加 child，调用 `RegisterNode`，设置可见 bounds/color/image |
| Drawing 代码编译失败 | 使用了泛化 Drawing API 签名，没有贴合本地风格 | 查看相邻 Drawing 测试，使用 `Brush`/`Pen` 和 `AttachBrush`/`DetachBrush` |
| 测试未参与构建 | 新 `.cpp` 没加到 `test/BUILD.gn` 分类数组 | 把相对路径加入正确 sources list |
| 输出分组错误 | 独立用例误用了 `GRAPHIC_TESTS` | 除非明确需要网格聚合，否则使用 `GRAPHIC_TEST` |
| 自动截图前特殊查询存在竞态 | 查询渲染输出前没有提交事务 | 添加 `FlushImplicitTransaction`，并参考相邻测试的等待模式 |
| 依赖资源的测试渲染为空 | 设备上缺少图片路径 | 复用同目录已有 `/data/local/tmp/...` 路径，或在代码中生成 PixelMap 数据 |

## 当前语料特点

当前 `graphic_test/test` 以 `GRAPHIC_TEST` 自动截图为主；`GRAPHIC_N_TEST` 大量用于脏区、surface、screen、水印和手动截图流程。`GRAPHIC_TESTS` 主要出现在 `test_template` 风格的网格聚合场景，应谨慎选择。

多数视觉属性测试不会在 C++ 中断言像素值，而是创建确定性的渲染场景，由框架把 PNG 保存到 `/data/local/graphic_test/...` 后再做比对。
