---
name: ascendc
description: Guides the agent to develop AscendC transformer GMM-style custom ops (such as grouped_matmul_finalize_routing) and their CANN aclnn examples by following existing patterns under ops-transformer/gmm and attention/example_op/examples. Use when adding or modifying these ops, their kernels, tiling/infershape logic, or CANN API examples.
keywords:
    - ascend
    - ascendc
    - kernel
    - npu
    - development
    - 开发环境
    - 算子
    - 昇腾
---
# AscendC Transformer Operator Development

This skill guides the agent to develop/modify AscendC transformer-related operators according to existing patterns, including:

- FFN (Feed Forward Network) operators
- GMM (Grouped Matrix Multiplication) type operators
- MoE (Mixture of Experts) routing operators
  And the corresponding CANN `aclnn_*` example code.

## When to Use

Apply this skill in the following scenarios:

- Need to add or modify FFN (Feed Forward Network) related AscendC operators
- Need to add or modify GMM (Grouped Matrix Multiplication) type AscendC operators
- Need to add or modify MoE (Mixture-of-Experts) routing type AscendC operators
- Need to supplement `op_host` definitions, tiling/infershape logic, or `op_kernel` implementations for existing AscendC operators
- Need to write CANN `aclnn_*` examples similar to `ffn/ffn/examples/test_aclnn_ffn.cpp`
- Need to align, refactor, or bug-fix these operators while maintaining consistency with existing operator styles

---

## Overall Workflow

When users request to develop/modify such operators, follow these steps (order matters):

1. **Locate Reference Operators/Examples**
   - Based on operator type, search in corresponding directories:
     - FFN operators: `ops-transformer/ffn/`
     - GMM operators: `ops-transformer/gmm/`
     - MoE operators: `ops-transformer/moe/`
   - Look for the following file types:
     - `*_def.cpp` (operator definition)
     - `*_tiling*.h/.cpp` (tiling, scheduling logic)
     - `op_kernel/*.h` (AscendC kernel implementation)
   - Find CANN `aclnn_*` examples in the `examples/` subdirectory under the corresponding operator directory, e.g.:
     - FFN: `ffn/ffn/examples/test_aclnn_ffn.cpp`
     - GMM: `gmm/grouped_matmul/examples/`
     - MoE: `moe/moe_init_routing/examples/`
2. **Define Graph operator interface in op_host**
3. **Implement AscendC kernel in op_kernel (including quantization/routing logic)**
4. **Complete/reuse tiling, infershape and registration logic (if relevant files exist)**
5. **Write or update CANN API examples and unit tests**

Subsequent sections will detail what to do in each step and which details to pay attention to.

---

## Step 1: Reuse Existing Patterns

### Required Reading References

- FFN Operator Reference:
  - Graph definition: `ops-transformer/ffn/ffn/op_host/ffn_def.cpp`
  - Tiling implementation: `ops-transformer/ffn/ffn/op_host/ffn_tiling.cpp`
  - CANN API example: `ops-transformer/ffn/ffn/examples/test_aclnn_ffn.cpp`
- GMM Operator Reference:
  - Graph definition: `ops-transformer/gmm/grouped_matmul/op_host/grouped_matmul_def.cpp`
  - AscendC kernel implementation: `ops-transformer/gmm/grouped_matmul/op_kernel/grouped_matmul.h`
- MoE Operator Reference:
  - Graph definition: `ops-transformer/moe/moe_init_routing/op_host/moe_init_routing_def.cpp`
  - CANN API example: `ops-transformer/moe/moe_init_routing/examples/test_aclnn_moe_init_routing.cpp`
- General CANN API Example Reference:
  - `ops-transformer/examples/add_example/examples/test_aclnn_add_example.cpp`
- Type / Format Enum Reference (CANN):
  - 详见本 skill 下的 **references/type_format_reference.md**。
  - Data types: `enum DataType` in `graph/types.h` (e.g. lines 80–123) under CANN install path, such as
    `/usr/local/Ascend/cann-8.5.0-beta.1/aarch64-linux/include/graph/types.h`
  - Tensor formats: `enum Format` in the same `graph/types.h` (e.g. lines 189–247)
  - **op_host 定义约定**：每个输入/输出的 `.DataType({...})`、`.Format({...})`、`.UnknownShapeFormat({...})` 三个列表的**元素个数必须相同**（见 references/type_format_reference.md）。
- **Kernel 开发参考**:
  - 详见本 skill 下的 **references/ascendc_kernel_implement.md**。
  - 提示 CopyIn, Compute, CopyOut 三个阶段的正确写法。以及 TQue, TQue, GlobalTensor 等内存搬运相关类的正确用法。

### References 索引

| 文档 | 说明 |
|------|------|
| references/type_format_reference.md | op_host 类型/格式枚举与定义约定 |
| **references/ascendc_kernel_implement.md** | **Kernel 开发：CopyIn, Compute, CopyOut 等编写引导** |
| references/genop_functionality_index.md | genop 功能索引（如有） |

### Behavioral Guidelines

- **Always copy the skeleton from existing similar operators first, then make minimal necessary modifications**
- Maintain:
  - Naming style (file names, class names, namespaces)
  - Macro usage patterns (`ASCEND_IS_AIC`, `ASCEND_IS_AIV`, etc.)
  - Queue and UB buffer management patterns (`TQue`, `TPipe`)
  - AICore configuration and support for different chips (e.g., `ascend910b` / `ascend910_95`)

---

## Step 2: Define Operator Interface in op_host

### Key Patterns

Inherit from `OpDef`, define the class within the `namespace ops`, and register using `OP_ADD`:

- Inputs:
  - Use `Input("name")` + `.ParamType(REQUIRED/OPTIONAL)`
  - Explicitly define `.DataType({ ... })`, `.Format({ ... })`, and `.UnknownShapeFormat({ ... })`
  - For multi-scenario/multi-type support, list all combinations using vector format
