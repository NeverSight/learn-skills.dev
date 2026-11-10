---
name: dido-frontend-nuxt
description: Usare ogni volta che si scrive, modifica, revisiona o crea codice in un frontend Nuxt di Dido, anche per un ritocco a un componente o a uno stile (pagine, componenti Vue, composable, store Pinia, SCSS con slamp e react, i18n, configurazione di Nuxt, query GraphQL, terze parti, animazioni, accessibilità e SEO), e quando si avvia un sito nuovo dal boilerplate Nuxt.
---

# Frontend Nuxt di Dido

Il metodo dei frontend Nuxt di Dido. **Skill richiesta:** dido-code-style, con i principi validi per ogni stack. Qui c'è solo ciò che è specifico del frontend.

**Implementazione di riferimento:** il boilerplate Nuxt 4 di Dido (`DidoMarchet/starter-kit-nuxt-webapp` su GitHub). Un sito nuovo parte da lì, e lì si legge il codice di composable, plugin e configurazione. I fatti del boilerplate (cosa è già cablato, moduli, rendering, sistema SCSS) stanno nei suoi `docs/project-architecture.md` e `docs/scss-system.md`.

Nei progetti nati dal boilerplate le regole che una macchina sa controllare le controlla il lint (`eslint.starter.mjs`, `stylelint.starter.mjs`), dopo ogni file che scrive Claude Code. Se il progetto (il suo `CLAUDE.md` o le sue doc, non il codice) dice una cosa diversa da questa skill, vale il progetto, e la differenza va segnalata nel report perché una delle due fonti è da correggere.

| Stai per toccare | Leggi |
|---|---|
| chiamate a un backend di Dido: login, token, errori | `riferimento/chiamate-al-backend.md` |
| un admin (SPA con Tailwind) | la sezione "Admin" in fondo |
| una skill che non è `dido-*` (design, GSAP, DatoCMS, Vue, FormKit…) | `riferimento/skill-di-terzi.md` |

## Principi

- **Componi con il design system.** Margini e padding con le classi utility, i gap con i token, la larghezza con le righe (`.row-*`). Riusa tipografia, bottoni e card che ci sono già, niente spaziature su misura.
- **Token pragmatici.** I token sono variabili SCSS esposte come classi numerate, non un sistema formale di design token. Un valore usato una volta sola si scrive dov'è, sono token solo i valori ricorrenti.
- **Valori disciplinati.** Numeri pieni o multipli di 5, anche nelle misure di layout, e font a multipli di 2 o 4. Se il progetto ha un Figma, i valori vengono da lì e non si inventano, ma si arrotondano: un valore che non è un token della scala né un multiplo di 5 diventa il più vicino dei due (67 → 65, 17 → 16). Le regole di questa skill valgono sopra il layout: una differenza dal frame dovuta a loro non è un errore.
- **Dal Figma.** Se c'è un Figma, prima di scrivere lo si legge con l'MCP (struttura, valori, screenshot del nodo giusto) e si misurano content box, gap e padding: niente a memoria.
- **Testi staccati dalle righe.** Un testo, un titolo o una CTA non stanno mai appoggiati a una riga visibile (righe della griglia di sfondo, divisori verticali): hanno un padding minimo dalla riga anche se il Figma li allinea lì, con un token del progetto applicato da una classe. Le immagini possono toccarla.
- **Degrada, non cadere.** Un dato o una config che manca produce uno stato gestito (fallback, messaggio, sezione assente), mai una pagina in errore. Fa eccezione il contenuto principale della pagina: se il CMS non risponde la pagina risponde 500, se il contenuto non c'è 404. In SSR una proprietà letta su un oggetto che può mancare fa fallire tutta la pagina, quindi il valore di sicurezza va dove leggi (`config?.chiave ?? default`).

## JS e Vue

- Arrow function, nomi interi e niente `console.log`: "Forma del codice" in dido-code-style.
- Sempre `<script setup>`, niente Options API. Il nome del componente lo dà Nuxt dal percorso (`components/widget/media-text/index.vue` è `WidgetMediaText`), quindi niente `defineOptions({ name })`.
- Gli effetti su DOM, scroll e animazioni stanno in un composable (`app/composables/`, `useX`), che espone stato e azioni e non markup. La logica pura sta in `app/utils/`, con i suoi test. Query e chiamate stanno in cartelle dedicate, mai dentro i componenti.
- Niente testo statico nei template: il brand viene dalla config (`siteName`), le label da i18n, i contenuti dal CMS.

