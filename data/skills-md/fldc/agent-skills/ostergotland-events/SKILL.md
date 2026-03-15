---
name: ostergotland-events
description: Hitta och sammanfatta tidsatta evenemang i Östergötland, som konserter, marknader, föreställningar och familjeaktiviteter. Använd när användaren frågar vad som händer i en stad eller under en viss dag eller helg i Linköping, Norrköping, Mjölby, Motala, Vadstena eller andra orter i regionen.
---

# Evenemang i Östergötland

Denna skill hjälper till att hitta och presentera lokala evenemang i Östergötland genom att använda kommuners och venues evenemangskalendrar.

## Arbetsflöde

1.  **Identifiera plats & tid**: Bestäm vilken del av Östergötland (t.ex. Linköping, Mjölby) och vilken tidsram (t.ex. denna helg, specifikt datum) användaren är intresserad av.
2.  **Välj källor**: Se [references/calendars.md](references/calendars.md) för att hitta relevanta URL:er för platsen eller specifika venues.
3.  **Hämta innehåll**: 
    *   Använd `webfetch` med `format: markdown` för de flesta sajter.
    *   **För sajter med certifikatproblem** (markerade med `[CURL]` i calendars.md):
        - Första försöket: `curl -k <url>` för rå HTML
        - Om outputen trunkeras: Använd `curl -k <url> | lynx -dump -stdin` för att konvertera HTML till läsbar text
        - Detta ger oftast bättre resultat än webfetch för problematiska sajter

4.  **Tolka och sammanfatta**:
    - Extrahera titel, datum, tid och plats.
    - Inkludera en kort beskrivning om tillgänglig.
    - **Lyft proaktivt fram evenemang för barn och familjer.**
    - **Exkludera strikt tävlingsidrott och matcher** (t.ex. match, cup, serie, division, vs, mot, LHC, LVC, IFK, SHL) om inte användaren specifikt efterfrågar det.
    - **Inkludera alltid publika aktiviteter för eget deltagande** även i sportarenor (t.ex. allmänhetens åkning, skridskoåkning, simhall, bad, prova-på, öppet hus, workshop).
    - Inkludera länk till originalkällan eller evenemangssidan.
5.  **Presentera resultat**: Kategorisera evenemang för enkel överblick.

## Kategorier

Använd dessa kategorier vid presentation:

- **Barn & Familj** – Sagostunder, barnteater, familjeaktiviteter
- **Musik & Konserter** – Livemusik, konserter, festivaler
- **Teater & Föreställningar** – Teater, stand-up, cirkus
- **Marknader & Loppisar** – Julmarknader, loppis, mässor
- **Utställningar & Museer** – Konstutställningar, museum, vernissage
- **Kurser & Workshops** – Prova-på, pyssel, föreläsningar

## Resurser

- **references/calendars.md**: En kurerad lista med URL:er för evenemangskalendrar och venues i Östergötland.
