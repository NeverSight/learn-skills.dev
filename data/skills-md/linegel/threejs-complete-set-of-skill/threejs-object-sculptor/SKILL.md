---
name: threejs-object-sculptor
description: Sculpt reference-image objects into procedural Three.js models. Use for reconstruction feasibility, procedural build planning, code-native implementation, or animation-, collider-, and destruction-ready structure from one or more object views.
---

# Three.js Object Sculptor

Turn object images into an evidence-bound procedural reconstruction. The output may be a feasibility verdict, a build plan, or working code; every branch follows the same six stages.

## Inputs and limits

Use every supplied view. If the target or intended use is ambiguous, resolve that ambiguity before committing to a representation. Otherwise, assume an interactive browser prop whose authored scale can be revised.

A single view determines only visible evidence. Hidden surfaces, thickness, absolute dimensions, material parameters, and articulation remain assumptions unless symmetry, known construction, extra views, or measurements constrain them. Label each assumption. Exact likeness, manufacturing dimensions, or an unseen mechanism requires the missing view or measurement; a stated stylized approximation is a valid alternative.

For a local image, set `<skill-dir>` to the directory containing this `SKILL.md`,
then run `python3 "<skill-dir>/scripts/probe_reference_image.py" "<image>"` using
[probe_reference_image.py](scripts/probe_reference_image.py). It reports format,
byte count, dimensions, aspect ratio, and metadata parsing status. That status
describes file metadata only; visual inspection in stage 1 alone determines
whether the pictured object is readable. The helper reads a bounded prefix
(default 1 MiB, `--max-header-bytes` up to 64 MiB) and reports file bytes and
scanned bytes separately. Its width/height are stored raster or canvas dimensions,
not EXIF-oriented, pixel-aspect-corrected, or decoded-image validation. A partial
result for a valid but unsupported or late header is not an unreadable object.
Supported headers are PNG IHDR, JPEG SOF before scan data, GIF logical screen,
WebP VP8/VP8L/VP8X, BMP CORE/Windows INFO families, and the first classic TIFF
IFD. BigTIFF and JPEG DNL height recovery are outside this helper. File validity,
all animation/page frames, orientation, and color remain separate inspections.
Header rules follow [PNG](https://www.w3.org/TR/png-3/#11IHDR),
[WebP](https://developers.google.com/speed/webp/docs/riff_container),
[BMP CORE](https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapcoreheader),
and the [JPEG frame reader](https://github.com/libjpeg-turbo/libjpeg-turbo/blob/main/src/jdmarker.c).

## Six-stage sculpt

### 1. Inspect

Inspect every view before planning geometry. Record:

- the target boundary, crop, resolution, blur, occlusion, transparency, and conflicting subjects;
- visible front/up cues, camera projection clues, a scale anchor when one exists, and view-to-view consistency;
- the reference identity and orientation/crop transform, including mirroring, pixel
  aspect, lens distortion, and which frame of an animation is being compared;
- which contours, negative spaces, contacts, material regions, and repeated features are directly observed;
- which hidden forms or physical properties remain assumptions.

Visual inspection alone assigns an **evidence readability** verdict:

- `readable`: the target and its dominant silhouette are clear enough to choose a reconstruction;
- `conditional`: a useful approximation is possible with named assumptions, reduced scope, or another view;
- `unreadable`: target identity or defining form is too ambiguous for a defensible reconstruction.

When conditional or unreadable evidence affects an identity-defining feature, request the smallest missing input or state the reduced claim. Inspection is complete when every supplied view is accounted for, the verdict has evidence, and every consequential uncertainty is explicit.

### 2. Decompose

Freeze one object coordinate frame and one authored unit. Partition the object coarse to fine:

1. macro masses and the outer silhouette;
2. meso parts, openings, contacts, joints, and repeated systems;
3. micro features that remain visible at the closest required view;
4. material regions and their observable response.

Mark **identity anchors**: silhouette breaks, negative spaces, signature proportions, distinctive joints, repeated rhythms, and local material or geometric features whose loss would change what the object is. Keep each anchor as an explicit component, boundary, field, or verification target; a later average that erases one fails the reconstruction.

Decomposition is complete when every visible identity anchor has one owner, every child part names its parent/contact, and every inferred part is labeled as an assumption rather than image evidence.

### 3. Select representation

Choose a representation per semantic part, using the cheapest form that preserves its identity anchors and future ownership:

- analytic primitive or beveled primitive;
- lathe profile;
- parallel-transport sweep;
- shape extrusion or justified CSG;
- instanced, batched, or card-based repeated detail;
- a separately routed generated/deforming surface when these supports cannot express the target.

After choosing one or more of these branches and before implementation, read the matching sections of [procedural object patterns](references/procedural-patterns.md) and apply their construction and verification rules.

Keep stable logical identities and independent transform/update ownership for
parts that move, detach, change material, need picking/collision identity, or own
an attachment. Use separate nodes when their parent/child hierarchy requires
them; instanced or batched parts may use a stable semantic-to-instance mapping
when it preserves those operations. When a child part touches, enters, hinges from, or follows a parent, read [attachment and joint correctness](references/attachment-joint-correctness.md) before blockout.

Selection is complete when every decomposed part has exactly one representation and owner, every rejected alternative has a concrete failure condition, and every conditional reference required by the selected branches has been applied.

### 4. Block out

Build only macro masses, dominant openings, coordinate frame, and identity-critical negative space. For feasibility or planning, the blockout is a dimensioned primitive/profile sketch; for implementation, it is renderable coarse geometry in the target repository.

Use the intended comparison camera before adding detail. Normalize the reference
orientation/crop first. Match framing and projection separately from object
proportions so camera error does not become geometry. With several views, retain
one shared model and per-view cameras instead of fitting a different object to
each image. Calibrate against landmarks with uncertainty before freezing the
comparison views; do not retune the camera to hide each geometry regression. Preserve semantic node boundaries needed by later attachments or motion.

Blockout is complete when the target reads from silhouette alone in every required view, dominant proportions and negative spaces are within the declared tolerance, and geometry and layout carry the match without relying on material or micro detail.

### 5. Refine applicable branches

Open only branches supported by the request and evidence, in this order:

1. **Structure:** add meso parts, holes, seams, repeated systems, and attachment roots. Apply the attachment reference to every applicable child and verify contact before continuing.
2. **Form:** add bevels, tapers, bends, profile changes, caps, asymmetry, and silhouette-affecting relief. Apply the chosen representation's pole, seam, winding, and frame rules.
3. **Material:** separate base color from lighting; implement observable roughness, metalness, clearcoat, transmission, normal/bump/displacement, wear, or local masks. Band-limit detail to its screen footprint.
4. **Action:** add stable pivots, sockets, independent nodes, or detachable groups only when the requested use needs them. For collider intent, name each semantic part's collider representation, units/frame, fit tolerance, and collision LOD independently of render LOD. For destruction intent, author stable breakable groups, seams and cut faces, fragment IDs/mass/pivots, and effect sockets. Keep authored metadata distinct from a physics solver claim.
5. **Performance:** simplify by measured projected error; instance or batch only where semantic identity and update ownership survive.

After each opened branch, compare against its identity anchors before opening the next. Refinement is complete when every applicable branch meets its local criterion, every omitted branch is inapplicable rather than forgotten, and every identity anchor remains visible or structurally represented.

### 6. Verify

For code, run the target repository's syntax/type/build checks and its existing capture path. Inspect the final render directly. Keep comparison camera, projection, framing, viewport, exposure, and review lighting fixed across iterations.

Compare in this order:

1. silhouette, proportions, and negative space;
2. component placement, hierarchy, contacts, repeated rhythm, and any requested collider or fracture structure;
3. form transitions and identity anchors;
4. material response under neutral and grazing light;
5. camera and reference-lighting match.

Route each mismatch to one cause:

- `ambiguity`: evidence cannot determine the answer; request a view/measurement or reduce the claim;
- `decomposition`: a part, boundary, or identity anchor is missing or owned incorrectly; revise stage 2;
- `implementation`: the chosen representation is correct but its geometry, material, hierarchy, or filtering is wrong; revise stages 4-5;
- `camera-lighting`: framing, projection, exposure, or illumination prevents a fair comparison; fix the review setup before judging the model.

Verification is complete when the artifact passes the checks appropriate to its branch, every required view has been inspected in the stated order, every remaining mismatch has a routed correction or explicit limitation, and the final report distinguishes observed fidelity from remaining assumptions.

## Result

Return the evidence-readability verdict, evidence and assumptions, decomposition and identity anchors, representation decisions, branch results, verification evidence, and remaining limits. For implementation requests, edit the target code and report only checks and images actually inspected.
