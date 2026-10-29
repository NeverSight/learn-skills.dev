---
name: maxilun-scaffold
description: >
  Project context scaffolder. Generates a complete set of AI-readable
  project documents (PRD, TECHSTACK, DESIGN, SECURITY, STYLEGUIDE, TASK,
  ARCHITECTURE, SKILLS, GLOSSARY, ONBOARDING) into a single `docs/` folder
  before coding begins. Grounds PRD invariants in domain archetypes and seeds
  DESIGN.md from the 100 production UI/UX references in maxilun-craft.
  Ensures every AI assistant — Claude, Antigravity, Codex, Cursor, Grok, or any
  other — has instant shared context without re-reading the codebase.
  Triggers: "/maxilun-scaffold", "/msal-init", "scaffold dokumen", "buat docs project",
  "init konteks project", "generate project docs", "siapkan dokumen awal",
  "bikin PRD", "setup dokumentasi project", or any request to bootstrap
  project context files before development begins.
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
    - references/doc-templates.md
    - references/prd-archetypes.md
---

# Maxilun Scaffold: Project Context Generator

Menghasilkan satu set dokumen konteks project yang lengkap ke folder `docs/` sebelum coding dimulai. Dokumen ini menjadi **shared context** yang dibaca semua AI assistant — sehingga tidak perlu menjelaskan ulang stack, aturan, atau tujuan project setiap sesi baru.

## Skill Contract

- **Owns**: initial project-context document structure and baseline context capture (`docs/PRD.md`, `TECHSTACK.md`, `DESIGN.md`, `SECURITY.md`, `STYLEGUIDE.md`, `TASK.md`, `ARCHITECTURE.md`, `SKILLS.md`, `GLOSSARY.md`, `ONBOARDING.md`).
- **Does not own**: detailed architecture decisions, implementation, or final technical documentation.
- **Inputs**: repository context, stated product goals, stack facts, known constraints, `references/prd-archetypes.md`, `references/doc-templates.md`, and at most two relevant design references from `../maxilun-craft/references/design-md/index.md`.
- **Outputs**: a consistent, labeled 10-document project-context set in `docs/` with unknowns preserved and `DESIGN.md` grounded in real UI/UX references.
- **Handoff**: send architecture decisions to `maxilun-architect`, engineering docs and feature specs to `maxilun-docsmith`, UI implementation to `maxilun-craft`, and code implementation to the relevant specialist.

### Reference & UI/UX Grounding Contract

The bundled corpus in `references/index.md`, `references/prd-archetypes.md`, and `references/doc-templates.md` is part of this skill. Before generating `docs/PRD.md` and `docs/DESIGN.md`, read `references/prd-archetypes.md` and `../maxilun-craft/references/design-md/index.md` (plus `../maxilun-craft/references/design-md/README.md`). Select at most two comparable product references from `../maxilun-craft/references/design-md/` based on product domain similarity, translate their hierarchy/typography/OKLCH token principles into `docs/DESIGN.md`, and record `References`, `Applied`, `Rejected`, and `Reason`. Never leave `docs/DESIGN.md` as an empty placeholder when the product category is known.

## 0. Filosofi

> Kode yang baik dimulai dari konteks yang jelas. AI yang baik dimulai dari dokumen yang tepat.

Tanpa konteks tertulis, setiap AI session dimulai dari nol. Dengan `docs/` yang lengkap:
- AI langsung tahu stack, konvensi, invarian domain, dan batasan — tanpa tanya berulang
- Onboarding developer baru dari hari pertama
- Keputusan teknis dan arah visual terdokumentasi di repo, bukan hilang di chat history
- Semua AI platform bekerja dari sumber kebenaran yang sama

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

