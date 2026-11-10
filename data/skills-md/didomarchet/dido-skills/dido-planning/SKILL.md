---
name: dido-planning
description: Usare quando un lavoro di Dido ha più passi o va oltre una sessione (un progetto nuovo, una milestone, una funzionalità grande, un ridisegno, una migrazione, una richiesta che tocca app e backend insieme), quando Dido chiede un piano, una roadmap, gli step, "dove siamo", di riprendere un lavoro, di chiudere una milestone o di scrivere il report di chiusura, e quando arriva una sua richiesta a metà di un piano.
---

# Pianificare e portare a termine i lavori grandi

Il metodo con cui Dido porta avanti un lavoro di più passi: un piano scritto e approvato, passi piccoli verificati uno alla volta, un report alla chiusura, e le doc come memoria tra una sessione e l'altra. **Skill richiesta:** dido-code-style, più la skill dello stack.

Una richiesta piccola (un fix, un ritocco, una pagina) non passa da qui: si fa e basta. Se non è chiaro se serve un piano, proponilo in chat in poche righe e lascia scegliere a Dido.

Le skill di processo di altri (superpowers: brainstorming, writing-plans, executing-plans, subagent-driven-development) si possono usare per le loro tecniche, ma piano, cartelle, domande, commit e report restano quelli di questa skill, anche quando quelle dicono "sempre" (dido-code-style, `riferimento/skill-di-terzi.md`).

## Chi decide cosa

- **Dido** decide il prodotto (cosa fa, per chi, le priorità), il design delle schermate e dei gesti, approva il piano, decide quando una milestone si apre e si chiude, e fa le prove sui dispositivi veri.
- **L'agente** fa le scelte tecniche (schema, migration, librerie, decisioni) e le scrive nel piano, dentro i paletti di Dido: semplicità, scalabilità, niente colli di bottiglia, niente risorse sprecate, niente overengineering. A Dido si chiedono le decisioni di prodotto e i consensi che le skill `dido-*` gli riservano (operazioni distruttive, produzione, parti chiuse).
- Prima del piano si chiede solo ciò che manca e cambia il risultato, in un messaggio solo, con una proposta per ogni domanda. Se Dido approva senza rispondere vale la proposta, e il piano la riporta. Con un Figma, il brief è il Figma.

## Dove stanno le cose

Nel `docs/` del repo principale del progetto: quello che il suo `AGENTS.md` o `CLAUDE.md` indica, di solito l'app. Un piano che tocca più repo (app, backend, admin) sta lì, e negli altri repo i commit citano piano e passo: una copia sola.

| File | Cosa |
|---|---|
| `docs/PROJECT_CHARTER.md` | solo per un prodotto nuovo: requisiti, invarianti, milestone con i criteri di chiusura, registro delle richieste di Dido (D1, D2…). Su cosa fa il prodotto vince il charter, su come si scrive il codice vincono le skill |
| `docs/plans/<nome>.md` | un piano per milestone o per funzionalità |
| `docs/design/<nome>.html` | il design da far approvare prima di costruire |
| `docs/decisions/NNNN-<titolo>.md` | una decisione tecnica non banale. Se il repo ha già un registro delle decisioni (nel backend `docs/DECISIONI-ARCHITETTURA.md`), va lì, con il suo schema |
| `docs/reports/<nome>.md` | il report di chiusura |
| sezione "Dove siamo", in fondo al piano in corso | lo stato, aggiornato a ogni passo: è la memoria tra le sessioni |

## Il piano

```md
# Piano <nome>: <cosa, in una riga>

> Stato: **bozza, da approvare** (oppure **approvato da Dido il gg/mm/aaaa**, "<le sue parole>").
> Riguarda <repo e parti>. Lo stato sta in "Dove siamo", in fondo a questo piano.

## Cosa si chiede e cosa si fa
| Voce (dal charter o dalla richiesta) | Cosa si fa |

**Si chiude quando**: <criteri che si verificano con una prova>.

## Cosa c'è già
## Step
1. **Design** delle schermate e dei gesti che il Figma non ha, da approvare prima di costruire (`docs/design/`). Senza un'interfaccia nuova, niente design.
2. **Decisione tecnica** (`docs/decisions/NNNN-<titolo>.md`), con le misure che servono a prenderla.
3. Un passo per ogni pezzo che si verifica da solo (backend, app, una funzione).
4. **Prove** di chiusura.
5. **Revisione del codice** indipendente, con le correzioni.
6. **Chiusura**: report e "Dove siamo".
## Interfacce tra i passi  (solo se un passo usa ciò che ne produce un altro: funzione, endpoint, campo, con i nomi esatti)
## Casi che i test non coprono  (gli input e i guasti più probabili che nessun test dei passi prova, ognuno con il test da aggiungere al passo giusto)
## Misure            (solo se il lavoro ha un rischio di memoria, carico o tempi)
## Dipendenze nuove  (o "nessuna")
## Cosa non si fa    (e dove andrà)
## Domande per Dido  (solo di prodotto, con la proposta; le risposte con la data)
## Dove siamo        (a ogni passo: data, passo, commit, come è stato provato, cosa resta, scelte fatte senza chiedere; l'ultimo commit rivisto)
```

