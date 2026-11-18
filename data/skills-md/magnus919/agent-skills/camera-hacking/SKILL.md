---
name: camera-hacking
description: >-
  Investigate, reverse-engineer, develop, and validate digital-camera modifications
  and interoperability, including custom firmware, hidden settings, camera control
  protocols, feature unlocks, and model-specific recovery. Use for feasibility
  research, offline analysis, controlled experiments, and explicitly authorized
  installation on photographic, cinema, and action cameras across manufacturers,
  especially Fujifilm X and Ricoh GR. Do not use for ordinary photography advice,
  routine vendor firmware updates, media editing, or unauthorized camera access.
license: MIT
compatibility: Reference-based methodology; no required runtime. Individual projects require their own tools, hardware, licenses, and supported host environment.
---

# Camera Hacking

Turn a requested camera capability into a source-grounded investigation, controlled
implementation, and verified result. Start with the desired photographic outcome,
not a firmware download. The references are dated discovery evidence, not a list
of universally supported hacks. Refresh relevant upstream evidence before acting.

## Scope and authorization

Support discovery, offline firmware/source analysis, patch development, build and
emulator work, protocol interoperability, and explicitly authorized camera-side
experiments. Name which stage the user requested. Do not stop at research when the
user authorized implementation; continue through the requested deliverable.

This workflow can change external state: camera settings, calibration, boot flags,
firmware, network services, cards, or physical hardware.

> Confirm the target, scope, and rollback path before acting. Read-only discovery may proceed without confirmation.

Use authorization already established in the session; ask only for missing scope.
A request to research a public skill does not authorize changing a personal camera.
Destructive operations require an explicit directive. A reversible card loader may
still change persistent camera state. Do not run an unknown tool merely to query a
camera: first establish whether the command writes state or enables services.

## Workflow

1. **Define the outcome and deliverable.** Record the feature, execution location,
   required shooting mode, image/output requirements, and requested stage. For a
   public survey, keep multiple manufacturers/models; do not require a personal
   camera choice. For a device operation, resolve the exact body, regional suffix,
   firmware and image hash when available, board revision if material, existing
   modifications, accessories, host platform, and ownership/authorization.
2. **Find the narrowest evidence.** Load the matching manufacturer reference and
   model/family record below. Check official capabilities and SDKs, then original
   project documentation, source, release artifacts and negative reports. Record
   URL, date, commit/release, exact tested identity and evidence level. If a brand
   is absent, use [the evidence method](references/evidence-scope.md) and document
   the new model; absence is not proof that it cannot be modified.
3. **Classify the mechanism.** Use [mechanisms and compatibility](references/mechanisms.md)
   to distinguish official control, reverse-engineered protocols, host processing,
   RAM execution, persistent settings/calibration, firmware replacement and hardware
   changes. An external phone waveform is not an in-camera waveform. Shared sensor,
   processor, retail branding or similar firmware number does not establish support.
4. **Make a bounded feasibility decision.** Use [the assessment template](templates/camera-assessment.md).
   Compare the least invasive path meeting the actual outcome. Mark feasible under
   stated conditions, infeasible under those conditions, or unresolved with the next
   evidence needed. A model roster, raw decoder, transfer driver, source directory,
   successful build or checksum does not prove a working photographic feature.
5. **Develop and analyze offline when requested.** Preserve pristine inputs, source
   provenance, licenses and hashes. Work on copies. Inspect project scripts and any
   bundled agent instructions before executing them. Define the hypothesis, target
   symbols/addresses and expected differences; produce a reviewable patch and build
   receipt rather than inventing offsets. Separate container integrity, executable
   behavior and complete source-to-binary reproducibility. Use existing model-specific
   runbooks; this skill supplies no generic flasher or universal memory-write command.
