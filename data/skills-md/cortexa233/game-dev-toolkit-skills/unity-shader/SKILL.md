---
name: unity-shader
description: Hand-write, debug, convert, and optimize Unity ShaderLab/HLSL shaders across URP, HDRP, and Built-in Render Pipeline with cross-platform targets (mobile, PC, console, WebGL). Use for shader authoring, pipeline migration, BRDF or lighting work, shader performance tuning, Custom Renderer Feature or Custom Pass integration, and shader artifact troubleshooting.
---

# Unity Shader

## Goal

Deliver production-ready Unity shader solutions that are explicit about pipeline support, platform constraints, and performance tradeoffs.

## Cross-Agent Use

- Treat this skill as an agent-agnostic instruction set.
- If the host does not support skill invocation syntax, load this file as system/developer instructions.
- Reuse `references/pipeline-rules.md` and `references/performance-and-response.md` as shared policy docs in any AI workflow.

## Workflow

1. Confirm render pipeline, Unity version, target platforms, and requested task type.
2. Assume URP when the pipeline is not provided, and state that assumption explicitly.
3. Choose the response mode: new shader, concept explanation, or optimization pass.
4. Read `references/pipeline-rules.md` for pipeline API conventions and coding constraints.
5. Read `references/performance-and-response.md` when the request includes mobile, WebGL, performance tuning, or quality tiers.
6. Produce complete, paste-ready output files instead of partial fragments.
7. Validate platform and pipeline compatibility before responding.

## Response Contracts

### New shader implementation

- Start with a 2-3 sentence summary of the rendering technique and algorithm.
- Provide one complete `.shader` file ready to paste into Unity.
- Add a file header comment that states supported pipeline(s) and platform assumptions.
- Add inline comments for non-obvious math and coordinate-space transforms.
- List all shader properties with short control descriptions and practical defaults.
- Include required C# code when the shader depends on URP Renderer Features, HDRP Custom Passes, compute dispatch, or runtime property binding.

### Concept explanation

- Explain required transforms: object -> world -> view -> clip -> NDC -> screen.
- Include the relevant formula when useful.
- Mention Unity helper functions that implement key steps.
- Note pipeline-specific differences for the same concept.

### Optimization review

- Show before and after changes with estimated ALU and texture sample impact.
- Recommend profiler checks: RenderDoc, Unity Frame Debugger, Xcode GPU tools, Mali Offline Compiler.
- Suggest LOD or quality-tier strategy when applicable.
- Call out platform-specific risks.

## Non-Negotiable Rules

- Keep response language the same as the user language.
- Keep shader code and shader comments in English.
- Do not mix pipeline conventions in one shader file.
- Keep one effect per shader file.
- Use `shader_feature` or `shader_feature_local` for material features; use `multi_compile` only for true global variants.
- Prefer reusable math in standalone `.hlsl` include files with no pipeline API calls.
- Avoid deprecated `fixed`.
- Avoid Surface Shaders outside Built-in RP.
- Avoid `tex2D()` inside `HLSLPROGRAM` blocks.
- Warn when expected variant count can become excessive.

## Reference Map

- Read `references/pipeline-rules.md` for URP, HDRP, and Built-in conventions plus portability structure.
- Read `references/performance-and-response.md` for precision policy, optimization rules, quality tiers, and output formatting requirements.
- Read `references/generic-agent-template.md` for a host-agnostic prompt template.

