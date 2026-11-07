---
name: maxilun-craft
description: >
  Production UI/UX & Brand Identity specialist for design systems, mathematical SVG logo
  construction, Brand Guidelines PDF generation, spatial rhythm, responsive layouts, WCAG
  accessibility, and interaction polish. Combines mathematical scales (4px grid, OKLCH tokens)
  with 100 real-world brand design references (references/design-md/) and 20 art directions.
  Triggers: "/maxilun-craft", "/maxilun-ui", "/msal-craft", "/msal-ui", "desain UI", "buat logo",
  "brand identity", "brand guideline pdf", "sistem desain", "tampilan antarmuka", "responsif",
  "aksesibilitas", "dark mode", "interaksi tombol", or any visual frontend/brand task.
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
    - references/design-md/README.md
    - references/design-md/index.md
    - references/component-mobile-patterns.md
    - references/brand-logo-guidelines.md
---

# Maxilun Craft: UI/UX & Production Design Systems

Bertanggung jawab atas rekayasa visual tingkat produksi: sistem desain konsisten berbasis token semantik OKLCH, tipografi matematis, tata letak responsif 4px grid, aksesibilitas WCAG AA/AAA, serta arsitektur 4 state komponen yang terbebas dari estetika generik AI.

## Skill Contract

- **Owns**: visual direction, mathematical SVG logo design (`logo-mark.svg`, `logo-horizontal.svg`, `logo-mono.svg`, `favicon.svg`), Brand Guidelines PDF (`Brand-Guidelines.pdf`), design tokens, layout, typography, component appearance, interaction states, and design accessibility.
- **Does not own**: React/Next.js runtime architecture (`maxilun-frontend`), general backend/code implementation (`maxilun-engineer`), technical SEO (`maxilun-seo-audit`), or final video rendering (`maxilun-cinecode`).
- **Inputs**: product context (`PRODUCT.md` / `PRD.md`), surface brief, existing `DESIGN.md`, platform constraints, `references/component-mobile-patterns.md`, `references/brand-logo-guidelines.md`, and at most two relevant files from `references/design-md/index.md`.
- **Outputs**: a grounded design direction, mathematical SVG logo suite, print-ready 8-page Brand Guidelines PDF, token/component specifications, implementation-ready UI code, or a visual audit with evidence.
- **Handoff**: send runtime work to `maxilun-frontend`, code changes to `maxilun-engineer`, animated SVG/Lottie logo motion to `maxilun-motion`, MP4/WebM logo reveal video rendering (`<LogoReveal>`) to `maxilun-cinecode`, and verification to `maxilun-verify`.

### Design Reference Contract

The bundled corpus in `references/design-md/` (100 production brand analyses) and `references/component-mobile-patterns.md` is part of this skill, not an external dependency. Read `references/design-md/README.md` and `references/design-md/index.md` before selecting a reference. Select by problem similarity, use no more than two references, and record `References`, `Applied`, `Rejected`, and `Reason` in the design output. Never reproduce a brand identity or use a reference as a substitute for product context.

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

## 0. Design Context Check (Pre-Generation Gate Wajib)

Sebelum menulis kode UI, periksa konteks proyek (`docs/PRD.md`, `docs/DESIGN.md`, `PRODUCT.md`). Tanyakan hanya hal yang belum diketahui dan mengubah keputusan desain secara material.

### 0a. Purity Name & Label Check
Sebelum menamai halaman, menu navigasi, tombol, atau fitur:

| DILARANG (Klise Generik) | WAJIB DIGANTI DENGAN (Fungsi Spesifik) |
|---|---|
| `Dashboard`, `Admin Panel`, `Control Center` | `[Nama Fungsi] Monitor`, `Ringkasan [Aktivitas]`, `Antrean [Entitas]` |
| `Get Started`, `Learn More`, `Explore`, `Submit` | Aksi konkret `<= 3 kata`: `Buat Akun`, `Lihat Harga`, `Kirim Tagihan` |
| `Settings`, `Configuration`, `Preferences` | Konteks spesifik: `Notifikasi Email`, `Akses Tim`, `Metode Pembayaran` |
| `Home`, `Features`, `Pricing`, `About` (Nav Generik) | Objek domain nyata: misal `Topologi Cluster`, `Direktori Klien`, `Katalog API` |
| `Overview`, `Analytics`, `Reports`, `Users` (App Generik) | Workflow harian: `Antrean Tagihan`, `Aktivitas Tim`, `Insiden Aktif` |
| `Powerful`, `Smart`, `AI-Powered`, `Next-Gen`, `Mutakhir` | Hapus klaim kosong; jelaskan fungsi nyata dalam 3–6 kata |
| `Home > ...`, `Dashboard / ...` (Breadcrumb) | **HAPUS BREADCRUMB.** Breadcrumb adalah ciri khas template AI. Gunakan link balik kontekstual tunggal (`← Kembali ke [Induk]`) bila perlu |

### 0b. Visual Direction Declaration (Design Read) & Reference Selection
Sebelum implementasi, deklarasikan satu baris arah visual + catatan referensi dari `references/design-md/index.md` dan 20 Art Directions di `references/component-mobile-patterns.md`:

```text
🔒 DESIGN CONTEXT CHECK
- Design Read: "Reading this as: <page kind> for <audience>, in a <visual direction> style, dial ENERGY X / RHYTHM Y / MOTION Z."
- References: <1-2 files from references/design-md/index.md>
- Applied: <hierarchy, type scale, spacing density, or color roles adapted>
- Rejected: <elements omitted for this product>
- Reason: <audience, task, and platform constraint>
- Verdict: PROCEED / BLOCKED
```
*(Jika belum ada arah dari user, beri label eksplisit **"DRAFT TANPA ARAH"** dengan dial jujur `ENERGY 1 / RHYTHM 1 / MOTION 1` — dilarang diam-diam jatuh ke gradien ungu-biru default AI).*

### 0c. Copywriting Purity Filter (Inline)
Seluruh teks di dalam UI (heading, deskripsi, label input, empty state, toast, error message) wajib mematuhi aturan ini:
1. **Tulis seperti manusia berbicara**, bukan brosur korporat. Satu kalimat = satu ide (`<= 20-25 kata`).
2. **Kata kerja aktif & spesifik**: `"Upload invoice PDF (maks 5MB)"` bukan `"Dokumen dapat diunggah di sini"`.
3. **Bebas em-dash berlebihan & bebas buzzword** dari `../maxilun/references/purity-catalog.md` (butir A.5–A.6).

## 1. Engine Overrides

Delta domain terhadap Core Rules di atas. Override craft:
- **Purity**: Tolak klise visual AI (gradien biru-ungu dekoratif `CLR-001`, glow di semua border, glassmorphism bertumpuk, angka/testimoni palsu). Tunduk pada `../maxilun/references/purity-catalog.md`.
- **Minimalist**: Utamakan CSS native modern (CSS Grid, `@container`, `oklch()`, `<dialog>`, CSS View Transitions) di atas dependency berat.

## Workflow
```mermaid
flowchart LR
    A[§0 Context & Ref Check] --> B[Tokens & Typography]
    B --> C[Layout & Component Patterns]
    C --> D[4 UI States & Mobile Touch]
    D --> E[3-Width Review]
    E --> F[§8 Delivery Gate]
```

**Warisan Konteks**: Periksa apakah `maxilun-knowledge-graph` tersedia untuk memahami struktur komponen yang ada sebelum mengubah UI.

## 2. Fondasi Sistem Desain (Design Tokens & Tipografi)

### 2.1 Skala Spasial (4px Grid) & Hierarki Radius
```css
:root {
  --space-1: 4px;   --space-2: 8px;   --space-3: 12px;  --space-4: 16px;
  --space-6: 24px;  --space-8: 32px;  --space-12: 48px; --space-16: 64px;
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px;
}
```
- **Formula Radius Konsentris**: `radius_inner = max(0, radius_outer - padding)`. Jika Card memakai `16px` dan padding `8px`, tombol/input di dalamnya wajib memiliki radius `8px`, bukan seragam `16px` di semua elemen (`CMP-004`).