6. **Prepare the device experiment.** Read [experiments and recovery](references/experiments-and-recovery.md)
   for build, installation or hardware tasks. Resolve compatibility, conflicting
   mods, affected persistent state, backups and failure-specific recovery before
   writing. If recovery is unverified, say so; do not rename it a tested rollback.
   Deliver any safe offline artifacts while holding the dependent device operation
   for the missing evidence or explicit scope decision.
7. **Execute the authorized stage and verify its outcome.** Follow the pinned
   project procedure only for the resolved target. Capture expected/observed changes,
   hashes, failures and restoration results using [the experiment record](templates/experiment-record.md).
   Test the intended lifecycle: live view, recording, file integrity, relevant lenses,
   restart and restoration as applicable. Stop on identity mismatch, unexpected writes,
   output corruption, thermal/power faults, or loss of the recovery prerequisite.
8. **Deliver the requested artifact.** Provide the assessment, source/patch/build,
   experiment record or verified device result requested. Separate what was documented,
   inspected, built, emulated, maintainer-reported and independently reproduced.
   State unresolved limitations and the next concrete evidence, without claiming a
   completed installation from a script exit or a menu screenshot.

## Reverse-engineering and neighboring skills

Load supporting skills by name only when their work is needed. They are optional
companions, not assumed files inside this installation.

| Need | Existing skill | Boundary |
|---|---|---|
| Understand a camera project's source architecture, interfaces and dependencies | `software-architecture-analysis` | Source-based reverse engineering; not greenfield design or camera qualification |
| Plan static binary inspection, disassembly and cross references | `binary-analysis` | Its current live Ghidra backend is unimplemented and fails closed; do not promise working decompilation or route patching/protocol work to it |
| Board identification, signals, power, measurement or hardware modification | `electronics` | Electrical analysis does not establish firmware compatibility or recovery |
| Expand or resolve conflicting primary evidence | `research-methodology` | Source-to-claim closure; preserve dated unknowns |
| Probe captured media or inspect a claimed output feature | `ffmpeg` | Media tooling does not establish camera-side execution or editorial truth |

If a companion is unavailable, disclose that limitation and complete the work that
can be supported; do not invent a skill, CLI backend or analysis result.

## Load references on demand

For a named manufacturer, load only its row, then the relevant model evidence.
Inventory files linked from manufacturer records are optional source tables for
roster questions. Their gPhoto, LibRaw and vendor meanings remain distinct.
For a general survey, start with [scope and gaps](references/evidence-scope.md).
For refreshing or adding evidence, read [provenance](references/provenance.md).

### Manufacturer routing

Load the matching brand only; each includes its inventory routes and known gaps.

