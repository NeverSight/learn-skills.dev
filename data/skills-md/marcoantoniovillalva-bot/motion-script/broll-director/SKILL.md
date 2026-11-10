---
name: broll-director
description: Pianifica (con IA), genera e integra i b-roll — motion graphics glass, immagini AI, screen-recording tutorial — dentro il video talking-head editato, come layer Remotion tra footage e sottotitoli. Triplo output per il collaudo — video completo, video pulito, layer b-roll solo con alpha. Trigger; "b-roll", "aggiungi motion graphics al video", "inserisci immagini nel talking head", "tutorial nello schermo", "broll director".
metadata:
  tags: b-roll, motion-graphics, remotion, talking-head, replicate, glass-ui
---

Sei il regista dei b-roll per i video talking-head del progetto:
`C:\Users\Villalva\Desktop\Marketizzati definitifo\marketizzati-video-renderer\`

**Questa skill NON modifica la skill `remotion_marketizzati`** (motion graphics standalone da copione) né la skill `talking-head-editor` (edit del footage): le **riusa**. Prende un talking-head già editato (captions + zoom plan + face track pronti in `raw-edits/<slug>/`) e vi aggiunge il layer b-roll.

## Principio architetturale (deciso col cliente, 2026-07-15)

I b-roll sono un **layer Remotion dentro la composizione `TalkingHeadEdit`**, inserito tra il footage e le captions: mai sopra i sottotitoli, sincronia garantita, un solo progetto. Niente montaggio manuale a posteriori — ma in fase di collaudo si producono **tre output**:

1. `renders/talking-head/<slug>.mp4` — video completo con b-roll integrati
2. `renders/talking-head/<slug>-clean.mp4` — stesso video senza b-roll (fallback)
3. `renders/talking-head/<slug>-broll.mov` — SOLO il layer b-roll su **trasparenza** (ProRes 4444 con alpha), stessa durata/timeline del video: se un b-roll è sbagliato, il cliente lo sovrappone e corregge a mano in CapCut

Il render alpha si fa con `--codec prores --prores-profile 4444 --image-format png` e composizione con sfondo trasparente (prop `transparentBase: true` che spegne il footage layer).

## La palette e lo stile (NON derogare)

- Bianco caldo `#FAF9F5`, arancione `#FF8A1F` / `#D97757`, testo scuro `#1A1A1A` — stile Anthropic, come i componenti esistenti in `src/motion-components/`
- Estetica premium "glass Apple": card con blur/backdrop, angoli molto arrotondati, ombre morbide, animazione d'ingresso a rimbalzo (spring) come un'icona iOS
- Font: gli stessi del progetto (Montra per UI, Lobster per accenti — vedi `src/talking-head-fonts.ts`)

## Il catalogo template (validato col cliente 2026-07-16 — l'IA sceglie per ogni momento)

Template di piazzamento:
1. **CARD** (default) — card glass compatta sotto le captions, entra con spring bounce. Contenuti: icone 3D fluttuanti, stat col contatore, testo con parola enfasi, loghi affiancati (kind `logos`), fila di icone.
2. **SPLIT** — finestra mock macOS sopra, talking head sotto, captions sulla giuntura. Contenuti: video/foto stock, mockui, screen reali. Flag `tilt: true` per l'inclinazione 3D progressiva premium — SOLO su contenuti visual (mai testo denso né screen reali), max 1-2 a video.
3. **TAKEOVER** — schermo intero 2-4s max, con parsimonia.
BOCCIATI dal cliente (non riproporre): PiP col volto in mini-card ("troppo piccolo"), bolle commento sparse sul footage ("cheap e confusionario").

Contenuti mockui (visual-first — REGOLA CLIENTE: immagini/emoticon/visuale > scritte, i sottotitoli portano già il testo):
- `tasks` — checklist di automazioni che si spunta da sola (+tick SFX)
- `chat` — conversazione con l'agente che scrive
- `phone` — iPhone mock con notifiche che scivolano dentro ("💰 Nuovo cliente") — la versione premium della riprova sociale
- `iconrow` — 3-4 icone 3D che poppano con micro-etichette — il SOSTITUTO di default delle liste testuali
- `compare` — due card scure, icone grandi + UNA parola per lato, bordo+glow arancione sul vincitore, pill sotto; ottimo con `tilt`
- `orbit` — loghi tool che orbitano attorno al logo centrale (integrazioni) — colpo d'effetto, max 1 a video
- `product` — superficie prodotto (logo + feature name digitato + badge NEW) per hook di brand
- `doc` — anteprima risorsa/guida con badge GRATIS e indice a scorrimento (placeholder finché la risorsa non esiste)
- `agentconsole` — RICREAZIONE FEDELE della console di un prodotto reale: ricercare prima la documentazione ufficiale del tool (comandi veri, formato output autentico) e ricostruirla animata. Pattern ripetibile per qualsiasi tool di cui si parla (workflow: ricerca docs → elementi autentici → mock vettoriale animato → piazzato dove se ne parla).
- stat con contatore automatico (i numeri si contano da soli)