Delta domain terhadap Core Rules di atas. Override scaffold:
- **Purity**: Dokumen yang dihasilkan harus berisi fakta konkret project ini — bukan template generik yang copy-paste dari mana saja. Placeholder yang masih terbuka harus memakai `[TBD: alasan]`; dalam mode cepat, gunakan `[TBD: perlu konfirmasi pengguna]` lalu rangkum pertanyaan yang belum terjawab. Tunduk pada `../maxilun/references/purity-catalog.md`.
- **Minimalist**: Tidak semua dokumen harus panjang. PRD 1 halaman yang padat invarian lebih baik dari PRD 10 halaman yang tidak dibaca. Setiap bagian harus justify keberadaannya.
- **Clarity**: Gunakan `[CONFIRMED]` untuk fakta yang sudah dipastikan dari repo/user, `[TBD: alasan]` untuk hal yang belum diputuskan, dan `[ASSUMED]` untuk asumsi domain yang belum divalidasi.

## Workflow

```mermaid
flowchart LR
    A[Discovery & Repo Scan] --> B[Archetype & UI Ref Match]
    B --> C[Adaptive Interview]
    C --> D[Generate 10 Docs]
    D --> E[Quality Gate]
    E --> F[Update per Milestone]
```

## 2. Fase Discovery — Sebelum Generate

Sebelum menghasilkan dokumen apapun, scaffold wajib mengumpulkan konteks melalui:

### 2.1 Scan Otomatis (jika project sudah ada)
Baca file-file berikut jika tersedia:
- `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml` → stack detection (`[CONFIRMED]`)
- `README.md`, `README*.md`, `docs/*` → existing context
- `.env.example`, `docker-compose.yml`, `Dockerfile` → infrastruktur & variabel lingkungan
- `src/`, `app/`, `lib/`, `prisma/`, `drizzle/` → struktur modul & skema data
- Git log (5 commit terakhir) → momentum dan konteks terkini

### 2.2 Pemetaan Archetype & Referensi UI/UX
Cocokkan hasil scan atau deskripsi awal user dengan `references/prd-archetypes.md`:
1. Tentukan kategori domain: **Fintech/Payment**, **B2B SaaS/Workflow**, **DevTools/AI**, **E-Commerce/Booking**, atau **Media/EdTech**.
2. Pilih 1–2 file referensi dari `../maxilun-craft/references/design-md/index.md` yang sesuai dengan kategori tersebut untuk mengisi fondasi `docs/DESIGN.md` dan persyaratan state UI di `docs/PRD.md`.

### 2.3 Interview Adaptif
Hanya tanya informasi yang **tidak bisa disimpulkan** dari scan. Format pertanyaan:

```text
📋 Saya akan men-generate 10 dokumen konteks di docs/.
   Berdasarkan scan awal, berikut beberapa hal yang perlu dikonfirmasi:

   1. Apa tujuan utama project ini dan masalah konkret yang diselesaikan? (1-2 kalimat)
   2. Siapa pengguna utamanya (role/persona) dan di perangkat apa mereka paling sering bekerja?
   3. Stack yang PASTI dipakai? (yang belum diputuskan akan saya tandai [TBD: alasan])
   4. Ada batasan khusus (timeline, compliance UU PDP/PCI-DSS, atau arsitektur wajib)?
   5. Apakah ada preferensi arah visual/brand, atau gunakan rekomendasi dari referensi UI/UX Maxilun?
```

Jika sudah ada README atau brief yang jelas, lewati pertanyaan yang sudah terjawab.

### 2.4 Mode Cepat (`--quick`)
Jika user menambah flag `--quick` atau `cepat`, lewati interview — pilih archetype terdekat dari `references/prd-archetypes.md`, pilih referensi desain yang sesuai dari `../maxilun-craft/references/design-md/index.md`, generate ke-10 dokumen dengan label `[ASSUMED]` atau `[TBD: perlu konfirmasi pengguna]`, lalu tampilkan ringkasan asumsi di akhir.

## 3. Output: 10 Dokumen di `docs/`

Semua dokumen digenerate ke folder `docs/` di root project menggunakan struktur kanonik di `references/doc-templates.md`:

```text
docs/
├── PRD.md            # Product requirements, user stories (Gherkin), 4 UI states, non-goals, KPIs
├── TECHSTACK.md      # Stack, versi, alasan pemilihan, alternatif ditolak, env vars
├── DESIGN.md         # Visual direction, Design Reference Record (maxilun-craft), OKLCH tokens, 4px grid
├── SECURITY.md       # Threat model STRIDE spesifik domain, auth/authz, kriptografi, PII policy
├── STYLEGUIDE.md     # Konvensi penamaan, batas kompleksitas (<=300 baris), error handling, git rules
├── TASK.md           # Milestone goal, max 3 active tasks, prioritized backlog, blockers
├── ARCHITECTURE.md   # Diagram C4 L1/L2 (Mermaid), module boundaries, alur data, ringkasan ADR
├── SKILLS.md         # Peta spesialis Maxilun aktif di project ini & ringkasan cepat untuk AI
├── GLOSSARY.md       # Ubiquitous language (istilah bisnis kanonik & sinonim yang dilarang)
└── ONBOARDING.md     # Urutan baca untuk AI assistant & langkah setup lokal terverifikasi untuk engineer
```

## 4. Aturan Penyusunan Tiap Dokumen Inti

Baca template lengkap di `references/doc-templates.md` dan terapkan aturan pengisian berikut:

### 4.1 `PRD.md` (Terikat Domain & UI States)
- **Problem Statement**: Wajib menyebutkan rasa sakit yang terukur (waktu terbuang, risiko finansial, atau frekuensi error), bukan kalimat abstrak.
- **Fitur MVP**: Setiap fitur wajib memiliki *Acceptance Criteria* deterministik (Given/When/Then) dan mewajibkan 4 state UI (Loading skeleton, Empty state + CTA, Populated state, Error state + recovery) yang merujuk ke `DESIGN.md`.
- **Out of Scope (Non-Goals)**: Wajib mencantumkan minimal 2 fitur yang sengaja ditolak/ditunda pada fase ini agar scope tidak melebar.
- *Catatan*: Jika user hanya meminta pembuatan/pembaruan spesifikasi teknis mendalam untuk satu fitur baru (RFC / Feature PRD + spesifikasi OpenAPI) pada project yang sudah berjalan, arahkan atau kolaborasikan dengan `maxilun-docsmith` (`../maxilun-docsmith/references/prd-rfc-specs.md`).

### 4.2 `DESIGN.md` (Terintegrasi Referensi `maxilun-craft`)
- Wajib membaca `../maxilun-craft/references/design-md/index.md` dan mencantumkan blok **Design Reference Record** (`References`, `Applied`, `Rejected`, `Reason`, dan deklarasi `Design Read`).
- Turunkan token warna semantik `oklch()`, skala tipografi, `tabular-nums` (untuk tabel/angka), dan hierarki `border-radius` (anak `<=` induk) berdasarkan masalah produk, bukan template AI default (tolak gradien ungu-biru dekoratif).

### 4.3 `ARCHITECTURE.md`, `TECHSTACK.md` & `SECURITY.md`
- Selaraskan batas modul di `ARCHITECTURE.md` dengan folder nyata di repo (`src/`, `app/`, `core/`, `db/`).
- Setiap teknologi di `TECHSTACK.md` wajib mencantumkan kolom **Alternatif Ditolak** beserta alasannya.
- Ancaman STRIDE di `SECURITY.md` wajib spesifik terhadap archetype produk di `references/prd-archetypes.md` (misal: manipulasi harga/idempotency untuk e-commerce/fintech; kebocoran lintas-tenant IDOR untuk B2B SaaS).

## 5. Mode Update (`--update`)

Jika project sudah berjalan dan butuh sinkronisasi dokumen terhadap perubahan kode:

```bash
/maxilun-scaffold --update
```

**Prosedur**:
1. Bandingkan isi `docs/` saat ini dengan kondisi terbaru repositori (`package.json`, skema DB, route baru, dan `git log`).
2. Identifikasi bagian dokumen yang tidak lagi sinkron dengan kode aktual.
3. Perbarui fakta yang sudah pasti berubah (`[CONFIRMED]`), pertahankan keputusan yang masih valid, dan tandai bagian yang ambigu dengan `[STALE: perlu konfirmasi]`.
4. Jika ada penambahan endpoint publik atau README utama perlu disinkronkan, handoff ke `maxilun-docsmith`.

