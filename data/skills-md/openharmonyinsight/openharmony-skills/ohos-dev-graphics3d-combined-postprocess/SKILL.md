---
name: ohos-dev-graphics3d-combined-postprocess
description: "Implement Combined post-processing effects (tone mapping, color grading, vignette) in Graphics3D. MUST use when: (1) Adding effect to Combined post-process, (2) User mentions 'Combined post-process' or 'post-processing'. DOES NOT apply to multi-pass effects (bloom, depth-of-field)."
metadata:
  display_name: OpenHarmony Graphics3D Combined Post-Process Implementation
  scope: domain
  stage: development
  domain: graphics3d
  capability: combined-postprocess
  version: 0.1.0
  status: stable
---

# Combined Post-Process Implementation Guide

Implement Combined post-processing effects across three modules following the dependency chain:
**LumeRender** → **Lume3D** → **LumeScene**

## Task and Boundaries

This skill guides implementation of single-pass post-processing effects in OpenHarmony Graphics3D. 

**Applicable:**
- Effects running in single fullscreen shader pass (tone mapping, color grading, vignette)
- Adding effects to Combined post-process system

**Not Applicable:**
- Effects requiring separate render passes (bloom with blur passes, depth-of-field, motion blur)

## Module Dependency Overview

```
LumeRender (AGPRender)
    ↓
Lume3D (AGP3D) 
    ↓
LumeScene
```

- **LumeRender**: Low-level rendering module, provides shader/render node infrastructure
- **Lume3D**: 3D scene module, provides ECS components, depends on LumeRender
- **LumeScene**: High-level scene module, provides user-friendly interfaces, depends on Lume3D

---

## Pre-Implementation Checklist

**Before implementing any Combined post-process effect, ask yourself:**

1. **Visual Effect Goal**: What visual effect do you want to achieve? (tone mapping, color grading, vignette, custom effect)
2. **Parameter Complexity**: How many parameters does the effect need?
   - 1-4 parameters: Use `factors[]` Vec4 only
   - 5-8 parameters: Split into `factors[]` + `userFactors[]`
   - >8 parameters: Consider if this is appropriate for Combined system
3. **Render Pass Requirement**: Does the effect need intermediate framebuffers?
   - Single fullscreen pass: ✓ Use Combined post-process (this skill)
   - Blur passes, downscale/upscale, temporal: ✗ Use multi-pass system (not this skill)
4. **Index Availability**: Are indices 0-7 available in Combined system?
   - Currently used: 0 (tone), 1 (vignette), 2 (dither), 3 (color conversion), 4 (fringe), 5 (upscale), 6 (white balance), 7 (color adjustments)
   - Need unused index: Must register new index in both shader and C++

**Decision Tree:**

```
Effect needs >4 params? ─────YES──→ Split: factors[] + userFactors[]
                         │
                         NO
                         ↓
Effect needs blur/temporal? ─YES──→ Use multi-pass system (EXIT this skill)
                         │
                         NO
                         ↓
Index 0-7 available? ──────YES──→ Continue with Combined implementation ✓
                         │
                         NO
                         ↓
Need to register new index → Follow LumeRender Step 1-3 first
```

## Workflow

**LumeRender (8 steps):**
1. Define configuration structure
2. Register metadata
3. Define shader constants
4. Implement config-to-shader conversion
5. Fill post-process stack
6. Add conversion in RenderNodeUtil
7. Implement shader processing function
8. Integrate into render pipeline

**Lume3D (5 steps):**
1. Add flag bit
2. Define component property
3. Register metadata
4. Integrate into render system
5. Integrate into Lume3D shader

**LumeScene (9 steps):**
1. Define interface
2. Add to IPostProcess interface
3. Implement API wrapper
4. Implement effect class
5. Register in PostProcess
6. Register component type
7. Register plugin type
8. Register Any type
9. Update build files

---

## LumeRender Implementation

