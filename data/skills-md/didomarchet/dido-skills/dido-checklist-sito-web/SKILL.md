---
name: dido-checklist-sito-web
description: Usare quando l'utente chiede di collaudare, controllare, fare il QA o l'audit di un sito web, prima di un lancio, dopo una migrazione, come revisione periodica o per una due diligence, anche solo per una parte (tecnica, performance, accessibilità, SEO, GEO e ricerca con AI, e-commerce, email, privacy e legale, sicurezza, analytics, contenuti, monitoraggio, consegna al cliente).
---

# Checklist QA sito web

Skill **a due velocità**: una parte è **verificabile** (scarichi la pagina, guardi l'HTML, gli
header, il JSON-LD, i redirect: o c'è o non c'è) e una parte è **giudicabile o solo umana**
(un pagamento reale, la qualità di una traduzione, la conformità legale di una clausola).

**Regola d'oro: non spuntare mai una voce che non hai davvero verificato.** Ogni voce del
report ha un esito esplicito, e `NON VERIFICATO` è un esito legittimo e frequente. Un report
con 40 voci verificate e 60 dichiarate non verificabili vale infinitamente più di uno con 100
voci verdi di cui metà inventate. Questo è l'unico modo in cui questa skill resta utile.

## Richieste parziali

Se l'utente chiede solo una parte ("controlla la SEO tecnica di X"), esegui le sole sezioni
pertinenti, con lo stesso formato del report e le stesse regole di onestà.

## Passo 0. Contesto (non saltarlo)

Senza queste risposte metà delle voci non è applicabile e rischi di segnalare come errori cose
volute. Chiedi in una volta sola, e se l'utente non risponde procedi con le assunzioni scritte
in testa al report:

1. **URL** del sito e, se diverso, dell'ambiente da collaudare (staging o produzione).
2. **Tipo**: vetrina, blog/editoriale, e-commerce, web app con login, portale multilingua.
3. **Momento**: pre-lancio, post-migrazione (allora serve la lista degli URL vecchi), audit
   su sito in esercizio.
4. **Accessi disponibili**: Search Console, GA4, admin CMS, hosting, caselle email di test.
   Senza questi, intere sezioni restano `NON VERIFICATO` — dichiaralo subito, non alla fine.
5. **Stack** (CMS, framework, hosting, CDN) e chi ha fatto cosa, se lo sanno.

Poi rileva le capacità dell'ambiente (Passo 0-bis) e definisci il perimetro con la mappa
dei tag qui sotto.

## Passo 0-bis. Rileva le capacità dell'ambiente (non darle per scontate)

Questa skill gira su host diversi (claude.ai, Claude Code, API). **Non assumere quali
strumenti hai: provalo, una volta sola, all'inizio, e scrivi l'esito nell'appendice del report.**

| Capacità | Prova | Se c'è | Se non c'è |
|---|---|---|---|
| Fetch HTML | scarica la home col tool web disponibile | voci `[A]` su HTML eseguibili | senza fetch né shell la checklist è tutta `[M]`: dillo e fermati |
| Shell HTTP | `curl -sI https://<dominio>` | header, redirect, status, TLS verificabili → applica le promozioni sotto | quelle voci restano `NON VERIFICATO` con lo strumento indicato |
| Browser agentico | esiste un tool di controllo browser? | le voci `[B]` le esegui tu | le `[B]` passano all'utente con istruzione operativa |
| Export forniti | l'utente ha allegato Screaming Frog / Lighthouse / Semrush? | molte `[M]` diventano `[A]` | nessun cambiamento |

**Promozione per capacità.** `[M]` significa "non basta l'HTML", non "impossibile". Se hai
una shell HTTP è **obbligatorio** eseguire invece di delegare: GO-05, GO-08, GO-09, PRF-06,
PRF-07, PRF-08, PRF-09, SEC-02, SEC-03, SEC-04, EML-01, EML-03. Dichiara nel report quali
promozioni hai applicato.

**Nota (caso particolare, non la regola).** Nel container di claude.ai la rete è su
allowlist: curl verso il sito del cliente non funziona e si usa solo il tool di fetch web —
hai l'HTML ma non header, redirect né rendering JS. In Claude Code o via API la shell di
norma c'è: **non riportare i limiti di claude.ai in un ambiente che non li ha.**

