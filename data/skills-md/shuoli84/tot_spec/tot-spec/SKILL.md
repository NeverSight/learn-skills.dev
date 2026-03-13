---
name: tot-spec
description: "Language-agnostic model definition and RPC code generator from YAML specifications. Use for generating type-safe data (Rust, Python, TypeScript, Java, Swift) from a single source of truth, defining RPC service interfaces with request/response types, creating cross-language type definitions for microservices, working with existing .yaml spec files in the project, or creating new model definitions, enum types, or service methods."
---

> ⚠️ **IMPORTANT**: 常见错误提醒
>
> - 命令名是 `tot_spec` (下划线), **不是** `tot-spec` (连字符)
> - `-o` 参数必须是**文件夹路径**, **不是**文件名
> - **禁止手动修改 codegen 生成的代码**, 使用 [Field Attributes](#field-attributes) 调整

# tot-spec

Generate type-safe data structures and RPC service interfaces from YAML specifications. Ensures consistency across Rust, Python, TypeScript, Java, and Swift codebases.

## Installation

```bash
cargo install --locked --force tot_spec_cli
# or from local
cargo install --locked --force --path .
```

## Quick Start

```bash
# Generate code for a specific language
tot_spec -i <spec_folder> -c <generator> -o <output_FOLDER>

# Available generators: rs_serde, java_jackson, swift_codable, py_dataclass, typescript, swagger
```

## Spec File Structure

```yaml
meta:
  rs_serde:
    package: my_crate
  java_jackson:
    package: com.example.myapp

models:
  - name: User
    type:
      name: struct
      fields:
        - name: id
          type: string
          required: true
        - name: age
          type: i32

methods:
  - name: GetUser
    desc: "Get user by ID"
    request: GetUserRequest
    response: GetUserResponse
```

## Model Types

### Struct

Standard data structure with fields.

```yaml
models:
  - name: CreateUserRequest
    type:
      name: struct
      fields:
        - name: username
          type: string
          required: true
        - name: email
          type: string
```

### Enum

Tagged union/sum type with variants.

```yaml
models:
  - name: PaymentMethod
    type:
      name: enum
      variants:
        - name: CreditCard
          payload_type: string
        - name: PayPal
```

### New Type

Wrapper type for domain modeling.

```yaml
models:
  - name: UserId
    type:
      name: new_type
      inner_type: string
    attributes:
      rs_extra_derive: Hash, PartialEq
```

### Virtual

Shared fields mapped to traits/interfaces.

```yaml
models:
  - name: BaseRequest
    type:
      name: virtual
      fields:
        - name: request_id
          type: string

  - name: CreateUserRequest
    type:
      name: struct
      extend: BaseRequest
      fields:
        - name: username
          type: string
```

### Const

Enum-like constant definitions.

```yaml
models:
  - name: StatusCode
    type:
      name: const
      value_type: i32
      values:
        - name: Ok
          value: 0
        - name: Error
          value: 1
```

## Supported Types

**Primitives**: `bool`, `i8`, `i16`, `i32`, `i64`, `f64`, `string`, `bytes`

**Special**: `decimal`, `bigint`, `json`

**Containers**: `list[T]`, `map[string]` (key is always string)

**References**: `TypeName` or `namespace.TypeName`

## RPC Methods

Define service methods with typed requests and responses.

```yaml
methods:
  - name: CreateUser
    desc: "Create a new user account"
    request: CreateUserRequest
    response: CreateUserResponse
```

## Field Attributes

> ⚠️ **NEVER manually edit generated code!** Use attributes in the spec to customize codegen output.

Language-specific customization via `attributes`:

```yaml
models:
  - name: MyModel
    type:
      name: struct
      fields:
        - name: custom_map
          type: map[string]
          attributes:
            rs_type: std::collections::BTreeMap<String, String>
            rs_extra_derive: Hash, PartialEq
```

### Rust Attributes

| Attribute         | Description                                                         |
| ----------------- | ------------------------------------------------------------------- |
| `rs_type`         | Override the generated Rust type                                    |
| `rs_extra_derive` | Add extra derive macros (e.g., `Hash, PartialEq`)                   |
| `rs_rename`       | Rename field in serialization (use with `#[serde(rename = "...")]`) |

### Python Attributes

| Attribute   | Description                        |
| ----------- | ---------------------------------- |
| `py_type`   | Override the generated Python type |
| `py_rename` | Rename field in serialization      |

### Other Languages

Similar attributes exist for Java (`java_*`), Swift (`swift_*`), TypeScript (`ts_*`).

## Includes

Compose specs with namespace prefixes.

```yaml
includes:
  - path: common_types.yaml
    namespace: common

models:
  - name: MyModel
    type:
      name: struct
      fields:
        - name: data
          type: common.DataModel
```

## Language Examples

See [examples/](references/examples.md) for generated code in each language.

**Rust (rs_serde)**: serde structs with `#[derive(Serialize, Deserialize)]`

**Python (py_dataclass)**: `@dataclass` with `to_dict`/`from_dict`

**TypeScript**: interface definitions

**Swift (swift_codable)**: `Codable` structs

**Java (java_jackson)**: Jackson POJOs

## Resources

### references/

- **examples.md** - Generated code samples for each language with usage examples
- **patterns.md** - Common patterns: pagination, error handling, CRUD operations
- **rpc.md** - RPC service definitions with JSON-RPC models

### scripts/

- **validate_spec.py** - Validate YAML spec syntax before generation
- **update_fixtures.sh** - Update test fixtures for CI/CD
