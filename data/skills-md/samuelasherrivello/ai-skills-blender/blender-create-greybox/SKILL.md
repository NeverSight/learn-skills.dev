---
name: blender-create-greybox
description: Quickly communicate a spatial, layout, or silhouette idea in Blender with the fewest clear primitives; use before detailed modeling or as a deliberately low-fidelity deliverable.
---

# blender-create-greybox

## Purpose and scope

Create the least detailed Blender scene that clearly answers the user's question. A greybox communicates scale, occupancy, circulation, layering, sightlines, or a primary silhouette—not a finished asset, realistic architecture, or final art direction.

Use it for requests such as a house massing, city volume study, 2.5D arrangement, level-layout concept, or camera/blocking test. It can also be an early planning step within another Blender task when that reduces uncertainty. Do not treat the greybox as that other skill's final deliverable unless the user asks for a deliberately low-fidelity result.

## Operating boundaries

Read [operating boundaries](references/operating-boundaries.md) before launching a helper, modifying Blender, capturing editor pixels, or changing an example `.blend`.

## Agent workflow

1. State the spatial question the scene must answer and identify any necessary assumptions about scale, use, and viewing direction before creating content.
2. Create or reuse one dedicated owned collection for the task. Keep generated geometry editable and role-named; use scene-specific role prefixes when several greyboxes share a file. Preserve unrelated scene content and checkpoint before replacing owned geometry.
3. Establish and record a scale convention when scale, clearance, circulation, or contact matters. Treat an inferred convention as an assumption, not a verified fact.
4. Create only the boundary and floor forms needed to establish the spatial frame. Omit either when it cannot clarify the question.
5. Add primary masses, routes, and landmarks in role order using planes, boxes, cylinders, wedges, or other low-sided primitives. Preserve one minimal cue that distinguishes the subject when plain boxes would not: wheels under two masses for a car, a road void among varied-height blocks for a city, or counter/appliance masses inside an open room shell for a kitchen. Add a form only when it makes the requested relationship legible.
6. Validate intended joins, gaps, overlaps, ground contact, and clearances before calling the layout clear. Preserve voids needed for circulation, roads, or an open interior viewing side. Correct only relationships that affect the stated question.
7. Use neutral viewport display by default. Assign a material only when it communicates a required semantic role such as walkable surface, obstacle, boundary, depth layer, or target. When a grid clarifies scale, orientation, or roles, make it procedural and world-aligned: use one shared `Greybox_GridReference` coordinate object (or equivalent world-space/triplanar projection), uniform XYZ mapping, and a documented fixed tile size. Never use Generated or per-object local coordinates, non-uniform mapping, image textures, or UV-dependent mapping for the grid.
8. Select an intentional proof view: use orthographic views for proportion or alignment questions, and perspective or a minimal role-named camera for spatial experience, silhouette, composition, or fixed sightlines. Frame every critical mass; for an interior, do not let a wall or foreground block conceal the work zone. Inspect actual preview or captured pixels from that view.
9. If inspection reveals ambiguity, make the smallest targeted correction and re-inspect the same proof view. Do not introduce texture maps, UV work, bevels, modifiers, interiors, foliage, props, decals, lighting, or final-art detail unless one directly answers the question.
10. Stop as soon as the answer is visually unambiguous. If refinement is requested, identify the smallest next fidelity step instead of skipping to a finished asset.

## Material language

Use a grid only when it improves the answer to the spatial question. A grid is a measurement aid and shared scale language, not decoration: its cells must remain square and the same world-space size across floors, walls, routes, and stretched primitives. Default to one Blender world unit per major tile (one metre only when the scene's unit convention establishes that equivalence); choose another fixed size only when the question warrants it, and report the assumption. Keep its two cells readable but close in value, with low saturation and a restrained grey hue.

Build the checker from the Object output of a Texture Coordinate node explicitly assigned to the one owned `Greybox_GridReference` Empty, through one Mapping node whose X, Y, and Z scales are identical and equal to the reciprocal of the chosen world-space tile size. Do not compensate for an object's dimensions, apply per-object texture scale, or substitute Generated coordinates: those make cells stretch or change size as primitive dimensions change. A 3D procedural checker is preferred because it keeps the grid square on horizontal and vertical faces alike.

Use this fixed ordered palette only: `PowderBlue`, `SoftSage`, `SoftRose`, `Lavender`, `Sand`, `MistTeal`, `Apricot`, and `PalePlum`. All eight have deliberately similar lightness, saturation, procedural nodes, checker contrast, roughness, grid reference, and tile scale. Do not invent an additional color or use a color symbolically (for example, red for fire). The palette only separates groups so the spatial question is easier to read.

Assign palette entries mechanically in the order categories are introduced by the spatial question: first category → `PowderBlue`, second → `SoftSage`, third → `SoftRose`, and so on. Create one shared material datablock per present category, named `Greybox_<PaletteEntry>_<Category>`, and assign that exact datablock to every object in that category. Repeated or structurally similar objects must share their category material even when their individual geometry differs: all city buildings share one material, all kitchen furniture can share one material, and a car's wheel caps and tire sides share the car-body material when they should read as one vehicle. Do not create a separate material merely because an object is repeated, stretched, circular, tall, or narrow.

Choose categories to clarify what is distinct in the user's question, then use the smallest useful count. A car commonly has `Floor` and `Car`; a city commonly has `Floor` and `Buildings`, with roads using the floor material unless road identity is itself the question; an interior commonly has `Floor`, `Walls`, and `Furniture`. Add another category only when it changes the answer, not to decorate or semantically color-code the greybox.

Report the palette entries used, tile size in scene units, world-space/projection method, present category-to-material map, and every exception to category sharing. If material differentiation would not clarify the question, say that it was intentionally omitted.

## Delivery

Save the editable source when requested. Report the demonstrated question, assumptions, owned collection and key object names, proof view, intentionally omitted detail, and visual-validation status. Make visual-quality claims only from inspected preview or captured pixels; report unavailable validation as unverified.
