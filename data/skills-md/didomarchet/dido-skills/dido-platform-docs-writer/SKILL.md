---
name: dido-platform-docs-writer
description: Usare quando l'utente chiede di documentare un repository, scrivere o rifare il README o il documento di un servizio, spiegare come si avvia in locale o come va in produzione, descrivere variabili d'ambiente, deploy e troubleshooting, allineare documentazione obsoleta al codice attuale, o segnala che nessuno sa più come far partire il progetto. Non per documentazione di prodotto, API reference generabile dal codice o testi commerciali.
---

# Documentazione operativa di un repository

Manuali che servono a **far girare** il progetto: avviarlo in locale, metterlo in produzione,
capire cosa si è rotto quando si rompe. Il lettore è chi manutiene, non chi valuta: non gli
serve sapere che il progetto è scalabile, gli serve il comando esatto e la variabile esatta.

**Regola d'oro: si documenta solo ciò che i file del repository dimostrano.** Ogni affermazione
operativa (una porta, una variabile, un comando, un dominio, un passo di deploy) deve essere
riconducibile a un file preciso. Quando non lo è, l'esito è `NON DEDUCIBILE`, ed è un esito
legittimo e frequente. Un README con dieci sezioni verificate e tre marcate NON DEDUCIBILE vale
molto più di uno completo per metà inventato: è l'unico modo in cui questa documentazione resta
affidabile a sei mesi di distanza.

**Un fatto, un posto.** Il documento dice ciò che i file non dicono da soli: le procedure (come
si avvia, si aggiorna e si ripara, con i comandi e gli URL che servono), le decisioni e il loro
perché, il ruolo di ogni servizio, ciò che manca. Per il resto rimanda alla fonte: porte,
versioni, variabili, immagini e volumi stanno nel loro file, e il documento dice quale. Una
tabella, un elenco o un diagramma che riporta ciò che un file già definisce è una copia: è giusta
il giorno in cui la scrivi e resta indietro al primo cambio. Per questo una copia trovata in un
documento esistente si toglie, anche se è ancora giusta, e al suo posto va il rimando.

## Quando NON usarla

- **Documentazione di prodotto o per l'utente finale**: guide per chi *usa* l'applicazione,
  non per chi la fa girare. Sono un altro mestiere e un altro tono.
- **API reference** (la spec OpenAPI, docstring, typedoc): sta nella sua fonte, e riscriverla
  in un documento crea una seconda verità che diverge.
- **Repository che non hai potuto leggere**: solo un URL, uno screenshot, o la descrizione a
  voce dell'utente. Senza file non c'è niente da dedurre — dillo e fermati, non ricostruire.
- **Scelte di architettura o di stack**: questa skill descrive ciò che c'è, non propone ciò che
  dovrebbe esserci. Se durante la lettura emergono problemi (secret fuori dai file env, servizi senza
  healthcheck, script che puntano a host non definiti da nessuna parte) annotali in coda al
  documento sotto "Punti da verificare" e vai avanti: il manuale non diventa una review.
  Prima controlla commenti, decisioni e limiti noti: una scelta documentata (per esempio un
  container senza healthcheck per scelta) non è un punto da verificare.
- **Modifiche minime** (un comando da correggere, un rimando da aggiornare): falle e basta,
  il workflow completo qui non serve.

## Obiettivi

- Rendere il progetto avviabile da chi non l'ha scritto, senza chiedere niente a nessuno.
- Distinguere sempre **sviluppo locale** e **produzione**, e dire chi gestisce cosa in ciascuno.
- Documentare la configurazione **reale rilevata nel repo** (orchestratore, proxy, motore di
  deploy, gestore delle variabili) chiamandola col suo nome. Se il repo usa Coolify e Traefik
  scrivi Coolify e Traefik; se usa Kubernetes, Fly.io o una unit `systemd`, scrivi quelli.
  **Nessuno stack è quello atteso.**
- Prevenire i blocchi operativi: prerequisiti scomodi, dipendenze fra servizi, errori ricorrenti.

### Vincoli di scrittura, al posto del tono

- Ogni frase serve a chi deve avviare, aggiornare o riparare il progetto. Con uno o due servizi
  il README sta intorno alle 1.000 parole e non supera le 1.500; con più servizi resta un quadro
  d'insieme e il dettaglio va nei documenti per servizio.
- Un file si cita quando chi legge deve aprirlo, per nome e senza numero di riga: le righe si
  spostano a ogni modifica. Il controllo riga per riga lo fa il gate, non il documento.
- Frasi brevi e punteggiatura normale: trattino lungo al massimo uno per paragrafo, tra un
  termine e la sua spiegazione i due punti.
- Niente aggettivi non misurabili ("potente", "scalabile", "moderno"): se non è un valore o un
  comando, non è documentazione operativa.