## Nomi

- File e cartelle in kebab-case, sempre (`widget/media-text`). Nel template i tag restano PascalCase (`<WidgetMediaText>`), perché l'auto-import concatena il percorso.
- Composable `useX`, in un file kebab-case senza `use` (`composables/api-fetch.js` esporta `useApiFetch`); componenti in una cartella kebab-case con `index.vue`, anche nell'admin (`components/ui/button/index.vue` è `<UiButton>`); util con un nome d'azione (`buildTrack`, `isLightHex`), plugin con il suffisso d'ambiente dove serve (`*.client.js`).
- Classi BEM: blocco `.componente`, `__elemento`, `--modificatore`. Le varianti si chiamano per sezione o brand, mai per colore (`--footer`, non `--dark`).
- Una sola scala tipografica numerata (`.title-1…4`, `.text-1…3`), mai due nomenclature insieme.
- Colori a scala per famiglia (`$black-1`, `$grey-2`), non semantici. Gli id solo quando servono (àncora, `aria-*`, JS), in kebab-case. Il maiuscolo si fa con `text-transform`, mai scritto nel testo.

## Componenti

- Un componente è una cartella `components/<area>/<nome>/` con `index.vue`, `style.scss` e i suoi asset, raggruppata per dominio (`article/`, `navigation/`).
- In `widget/` stanno solo i componenti agnostici e riusabili: ricevono tutto da prop ed espongono slot. Un pattern ripetuto, come un carosello, esiste una volta sola come widget. Un componente di una sezione specifica resta nella sua area.
- Stesso tipo di elemento, stesso comportamento in tutto il sito: un pattern ripetuto, mai una pagina con controlli che funzionano a modo loro. Tutti i caroselli e le file che scorrono si trascinano, scorrono e rispondono alle frecce allo stesso modo, qualunque cosa contengano; tutte le schede, le sottolineature, gli hover, le dissolvenze e i cambi d'immagine si muovono uguali, con la stessa easing e lo stesso stato alla pressione. Il file di un componente contiene solo ciò che è suo: quello che si ripete (comportamento, hover, sottolineatura, manina, valori del motion) sta una volta sola nel widget, composable, mixin o classe globale che lo fa, e il componente lo usa.
- Ordine nel `.vue`: `<template>`, `<script setup>`, `<style lang="scss" src="./style.scss"></style>`. Gli stili non sono scoped.
- Un componente usa solo le classi del suo blocco e quelle del design system, e parla con gli altri con prop, eventi, slot o uno store, mai cercando il loro DOM. Gli stili arrivano insieme al loro componente: le classi di un altro spariscono quando lo togli, o in una pagina dove non c'è.
- Asset permanenti in `app/assets/img/` con nomi kebab-case descrittivi per la SEO (`<azienda>-logo.svg`), i segnaposto in una cartella a parte. In `<img>` il path va in `src`, e l'`import` serve solo quando l'URL finisce in JS. Le icone sono SVG usate come immagini, ricolorate con un secondo file o con `mask`.

## SCSS

