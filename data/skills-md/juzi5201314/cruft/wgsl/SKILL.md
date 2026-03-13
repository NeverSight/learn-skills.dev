---
name: wgsl
description: WebGPU WGSL（现代语法、硬切换）写作指导：严格类型、入口点与 @location/@builtin IO、资源绑定 @group/@binding、常见语法差异与易错点；输出包含 WGSL + bindings/IO 摘要，便于直接接入渲染管线。
---

# WGSL Skill（WebGPU / wgpu / Bevy 通用）

本 skill 的目标是：把“需求描述”稳定转成**可编译、可接入**的 WGSL，并把**管线对接信息**（bindings / locations / entry points）一并输出，减少来回试错。


## 🎯 硬约束（必须遵守）

- 只写**现代 WGSL**：使用 `@vertex` / `@fragment` / `@compute` 与 `@location` / `@builtin` 等新语法；不写任何旧版/兼容写法。
- WGSL **严格类型**：每个变量/参数/返回值必须可推导或显式标注；需要时必须显式转换（例如 `f32(i32_value)`）。
- 默认不使用 `f16`（它是可选特性）；除非用户明确要求并说明已启用对应 feature。
- 代码标识符用英文；解释用中文（可混用英文术语）。


## 🧭 使用流程（每次写 WGSL 都按这个走）

1. 明确目标：
   - shader stage：`vertex` / `fragment` / `compute`
   - entry point 名称（例如 `vs_main` / `fs_main` / `cs_main`）
   - 输入/输出：顶点属性布局、inter-stage 变量、fragment 输出 attachment 数量
   - 资源：有哪些 buffer/texture/sampler，分别用于哪个 stage
2. 先画“接口”再写“算法”：
   - 用 `struct` 定义 VSIn / VSOut / FSIn / FSOut（或直接用参数与返回标注）
   - 写清所有 `@location(n)` 与 `@builtin(...)`
   - 写清所有 `@group(g) @binding(b)` 声明
3. 再实现逻辑（函数 + 控制流），并做“可编译自检清单”（见文末）。
4. 输出时必须带上：
   - 完整 WGSL
   - **Bindings 摘要表**（group/binding/kind/type/stage）
   - **IO 摘要表**（locations/builtins/类型）


## 🧱 语言核心速查（写对比写快更重要）

### 1) 类型与字面量

- 标量：`i32` / `u32` / `f32` / `bool`（`f16` 可选）
- 数字后缀（常用）：
  - `3u` → `u32`，`2i` → `i32`，`4f` / `4.5f` → `f32`，`5h` → `f16`
  - `6` / `7.0` 可能是抽象数（编译期推导），但**不要依赖它跨表达式自动“帮你转换”**
- 常见坑：
  - `let a = 1; let b = 2.0; a + b` 会类型不匹配；改成 `f32(a) + b` 或把两边统一成同类型。

### 2) `let` / `var` / `const`

- `let`：不可变值（常用）
- `var`：可变变量（有存储，能赋值）
- `const`：**编译期常量**（只能由编译期表达式组成，不能依赖运行时值）
- `override`：**管线常量（specialization constant）**，由宿主在创建 pipeline 时提供；适合做开关/常量参数/工作组大小等（见下文模板）

### 3) 向量与矩阵

- 向量：`vec2<T>` / `vec3<T>` / `vec4<T>`，常用别名：`vec2f` / `vec3f` / `vec4f`（`f32`）、`vec4u`（`u32`）等
- 访问：`.x/.y/.z/.w`、`.r/.g/.b/.a`、`a[i]`
- swizzle：`a.zx`、`a.zzy` 等
- 矩阵：`matCxR<T>`（列向量数组），常用 `mat4x4f`
  - `m[2]` 取第三列向量
  - `mat4x4f * vec4f` 合法，返回 `vec4f`

### 4) 数组

- 固定大小：`array<T, N>`
- 构造器：`array(v0, v1, ...)` 或 `array<T, N>(...)`
- runtime-sized array：
  - 仅允许在**根作用域 storage 声明**，或作为**根作用域 struct 的最后一个字段**（并绑定为 storage）
  - 用 `arrayLength(&arr)` 查询长度（仅对 runtime-sized array 有意义）

### 5) 函数与入口点

- 函数：`fn name(params) -> returnType { ... }`
- 入口点：`@vertex` / `@fragment` / `@compute`
- 易忽略但很关键：
  - shader “需要哪些 bindings”，只由 entry point **可达的访问路径**决定（未被入口点访问到的全局资源不会成为必需绑定）
  - 如果你想强制某个 binding 出现在管线需求里，可用 `_ = resource;` 做“假使用”

