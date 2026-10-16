---
name: nle-export
description: 'Hand a cut built from the user''s own footage to a professional editor as an FCPXML, XML or EDL that references the original files, for Adobe Premiere Pro, Final Cut Pro or DaVinci Resolve finishing. Uses Reelary (local, Mac or Windows). Trigger on "export to Premiere", "export to Final Cut", "send to DaVinci Resolve", "FCPXML", "EDL", "XML timeline", "roundtrip to my NLE", "AI rough cut then finish in Resolve". Not for converting existing NLE projects between formats.'
---

# NLE export

## Steps

1. Make sure a project exists: build one with [rough-cut](../rough-cut/SKILL.md) or ask which saved project to use.
2. Pick the format: `fcpxml` for Final Cut Pro and DaVinci Resolve, `xml` for Premiere Pro (FCPXML import), `edl` as the universal fallback.
3. Call `reelary_export_nle` with `project_id` and `format`. Give the user the file path and the import menu: Premiere File > Import, Final Cut File > Import > XML, Resolve File > Import > Timeline.
4. The timeline links to the original files on this computer, so import on the same machine (or relink).

## Without MCP

`npx -y reelary export <project_id> --nle fcpxml`

## Notes

- NLE export is a Pro feature. On `pro_required`, explain and share the upgrade link once; MP4 export ([rough-cut](../rough-cut/SKILL.md)) works on the free plan.
- If the `reelary_*` tools are missing, use the [reelary](../reelary/SKILL.md) skill first.
