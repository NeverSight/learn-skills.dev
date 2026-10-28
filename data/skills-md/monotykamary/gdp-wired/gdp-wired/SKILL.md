---
name: gdp-wired
description: Prove the laws of stateful rules in TypeScript with gdp-wired, an automatic prover (no proof to write, every proof checkable again in Lean). Use when adding, changing or reviewing a budget, cap, quota, rate limit, sliding window, workflow, ledger, access policy or any state machine whose invariants matter; when code imports from 'gdp-wired'; when a gdp-ts trusted module's check (an authorization or entitlement policy) should be proven, not just trusted; when a law comes back refuted or unproven; or when deciding whether a claim belongs to gdp-wired, Lean or Bend.
---

# gdp-wired

A rule is a state machine: params, a request's inputs, state, and one step.
A law is a claim about every run of it. `proveRule(rule, [law])` either
proves the law (a kernel checks the proof tree; nothing to write) or says
where it fails, and a search turns a false law into a real run.

```ts
import {min, nat, proveRule, rule, when} from 'gdp-wired'
import {search} from 'gdp-wired/machine'

const budget = rule('budget')
  .params({b: nat, m: nat})
  .inputs({c: nat})
  .state({s: 0})
  .step(({b, m, c, s}) => ({s: when(s.lt(b), s.plus(min(c, m)), s)}))
const bounded = budget.law('spend stays within b + m', ({s, b, m}) => s.atMost(b.plus(m)))

proveRule(budget, [bounded]) // {proven: true, checked: true}

const uncapped = budget.step(({b, c, s}) => ({s: when(s.lt(b), s.plus(c), s)}))
proveRule(uncapped, [bounded]) // {proven: false, goal: 'spend stays within b + m @step', stuck: 'sat', witness: {...}}
search(uncapped.machine, bounded) // {params: {b: 1, m: 0}, trace: [{c: 2}]}
```

It decides laws about stateful rules over naturals, records, variants, maps,
sets and logs, and proves the lemmas you state about a recurrence by
induction. Recursion it would have to invent a lemma for belongs to Lean or
Bend ([where it fits](references/where-it-fits.md)).

## Workflow

When adding or changing a rule whose invariants matter:

1. **Write the rule as the code does it.** One `rule(...)` with the same
   params, inputs, state and step as the production code. Use kinds for what
   isn't a natural (`bool`, `oneOf`, `maybe`, `int`, `decimal`, `str`), records
   and variants for objects and tagged unions (`record`, `variant`), maps for
   per-key state, `.log` for histories, `chart` for a workflow with many states ([writing rules](references/writing-rules.md)).
