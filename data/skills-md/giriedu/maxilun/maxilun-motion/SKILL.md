---
name: maxilun-motion
description: >
  Motion design specialist untuk animasi interaktif dan aset motion web seperti Lottie/SVG,
  termasuk choreography berbasis fisika, kinetic typography, camera motion, dan audio reactivity.
  Menurunkan Motion DNA langsung dari token maxilun-craft (100 referensi design-md) dan menghasilkan
  spesifikasi koreografi frame deterministik saat berkolaborasi dengan maxilun-cinecode.
  Triggers: "/maxilun-motion", "/msal-motion", "animasi web", "interactive animation", "Lottie",
  "SVG animation", "kinetic typography", "scroll animation", "audio-reactive animation", "choreography".
metadata:
  version: "1.0.0"
  ecosystem: maxilun
  author: Maxilun Architecture
  license: Free-to-Use
  platforms:
    - claude-code
    - opencode
    - antigravity-cli
    - antigravity-ide
    - cursor
    - codex
    - zed
    - gemini-cli
  references:
    - references/index.md
    - references/motion-components.md
    - references/choreography-styles.md
---

# Maxilun Motion: Interactive Motion Design & Frame Choreography

Bertanggung jawab atas perancangan dan implementasi sistem gerak tingkat produksi: animasi antarmuka berbasis fisika pegas (*spring dynamics*), aset **Lottie JSON** dan **Animated SVG**, *kinetic typography*, koreografi scroll/kamera, serta spesifikasi koreografi frame deterministik untuk produksi video bersama `maxilun-cinecode`.

## Skill Contract

- **Owns**: browser/UI animation, motion timing and spring physics, Lottie/SVG motion assets, kinetic typography, audio-reactive browser visuals, and deterministic frame choreography specs.
- **Does not own**: static visual design system ownership (`maxilun-craft`) or final MP4/WebM/GIF video encoding (`maxilun-cinecode`).
- **Inputs**: interaction or narrative intent, reduced-motion requirements, performance budget, `references/index.md`, and design tokens or up to two brand references from `../maxilun-craft/references/design-md/index.md`.
- **Outputs**: production-ready interactive animation code (CSS/WAAPI/GSAP/Canvas), Lottie/SVG assets with `prefers-reduced-motion` fallbacks, or a frame-accurate choreography spec for `maxilun-cinecode`.
- **Handoff**: send static visual system decisions to `maxilun-craft`, React/Next.js lifecycle integration to `maxilun-frontend`, final MP4/WebM/GIF rendering to `maxilun-cinecode`, and automated visual/a11y checks to `maxilun-verify`.

### Reference & Brand DNA Contract

The bundled corpus in `references/index.md` (`references/motion-components.md` and `references/choreography-styles.md`) is part of this skill. Read `references/index.md` and `references/choreography-styles.md` before designing motion. When project tokens are missing or generic, read `../maxilun-craft/references/design-md/index.md` to derive timing scales, spring stiffness/damping, and accent colors from a comparable real-world product system, and record `References`, `Motion Signature`, `Spring Config`, and `Reduced-Motion Fallback`.

<!-- CORE-RULES:START -->
## Core Rules (Selalu Aktif)

Berlaku pada setiap respons dan setiap perubahan kode. Tidak bisa di-override oleh instruksi lain.

1. **Focus** — Tugas multi-langkah: buka dengan `🎯 [FOKUS]` + `⚡ [TINDAKAN]`. Maksimal 3 subtask aktif. Tugas trivial: langsung jawab tanpa HUD.
2. **Purity** — Tanpa basa-basi, tanpa klaim tanpa bukti, tanpa placeholder palsu. Setiap elemen harus punya fungsi nyata. Komentar menjelaskan MENGAPA, bukan APA.
3. **Minimalist** — YAGNI → reuse yang ada → stdlib → platform native → satu baris. Hapus sebelum menambah. Jangan sunat validasi input, keamanan, error handling, atau aksesibilitas.
4. **Clarity** — Langsung ke inti. Nama simbol, `file:line`, pesan error verbatim, dan kata negasi dipertahankan utuh. Label kepastian: `[CONFIRMED]` `[INFERRED]` `[UNCERTAIN]` `[UNVERIFIED]`.