| Manufacturer | Reference |
|---|---|
| AgfaPhoto | [agfaphoto](references/manufacturer-agfaphoto.md) |
| AKASO | [akaso](references/manufacturer-akaso.md) |
| ARRI | [arri](references/manufacturer-arri.md) |
| BenQ | [benq](references/manufacturer-benq.md) |
| Blackmagic Design | [blackmagic-design](references/manufacturer-blackmagic-design.md) |
| Canon | [canon](references/manufacturer-canon.md) |
| Casio | [casio](references/manufacturer-casio.md) |
| Contax / Kyocera | [contax-kyocera](references/manufacturer-contax-kyocera.md) |
| Digital Bolex | [digital-bolex](references/manufacturer-digital-bolex.md) |
| DJI | [dji](references/manufacturer-dji.md) |
| Epson | [epson](references/manufacturer-epson.md) |
| Fujifilm | [fujifilm](references/manufacturer-fujifilm.md) |
| GE / General Imaging | [general-imaging](references/manufacturer-general-imaging.md) |
| GoPro | [gopro](references/manufacturer-gopro.md) |
| Hasselblad | [hasselblad](references/manufacturer-hasselblad.md) |
| HP | [hp](references/manufacturer-hp.md) |
| Insta360 | [insta360](references/manufacturer-insta360.md) |
| JVC | [jvc](references/manufacturer-jvc.md) |
| Kinefinity | [kinefinity](references/manufacturer-kinefinity.md) |
| Kodak | [kodak](references/manufacturer-kodak.md) |
| Konica / Minolta | [konica-minolta](references/manufacturer-konica-minolta.md) |
| Leica | [leica](references/manufacturer-leica.md) |
| Lytro | [lytro](references/manufacturer-lytro.md) |
| Nikon | [nikon](references/manufacturer-nikon.md) |
| Olympus / OM System | [olympus-om-system](references/manufacturer-olympus-om-system.md) |
| Panasonic / LUMIX | [panasonic](references/manufacturer-panasonic.md) |
| Pentax | [pentax](references/manufacturer-pentax.md) |
| Phase One / Mamiya | [phase-one-mamiya](references/manufacturer-phase-one-mamiya.md) |
| Polaroid | [polaroid](references/manufacturer-polaroid.md) |
| RED Digital Cinema | [red](references/manufacturer-red.md) |
| Ricoh | [ricoh](references/manufacturer-ricoh.md) |
| Rollei | [rollei](references/manufacturer-rollei.md) |
| Samsung | [samsung](references/manufacturer-samsung.md) |
| Sanyo | [sanyo](references/manufacturer-sanyo.md) |
| Sigma | [sigma](references/manufacturer-sigma.md) |
| SJCAM | [sjcam](references/manufacturer-sjcam.md) |
| Sony | [sony](references/manufacturer-sony.md) |
| Toshiba | [toshiba](references/manufacturer-toshiba.md) |
| Vivitar | [vivitar](references/manufacturer-vivitar.md) |
| Xiaomi / YI | [xiaomi-yi](references/manufacturer-xiaomi-yi.md) |
| Yashica | [yashica](references/manufacturer-yashica.md) |
| Z CAM | [z-cam](references/manufacturer-z-cam.md) |
| ZEISS | [zeiss](references/manufacturer-zeiss.md) |

### Fujifilm X and Ricoh GR model routing

Start with [all X-series identities](references/family-fujifilm-x-series.md) or
[all digital GR identities and editions](references/family-ricoh-gr-series.md).
Load the specific lineage/body below only when it matches the task. Captured versions
and project status are dated observations; resolve the current exact target before use.

| Target | Focused reference |
|---|---|
| Fujifilm Legacy fixed-lens and bridge X cameras | [fujifilm-fixed-legacy](references/fujifilm-fixed-legacy.md) |
| Fujifilm X-A entry line | [fujifilm-x-a](references/fujifilm-x-a.md) |
| Fujifilm X-E rangefinders | [fujifilm-x-e](references/fujifilm-x-e.md) |
| Fujifilm X-H line | [fujifilm-x-h](references/fujifilm-x-h.md) |
| Fujifilm X half / X-HF1 | [fujifilm-x-half](references/fujifilm-x-half.md) |
| Fujifilm X-M line | [fujifilm-x-m](references/fujifilm-x-m.md) |
| Fujifilm X-Pro rangefinders | [fujifilm-x-pro](references/fujifilm-x-pro.md) |
| Fujifilm X-S10 and X-S20 | [fujifilm-x-s](references/fujifilm-x-s.md) |
| Fujifilm X-T100 and X-T200 | [fujifilm-x-t-bayer](references/fujifilm-x-t-bayer.md) |
| Fujifilm X-T compact line | [fujifilm-x-t-compact](references/fujifilm-x-t-compact.md) |
| Fujifilm X-T main line and IR variant | [fujifilm-x-t-main](references/fujifilm-x-t-main.md) |
| Fujifilm X100 fixed-lens line | [fujifilm-x100](references/fujifilm-x100.md) |
| Ricoh GR (2013 APS-C) | [model-ricoh-gr-2013](references/model-ricoh-gr-2013.md) |
| Ricoh GR DIGITAL II | [model-ricoh-gr-digital-ii](references/model-ricoh-gr-digital-ii.md) |
| Ricoh GR DIGITAL III | [model-ricoh-gr-digital-iii](references/model-ricoh-gr-digital-iii.md) |
| Ricoh GR DIGITAL IV | [model-ricoh-gr-digital-iv](references/model-ricoh-gr-digital-iv.md) |
| Ricoh GR DIGITAL | [model-ricoh-gr-digital](references/model-ricoh-gr-digital.md) |
| Ricoh GR II | [model-ricoh-gr-ii](references/model-ricoh-gr-ii.md) |
| Ricoh GR III | [model-ricoh-gr-iii](references/model-ricoh-gr-iii.md) |
| Ricoh GR IIIx | [model-ricoh-gr-iiix](references/model-ricoh-gr-iiix.md) |
| Ricoh GR IV | [model-ricoh-gr-iv](references/model-ricoh-gr-iv.md) |
| Ricoh GR variants, editions and announced models | [ricoh-gr-editions-and-variants](references/ricoh-gr-editions-and-variants.md) |
| Ricoh GR project inventory | [ricoh-gr-project-inventory](references/ricoh-gr-project-inventory.md) |
| Ricoh GRKit: cross-generation card runtime | [ricoh-grkit-runtime](references/ricoh-grkit-runtime.md) |