## 6. Integrasi Lintas-Spesialis Maxilun

| Dokumen di `docs/` | Bootstrap Awal | Spesialis Pengembang & Validator Lanjutan |
|---|---|---|
| `PRD.md` | `maxilun-scaffold` | `maxilun-docsmith` (Feature PRD/RFC detail), `maxilun-content` (microcopy) |
| `DESIGN.md` | `maxilun-scaffold` (via corpus `maxilun-craft`) | `maxilun-craft` (implementasi UI, audit 4 state & aksesibilitas) |
| `TECHSTACK.md` & `ARCHITECTURE.md` | `maxilun-scaffold` | `maxilun-architect` (keputusan ADR kritis, batas sistem), `maxilun-diagrams` |
| `SECURITY.md` | `maxilun-scaffold` | `maxilun-sentinel` (threat modeling mendalam & audit kode keamanan) |
| `STYLEGUIDE.md` | `maxilun-scaffold` | `maxilun-engineer` (penegakan code hygiene & refactoring) |
| `ONBOARDING.md` & `SKILLS.md` | `maxilun-scaffold` | `maxilun-deploy` (CI/CD & Docker), `maxilun-docsmith` (`README.md` & `llms.txt`) |

## Companion Skills Awareness

`maxilun-scaffold` menghasilkan 10 dokumen konteks project secara mandiri. Pilih companion hanya bila bagian deliverable membutuhkan keputusan spesialis:

| Companion | Scaffold's Role | Purity & Quality Contribution |
|---|---|---|
| `maxilun-craft` | Menggunakan `../maxilun-craft/references/design-md/index.md` untuk `DESIGN.md` | Mencegah `DESIGN.md` berisi token kosong atau estetika AI generik |
| `maxilun-docsmith` | Handoff untuk Feature RFC, OpenAPI spec, `README.md`, dan `llms.txt` | Memastikan kontrak API dan dokumentasi engineer akurat hingga level skema |
| `maxilun-architect` | Validasi batas modul dan ADR di `ARCHITECTURE.md` | Memastikan diagram C4 dan aturan impor sesuai arsitektur nyata |
| `maxilun-content` | Penyuntingan bahasa produk dan value proposition di `PRD.md` | Mencegah bahasa brosur korporat pada deskripsi produk |

## 7. Delivery Gate Kualitas Dokumen

Sebelum menyerahkan hasil `docs/` ke pengguna, verifikasi seluruh checklist ini:

- [ ] Ke-10 file di `docs/` terbentuk lengkap mengikuti struktur `references/doc-templates.md`.
- [ ] Tidak ada klaim tanpa ukuran/bukti (`"performansi tinggi"`, `"sangat aman"` dihapus atau diganti target konkret).
- [ ] Setiap `[TBD: alasan]` mencantumkan alasan jelas mengapa belum diputuskan.
- [ ] `docs/PRD.md` memiliki kriteria penerimaan deterministik, matriks 4 state UI, dan bagian *Out of Scope (Non-Goals)*.
- [ ] `docs/DESIGN.md` menyertakan blok **Design Reference Record** yang merujuk ke `../maxilun-craft/references/design-md/index.md`.
- [ ] Seluruh nama script dan environment variable di `TECHSTACK.md` dan `ONBOARDING.md` cocok dengan file konfigurasi repositori jika kode sudah ada.

## Related Skills
- **maxilun-docsmith**: Spesifikasi fitur/RFC mendalam, kontrak OpenAPI/AsyncAPI, runbook, ADR, dan `llms.txt`
- **maxilun-craft**: Pemilik utama sistem desain UI/UX dan penyedia 100 referensi di `../maxilun-craft/references/design-md/`
- **maxilun-architect**: Desain arsitektur mendalam, kontrak antar-modul, dan ADR
- **maxilun-sentinel**: Audit keamanan aplikasi dan threat modeling STRIDE
- **maxilun-content**: Copywriting produk dan microcopy antarmuka