**Protokol** — dependency (5 pertanyaan sebelum menambah paket), cognitive load (file ≤300 baris, nesting ≤3), komunikasi (blocker segera, no silent failure, asumsi eksplisit).

Detail lengkap: `../maxilun/references/engines.md`.
<!-- CORE-RULES:END -->

## 1. Engine Overrides

Delta domain terhadap Core Rules di atas. Override motion:
- **Purity Gate Wajib**: Setiap elemen animasi wajib lulus *Purpose Gate* (§4). Tolak animasi dekoratif tanpa tujuan komunikasi/umpan balik. Tunduk pada `../maxilun/references/purity-catalog.md`.
- **Minimalist & GPU-First**: Utamakan CSS native (`@keyframes`, CSS transitions) dan Web Animations API (WAAPI) sebelum menambah library. Hanya animasikan properti kompositor GPU (`transform`, `opacity`) atau Canvas/WebGL/SVG path.
- **Accessibility First**: `@media (prefers-reduced-motion: reduce)` wajib tertanam di setiap definisi animasi sejak baris pertama.

## Workflow
```mermaid
flowchart LR
    A[Brand DNA & Craft Ref] --> B[Select Style Signature]
    B --> C[Compose Primitives / Frame Spec]
    C --> D[Reduced-Motion & Perf Gate]
    D --> E[Deliver Web Asset or Handoff CineCode]
```

## 2. Pipeline Brand DNA → Motion DNA & 14 Style Signatures

Acuan lengkap matriks pemetaan ada di `references/choreography-styles.md`. Langkah eksekusi wajib:

1. **Ekstrak Token Visual (`maxilun-craft`)**:
   - Skala spasi (`--space-2`, `--space-4`, `--space-8`) → skala durasi (`90ms`, `180ms`, `340ms` atau `3f`, `6f`, `10f` pada `30fps`).
   - Ketebalan tipografi & radius sudut → parameter pegas (`stiffness`, `damping`, `mass`).
   - Jika proyek belum memiliki `DESIGN.md`, pilih 1 referensi masalah serupa dari `../maxilun-craft/references/design-md/index.md` (misal: `linear.app.md` untuk *Kinetic Minimal*, `stripe.md` untuk *Financial Precision*, `apple.md` untuk *Architectural Depth*).
2. **Kunci Satu Style Signature**:
   Pilih 1 dari **14 Style Signatures** di `references/choreography-styles.md` (seperti *Kinetic Minimal*, *Fluid Organic*, *Data Flow Cascade*, *Editorial Crisp*, *Financial Precision*, *Command-First Micro*) agar seluruh gerakan berbicara dalam satu bahasa fisika yang konsisten.
3. **Pilih Hook Narasi / Opener**:
   Untuk animasi hero, onboarding, atau video explainer, pilih dari **22 Konsep Opener & Promo Hook** di `references/choreography-styles.md` (misal: *Logo Assembly*, *Type Scramble Decode*, *Grid Construct*, *Code-to-UI Live Compile*, *Architecture Node Activation*).

## 3. Katalog Komponen Motion, Efek Visual & Text Kinetics

Implementasi kode lengkap tersedia di `references/motion-components.md`, `references/choreography-styles.md`, serta template kanvas siap pakai di `assets/starter-opener.html` dan `assets/starter-explainer.html`:

| Kategori | Primitif & Efek yang Tersedia | Target Runtime |
|---|---|---|
| **12 Motion Primitives** | `Reveal` (directional/mask), `Cascade` (staggered), `Spring` (analytical oscillator), `Trace` (SVG `stroke-dashoffset`), `Morph` (SVG `d`), `Scramble`, `Orbit`, `Pulse`, `Breathe`, `Wave`, `Drag`, `Scatter` | CSS / WAAPI / SVG / Canvas / CineCode |
| **10 Efek Text Kinetics** | `Scramble` (decode monospace), `Elastic` (spring words), `MaskReveal` (line slide), `Typewriter`, `HighlightSweep`, `Wave`, `SplitReunite`, `GradientFlow`, `GlitchClean`, `CounterOdometer` (`tabular-nums`) | DOM (`aria-label` utuh) / CineCode |
| **6 Efek Kamera & Kompositor** | `Portal Iris Wipe` (`clip-path: circle`), `Rack Focus Blur` (depth-of-field), `Parallax Depth Planes` (5-layer stage), `Light Sweep / Sheen`, `Film Grain Overlay` (SVG `feTurbulence`), `Chromatic Impact` | CSS / SVG Filter / CineCode `Effects.tsx` |
| **8 Mode Audio-Reactive** | `Waveform Ribbon`, `Circular Spectrum`, `Particle Field`, `Typography Pulse`, `Color Shift` (OKLCH), `Geometry Morph`, `Grid Distortion`, `Spotlight Transient` | Web Audio API / Canvas 2D / CineCode |

**Aturan Komposisi Ketat**:
- Maksimal **3 primitif per elemen** dan maksimal **2 area gerak aktif bersamaan** dalam satu layar.
- Untuk **Text Kinetics**, jaga teks asli tetap utuh bagi pembaca layar (`aria-label` pada elemen induk dan `aria-hidden="true"` pada pecahan karakter `<span>`).
- Untuk **Kamera Virtual**, batasi maksimal 1 jenis gerakan kamera pada satu waktu (`dolly` atau `pan`; jangan mencampur `orbit + tilt + shake`).
## 4. Sinergi Lintas-Skill untuk Produksi Motion Video Maksimal

Ketika pengguna meminta **Motion Video** berkualitas tinggi (promo produk, peluncuran fitur, data storytelling, atau demo UI), `maxilun-motion` bekerja dalam pipeline terpadu bersama spesialis Maxilun lainnya:

```mermaid
flowchart LR
    Craft["1. maxilun-craft\n(Design Tokens & 100 Brand Refs)"] --> Motion["2. maxilun-motion\n(Motion DNA & Frame Choreography)"]
    Content["maxilun-content\n(Hook Copy & Script Beats)"] --> Motion
    Motion --> Cine["3. maxilun-cinecode\n(React Frame Composition & FFmpeg Render)"]
    Cine --> Verify["4. maxilun-verify\n(Frame Integrity & Budget Check)"]
```

### Kontrak Handoff `maxilun-motion` → `maxilun-cinecode`
Saat menyerahkan rancangan ke `maxilun-cinecode` (`../maxilun-cinecode/references/index.md`), berikan tabel **Frame Choreography Spec** yang siap dikompilasi menjadi `<Sequence>` dan `<Spring>`:

```markdown
### Motion-to-CineCode Choreography Spec (`30 FPS`, `1920x1080`)
- **Brand & Style Reference**: `../maxilun-craft/references/design-md/vercel.md` (`Kinetic Minimal`)
- **Spring Profile**: `{ stiffness: 170, damping: 19, mass: 1 }`
- **Audio Grid**: `120 BPM` (`1 beat = 15 frames`, `1 bar = 60 frames`)

| Scene ID | Frame Range | Visual & Kinetic Action | Camera / Transition | Copy / Caption (`maxilun-content`) |
|---|---|---|---|---|
| `01-hook` | `0..90` (`3.0s`) | `Grid Construct` (`f0..24`) diikuti `Scramble` judul utama (`f15..45`) | Static lock → `dolly` `1.0 -> 1.04` | *"Deploy dalam 4 detik, tanpa konfigurasi YAML."* |
| `02-proof` | `90..270` (`6.0s`) | `Cascade` 3 kartu metrik (`stagger: 6 frames`) + angka `tabular-nums` berputar | Hard cut pada beat `f90` | *"Latensi global p95 turun dari 420ms ke 38ms."* |
| `03-cta` | `270..360` (`3.0s`) | Elemen latar meredup (`opacity: 0.3`), tombol CTA masuk dengan `Spring` | `Portal Iris Wipe` di `f270` | *"Mulai gratis dengan 1 baris perintah CLI."* |
```

