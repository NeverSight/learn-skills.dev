---
name: plot-hole-continuity-checker
description: Audits fiction manuscripts for timeline errors, plot holes, rule breaks, character behavior breaks, and unanswered foreshadowing.
---

# Plot Hole & Continuity Checker

Agen spesialis audit kontinuitas dan keutuhan plot fiksi. Menjamin tidak ada kontradiksi garis waktu, pelanggaran aturan dunia, atau ketidakkonsistenan sifat tokoh.

---

## Audit Checklist

1. **Timeline Audit**:
   - Memastikan urutan hari, waktu (pagi/malam), dan usia tokoh tidak melompat secara janggal.
   - Jalankan `python helpers/python/check_timeline_continuity.py --input chapters/full_manuscript.md`.

2. **Worldbuilding Rule Audit**:
   - Memastikan batas kekuatan sihir/teknologi yang ditetapkan di `worldbuilding_codex.md` tidak dilanggar secara ajaib tanpa konsekuensi.

3. **Character Integrity Audit**:
   - Memeriksa apakah tindakan tokoh di adegan tertentu bertentangan dengan kebiasaan/motivasi di `character_sheets/`.

4. **Foreshadowing & Unanswered Hooks**:
   - Memastikan rahasia/objek yang ditanam di bab awal mendapatkan bayaran (*payoff*) di bab akhir.

---

## Output Artifact
Menghasilkan laporan audit `continuity_report.md` yang memuat daftar temuan kontradiksi beserta saran perbaikan.
