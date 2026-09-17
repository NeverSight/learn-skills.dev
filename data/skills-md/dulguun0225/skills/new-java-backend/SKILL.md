---
name: new-java-backend
description: Take an empty directory to the point where spec-kit's first command can run, for a Java backend on Spring Boot Web MVC, jOOQ and PostgreSQL — one pinned script that instantiates dulguun0225/java-backend-template with every build gate already wired, then specify init, then a hand-off to /speckit.constitution for the project's own articles only. Nothing here is a decision and nothing here is written by hand. ALWAYS load before creating a new Java backend repository or project directory, before writing a pom.xml or any build file for one, and before running /speckit.constitution in a project that has no backend/ yet.
---
# New Java backend — from an empty directory to spec-kit's first command

**Premise, shared with every skill in this set:** the code is written by LLM agents and no human reads it line by line. The consequence for the first session of a project is specific: **scaffolding is not a decision, so nothing an agent writes during it is wanted.** The stack is decided in `backend-stack`, the rules that bind every line are in `java-backend-rules`, and the template `dulguun0225/java-backend-template` is those rules' consequence with every build-enforceable gate wired and green. This skill is the procedure that lands it, and it ends exactly where spec-kit's own sequence begins.

## Run the script; write nothing

**Run [`scripts/new-backend.mjs`](scripts/new-backend.mjs) from this skill's own directory, with the three inputs the user supplies, and write no file yourself.** The inputs are the base package, the artifact name and the Maven group — the only three things about a scaffold that are the project's to decide, and the agent asks for them rather than inventing them, because the package rename is permanent once the tree exists.

```
node <this skill dir>/scripts/new-backend.mjs --package <pkg> --name <artifact> --group <group> --dir .
```

The default is vendored: the directory is the project root, the template lands in `backend/` by `git subtree add` at the pinned commit, its own `init.mjs` renames the package and lifts the project-level files one level up — root CI with `backend` and `frontend` jobs, the branch ruleset, `compose.yaml`, the `frontend/` stub, the pre-filled spec-kit constitution, the project `CLAUDE.md`. Then jOOQ codegen and `mvn verify` run against a real PostgreSQL, and the result is committed as `init: <artifact> from java-backend-template <sha> (mvn verify green)`. `--standalone` is for a repository that *is* the service; `--skip-verify` defers codegen and verify, and the commit message then says so. Preconditions the script checks itself: the directory is empty or absent, `git` and `mvn` are on `PATH`, and verify needs Docker.

The default an agent reaches for — a `pom.xml`, an ArchUnit ban list, a CI file and an error-response skeleton written from the directives in `java-backend-rules` — is rejected on three grounds: it costs the first session, it produces a different ban list each time, and on 2026-09-01 it pinned a superseded Java LTS and a superseded Spring Boot major while passing every gate it had just written. The template is one tree, byte-identical for a given commit, package and name.

The pinned commit is `DEFAULT_REF` inside the script, recorded with its source and date in the comment beside it. It moves deliberately, in a commit that says which gate change it brings in; `--ref` overrides it for one run.

(Check: after the run, the directory's `git log` holds the script's `init:` commit and nothing hand-written precedes it; a build file that exists before that commit is the finding — *convention*, 2026-09-16.)

## Stop where the script stops

**Do only the printed next step that has no side effect outside the directory, and hand the rest to the user by name.** The script stops, on purpose, before anything that touches the forge or the wider machine, and prints those steps: `gh repo create`, `node scripts/apply-ruleset.mjs`, `npx skills add dulguun0225/skills`, `specify init --here`. Of these, run `specify init --here` when `specify` is on `PATH` — it seeds only files that are missing, so the pre-filled constitution survives it — and skip `npx skills add` when this skill is already installed, which it is if you are reading this. Do not create the forge repository or apply the ruleset unless the user has named the organisation and asked for it in this session.

(Check: the session's tool calls contain no `gh repo create` and no `apply-ruleset` the user did not ask for by name — *convention*.)

## Hand off to /speckit.constitution, Article VII only

**The order is scaffold, `specify init --here`, `/speckit.constitution`, then `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, `/speckit.implement`; and `/speckit.constitution` amends Article VII alone.** The constitution the template lifts to `.specify/memory/constitution.md` already carries Articles I–VI — the platform, the gates as the review, explicit over silent, the committed contract, the repo shape, features as packages — each restating what `mvn verify` in `backend/` already enforces. They are not re-planned per feature; a plan's Technical Context inherits them. Article VII is empty and is the project's: domain invariants, the coverage floor and why, the money precision, the idempotency replay status, tenancy, authentication — each naming the test or gate that holds it. That is the input to `/speckit.constitution`, and this skill does not write it: the product's decisions are the user's, and `enforceable-rules` governs how each is stated. Once Article VII is in, `build-feature` runs the four feature commands unattended, one feature at a time.

The opposite order is the trap. Run `/speckit.constitution` first and it writes the file from spec-kit's generic template; the scaffold's `init.mjs` never overwrites, so the platform articles are dropped with a warning and `/speckit.plan` re-decides the stack the template has already decided. **Scaffold first, decided 2026-09-16.**

(Check: `.specify/memory/constitution.md` in the project holds the six platform articles verbatim and `init.mjs` printed no constitution warning; either failing is the finding — *convention*, 2026-09-16.)

## What this skill does not do

It does not choose the stack — `backend-stack` does, and it has. It does not state or explain a rule — `java-backend-rules`, `java-backend-api` and `java-backend-observability` do, and the template's own `docs/GATES.md` maps each wired gate to the directive it implements and names what no gate reaches. It does not verify that the template's pins were newest at its recorded date; that is the convention `java-backend-rules` names under its gate-wiring section, performed once in the template and decaying the same way. It does not run on Windows or macOS as a measured fact: the script is Node on the standard library and removes the Linux assumptions that were visible, and the claim that it runs there is the standard library's until someone runs it.

**Status: *decided, not yet validated*** as a skill — the template it lands ran green on Java 25 and Spring Boot 4.1.1 on 2026-09-16, and the procedure has been run by hand; no project has yet been created by an agent invoking this skill. **Firing:** meant to be invoked by name (`/new-java-backend`); whether the description earns the load unprompted on "create a new Java backend here" is unmeasured. Grounds and dates in [evidence.md](evidence.md).