- Ogni comando in un blocco `bash` copiabile e completo, non a frammenti in prosa.
- Ogni confronto fra ambienti in tabella, mai in paragrafo.
- Imperativo e seconda persona per le istruzioni ("Avvia", "Verifica"), non condizionale.

## Passo 1. Discovery (l'inventario è parte dell'output)

Non scrivere una riga prima di aver letto i file. Non incollare in risposta il contenuto grezzo
di ciò che leggi, ma **dichiara sempre cosa hai letto**: l'inventario è la base di prova del
documento e si consegna insieme ad esso. Una discovery che non lascia traccia non è
distinguibile da una discovery non fatta.

| Cosa cerchi | Dove | Cosa stabilisce |
|---|---|---|
| Stack e runtime | `package.json`, `pyproject.toml`, `go.mod`, `composer.json`, lockfile | linguaggio, versioni, script già definiti |
| Orchestrazione | `Dockerfile*`, `compose*.y*ml`, override, chart, manifest | servizi, porte interne, volumi, dipendenze, comandi di avvio |
| Configurazione | `.env.example`, `config/`, `settings.*` | variabili, quali obbligatorie, quali hanno default |
| Automazione | `Makefile`, `justfile`, `scripts/`, `.github/workflows/` | comandi reali, cosa gira in CI e cosa resta manuale |
| Rete ed esposizione | label del proxy, `nginx.conf`, config del reverse proxy, ingress | chi termina TLS, chi instrada, quali host |
| Storia | README attuale, `CHANGELOG`, `docs/` | cosa era vero prima, da verificare e mai da recepire |

Chiudi la discovery con questa riga, che apre la risposta:

`Discovery: N file letti. Stack {…}, servizi {…}, deploy {…}. Non trovato: {elenco}.`