### 6) `override`（推荐：把可调参数都做成它）

```wgsl
override USE_FOG: bool = false;
override WORKGROUP_SIZE_X: u32 = 64u;

@compute @workgroup_size(WORKGROUP_SIZE_X)
fn cs_main(@builtin(global_invocation_id) gid: vec3u) {
  if (USE_FOG) {
    // ...
  }
}
```

要点：

- `override` 是“管线创建时决定”的常量，不是运行时变量。
- 适合：分支开关、数组上限、workgroup size、算法常量等。


## 🔌 管线 IO 与 Attributes（最常出错的地方）

### `@location(n)`：用户自定义 IO

- VS 输入：entry point 参数上的 `@location(n)`，或参数 struct 字段上的 `@location(n)`
- VS→FS：VS 输出 struct 字段 `@location(n)` 与 FS 输入 struct 字段 `@location(n)` 必须匹配（名字可不同，location 必须对）
- FS 输出：`@location(n)` 对应第 n 个 color attachment

### `@builtin(name)`：内建 IO

常用例子：

- VS 输入：`@builtin(vertex_index)`、`@builtin(instance_index)`
- VS 输出：`@builtin(position)`（裁剪空间 position，通常 `vec4f`）

### 插值控制（inter-stage 细节，做对了能少很多“奇怪闪烁/颜色不对”）

- 默认会对 float varyings 做透视正确插值（perspective interpolation）。
- 对 **整型/枚举/ID** 这类不该插值的值，显式使用 `@interpolate(flat)`（否则会报错或产生不符合预期的结果）。
- 需要屏幕空间线性插值时，可用 `@interpolate(linear)`（按需使用）。
- MSAA 下的插值采样位置（fragment）：
  - `@interpolate(center)`：默认，按像素中心插值
  - `@interpolate(centroid)`：保证采样点在图元覆盖区域内（更适合边缘）
  - `@interpolate(sample)`：每个 sample 都执行一次 fragment shader（更贵，但可精确到 sample）

### Builtins 全表（按 stage/方向使用，避免写错）

> 说明：以下表按 WebGPU 常用内建整理。`position` 在 VS 输出与 FS 输入语义不同。

| builtin | stage | io | type | 备注 |
| --- | --- | --- | --- | --- |
| `vertex_index` | vertex | in | `u32` | 当前 draw 的顶点索引（与 index buffer / baseVertex 等相关） |
| `instance_index` | vertex | in | `u32` | 当前 draw 的 instance 索引 |
| `position` | vertex | out | `vec4f` | 裁剪空间坐标（齐次坐标） |
| `position` | fragment | in | `vec4f` | framebuffer 空间位置（`w` 为 1，`xy` 像素坐标语义） |
| `front_facing` | fragment | in | `bool` | 是否正面 |
| `frag_depth` | fragment | out | `f32` | 写入深度（不写则用固定管线深度） |
| `sample_index` | fragment | in | `u32` | 当前 sample（MSAA） |
| `sample_mask` | fragment | in | `u32` | 覆盖到的 samples mask |
| `sample_mask` | fragment | out | `u32` | 输出 samples mask（可屏蔽某些 samples 写入） |
| `local_invocation_id` | compute | in | `vec3u` | workgroup 内线程坐标 |
| `local_invocation_index` | compute | in | `u32` | workgroup 内线性索引 |
| `global_invocation_id` | compute | in | `vec3u` | 全局线程坐标 |
| `workgroup_id` | compute | in | `vec3u` | workgroup 坐标 |
| `num_workgroups` | compute | in | `vec3u` | dispatch 的 workgroup 数量 |


## 🧩 资源绑定（Bindings）写法模板

> 注意：有些旧文章/示例会写成 `var<uniforms>`；现代 WGSL 关键字是 `var<uniform>`。

```wgsl
struct Uniforms {
  color: vec4f,
};

@group(0) @binding(0)
var<uniform> uniforms: Uniforms;

@group(0) @binding(1)
var my_sampler: sampler;

@group(0) @binding(2)
var my_tex: texture_2d<f32>;
```

storage buffer（示例）：

```wgsl
@group(0) @binding(3)
var<storage, read_write> data: array<vec4f>;
```

### Address spaces / access mode（经常漏写/写错）

- module-scope 资源变量必须是 `var<address_space, access>` 这种形式（例如 `var<uniform>`、`var<storage, read>`、`var<storage, read_write>`）。
- `arrayLength(&x)` 里的 `&` 是“取引用/指针”；很多内建需要传指针（尤其针对 runtime-sized array）。
- compute 中需要跨线程共享中间结果时，用 `var<workgroup>`；只在当前 invocation 内用临时变量时，用函数内 `var` 即可。

