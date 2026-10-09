---
name: islamic-hijri
description: >
  Convert between Gregorian and Hijri (Islamic) calendar dates in both directions.
  Use this skill whenever the user asks: "كم يوافق 1 رمضان 1447 ميلادي؟",
  "convert 20 March 2026 to Hijri", "ما التاريخ الهجري اليوم؟",
  "1 شوال 1447 يوافق كم ميلادي؟", "what Hijri date is April 5 2026?",
  "حوّل تاريخ ميلادي إلى هجري", or any Gregorian↔Hijri date conversion request.
---

# Islamic Hijri ↔ Gregorian Converter

Accurate bidirectional date conversion using the `hijridate` library (Umm al-Qura algorithm).

## Script

```
islamic-hijri/scripts/hijri.py
```

## Usage

**Gregorian → Hijri:**
```bash
python scripts/hijri.py --date 20-03-2026
python scripts/hijri.py --date 2026-03-20
```

**Hijri → Gregorian:**
```bash
python scripts/hijri.py --day 1 --month 10 --year 1447
python scripts/hijri.py --day 9 --month 12 --year 1447
```

## Output fields

For G→H: `mode`, `gregorian_input`, `hijri_day`, `hijri_month`, `hijri_year`,  
`hijri_month_name`, `hijri_string`

For H→G: `mode`, `hijri_input`, `gregorian_day`, `gregorian_month`, `gregorian_year`,  
`gregorian_string` (DD-MM-YYYY), `gregorian_iso`

## Hijri month numbers

| #  | Name         | #  | Name          |
|----|--------------|----|---------------|
| 1  | Muharram     | 7  | Rajab         |
| 2  | Safar        | 8  | Sha'ban       |
| 3  | Rabi' al-Awwal | 9 | Ramadan      |
| 4  | Rabi' al-Akhir | 10 | Shawwal      |
| 5  | Jumada al-Ula  | 11 | Dhul Qi'dah  |
| 6  | Jumada al-Akhira | 12 | Dhul Hijjah |
