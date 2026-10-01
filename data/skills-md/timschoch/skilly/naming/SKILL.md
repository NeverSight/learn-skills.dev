---
name: naming
description: The code-naming rules. Use before naming a variable, function, file, type, table, route, component, event, or env var, and when a request's word differs from the repo's.
---

# Naming

One list, synced from the hub. The gate `naming` checks what a machine can check, on push and in CI; the rest is your judgement. [references/lint.md](references/lint.md) draws the line.

Before you name anything, run `node .agents/skills/naming/scripts/config.mjs` and read its output as the current rules: it prints [references/naming.json](references/naming.json) merged with the project's overrides.

## Rules

1. One word per thing, and the word comes from `GLOSSARY.md`. Look there first, then in existing types, DB tables and API routes. The repo's word beats the request's word.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `testimonial` | `customerQuote` | the request said "customer quotes", the repo says `testimonial` |
   | `Testimonial` type, `testimonials` table, `/api/testimonials` | `Testimonial` type, `reviews` table | one word per thing, everywhere |
   | `order` | `purchase` beside `order` | two words for one thing splits the search |

2. No word yet? Run [term-check](.agents/skills/term-check/SKILL.md), show the result to the user, get sign-off, then add the word to `GLOSSARY.md` through [domain-modeling](.agents/skills/domain-modeling/SKILL.md), which owns that file.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `carryOver`, term-checked, in `GLOSSARY.md` | `carryOver`, invented in the PR | a new word needs the user's sign-off |
   | `caseStudy` recorded with plural `caseStudies` | `caseStudy` with no entry | the next agent picks a different word |
   | `grid` added to the role list | `Grid` used, list unchanged | a role outside the closed list is a new word |

3. Name by role, not by type. No `I` or `T` prefix, no Hungarian, no noise word (see `noiseWords` in naming.json).

   | Good | Bad | Why |
   | --- | --- | --- |
   | `User` | `IUser` | no `I` prefix |
   | `count` | `nCount` | no Hungarian |
   | `accounts` | `accountList`, `accountData` | no noise word, the plural already says many |

4. Full words only, no single-letter name, no magic number. The banned short words are `shortWords` in naming.json.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `options` | `opts` | full word |
   | `error` | `e`, `err` | no single letter, no abbreviation |
   | `const MAX_RETRIES = 3` | a bare `3` | a number needs a name |

5. Say nothing the call site already says.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `user.name` | `user.userName` | the object says `user` |
   | `testimonials.add(item)` | `testimonials.addTestimonial(item)` | the collection says `testimonial` |
   | field `name` in table `testimonials` | field `testimonial_name` | the table says `testimonial` |

6. An action starts with a verb from `prefixes` in naming.json, one verb per meaning. A pure derived value may be a noun.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `fetchTestimonials` | `loadTestimonials` beside it | one verb per meaning, `fetch` is over the network |
   | `listUsers` | `getAllUsers` | `list` means many |
   | `branchSha` | `getBranchSha` | a pure derived value may be a noun |

   A prefix promises its meaning: `get` only reads, `set` returns nothing, `is` returns a boolean, `find` may return nothing while `get` may not. A name with `and` in it (`saveAndNotify`) is two functions.

7. Stored boolean state is a bare adjective; a check is `is`, `has`, `can` or `should`; never `notX`.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `archived` | `isArchived` | stored state is a bare adjective |
   | `isEmpty`, `canRetry` | `empty()`, `retryAllowed` | a check carries the prefix |
   | `enabled` | `notDisabled` | positive names only |

8. Entity singular, collection plural. Record an irregular plural in `GLOSSARY.md` next to the word.

   | Good | Bad | Why |
   | --- | --- | --- |
   | type `Testimonial`, file `testimonial.ts` | type `Testimonials` | one entity is singular |
   | table, path, folder `testimonials` | table `testimonial` | a collection is plural |
   | `case_studies`, plural recorded in `GLOSSARY.md` | `case_studys` | an irregular plural is written down once |