- Outputs:
  - Use `Output("y")`, similarly configure DataType / Format
- Attributes:
  - Use `.Attr("attr_name").AttrType(OPTIONAL/REQUIRED).Int/Float/Bool/ListInt(...)` to set default values
- AICore Configuration:
  - Construct `OpAICoreConfig`, setting:
    - `DynamicCompileStaticFlag(true)`
    - `DynamicFormatFlag(true)`
    - `DynamicRankSupportFlag(true)`
    - `DynamicShapeSupportFlag(true)`
    - `NeedCheckSupportFlag(false)` (if reference operators do so)
    - Necessary `ExtendCfgInfo(...)`, e.g., `"softsync.flag"`, `"prebuildPattern.value"`, `"coreType.value"`, `"aclnnSupport.value"`
  - Call `this->AICore().AddConfig("ascend910b", config);` etc. based on chip model
- Register at the end with `OP_ADD(YourOpClassName);`

### Operator-Specific Examples

#### FFN Operator (Refer to `ffn_def.cpp`)

The FFN operator supports Feed Forward Network computation with optional activation functions:

cpp

```
// Input definitions
Input("x")
    .ParamType(REQUIRED)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT8})
    .Format({FORMAT_ND});
Input("weight1")
    .ParamType(REQUIRED)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT8})
    .Format({FORMAT_ND});
Input("weight2")
    .ParamType(REQUIRED)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT8})
    .Format({FORMAT_ND});
Input("bias1")
    .ParamType(OPTIONAL)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT32})
    .Format({FORMAT_ND});
// Output definitions
Output("y")
    .DataType({DT_FLOAT16, DT_BF16, DT_INT8})
    .Format({FORMAT_ND});

// Attribute definitions
Attr("activation").AttrType(OPTIONAL).Int({0}); // 0: GELU, 1: RELU, 2: FASTGELU, 3: SILU, 4: SIGMOID, 5: TANH
Attr("inner_precise").AttrType(OPTIONAL).Int({0}); // 0: BF16, 1: FLOAT32
```

#### GMM Operator (Refer to `grouped_matmul_def.cpp`)

The GMM operator supports grouped matrix multiplication with configurable grouping and data types:

cpp

```
// Input definitions
Input("x")
    .ParamType(REQUIRED)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT8})
    .Format({FORMAT_ND});
Input("weight")
    .ParamType(REQUIRED)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT8})
    .Format({FORMAT_ND});
Input("bias")
    .ParamType(OPTIONAL)
    .DataType({DT_FLOAT16, DT_BF16, DT_INT32})
    .Format({FORMAT_ND});

// Output definitions
Output("y")
    .DataType({DT_FLOAT16, DT_BF16, DT_INT32, DT_INT8})
    .Format({FORMAT_ND});

// Attribute definitions
Attr("split_item").AttrType(OPTIONAL).ListInt({}); // Grouping information
Attr("dtype").AttrType(OPTIONAL).Int({0}); // 0: FLOAT16, 1: BF16, 2: INT8
Attr("transpose_weight").AttrType(OPTIONAL).Int({0}); // 0: No transpose, 1: Transpose
```

#### MoE Operator (Refer to `moe_init_routing_def.cpp`)

The MoE operator supports Mixture-of-Experts routing logic:

cpp

```
// Input definitions
Input("x")
    .ParamType(REQUIRED)
    .DataType({DT_FLOAT16, DT_BF16})
    .Format({FORMAT_ND});
Input("rowIdx")
    .ParamType(REQUIRED)
    .DataType({DT_INT32})
    .Format({FORMAT_ND});
Input("expertIdx")
    .ParamType(REQUIRED)
    .DataType({DT_INT32})
    .Format({FORMAT_ND});

// Output definitions
Output("expandedXOut")
    .DataType({DT_FLOAT16, DT_BF16})
    .Format({FORMAT_ND});
Output("expandedRowIdx")
    .DataType({DT_INT32})
    .Format({FORMAT_ND});
Output("expandedExpertIdx")
    .DataType({DT_INT32})
    .Format({FORMAT_ND});

// Attribute definitions
Attr("activeNum").AttrType(OPTIONAL).Int({0}); // Number of active experts
```

### Agent Key Points

- When creating new operators:
  - **Completely copy the class declaration and constructor body from reference operators**, then only modify:
    - Class name / file name
    - Input/output names and counts
    - Supported `DataType` / `Format`
    - Specific attributes and default values
  - Unless there are special reasons, do not arbitrarily change the AICore flags and `ExtendCfgInfo` structure from reference operators
- If `aclnn` support is needed:
  - Follow the `"aclnnSupport.value", "support_aclnn"` configuration in reference operators

---

## Step 3: Implement AscendC Kernel in op_kernel

### Common Characteristics

- Use the same namespace as the operator (e.g., `namespace FFN`, `namespace GroupedMatmul`, `namespace MoeInitRouting`)
- Include necessary headers:
  - `kernel_operator.h`
  - `lib/matmul_intf.h` (for matrix multiplication related operators)
  - Your own utility headers (e.g., `ffn_utils.h`, `grouped_matmul_utils.h`)
- Define type aliases:
  - `using aT = MatmulType<...>;`
  - `using bT = MatmulType<...>;`
  - `using BiasT = ...;`
  - `using cT = ...;`
  - `using MT = matmul::MatmulImpl<aT, bT, cT, BiasT, CFG_MDL>;`
- Use template parameters to control different scenarios (data types, quantization modes, activation functions, etc.)

### Operator-Specific Implementations

#### FFN Operator Implementation

The FFN operator implements Feed Forward Network computation, containing two linear transformations and an activation function:

cpp