**MANDATORY - READ ENTIRE FILE**: Before starting LumeRender steps, you MUST read [`references/code_templates.md`](references/code_templates.md#lumarender-templates) "LumeRender Templates" section (Steps 1-8, ~300 lines) completely. **Do NOT set any range limits when reading this file.**

**Do NOT load** `advanced_reference.md` yet — save for troubleshooting phase.

### Step 1: Define Configuration Structure

**File**: `api/render/datastore/render/render_data_store_render_pods.h`

Define effect configuration struct with properties and default values. Add enum indices, flag bits, and property type declaration.

**Details**: See [references/code_templates.md#step-1-define-configuration-structure](references/code_templates.md#step-1-define-configuration-structure)

---

### Step 2: Register Metadata

**File**: `src/postprocesses/render_post_process_combined_node.cpp`

Register enum values, type metadata, and configuration structure metadata for reflection system.

**Details**: See [references/code_templates.md#step-2-register-metadata](references/code_templates.md#step-2-register-metadata)

---

### Step 3: Define Shader Constants

**File**: `api/render/shaders/common/render_post_process_structs_common.h`

Define shader macro constants for effect specialization bits and indices.

**Details**: See [references/code_templates.md#step-3-define-shader-constants](references/code_templates.md#step-3-define-shader-constants)

---

### Step 4: Implement Config-to-Shader Conversion

**File**: `src/datastore/render_data_store_post_process.h`

Implement conversion functions to pack configuration into shader-friendly Vec4 factors.

**Details**: See [references/code_templates.md#step-4-implement-config-to-shader-conversion](references/code_templates.md#step-4-implement-config-to-shader-conversion)

---

### Step 5: Fill Post-Process Stack

**File**: `src/datastore/render_data_store_post_process.cpp`

Add effect to post-process stack with built-in data and factors.

**Details**: See [references/code_templates.md#step-5-fill-post-process-stack](references/code_templates.md#step-5-fill-post-process-stack)

---

### Step 6: Add Conversion in RenderNodeUtil

**File**: `src/nodecontext/render_node_util.cpp`

Add factor conversion call in `GetRenderPostProcessConfiguration()` function.

**Details**: See [references/code_templates.md#step-6-add-conversion-in-rendernodeutil](references/code_templates.md#step-6-add-conversion-in-rendernodeutil)

---

### Step 7: Implement Shader Processing Function

**File**: `api/render/shaders/common/render_post_process_blocks.h`

Implement GLSL shader processing function with effect logic.

**Details**: See [references/code_templates.md#step-7-implement-shader-processing-function](references/code_templates.md#step-7-implement-shader-processing-function)

---

### Step 8: Integrate into Render Pipeline

**File**: `assets/render/shaders/shader/fullscreen_combined_post_process.frag`

Call shader processing function in fullscreen render pipeline.

**Details**: See [references/code_templates.md#step-8-integrate-into-render-pipeline](references/code_templates.md#step-8-integrate-into-render-pipeline)

---

## Lume3D Implementation

**MANDATORY - READ SECTION**: Now read [`references/code_templates.md`](references/code_templates.md#lume3d-templates) "Lume3D Templates" section (Steps 1-5, ~100 lines) for ECS integration examples.

**Do NOT load** `advanced_reference.md` yet — continue following workflow steps.

### Step 1: Add Flag Bit

**File**: `api/3d/ecs/components/post_process_component.h`

Add flag bit to PostProcessComponent::FlagBits enum.

**Details**: See [references/code_templates.md#lume3d-step-1-add-flag-bit](references/code_templates.md#lume3d-step-1-add-flag-bit)

---

### Step 2: Define Component Property

**File**: `api/3d/ecs/components/post_process_component.h`

Define component property with DEFINE_PROPERTY macro.

**Details**: See [references/code_templates.md#lume3d-step-2-define-component-property](references/code_templates.md#lume3d-step-2-define-component-property)

---

### Step 3: Register Metadata

**File**: `src/ecs/components/post_process_component_manager.cpp`

Register enum values and configuration metadata.

**Details**: See [references/code_templates.md#lume3d-step-3-register-metadata](references/code_templates.md#lume3d-step-3-register-metadata)

---

### Step 4: Integrate into Render System

**File**: `src/ecs/systems/render_system.cpp`

Assign configuration in `ProcessPostProcessComponents()` function.

**Details**: See [references/code_templates.md#lume3d-step-4-integrate-into-render-system](references/code_templates.md#lume3d-step-4-integrate-into-render-system)

---

### Step 5: Integrate into Lume3D Shader

**File**: `api/3d/shaders/common/3d_dm_inplace_post_process.h`

Call shader processing function in Lume3D inplace post-process.

**Details**: See [references/code_templates.md#lume3d-step-5-integrate-into-lume3d-shader](references/code_templates.md#lume3d-step-5-integrate-into-lume3d-shader)

---

## LumeScene Implementation

**MANDATORY - READ SECTION**: Read [`references/code_templates.md`](references/code_templates.md#lumescene-templates) "LumeScene Templates" section (Steps 1-9, ~400 lines) for API wrapper and registration examples.

**Do NOT load** `advanced_reference.md` yet — only load when encountering errors or need data flow diagrams.

### Step 1: Define Interface

**File**: `include/scene/interface/postprocess/intf_your_effect.h`

Define interface class with META_INTERFACE and property declarations.

**Details**: See [references/code_templates.md#lumescene-step-1-define-interface](references/code_templates.md#lumescene-step-1-define-interface)

---

### Step 2: Add to IPostProcess Interface

**File**: `include/scene/interface/intf_postprocess.h`

Add include and META_READONLY_PROPERTY for effect interface.

**Details**: See [references/code_templates.md#lumescene-step-2-add-to-ipostprocess-interface](references/code_templates.md#lumescene-step-2-add-to-ipostprocess-interface)

---

### Step 3: Implement API Wrapper

**File**: `include/scene/api/post_process.h`

Implement wrapper class with META_INTERFACE_OBJECT and property macros.

**Details**: See [references/code_templates.md#lumescene-step-3-implement-api-wrapper](references/code_templates.md#lumescene-step-3-implement-api-wrapper)

---

### Step 4: Implement Effect Class

**Files**: 
- Header: `src/postprocess/your_effect.h`
- Implementation: `src/postprocess/your_effect.cpp`

Implement effect class inheriting from PostProcessEffect template with META_OBJECT macros.

**Details**: See [references/code_templates.md#lumescene-step-4-implement-effect-class](references/code_templates.md#lumescene-step-4-implement-effect-class)

---

### Step 5: Register in PostProcess

**Files**: 
- Header: `src/postprocess/postprocess.h`
- Implementation: `src/postprocess/postprocess.cpp`

Add static property data and InitDynamicProperty handler.

**Details**: See [references/code_templates.md#lumescene-step-5-register-in-postprocess](references/code_templates.md#lumescene-step-5-register-in-postprocess)

---

### Step 6: Register Component Type

**File**: `src/component/postprocess_component.h`

Add META_TYPE registration and property macros.

**Details**: See [references/code_templates.md#lumescene-step-6-register-component-type](references/code_templates.md#lumescene-step-6-register-component-type)

---

### Step 7: Register Plugin Type

**File**: `src/plugin.cpp`

Add RegisterObjectType and UnregisterObjectType calls.

**Details**: See [references/code_templates.md#lumescene-step-7-register-plugin-type](references/code_templates.md#lumescene-step-7-register-plugin-type)

---

### Step 8: Register Any Type

**File**: `src/register_anys.cpp`

Add interface pointer type to ObjectTypes list.

**Details**: See [references/code_templates.md#lumescene-step-8-register-any-type](references/code_templates.md#lumescene-step-8-register-any-type)

---

### Step 9: Update Build Files

**Files**: 
- `include/CMakeLists.txt`
- `src/CMakeLists.txt`
- `BUILD.gn`

Add interface and source files to build targets.

**Details**: See [references/code_templates.md#lumescene-step-9-update-build-files](references/code_templates.md#lumescene-step-9-update-build-files)

---

## Prohibited Practices

### NEVER Apply to Multi-Pass Effects

**Effects requiring separate render passes** (bloom with blur, depth-of-field, motion blur, FXAA, TAA):

- **WHY**: Combined post-process shader (`fullscreen_combined_post_process.frag`) only handles indices 0-7. Multi-pass effects use indices 8+ with separate shaders and intermediate framebuffers.
- **CONSEQUENCE**: Attempting Combined approach causes `factors[INDEX_BLOOM]` (index 9) to be ignored in Combined shader. Effect won't render, or may read garbage data from wrong memory offset.
- **VALIDATION**: Check if effect needs intermediate render passes (blur passes, downscale/upscale). If yes → use multi-pass system, not Combined.
- **CORRECT**: Use dedicated multi-pass post-process implementation with separate render node graph.

---

### NEVER Mismatch Shader-C++ Indices

**Index consistency between GLSL constants and C++ enums**:

- **WHY**: Shader accesses `uGlobalData.factors[POST_PROCESS_INDEX_TONEMAP]` directly. If shader defines `POST_PROCESS_INDEX_TONEMAP 0` but C++ defines `INDEX_TONEMAP 1`, shader reads wrong Vec4 from factors array.
- **CONSEQUENCE**: Visual artifacts (wrong colors, parameters not applied) or GPU validation error "array index out of bounds" if index exceeds `POST_PROCESS_GLOBAL_VEC4_FACTOR_COUNT (14)`.
- **VALIDATION**: Cross-check three files:
  1. Shader: `render_post_process_structs_common.h` → `POST_PROCESS_INDEX_*` values
  2. C++ config: `render_data_store_render_pods.h` → `PostProcessConfiguration::INDEX_*` values
  3. DataStore conversion: `render_data_store_post_process.cpp` → `factors[INDEX_*]` assignment
- **CORRECT**: Ensure all three locations use same numeric value. File comment explicitly states: "needs to match api/core/render/render_data_store_render_pods.h".

---

### NEVER Forget userFactors for >4 Parameters

**Effects needing more than 4 float parameters**:

- **WHY**: Vec4 only holds 4 floats. GlobalPostProcessStruct has `factors[14]` (Vec4 array) and `userFactors[16]` (Vec4 array). If effect has 5+ parameters, must split into factors + userFactors.
- **CONSEQUENCE**: Shader tries to read `uGlobalData.userFactors[USER_INDEX_*]` but constant undefined → compilation error "undefined macro". Or if defined but not filled → shader reads zero Vec4 → effect parameters wrong.
- **VALIDATION**: Count effect parameters. If >4, verify:
  1. `USER_INDEX_*` constant defined in `render_data_store_render_pods.h`
  2. `GetFactorXXX()` function for userFactors in `render_data_store_post_process.h`
  3. Shader uses correct userFactors index: `uGlobalData.userFactors[POST_PROCESS_USER_INDEX_*]`
- **CORRECT**: For 5-8 parameters: use factors[0-3] + userFactors[0-3]. Define `USER_INDEX_*` constant, implement conversion function, call in FillDefaultPostProcessData.

---

### NEVER Skip LumeRender/Lume3D/LumeScene Consistency

**All three modules must be updated**:

- **WHY**: Combined post-process flows through three modules: LumeRender defines shader constants → Lume3D integrates into ECS → LumeScene wraps API. Skipping one module breaks the chain.
- **CONSEQUENCE**: 
  - Skip LumeRender: Shader can't find `PostProcessXXXBlock()` function → compilation error
  - Skip Lume3D: `PostProcessComponent` missing property → ECS system won't propagate configuration → shader receives zero factors
  - Skip LumeScene: User API missing → developers can't configure effect → unusable
- **VALIDATION**: Use implementation checklist (22 steps across 3 modules). Check each module's key files exist and are modified.
- **CORRECT**: Follow all 22 steps. LumeRender (8) → Lume3D (5) → LumeScene (9) in sequence.

---

## Exceptions and Fallbacks

### Effect Requires Multiple Render Passes

**Symptom**: Effect needs blur passes, downscale/upscale, temporal accumulation.

- **Fallback**: This skill doesn't apply. Use dedicated multi-pass post-process system with separate render node graph.
- **Evidence**: Check if shader needs `uImgSampler` + `uBloomSampler` + intermediate framebuffers (like bloom). If yes → multi-pass.

### Shader Compilation Error

**Symptom**: "undefined macro POST_PROCESS_INDEX_XXX" or "array index out of bounds".

- **Diagnosis**: Index mismatch or missing constant definition.
- **Fix**: Check shader constant matches C++ enum value. Verify index < 14 (POST_PROCESS_GLOBAL_VEC4_FACTOR_COUNT).

### Visual Artifacts or Effect Not Applied

**Symptom**: Wrong colors, parameters ignored, effect invisible.

- **Diagnosis**: Wrong factors index, or GetFactorXXX() not called in DataStore.
- **Fix**: Verify conversion function called in both `render_data_store_post_process.cpp` (Step 5) and `render_node_util.cpp` (Step 6).

---

## References

### Primary Reference Files

- **[`references/code_templates.md`](references/code_templates.md)** (785 lines): Complete code templates with Generic Template and Tone Mapping Example for all 22 steps. **MANDATORY loading during implementation**.
- **[`references/advanced_reference.md`](references/advanced_reference.md)** (306 lines): Advanced reference with data flow diagrams, implementation checklists, and troubleshooting guide. **Load ONLY when troubleshooting or need data flow understanding**.

### Loading Strategy

**Phase 1 - Initial Implementation**:
- ✅ **MANDATORY**: Load `code_templates.md` in three stages (LumeRender → Lume3D → LumeScene sections)
- ❌ **Do NOT load**: `advanced_reference.md` (save for later)

**Phase 2 - Troubleshooting**:
- ✅ **Load when needed**: `advanced_reference.md` if encountering errors, need data flow diagrams, or implementation checklists
- ❌ **Do NOT reload**: `code_templates.md` if already loaded

---

## Key Points

1. **Architecture: Configuration-Conversion Separation**
   - Configuration structs for user interfaces
   - Conversion functions pack into shader-friendly Vec4
   
2. **Critical: Shader-C++ Index/Bit Consistency**
   - `POST_PROCESS_INDEX_*` ↔ `PostProcessConfiguration::INDEX_*`
   - `POST_PROCESS_SPECIALIZATION_*_BIT` ↔ `FlagBits` enum
   - Mismatch causes GPU validation errors or visual artifacts
   
3. **Mandatory: Dual Path Support**
   - Add conversions in BOTH DataStore (Step 5) AND RenderNodeUtil (Step 6)
   - Single-path implementation fails in some scenarios
   
4. **Naming and Macro Conventions**
   - Shader function: `PostProcess<Effect>Block` naming
   - META_TYPE: include only when interface has enum types
   - META_READONLY_PROPERTY: must add to IPostProcess interface