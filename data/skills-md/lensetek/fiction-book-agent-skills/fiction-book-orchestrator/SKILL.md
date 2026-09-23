---
name: fiction-book-orchestrator
description: Coordinator and workflow manager for end-to-end fiction writing, novels, comics, webtoons, and children's storybooks. Use when starting a new fiction project or coordinating multi-stage story creation.
---

# Fiction Book Orchestrator

Koordinator dan pengelola alur kerja penulisan karya fiksi, novel, cerita anak, komik/webtoon, dan naskah fiksi kreatif. Agen ini memandu penulis dari ide awal, pematangan konsep, *worldbuilding*, penyusunan tokoh, arsitektur plot, penulisan draf adegan, hingga penyempurnaan kontinuitas dan penataan letak (*layout export*) untuk cetak & digital.

---

## Workflow Phases & Skill Routing

Ketika pengguna memulai proyek fiksi baru atau meminta bantuan membuat novel/komik/cerita anak, jalankan alur kerja bertahap berikut:

```mermaid
graph TD
    A[Phase 1: Story Concept Intake] --> B[Phase 2: Worldbuilding & Character Psychology]
    B --> C[Phase 3: Plot Architecture & Scene Beats]
    C --> D[Phase 4: Scene Drafting & Editing]
    D --> E[Phase 5: Continuity, Polish & Publisher Export]
```

### Phase 1: Intake & High-Concept Clarification
1. Panggil **`story-concept-intake`** untuk menggali genre, sub-genre, *high-concept logline*, demografi pembaca, *core trope*, dan tema emosional utama.
2. Buat dokumen `story_brief.md` di direktori proyek.
3. Minta persetujuan Penulis (*HITL Gate 1*).

### Phase 2: Worldbuilding & Character Arc Setup
1. Panggil **`worldbuilding-architect`** untuk merancang sistem dunia, aturan sihir/teknologi, geografi, faksi, dan atmosfer (`worldbuilding_codex.md`).
2. Panggil **`character-designer-psychologist`** untuk menyusun profil psikologis tokoh utama, *character arc*, *fatal flaw*, gaya bicara, dan matriks relasi (`character_sheets/`).
3. Minta persetujuan Penulis (*HITL Gate 2*).

### Phase 3: Plot Architecture & Scene Breakdown
1. Panggil **`plot-narrative-architect`** untuk memilih kerangka plot (*Save the Cat, 3-Act Structure, Hero's Journey, Kishōtenketsu, atau Snowflake Method*) dan menyusun `plot_outline.md`.
2. Panggil **`storyboard-scene-planner`** untuk memecah bab menjadi adegan berurutan dengan *Scene Beats* (Goal, Conflict, Disaster, Reaction, Dilemma, Decision) di `scene_breakdown.md`.
3. Minta persetujuan Penulis (*HITL Gate 3*).

### Phase 4: Chapter Drafting & Editing
1. Panggil **`novel-scene-writer`** (atau `comic-webtoon-scriptwriter` / `children-story-creator` sesuai bentuk karya) untuk menulis draf narasi adegan per adegan menggunakan teknik *"Show, Don't Tell"*, detail sensori, dan dialog alami.
2. Panggil **`prose-dialogue-polisher`** untuk menghaluskan ritme prosa, diksi, dan dialog.
3. Minta persetujuan Penulis (*HITL Gate 4*).

### Phase 5: Continuity Audit, Beta Feedback & Publisher Export
1. Panggil **`plot-hole-continuity-checker`** dan jalankan skrip `helpers/python/check_timeline_continuity.py` untuk mengaudit garis waktu dan konsistensi cerita.
2. Panggil **`beta-reader-critique-simulator`** untuk mensimulasikan umpan balik pembaca target.
3. Panggil **`fiction-layout-exporter`** untuk menghasilkan file **Buku Cetak** (`generate_fiction_docx.py` preset Novel 13x19cm / A5) dan file **Digital** (EPUB / Mobile Web Reader).
4. Selesaikan pintu persetujuan akhir (*HITL Gate 5*).

---

## Principles & Rules
- **Prinsip Utama**: Mengutamakan kualitas narasi fiksi yang imersif, emosional, dan konsisten.
- **Dukungan Cetak & Digital**: Memastikan keluaran naskah siap kirim ke penerbit cetak (marjin jilid, penomoran recto/verso) maupun platform digital (Wattpad/Webtoon/EPUB).
- **Integritas Penulis**: Selalu melibatkan penulis manusia pada setiap pintu persetujuan (*Human-In-The-Loop*).