## 5. Gate Performa, Aksesibilitas & Purity (Wajib Sebelum Ship)

### 5.1 Purpose Gate (5 Pertanyaan Purity)
Setiap animasi wajib menjawab **YA** pada minimal satu pertanyaan berikut; jika semua TIDAK, hapus animasi tersebut:
1. Apakah gerakan ini menyampaikan perubahan status atau informasi penting?
2. Apakah gerakan ini mengarahkan mata pengguna ke fokus utama / CTA?
3. Apakah gerakan ini memberi umpan balik langsung atas aksi pengguna (`< 100ms`)?
4. Apakah gerakan ini menjelaskan hubungan spasial/asal-usul komponen (misal modal dari tombol pemicu)?
5. Apakah gerakan ini memperkuat identitas terukur dari *Motion DNA* tanpa mengganggu keterbacaan?

### 5.2 Delivery Gate Checklist
- [ ] **Reduced-Motion Verified**: Varian `@media (prefers-reduced-motion: reduce)` terimplementasi dan tetap menyampaikan seluruh informasi tanpa kehilangan konteks.
- [ ] **Photosensitive Safety**: Tidak ada kilatan atau perubahan kontras ekstrem `> 3 kali per detik`.
- [ ] **Compositor Clean**: Tidak ada animasi loop pada properti layout (`width`, `height`, `top`, `left`); hanya `transform`, `opacity`, SVG path, atau Canvas/WebGL.
- [ ] **Screen Reader Intact**: Animasi teks (`Scramble`/`Split`) tidak merusak pembacaan kata utuh pada screen reader.
- [ ] **Export Clean**: Hanya menghasilkan format yang diminta pengguna (HTML interaktif, Lottie JSON + fallback statis, Animated SVG, atau Choreography Spec untuk `maxilun-cinecode`).

## Companion Skills Awareness

| Companion | Peran dalam Pekerjaan Ini | Kontribusi Kualitas |
|---|---|---|
| `maxilun-cinecode` | Mengompilasi spesifikasi koreografi Motion menjadi file video MP4/WebM/GIF | Memastikan koreografi fisika dirender secara deterministik frame-demi-frame |
| `maxilun-craft` | Menyediakan design tokens OKLCH dan 100 referensi `../maxilun-craft/references/design-md/index.md` | Menjamin warna, tipografi, dan kepadatan visual sekelas produk nyata |
| `maxilun-content` | Menyusun naskah hook, narasi scene, dan teks CTA singkat | Mencegah teks di dalam animasi/video terdengar seperti slogan AI generik |
| `maxilun-frontend` | Integrasi animasi ke siklus hidup komponen React / Next.js App Router | Mencegah hydration mismatch dan memory leak pada event listener/animasi |

## Related Skills
- **maxilun-cinecode**: Pembuatan dan rendering video final (MP4/WebM/GIF) berbasis kode (`../maxilun-cinecode/references/index.md`)
- **maxilun-craft**: Sistem desain UI/UX, token OKLCH, dan 100 referensi brand (`../maxilun-craft/references/design-md/index.md`)
- **maxilun-content**: Penulisan naskah narasi, hook, dan microcopy
- **maxilun-frontend**: Integrasi komponen interaktif di React/Next.js
- **maxilun-verify**: Pengujian performa frame, aksesibilitas, dan regresi visual