## Dai tipi ai tag: mappa esplicita

Vocabolario completo, sette valori (**diversi** dai tag di modalità `[A]/[B]/[M]`):
`#tutti`, `#lancio`, `#ecom`, `#login`, `#multi`, `#blog`, `#form`.

| Asse | Risposta al Passo 0 | Tag attivati |
|---|---|---|
| Base | sempre | `#tutti` (mai filtrabili) |
| Momento | pre-lancio o post-migrazione | `#lancio` |
| Tipo | vetrina | nessun tag di tipo |
| | blog / editoriale | `#blog` |
| | e-commerce | `#ecom` + `#login` + `#form` |
| | web app con login | `#login` + `#form` |
| Caratteristiche (**osservate sul sito**, non solo dichiarate) | c'è anche un solo modulo | `#form` |
| | c'è un'area riservata | `#login` |
| | ci sono più lingue | `#multi` |
| | c'è una sezione news/blog | `#blog` |

**È un'unione, non un'intersezione.** Una voce si esegue se **almeno uno** dei suoi tag è
attivo. Un e-commerce multilingua con area clienti attiva quasi tutte le voci: è
corretto così, è il caso più rischioso.

**Il filtro si applica voce per voce, non solo per sezione.** Dentro sezioni per il resto
applicabili ci sono voci con un tag di tipo (`#ecom`, `#login`, `#form`, `#blog`, `#multi`): il
tag di ogni voce sta accanto al suo titolo in `reference/checklist.md`. Se il loro tag non è
attivo vanno marcate **`N/A` con il motivo, riga per riga**: non collassarle in un range né
lasciarle cadere in `NON VERIFICATO`. Un `N/A` dichiarato è
informazione; un `NON VERIFICATO` su una voce non pertinente è rumore che nasconde i
buchi veri.

**Feature assente ≠ feature rotta.** Se una voce riguarda una funzionalità che il sito
semplicemente non ha (ricerca interna, commenti, video, modali, testimonianze, llms.txt,
area riservata, filtri), l'esito è `N/A: funzionalità non presente sul sito`, non `KO` e
non `NON VERIFICATO`. Verifica l'assenza prima di dichiararla: un `N/A` è un'osservazione
e vale come tale.

Nell'appendice del report scrivi: `Tag attivi: #tutti #ecom #form, voci in perimetro: N su M`,
dove M sono le voci di `reference/checklist.md`, contate.
Senza quella riga il perimetro non è riproducibile.

Definito il perimetro, carica `reference/checklist.md` sezione per sezione, quando stai
per eseguirla.

## Come si verifica, concretamente

Ogni voce porta un tag di **modalità**, che dice chi può eseguirla:

| Tag | Significato | Chi la esegue |
|---|---|---|
| `[A]` | Automatica: basta scaricare e leggere la pagina | tu, da solo |
| `[B]` | Serve un browser che clicchi, compili, navighi | tu se hai un browser agentico, altrimenti l'utente |
| `[M]` | Manuale: giudizio umano, credenziali, denaro vero | l'utente, tu prepari le istruzioni |

La modalità è il **default**, non un destino: va combinata con le capacità rilevate al
Passo 0-bis.

- Voci su HTML, meta, JSON-LD, hreflang, canonical, testi, link presenti → `[A]`, le fai tu
  con il tool di fetch web disponibile.
- Voci su header HTTP (HSTS, CSP, cache, catena di redirect), status code, TLS → `[M]` solo
  se **non** hai una shell. Se ce l'hai, eseguile: vedi l'elenco delle promozioni.
- Voci su Core Web Vitals di campo e crawl completo → servono strumenti esterni comunque.
  Marca `NON VERIFICATO` e indica lo strumento (PageSpeed Insights, Screaming Frog,
  securityheaders.com).
- Se ti passano un export di Screaming Frog / Semrush / un report Lighthouse, **usalo**: molte
  voci `[M]` diventano `[A]` a partire da quel file.

Non simulare mai l'output di uno strumento che non hai eseguito.

