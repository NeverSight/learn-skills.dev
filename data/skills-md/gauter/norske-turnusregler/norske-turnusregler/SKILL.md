---
name: norske-turnusregler
version: 1.0.0
description: Sette opp og vurdere turnus, arbeidsplan og vaktliste ut fra norsk lov for stat, kommune og privat; lese Excel og generere forslag til fordeling; arbeidstidsgrenser og fordeling deltid/heltid etter stillingsprosent. Brukes når bruker spør om turnus, vaktliste, arbeidsplan, skift, Excel-turnus, fordeling, deltid, stillingsprosent, arbeidstid, AML, Arbeidstilsynet, stat, kommune eller privat.
---

# Norske turnusregler for AI-agenter

## Gjelder alle områder

Skillen gjelder **stat, kommune, privat** og andre virksomheter. Ikke anta én bestemt sektor; AML og Arbeidstilsynets krav er felles. Når bruker oppgir sektor (f.eks. stat, kommune, privat), sjekk selv i [sector-rules.md](sector-rules.md) og [reference.md](reference.md) og oppgi gjeldende krav. Ikke anbefale at bruker sjekker – utfør sjekkene selv.

## Trigger-scenarioer

Bruk skillen når bruker ber om eller spør om:

- Oppsett av turnus, vaktliste eller skiftplan
- Sjekk av plan mot lovkrav (varsel, innhold, tilgjengelighet)
- Hvem som har krav på arbeidsplan og unntak (f.eks. tilkallingsvikar)
- Endringsregler (14 dager, tillitsvalgt, tariffavtale)
- Rolle for tillitsvalgt, fagforening eller tariffavtale ved arbeidsplan
- Lese Excel-regneark med turnus og generere forslag til fordeling
- Arbeidstidsgrenser i turnus, hvor ofte man kan jobbe skift, deltid vs heltid og fordeling av vakter etter stillingsprosent

## Kravssammendrag

- **Innhold i arbeidsplanen**: uker, dato (konkret dato), dager, klokkeslett start/slutt.
- **Hvem har krav**: arbeidstakere med varierende arbeidstid (turnus/skift), ikke fast mønster; unntak for tilkallings-/ringevikarer.
- **Varsel**: minst 14 dagers varsel før oppstart; plan klar og drøftet med tillitsvalgte; fra 1. juli 2024 skal arbeidsavtalen beskrive ordninger for vaktendringer.
- **Endringer**: minst 14 dager varsel, drøftet med tillitsvalgt; unntak (tariffavtale, uforutsette hendelser, overtid på kort varsel).
- **Konsekvenser ved brudd**: brudd på AML, mulig tilsyn; dårlig forutsigbarhet og helse; ikke automatisk krav på ulempetillegg ved endring.
- **Arbeidstid og turnus (AML)**: Arbeidsmiljøloven kap. 10 setter grenser – f.eks. alminnelig arbeidstid inntil 37,5 t/uke; særregler for skift/turnus (natt 20–06, søndag/helg). Sjekk selv at turnus/fordeling er innenfor AML-arbeidstid ut fra reference.md og ev. data i Excel; oppgi konkret om brudd og hva som bryter.
- **Deltid vs heltid**: Fordeling av vakter skal reflektere stillingsprosent over en periode (f.eks. 2–4 uker), ikke nødvendigvis likt per enkelt uke. Deltidsansatte kan ha flere vakter én uke og færre neste – sjekk at snitt over perioden er forholdsmessig. Deltidsansatte skal ikke over tid ha like mange skift som heltidsstillinger. Se [reference.md](reference.md) for detaljer.
- **Fordeling av dager og åpne/lukke**: Flere personer kan ha forskjellige dager. Samme person bør ikke både åpne og lukke samme dag (én person skal ikke ha både tidligste og seneste vakt på en og samme dag). Ved fordelingsforslag og ved validering: sjekk at ingen har både åpne- og lukkevakt på samme dag.

## Fagforening og tillitsvalgt

- **Praktisk**: Vanligvis setter **én person** (leder, koordinator) opp turnuslisten. Tillitsvalgte er ikke involvert i selve utarbeidelsen. Ikke anta at tillitsvalgte deltar i det løpende arbeidet.
- **Lovkrav**: Før planen (eller en endring) gjelder, skal den være drøftet med tillitsvalgte og klar minst 14 dager før oppstart. Sjekk selv det som kan sjekkes (f.eks. at oppstart er minst 14 dager fram i tid ut fra datoer i plan/Excel). Det som ikke kan sjekkes i data (at drøfting med tillitsvalgt er gjennomført) oppgis som krav som må være oppfylt. Kreve ikke at tillitsvalgt er med i selve oppsettet.
- **Tariffavtale**: Kan gi andre frister enn 14 dager. Sjekk selv i reference.md og sector-rules.md når sektor er oppgitt, og oppgi gjeldende krav.
- **Ved brudd**: Arbeidstaker kan ta kontakt med tillitsvalgt og fagforening – nevne dette som reaksjonsmulighet.

## Workflow

1. **Avklar**: Er det fast arbeidstidsmønster (da arbeidsavtale) eller turnus/skift (da arbeidsplan)?
2. **Innhold**: Sjekk at planen har uker, dato (ev. dag), dager og klokkeslett.
3. **Sjekk selv**:
   - (a) Er oppstart/endring minst 14 dager fram i tid (ut fra plan/Excel)? Oppgi resultat.
   - (b) For oppgitt sektor: les sector-rules.md og reference.md og oppgi gjeldende krav (inkl. tariffavtale).
   - (c) Drøfting med tillitsvalgt kan ikke sjekkes i data – oppgi som krav som må være oppfylt.