## Proporre template NUOVI (richiesta esplicita del cliente, 2026-07-16)

NON limitarti al catalogo: a ogni video, se il contenuto lo suggerisce, **proponi 1-3 template nuovi** coerenti con lo stile. Regole per le proposte:
- INERENZA PRIMA DI TUTTO: il template nuovo deve nascere da ciò che si DICE in quel video (un concetto specifico che i template esistenti non visualizzano bene) — mai novità fine a sé stessa. Se il catalogo copre già bene ogni momento, va benissimo non proporre nulla.
- SEMPRE visual-first: immagini, video, motion visivi, icone, grafici — mai template basati su testo (i sottotitoli portano già il testo)
- Sempre dentro il linguaggio: glass Apple, palette Anthropic, animazioni spring/fluttuanti — mai stili estranei (collage, halftone, ecc. già bocciati)
- Flusso obbligatorio: descrivi la proposta in 1-2 righe → se il cliente è interessato, **renderizza un DEMO nel suo video reale** (piano demo separato, `--broll=<plan-demo.json>` su un range di frame) → solo dopo l'approvazione entra nel piano ufficiale e in questo catalogo
- I nuovi template si implementano come varianti `mockui` in `src/BrollLayer.tsx` (pattern esistente: componente + case nello switch + tipo in `broll-types.ts`)

## Flusso di lavoro (tutto implementato e collaudato — comandi reali)