- I passi sono piccoli e ognuno si verifica da solo. Uno che non si riesce a provare va diviso.
- Una richiesta di Dido a metà piano che cambia il piano diventa un passo con la sua data, messo dove va fatto (8b, 9b.1, 9b.2…). Se c'è il charter, entra anche nel registro. Una richiesta piccola si fa e si scrive in "Dove siamo".
- Ciò che resta fuori si scrive in "Cosa non si fa", così non torna a ogni sessione.
- Niente si perde: ciò che emerge durante il lavoro (un problema fuori dal passo, una richiesta, un dubbio, un rinvio) entra subito nel piano, con la data: un passo nuovo, "Cosa non si fa" o "Domande per Dido". Mai solo in chat.

## Eseguire

- Un passo alla volta, nell'ordine del piano. Niente funzioni di una milestone successiva: al massimo gli agganci nel modello dei dati che il piano approvato prevede.
- Il design viene prima del codice: un'interfaccia nuova non si costruisce prima dell'ok di Dido. Il design lo propone l'agente, con gli screenshot o un prototipo in `docs/design/`.
- Un invariante del charter non si viola mai: se un passo sembra chiederlo, ci si ferma e si chiede.
- Una scelta tecnica non banale va nel registro delle decisioni (vedi la tabella) nella stessa modifica: contesto, scelta, cosa è stato verificato, alternative scartate. Se cambia il charter, si aggiorna anche lui.
- Ogni passo finisce verificato (dido-code-style, "Fatto vuol dire verificato") e con "Dove siamo" aggiornato: cosa è fatto, come è stato provato, cosa resta, le scelte fatte senza chiedere.
- Un commit per passo (dido-code-style dice quando), con piano e passo nel messaggio, nella lingua del progetto: `M2 step 4: filtri della lista ordini`. Un agente che lavora da solo su un repo fa i suoi commit. Se sullo stesso repo lavorano più agenti, committa solo chi coordina, dopo aver guardato il diff e rilanciato le prove.

## Chiudere

Prima del report si ripassa il piano voce per voce: ogni riga di "Cosa si chiede", ogni passo, ogni domanda e ogni cosa emersa ha un esito, e quello che non è fatto va in "Cosa resta aperto" con dove andrà. Poi una revisione del codice indipendente sulle modifiche dal commit dell'ultima revisione, che "Dove siamo" segna. La fa un agente che non ha scritto il codice (un subagente, Codex), con il diff e senza le conclusioni di chi l'ha scritto. Solo Alta e Media (dido-code-style, Parte 2), ognuna corretta con un test che senza la correzione fallisce dove un test si può scrivere, altrimenti con la prova nel report. Poi il report:

```md
# Report <nome>: <cosa>

> Stato al gg/mm/aaaa: **pronta per la chiusura** (o cosa manca; **chiusa da Dido il gg/mm/aaaa** quando la chiude). Piano: [<nome>](../plans/<nome>.md).

## In breve
| Voce | Esito (con la decisione o il passo) |
## La prova di chiusura    (cosa, su cosa, con i numeri)
## Prove                   (lint, test, E2E, moduli spenti: comando, data, esito)
## Revisione del codice    (cosa ha letto, cosa ha trovato, come è stato corretto)
## Sicurezza              (cosa è stato controllato, cosa è emerso)
## Scelte fatte senza chiedere
## Cosa resta aperto
## Come rifare le prove
```

La milestone la chiude Dido. Fino ad allora il piano resta in corso. Le parti che Dido chiude vanno in `docs/parti-chiuse.md` (dido-code-style).

## Riprendere

A inizio sessione si leggono il piano in corso con il suo "Dove siamo" e le ultime decisioni, prima di toccare il codice. Ciò che è segnato come fatto non si rifà: si riapre solo con un difetto riprodotto e, in una parte chiusa, con l'ok di Dido.