### 2.2 Sistem Warna Semantik (Perceptually Uniform OKLCH & Dark Mode)
```css
:root {
  --surface-base:    oklch(98.5% 0.004 250);
  --surface-card:    oklch(100% 0 0);
  --border-hairline: oklch(89% 0.008 250);
  --text-main:       oklch(18% 0.012 250);
  --text-muted:      oklch(46% 0.012 250);
  --brand-primary:   oklch(50% 0.17 255);
  --brand-hover:     oklch(43% 0.17 255);
  --status-success:  oklch(58% 0.16 145);
  --status-warning:  oklch(72% 0.17 75);
  --status-danger:   oklch(56% 0.21 25);
}
```
- **Dark Mode Tanpa Kedip (Flash Prevention)**: Definisikan pasangan token gelap dalam satu sistem, pasang `color-scheme: dark` pada `<html>` saat tema gelap aktif, dan gunakan inline synchronous script di `<head>` sebelum body dirender (lihat detail di `references/component-mobile-patterns.md`).

### 2.3 Tipografi & Disiplin Angka
- Skala: `12px (xs)`, `14px (sm)`, `16px (md/body)`, `18-20px (lg)`, `24-32px (xl)`, `40-56px (display)`.
- `line-height`: Heading `1.15–1.25`, Body `1.5–1.6`, lebar baca paragraf `60ch–75ch`.
- **Wajib `font-variant-numeric: tabular-nums`** pada setiap kolom tabel, harga, waktu, metrik KPI, dan penghitung angka.
- **Standar Tipografi Mikro WIG**: Judul/heading wajib menggunakan `text-wrap: balance` atau `text-pretty`, elipsis unicode `…` (bukan tiga titik biasa `...`), kutip lengkung `“` `”`, dan spasi non-breaking `&nbsp;` pada shortcut (`⌘&nbsp;K`) atau besaran satuan (`10&nbsp;MB`).

## 3. Gerbang Aksesibilitas & Responsivitas (Non-Negotiable)

1. **Kontras WCAG AA/AAA**: Rasio kontras teks biasa minimal `4.5:1` (`7:1` AAA); teks besar minimal `3:1`. Status tidak boleh hanya mengandalkan warna (sertakan ikon/teks).
2. **Navigasi Keyboard & Screen Reader**: Indikator `:focus-visible` wajib jelas; urutan `Tab` logis; semua tombol ikon wajib memiliki `aria-label` deskriptif.
3. **Mobile-First & Touch Target**: Mulai dari `375px` → `768px` → `1440px`. Target sentuh minimal `44x44px` (jarak `>= 8px`), tanpa horizontal overflow, dan ukuran font `<input>` minimal `16px`.
4. **Mikro-Interaksi Taktil**: Durasi `100ms–250ms`, hanya menganimasikan `transform` dan `opacity`, serta wajib mematuhi `@media (prefers-reduced-motion: reduce)`. Tombol aktif mengecil secara taktil (`scale(0.97)`).
5. **Higienitas Form & Layout (WIG Compliance)**: Dilarang mematikan fungsi tempel (`onPaste.preventDefault()`), pasang `spellCheck={false}` pada input kode/token/email/username, flex children dengan teks truncate wajib `min-w-0`, dan modal/drawer wajib `overscroll-behavior: contain`.

## 4. Desain 4 Keadaan UI & 8-State Komponen

Setiap halaman, tabel, list, dan komponen asinkron wajib mengimplementasikan **4 state**:
1. **Loading State**: Skeleton yang meniru proporsi geometri konten final (`CLS = 0`), bukan sekadar spinner di tengah layar.
2. **Empty State**: Penjelasan konkret mengapa data belum ada + tombol aksi pertama (*first action CTA*).
3. **Populated State**: Tampilan data normal yang tahan terhadap teks sangat panjang (`truncate`/`line-clamp`) dan angka ekstrem.
4. **Error State**: Pesan spesifik apa yang gagal (bukan *"Something went wrong"*) + langkah/tombol pemulihan (*Retry* atau jalur alternatif).