```
namespace FFN {

// Define activation type enum
enum ActiveType {
    ACTIVE_GELU = 0,
    ACTIVE_RELU = 1,
    ACTIVE_FASTGELU = 2,
    ACTIVE_SILU = 3,
    ACTIVE_SIGMOID = 4,
    ACTIVE_TANH = 5
};

// Define parameter structure
template <typename T, ActiveType ACTIVE, bool WITH_BIAS>
struct Param {
    using InputType = T;
    using OutputType = T;
    static constexpr ActiveType kActive = ACTIVE;
    static constexpr bool kWithBias = WITH_BIAS;
};

// Main computation class
template <class P> class FfnCompute {
public:
    using InputType = typename P::InputType;
    using OutputType = typename P::OutputType;

    // Initialization function
    void Init(const InitParams &initParams, const FFNTiling *tiling) {
        // Initialize global tensors, UB buffer, queues, etc.
    }

    // Processing function
    void Process() {
        // First linear transformation: x * weight1 + bias1
        // Apply activation function
        // Second linear transformation: (x * weight1 + bias1) * weight2 + bias2
        // Write back results
    }

private:
    // Implement activation function
    void ApplyActivation(InputType *src, OutputType *dst, uint32_t size) {
        switch (P::kActive) {
            case ACTIVE_GELU:
                // Implement GELU activation
                break;
            case ACTIVE_FASTGELU:
                // Implement FASTGELU activation
                break;
            // Other activation function implementations
        }
    }
};

} // namespace FFN
```

#### GMM Operator Implementation

The GMM operator implements grouped matrix multiplication:

cpp

```
namespace GroupedMatmul {

// Define parameter structure
template <typename T, typename WeightT, typename BiasT, typename OutputT>
struct Param {
    using InputType = T;
    using WeightType = WeightT;
    using BiasType = BiasT;
    using OutputType = OutputT;
};

// Main computation class
template <class P> class GroupedMatmulCompute {
public:
    using InputType = typename P::InputType;
    using WeightType = typename P::WeightType;
    using BiasType = typename P::BiasType;
    using OutputType = typename P::OutputType;

    // Initialization function
    void Init(const InitParams &initParams, const GroupedMatmulTiling *tiling) {
        // Initialize global tensors, grouping information, UB buffer, queues, etc.
    }

    // Processing function
    void Process() {
        // Loop through each group
        for (uint32_t groupIdx = 0; groupIdx < tiling_->groupNum; ++groupIdx) {
            // Compute matrix multiplication for current group
            ComputeGroup(groupIdx);
        }
    }

private:
    // Group computation function
    void ComputeGroup(uint32_t groupIdx) {
        // Set input, weight, output offsets for current group
        // Execute matrix multiplication
        // Add bias (if any)
        // Write back current group results
    }
};

} // namespace GroupedMatmul
```

#### MoE Operator Implementation

The MoE operator implements Mixture-of-Experts routing logic:

cpp

```
namespace MoeInitRouting {

// Define parameter structure
template <typename T, typename IndexT>
struct Param {
    using InputType = T;
    using IndexType = IndexT;
};

// Main computation class
template <class P> class MoeInitRoutingCompute {
public:
    using InputType = typename P::InputType;
    using IndexType = typename P::IndexType;

    // Initialization function
    void Init(const InitParams &initParams, const MoeInitRoutingTiling *tiling) {
        // Initialize global tensors, UB buffer, queues, etc.
    }

    // Processing function
    void Process() {
        // Process routing logic
        // Expand input x based on rowIdx and expertIdx
        // Generate expanded rowIdx and expertIdx
        // Write back results
    }

private:
    // Expand input tensor
    void ExpandInput(const InputType *x, IndexType *rowIdx, IndexType *expertIdx,
                    InputType *expandedX, IndexType *expandedRowIdx, IndexType *expandedExpertIdx) {
        // Implement expansion logic
    }
};

} // namespace MoeInitRouting
```

### Typical Structure (Reference Only, Don't Memorize Rigidly)

- Utility functions:
  - e.g., `DataCopyPad2D`, with two GM↔UB overloads, carrying `DataCopy2DDimParams`
- Main class:
  - Contains `Init(...)` method: initializes global tensors, UB buffer, queues, etc.
  - Contains `Process()` method: overall execution flow, including computation logic and result writing
  - Contains private helper methods: implements specific computation logic (e.g., activation functions, group processing)
  - If new operator logic is similar, **try to reuse this entire structure as much as possible, making only necessary changes**

### Agent Key Points

- When creating new operators/variants:
  - First confirm:
    - Whether it's still based on `MatmulImpl`, and which GM tensors are needed
    - Which fields are in the tiling structure (e.g., `matmulTiling.baseM/baseN/k`, `groupNum`, etc.)
  - Modify only:
    - Add/remove GM inputs (e.g., additional scale/bias/logits)
    - Adjust tensor combinations used in `ComputeDequantAndActivate` / `PerTokenScaleBrcb`, etc.
    - Modify business-logic-specific initialization in `InitOutputWithZeros`, `PreProcess`
  - Maintain:
    - Patterns for queue/UB allocation, `PipeBarrier`, `DataCopyPad`, `SetAtomicAdd` - do not change these unless there are clear bugs or requirements

---

## Step 4: Tiling / Infershape / Other Host Logic

Although this skill example doesn't expand all files, the agent should follow these patterns in the codebase:

1. Search under `op_host/` for:
   - `*_tiling*.h/.cpp`
   - `*_infershape.cpp`
   - Other `${op_name}_*.cpp` files
2. Analyze in reference operators:
   - Tiling parameters (batch, M/N/K, group count, deterministic flag, etc.)
   - How to convert Graph-level shape/attr to the `tiling` structure needed by kernel
3. When creating new operators:
   - If semantics are similar, prioritize copying reference tiling/infershape code, then rename and modify fields
   - Ensure:
     - Graph attributes/shapes correctly map to `tiling->...` fields accessed in kernel
     - Deterministic switches, workspace size, coreNum/parallNum calculation logic maintain consistent style

### 4.1 使用 JSON + `graph/types.h` 驱动 op_host/op_kernel 对齐（通用流程）

在很多自定义算子工程中，会存在一个用于描述算子接口的 JSON（例如 `moe_init_routing_grouped_matmul_grad.json`），其中列出每个输入/输出的:

- name（张量名称）
- param_type（required / optional）
- type（如 `fp16` / `bf16` / `float` / `int32`）
- format（如 `ND`）

为了保证 `op_host` / `infershape` / `tiling` / `op_kernel` 一致，建议按如下通用步骤处理：

1. **从 JSON 提取接口信息**
   - 读取 JSON 中的:
     - `input_desc[i].name` / `output_desc[j].name`
     - `input_desc[i].type` / `output_desc[j].type`
     - `input_desc[i].format` / `output_desc[j].format`
   - 明确哪些张量是数据（`fp16`/`bf16`/`float` 等），哪些是索引/标量（`int32` 等）。

2. **在 `op_host/*_def.cpp` 中映射 DataType / Format**
   - DataType 必须使用 `ge::DataType` 枚举，参考 CANN 头文件:
     - `ge::DT_FLOAT16`, `ge::DT_BF16`, `ge::DT_FLOAT`, `ge::DT_INT32`, ...
       这些可以在 `graph/types.h` 的 `enum DataType` 中找到（如 \(L80\text{-}L123\)）。
   - Format 必须使用 `ge::Format` 枚举，参考:
     - `ge::FORMAT_ND`, `ge::FORMAT_NCHW`, `ge::FORMAT_NHWC`, ...
       这些可以在 `graph/types.h` 的 `enum Format` 中找到（如 \(L189\text{-}L247\)）。
   - 通用映射示例（JSON → C++）:
     - `type: "fp16"` → `ge::DT_FLOAT16`
     - `type: "bf16"` → `ge::DT_BF16`
     - `type: "float"` → `ge::DT_FLOAT`
     - `type: "int32"` → `ge::DT_INT32`
     - `format: "ND"` → `ge::FORMAT_ND`
   - 在 `Input("xxx")` / `Output("yyy")` 中：
     - `.DataType({ ... })` 的内容严格来源于 JSON 中的 `type` 列表（按需求去重即可）。
     - `.Format({ ... })` / `.UnknownShapeFormat({ ... })` 一般与 JSON 的 `format` 对齐（多数场景直接用 `FORMAT_ND`）。

3. **在 infershape 中对齐 shape 关系**
   - 使用 JSON 中的语义决定输出 shape 与哪个输入 shape 对齐，例如：
     - 梯度算子中 `grad_x` 通常与其对应前向输入 `x` 同 shape；
     - `grad_weight` 与 `weight` 同 shape。
   - 在 `*_infershape.cpp` 中：
     - 通过 `context->GetInputShape(index)` / `GetOutputShape(index)` 获取形状。
     - 明确索引常量（如 `IDX_EXPANDED_X`, `IDX_WEIGHT`, `IDX_GRAD_X`, `IDX_GRAD_WEIGHT`），并保持与 JSON / `op_host` 输入输出顺序一致。
     - 遍历维度拷贝：`SetDimNum` + `SetDim(i, ...)`，逻辑上保证“谁等于谁”与 JSON 的设计一致。

4. **在 tiling 中使用 JSON + types.h 做一致性校验**
   - 从 `TilingContext` 中获取某个关键输入（通常是主数据张量，如 `x` 或 `expanded_x`）的 shape 与 dtype：
     - 使用 `context->GetInputShape(idx)->GetStorageShape()` 作为 tiling 参考 shape。
     - 使用 `context->GetInputDesc(idx)->GetDataType()` 获取真实 dtype。
   - 根据 JSON 中的 `type` 列表构造支持集合，例如：
     - 若 JSON 仅包含 `["fp16","bf16","float"]`，则 tiling 中应只允许：
       `const std::set<ge::DataType> supportedDtype = {ge::DT_FLOAT16, ge::DT_BF16, ge::DT_FLOAT};`
   - shape 维度约束（如必须是 4D）应与内核实现的假设一致：
     - 检查 `GetDimNum()`，不符则返回 `GRAPH_FAILED` 并打印清晰错误。
     - 将关键维度（如 N/C/H/W）记录到 tiling 结构，供 AscendC kernel 使用。

5. **在 op_kernel 中保持命名与接口一致**
   - tiling 结构体（如 `CustomOpTilingData`）的字段命名，应能从 JSON / 算子语义直接对应过来，例如 `totalLength`, `tileNum`。
   - AscendC kernel 中的 GM tensor 命名（如 `gmExpandedX`, `gmWeight`, `gmGradY`, `gmGradX`, `gmGradWeight`）建议与 JSON 的 `name` 一致或做简单可读映射，避免 “x1/x2/y” 这种含义不清的名称。

6. **通用注意事项**
   - **不要手写随意的 DataType / Format 枚举值**，优先从 `graph/types.h` 中查找并复制，确保与当前 CANN 版本兼容。
   - 当 JSON 中出现新类型（例如 `int8`、`bool`、`float8` 等）时：
     - 先在 `graph/types.h` 中确认是否存在对应的 `ge::DT_*`；
     - 确认算子语义与内核实现是否真的支持该类型，再加入 `DataType` 列表和 tiling 校验。
   - 若 JSON 与现有 `op_host` / `infershape` / `tiling` 存在冲突，以**内核实现能力为上限**，在此基础上尽量向 JSON 靠拢，并在注释中标明差异原因。

---

## Step 5: CANN aclnn Examples (examples)

Refer to `test_aclnn_example_op.cpp`, the pattern is as follows:

1. **Common Utility Functions**
   - `GetShapeSize`: calculates product of shape dimensions
   - `PrintOutResult<T>`: copies device results back to host and prints
   - `Init(deviceId, &stream)`:
     - `aclInit`
     - `aclrtSetDevice`
     - `aclrtCreateStream`
   - `CreateAclTensor<T>`:
     - Use `aclrtMalloc` to allocate device memory
     - `aclrtMemcpy` to copy from host to device
     - Calculate `strides` for contiguous tensors
     - Call `aclCreateTensor` to create `aclTensor*`