## Flusso

```
QA sito, avanzamento:
[ ] 1. Contesto raccolto, sezioni applicabili filtrate, assunzioni scritte
[ ] 2. Raccolta prove: home + 5-10 pagine campione (una per template), robots.txt,
       sitemap, 404, pagine legali, eventuali export forniti dall'utente
[ ] 3. Esecuzione voci [A] sezione per sezione, annotando la prova per ciascuna
[ ] 4. GATE 1: test della prova su ogni esito emesso (vedi "I due gate di onestà")
[ ] 5. Voci [B]/[M]: non inventare l'esito, scrivi l'istruzione operativa per chi le farà
[ ] 6. Report: tabella per sezione + piano di intervento prioritizzato
[ ] 7. Checklist spuntata, solo se chiesta: generata dal report appena scritto (vedi "Report")
[ ] 8. GATE 2: prima di consegnare (vedi "I due gate di onestà")
```

Il **campionamento** del passo 2 conta più della quantità: una pagina per ciascun template
(home, categoria, dettaglio prodotto/articolo, pagina statica, form, checkout, 404, e per i
multilingua la stessa pagina in due lingue). Venti pagine dello stesso template non
aggiungono informazione.

## Esiti e severità

Esiti ammessi: `OK`, `KO`, `PARZIALE`, `N/A`, `NON VERIFICATO` (con motivo).

Severità di un `KO`:

- **BLOCCANTE**: non si va live / va risolto entro 24h. Sito o pagine chiave irraggiungibili,
  staging indicizzabile, checkout o form rotti, HTTPS assente o certificato scaduto, dati
  personali esposti, cookie non tecnici senza consenso, backup inesistenti.
- **ALTA**: impatto diretto su traffico, conversioni, conformità o sicurezza. Da risolvere
  prima del lancio o nello sprint corrente.
- **MEDIA**: degrada qualità o performance senza rompere nulla. Prossimo ciclo.
- **BASSA**: rifinitura, debito tecnico, nice-to-have.

La severità indicata in checklist è il **valore di default**: alzala o abbassala in base al
contesto e **scrivi perché**. Un `alt` mancante su un'icona decorativa non è come su un
bottone del carrello.

## I due gate di onestà

Non sono raccomandazioni: sono condizioni di uscita.

**Test della prova (gate 1).** Una voce può essere `OK` o `KO` solo se sai incollare
*adesso*, nella colonna Prova, una di queste: URL esatto + valore osservato, output del
comando eseguito, nome del file dell'utente e punto in cui l'hai letto. Se la prova sarebbe
una parafrasi, un'inferenza o un ricordo, l'esito è `NON VERIFICATO`. **Se la nota della
riga contraddice l'esito, vince la nota.**
Output obbligatorio: una riga nell'appendice del report, `Gate 1: X voci riviste, Y declassate`.
Se Y = 0 su un audit ampio, ricontrolla le voci più facili da dare per buone: quelle viste su una
pagina sola e quelle dedotte dallo stack. Se reggono tutte, Y = 0 è un esito valido.

**Gate 2 (prima di consegnare).** Ogni BLOCCANTE ha prova citabile e un'azione con
destinatario. Ogni `OK` è osservato. Ogni `N/A` ha il motivo. I numeri della tabella di
sintesi sono **contati**, non stimati, e quadrano col piano di intervento.

Se hai prodotto la checklist spuntata, il gate include tre riscontri di quadratura — sono
conteggi, si fanno in un minuto e sono l'unica difesa contro due documenti che divergono:

1. Le caselle `[x]` sono **esattamente** quante gli `OK` della tabella di sintesi.
2. Le righe del file sono **esattamente** quante le voci in perimetro dichiarate in testa.
3. Nessuna casella vuota è priva del motivo accanto.

Se un riscontro non torna, l'errore è nella checklist spuntata: rigenerala dal report, non
correggere il report per farlo quadrare.

### Razionalizzazioni tipiche e risposta obbligata

