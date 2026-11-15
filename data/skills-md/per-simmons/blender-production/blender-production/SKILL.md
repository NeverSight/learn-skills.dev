---
name: blender-production
description: Build, refine, inspect, render, and visually verify Blender projects using Python and available MCP tools. Use for reference-based modeling, materials and lighting, procedural scenes, animation, render performance, and Blender deliverables.
---

# Blender Production

Produce editable 3D work whose shape, appearance, motion, and delivery are supported by actual inspection. Use Blender Python for repeatable construction and checks, MCP for live inspection and targeted operations, and the native UI for the experience the user receives. MCP is a transport; realism comes from the scene and renderer.

Apply this workflow to buildings, products, environments, characters, abstract/stylized scenes, and animation. Select domain-specific modeling techniques from the brief. Do not turn every task into photoreal architecture. A skill cannot guarantee a perfect reconstruction from incomplete references: define observable acceptance criteria and report what was verified.

## Establish the task and owned session

Read the brief, current status, accepted work, and latest user scope. Identify the deliverable: editable scene, stills, film, interactive experience, or export. A request to wrap up or show current work ends unsolicited refinement; render and package the accepted state.

Before a live mutation, identify Blender version/build, PID, exact open file, scene, engine, and active job. Multiple windows/MCP connections may belong to different projects. A tool connection is not proof of the correct target. Keep one writer per scene and one clear source checkpoint.

Read [control.md](references/control.md) for API/MCP selection, scoped session control, dependency failures, and recovery. Run [probe_scene.py](scripts/probe_scene.py) inside Blender for bounded scene/asset/device diagnostics; ordinary Python generally lacks bpy.

## Translate the brief into checks

Select criteria with tolerances based on sources and intended camera distance:

- Reference modeling: units, silhouette, proportions, landmark alignment, openings/contact, source confidence.
- Products: edge radii, assembly fit, finish, labels, grazing reflections.
- Characters: anatomy/style, silhouette, pose deformation, skin/hair response.
- Environments: terrain, distribution, scale, foliage silhouette, near/far detail.
- Animation: path/pose, timing, deterministic caches, continuity, temporal artifacts.
- Delivery: assets reopen, requested resolution/fps, complete sequence, real playback, working destination.

Keep a small defect ledger: location/view, observed defect, evidence, proposed cause, change, verification. A successful script, object count, or attractive hero frame cannot close unrelated criteria.

## Build in dependency order

1. Establish units, coordinates, references, major shape, and camera. For image matching, solve camera/lens before deforming geometry to fit a photograph.
2. Build visible structure and interfaces: thickness, joints, support/contact, gaps and silhouette detail. Validate evaluated geometry after modifiers.
3. Develop materials with physical texture scale, correct color/data interpretation, projection orientation, and restrained relief.
4. Establish coherent lighting, explicit color management, and renderer-specific reflection/indirect-light behavior.
5. Add detail where it changes the intended view; retain instances and economical distant assets.
6. Inspect actual outputs at intended display size and close crops; repair the largest visible defect and recheck affected views.

Read [realism.md](references/realism.md) for appearance methods and diagnostic vocabulary. Keep parameterized scripts, deterministic seeds, asset provenance, and checkpoints where useful. Regeneration replaces only owned components and preserves accepted hand edits.

## Benchmark delivery early

Interactive navigation, a converged viewport, and a finished movie have different performance requirements. Determine what the user wants to see before changing engines or quality.

Read [rendering.md](references/rendering.md) before costly bakes or films. Benchmark the real scene across representative views, separate cold setup from warm rendering, and inspect a short consecutive-frame motion test. Keep a candidate only when speed and appearance both pass.

Use [benchmark.py](scripts/benchmark.py) on JSONL frame logs to summarize phase costs and warm timings. An ETA from one room is unreliable for a mixed tour.

Render long films as resumable image sequences. Bind reused frames to the same source/dependencies/render configuration; existence is not proof of compatibility. [sequence_tools.py](scripts/sequence_tools.py) checks PNG integrity/dimensions and encodes a gap-free sequence with stream/decode verification. It does not render missing frames or certify visual quality.

## Verify and deliver

Read [qa-delivery.md](references/qa-delivery.md). Review actual images from relevant views and actual motion for animation. Reopen the saved deliverable and check assets/caches. Separate technical checks from visual judgments.

Long jobs run continuously in Blender or a worker. A scheduled monitor only checks completion/failure; its interval is not render cadence. Start encoding directly after successful rendering. If monitoring is requested, stay quiet during healthy progress and stop after agreed delivery. Remote viewing needs an uploaded artifact/hosted viewer; a local path alone does not work on another device.

Report output, meaningful validation, and specific limitations. Do not claim source fidelity, realism, smooth playback, or completion without evidence. Stop refining when the requested delivery passes.

## Compatibility

Discover actual tools, executable, Blender version, GPU and supported RNA properties. Do not assume an MCP provider, port, operating system, hardware backend, or generation service. Use installed-version documentation. See [validation.md](references/validation.md) for the scope of this skill's own checks.