2. **Main() Workflow**
   - Initialize ACL runtime
   - For each input/output construct:
     - Host-side data (`std::vector<T>`)
     - Corresponding shape (`std::vector<int64_t>`)
     - Call `CreateAclTensor(...)` to create `aclTensor*` and device addr
   - Get workspace size and executor:
     - Call `aclnnYourOpGetWorkspaceSize(...)`
   - If `workspaceSize > 0`:
     - `aclrtMalloc` to allocate workspace
   - Call actual operator:
     - `aclnnYourOp(workspaceAddr, workspaceSize, executor, stream);`
   - `aclrtSynchronizeStream(stream);`
   - Copy back output and call `PrintOutResult` to print results
   - Destroy tensors, free device memory, destroy stream, reset device, `aclFinalize`

### Agent Key Points

- When creating new `aclnn_*` examples:
  - **Completely copy the structure of `test_aclnn_example_op.cpp`**, then modify:
    - Header includes (`aclnnop/aclnn_xxx.h`)
    - Number of tensors, shapes, dtypes, and fill data
    - Function names and parameter lists for `aclnnXxxGetWorkspaceSize` / `aclnnXxx`
  - Maintain:
    - Error checking macros (`CHECK_RET`) and logging output macros
    - Paired allocation/release of all `acl*` resources

---

## Step 6: Testing and Verification (If Python Frontend Exists)

If Python tests exist in the project (e.g., `op-plugin/test/test_custom_ops/test_*.py`):

1. Use existing test files as templates:
   - Usually named `test_npu_<op_name>_*.py`
   - Use NPU device, call op encapsulated by frontend API
2. When creating new operators:
   - Construct typical input shapes (including boundary scenarios)
   - If there's a comparable reference implementation (e.g., CPU version or simple Python algorithm), use it to calculate expected outputs
   - Assert:
     - Shape and dtype are correct
     - Numerical errors are within reasonable range (especially in quantization/dequantization scenarios)

---

## Additional Constraints for the Agent

- **Don't lazily invent patterns from scratch**: Always first search and align with implementations and examples of adjacent operators
- Before modifying any existing file:
  - Read the entire file first to understand its role in the overall operator
- For logic involving chip support / dynamic shapes / deterministic behavior:
  - Prioritize maintaining consistency with existing operators, unless bugs or requirements demand changes
- For examples and tests:
  - Better to have small, clear examples (single shape, easy to manually verify) rather than complex scenarios from the beginning

---

## Brief Usage Example

- **User**: Add a new GMM routing operator similar to `grouped_matmul_finalize_routing`, but with different scale/bias combinations
- **Agent Behavior (following this skill)**:
  1. Find and read `grouped_matmul_finalize_routing_*` related files in the `gmm` directory
  2. Copy `*_def.cpp`, rename and modify interface, adjust inputs/attributes
  3. Copy the core class from `op_kernel/grouped_matmul_finalize_routing.h`, adjust GM tensors and dequantization flow according to new requirements
  4. Refer to related tiling/infershape files to ensure correct parameter mapping from Graph to kernel
  5. Refer to `test_aclnn_example_op.cpp` to write a new `aclnn` example, and supplement unit tests if needed

---

## Operator Project Generation (genop)

### Overview

The `genop` functionality is a tool provided in the `ops-transformer` project that allows users to quickly create the initial directory structure for a new operator. It uses a template-based approach to generate all the necessary files and directories for a new operator project.

### How to Use genop

To create a new operator project, use the following command in the `ops-transformer` directory:

```bash
bash build.sh --genop=op_class/op_name
```

Where:
- `op_class` is the category of the operator (e.g., `gmm`, `moe`, `ffn`)
- `op_name` is the name of the new operator (e.g., `my_custom_op`)

### Example Usage

```bash
bash build.sh --genop=gmm/my_custom_gmm_op
```

This command will create a new directory structure under `gmm/my_custom_gmm_op` with all the necessary files for a new GMM operator.

### What genop Generates

The `genop` tool generates the following structure for a new operator:

1. **Directory Structure**:
   - `op_host/`: Contains operator definition, tiling, and infershape logic
   - `op_kernel/`: Contains AscendC kernel implementation
   - `examples/`: Contains CANN API usage examples
   - `CMakeLists.txt`: Build configuration for the operator

2. **Key Files**:
   - `op_host/*_def.cpp`: Operator definition with input/output/attribute declarations
   - `op_host/*_tiling.cpp`: Tiling and scheduling logic
   - `op_kernel/*.h`: AscendC kernel implementation
   - `examples/test_aclnn_*.cpp`: CANN API usage example

### Customization After Generation

After generating the operator project with `genop`, you need to:

1. **Modify the operator definition** in `op_host/*_def.cpp`:
   - Update input/output parameters and data types
   - Adjust attributes and their default values
   - Configure AICore settings if needed

2. **Implement the kernel logic** in `op_kernel/*.h`:
   - Add the actual computation logic
   - Handle different data types and quantization modes
   - Optimize for performance

3. **Update tiling logic** in `op_host/*_tiling.cpp`:
   - Adjust tiling parameters for optimal performance
   - Handle different input shapes and configurations

4. **Write or update examples** in `examples/`:
   - Create test cases for the new operator
   - Verify functionality with different input shapes

### Benefits of Using genop

- **Saves time**: Automatically creates the entire directory structure and boilerplate code
- **Ensures consistency**: Follows the same patterns as existing operators
- **Reduces errors**: Minimizes manual errors when setting up a new operator project
- **Simplifies onboarding**: Makes it easier for new developers to create operators

---

## Generic Operator Example Generation

### Overview

This section provides a general guide for generating CANN `aclnn_*` examples for any AscendC operator, including how to automatically extract operator information from `op_host` or `op_kernel` files to create accurate example code.

### How to Generate Generic Operator Examples

#### Step 1: Locate Operator Definition Files