- Ogni `style.scss` e ogni partial apre con il toolbox, che dà token e mixin senza emettere CSS: `@use "~/assets/styles/scss/core" as *;`. Arriva anche da `additionalData`, ma scritto in cima il file si legge da solo.
- Un token che `core` non `@forward`-a non esiste nei file che lo usano: un file nuovo in `vars/` o `mixins/` va aggiunto al suo `_index.scss`.
- Fluido con `slamp(min, max)`. La finestra di viewport si configura una volta per progetto, e si passa esplicita solo per una finestra diversa.
- Font e spazi grandi sempre fluidi: i titoli della scala, i font da 40px in su scritti nei componenti, e margin, padding, gap, `top` e `bottom` da 80px in su. Il massimo viene dal Figma desktop, il minimo dallo stesso elemento nel Figma mobile. Dove il frame mobile manca, il minimo si stima (circa la metà, poi arrotondato). Un valore che cambiava solo con `react("large")` diventa uno `slamp` tra i due. Restano fissi il testo corrente e i token di spazio piccoli. La spaziatura negativa dei titoli va in `em`, così scende col font.
- Controlli e card scalano insieme dal mobile al desktop: pochi token fluidi condivisi (altezza e testo dei controlli, padding e titolo delle card, altezza della CTA), con il valore del Figma a 1920, usati da tutti i componenti. Nessun componente resta a misura desktop accanto a uno già compatto.
- Margini e padding laterali mai fissi, salvo indicazioni di Dido: il margine della pagina va con `slamp` dal mobile al desktop, con un token del progetto (es. `$side-margin: slamp($grid-gutter, $grid-margin)`), e una colonna larga fissa nel Figma desktop si stringe sotto il desktop. Con i valori di 1920 fissi, a 1024 margini e colonne laterali tolgono il posto al contenuto.
- Media query con `@include react("chiave")` (`large`, `<medium`), mai `>=` scritti a mano. L'hover sta sempre dentro `react("pointer-and-hover")`, così sul touch non resta attaccato.
- Ogni elemento cliccabile ha un hover, con la transizione del sito (durata a token, easing di sito): mai un cambio istantaneo, anche dove il Figma lo ha. I testi-azione ("Chiudi", "Filtra", i link) prendono tutti la stessa sottolineatura animata del progetto, anche quelli sottolineati da fermo (lì la linea si ridisegna), e in hover il testo cambia di un tono. I bottoni a icona prendono un tono più scuro o un fondo, quelli pieni un tono più scuro dello stesso colore. Lo stesso stato vale alla pressione (`:active`), che sul touch è il riscontro al tocco: un mixin del progetto scrive hover e pressione insieme, e i pulsanti pieni si stringono appena (0,97, fermi con reduced motion). Di base: `-webkit-tap-highlight-color: transparent`, `touch-action: manipulation` su link e pulsanti, testo dei pulsanti non selezionabile.
- Un'immagine fusa con il fondo (`mix-blend-mode`) non ha mai `opacity`, `filter` o `transform` animati, né lei né i suoi contenitori: il livello nuovo che il browser crea per la transizione la fa lampeggiare con il suo fondo bianco. Per farla comparire si dissolve sopra di lei un velo del colore del fondo, animando solo il colore. Le icone si ricolorano con `mask` e `currentcolor`, non con `filter`.
- Un testo-azione accanto a un titolo ("Chiudi", "Conferma") è un passo sotto il titolo e sta sulla sua linea di base, così non si confonde con lui. I titoli che stanno sulla stessa riga in colonne diverse (il nome e la prima card accanto) condividono la linea di base, anche quando uno è fluido.
- La conferma di un'azione fatta da un pulsante (link copiato) è un tooltip attaccato a quel pulsante, con la punta verso di lui, non un avviso lontano.
- Un pannello, un cassetto o una modale si riapre sempre dall'inizio: scroll in cima e stato del giro prima azzerato (il modo più semplice è rimontarlo a ogni apertura con una `:key`).
- Nel mobile una scelta tra card si fa in una lista verticale a tutta larghezza, non in una fila che scorre di lato: in orizzontale su un telefono non si capisce cosa si sta scegliendo.
- Classi, non mixin: i token diventano classi numerate generate da un `@each` sulla scala, nel layer giusto (`layout/`, `typo/`). I mixin servono solo per gli helper responsive e per i comportamenti interattivi, come la sottolineatura animata dei link.
- Margini e padding con le classi, i `gap` con i token nello stile del componente, la larghezza con `.row-*`. Uno sfondo a tutta pagina è una sezione con una row dentro.
- Motion con una sola easing di sito e durate a token (`$speed-*`), in `vars/_timings.scss`.

## i18n

- I testi passano da `$t`, mai ternari sulla lingua nel template.
- Dizionari divisi per area: una cartella per lingua, un file per area, e l'entry della lingua compone i moduli senza stringhe. Negli import dei file-area serve l'alias `~~`, perché con un percorso relativo `@nuxtjs/i18n` v10 non li carica.
- Le lingue sono specchi: una stringa nuova va in tutte, con la stessa chiave e nella stessa area. Il file unico si divide alla prima sezione, non dopo.
- Gli slug localizzati stanno nella config i18n (`pages`). Ogni pagina va dichiarata lì anche quando lo slug è uguale nelle due lingue, altrimenti non entra nella sitemap. Per gli slug dinamici si impostano i parametri per lingua, così hreflang e canonical puntano allo slug giusto.

