---
name: vtk
description: "专门用于编写、修改、解释和调试 VTK（Visualization Toolkit）Python/C++ 代码。用户只要在做 VTK 编程、vtk pipeline、vtkPolyData/vtkImageData/vtkUnstructuredGrid、reader/filter/mapper/actor/writer、STL/OBJ/PLY/VTP/VTU/DICOM、体绘制、Qt 集成、CMake、vtk_module_autoinit、代码不显示/不更新/崩溃、Python/C++ 互转、VTK 类名/头文件/module 查询或想参考官方示例程序时，就应使用本 skill。此 skill 是代码优先的总入口路由：先判断要写/改/调哪类 VTK 代码，再按需读取少量 reference；类索引和 examples 只是辅助，避免编造 API。"
---

# VTK 编程助手 Router

本 skill 的目标不是“查资料”，而是让 Claude 更可靠地写、改、解释、调试 VTK Python/C++ 代码。总入口保持轻量：先判断编程任务类型，再读取 1–3 个相关 reference。类索引和官方 examples 是辅助工具，只在需要确认类名、头文件、CMake module 或寻找示例思路时使用。


## 环境与版本策略

本 skill 面向 VTK 9.x，随仓库提供的 class/header/module 快照由 VTK 9.3.1
源码生成。生成代码时先确认用户实际安装的 VTK 版本；若版本不同，优先使用
用户环境中的 CMake package 和源码进行核对，不要假设存在某个本机盘符。

| 配置项 | 值 |
|---|---|
| **参考版本** | 9.3.1 |
| **CMake package** | 由用户通过 `VTK_DIR` 或 CMake package registry 提供 |
| **编译器** | 与用户 VTK 二进制包匹配的编译器和架构 |

**CMake 配置建议：**
```cmake
cmake -S . -B build -DVTK_DIR=<path-to-vtk>/lib/cmake/vtk-9.3
```

Windows 运行时，把用户 VTK 的 `bin` 目录加入当前进程的 `PATH`；Linux/macOS
使用对应的 `LD_LIBRARY_PATH`/`DYLD_LIBRARY_PATH` 或安装规则。不要把这些路径
写死进项目的 `CMakeLists.txt`。

Windows 示例（用户自行替换路径）：
```bash
set PATH=<path-to-vtk>\bin;%PATH%
```

**注意事项：**
- C++ 编译器、架构和 Debug/Release 配置必须与 VTK 二进制包匹配。
- 生成 `CMakeLists.txt` 时优先使用 `find_package(VTK REQUIRED COMPONENTS ...)`，
  通过配置命令传入 `VTK_DIR`，不要写入个人绝对路径。

## 查找源码 / 符号索引

需要查看 VTK 源码、头文件内容、类/符号定义时，使用用户提供的未加密源码树
（例如通过 `VTK_SOURCE_DIR` 环境变量或用户明确给出的路径）。

```
<VTK_SOURCE_DIR>
```

具体规则：
- 需要查看某个类的声明、方法签名、宏定义、头文件内容时，在 `<VTK_SOURCE_DIR>`
  下按文件名查找（如 `vtkPolyData.h` 在 `Common/DataModel/`，`vtkSTLReader.h` 在
  `IO/Geometry/`）。
- 构建类索引、确认类是否存在、查头文件 / CMake module 归属时，源数据也来自源码树。
- 找到头文件后，实现在同模块同名的 `.cxx` / `.txx` 文件里（VTK 源码约定），需要看实现时一并读。
- 安装包中的 include/lib/bin 路径只用于编译和运行；符号核对优先使用源码树。

---

## 首要工作流：先把代码任务定型

1. 明确用户是在做哪件事：新写示例、改已有代码、排错、Python/C++ 互转、CMake/工程集成、查类/API、按官方 example 改造。
2. 明确语言和运行环境：Python 还是 C++；如果是 C++，默认需要 include、CMake components、`vtk_module_autoinit`；如果是 Python，默认 `import vtk`，必要时使用 `vtkmodules.*` 或 `vtk.util.numpy_support`。
3. 明确核心数据对象：`vtkPolyData`、`vtkImageData`、`vtkUnstructuredGrid`、`vtkMultiBlockDataSet`、table/graph/view。VTK 代码是否正确，首先取决于数据对象和 filter/mapper 是否匹配。
4. 组织 pipeline：reader/source → filter(s) → mapper/actor/volume 或 writer。需要拿数据检查时才 `Update()`；手工改数据时标记 `Modified()`；显示后要 `Render()`。
5. 生成代码时优先给“最小可运行完整示例”，不是零散片段。C++ 示例通常同时给 `main.cpp` 和 `CMakeLists.txt`。Python 示例要能直接运行，并打印关键诊断信息。
6. 调试时先按概率排序：数据是否为空、输入连接方式是否错、mapper/filter 类型是否错、没有 `Modified()`/`Render()`、CMake module/include 错、对象生命周期/Qt 事件循环错、OpenGL/环境问题。

