---
name: project-naming
description: Use when asked to name or rename a project, repository, tool, package, or paper, or when a name is rejected as hard to say, taken, or misleading.
license: SEE LICENSE IN LICENSE.md
metadata:
  author: Vivswan
---

# Project Naming

> A name is chosen from a table, never from a list. Every candidate reaches the owner with its registry row, its meaning check, and its score against the names the owner already likes. The owner's taste is asked for first and never guessed.

```text
1 interview -> 2 brief -> 3 lanes (parallel) -> 4 machine check -> 5 meaning check
                   ^                                                      |
                   |                                                      v
              7 rejection round  <--  6 one table to the owner  <--  verdicts
                                              |
                                              v  (owner picks)
                                8 re-verify same day -> 9 record and "not checked"
```

## When to Apply

- "name this project" / "is there a better name for this?" / "what should I call the package?"
- A name was rejected: hard to pronounce, already taken, or it points the reader the wrong way
- A paper, tool, or dataset needs a name before it is published

## Workflow

### 1. Interview

Ask before generating anything. The owner's answers are the brief; a lane without them converges on the generator's taste.

```text
Which two or three existing names do you like the SOUND of? (any product, any field)
What killed the last name, in your words?
What must this project be able to grow into?
Where will the name be claimed? (PyPI, npm, crates, Homebrew, Docker Hub, Maven, Hugging Face, GitHub, Bluesky, which domains, arXiv)
Which languages do your users read?
```

### 2. Brief

Turn the answers into one page every lane reads. The owner approves it before any name is generated.

```text
exemplars:   <the names the owner likes>, scored 1 to 5 by closeness
vector:      <per exemplar: letters, syllables, stress, open or closed vowels, Latinate or Germanic, hard letters>
grows into:  <scope in one line>
claims:      pypi npm docker hf github dns:com,ai
languages:   <the languages the users read, from the interview>
hard gate:   the table under Conditions, plus anything the owner added
soft scores: exemplar closeness, elegance, room to grow
```

The hard gate is general. The owner's taste lives in the exemplars, so a different owner gets a different search from the same skill.

The vector decomposes each exemplar once, so every lane scores closeness against the same six facts instead of its own impression. An example, for an owner who likes `vercel` and `linear`:

```text
vercel:  6 letters, 2 syllables, stress on the first, closed vowels, Latinate, no hard letters
linear:  6 letters, 3 syllables, stress on the first, open vowels, Latinate, no hard letters
```

### 3. Lanes

One lane per style, run in parallel (the `/orchestrator-mode` skill, where installed, owns the fan-out). Each lane brainstorms 50 to 100 names, drops what fails the gate by eye, and checks its best 20 with the script in step 4.

| Lane | Generates |
| --- | --- |
| real word | one existing word, common or rare |
| invented | a coined word with the exemplars' sound |
| Latin or Romance | forms from Latin, Italian, Spanish, Portuguese roots |
| metaphor | an object or place that evokes the work |
| two short words | a compound of two real words |
| borrowed | a word from a named language, with its plain meaning |

Drop a lane the brief rules out. Add a lane when the owner's exemplars share a style the table lacks.

Where the harness has a pipeline or workflow tool, steps 3 to 6 are one run, not prose between agents. Each lane returns rows in a fixed shape (name, say it, the three scores, registries, meaning verdict, verdict) plus what it dropped. A lane with no survivor reruns once with a tightened prompt.

The merge dedupes against the brief's rejected list and runs the arXiv and `github-repo` columns once.

The rejection round (step 7) sits between runs: rewrite the brief, rerun only the lanes it changed. A lane report that travels as a message gets cut; rows in a schema do not.

### 4. Machine check

```bash
bun "<skill-dir>/scripts/check-name.mts" <name> <name> ...
bun "<skill-dir>/scripts/check-name.mts" --registries pypi,npm,docker,hf,github-user,dns-com,dns-ai <name>   # the brief's claims except github-repo
```

```text usage=skills/project-naming/scripts/check-name.mts
usage: check-name.mts [--domain <tld>]... [--registries <id,id,...>] [--no-arxiv] [--json] <name>...
       check-name.mts --list-registries
  --domain <tld>          a DNS column per zone (default: com, ai, dev; the list replaces the default)
  --registries <id,...>   the availability columns to run; the gate columns run on every name regardless
  --no-arxiv              skip the arXiv column (one request every three seconds)
  --json                  one JSON object, rows and failures, instead of the table
  --list-registries       the live column table: id, label, taken control, gate
exits: 0 every row printed and every control answered as expected;
       1 a control answered wrongly: the named columns are not evidence; 2 usage error
```

One row per name, one column per registry; the registries live in one table in `scripts/columns/registries/table.mts`, and `--list-registries` prints it. Every cell reads `free`, `taken(<why>)`, or `unknown(<why>)`, except the `say` column's `note(<reading>)`:

```text
name    pypi  npm                 crates  homebrew                        docker                  maven  hf    github-user           github-repo  bluesky                arxiv  dns-com                     dns-ai  wiktionary                    urban                typosquat                                                         say
lumera  free  taken(npm package)  free    free                            taken(docker hub user)  free   free  taken(github handle)  free         taken(bluesky handle)  free   taken(lumera.com resolves)  free    taken(word in Italian,Latin)  free                 free                                                              note(ok(3s))
tarnix  free  free                free    taken(homebrew formula tarnix)  free                    free   free  free                  free         free                   free   free                        free    free                          taken(1 entry: ...)  free                                                              note(flag(2s; hard x))
numpi   free  free                free    free                            free                    free   free  free                  free         free                   free   free                        free    free                          free                 taken(1 edit from numpy on claimed pypi (top 5000 by downloads))  note(ok(2s))
```

- `--registries` selects the availability columns; the gate columns `say`, `typosquat`, `wiktionary`, and `urban` run on every name whatever it names, so a selective run cannot skip them: the hard gate reads the first two, and step 5 reads the two meaning columns, on every name.
- Two controls run with every batch: per registry column, a name known to be taken there (the zone's own delegation for DNS, spelled `@`; a word with a flagged sense for Wiktionary), and one random string that must be free everywhere. A column that answers either wrongly is reported on stderr as a failed instrument and the exit code is 1. Do not read that column.
- `unknown` is not `free`. A rate-limited arXiv or a 5xx stays `unknown` in the table; rerun later or drop the column with `--no-arxiv`.
- arXiv allows one request every three seconds, and the script spaces its own that far. Lanes run with `--no-arxiv`; the lead runs the arXiv column once, over the merged shortlist, in step 6.
- Maven Central's search holds some requests for half a minute and more, so the script runs its lookups one at a time and asks again after a short wait; an `unknown(maven TimeoutError ...)` cell is three holds in a row, rerun later.
- Docker Hub ids are 4 to 30 lowercase letters and digits; a name outside that reads `unknown` there because Docker would refuse it, not because it is free.
- GitHub counts an exact-name repository as taken from 20 stars. Pass `GH_TOKEN` or be logged into `gh` for the per-token search limit.
- GitHub allows 30 searches a minute per token, 10 with none, shared by every lane, so the script spaces its searches two seconds apart with a token and six without: a 20-name batch takes about a minute on the `github-repo` column, three with no token. A rate-limited reply is `unknown(github search rate-limited; retry later)`.
- Lanes leave `github-repo` out of `--registries`; the lead runs that column once, over the merged shortlist, in step 6, as with arXiv.
- Homebrew's per-name pages answer an entry's own name only (`python` is an alias of `python@3.15` and has no page), so the script reads the formula and cask indexes whole, kept a day in the same cache as the typosquat lists. The cell names the formula or cask, and `via alias`, `via old name`, or `via old token` when the name is one of those.
- The `typosquat` column is one edit (a letter added, dropped, changed, or two swapped) from a popular package. The cell names the package, the registry as `claimed` or `unclaimed` (`--registries` names the claimed ones; without it every registry is claimed), and the list it came from. The lists are kept a day under the OS temp dir in `check-name-cache`.
- A list that could not be read is named in the same cell beside any hit (`taken(1 edit from lumeras on unclaimed pypi (...); claimed crates lookup failed (crates ranking page 1 HTTP 503))`), and is the cell when nothing hit. A hit list with a failed source is not complete: rerun before reading it as the only collision.
- Those lists: PyPI's top 5000 by downloads (the public top-pypi-packages JSON); npm's top 5000 by downloads from the npm-high-impact dataset (npm publishes no ranking and its search is not fuzzy); crates.io's top 2000 by downloads, read from its crate list 100 a page (it publishes no ranking file, and its search returns what matches the name, not the popular crate one edit away).
- A list shorter than its source publishes is a cut list, not a shorter ranking: a crates page under its 100 entries, or a PyPI or npm list under the 5000 the column reads, fails that source the same way (`claimed crates lookup failed (crates ranking page 7 reply malformed: page has 40 entries, expected 100)`), since the names past the cut were never compared.
- crates.io asks automated clients for one request a second. Within a process the script spaces its crate lookups and the ranking's twenty pages that far: a 20-name batch is about twenty seconds on the `crates` column, per process.
- Across processes the ranking is fetched once a day: the first process to reach a page holds a lock file beside the cache entry while it fetches, and the others wait on it and read what it wrote, so six lanes on a cold cache are one fetch of the ranking, about twenty seconds.
- The `say` column reads the spelling alone, so it is a `note`, never free or taken, and runs no control: `ok(<syllables>s)` or `flag(<syllables>s; <reasons>)`. The "said as spelled" row under Conditions names each reason.
- `--json` prints the rows and the control verdicts as one object for a lane report.

### 5. Meaning check

The script's Wiktionary column reads every sense in every language from the page's wikitext and flags a register label (vulgar, offensive, slur, derogatory) on any of them; the Urban Dictionary column reads exact entries only. That covers the exact spelling. Near-homophones and transliterations are judgment, done on the names that survived step 4:

```text
for each survivor:
  say it aloud in every language the brief lists, then in Spanish, Portuguese, French,
    Italian, German, Hindi, Turkish, Arabic, Japanese, Mandarin, Russian, Korean:
    which word is it one sound away from?
  is it a drug, a perfume, a car, a company, an ML method? (one web search: "<name>" AI OR company OR app)
verdict per name: SERIOUS (the word named), MILD (the word named), NONE, each with its source
```

Native speakers do this step at naming agencies. The report says it was done by a model and lists it under "not checked" in step 9.

### 6. One table to the owner

All lanes merge into one ranked table. A name never reaches the owner without its row.

| name | say it | exemplar 1-5 | elegance 1-5 | grow 1-5 | registries | meaning | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<name>` | `<stress and vowels>` | `<score>` | `<score>` | `<score>` | `<free, or the taken cells named>` | `<NONE, MILD: word, SERIOUS: word>` | CLEAR / MINOR: `<the one collision>` / TAKEN |

- CLEAR: free on every claimed registry, meaning NONE.
- MINOR: one collision the owner can accept knowingly, named in the cell.
- TAKEN: fails the hard gate; shown only when the owner asked to see what was ruled out.

Two more checks run on each finalist before the table goes out, and their results join the `say it` and `meaning` cells:

- **Say it to a stranger.** Spell the name, letter by letter, to a fresh agent with no context, and ask it to pronounce the name and spell it back. A pronunciation that differs from the row's `say it` cell, or a spelling that differs from the name, is MILD, with the stranger's reading quoted.
- **Look at it.** Write the name four ways: lowercase, Title Case, as a terminal command (`<name> --help`), and as a short icon label. A form that misreads (a lowercase `l` for an `I`, a word that splits wrong in Title Case) is named in the row.

### 7. Rejection round

"None of these" is information, not failure. Ask what put them off and which row came closest. Rewrite the brief with the new exemplar and rerun the lanes that produced the near misses. Two or three rounds is the normal count.

### 8. Re-verify

The chosen name alone, same script, same day, run by the lead and not by the lane that proposed it. Registries change weekly; the row in the decision carries its date.

### 9. Record

```text
chosen:       <name>, claimed at <registries> on <date>
why it won:   <the exemplar it matched, the gate it passed>
not checked:  trademark offices, app stores, social handles, native-speaker review, <anything the brief skipped>
```

## Conditions

A name fails the hard gate on any one row:

| Gate | Fails when |
| --- | --- |
| said as spelled | the `say` column flags it: `hard x,q,z,k`; `doubled ll`; `cluster str` (three consonants together); `two readings` for ch, gh, ough, ea, a trailing e, or c and g before e, i, y; `spoken digits 1,2,3` (a digit is said, and counted one syllable) |
| short | more than 3 syllables, more than about 8 letters, or more than one token |
| free | taken on any registry the brief claims, or an exact-name repository with 20 or more stars |
| no neighbour | an AI company, product, or ML method already uses it (web search) |
| no bad meaning | a SERIOUS meaning finding in any language |
| no wrong signal | the name means something, and that something is not what the project is |
| not a typosquat | the `typosquat` column names a package on a registry the brief claims; a hit on an unclaimed registry is a MINOR note |

Meaning is either plain at a glance or absent. A name that means nothing passes; a name that means the wrong thing fails; a name whose meaning the reader must decode (a pun, a reference, a chain of hops) is rejected by default.

Soft scores, 1 to 5 each, shown in the table and never used to rescue a gate failure:

- **Exemplar closeness**, the main score: how much it sounds like the names the owner gave in step 1.
- **Elegance**: soft consonants, open vowels, reads cleanly in lowercase and in Title Case.
- **Room to grow**: not tied to one feature the project may outgrow.

Rejected by default unless the brief says otherwise: acronyms, the letters x q k z, doubled letters, consonant clusters, the suffixes -lens -scope -lux -ly -ify, version numbers, overused references (jarvis, alfred, hal).

## What the script does not check

Trademark registers, app stores, social handles other than Bluesky, and registered-but-unresolved domains. The decision record names them under "not checked" every time, so the owner knows what a later claim may still hit.

Go modules: a module path is a URL (`github.com/<owner>/<name>`), so a bare name is not claimable there, and pkg.go.dev serves its search as HTML only. The GitHub columns cover the repository the path would point at.

## Related

- `/verify-with-controls`: the control rows in step 4 are its rule 2 (a positive control before trusting a zero) and rule 6 (a checker seen failing).
- `/orchestrator-mode`: the step 3 lanes as parallel subagents, where installed.