## Configurazione

- `nuxt.config.ts` fa solo lo spread degli slice di `configuration/`, uno per area, e un'impostazione si cambia nel suo slice. Modificare uno slice non fa ripartire il dev server.
- Env e segreti arrivano da `runtimeConfig` letto da `process.env`, mai scritti nei componenti. `runtimeConfig.public` finisce nel bundle client, quindi contiene solo valori pubblici per natura (es. un token CMS in sola lettura).
- `robots` e `noindex` dipendono dall'ambiente: si indicizza solo la produzione.

## Dati e terze parti

- Il CMS si legge solo con `useGraphql()`, con query e fragment in `app/graphql/<cms>/`. Dentro lavorano `useAsyncData` di Nuxt e `executeQuery` di `@datocms/cda-client`. Il client del CMS lo importano solo `useGraphql()` e le sorgenti lato server. Le chiamate REST passano da `useApiFetch()`. Pagine e componenti non parlano mai con il client del CMS o con quello HTTP.
- Un errore del CMS non è una pagina che non esiste: la pagina risponde 500, e 404 solo quando il contenuto non c'è.
- SEO e hreflang con `useSeo()` nella pagina. Con gli slug localizzati servono `generateSeoLocaleParams` e `setI18nParams`, altrimenti gli alternate dichiarano URL che non esistono.
- `useLenis()` si inizializza una volta sola per l'app, nel layout o in `app.vue`. Ogni contenitore che scorre da solo (foglio di una modale, cassetto, menu a tendina, pannello dei filtri) ha lo stesso scorrimento fluido della pagina con un Lenis suo, nel ticker di GSAP. Il contenitore ha un figlio solo, perché Lenis ricalcola quanto si può scorrere quando cambia la misura del primo figlio. Lenis cerca `data-lenis-prevent` solo dentro il proprio contenitore, e gli eventi che arrivano da un'altra modale aperta sopra non lo devono muovere.
- Una terza parte che serve a tutto il sito (analytics, error tracking, consenso) è un plugin. Una che serve a una pagina o a un componente (un form, un widget di prenotazione, un player) è un composable per l'effetto più un componente per il markup.
- La libreria di una terza parte la importa solo il suo plugin o il suo composable, che senza la sua config non fa niente. Così si toglie cancellando quei file, la dipendenza e il punto in cui si usa. Se deve ricevere qualcosa dal sito, come gli errori di GraphQL per l'error tracking, è lei che si aggancia a un hook (`graphql:error`, che `useGraphql()` chiama sugli errori, o `vue:error`).
- Gli embed si vestono con il design system: niente CSS del servizio, le classi dei tuoi bottoni. Se il servizio rende in un `<iframe>` non si può vestire, quindi va verificato prima di prometterlo.
- Prima di dire cosa fa una terza parte, misura quali domini contatta e quali cookie scrive.
- Le sorgenti dinamiche lato server, come la sitemap, chiamano il servizio dal server con il suo client, senza `useGraphql()`, paginano dove il servizio lo chiede e non rompono il build quando falliscono. Un modello con pagina di dettaglio entra nella sitemap interrogando ogni lingua.
- Lo schema del CMS cambia solo con migration versionate, provate su una sandbox: mai a mano, nemmeno sulla sandbox.

## Motion

