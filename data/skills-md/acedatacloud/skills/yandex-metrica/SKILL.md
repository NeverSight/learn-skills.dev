---
name: yandex-metrica
description: Read Yandex Metrica counters and segmented website visits for Russian-language acquisition analysis. Use for country, source, or UTM campaign reporting.
when_to_use: |
  Use when the connected user requests Yandex Metrica traffic, acquisition,
  country, or campaign data. Read-only; requires metrika:read access.
connections: [yandexmetrica]
allowed_tools: [Bash]
license: Apache-2.0
metadata:
  author: acedatacloud
  version: "1.0"
---

# Yandex Metrica

The BYOC token is injected as `$YANDEXMETRICA_ACCESS_TOKEN`. Keep it in the
Authorization header; never print it. Discover a counter before reporting.

```bash
SCRIPT="$SKILL_DIR/scripts/yandex_metrica.py"
python3 "$SCRIPT" counters
python3 "$SCRIPT" report --counter-id 12345678 --dimension country --start 2026-09-01 --end 2026-09-30
python3 "$SCRIPT" report --counter-id 12345678 --dimension utm-source --start 2026-09-01 --end 2026-09-30
```

Dimensions are deliberately limited to `country`, `source`, and `utm-source`;
the script does not make configuration or audience changes. Interpret visits
as a traffic signal. Use first-party registration and payment data to decide
whether a country or channel brings customers.

Official API: https://yandex.com/dev/metrika .