| Quello che stai pensando | Cosa fai |
|---|---|
| "Su WordPress/Shopify di norma c'è" | `NON VERIFICATO`. La norma non è un'osservazione. |
| "L'ho visto su un'altra pagina, sarà uguale" | `PARZIALE`, elencando le sole pagine osservate. |
| "Il nome del file dice 200×200" | `NON VERIFICATO`. Il nome non è una misura. |
| "Il cliente mi ha detto che funziona" | `NON VERIFICATO (dichiarato dal cliente)`. |
| "Un report con 60 NON VERIFICATI fa brutta figura" | Consegnalo così. |
| "L'utente ha fretta" | La sintesi si accorcia, gli esiti no. |

Se l'utente chiede di togliere i `NON VERIFICATO`: rifiuta e spiega che sono il perimetro
di validità del documento. Puoi spostarli in appendice, non cancellarli.

## Report

Usa `assets/report-template.md`. Regole che valgono più del formato:

- **Il report lo legge il cliente**: frasi brevi, con le sue parole. Tag, modalità e gate
  stanno solo nell'appendice. Trattino lungo al massimo uno per paragrafo.
- **Ogni KO porta la sua prova**: URL preciso, riga di codice, screenshot, valore misurato.
  "Meta description assente" senza URL è un'opinione, non un rilievo.
- **Ogni KO porta l'azione**, non solo il problema: cosa fare, dove, chi (dev / SEO / legale /
  cliente), stima grossolana dello sforzo.
- **In testa al report**: data, ambiente collaudato, cosa NON è stato verificato e perché.
  Questa sezione va scritta per prima, non aggiunta alla fine. Il resto del contesto (tipo di
  sito, capacità, perimetro, promozioni, gate) va nell'appendice finale.
- Il piano di intervento è **ordinato per severità, poi per rapporto impatto/sforzo**, e sta
  in una tabella sola: è l'unica pagina che verrà letta davvero.

### La checklist spuntata (solo su richiesta)

Se chi lavora con te la chiede, oltre al report consegna `checklist-esiti-{{sito}}.md`, con `assets/checklist-esiti.md`: le
voci in perimetro raggruppate per sezione, casella spuntata **solo** dove l'esito è `OK`.

Si compila **per ultimo, dal report già scritto**, riga per riga. È una vista, non una seconda
verifica: non contiene esiti che nel report non ci siano, e non è un'occasione per rivedere un
giudizio già passato per il Gate 1.

Ogni casella vuota porta il motivo accanto: `KO` con severità, `PARZIALE`, `N/A`, oppure
`NON VERIFICATO` con lo strumento mancante. Questo è il file che il cliente aprirà per primo e
leggerà come "verde = fatto, vuoto = rotto": senza il motivo, i tuoi `NON VERIFICATO`, che
sono il perimetro di validità del lavoro, gli si presentano come altrettante accuse.

Se serve lavorarla in un foglio (ticket, assegnazioni, avanzamento nel tempo), esporta lo
stesso contenuto anche in .csv o .xlsx, una riga per voce.

## Falsi positivi da evitare

Prima di segnalare, controlla di non essere caduto in uno di questi:

- `noindex` o `Disallow` **voluti** su aree private, filtri, carrello, risultati di ricerca.
- Parametri di tracciamento che sembrano contenuto duplicato ma hanno il canonical giusto.
- Redirect "sbagliati" che sono in realtà normalizzazioni volute (www, trailing slash, lingua).
- CDN e servizi terzi che restituiscono header diversi dall'origin.
- Un `KO` di accessibilità automatico non è una violazione WCAG accertata: gli strumenti
  automatici intercettano circa un terzo dei problemi reali e producono falsi positivi.
  Riporta il rilievo, non emettere una sentenza di conformità.
- Non dichiarare mai **conformità legale** (GDPR, EAA, codice del consumo): puoi rilevare
  indizi e segnalare cosa manca, la conformità la valuta un legale. Scrivilo nel report.

## Manutenzione della checklist

`reference/checklist.md` invecchia: metriche, obblighi e strumenti cambiano. Se durante
l'esecuzione una voce risulta superata o ne manca una rilevante, segnalalo nella risposta
sotto "Proposte di aggiornamento checklist" invece di correggere in silenzio. Nel report non
va: è del cliente, non della skill.