9. No `enum`. Use a string-literal union or an `as const` object. The discriminant key is `discriminant` in naming.json (`kind`). Own values are kebab-case; values mirrored from an external API stay verbatim.

   | Good | Bad | Why |
   | --- | --- | --- |
   | `type Status = 'open' \| 'in-progress'` | `enum Status { Open }` | no `enum` |
   | `{ kind: 'pull-request' }` | `{ type: 'pull-request' }` | the discriminant key is `kind` |
   | `'MERGED'` from the GitHub API | `'merged'` | a mirrored value stays verbatim |

10. Build every name from `parts` in naming.json, big to small: `project · area · entity · role · action · attribute · consumer`. Take the parts you need, keep their order. Each `artifacts` entry lists parts, case and examples. `role` is a closed list per repo (`artifacts.component.roles`, `artifacts.env.roles`). Env vars follow `artifacts.env.shape`. Payload CMS: collection slug = API path = table; the slug is kebab-case and plural (`case-studies`), the table replaces the hyphen with an underscore (`case_studies`).

    | Good | Bad | Why |
    | --- | --- | --- |
    | `COLIN_SYNC_KEY_FOR_TWENTY` | `TWENTY_API_KEY` | issuer first, then what the key is for, then who holds it |
    | `TestimonialGrid` | `GridTestimonial` | entity first, then role |
    | `testimonial.added` | `addTestimonial` | an event is a fact in the past, not a command |

11. Casing follows the language guide and the repo's linter. Files and folders are lowercase kebab-case. An existing repo convention wins over this line: set it in `artifacts.file.case` and `artifacts.folder.case`, one case or a list (`["kebab", "PascalCase", "camelCase"]` for React components and hooks).

    | Good | Bad | Why |
    | --- | --- | --- |
    | `render-pr-body.mjs` | `renderPrBody.mjs` | files are kebab-case |
    | `src/components/case-studies/` | `src/components/case_studies/` | folders are kebab-case |
    | `loadUser` in a repo that uses `load` everywhere | `fetchUser` beside it | the existing convention wins |

12. Meaning changed? Rename everywhere in the same change, rule 204 in [writing-rules](.agents/skills/writing-rules/rules/all.md).

    | Good | Bad | Why |
    | --- | --- | --- |
    | `draft` renamed to `proposal` in code, docs and DB in one PR | code renamed, docs still say `draft` | two words for one thing |
    | `retryCount` after the value stopped being a limit | `maxRetries` kept | the name lies |
    | rename plus a `GLOSSARY.md` update | rename only | the glossary is the source |

## Per-project overrides

Override file: `.skilly/naming.json`, same shape as [references/naming.json](references/naming.json), only the keys you change. An old `docs/agents/naming.json` is read only while `.skilly/naming.json` is missing: move it to `.skilly/naming.json`.

Merge order:

1. [references/naming.json](references/naming.json)
2. `references/stacks/<bundle>.json`, for each bundle listed in `.skilly/config.json` `bundles`, in that order. Missing file: skipped. Bundles reached only through `includes` do not count.
3. `.skilly/naming.json`

Merge rules:

- Objects merge by key. `null` drops a key.
- Arrays append and dedupe. `"-Data"` drops the default `Data`.
- Scalars override.

```json
{
  "prefixes": { "sync": { "meaning": "mirror to a remote system", "not": ["push", "mirror"] } },
  "noiseWords": ["-Data"],
  "allow": {
    "ctxTools": { "names": ["^ctx_"], "rules": ["short-word"], "why": "lean-ctx tool names." },
    "payload/migrations": null
  }
}
```

`allow` holds named entries. Shape and what they silence: [references/lint.md](references/lint.md#exceptions).

## References

- [references/naming.json](references/naming.json): prefixes, parts, artifacts, short words, noise words, synonyms, discriminant, allow
- [references/stacks/](references/stacks/): per-bundle defaults, same shape
- [references/lint.md](references/lint.md): what the gate checks, what you judge, per-repo exceptions
- [references/biome.json](references/biome.json): opt-in Biome block for consumers
- [scripts/config.mjs](scripts/config.mjs): prints the merged config
- [scripts/check.mjs](scripts/check.mjs): runs the gate on the files the branch changes