Selain itu, elemen interaktif kontrol primer (Button, Input) wajib mendukung **8 state interaktif**: `[Default]`, `[Hover]`, `[Focus-Visible]`, `[Active/Press]`, `[Disabled]`, `[Loading/Spinner]`, `[Error]`, `[Success]`. Serta sertakan minimal **satu interaksi hidup ("One Live Thing")** yang membuktikan nilai domain secara langsung.
## 5. Pola Komponen Produksi, Mobile & 24 Perintah Iteratif

Spesifikasi teknis lengkap untuk implementasi komponen dan interaksi mobile tersedia di `references/component-mobile-patterns.md`:
- **Sistem Navigasi & Menu (§4.0 di referensi)**: Domain-First IA Protocol, Command-Driven Header (`Cmd+K`, sliding pill indicator), Operational Sidebar Rail (workspace switcher, grouped section headers, counter badges, keyboard shortcut tooltips), Ergonomic Mobile Bottom Nav (thumb zone 3–4 item) & Draggable Bottom Sheet Drawer, Contextual Mega-Menu, dan active route indicator (`aria-current="page"`).
- **Tata Letak Otentik & Anti-Cetakan (§4.5 di referensi)**: Asymmetric Bento Grid (`2:1` / `1:2:1`), 4-Level Surface & Elevation Ladder (`Canvas` → `Surface` → `Elevated` → `Overlay`), Typographic Tension & Density Rhythm (kontras tajam Display vs Technical Metadata).
- **Pola Komponen Form & Data (§4.1–§4.4 di referensi)**: Form Validation UX (validasi saat `blur`, `aria-describedby`), Data Tables (sort, filter debounce 300ms, mobile card collapse), File Upload, Toast System (`aria-live`, pause-on-hover), Modal (`<dialog>` focus trap), Multi-Step Wizard, dan Skeleton.
- **Pola Mobile & PWA (§5 di referensi)**: Bottom Sheet (`visualViewport` + `env(safe-area-inset-bottom)`), Bottom Nav (3–5 item), Pull-to-Refresh, Swipe Actions + Undo Toast, dan `inputmode` semantik.
- **24 Perintah Iteratif & 20 Art Directions (§2–§3 di referensi)**: `/maxilun-craft init|shape|build|polish|audit|critique|bolder|quieter|distill|harden|clarify|typeset|colorize|layout|animate|direction|images|review|app|frame`.
- **Desain Logo SVG Matematis, Brand Identity & Brand Guidelines PDF (`references/brand-logo-guidelines.md`)**:
  - Konstruksi 6 varian logo SVG berbasis grid matematis (`64x64`, lulus *1-Bit Monochrome Test* sebelum diberi warna OKLCH, bebas klise ikon bola lampu/roket/otak AI).
  - Kompilasi **8-Page Brand Guidelines PDF (`Brand-Guidelines.pdf`)** vektor tajam menggunakan `@page` CSS Paged Media + headless Chromium (`page.pdf({ printBackground: true })`).
  - Kolaborasi langsung dengan `maxilun-motion` (animasi `stroke-dashoffset` SVG/Lottie) dan `maxilun-cinecode` (`<LogoReveal>` untuk video intro/stinger MP4 & WebM Alpha).

## 6. Gerbang Purity Visual (15 Larangan Mutlak)