### 纹理/采样（决定了你该用 sample 还是 load）

常用类型：

- 可采样 2D：`texture_2d<f32>` + `sampler` → 常用 `textureSample(...)`
- 不可过滤（unfilterable）或需要精确 texel：优先 `textureLoad(...)`（坐标通常是整数 texel + mip）
- 深度：`texture_depth_2d` 往往搭配 `sampler_comparison` 与 `textureSampleCompare(...)`
- Storage texture：`texture_storage_2d<format, access>`（用于读写像素；和采样纹理是两套东西）

自检提示（非常实用）：

- `textureSample` 需要“可过滤/可采样”的纹理格式与匹配的 sampler；如果验证层报“filtering sampler / sampleType 不匹配”，优先回到 bind group layout 检查 sampleType 与 sampler 类型。
- `textureLoad` 是不经过采样器的，常用于 G-buffer、图像处理、unfilterable、storage texture 的读取等场景。

### 纹理家族与查询函数（把“能不能用”一次说清）

常见 sampled textures（配 `sampler`）：

- `texture_1d<f32>`（较少见）
- `texture_2d<f32>` / `texture_2d_array<f32>`
- `texture_3d<f32>`
- `texture_cube<f32>` / `texture_cube_array<f32>`
- `texture_multisampled_2d<f32>`（MSAA color）
- `texture_external`（外部图像源，受限更多）

常见 depth textures（配 `sampler` 或 `sampler_comparison`）：

- `texture_depth_2d` / `texture_depth_2d_array`
- `texture_depth_cube` / `texture_depth_cube_array`
- `texture_depth_multisampled_2d`

常见 storage textures（不配 sampler，直接 load/store）：

- `texture_storage_2d<F, access>` / `texture_storage_2d_array<F, access>`
- `texture_storage_3d<F, access>`

要点：

- storage texture 的读写是“逐 texel”的：用 `textureLoad` / `textureStore`。
- storage texture 通常只作用在 mip level 0（接口上不需要/不支持传 mip level）；不要把 sampled texture 的 `textureLoad(..., level)` 习惯带过来。

高频“查询/辅助”函数（写 shader 时常用来避免硬编码）：

- `textureDimensions(...)`：纹理尺寸（按维度返回 `u32/vec2u/vec3u`，mip 版本也有）
- `textureNumLevels(...)`：mip 层数
- `textureNumLayers(...)`：array layers
- `textureNumSamples(...)`：MSAA sample 数

### 采样函数选择（最常见的正确姿势）

> 关键点：很多采样函数在“非 uniform control flow”里会出问题（见后面的 Uniformity 章节）。

- **最常用**：`textureSample(t, s, coords)`（隐式 LOD，通常依赖导数）
- **显式 LOD**：`textureSampleLevel(t, s, coords, level)`（不计算导数；适合分支里采样）
- **显式导数**：`textureSampleGrad(t, s, coords, dpdx, dpdy)`（自己提供导数）
- **偏置 LOD**：`textureSampleBias(t, s, coords, bias)`（同样可能受 uniformity 约束影响）
- **精确 texel**：
  - sampled/depth：`textureLoad(t, coords, level)`（整数 texel 坐标；MSAA 变体会带 `sample_index`）
  - storage：`textureLoad(t, coords)`（逐 texel 读取，通常只对应 level 0）
- **写入 storage**：`textureStore(t, coords, value)`（storage texture 才能写）

`texture_external` 提示：

- 常用于视频/外部图像源；可用 `textureLoad(texture_external, coords)`。
- 采样时常用 `textureSampleBaseClampToEdge(...)`（用于外部纹理的受限采样场景）。

### 深度/模板（Depth & Stencil）提炼

- 深度“采样”：
  - `textureSample(texture_depth_*, sampler, coords)` 返回 `f32` 深度值
  - 深度“比较采样”：`textureSampleCompare(texture_depth_*, sampler_comparison, coords, depth_ref)` 返回比较结果（`0..1`）
  - 有些场景可用 `textureSampleCompareLevel(..., level=0)`：它不计算导数、且没有 uniform control flow 限制，并且可在任意 stage 调用（适合避开 uniformity 问题）。
- 写 `frag_depth`：
  - fragment 输出 `@builtin(frag_depth) depth: f32` 或直接返回值标注 builtin（取决于你用 struct 还是返回标注）。