### Fase 1 — Piano IA
```bash
node scripts/broll-plan.mjs --captions=raw-edits/<slug>/captions-trimmed.json --output=raw-edits/<slug>/broll-plan.json --slug=<slug>
```
Il prompt del piano contiene già le regole di densità aggiornate (2026-07-15, feedback "il video deve essere sempre in movimento"): 12-18 segmenti per ~2 min, PRIMI 10 SECONDI con almeno 2 elementi dinamici (hook visivo), solo gli ultimi ~6s puliti per la CTA, varietà obbligatoria (mai due segmenti consecutivi uguali), abbinamento contenuto-asset guidato dalle parole chiave da imprenditore (clienti, fatturato, costi, tempo), parti tecniche/noiose SEMPRE coperte (mockui o video).
**Mostra sempre il piano al cliente in tabella leggibile in chat prima di generare gli asset** (l'app desktop a volte non apre i file del progetto).

### Fase 2 — Asset
```bash
node scripts/broll-assets.mjs --plan=raw-edits/<slug>/broll-plan.json
```

Ordine di preferenza per fonte (deciso col cliente, 2026-07-15):
1. **Motion graphics** (stat/list/text): gratis, renderizzate live dal layer — nessun file
2. **Fluent Emoji 3D** (Microsoft, GitHub, MIT): il DEFAULT per icone/emoticon 3D nelle card — PNG trasparente garantito, stile coerente, gratis, zero API key
3. **SVGL** (api.svgl.app): loghi UFFICIALI dei brand tech (Anthropic, Claude, OpenAI, n8n…) in SVG trasparente — per quando si nomina un'azienda; nel layer ricevono ombra/profondità glass via CSS
4. **Vecteezy** (`scripts/vecteezy-client.ts`): SOLO `content_type=vector` come fallback icone (le "photo" di icone 3D sono SEMPRE JPG = sfondo opaco, mai usarle per overlay). Lo zip viene estratto e si usa l'SVG più grande
5. **Pexels**: foto/video REALI per split e takeover (soggetti generici: uffici, laptop, persone)
6. **Replicate (AI)**: ultima spiaggia, solo per soggetti troppo specifici per lo stock.
  Workflow cinematografico per i realistici: (a) immagine base con prompt fotografico completo — lente (es. 85mm f/1.8), luce, composizione; (b) solo se serve movimento: image-to-video breve (2-4s) con motion prompt semplice. Mai text-to-video diretto.

REGOLE QUALITÀ NON NEGOZIABILI:
- **Trasparenza icone**: dentro le card solo asset senza sfondo; ogni PNG scaricato passa un check del canale alpha (PIL) — se opaco si scarta e si prova il risultato successivo
- **No watermark**: da Vecteezy usare SEMPRE l'endpoint firmato `/download`, MAI `thumbnail_url` come asset finale (i watermark stanno solo sulle anteprime); Pexels/Fluent/SVGL sono watermark-free per natura
- **Motion loop video di icone**: NON usarli per ora (decisione cliente: prima si roda la base con icone statiche)

- **Screen-recording tutorial** (SEMI-AUTO, conferma obbligatoria): il cliente fornisce il video e il punto del copione; tu rilevi la zona attiva (frame-differencing ffmpeg o ispezione frame), calcoli velocità = durata_clip ÷ durata_slot, generi UN frame di anteprima col crop proposto e **aspetti conferma del cliente** prima di processare (crop + setpts + eventuale trim).

### Fase 3 — Anteprime di approvazione
**OBBLIGATORIA e per prima: l'anteprima dei PRIMI 10-13 SECONDI** (frames 0-400 circa) — è lì che si decide la maggior parte della retention, e il cliente la vuole SEMPRE vedere e approvare prima del render finale. Poi 1-2 clip degli altri momenti nuovi/rischiosi. In chat compresse (CRF 24) se >30MB:
```bash
node.exe render-edit.mjs --slug=<slug> --frames=0-400 --output=raw-edits/<slug>/preview-hook.mp4   # SEMPRE
node.exe render-edit.mjs --slug=<slug> --frames=<da>-<a> --output=raw-edits/<slug>/preview-X.mp4  # momenti nuovi
```

### Fase 4 — Render finale (catena completa, in background, ~3-4h)
```bash
node.exe render-edit.mjs --slug=<slug>                                                   # completo con b-roll
node.exe render-edit.mjs --slug=<slug> --no-broll --output=renders/talking-head/<slug>-clean.mp4
node.exe render-edit.mjs --slug=<slug> --broll-only                                      # layer alpha ProRes 4444 (con SFX)
node.exe scripts/export-social.mjs --input=renders/talking-head/<slug>.mp4               # FILE DA CARICARE: ~12Mbps + loudness -14 LUFS
```
- `render-edit.mjs` aggancia `broll-plan.json` da solo; il layer CARD si posiziona sotto `captionY` dinamico, mai sopra le captions
- SFX (pop/whoosh/tick/reveal in `public/sfx/`, sintetizzati, zero licenze) sono automatici via `BrollAudio` e viaggiano anche nel layer alpha
- DOPO ogni render: verificare durata (`ffprobe`), estrarre 2-3 frame chiave e guardarli, e per il .mov verificare l'alpha con `ffmpeg -vf alphaextract` (il probe pix_fmt deve dire `yuva…`); consegnare al cliente l'anteprima leggera in chat + percorso Windows della cartella
- Render notturni: la sospensione AC è già disattivata (powercfg); se il PC va comunque in sleep il file in scrittura resta corrotto (moov atom mancante) → si ri-renderizza solo quel file

## Vincoli tecnici del progetto (ereditati — vedi memoria progetto)

- Da WSL usare SEMPRE `node.exe`, `.venv/Scripts/python.exe`, `ffmpeg.exe` (toolchain Windows)
- Render lunghi in background; typecheck con `npx tsc --noEmit` prima di ogni render
- Verificare sempre frame estratti dai render prima di consegnare

## Stato implementazione

- [x] `scripts/broll-plan.mjs` — piano IA con regole di densità/varietà (2026-07-15/16)
- [x] `src/BrollLayer.tsx` — tutti i template e mockui del catalogo + `BrollAudio` SFX (2026-07-16)
- [x] `render-edit.mjs` — flag `--broll=`, `--no-broll`, `--broll-only` con alpha (`proResProfile` con R maiuscola + `pixelFormat: yuva444p10le`, entrambi obbligatori) (2026-07-16)
- [x] `scripts/broll-assets.mjs` — fetcher Fluent/SVGL/Vecteezy/Pexels con check alpha (2026-07-15)
- [x] `scripts/vecteezy-client.ts` — client V2 tipato e verificato (2026-07-15)
- [x] `scripts/export-social.mjs` — export di consegna social con loudness (2026-07-16)
- [x] SFX sintetizzati in `public/sfx/` (2026-07-16)
- [ ] `scripts/process-screenrec.mjs` — crop/speed semi-auto per i tutorial (al primo screen recording reale)
- [ ] Integrazione Replicate per immagini (flux-schnell) + workflow cinematografico image-to-video
- [ ] Avatar 3D Pixar del cliente via Replicate (backlog: serve foto di riferimento + ok costi ~$0.10-0.30/clip)
- [ ] Riser audio nell'hook — PROVATO E PARCHEGGIATO (2026-07-16): tre varianti sintetizzate esistono in `public/sfx/riser-{a,b,c}.wav` ma il cliente non è convinto ("neanche tanto") → NON attivi. Non riproporre a meno che non lo richieda lui.
- [ ] Walkthrough tutorial ricostruito (storyboard di azioni UI sincronizzate al parlato) — al primo video tutorial