## Reference 路由表

| 编程任务 | 先读 | 可能再读 |
|---|---|---|
| 写/改 VTK pipeline、解释 `SetInputData`/`SetInputConnection`、数据对象选择 | `references/pipeline-data-model.md` | `references/performance-debugging.md` |
| 写 C++ 工程、补 include、CMake components、链接错误、Windows DLL、Qt 工程 | `references/build-install-integration.md` | `references/class-index-guide.md` |
| 写 reader/writer 代码，STL/OBJ/PLY/VTP/VTU/VTI/VTM/DICOM/图片/CSV | `references/io-formats.md` | `references/class-index-guide.md` |
| 写显示代码，actor/mapper/renderer/camera/颜色映射/截图/离屏 | `references/rendering-visualization.md` | `references/performance-debugging.md` |
| 写网格处理代码，clean/triangulate/normals/smooth/decimate/clip/cut/connectivity | `references/filters-geometry-mesh.md` | `references/pipeline-data-model.md` |
| 写图像/体数据代码，DICOM、切片、重采样、阈值、FlyingEdges/MarchingCubes、体绘制 | `references/image-volume.md` | `references/rendering-visualization.md` |
| 写交互、picking、widget、PyQt/PySide、C++ Qt 嵌入代码 | `references/interaction-qt-widgets.md` | `references/build-install-integration.md` |
| 代码不显示、不更新、黑屏、慢、崩溃、数组不生效 | `references/performance-debugging.md` | 对应领域 reference |
| Python/C++ 互转、`vtkNew`/`vtkSmartPointer`、NumPy/VTK 数组互转 | `references/python-cpp-api-patterns.md` | `references/build-install-integration.md` |
| 需要确认类是否存在、头文件、CMake module、同类对象 | `references/class-index-guide.md` | `scripts/search_vtk_class_index.py` |
| 对某个具体类的真实用法没把握、要看官方测试/示例源码怎么写 | `references/examples-tests-index.md` | `scripts/search_vtk_examples.py` |
| 用户明确要官方 example 或 demo（examples.vtk.org 教学示例） | `references/examples-official.md` | `references/examples-tests-index.md` |

## 防幻觉检查：随包快照与降级路径

两个索引随 Skill 一起发布，完整安装后用户不需要另行生成或安装“本地索引”。
它们只是写代码时的核查工具。脚本在 skill 目录下，运行时用本 skill 基目录拼出
绝对路径（当前工作目录通常是用户项目，相对路径会找不到脚本）。

确认某类是否存在、C++ include、CMake module：

```bash
python <skill基目录>/scripts/search_vtk_class_index.py vtkSTLReader
python <skill基目录>/scripts/search_vtk_class_index.py --category filters-geometry-mesh Decimate
python <skill基目录>/scripts/search_vtk_class_index.py --module IOXML XML
```

如果发行包被裁剪、用户只复制了 `SKILL.md`，可以从用户的 VTK 源码即时扫描：

```bash
python <skill基目录>/scripts/search_vtk_class_index.py \
  --vtk-source <VTK_SOURCE_DIR> vtkSTLReader
```

也可以使用 `VTK_SOURCE_DIR` 或 `VTK_CLASS_INDEX` 环境变量。两者都没有时，脚本
会返回明确的缺失提示；此时通过官方 VTK 源码/文档核对 API，不要猜测 header 或
CMake module。类索引快照来自 VTK 9.3.1 源码：3111 个 `vtk*.h` 头文件，2925 个
class/struct 声明，198 个模块。需要刷新快照时运行
`scripts/build_class_index.py --vtk-source <VTK_SOURCE_DIR>`。

确认某类官方真实用法（随包索引：1959 个类 → 11911 条官方测试/示例源码路径，用法与源码抓取见 `references/examples-tests-index.md`）：

```bash
python <skill基目录>/scripts/search_vtk_examples.py vtkImagePlaneWidget
```

官方 examples 索引缺失时，使用 `VTK_EXAMPLES_INDEX` 或 `--index` 指定替代文件；
没有替代文件就按 `references/examples-tests-index.md` 的官方在线索引流程查找，
并明确说明当前结果未经过随包索引核对。

## 输出规范

写代码时，优先使用这个结构：

1. 一句话说明方案和数据流。
2. 给完整代码。C++ 同时给 `CMakeLists.txt`；Python 给单文件脚本。
3. 解释关键 VTK 点：输入输出数据类型、为何用 `SetInputConnection` 或 `SetInputData`、何时 `Update/Modified/Render`、CMake module 来自哪里。
4. 给 3–5 个调试检查点，而不是泛泛列十几条。

用户用中文时，用中文回答；VTK 类名、函数名、模块名保留英文原文。不要为了显得全面而复制大量参考资料；回答要服务当前代码任务。
