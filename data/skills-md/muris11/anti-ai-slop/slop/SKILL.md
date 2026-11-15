---
name: slop
description: "One-shot loader for the full anti-ai-slop family. Invoke when the user says 'slop', 'anti slop', 'antislop semua', or wants every anti-ai-slop skill active at once for UI, copy, code, mobile, dashboard, motion, or accessibility work. Loads: antislop (core), antislop-master, antislop-ui, antislop-layout, antislop-copywriting, antislop-human, antislop-layoutmobile, antislop-mobile, antislop-dashboard, antislop-forms, antislop-motion, antislop-nav, antislop-authenticity, antislop-designsystem, antislop-imagery, antislop-code."
---

# slop

Load ALL anti-ai-slop skills at once, then follow them for the rest of the session.

## Steps

1. Invoke each skill via the skill tool, one after another, in this order:
   - `antislop` (core filter)
   - `antislop-master` (the P0–P6 taxonomy catalog)
   - `antislop-ui`
   - `antislop-layout`
   - `antislop-copywriting`
   - `antislop-human`
   - `antislop-layoutmobile`
   - `antislop-mobile`
   - `antislop-dashboard`
   - `antislop-forms`
   - `antislop-motion`
   - `antislop-nav`
   - `antislop-authenticity`
   - `antislop-designsystem`
   - `antislop-imagery`
   - `antislop-code`

2. Follow the core `antislop` rules from there, with all the sub-skills' rules active simultaneously. For a broad audit, start from `antislop-master`. No re-asking which sub-skill to install; the user already chose "all".

3. If any skill fails to load or is missing, report which one, continue with the rest.

Usage-mode question from core antislop still applies: ask the user (in their chat language) whether antislop applies during the work or after it is done, before starting.

## Custom Bans (user-specific, applies on top of the antislop skills)

These patterns are FORBIDDEN in ANY UI this session produces, without exception, for every screen and every component. Run alongside the UI Skill Checklist; a FAIL on any of these fails the Delivery Gate. "Specific example" is illustrative only — the rule applies to ALL instances, not just the named ones.

### Dot / Status Indicator Badges

- **Tell:** pill badge with a small colored dot plus a label and a count, e.g. `• Aktif 21`, `• Lulus 1.389`, `• Pending 4`.
- **Why:** the dot-plus-count badge is the default status decoration. The dot adds no information, and a bare count without a defined basis is a number with no story behind it (R-17, R-31).
- **Fix:** remove the dot entirely. Use a plain text label (`Aktif 21`). No dot, no colored status indicator dot, no status dot badge (R-01).

### Sparkles Icon

- **Tell:** the sparkles glyph anywhere in the UI: `✨` emoji, Material Symbols `auto_awesome`, Lucide `sparkles`.
- **Why:** it is the generic "AI magic" glyph. It communicates nothing about the specific feature (R-04).
- **Fix:** delete it. No sparkles glyph anywhere, no exceptions (R-04).

### Uppercase Tracked Label Card (e.g. "PROGRAM AKTIF")

- **Tell:** a small uppercase label with wide letter-spacing used as a card/section header, e.g. `PROGRAM AKTIF`, `FEATURES`, `HOW IT WORKS`.
- **Why:** wide-tracked uppercase is the default AI typography shortcut for "modern and technical"; it does no real typographic work (R-06).
- **Fix:** use sentence case. No wide-tracked uppercase labels, no exceptions (R-06).

### Text Wrapped in Decorative Containers / Cards / Grids

- **Tell:** ANY word, short label, tag, status, category, or number placed inside a bordered, tinted, pill, chip, card, or grid cell just to give it "shape". This includes every tag and label chip: `SENBUD`, `PRESTASI MANDIRI`, `RISNOV`, `UMUM`, `SERTIFIKASI`, `TERVERIFIKASI`, `DITOLAK`, `Aktif`, `Pending`, `Tersalurkan`, `Proyeksi`, `Pengajuan`, `1 Pendaftar`, `<= 3 hari`. Plus any text boxed purely because a container was available.
- **Why:** when text is boxed purely to look "designed", every container is decoration with no information. This is the single most common AI-slop UI tell: the model wraps categories, statuses, and numbers in colorful chips and cards to feel structured, and it reads as slop the moment the box adds nothing (R-01, R-09, R-14, R-31).
- **Fix:** let the text be text. Plain label, plain list, or plain inline tags separated by space or comma. NO chip, NO pill, NO tinted tag, NO badge, NO bordered box around a data value — none of it. If you find yourself wrapping a value in a colored box to make it look like a dashboard, you are generating AI slop (C-1).

### Capsule / Pill Badges (ANY)

- **Tell:** ANY element shaped as a capsule or pill used as a badge, tag, status, chip, or label — a fully-rounded (border-radius = 9999px or similar) shape containing text — for ANY purpose: status pills, category chips, count badges, "AI Powered"/"Beta"/"New" capsules, the "Most Popular" badge on a pricing card, a pill toggle, a pill button, a pill label. Capsule shape = text wrapped in a fully-rounded container.
- **Why:** the capsule/pill is the single most recognizable AI-slop shape. It is the default container the model reaches for to make any label, status, or count feel "badge-like", and it reads as generated the moment the rounding exists for decoration, not for a real function (R-01, R-09, R-11, R-31).
- **Fix:** remove the capsule/pill shape entirely. Use plain text, a rectangular design-system component with the correct radius from `DESIGN.md`, or no container at all. NO fully-rounded badge/pill/chip/capsule anywhere (C-1).