Rujukan lengkap: `../maxilun/references/purity-catalog.md`. Hapus segera jika ditemukan:
1. **Breadcrumb (`Home > ...` / `Dashboard / ...`)** — tanda paling mencolok bahwa web di-generate oleh AI (`CMP-001` / `CMP-011`). **Dilarang merender breadcrumb secara default** di semua halaman; gunakan tombol kembali kontekstual tunggal (`← Kembali ke [Nama Halaman Induk]`) hanya jika berada di halaman detail.
2. **Gradien biru-ungu dekoratif** sebagai latar default (`CLR-001`).
3. **Card di dalam card berlebihan** untuk teks sederhana yang cukup dipisah spasi/hairline.
4. **Badge pujian palsu** (*"Powerful"*, *"AI-Powered"*, *"New"*) tanpa dasar faktual (`CMP-002`).
5. **Emoji sebagai pengganti ikon UI** (`CMP-003`).
6. **Border-radius seragam** antara container induk dan elemen anak (`CMP-004`).
7. **Hero klise & tombol kembar simetris** dengan dua CTA primer berdampingan yang saling berebut perhatian (`LAY-010`).
8. **Statistik atau testimoni fiktif** (`"99.9% uptime"`, `"10K+ users"`, avatar acak) tanpa sumber nyata.
9. **Animasi dekoratif tanpa tujuan UX** (floating blobs, glow berkedip, parallax berat).
10. **Layout cetakan AI** (*Hero + 3 Cards identik + Testimonials + FAQ* atau *strip 4 kotak KPI seragam*) (`LAY-008`, `LAY-009`).
11. **Komponen mati / non-fungsional** (tombol search, filter, atau lonceng notifikasi yang tidak bekerja) (`CMP-005`, `CMP-012`).
12. **Navigasi generik & mobile canggung** (menu tanpa nama entitas domain nyata `CMP-010`, menu mobile fullscreen kaku tanpa thumb-zone tab bar/sheet `CMP-013`, item tanpa active indicator `CMP-014`).

## 7. DELIVERY GATE (Wajib Lulus Sebelum Ship)

Jalankan pemeriksaan ini sebelum menyerahkan hasil ke pengguna:

```text
🔒 DELIVERY GATE STATUS
Block A (Context & Reference Record): ✅ PASS / ❌ FAIL (Design Read + 1-2 design-md refs recorded)
Block B (Purity Catalog Compliance):  ✅ PASS / ❌ FAIL (No CLR-001, CMP-001..014, LAY-008..010, or TYPO-001 violations)
Block C (Functional & 4 UI States):   ✅ PASS / ❌ FAIL (Loading skeleton, empty + CTA, populated, error + recovery)
Block D (Navigation, Mobile & A11y):  ✅ PASS / ❌ FAIL (Domain IA, active route state, 375px/768px/1440px, tap >=44px, contrast >=4.5:1)
Block E (Evidence & Copywriting):     ✅ PASS / ❌ FAIL (Zero fake stats, natural copy <=25 words, specific CTAs)
Verdict: SHIP / FIX FIRST
```
**Aturan Keras**: Jika ada satu saja blok yang `FAIL`, perbaiki kodenya terlebih dahulu sebelum menyerahkan hasil.

## Companion Skills Awareness

| Companion | Peran dalam Pekerjaan Ini | Kontribusi Kualitas |
|---|---|---|
| `maxilun-content` | Menyusun copy antarmuka, pesan error, dan empty state | Memastikan teks terdengar manusiawi dan bebas jargon AI |
| `maxilun-frontend` | Mengintegrasikan komponen UI ke arsitektur Next.js RSC & Server Actions | Menjaga batas server/client dan performa bundle tetap optimal |
| `maxilun-motion` | Merancang koreografi animasi berbasis fisika pegas dan aset Lottie/SVG | Memberikan gerak yang fungsional dengan fallback `prefers-reduced-motion` |
| `maxilun-cinecode` | Menggunakan token dan referensi `design-md` untuk merender scene video produk | Menjamin konsistensi identitas visual antara aplikasi web dan video MP4/WebM |
| `maxilun-docsmith` & `maxilun-scaffold` | Mengisi `docs/DESIGN.md` dan matriks 4 state UI di dalam `PRD.md` | Mengikat spesifikasi dokumen langsung ke standar desain produksi |

## Related Skills
- **maxilun-motion**: Animasi interaktif, *Motion DNA*, dan koreografi fisika (`../maxilun-motion/references/index.md`)
- **maxilun-cinecode**: Kompilasi dan render video programatik (`../maxilun-cinecode/references/index.md`)
- **maxilun-frontend**: Arsitektur React Server Components, App Router, dan state management
- **maxilun-content**: Copywriting produk, microcopy, dan panduan suara brand
- **maxilun-docsmith**: Spesifikasi PRD fitur dan dokumentasi teknis (`../maxilun-docsmith/references/index.md`)
- **maxilun-verify**: Pengujian otomatis aksesibilitas, E2E Playwright, dan regresi visual