- Le animazioni si fanno con GSAP: entrate e uscite, modali, fogli e cassetti, tendine, schede, comparse allo scroll, sequenze e microinterazioni. Restano in CSS solo gli hover e le pressioni di bottoni e link (colore, fondo, sottolineatura, la stretta alla pressione).
- Si anima a componenti. Un movimento che si ripete esiste una volta sola, in un composable (`useXMotion`) o in un widget, e i componenti lo riusano invece di scriversi la loro timeline. La modale è un widget unico con entrata e uscita in GSAP, usato da fogli, cassetti e ricerca. La dissolvenza tra due contenuti è un wrapper unico: una `<Transition :css="false">` con gli hook in GSAP.
- Le animazioni di un componente nascono dentro `gsap.context()`, con il suo elemento come scope, e si annullano con `revert()` quando si smonta. Girano solo nel client, da `onMounted` in poi.
- Apertura e chiusura sono la stessa timeline, con `play()` e `reverse()`, anche quando la chiusura parte dalla tastiera (Esc): chi chiude a metà apertura torna indietro da dove è, senza ripartire da zero. Tutte le parti di un passaggio (l'header che si svuota e la ricerca che compare) stanno nella stessa timeline, mai metà in CSS e metà in GSAP.
- Una sola easing di sito e durate a token. Lineare solo per il motion legato allo scroll e per i loop continui (marquee, loader). Il pinning si fa con `position: sticky`, non in JS.
- Easing, durate e stagger stanno solo nei token SCSS (`$ease-site`, `$speed-*`, `$stagger` in `vars/_timings.scss`), e il JS li legge con `useMotion()`, che li prende da un modulo SCSS: mai numeri ricopiati nel JS. Un plugin client registra i plugin di GSAP e imposta una volta sola `gsap.defaults` con l'easing del sito e la durata di base.
- Il motion che segue lo scroll (parallasse, testo che si accende, header che si nasconde) usa ScrollTrigger agganciato a Lenis, così si aggiorna nello stesso frame. Lo scroll comandato (un'ancora, "torna su") passa dallo `scrollTo` di `useLenis()` (nei componenti `inject("scrollTo")`), che con reduced motion salta al punto senza animazione: mai `window.scrollTo` scritto a mano o un secondo sistema di scroll. L'inerzia si fa con GSAP.
- Un popover o una tendina nasce dal suo bottone (`transformOrigin` verso di lui). Dopo il primo tooltip, i successivi compaiono senza ritardo finché il puntatore resta lì. Un elemento che si trascina (foglio, carosello) si chiude o scorre in base alla velocità del gesto, con resistenza ai bordi: Draggable e InertiaPlugin di GSAP.
- Ogni animazione gira a tutti i fotogrammi dello schermo (60 o 120 al secondo), senza scatti:
  - si muove e si ingrandisce solo con `transform` e `opacity` (`x`, `y`, `scale`, `rotation`, `autoAlpha`), mai con `width`, `top`, `margin` o `padding`. L'altezza si anima solo dove il contenuto sotto deve spostarsi (una fisarmonica), su un blocco piccolo. `clip-path` e `filter` solo su superfici piccole, quando con `transform` non si può;
  - i valori che non cambiano durante il movimento (`transformPerspective`, `transformOrigin`) si fissano prima con `gsap.set`: dentro un `to()` GSAP li anima da zero, e la forma salta nei primi fotogrammi;
  - GSAP gira sul thread principale, quindi mentre si anima il thread va tenuto libero. Il contenuto è montato e misurato prima di partire (prima tutte le letture, poi le scritture), le immagini sono già caricate e Vue non ridisegna niente di grande nello stesso momento;
  - `will-change` solo sulle superfici che si muovono, più elementi uguali con `stagger` a token, i valori che seguono il puntatore con `gsap.quickTo`;
  - si verifica rallentando GSAP (`gsap.globalTimeline.timeScale(0.1)`) e guardando i fotogrammi uno per uno: tra due fotogrammi la forma non salta.
- Il velo di una modale è un elemento nella stessa timeline della superficie, perché GSAP non anima il `::backdrop`, che resta trasparente. Un foglio o un cassetto scorre senza dissolvenza, e il `<dialog>` ha `overflow: clip`: senza, mentre la superficie entra da fuori compare la sua scrollbar. Non `hidden`, che dal codice si scorre ancora: il focus che `showModal()` mette nel contenuto, ancora fuori schermo con la superficie, fa scorrere il dialogo fino a lui, e la superficie compare già al suo posto mentre GSAP la muove.
- Un movimento che attraversa lo schermo (foglio, cassetto, pannello) dura in base alla corsa: un token di riferimento (es. `$speed-medium` per 1000px) con la radice della distanza, tra due durate a token. Più breve sul telefono, più lungo sul desktop.
- Un contenuto che compare al posto di un altro (schede, pannelli con `v-show`) entra in dissolvenza con il wrapper di dissolvenza, mai a scatto.
- La superficie di una modale animata in entrata ha `will-change: transform`: se il browser toglie il suo livello a fine animazione, al primo ridisegno (il primo hover) testo e immagini sfarfallano.
- In una galleria le immagini stanno tutte nel riquadro, una sopra l'altra e solo la corrente visibile: al cambio quella nuova è già caricata. Sempre con `NuxtImg`.
- `prefers-reduced-motion` sempre rispettato: niente scale o translate animati, al massimo una dissolvenza. Si legge quando l'animazione parte, perché può cambiare mentre si naviga.
- Mai lo zoom delle immagini all'hover: al massimo un overlay o il testo.

## Accessibilità e SEO

- Immagini decorative con `alt=""`, informative con un `alt` che le descrive. Nomi dei file pensati per la SEO, `loading="lazy"` e `decoding="async"` dove ha senso.
- Un solo `<h1>` per pagina, heading in ordine, markup semantico e landmark.
- Contrasto almeno WCAG AA (4,5:1, 3:1 per i testi grandi). Le combinazioni che non passano si segnalano, non si scelgono in silenzio.
- Focus visibile con `:focus-visible`, distinto da `:focus`.
- L'esito di un'azione asincrona si annuncia spostando il focus sul messaggio (`tabindex="-1"` e `.focus()`). Una live region funziona solo se era già nel DOM prima che il contenuto cambiasse.
- In `<noscript>` solo testo, con una sola interpolazione, e nessun `display` nel CSS. Con il JavaScript attivo il browser lo legge come testo, e dei tag dentro danno un mismatch di idratazione.
- Immagini dimensionate per larghezza, mai con un'altezza fissa (`block-size: auto`, o un box con un `object-fit` scelto apposta).

## Verifica

Oltre a quanto chiede dido-code-style:

- lint pulito, JS e CSS, sui file toccati;
- la pagina toccata risponde 200 con zero errori in console e nel log, compresi i mismatch di idratazione;
- test verdi: util e composable toccati hanno sempre i loro test; un componente li ha quando contiene della logica (con `@nuxt/test-utils`); motion e aspetto si verificano con gli screenshot, non con i test;
- ogni elemento della parte toccata confrontato con quelli simili del sito (carosello con carosello, schede con schede, link con link): stesso componente e stesso comportamento, compresi trascinamento, hover, pressione e transizioni;
- l'interfaccia toccata guardata a 375, 768, 1024, 1440 e 1920 con le skill di design del progetto (impeccable, design-taste-frontend, mobile-native, dove ci sono): il contenuto si legge, è bilanciato e si usa bene. Non basta che non si rompa;
- se hai toccato una terza parte, domini e cookie misurati;
- con una terza parte nuova, la pagina risponde 200 anche senza la sua variabile d'ambiente.

## Admin

Gli admin nati da `starterkit-backend-admin` (SPA, `ssr: false`) seguono questa skill, tranne dove lo stack è diverso:

- **Stile**: Tailwind con i token del `@theme` di `app/assets/styles/main.css` e i pattern di `docs/design-system.md`, al posto di SCSS, `slamp` e `react`. I colori hanno nomi di ruolo (`--color-ink`, `--color-surface`), i font stanno nella scala `title-1…2`, `text-1…3`. Niente colori né dimensioni scritti nelle classi; le dimensioni le segnala il lint.
- **Configurazione**: un solo `nuxt.config.ts`, senza gli slice di `configuration/`.
- **Motion**: le transizioni di Tailwind e le `<Transition>` di Vue, come dice `docs/design-system.md`. Il reduced motion lo annulla una regola sola in `main.css`: niente classi `motion-reduce:`. Niente GSAP.
- **Testi**: i18n solo se l'admin ha più lingue; in una lingua sola i testi stanno nel template.
- **Uguali al sito**: forma del codice, `<script setup>`, ordine dei blocchi, file e cartelle in kebab-case, componente in una cartella, chiamate al backend solo con `useApi()` (`riferimento/chiamate-al-backend.md`). Fanno eccezione login e reset della password, che usano la fetch diretta con `useApiUrl()`: lì un 401 vuol dire credenziali sbagliate, non sessione scaduta.