4. **Ved endringer**: Samme regel – drøfting og varsel før endringen trer i kraft.
5. **Ved Excel**: **Tolk filen selv** – les .xlsx (f.eks. med Python openpyxl eller pandas), identifiser kolonner/ark (uke, dato, dag, tid, person, ev. stillingsprosent), kjør sjekkene og gi forslag/vurdering **i chat** (tabell i markdown eller strukturert tekst). Et eget script er ikke nødvendig; agenten utfører lesing og tolkning. Ikke skriv til Excel-fil med mindre bruker eksplisitt ber om det.

For full lovtekst og detaljer, se [reference.md](reference.md).

## Excel og fordelingsforslag

- **Inndata**: Bruker legger ved eller peker på Excel-filer (.xlsx). Agenten leser og tolker filen selv.
- **Tolkning**: Les .xlsx (f.eks. med openpyxl eller pandas), identifiser struktur (uker, dato, dager, klokkeslett, arbeidstakere, stillingsprosent – fra overskrifter eller innhold). Sjekk at innholdet dekker AML-krav (uker, dato/dager, start/slutt), at vaktfordeling er forholdsmessig stillingsprosent over perioden (deltid kan variere uke til uke), og at samme person ikke både åpner og lukker samme dag. Ta høyde for ferier og annet fravær når du vurderer eller lager fordelingsforslag – ekskluder fraværsdager eller juster antall vakter for de som er borte. Et eget script er ikke nødvendig; agenten utfører tolkningen.
- **Utdata**: Gi forslag/vurdering **i chat** – som markdown-tabell eller strukturert tekst (uke, dato, dag, start, slutt, person, ev. stillingsprosent). Tabell: én rad per vakt; inkluder dato i norsk format (dd.mm, f.eks. 09.03); vis år (dd.mm.åååå) kun ved turnusliste over årsskifte; hver dag kan ha mange personer (flere rader med samme dato). Sjekk selv det som kan sjekkes (14 dagers varsel, innhold, stillingsprosent, AML-arbeidstid, åpne/lukke) og oppgi konkret resultat. For krav som ikke kan sjekkes i data (f.eks. drøfting med tillitsvalgt) oppgi at det er et krav som må være oppfylt. Skriv **ikke** til Excel-fil med mindre bruker eksplisitt ber om det.

## Rapport til chat – standard mal

Bruk denne strukturen når du presenterer vurdering av turnus eller fordelingsforslag i chat. Utelat avsnitt som ikke er relevante (f.eks. «Åpne/lukke» hvis det ikke ble sjekket).

```markdown
## Turnusvurdering

**Oppsummering:** [Én setning: oppfyller kravene / har avvik / mangler data – og for hva.]

**Innhold og struktur:** [Har planen uke, dato, dag, start, slutt, person? Mangler noe?]

**14 dagers varsel:** [Oppfylt / ikke oppfylt / kunne ikke sjekkes. Ev. første vakt-dato og dager fram.]

**Fordeling per person:** [Kort: antall personer og vakter; forholdsmessig stillingsprosent eller avvik.]

**Åpne/lukke samme dag:** [Ingen brudd / liste over dager der samme person åpner og lukker / ikke sjekket.]

**AML arbeidstid:** [Innenfor grenser / konkret brudd / ikke vurdert.]

**Krav som må bekreftes:** [F.eks. at planen er drøftet med tillitsvalgt før den gjelder.]

[Ved forslag til fordeling – tabell. Én rad per vakt; samme dag kan ha mange personer:]
| Uke | Dato       | Dag   | Start | Slutt | Person |
|-----|------------|-------|-------|-------|--------|
| 1   | 09.03      | man   | 08:00 | 16:00 | Ola    |
| 1   | 09.03      | man   | 10:00 | 18:00 | Kari   |
| 1   | 09.03      | man   | 12:00 | 20:00 | Per    |
| 1   | 10.03      | tir   | 08:00 | 16:00 | Kari   |
| …   | …          | …     | …     | …     | …      |
```

## Eksempler

### Eksempel – plan som oppfyller kravene

- Arbeidsplan med uker 1–4, konkrete dager og klokkeslett (f.eks. mandag 08:00–16:00, tirsdag 08:00–16:00).
- Oppstart første vakt 14 dager eller mer etter dagens dato.
- Vaktfordeling forholdsmessig stillingsprosent over perioden (f.eks. 50 % stilling får omtrent halvparten av vaktantallet til 100 % over 2–4 uker; deltid kan ha flere vakter én uke og færre neste).
- Ferier og annet fravær er tatt med i fordelingen (fraværende får ikke vakter på fraværsdager; andres andel kan øke i perioden).

### Eksempel – typisk brudd

- Endring av arbeidsplan med oppstart om 7 dager uten at tariffavtale eller unntak (uforutsett hendelse, overtid på kort varsel) gjelder – brudd på 14 dagers varsel.
- Deltidsansatt over tid med like mange vakter som heltidsansatt uten at stillingsprosent tilsier det – brudd på forholdsmessig fordeling.

## Progressive disclosure

- Detaljer, paragrafer og sektorspørsmål: [reference.md](reference.md) og [sector-rules.md](sector-rules.md).
- Når bruker nevner sektor, bransje eller tariffavtale: sjekk sector-rules.md.