- stencil：
  - stencil 更多由**管线状态**控制（compare/op/writeMask 等）；WGSL 侧通常不“读写 stencil 值本身”。

### 宿主侧绑定约束（WebGPU 常见验证错误来源）

- 如果 pipeline 用 `layout: 'auto'`（WebGPU 常见默认），WebGPU 会根据 WGSL 自动推导 bind group layout；这会对纹理的 sampleType、sampler 类型等做出**更严格**的要求。
- 想在多个 pipeline 之间复用同一个 bind group 时，通常需要显式创建并共享同一个 bind group layout / pipeline layout（避免“auto layout 不兼容”）。
- 使用 dynamic offsets 时，需要在 bind group layout 中显式开启对应 binding 的动态偏移能力；否则 `setBindGroup` 传 offsets 会直接报错。

## 📦 数据布局与对齐（uniform/storage 最常见 bug）

- buffer 里的 `struct` / `array` 有**对齐与 size 规则**；CPU 侧写入的 bytes 必须和 WGSL 侧布局一致。
- 高频坑：`vec3<f32>` 的对齐通常是 **16 bytes**，所以它在 struct/array 里经常会产生 padding；“看起来连续”的字段在内存里可能并不连续。
- 这类错误通常**不会报错**，但会让 shader 读到错误数据（表现为模型不见了/数值计算怪异）。
- 实战建议：
  - 不确定布局时，优先用 `vec4f` 对齐，或在 struct 中显式加 padding 字段（例如 `pad0: f32`）。
  - 用工具/计算器自动算 offset/size（避免手算）。


## 🧪 常用骨架（直接改就能用）

### Vertex + Fragment（最小可接入骨架）

```wgsl
struct VSIn {
  @location(0) position: vec3f,
  @location(1) uv: vec2f,
};

struct VSOut {
  @builtin(position) clip_pos: vec4f,
  @location(0) uv: vec2f,
};

@vertex
fn vs_main(v: VSIn) -> VSOut {
  var o: VSOut;
  o.clip_pos = vec4f(v.position, 1.0);
  o.uv = v.uv;
  return o;
}

@group(0) @binding(0) var my_sampler: sampler;
@group(0) @binding(1) var my_tex: texture_2d<f32>;

struct FSOut {
  @location(0) color: vec4f,
};

@fragment
fn fs_main(@location(0) uv: vec2f) -> FSOut {
  var o: FSOut;
  o.color = textureSample(my_tex, my_sampler, uv);
  return o;
}
```

### Compute（最小骨架）

```wgsl
@group(0) @binding(0)
var<storage, read_write> out_data: array<u32>;

@compute @workgroup_size(64)
fn cs_main(@builtin(global_invocation_id) gid: vec3u) {
  let idx = gid.x;
  if (idx < arrayLength(&out_data)) {
    out_data[idx] = idx;
  }
}
```

### Compute 并行模型补充（避免数据竞争）

- 常用 builtins：
  - `@builtin(global_invocation_id)`：全局线程 id（跨工作组唯一）
  - `@builtin(local_invocation_id)`：工作组内线程 id
  - `@builtin(local_invocation_index)`：工作组内线性索引
  - `@builtin(workgroup_id)`：工作组 id
- 写 storage buffer 时默认就有并发写入风险：
  - 每个 invocation 写自己独占的 index（最简单、最安全）
  - 需要汇总/计数时，用 `atomic<T>` 与 `atomicAdd/atomicMin/...`（否则会出现竞态）
  - 需要工作组内共享数据时，用 `var<workgroup>` 并在读写阶段之间插入 `workgroupBarrier()`


## ⚠️ 语法差异与易错点清单（写完逐条对）

- 没有三元运算符：用 `select(falseValue, trueValue, cond)`。
- 控制流不强制括号：`if cond { ... }` 合法（别把括号当成必须）。
- `++`/`--` 是**语句**不是表达式：不能写 `let x = a++;`，只能单独一行 `a++;`。
- `+=`/`-=` 是赋值语句，不是表达式：不能写 `let x = (a += 1);`。
- swizzle 不能出现在赋值左侧：不能写 `color.rgb = ...`，要构造新向量再整体赋值。
- 遇到位移/比较相关解析错误时，优先给子表达式加括号（WGSL 的运算符优先级/解析规则比很多语言更“严格”）。
- `discard` 只能在 fragment shader 使用。
- `switch` 只支持 `i32/u32`，`case` 必须是常量。
- 遇到“某个 binding 不在错误提示里/不被要求”：
  - 检查它是否真的被 entry point 可达代码访问到；必要时 `_ = resource;` 强制标记使用。