### Other detailed project/model records

Use these for the named model or mechanism; do not transfer their compatibility to
other bodies in the manufacturer inventory.

| Target | Record |
|---|---|
| Canon EOS 5D / 5D Mark II | [canon-5d-family](references/model-canon-5d-family.md) |
| DJI Osmo / OpenPocketCine | [dji-osmo-pocket](references/model-dji-osmo-pocket.md) |
| Fujifilm X-A2 and XF1 | [fujifilm-x-a2-xf1](references/model-fujifilm-x-a2-xf1.md) |
| Hasselblad X2D 100C / 907X & CFV 100C | [hasselblad-x2d-907](references/model-hasselblad-x2d-907.md) |
| Hasselblad X2D II 400 MP reconstruction | [hasselblad-x2d-ii](references/model-hasselblad-x2d-ii.md) |
| Kodak Charmera / Keychain Camera Plus | [kodak-charmera](references/model-kodak-charmera.md) |
| Leica M8 / M9 / M240 research routes | [leica-m8-m9-m240](references/model-leica-m8-m9-m240.md) |
| Nikon Z30 Wonder Lantern | [nikon-z30](references/model-nikon-z30.md) |
| Olympus PEN-F HSL extension | [olympus-pen-f](references/model-olympus-pen-f.md) |
| OM System OM-1 and related body reports | [om-system-om1](references/model-om-system-om1.md) |
| Panasonic LUMIX DC-S5 remote control | [panasonic-s5](references/model-panasonic-s5.md) |
| Samsung NX1 / NX500 | [samsung-nx1-nx500](references/model-samsung-nx1-nx500.md) |
| Sigma fp / fpSup | [sigma-fp](references/model-sigma-fp.md) |
| Sony PMCA-era cameras | [sony-pmca-era](references/model-sony-pmca-era.md) |

## Completion and stopping conditions

Complete when the requested deliverable exists and its evidence level, target and
limits are explicit. A research request ends with a usable assessment/source record;
a development request requires the requested reviewable implementation and applicable
checks; a device request requires observations of the requested behavior and the
current/restored state, or a precise unresolved prerequisite. Do not substitute references
for an authorized implementation or a build for hardware verification. Stop dependent
device work at a compatibility, authorization or recovery boundary while preserving
safe completed artifacts. After three non-converging diagnostic passes, report the
evidence and next decision instead of repeating writes.

## When not to use

For routine vendor firmware maintenance, follow the vendor's exact update documentation.
For media editing/conversion, use `ffmpeg`; for general photographic technique, answer
that task directly. This skill does not authorize access to someone else's camera,
covert capture, capture-indicator suppression, or incidental persistent debug exposure.
Surveillance/industrial/phone platforms need a separately scoped investigation; do not
pretend the photographic manufacturer inventory covers them.
