---
name: generate-judge-problems
description: Use when asked to generate Judge v2 problems (Exercode/Judgeの問題), or when coding is part of an Exercode course's learning objective and needs graded practice. Not for use outside Exercode/Judge.
---

# Generate judge v2 problems

Read these references before authoring any file:

- [references/problem-format.md](references/problem-format.md) — judge v2 directory layout and `problem.md` frontmatter schema.
- [references/problem-authoring.md](references/problem-authoring.md) — statement writing rules, difficulty levels, and machine-grading constraints.
- [references/example-problem.md](references/example-problem.md) — a complete minimal v2 example problem.

Generate v2 problems only: the statement file is exactly `problem.md` inside the problem directory. Never generate the legacy `<id>.problem.md` naming.

1. Confirm the inputs: learning objectives or the source material, target course, target programming language(s), number of problems, and difficulty range. Place each problem under `<courseId>/problems/<problemId>/`; never create a repository-global problem or reference another course's problem. Derive problem drafts (id, name, overview, objective, difficulty) from the inputs; when generating multiple problems, order them from easy to hard per the difficulty levels in [references/problem-authoring.md](references/problem-authoring.md).
2. Make the problem files reproducible from the repository. Preserve existing mise configuration and compatible pinned versions. If none of `mise.toml`, `.mise.toml`, or `.tool-versions` exists, create `.tool-versions`; otherwise keep the existing format. Add exact versions of every runtime, package manager, and command-line tool required to execute the tracked model answers, templates, judges, and debuggers. Declare their imported third-party libraries in each language's standard project manifest with exact direct versions when supported, and update its standard lockfile. Run `mise trust --yes` for a mise TOML config, run `mise install`, and then use the installed commands normally. Do not rely on global installations, ad hoc downloads, or temporary dependency environments, and do not add tools used only to author or validate the problem.
3. For each problem, write the primary model answer FIRST under `model_answers/<languageId>/` (e.g. `python/main.py`). Solving the problem yourself before writing the statement exposes ambiguities early. Use only concepts the learner has already studied; when no studied-concept list is given, derive reasonable assumptions from the learning objectives and state them in the final report.
4. Write `problem.md` (frontmatter + Japanese statement) per [references/problem-format.md](references/problem-format.md), following the statement rules in [references/problem-authoring.md](references/problem-authoring.md). Do NOT create `judge.ts` or `debug.ts` for a standard stdin/stdout problem — the judge server auto-generates both, and committed default-content copies are rejected by the validator. Write a custom `judge.ts` (with a matching `debug.ts`) only when the problem needs special judging (GUI, LLM, command-based, etc.); a genuinely custom `debug.ts` may also accompany a standard stdio problem on its own when the problem needs customized debugging.
5. Create test inputs under `test_cases/`: at least 1 `example_*` case (shown to learners and mirrored as 入力例/出力例 in the statement; for an input-only problem the 出力例 shows the judged output file, see [references/problem-format.md](references/problem-format.md)) and at least 1 hidden case, at least 4 in total. Make inputs diverse and include edge cases (minimum/maximum constraint values, boundary conditions such as 0 or negative numbers where allowed). All inputs must be distinct. A program that reads files instead of stdin takes them from `<id>.fin/`; a program that writes files is judged with `<id>.fout/` (see [references/problem-format.md](references/problem-format.md)).
6. Produce every `.out` file and every file under `.fout/` by RUNNING the model answer locally — never hand-write expected outputs. For a plain stdin/stdout problem:

   ```bash
   cd <problemDir> && for f in test_cases/*.in; do python3 model_answers/python/main.py < "$f" > "${f%.in}.out"; done
   ```

   When any case uses `.fin/`, `_shared.fin/` or `.fout/`, or omits `.in`, run each case in a scratch directory inside the problem directory (so the repository's pinned tools still apply), feeding `<id>.in` when it exists, capturing stdout, and replacing `<id>.fout/` with what the program wrote. Save the following as `<problemDir>/.tmp/expected.sh` (an indented heredoc would not terminate when pasted) and run `bash -euo pipefail <problemDir>/.tmp/expected.sh [<outputFile> ...]`:

   ```bash
   # The produced file paths are the arguments; stdout-only problems pass none.
   cd <problemDir>
   root=$PWD
   # A scratch directory inside the problem keeps the pinned tools; it is removed on success and kept on failure.
   mkdir -p .tmp && scratch=$(mktemp -d .tmp/expected.XXXXXX)
   trap 'st=$?; if [ $st -eq 0 ]; then rm -rf "$scratch"; else echo "kept $scratch for inspection" >&2; fi; exit $st' EXIT
   # Every test case id (the shared name of its entries), excluding the shared input directory.
   for id in $(ls -1 test_cases | sed -E -n 's/\.(in|out|fin|fout)$//p' | sort -u | grep -vx _shared); do
     # Stage the case's working directory: shared inputs first, then the case's own inputs.
     w=$scratch/$id && mkdir -p "$w"
     if [ -d test_cases/_shared.fin ]; then cp -R test_cases/_shared.fin/. "$w"/; fi
     if [ -d "test_cases/$id.fin" ]; then cp -R "test_cases/$id.fin/." "$w"/; fi
     # Run the model answer with the case's stdin (if any) and capture its stdout.
     in=/dev/null && if [ -f "test_cases/$id.in" ]; then in="$root/test_cases/$id.in"; fi
     (cd "$w" && python3 "$root/model_answers/python/main.py" < "$in" > "$root/$scratch/$id.stdout")
     if [ -d "test_cases/$id.fout" ]; then
       # A file case: the produced file paths (the script arguments) are required and every file must exist
       # before .fout/ is refilled, which protects committed contents; .out is refreshed only when the case has one.
       [ $# -gt 0 ] || { echo "usage: expected.sh <outputFile> ... (test_cases/$id.fout/ needs the produced file paths)" >&2; exit 2; }
       for f in "$@"; do test -f "$w/$f"; done
       find "test_cases/$id.fout" -mindepth 1 -delete
       for f in "$@"; do mkdir -p "test_cases/$id.fout/$(dirname "$f")" && cp "$w/$f" "test_cases/$id.fout/$f"; done
       if [ -f "test_cases/$id.out" ]; then mv "$scratch/$id.stdout" "test_cases/$id.out"; fi
     else
       # A stdout case: the captured stdout is its expectation.
       mv "$scratch/$id.stdout" "test_cases/$id.out"
     fi
   done
   ```

   Pass every relative path the program writes as the script arguments; a stdout-only problem passes none (the loop refuses to replace a `.fout/` without arguments and verifies each file exists first, and `bash -euo pipefail` stops at the first failure whatever the interactive shell is); the recipe assumes every file case writes the same paths, so adapt it per case when they differ. Create `test_cases/<id>.fout/` beforehand for every case judged by files: the loop refills existing directories, writes `.out` for every other case, and refreshes an existing `.out` of a file case (create an empty `test_cases/<id>.out` beforehand when a file case's stdout is compared as well). Adapt the commands to the model answer's language. For a custom `judge.ts`, follow its own contract instead: keep the `.in`, `.fin/` and `_shared.fin/` entries it reads, and do not create `.out` when it does not compare stdout (e.g. it compares a file listed in `requiredOutputFilePaths`) — never print a marker such as the output file name just to have stdout.

7. Cross-check with a second model answer: write an independent model answer in another target language under `model_answers/` (for a single-language problem, write the second implementation in any language under `<problemDir>/.tmp/cross_check/`, judge it with the same command, and delete it afterwards instead of committing it), then judge every model answer with the `exercode-problem` CLI from the problem directory (the CLI ships with `@exercode/problem-utils`, which must be a declared repository dependency — see [setup-exercode-course-repository](../setup-exercode-course-repository/SKILL.md)):

   ```bash
   cd <problemDir> && bunx exercode-problem judge model_answers/<languageId>
   ```

   Pass required harness parameters as the JSON second argument (e.g. `'{ "model": "<modelId>" }'` for an LLM judge). The run passes only when the command exits 0, prints at least one `TEST_CASE_RESULT` line, and every printed line has the accepted decision code `2000` (the comparison rule is described in [references/problem-format.md](references/problem-format.md)). On any failure, diagnose the decision code and stderr and fix that cause — an output mismatch means the statement is ambiguous or an answer is wrong; regenerate the `.out` files only when the expected outputs change.

8. If you provide starter code under `templates/`, ensure it does NOT solve the problem: judge each template directory from the problem directory with `bunx exercode-problem judge templates/<languageId>` (judge `templates/_default` as `bunx exercode-problem judge templates/_default`, and files placed directly under `templates/` as `bunx exercode-problem judge templates`; in both cases pass the target language as `'{ "language": "<languageId>" }'`), confirm at least one test case is not accepted by an actually executed run — a `main file not found` result (decision code `1201`) means the language param matched no file in the template directory, so rerun with the language of the files it contains — and confirm no template directory contains, unchanged, every file a model answer is judged by (its source files for a standard problem, every file for a custom judge; shared helper modules may be identical).
9. If the statement constrains syntax (see the 制約 rules in [references/problem-authoring.md](references/problem-authoring.md)), mirror the constraints in frontmatter `requiredRegExpsInCode` / `forbiddenRegExpsInCode` / `forbiddenTextsInCode`. Required patterns must match every model answer; forbidden patterns must match none, and must never match input-parsing helpers (`Scanner`, `map`, `int`, `split`, regexes). The patterns apply to submissions in every target language, so only use language-agnostic patterns; keep language-specific constraints (e.g. Python's `range`) in the statement prose instead.
10. Validate and fix until clean:

    ```bash
    bunx exercode-problem validate-problem <problemDir>...
    ```

    Fix every reported error and rerun. Repeat until the command reports success. Address warnings too unless they are intentional; if you keep a warning, tell the user why in the final report.

11. Report the created problem directories with their difficulties, and any open decisions (e.g. constraint values you chose, intentionally kept warnings).