2. **State the laws a reviewer would ask about.** Invariants with `law`
   ("no day passes its cap"), one-step facts with `stepLaw` ("a balance only
   goes down"), k steps with `stepsLaw`, "eventually" with `leadsTo`,
   request-only facts with `decide`. One claim per law, named as a sentence.
3. **Prove.** `proveRule`, `proveSteps`, `proveLeadsTo`, `proveDecision`,
   `proveLoop`. Require `proven && checked`; `checked` is the kernel's verdict
   on the tree the untrusted prover grew.
4. **When it fails, read the verdict before changing anything**
   ([reading verdicts](references/reading-verdicts.md)). `stuck: 'sat'` at
   `@step` means the law isn't inductive: run `search` from the start. A real
   run is a bug in the rule (or the law); no run means the law needs a
   helper invariant, so add the missing law next to it, never weaken the one
   that matters. `proveRule` and `proveSteps` look for it themselves (10 s by
   default; `{search: {ms}}`, or `{search: false}` for the prover alone):
   lemmas first (`discover`), then invariants (`inferLaws`), and the verdict's
   `found` holds what proved the laws, as laws to pass with them and as
   lemmas to state, each with the source to paste. An invariant found holds
   only in states reachable from the start, and the verdict says so
   (`assumes`). If the code steps the rule from states it is handed (a
   host's, a stored one), prove with `{from: 'any'}` and require
   `proven && checked && !assumes`.
5. **Never prove a different rule than the one that ships.** Ship the rule
   itself (`rule.compiled()`), or hold hand-written code to it with
   `rule.compare(reference)`; run `rule.crossCheck(laws)` in tests
   ([shipping](references/shipping.md)). With gdp-ts, mint its proofs from
   the proven check (`guard`, `gate` from `gdp-wired/gdp`) so every call site
   is held to it ([with gdp-ts](references/gdp-ts.md)).
6. **Keep the broken variant.** Next to each proven rule, keep the bug it
   rules out (the uncapped budget) and assert it is refused. It is the
   cheapest regression test you will write.
7. **State the lemma, find it, or hand off.** A recurrence on one natural (a
   backoff delay, a fee schedule): define it with `recur` and state the lemmas
   the rule needs; they are proven by induction and become its facts. When the
   law isn't proven and you don't know the lemma, `discover(rule, laws,
   stepLaws)` (`gdp-wired/discover`) looks for it, for a recurrence and for a
   carried list's folds (`discoverFold(fold, laws)` for a tree): paste what
   `found` gives into `recur`, `carriesList` or `.children`. Other
   recursive structure, or products of unknowns past what products of facts
   and squares refute: prove the function in Lean,
   give the rule the function with its facts, export with `toLean`
   ([Lean handoff](references/lean-handoff.md)). Don't approximate a
   recursive claim with a bounded one and call it proven.

## References

Read the one you need:

| File | Read it when |
|---|---|
| [`references/writing-rules.md`](references/writing-rules.md) | Writing a rule or a law: kinds, records and variants, maps, flags, step laws, k-step laws, histories, liveness, decisions, pure functions, two-run laws, loops. |
| [`references/reading-verdicts.md`](references/reading-verdicts.md) | A verdict is not `{proven: true, checked: true}`: `stuck: 'sat'`, `stuck: 'unknown'` with `why`, a witness, a search result. |
| [`references/shipping.md`](references/shipping.md) | Running the proven rule in an app, encoding runtime values, holding existing code to the rule. |
| [`references/gdp-ts.md`](references/gdp-ts.md) | The codebase uses gdp-ts (`@gdp-ts/core`, a `proofs/` folder), or an authorization check should be proven and demanded at every call site: `guard` and `gate`. |
| [`references/lean-handoff.md`](references/lean-handoff.md) | Exporting proofs to Lean, stating a lemma about a recurrence (`recur`), or a claim needs recursion or arithmetic the kernel doesn't decide. |
| [`references/where-it-fits.md`](references/where-it-fits.md) | Deciding whether gdp-wired, Lean or Bend should own a claim. |

## API

From `gdp-wired`:

| Export | What it is |
|---|---|
| `rule(name)` | A rule builder: `.params` `.inputs` `.state` `.maps` (of naturals, or of a kind: `kind.from(v)`) `.lists` `.items` (lists of a kind) `.carries` `.flags` `.step` `.pre` `.assume` `.fns` `.facts` `.log` `.sums` `.queries` `.keep` `.relations` `.prune`. |
| `nat`, `upTo(k)`, `bool`, `oneOf(...)`, `maybe(kind)`, `int`, `decimal(places)`, `str({like, maxLength})`, `record({...})`, `variant({...})` | Kinds; state of any kind with `kind.from(init)`; a variant's case built with `V.make({tag, ...fields})`, read with `is` and `match`; `same(a, b)` compares two values part by part. |
| `r.law`, `r.stepLaw`, `r.stepsLaw`, `r.leadsTo`, `r.decide`, `r.relate` | Claims: invariant, one step, k steps (k ≤ 64), liveness, a decision about one request, a decision about two. |
| `ratRule(name)`, `rat`, `nonneg`, `proveRatRule(rule, laws)` (`gdp-wired/rationals`) | A rule over the rationals: exact values (decimals, fractions), linear terms (`plus` `minus` `times(k)` `over(k)`, `rmin` `rmax` `rwhen`); `{proven, checked, goal?, stuck?, witness?, run?}`, refuted by an exact run from the start or proven by trees of Farkas certificates; `rule.run(params, requests)` computes exactly; `rationalsToLean` (`gdp-wired/lean`) checks the proofs in Lean. |
| `proveNeverEnds(loop, {from?, ms?})` | Some run of the loop never ends (the claim a halting proof refutes): `{proven, checked, recur, loop, by, run}`, the certificate a closed recurrent set with the turn from each state given; toLean's `{id, neverEnds: v.loop, recur: v.recur}` proves `NeverEnds` in Lean. |
| `proveRule`, `proveSteps`, `proveLeadsTo`, `proveDecision`, `proveLoop` | Verdicts: `{proven, checked, goal?, stuck?, witness?, why?, found?}`. `proveRule` and `proveSteps` take `{search}`: where the prover alone doesn't prove the laws and no run breaks them, they look for lemmas and invariants (10 s by default; `false` for the prover alone), and `found` says what proved them. `assumes` says the proof holds only in states reachable from the start; `{from: 'any'}` proves step laws from every state the laws allow. |
| `when`, `min`, `max`, `count`, `sum`, `all`, `any`, `not`, `forall`, `everyKey`, `someKey`, `relation` | Terms and conditions; terms have `plus` `minus` (truncated) `times(k)` `mul` `lt` `atMost` `atLeast` `gt` `eq`, conditions `and` `or` `not` `implies`. |
| `chart(name)` | A statechart: `.states({...})` (nested: `{states: {...}, initial, history, final}`) or `.regions({...})` (parallel), `.params`, `.inputs` (the payload), `.context` (extended state), `.outputs` (decided each step, reset to a default), `.events` (their order), `.on(event, {from, to, when, set, fresh})` (no `to`: internal; `fresh`: ignore history); `.check()` (every state reached with its run or proven unreachable, none stuck, no event ambiguous), `.law`, `.stepLaw` (`env.in('active.paid')`, `env.last('active')`), `.prove`, `.rule`. |
| `inferLaws(rule, laws, stepLaws?)` | `gdp-wired/infer`: the invariants a law that isn't inductive needs, found from runs and the kernel's counterexamples (bounds, sums, differences, guarded by a flag or a choice, laws about every key of a map); `found[i].source` is the `r.law(...)` call; proven and checked like `proveRule`. |
| `fromXState(machine, {guards, actions})` | `gdp-wired/xstate`: an XState v5 machine as a chart, each named guard and action given again; `conforms(chart, machine, createActor)` runs both on the same random events and names the first run where they part; what a chart can't run the same way is refused with the reason. |
| `fun(name)`, `loop(name)` | Pure functions (`.returns`, `.law`, `.relate`, `.run`) and loops (`.while`, `.body`, `.rank`; with no `.rank`, `proveLoop` finds one from the loop's runs, with the invariants it needs, in `found`). |
| `findCycles(facts, claims)`, `findRank(loop, laws)`, `cycleLemmas(machine, laws)` | `gdp-wired/cycles`: cyclic proofs nobody shaped, for claims about functions defined by their equations: ranks (linear, in order) from the runs, back-edges at the calls a goal reads, companions (constants abstracted, bounds on what a goal reads); checked by `kernel/cyclic.ts`. `proveRule`'s search tries `cycleLemmas` for functions known by their facts (`{search: {cycles: false}}` leaves it out). |
| `fn(arity, js, {facts, lean})`, `divBy(c)`, `modBy(c)` | Functions known by their facts. |
| `recur(name, {args, fns, zero, next}, lemmas, between)` | A function defined by a recurrence on its first argument (up to four further arguments fixed, other functions read), its lemmas and laws between two points proven by induction when made (`Unproven` otherwise); its equations, lemmas and laws are its facts, checked again by Lean as the kernel's own proof. |
| `discover(rule, laws, stepLaws)`, `discoverFold(fold, laws)` | `gdp-wired/discover`: lemmas nobody stated, for a recurrence's function, a carried list's folds or a tree fold, found from their values (bounds, linear relations, closed forms of degree 2 at most, laws between two points), proven by the same induction, only those the laws need kept; `verdict` is of `rule` (the rule made again with them), `found` is source to paste. |
| `r.carriesSeq(...names)`, `r.carriesSeqs(...names)`, `everyBelow(n, f)` | Sequences a request carries as positions and a length (`A.prefixOf(B)`, `startsWith`, `equals`, `extends(B, k)`, `has`, `at`, `len`), tables of them (`T.row(r)`, `T.rows`); laws about prefixes of paths need no lemma; rows compared at a witness. |
| `r.carriesList(name, kind, folds, lemmas)` | A list of values a request carries (an invoice's lines): `L.every`, `L.at(i)`, `L.fold.<f>`; folds and lemmas may read the params; fold lemmas proven by induction (they read the folds, not the items); decisions assume the folds too. |
| `fold(name)`, `proveFold`, `f.run(tree)` | A fold over a tree given as a value: `.leaf`, `.node`, `.law` (`.children` for any number of children per node); laws proven by induction over the tree. |
| `r.nodes(name, kind, children, folds)` | A tree (or lists of lists) in the state: a table of nodes that only grows, `T.make(value, kids, when)`, `T.node(n).fold`; a law about a subtree is a law about one node. |
| `optional(c, value)`, `variant(cases, {tag})`, `r.kindLaws()` | A value present where c holds; a variant whose runtime case key isn't `tag`; what the kinds of the state and cells keep true (proven by `proveSteps` on its own). |
| `r.compiled()`, `r.interpreter()`, `r.encodeParams`, `r.encodeInput`, `r.foldsOf`, `r.decode`, `r.crossCheck`, `r.compare` | Running and checking the rule. |

Also: `gdp-wired/gdp` (`guard`, `gate`, `Unproven`: gdp-ts proofs minted by proven checks),
`gdp-wired/machine` (`search`, `compileJs`, the interpreter), `gdp-wired/lean`
(`toLean`, `leanProject`), `gdp-wired/compose` (`product`, `interleave`,
`refinement`, `steps`, `ghost`), `gdp-wired/kernel`, `gdp-wired/prove`.