1. **Find op_host files**: Look for `*_def.cpp` or similar files in the `op_host` directory of the operator.
2. **Find op_kernel files**: Look for implementation files in the `op_kernel` directory.
3. **Extract operator information**: From these files, extract:
   - Input parameters (names, data types, shapes)
   - Output parameters (names, data types, shapes)
   - Attribute parameters (names, types, default values)
   - Supported data types and formats

#### Step 2: Generate Example Code Structure

Use the following template to structure your example code:

```cpp
#include "acl/acl.h"
#include "aclnnop/aclnn_[operator_name].h"
#include <iostream>
#include <vector>

// Define data types based on operator requirements
#define Kernel_dtype [appropriate_data_type]
#define Acl_dtpe [corresponding_acl_data_type]

// Error checking and logging macros
#define CHECK_RET(cond, return_expr)                                           \
  do {                                                                         \
    if (!(cond)) {                                                             \
      return_expr;                                                             \
    }                                                                          \
  } while (0)

#define LOG_PRINT(message, ...)                                                \
  do {                                                                         \
    printf(message, ##__VA_ARGS__);                                            \
  } while (0)

// Utility functions
int64_t GetShapeSize(const std::vector<int64_t> &shape) {
  int64_t shapeSize = 1;
  for (auto i : shape) {
    shapeSize *= i;
  }
  return shapeSize;
}

template <typename T>
void PrintOutResult(std::vector<int64_t> &shape, void **deviceAddr) {
  auto size = GetShapeSize(shape);
  std::vector<T> resultData(size, 0);

  auto ret = aclrtMemcpy(
      resultData.data(), resultData.size() * sizeof(T), *deviceAddr,
      size * sizeof(T), ACL_MEMCPY_DEVICE_TO_HOST);
  CHECK_RET(
      ret == ACL_SUCCESS,
      LOG_PRINT("copy result from device to host failed. ERROR: %d\n", ret);
      return);
  for (int64_t i = 0; i < size; i++) {
    LOG_PRINT("idx[%ld] (offset: %ld Bytes) : %f\n", i, i * sizeof(T), resultData[i]);
  }
}

int Init(int32_t deviceId, aclrtStream *stream) {
  auto ret = aclInit(nullptr);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclInit failed. ERROR: %d\n", ret); return ret);
  ret = aclrtSetDevice(deviceId);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtSetDevice failed. ERROR: %d\n", ret); return ret);
  ret = aclrtCreateStream(stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtCreateStream failed. ERROR: %d\n", ret); return ret);
  return 0;
}

template <typename T>
int CreateAclTensor(const std::vector<T> &hostData,
                    const std::vector<int64_t> &shape, void **deviceAddr,
                    aclDataType dataType, aclTensor **tensor) {
  auto size = GetShapeSize(shape) * sizeof(T);
  auto ret = aclrtMalloc(deviceAddr, size, ACL_MEM_MALLOC_HUGE_FIRST);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclrtMalloc failed. ERROR: %d\n", ret);
            return ret);
  ret = aclrtMemcpy(*deviceAddr, size, hostData.data(), size,
                    ACL_MEMCPY_HOST_TO_DEVICE);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclrtMemcpy failed. ERROR: %d\n", ret);
            return ret);

  std::vector<int64_t> strides(shape.size(), 1);
  for (int64_t i = shape.size() - 2; i >= 0; i--) {
    strides[i] = shape[i + 1] * strides[i + 1];
  }

  *tensor = aclCreateTensor(shape.data(), shape.size(), dataType,
                            strides.data(), 0, aclFormat::ACL_FORMAT_ND,
                            shape.data(), shape.size(), *deviceAddr);
  return 0;
}

int main() {
  // 1. Initialize ACL
  int32_t deviceId = 0;
  aclrtStream stream;
  auto ret = Init(deviceId, &stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("Init acl failed. ERROR: %d\n", ret); return ret);

  // 2. Construct inputs (based on operator definition)
  // [Input tensor declarations and initializations]

  // 3. Construct outputs (based on operator definition)
  // [Output tensor declarations and initializations]

  // 4. Get workspace size and executor
  uint64_t workspaceSize = 0;
  aclOpExecutor *executor;
  ret = aclnn[OperatorName]GetWorkspaceSize([input_tensors], [output_tensors], &workspaceSize, &executor);
  CHECK_RET(
      ret == ACL_SUCCESS,
      LOG_PRINT("aclnn[OperatorName]GetWorkspaceSize failed. ERROR: %d\n", ret);
      return ret);

  // 5. Allocate workspace if needed
  void *workspaceAddr = nullptr;
  if (workspaceSize > static_cast<uint64_t>(0)) {
    std::cout << "workspaceSize: " << workspaceSize << " bytes" << std::endl;
    ret = aclrtMalloc(&workspaceAddr, workspaceSize, ACL_MEM_MALLOC_HUGE_FIRST);
    CHECK_RET(ret == ACL_SUCCESS,
              LOG_PRINT("allocate workspace failed. ERROR: %d\n", ret);
              return ret);
  }

  // 6. Execute the operator
  ret = aclnn[OperatorName](workspaceAddr, workspaceSize, executor, stream);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclnn[OperatorName] failed. ERROR: %d\n", ret);
            return ret);

  // 7. Synchronize stream
  ret = aclrtSynchronizeStream(stream);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclrtSynchronizeStream failed. ERROR: %d\n", ret);
            return ret);

  // 8. Print results
  // [Print output tensors]

  // 9. Clean up resources
  // [Destroy tensors and free memory]

  aclrtDestroyStream(stream);
  aclrtResetDevice(deviceId);
  aclFinalize();

  return 0;
}
```

#### Step 3: Extract Operator Information

To automatically generate accurate examples, follow these steps to extract information from operator definition files:

1. **From op_host files**:
   - Look for `Input("name")` and `Output("name")` declarations
   - Extract data types from `.DataType({...})`
   - Extract formats from `.Format({...})`
   - Extract attributes from `.Attr("name")`