Se un'area non ha file che la coprano (niente CI, niente proxy, niente backup) **quella è
un'informazione**, non un buco da riempire: finisce in `non trovato`, e da lì nelle sezioni
NON DEDUCIBILE. Se il repository non è leggibile (hai solo un URL, uno screenshot o il
racconto dell'utente) fermati e dillo: senza file non c'è nulla da dedurre.

## Esiti e gate

Ogni affermazione operativa ha uno di tre esiti:

| Esito | Quando | Come si scrive nel documento |
|---|---|---|
| **Documentato** | c'è un file che lo dimostra | testo normale |
| **PARZIALE** | il file mostra il meccanismo ma non i valori (la variabile esiste, il valore no) | testo + nota `da confermare: {cosa}` |
| **NON DEDUCIBILE** | nessun file lo dimostra | blocco esplicito, mai testo plausibile |

Forma obbligatoria del blocco, da copiare:

> **NON DEDUCIBILE — {argomento}.** Nel repository non c'è nessun file che descriva {cosa}.
> File controllati: {elenco}. Per completare la sezione serve: {chi o cosa può fornirlo}.

**Gate prima di consegnare.** Non è una raccomandazione, è una condizione di uscita:

1. Ogni comando scritto compare in un file del repo, o è composto da elementi che ci compaiono.
2. Ogni variabile nominata esiste in `.env.example`, nel compose o nel codice.
3. Ogni porta, host e percorso scritto nel documento viene da un file, non dalla memoria.
4. Ogni sezione richiesta ma non supportata dai file porta il blocco NON DEDUCIBILE.
5. Ogni voce di troubleshooting riguarda un componente che nel repo esiste davvero.
6. Nessuna tabella, elenco o diagramma riporta ciò che un file già definisce (porte, versioni,
   variabili, immagini, volumi): al suo posto c'è il nome del file.

Chiudi con la riga: `Gate: X affermazioni riviste, Y declassate a NON DEDUCIBILE.`
Se Y = 0 su un repository che non hai scritto tu, ricontrolla le affermazioni più facili da dare
per scontate, come porte, versioni, deploy e backup. Se hanno tutte un file dietro, Y = 0 è un
esito valido.

### Razionalizzazioni tipiche e risposta obbligata

| Quello che stai pensando | Cosa fai |
|---|---|
| "Con Postgres la porta è la 5432" | Rimanda al file che la espone. Se non c'è: NON DEDUCIBILE. |
| "Una tabella con variabili e porte è comoda da leggere" | È una copia di `.env.example` e del compose: resta indietro al primo cambio. Rimanda ai file. |
| "Un progetto così avrà un backup" | NON DEDUCIBILE. L'assenza di backup è essa stessa un rilievo. |
| "Metto una sezione TLS generica, poi la correggono" | Non la correggerà nessuno: il testo plausibile è peggio del vuoto. |
| "L'utente ha chiesto proprio la sezione pipeline" | La sezione si scrive, il contenuto è il blocco NON DEDUCIBILE. |
| "Il vecchio README dice così" | Se è una copia di un file, toglila e rimanda al file. Il resto vale solo se il codice attuale lo conferma, altrimenti va segnalato. |
| "Il comando standard di questo framework è…" | La norma non è questo repository. |
| "Senza quella sezione il README sembra incompleto" | È incompleto il repository, e il README deve dirlo. |

Se l'utente chiede di togliere i blocchi NON DEDUCIBILE: rifiuta e spiega che sono il
perimetro di validità del documento. Puoi raccoglierli in una sezione finale
"Da completare", non cancellarli.

## Struttura dei documenti

Le strutture in `reference/struttura-documenti.md` sono un **repertorio**, non un indice da
riempire. Una sezione entra nel documento solo se ricorre uno di questi due casi:

- **la discovery l'ha trovata** → si scrive con i valori reali, citando il file;
- **l'utente l'ha chiesta esplicitamente e la discovery non l'ha trovata** → la sezione
  compare col solo blocco NON DEDUCIBILE.

Una sezione che nessuno ha chiesto e che i file non supportano **non si scrive**: la sua
assenza è documentata in "Da completare", non riempita di testo generico.

Esempio della differenza. Se `.env.example` contiene `BACKUP_DIR=` ma nel repo non c'è né
uno script né un cron che lo usi, la sezione Backup si scrive così:

> **NON DEDUCIBILE — Backup.** In `.env.example` esiste la variabile `BACKUP_DIR` ma nessun
> file che la consumi: nessuno script, nessun servizio nel compose, nessun workflow. Non è
> deducibile se, quando e con che retention il backup venga eseguito, né chi lo ripristini.
> File controllati: `.env.example`, `compose.yaml`, `scripts/`, `.github/workflows/`. Serve
> conferma da chi amministra il server.

Definito il perimetro delle sezioni, carica `reference/struttura-documenti.md` e usa i modelli
in `assets/` — uno per volta, quando stai per scrivere quel documento, non prima.

## Troubleshooting

**Le voci di troubleshooting si derivano dall'inventario, non da una lista fissa.** Una voce
entra nel documento solo se il componente che la causa compare fra i file letti: niente
sezione TLS se nel repo non c'è chi emette i certificati, niente sezione DNS se nessun file
nomina un dominio, niente crash loop da variabili mancanti se non esiste un `.env.example`.
Il repertorio per componente sta in `reference/troubleshooting.md`, organizzato per
tecnologia rilevata (reverse proxy, orchestratore container, CI/CD, database, accesso al
server): usalo come repertorio da cui pescare, mai come indice da riempire. Nel documento
vanno al massimo cinque voci, le più probabili per questo repo.

Se il repo usa una tecnologia che il repertorio non copre, scrivi comunque le voci (dedotte
dai suoi file) e segnalale nella risposta sotto "Proposte di aggiornamento del repertorio",
invece di aggiungerle in silenzio. Nel documento non vanno: è del progetto, non della skill.

## Consegna

Se l'ambiente permette di scrivere file, **scrivi i file** (`README.md`,
`docs/NOME-SERVIZIO.md`, i commenti in `.env.example`) e in risposta lascia solo il riepilogo. Incolla il Markdown completo
in chat solo se non puoi scrivere su disco o se l'utente lo chiede: sono host diversi, non
assumere quale sia il tuo.

La risposta contiene, in quest'ordine:

1. La riga di `Discovery` e la riga di `Gate`, una riga ciascuna: nomi e numeri, non descrizioni.
2. L'elenco dei file creati o modificati, col percorso.
3. **Da completare**: i blocchi NON DEDUCIBILE raccolti, ciascuno con chi può chiudere il punto.
4. **Punti da verificare**: anomalie viste nel repo che il manutentore dovrebbe guardare
   (secret fuori dai file env, servizi senza healthcheck, script che puntano a host non definiti).
   Nel documento vanno al massimo i cinque più gravi, quelli che impediscono l'avvio o
   espongono dati e segreti; gli altri stanno solo nella risposta.
5. **Proposte di aggiornamento del repertorio**, se ce ne sono.

Ogni voce di questi elenchi sta in una riga.

**Riscrivere un documento esistente non è cancellarlo.** Se sostituisci un README, elenca nella
risposta le sezioni che hai tolto e perché (copie di un file, contraddette dal codice,
obsolete). Per un'affermazione contraddetta scrivi cosa diceva e il file che la smentisce: chi
la credeva vera deve saperlo. Il contenuto non operativo che i file non dimostrano ma che
nemmeno smentiscono (contatti, accordi, cronologia, note del team) si conserva così com'è: non
è materiale da dedurre, quindi non è materiale da rimuovere.