## 🧠 Uniformity / Derivatives（很多“能编译但画面怪/不同机器不一致”的根源）

- 导数内建（`dpdx/dpdy/...`）以及依赖导数的操作，在**非 uniform control flow** 下会产生不确定结果（常见表现：验证层报错、或结果 indeterminate）。
- `textureSample*` 里大量变体都会标注 “Returns an indeterminate value if called in non-uniform control flow.”（尤其是隐式 LOD 的那些）。
- 实战策略：
  - 分支里想采样：优先用 `textureSampleLevel`（显式 level）或 `textureLoad`（按 texel）
  - 必须隐式 LOD：把采样挪到分支外，或保证控制流对同一 quad 的 invocations 一致（更难）
  - 深度比较且怕 uniformity：可考虑 `textureSampleCompareLevel`（固定 level=0，不计算导数）

## 🧵 原子与同步（把“高级并行/同步”纳入范围）

WGSL 内建同步函数（来自 WGSL Function Reference）：

- `storageBarrier()`：影响 `storage` 地址空间的内存与 atomic
- `workgroupBarrier()`：影响 `workgroup` 地址空间的内存与 atomic
- `workgroupUniformLoad(ptr<workgroup, T>) -> T`：把 workgroup 内某地址的值“统一广播”为 uniform 值（指针本身必须是 uniform）

原子类型与操作要点：

- 原子类型是 `atomic<T>`（常见 `atomic<u32>` / `atomic<i32>`），用于在多个 invocations 间安全累加/计数/最值等。
- 原子 + barrier 的使用要明确阶段：
  - workgroup 内共享：`var<workgroup>` + `workgroupBarrier()` 做“写完再读”
  - storage 的跨 workgroup 通信非常受限，通常通过原子/分阶段 pass 设计解决（别指望 barrier 让全局有序）

## 🧩 可选特性与 enable（硬切换：不用就不写，用就写全）

- `f16`：
  - WGSL 中 `f16` 是可选能力；如果要用，shader 顶部显式写 `enable f16;`，并且宿主侧必须在创建 device 时请求对应 feature（否则会编译/创建失败）。
- storage texture 的 `bgra8unorm`：
  - `bgra8unorm` 默认不能作为 storage texture；需要宿主请求 WebGPU feature：`bgra8unorm-storage`（详见 Storage Textures 文章）。
- 原则（非常重要）：
  - **不要默认开启**任何可选特性；必须由用户明确要求（或明确说明宿主已启用）。
  - 一旦启用，不做 fallback（hard cutover）。
  - `enable ...;` 放在模块作用域的顶部（在声明/函数之前），并且只写你确实要用的项。
  - 遇到“实验性 enable 名称/feature 名称”不要猜：让用户给出准确字符串，再按其要求写入（并同步更新 Bindings/管线需求）。

## 🔍 可编译自检清单（写完必做）

1. **入口点签名**：`@vertex/@fragment/@compute` 是否齐全？返回值/输出 struct 的 `@location/@builtin` 是否完整？
2. **类型一致性**：所有算术两端类型是否一致？需要时是否做了 `f32(...)` / `u32(...)` 等显式转换？
3. **Bindings 完整**：
   - `@group/@binding` 是否唯一且不冲突？
   - `var<uniform>` / `var<storage, ...>` / `texture_*` / `sampler*` 的类型是否和宿主侧 bind group layout 一致？
4. **纹理函数匹配**：
   - 用了 `textureSample` 的纹理是否“可采样且可过滤”？sampler 类型是否匹配？
   - 用了 `textureLoad` 的坐标/level 类型是否正确（通常是整数 texel + mip）？
5. **数据布局**：uniform/storage 里的 struct 是否考虑了 padding？是否避免了 `vec3f` 带来的隐式 padding 陷阱？
6. **Compute 安全**：
   - 对 output buffer 写入是否做了边界保护（`idx < arrayLength(...)`）？
   - 是否存在多个 invocation 写同一位置？若有，是否使用 atomic 或改写为无冲突写入？

7. **Uniformity**：fragment 中是否在分支/循环里调用了 `dpdx/dpdy/textureSample*` 这类对 uniformity 敏感的函数？能否改成 `textureSampleLevel/textureLoad`？

## ✅ 输出格式（强制）

当使用本 skill 生成 WGSL 时，输出必须包含 3 段：

1. `WGSL`：完整代码块（```wgsl ... ```）
2. `Bindings`：Markdown 表（`group` / `binding` / `kind` / `wgsl type` / `stages` / `note`）
3. `IO`：Markdown 表（`stage` / `location or builtin` / `name` / `type`）