2. **From op_kernel files**:
   - Look for parameter structures and data types
   - Extract computation logic to understand input/output relationships
   - Identify any special handling or requirements

#### Step 4: Customize Example for Specific Operator

Using the extracted information, customize the template by:

1. **Updating includes**: Change `aclnnop/aclnn_[operator_name].h` to the correct header
2. **Setting data types**: Adjust `Kernel_dtype` and `Acl_dtpe` based on supported types
3. **Defining input tensors**: Create tensors for each input parameter
4. **Defining output tensors**: Create tensors for each output parameter
5. **Calling the API**: Update the function names and parameter lists
6. **Printing results**: Add code to print output tensors
7. **Cleaning up**: Ensure all resources are properly released

### Example: moe_init_routing_grouped_matmul_grad

#### Overview

The `moe_init_routing_grouped_matmul_grad` operator is a specialized AscendC operator for Mixture-of-Experts (MoE) models, designed to compute gradients for the routing and grouped matrix multiplication operations in the backward pass.

#### Implementation Principle

This operator performs the following key computations:

1. **Gradient Propagation**: Computes gradients with respect to the input tensor(s) and weight matrix based on the gradient of the output.
2. **Grouped Matrix Multiplication**: Efficiently handles grouped matrix operations to support expert-specific computations.
3. **Routing Gradient Handling**: Uses routing indices to properly aggregate gradients back to the original input space.

#### Generated Example Code

```cpp
#include "acl/acl.h"
#include "aclnnop/aclnn_[operator_name].h"
#include <iostream>
#include <vector>

```#define Kernel_dtype float
#define Acl_dtpe aclDataType::ACL_FLOAT
#define Index_dtype int32_t
#define Acl_index_dtpe aclDataType::ACL_INT32

#define CHECK_RET(cond, return_expr)                                           \
  do {                                                                         \
    if (!(cond)) {                                                             \
      return_expr;                                                             \
    }                                                                          \
  } while (0)

#define LOG_PRINT(message, ...)                                                \
  do {                                                                         \
    printf(message, ##__VA_ARGS__);                                            \
  } while (0)

int64_t GetShapeSize(const std::vector<int64_t> &shape) {
  int64_t shapeSize = 1;
  for (auto i : shape) {
    shapeSize *= i;
  }
  return shapeSize;
}

template <typename T>
void PrintOutResult(std::vector<int64_t> &shape, void **deviceAddr) {
  auto size = GetShapeSize(shape);
  std::vector<T> resultData(size, 0);

  auto ret = aclrtMemcpy(
      resultData.data(), resultData.size() * sizeof(T), *deviceAddr,
      size * sizeof(T), ACL_MEMCPY_DEVICE_TO_HOST);
  CHECK_RET(
      ret == ACL_SUCCESS,
      LOG_PRINT("copy result from device to host failed. ERROR: %d\n", ret);
      return);
  for (int64_t i = 0; i < size; i++) {
    LOG_PRINT("idx[%ld] (offset: %ld Bytes) : %f\n", i, i * sizeof(T), resultData[i]);
  }
}

int Init(int32_t deviceId, aclrtStream *stream) {
  auto ret = aclInit(nullptr);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclInit failed. ERROR: %d\n", ret); return ret);
  ret = aclrtSetDevice(deviceId);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtSetDevice failed. ERROR: %d\n", ret); return ret);
  ret = aclrtCreateStream(stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("aclrtCreateStream failed. ERROR: %d\n", ret); return ret);
  return 0;
}

template <typename T>
int CreateAclTensor(const std::vector<T> &hostData,
                    const std::vector<int64_t> &shape, void **deviceAddr,
                    aclDataType dataType, aclTensor **tensor) {
  auto size = GetShapeSize(shape) * sizeof(T);
  auto ret = aclrtMalloc(deviceAddr, size, ACL_MEM_MALLOC_HUGE_FIRST);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclrtMalloc failed. ERROR: %d\n", ret);
            return ret);
  ret = aclrtMemcpy(*deviceAddr, size, hostData.data(), size,
                    ACL_MEMCPY_HOST_TO_DEVICE);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclrtMemcpy failed. ERROR: %d\n", ret);
            return ret);

  std::vector<int64_t> strides(shape.size(), 1);
  for (int64_t i = shape.size() - 2; i >= 0; i--) {
    strides[i] = shape[i + 1] * strides[i + 1];
  }

  *tensor = aclCreateTensor(shape.data(), shape.size(), dataType,
                            strides.data(), 0, aclFormat::ACL_FORMAT_ND,
                            shape.data(), shape.size(), *deviceAddr);
  return 0;
}

int main() {
  // 1. Initialize ACL
  int32_t deviceId = 0;
  aclrtStream stream;
  auto ret = Init(deviceId, &stream);
  CHECK_RET(ret == ACL_SUCCESS, LOG_PRINT("Init acl failed. ERROR: %d\n", ret); return ret);

  // 2. Construct inputs (based on operator definition)
  // Input 1: input_tensor_1
  aclTensor *inputTensor1 = nullptr;
  void *inputTensor1DeviceAddr = nullptr;
  std::vector<int64_t> inputTensor1Shape = {1, 1, 1, 1}; // FILL IN actual shape
  std::cout << "inputTensor1Shape: ";
  for (size_t i = 0; i < inputTensor1Shape.size(); i++) {
    std::cout << inputTensor1Shape[i] << " ";
  }
  std::cout << std::endl;
  std::vector<Kernel_dtype> inputTensor1HostData(GetShapeSize(inputTensor1Shape), 0.0f);
  // FILL IN actual data
  ret = CreateAclTensor(inputTensor1HostData, inputTensor1Shape, &inputTensor1DeviceAddr, Acl_dtpe, &inputTensor1);
  CHECK_RET(ret == ACL_SUCCESS, return ret);

  // Input 2: input_tensor_2
  aclTensor *inputTensor2 = nullptr;
  void *inputTensor2DeviceAddr = nullptr;
  std::vector<int64_t> inputTensor2Shape = {1, 1, 1, 1}; // FILL IN actual shape
  std::cout << "inputTensor2Shape: ";
  for (size_t i = 0; i < inputTensor2Shape.size(); i++) {
    std::cout << inputTensor2Shape[i] << " ";
  }
  std::cout << std::endl;
  std::vector<Kernel_dtype> inputTensor2HostData(GetShapeSize(inputTensor2Shape), 0.0f);
  // FILL IN actual data
  ret = CreateAclTensor(inputTensor2HostData, inputTensor2Shape, &inputTensor2DeviceAddr, Acl_dtpe, &inputTensor2);
  CHECK_RET(ret == ACL_SUCCESS, return ret);

  // Add more inputs as needed

  // 3. Construct outputs (based on operator definition)
  // Output 1: output_tensor_1
  aclTensor *outputTensor1 = nullptr;
  void *outputTensor1DeviceAddr = nullptr;
  std::vector<int64_t> outputTensor1Shape = {1, 1, 1, 1}; // FILL IN actual shape
  std::cout << "outputTensor1Shape: ";
  for (size_t i = 0; i < outputTensor1Shape.size(); i++) {
    std::cout << outputTensor1Shape[i] << " ";
  }
  std::cout << std::endl;
  std::vector<Kernel_dtype> outputTensor1HostData(GetShapeSize(outputTensor1Shape), 0.0f);
  ret = CreateAclTensor(outputTensor1HostData, outputTensor1Shape, &outputTensor1DeviceAddr, Acl_dtpe, &outputTensor1);
  CHECK_RET(ret == ACL_SUCCESS, return ret);

  // Add more outputs as needed

  // 4. Get workspace size and executor
  uint64_t workspaceSize = 0;
  aclOpExecutor *executor;
  ret = aclnn[OperatorName]GetWorkspaceSize([input_tensors], [output_tensors], &workspaceSize, &executor);
  CHECK_RET(
      ret == ACL_SUCCESS,
      LOG_PRINT("aclnn[OperatorName]GetWorkspaceSize failed. ERROR: %d\n", ret);
      return ret);

  // 5. Allocate workspace if needed
  void *workspaceAddr = nullptr;
  if (workspaceSize > static_cast<uint64_t>(0)) {
    std::cout << "workspaceSize: " << workspaceSize << " bytes" << std::endl;
    ret = aclrtMalloc(&workspaceAddr, workspaceSize, ACL_MEM_MALLOC_HUGE_FIRST);
    CHECK_RET(ret == ACL_SUCCESS,
              LOG_PRINT("allocate workspace failed. ERROR: %d\n", ret);
              return ret);
  }

  // 6. Execute the operator
  ret = aclnn[OperatorName](workspaceAddr, workspaceSize, executor, stream);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclnn[OperatorName] failed. ERROR: %d\n", ret);
            return ret);

  // 7. Synchronize stream
  ret = aclrtSynchronizeStream(stream);
  CHECK_RET(ret == ACL_SUCCESS,
            LOG_PRINT("aclrtSynchronizeStream failed. ERROR: %d\n", ret);
            return ret);

  // 8. Print results
  std::cout << "\n\n\noutputTensor1[after]: " << std::endl;
  PrintOutResult<Kernel_dtype>(outputTensor1Shape, &outputTensor1DeviceAddr);
  // Print other outputs as needed

  // 9. Clean up resources
  aclDestroyTensor(inputTensor1);
  aclDestroyTensor(inputTensor2);
  // Destroy other tensors as needed
  aclDestroyTensor(outputTensor1);
  // Destroy other output tensors as needed

  aclrtFree(inputTensor1DeviceAddr);
  aclrtFree(inputTensor2DeviceAddr);
  // Free other input device addresses as needed
  aclrtFree(outputTensor1DeviceAddr);
  // Free other output device addresses as needed
  if (workspaceSize > static_cast<uint64_t>(0)) {
    aclrtFree(workspaceAddr);
  }

  aclrtDestroyStream(stream);
  aclrtResetDevice(deviceId);
  aclFinalize();

  return 0;
}
```

### Handling Missing Operator Information

If the skill cannot find corresponding information in `op_host` or `op_kernel` files:

1. **Check file paths**: Ensure you're looking in the correct directories
2. **Look for alternative files**: Check for other files that might contain operator definitions
3. **Use placeholder values**: If information is missing, use generic placeholder values in the example
4. **Add comments**: Clearly mark sections where information is missing with comments
5. **Provide instructions**: Add instructions for users to fill in the missing information

#### Example of Placeholder Usage

```cpp
// Input tensors - FILL IN based on operator definition
aclTensor *input1 = nullptr;
void *input1DeviceAddr = nullptr;
std::vector<int64_t> input1Shape = {1, 1, 1, 1}; // FILL IN actual shape
std::vector<Kernel_dtype> input1HostData(input1Shape[0] * input1Shape[1] * input1Shape[2] * input1Shape[3], 0.0f);
ret = CreateAclTensor(input1HostData, input1Shape, &input1DeviceAddr, Acl_dtpe, &input1);
```

### Best Practices for Example Generation

1. **Start with a template**: Use the generic template as a starting point
2. **Extract accurate information**: Carefully read operator definitions to get correct parameter names, types, and shapes
3. **Use meaningful values**: Initialize tensors with values that make sense for the operator's functionality
4. **Add comments**: Explain the purpose of each section and any assumptions made
5. **Test the example**: Verify that the generated example compiles and runs correctly
6. **Handle edge cases**: Consider different input shapes and data types
7. **Follow existing patterns**: Maintain consistency with other examples in the codebase

By following this guide, you can efficiently generate accurate CANN `aclnn_*` examples for any AscendC operator, whether it's a simple arithmetic operation or a complex transformer-related operator like `moe_init_routing_grouped_matmul_grad`.
