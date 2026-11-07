---
name: git-for-research-code
description: When the user wants to version-control optimization research code - small commits per experiment change, tags for paper result snapshots, .gitignore for solver logs, linking result tables to commit hashes, and branch strategy for risky refactors. Also use when the user mentions "git workflow," "version control research," "tag results," "reproducible experiments git," "gitignore solver," or when a paper number must trace to an exact code state. For repository layout, see optimization-project-structure; for tidy result tables, see pandas-experiment-management.
---

# Git for Research Code

You are an expert in version control for computational optimization research. This skill covers the solo-researcher git workflow: commit granularity tied to experiments, annotated tags that freeze the code state behind every paper table, ignore rules for solver logs and result artifacts, provenance stamping that links each result row to a commit hash, and branch strategies that make risky refactors safe. Use the pattern catalog below to make every reported number reproducible from a single hash.

## Initial Assessment

Establish the following before recommending a workflow or writing tooling:

- **Repository status.** Does a repo exist already? If yes, run `git status` and `git count-objects -vH` mentally through the user: is the worktree clean, and has the repo already been polluted with large result files or solver logs?
- **Team size.** Solo PhD-style work, a 2-3 person lab project, or a larger team? Solo work permits rebase-based history cleanup and direct commits to `main`; shared remotes require merge discipline and protected branches.
- **Artifact inventory.** What does a run produce? Typical optimization artifacts: result CSV/parquet tables, solver logs (`.log`), model files (`.lp`, `.mps`), solution files (`.sol`), checkpoints, convergence traces, figures. Each class needs an explicit track/ignore decision.
- **Instance data.** Are benchmark instances small text files (TSPLIB-style, fine to commit), large binaries (need LFS or an external store plus checksums), or licensed data that must never enter a public repo?
- **Experiment cadence.** How often does the user change code and re-run? Daily parameter sweeps need a low-friction stamp-and-run loop; monthly campaign-style runs justify heavier manifests.
- **Paper pipeline.** Which deliverables consume results - LaTeX tables, figures, a results section? Every camera-ready number should trace back to a tag.
- **Reproducibility horizon.** Will results need re-running at revision time (6-12 months later)? If yes, environment capture (Python and package versions) must ride along with the git hash.
- **Solver licensing.** Gurobi license files (`gurobi.lic`), WLS credentials, and cluster SSH keys must be ignored and scanned for before any push to a public remote.
- **Remote and backup.** Is there a remote (GitHub/GitLab/institute server)? A repo with no remote is one disk failure away from losing the entire provenance chain.
- **Existing damage.** If history already contains multi-GB results or secrets, plan a history rewrite (`git filter-repo`) before adopting the clean workflow, not after.
- **Tooling constraints.** Python version, OS (path separators in hooks), whether the user can install the `pre-commit` framework or needs plain `.git/hooks` scripts.

## Workflow Anatomy

### The provenance chain

A reported result is reproducible only if it is a pure function of versioned inputs:

$$
\text{result} = \mathrm{Run}(\text{code}@\text{commit},\ \text{config},\ \text{instance},\ \text{seed},\ \text{environment})
$$

Git pins the first argument. The workflow below makes the remaining four ride along with it: configs and instance generators are committed code, seeds and config values are recorded in the result row, and the environment is captured in a per-run manifest. If any argument is missing from the record, the result is an anecdote, not evidence (Sandve et al. (2013), *Ten Simple Rules for Reproducible Computational Research*).

The chain has four links, each implemented by a pattern in this skill:

```text
commit hash --> run manifest --> result row --> aggregated table --> paper table/figure
   (git)        (JSON sidecar)   (stamped CSV)   (groupby + pivot)     (annotated tag)
```

### What goes in git - artifact taxonomy

| Artifact class | Track in git? | Reason |
|---|---|---|
| Source code (`src/`), scripts | Yes | The whole point |
| Config files (JSON/YAML) | Yes | Part of the run definition |
| Instance generators + seeds | Yes | Regenerate instead of storing |
| Small text instances (< ~1 MB) | Yes | Benchmarks are inputs, not outputs |
| Large/binary instances | LFS or external + checksum file | Bloat; clone time explodes |
| Result tables (CSV/parquet) | No (ignore) | Derived; regenerate from commit |
| Solver logs, `.lp`/`.mps`/`.sol` dumps | No (ignore) | Large, noisy, derived |
| Figures, compiled PDFs | No (ignore) | Derived from tables |
| Run manifests (small JSON) | Optional | Tiny; committing them is acceptable |
| License files, credentials | Never | Security; use global ignore too |
| LaTeX paper sources | Yes (same or separate repo) | Tags can bind paper to code |

### Commit granularity - one logical change per commit

The unit of commit is **one experiment-relevant change**: one operator added, one bug fixed, one parameter default changed, one config introduced. The test: can you write the subject line without the word "and"? Small commits are what make `git bisect` (find the commit that changed a number), `git revert` (undo one change), and result-to-commit linking work at all. A 40-file "weekly progress" commit destroys all three.

```text
Commit message convention (subject <= 72 chars, imperative):

  <area>: <what changed>

  <why - the experiment motivation, 1-3 lines>
  <observed effect on results, if known>

Examples:
  ils: add double-bridge kick with strength parameter
  config: raise tabu tenure 8 -> 12 for n>=100 instances
  fix: delta evaluation missed diagonal term (objectives change!)
```

Flag behavior-changing fixes loudly ("objectives change!") - they invalidate all earlier result rows, and the audit pattern below will show old hashes that must not be mixed with new ones in one table.

### Branch vs tag decision

| Situation | Mechanism | Why |
|---|---|---|
| Day-to-day experiment iteration (solo) | Commit to `main` | Branch overhead buys nothing |
| Risky refactor (rewrite evaluation, swap data structures) | Branch `refactor/<topic>` | Abandonable; regression-gate before merge |
| New algorithm variant you may discard | Branch `try/<idea>` | Keep `main` as the working baseline |
| Code state behind a submitted table/figure | Annotated tag `paper-<venue>-<rev>-<artifact>` | Immutable, findable, archivable |
| Revision round for a journal | Tag per round (`paper-ejor-r1`) | Reviewers ask "what changed since R0?" |
| Long-running experiment while you keep coding | `git worktree` at the launch commit | Code edits cannot corrupt the running job |

Use **annotated** tags (`git tag -a`), never lightweight ones: annotated tags store author, date, and a message describing exactly which tables the snapshot backs, and `git describe` prefers them.

## Provenance Patterns - Linking Results to Code State

Each pattern below is self-contained: motivation, implementation, pitfall. Together they implement the provenance chain end to end.

### Pattern 1: Capture the git state at experiment launch

Every experiment script should know which commit it runs from, before it computes anything. Capturing this in-process (rather than by hand) removes the human step that always gets skipped at 2 a.m. before a deadline.

```python
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class GitState:
    """Snapshot of repository state at experiment launch."""
    commit: str     # full 40-char SHA of HEAD
    branch: str     # current branch name, or "DETACHED"
    dirty: bool     # True if tracked files have uncommitted changes
    untracked: int  # count of untracked, non-ignored files


def _git(args: list[str], repo: str = ".") -> str:
    """Run a git command in `repo` and return stripped stdout."""
    out = subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def git_state(repo: str = ".") -> GitState:
    """Capture commit, branch, dirty flag, and untracked count of `repo`."""
    commit = _git(["rev-parse", "HEAD"], repo)
    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"], repo)
    status_lines = _git(["status", "--porcelain"], repo).splitlines()
    untracked = sum(1 for line in status_lines if line.startswith("??"))
    dirty = any(not line.startswith("??") for line in status_lines)
    return GitState(
        commit=commit,
        branch="DETACHED" if branch == "HEAD" else branch,
        dirty=dirty,
        untracked=untracked,
    )


if __name__ == "__main__":
    state = git_state(".")
    print(state.commit[:12], state.branch, "dirty" if state.dirty else "clean")
    # Expected: e.g. "3f2a91c0d4e7 main clean" - short hash, branch, clean flag.
```

**Pitfall:** `git rev-parse HEAD` succeeds even when the worktree is filthy, so the hash alone proves nothing. The `dirty` flag is the load: a result produced with `dirty=True` corresponds to *no commit at all*, because the uncommitted edits are unrecoverable. Also note `subprocess` with `check=True` raises `CalledProcessError` outside a git repo - that is the correct behavior (fail fast), do not swallow it.

### Pattern 2: Refuse to launch from a dirty worktree

The cheapest reproducibility guarantee: experiments simply do not start unless the code state is committed. One guard call at the top of every runner script enforces the discipline mechanically.

```python
import subprocess


class DirtyWorktreeError(RuntimeError):
    """Raised when an experiment starts from uncommitted code."""


def _porcelain(repo: str) -> list[str]:
    """Return `git status --porcelain` lines (tracked changes + untracked)."""
    out = subprocess.run(
        ["git", "-C", repo, "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip().splitlines() if out.stdout.strip() else []


def require_clean_worktree(repo: str = ".", allow_untracked: bool = True) -> str:
    """Return HEAD's hash, or raise if tracked files have uncommitted changes.

    Call first in every experiment runner. A result produced from a dirty
    worktree cannot be reproduced from any commit.
    """
    lines = _porcelain(repo)
    blocking = [ln for ln in lines
                if not (allow_untracked and ln.startswith("??"))]
    if blocking:
        details = "\n".join(blocking[:10])
        raise DirtyWorktreeError(
            f"{len(blocking)} uncommitted change(s) in {repo}:\n{details}\n"
            "Commit (or stash) before launching the experiment."
        )
    out = subprocess.run(
        ["git", "-C", repo, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


if __name__ == "__main__":
    commit = require_clean_worktree(".")
    print(f"launching experiment from {commit[:12]}")
    # Expected: prints the short hash on a clean repo; on a dirty repo raises
    # DirtyWorktreeError listing the modified files.
```

**Pitfall:** an escape hatch like `--allow-dirty` gets used once "just to check something quickly," and that one run becomes Table 2. If you must allow exploratory dirty runs, route them to a separate results file (`results/scratch_runs.csv`) that the paper pipeline never reads. The `allow_untracked=True` default is deliberate: untracked files are usually new result outputs, not code; tighten it to `False` when a new source file might silently change behavior (e.g., plugin/factory registration that globs a directory).

### Pattern 3: Stamp every result row with commit hash and seed

Result tables outlive memory. A tidy table where every row carries `commit`, `dirty`, `seed`, and parameters answers "which code produced this number?" forever - and lets you filter out rows from superseded code with one boolean mask. Atomic writes (temp file + `os.replace`) prevent a crashed run from truncating months of accumulated results.

```python
import os
import subprocess
import tempfile
from datetime import datetime, timezone

import pandas as pd


def head_commit(repo: str = ".") -> tuple[str, bool]:
    """Return (HEAD hash, dirty flag) for `repo`."""
    rev = subprocess.run(
        ["git", "-C", repo, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "-C", repo, "status", "--porcelain"],
        capture_output=True, text=True, check=True,
    ).stdout
    dirty = any(not ln.startswith("??") for ln in status.splitlines())
    return rev, dirty


def stamped_row(instance: str, algorithm: str, seed: int, objective: float,
                runtime_s: float, repo: str = ".") -> dict:
    """Build one tidy result row carrying full code provenance."""
    commit, dirty = head_commit(repo)
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "instance": instance,
        "algorithm": algorithm,
        "seed": seed,
        "objective": objective,
        "runtime_s": round(runtime_s, 3),
        "commit": commit,
        "dirty": dirty,
    }


def append_rows_atomic(rows: list[dict], csv_path: str) -> None:
    """Append rows to a CSV using write-to-temp + os.replace (crash-safe)."""
    new = pd.DataFrame(rows)
    combined = (pd.concat([pd.read_csv(csv_path), new], ignore_index=True)
                if os.path.exists(csv_path) else new)
    directory = os.path.dirname(os.path.abspath(csv_path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=directory, suffix=".csv.tmp")
    os.close(fd)
    combined.to_csv(tmp, index=False)
    os.replace(tmp, csv_path)


if __name__ == "__main__":
    rows = [stamped_row("rand_n50_s0", "tabu", seed=s,
                        objective=1234.5 - s, runtime_s=2.0)
            for s in range(3)]
    append_rows_atomic(rows, "results/raw_runs.csv")
    table = pd.read_csv("results/raw_runs.csv")
    print(table[["seed", "objective", "dirty"]].to_string(index=False))
    # Expected: 3 rows, all sharing one 40-char commit hash and dirty=False.
```

**Pitfall:** stamping the *aggregated* table instead of the raw runs. Aggregations (means over seeds, best-of-10) often mix rows from several commits without anyone noticing; only per-run stamping makes the mixing detectable. Keep one row per run in the raw file and rebuild aggregates from it (see **pandas-experiment-management** for the tidy-table discipline). Also: read-concat-rewrite is O(file size) per append - fine up to ~10^5 rows; beyond that, write per-run files and concatenate at analysis time.

### Pattern 4: Audit a result table's provenance before using it

Before a table feeds a paper, verify two invariants: every referenced commit still exists in the repo (it can vanish after a rebase or an aggressive `gc` of unreachable objects), and no dirty rows are present.

```python
import subprocess

import pandas as pd


def commit_exists(commit: str, repo: str = ".") -> bool:
    """True if `commit` resolves to a commit object in `repo`."""
    res = subprocess.run(
        ["git", "-C", repo, "cat-file", "-e", f"{commit}^{{commit}}"],
        capture_output=True, text=True,
    )
    return res.returncode == 0


def audit_provenance(csv_path: str, repo: str = ".") -> pd.DataFrame:
    """Per-commit report over a stamped result table: rows, dirty rows, existence."""
    df = pd.read_csv(csv_path)
    report = (
        df.groupby("commit")
          .agg(rows=("commit", "size"), dirty_rows=("dirty", "sum"))
          .reset_index()
    )
    report["in_repo"] = report["commit"].map(lambda c: commit_exists(str(c), repo))
    return report.sort_values("rows", ascending=False, ignore_index=True)


if __name__ == "__main__":
    report = audit_provenance("results/raw_runs.csv")
    print(report.to_string(index=False))
    bad = report[(~report["in_repo"]) | (report["dirty_rows"] > 0)]
    print("provenance problems:", len(bad))
    # Expected: "provenance problems: 0" when every hash resolves and no row
    # was produced from a dirty worktree.
```

**Pitfall:** rebasing or amending commits that already stamped result rows orphans those hashes - `commit_exists` returns False even though "the same code" exists under a new hash. Rule: history rewriting is allowed only for commits that no result row references yet. If you must clean history before publishing the repo, do it *after* tagging and re-running the final tables, or keep the old hashes reachable via a `archive/pre-cleanup` branch.

## Snapshot Patterns - Tags for Paper Results

### Pattern 5: One annotated tag per paper artifact

When a table or figure is final, freeze the exact code state behind it. Annotated tags are the right object: immutable, named, carrying a message that says which artifact they back. The naming scheme makes them sortable and greppable.

```text
Tag naming scheme:

  paper-<venue><year>-<round>-<artifact>

  paper-ejor2026-r0-table3      code behind Table 3, initial submission
  paper-ejor2026-r0-fig4        code behind Figure 4 convergence plot
  paper-ejor2026-r1-table3      Table 3 after first revision
  thesis-ch4-final              chapter-level snapshot

One tag per artifact (not one per paper) when tables were produced at
different commits; one tag for everything when the whole results section
was regenerated from a single commit (the cleaner setup - aim for it).
```

```python
import subprocess
from pathlib import Path


def tag_paper_snapshot(tag: str, message: str, repo: str = ".") -> None:
    """Create an annotated tag freezing the code state behind a paper artifact."""
    subprocess.run(
        ["git", "-C", repo, "tag", "-a", tag, "-m", message],
        check=True,
    )


def export_snapshot(tag: str, out_dir: str = "snapshots", repo: str = ".") -> Path:
    """Export the tagged tree as a zip (no .git history) for archival upload."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    target = (out / f"{tag}.zip").resolve()
    subprocess.run(
        ["git", "-C", repo, "archive", "--format=zip",
         f"--output={target}", tag],
        check=True,
    )
    return target


if __name__ == "__main__":
    tag_paper_snapshot(
        "paper-ejor2026-r0-table3",
        "Code state for Table 3: ILS vs SA, 30 instances x 10 seeds, "
        "configs/campaign_table3.json, results in raw_runs.csv commit-filtered.",
    )
    path = export_snapshot("paper-ejor2026-r0-table3")
    print("archived:", path)
    # Expected: annotated tag created; snapshots/paper-ejor2026-r0-table3.zip
    # contains the exact tagged tree, suitable for Zenodo/journal upload.
```

**Pitfall:** tags are local until you `git push --tags` (or `git push origin <tag>`); a disk failure before pushing destroys the snapshot. Push tags immediately after creating them. Second trap: re-pointing an existing tag (`git tag -f`) after the paper is submitted silently breaks the paper-to-code link - if the code must change, create a new tag for the new round instead.

### Pattern 6: Re-run an old result without disturbing current work

Reviewers ask for reruns months later. Checking out an old commit in your main worktree stalls current development and risks mixing states. `git worktree` gives you the old code in a separate directory while `main` keeps moving.

```python
import subprocess
from pathlib import Path


def add_rerun_worktree(commit: str, repo: str = ".",
                       root: str = "../reruns") -> Path:
    """Check out `commit` into a fresh detached worktree for re-running.

    The main checkout stays untouched; current development continues in
    parallel with the rerun.
    """
    dest = Path(root) / commit[:12]
    subprocess.run(
        ["git", "-C", repo, "worktree", "add", "--detach", str(dest), commit],
        check=True,
    )
    return dest


def remove_rerun_worktree(dest: Path, repo: str = ".") -> None:
    """Remove a finished rerun worktree and prune git's bookkeeping."""
    subprocess.run(
        ["git", "-C", repo, "worktree", "remove", "--force", str(dest)],
        check=True,
    )
    subprocess.run(["git", "-C", repo, "worktree", "prune"], check=True)


if __name__ == "__main__":
    target = "paper-ejor2026-r0-table3"   # tags and raw hashes both work
    dest = add_rerun_worktree(target)
    print("re-run inside:", dest)
    # Expected: ../reruns/<short-ref>/ holds the exact old tree; run the
    # recorded config + seed there and compare objectives row by row.
```

**Pitfall:** the worktree pins the *code*, not the *environment*. If numpy or Gurobi changed versions since the original run, objectives can differ (different default parameters, different tie-breaking, different RNG streams across major numpy versions). That is why Pattern 7's manifest records package versions: recreate the environment (`pip install numpy==1.26.4 ...` or a lockfile) inside a fresh virtualenv before re-running. Note `add_rerun_worktree(commit[:12])` builds `dest` from the first 12 chars of whatever ref you pass - for tag names the directory is just the truncated tag, which is fine.

### Pattern 7: Per-run manifest - commit + config + environment

The result row holds the scalars; the manifest holds everything else needed to re-run: full config, interpreter version, OS, and the exact versions of the packages that influence numerics.

```python
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path


def environment_snapshot(packages: list[str]) -> dict:
    """Record interpreter, OS, and installed versions of numerics packages."""
    versions: dict[str, str] = {}
    for pkg in packages:
        try:
            versions[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            versions[pkg] = "not installed"
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": versions,
    }


def write_run_manifest(run_id: str, config: dict, repo: str = ".",
                       out_dir: str = "results/manifests") -> Path:
    """Write a JSON sidecar binding one run to commit, config, and environment."""
    commit = subprocess.run(
        ["git", "-C", repo, "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    manifest = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit": commit,
        "config": config,
        "environment": environment_snapshot(["numpy", "pandas", "gurobipy"]),
    }
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{run_id}.json"
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    cfg = {"algorithm": "ils", "max_iter": 20000, "kick_strength": 4, "seed": 7}
    path = write_run_manifest("ils_rand_n50_seed7", cfg)
    print("manifest:", path)
    # Expected: results/manifests/ils_rand_n50_seed7.json containing the commit
    # hash, the full config dict, and pinned numpy/pandas/gurobipy versions.
```

**Pitfall:** dumping `pip freeze` (hundreds of lines) into every manifest creates noise that hides the signal; record only packages whose version can change numerics (solver, numpy/scipy, your own package). Conversely, recording *no* environment is the classic failure: "same commit, different numbers" at revision time is almost always a solver or numpy upgrade, and without the manifest you cannot prove it.

## Hygiene Patterns - Ignore Rules, Hooks, and Repository Size

### Pattern 8: A .gitignore built for optimization work

Solver and experiment artifacts appear in predictable shapes. Ignore them from day one - retro-fitting after `results/` is in history requires a rewrite.

```text
# --- experiment outputs (regenerate from commit + config + seed) ---
results/
snapshots/
figures/
*.csv
*.parquet
!data/instances/**/*.csv        # committed benchmark instances stay tracked

# --- solver artifacts ---
*.log                            # Gurobi/CP-SAT/HiGHS logs
*.lp
*.mps
*.sol
*.ilp                            # IIS output
*.prm                            # parameter dumps
*.rew *.dua *.bas

# --- secrets and licenses: NEVER in a repo ---
gurobi.lic
*.lic
.env

# --- python noise ---
__pycache__/
*.pyc
.venv/
*.egg-info/

# --- editor/OS noise ---
.idea/ .vscode/
.DS_Store Thumbs.db
```

**Pitfall:** the blanket `*.csv` rule also hides *input* data; the negation line (`!data/instances/...`) re-includes committed benchmarks, but git cannot re-include a file inside an ignored *directory* - which is why the rule ignores `*.csv` by extension and `results/` by directory, never `data/` itself. Test the net effect with `git check-ignore -v <path>` whenever a file mysteriously refuses to be added.

### Pattern 9: Pre-commit guard against artifacts and oversized files

`.gitignore` does not stop `git add -f` or a pattern gap. A pre-commit hook is the hard boundary: commits containing result artifacts or large blobs fail with an explanation.

```python
import subprocess
import sys

MAX_BYTES = 5_000_000
ALLOWED_PREFIXES = ("data/instances/",)
BLOCKED_PREFIXES = ("results/", "logs/", "snapshots/", "figures/")
BLOCKED_SUFFIXES = (".log", ".sol", ".lp", ".mps", ".ilp", ".parquet")


def staged_files() -> list[str]:
    """Paths of files added/copied/modified in the staged commit."""
    out = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.split()


def staged_blob_size(path: str) -> int:
    """Size in bytes of the staged version of `path` (index, not worktree)."""
    out = subprocess.run(
        ["git", "cat-file", "-s", f":{path}"],
        capture_output=True, text=True, check=True,
    )
    return int(out.stdout.strip())


def main() -> int:
    """Block commits that include experiment artifacts or oversized blobs."""
    failures: list[str] = []
    for path in staged_files():
        if path.startswith(ALLOWED_PREFIXES):
            continue
        if path.startswith(BLOCKED_PREFIXES) or path.endswith(BLOCKED_SUFFIXES):
            failures.append(f"{path}: experiment artifact - keep out of git")
        elif staged_blob_size(path) > MAX_BYTES:
            failures.append(f"{path}: {staged_blob_size(path)} B > {MAX_BYTES} B")
    for line in failures:
        print(f"pre-commit: {line}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
    # Expected: exit 0 on a clean commit; exit 1 listing each blocked file,
    # which aborts the commit.
```

```text
Installation (plain hook, no framework needed):

  cp scripts/precommit_guard.py .git/hooks/   # keep source in scripts/ too
  printf '#!/bin/sh\nexec python scripts/precommit_guard.py\n' > .git/hooks/pre-commit
  chmod +x .git/hooks/pre-commit

Or with the pre-commit framework (.pre-commit-config.yaml):

  repos:
    - repo: local
      hooks:
        - id: artifact-guard
          name: block experiment artifacts and large files
          entry: python scripts/precommit_guard.py
          language: system
          pass_filenames: false
```

**Pitfall:** hooks live in `.git/hooks/`, which is *not versioned* - a fresh clone has no hooks. Keep the hook script in `scripts/` (versioned) and document the one-line install, or use the `pre-commit` framework whose config file *is* versioned. Second trap: checking worktree file size instead of staged blob size (`git cat-file -s :<path>`) misses the case where a huge file was staged and then truncated on disk.

### Pattern 10: Regression gate for risky refactors

A refactor branch earns its merge by proving behavior is unchanged: same commit-pinned configs and seeds must give identical objectives. Run the baseline suite on `main`, run it on the branch, and diff per-(instance, algorithm, seed).

```python
import pandas as pd


def compare_baselines(old_csv: str, new_csv: str,
                      tol: float = 1e-9) -> pd.DataFrame:
    """Join per-(instance, algorithm, seed) objectives from two result tables.

    For a behavior-preserving refactor with fixed seeds, every delta must be
    zero (up to floating-point reordering tolerance).
    """
    keys = ["instance", "algorithm", "seed"]
    old = pd.read_csv(old_csv)[keys + ["objective"]].rename(
        columns={"objective": "objective_old"})
    new = pd.read_csv(new_csv)[keys + ["objective"]].rename(
        columns={"objective": "objective_new"})
    merged = old.merge(new, on=keys, how="outer", indicator=True)
    merged["delta"] = merged["objective_new"] - merged["objective_old"]
    merged["regression"] = ((merged["_merge"] != "both")
                            | (merged["delta"].abs() > tol))
    return merged


if __name__ == "__main__":
    report = compare_baselines("results/baseline_main.csv",
                               "results/baseline_refactor.csv")
    bad = report[report["regression"]]
    print(f"{len(bad)} regressions out of {len(report)} paired runs")
    if len(bad) > 0:
        print(bad[["instance", "algorithm", "seed", "delta"]].head(10)
              .to_string(index=False))
    # Expected: "0 regressions out of N paired runs" for a pure refactor;
    # any nonzero delta means the branch changed behavior, not just structure.
```

**Pitfall:** runtime is *not* part of the equality gate - a refactor for speed should change `runtime_s` and nothing else. But beware floating-point summation order: vectorizing a loop can change objectives in the 12th digit legitimately. Set `tol` to the level your objective arithmetic guarantees (exact integers: `tol=0`; float accumulation: `1e-9` relative is typical), and document the choice next to the gate.

## Advanced Techniques

### Bisecting a results regression

When a probe instance's objective silently changed somewhere in the last 60 commits, `git bisect run` finds the culprit commit in O(log n) probe runs - this is the payoff of small commits. Write a check script that exits 0 (good), 1 (bad), or 125 (skip: commit cannot run the probe).

```python
"""Bisect probe: exit 0 if the solver still reproduces the reference objective.

Usage:
    git bisect start <bad-commit> <good-commit>
    git bisect run python scripts/bisect_check.py
"""
import subprocess
import sys

REFERENCE_OBJECTIVE = 1234.5
TOLERANCE = 1e-9


def run_probe() -> float:
    """Run the fast probe experiment and parse the printed objective."""
    out = subprocess.run(
        [sys.executable, "scripts/run_experiment.py",
         "--config", "configs/probe_small.json", "--seed", "7"],
        capture_output=True, text=True, timeout=120,
    )
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-500:])
    last_line = out.stdout.strip().splitlines()[-1]   # e.g. "objective=1234.5"
    return float(last_line.split("=")[1])


def main() -> int:
    """Map the probe outcome onto git-bisect exit codes (0 good, 1 bad, 125 skip)."""
    try:
        objective = run_probe()
    except Exception:
        return 125    # this commit cannot run the probe: tell bisect to skip it
    return 0 if abs(objective - REFERENCE_OBJECTIVE) <= TOLERANCE else 1


if __name__ == "__main__":
    sys.exit(main())
    # Expected: `git bisect run` converges to the first behavior-changing
    # commit in ~log2(#commits) probe executions, then `git bisect reset`.
```

Keep the probe under ~2 minutes (small instance, short iteration budget, fixed seed); bisect may run it 8-12 times. The probe config must exist across the whole bisect range - if you renamed configs mid-range, have the script fall back or return 125.

### Branch strategy for risky refactors

Protocol: (1) on `main`, run the baseline suite and commit/record its results file with the commit hash; (2) branch `refactor/<topic>`; (3) commit in small steps, running the probe instance after each step so bisect stays usable *within* the branch; (4) at the end, run the full baseline suite and apply Pattern 10's gate; (5) merge with `--no-ff` so the branch shape survives in history, or rebase-then-merge if you prefer linear history *and* no result rows reference the branch commits yet (Pattern 4's pitfall). Abandoned branches: keep them under `try/` for a month, then delete - the reflog and the experiment log entry preserve what was learned.

### Paper repository coupling

Two workable setups. (a) Paper inside the code repo (`paper/` directory): a single tag freezes code and text together; ignore LaTeX build artifacts (`*.aux`, `*.bbl`, `*.synctex.gz`). (b) Separate paper repo: store the code tag name and commit hash in a `provenance.tex` comment block next to each table, and consider a git submodule pin if reviewers get repo access. In both setups, generate LaTeX tables programmatically from the stamped results file rather than pasting numbers - the generating script plus the commit hash *is* the audit trail (see **pandas-experiment-management** for `DataFrame.to_latex` pipelines).

### Large instances and external data

Committing 500 MB of benchmark instances makes every clone painful. Options, in order of preference: (1) commit the *generator* + seeds and regenerate (best - generators are tiny and exact); (2) a versioned download script plus a committed `checksums.sha256` file, verified before experiments run; (3) `git lfs track "data/large/**"` when the data is irreplaceable and must live with the repo (mind LFS bandwidth quotas on public hosts); (4) DVC when datasets themselves evolve and need their own versioning. Never option zero - raw blobs in plain git history.

### Cleaning history before publishing the repo

Before making a thesis/paper repo public: scan for secrets (`gurobi.lic`, tokens) over *all history*, not just HEAD - `git log --all --diff-filter=A --name-only` or a scanner like gitleaks; strip accidentally committed bulk with `git filter-repo --path results/ --invert-paths` (operate on a fresh clone; the rewrite changes all downstream hashes). Because rewriting breaks the hash links in stamped result tables, do this only after final tables are regenerated, or publish a clean *export* (Pattern 5's `git archive`) instead of the living repo.

## Practical Challenges

**Old results no longer reproduce after months of development.** The result rows carry commit hashes (Pattern 3) - use Pattern 6 to open a worktree at the recorded hash, recreate the environment from the run manifest (Pattern 7), and re-run with the recorded config and seed. If they *still* differ, the run was under-specified: typically an unseeded RNG, wall-clock-dependent stopping, or thread-count-dependent solver behavior (fix `Threads` and `Seed` in Gurobi params).

**The repo is 2 GB because results and logs were committed early on.** Stop the bleeding first: add the ignore rules (Pattern 8) and `git rm -r --cached results/` so new commits are clean. Then schedule a history rewrite with `git filter-repo` on a fresh clone - but only after auditing which stamped hashes would be orphaned (Pattern 4) and re-tagging final states.

**Forty commits in a row named "fix" or "wip".** History like this defeats bisect and code archaeology. Going forward, adopt the subject-line convention (`<area>: <change>`) and commit per logical change. For the existing mess: do not rewrite if result rows reference those hashes; instead, write one annotated tag now with a message summarizing the state, and start the discipline from here.

**A reviewer asks for new experiments 9 months after submission.** Check out the paper tag in a worktree, rebuild the environment from the manifests, re-run the baseline suite, and *verify it matches the submitted table before* running anything new. If it matches, run the new experiments from the same tag (or from a `revision-r1` branch off the tag if code changes are needed) and tag the new state `paper-<venue>-r1`.

**Results were produced from a dirty worktree and it is in the paper.** Quantify the damage: `dirty` rows are flagged in the table (Pattern 3). Re-run those exact (instance, algorithm, seed) cells from the nearest clean commit; if the numbers match, replace the rows and note nothing; if they differ, the published numbers are unreproducible and must be regenerated wholesale before camera-ready. Then install Pattern 2 so it cannot recur.

**A refactor silently changed objective values.** If the regression gate (Pattern 10) was skipped, bisect (Advanced Techniques) between the last-good and first-bad commits with a fast probe. The most common culprits in optimization code: changed iteration order altering RNG consumption, delta-evaluation bugs, and floating-point reassociation from vectorization.

**Binary or licensed instance data bloats or legally contaminates the repo.** Keep licensed data out entirely: a download script with checksum verification, plus an ignore rule for `data/licensed/`. For bulky open data, prefer regenerating from committed generators with seeds; the generator is the ground truth and diffs are reviewable.

**Experiments run on a cluster, development happens on a laptop.** Push before submitting jobs; the job script's first action is `git fetch && git checkout <hash>` into a job-specific worktree or clone, with the hash passed explicitly by the submit script - never "whatever the shared checkout currently has." Stamp rows with hostname as well; cross-machine numeric drift (different BLAS, different CPU) then becomes diagnosable.

**The Gurobi license file got committed and pushed.** Treat it as leaked: remove it from all history (`git filter-repo --path gurobi.lic --invert-paths`), force-push, and rotate the license/WLS credentials with the vendor. Add `*.lic` to both the repo `.gitignore` and your global ignore file (`git config --global core.excludesFile`).

**Two tables in the paper turn out to come from different commits.** Pattern 4's audit shows the mix. Decide which commit is canonical, re-run the stale table's cells from it, and from then on regenerate the *entire* results section from one commit per revision round - one tag, one hash, every table.

## Tools & Libraries

| Tool / library | When to use | Note |
|---|---|---|
| git (CLI via `subprocess`) | All patterns in this skill | Zero dependencies; porcelain `--porcelain` output is script-stable |
| GitPython | Heavier in-process repo manipulation | Convenient object model; slower, extra dependency - subprocess usually suffices |
| `pre-commit` framework | Versionable hook management | Config in-repo; solves the ".git/hooks not cloned" problem |
| git-lfs | Irreplaceable large binary data | Mind bandwidth/storage quotas on public hosts |
| `git filter-repo` | History rewrites (bulk/secret removal) | The maintained successor to filter-branch; work on a fresh clone |
| DVC | Datasets/models with their own version lifecycle | Overkill for code-only repos; good when instances evolve |
| gh / glab CLI | Releases, tag pushing, repo automation | `gh release create <tag> snapshots/<tag>.zip` publishes a snapshot |
| gitleaks | Secret scanning over full history | Run before any repo goes public |
| Zenodo / Software Heritage | Archival DOI for the tagged snapshot | GitHub releases can vanish; a DOI in the paper cannot |

## Output Format

A complete answer on this topic delivers checklists and templates the user can adopt verbatim.

```text
REPOSITORY SETUP CHECKLIST (once per project)
[ ] git init; add remote; first push
[ ] .gitignore from Pattern 8 (results, solver logs, secrets, python noise)
[ ] pre-commit guard installed and its source committed under scripts/
[ ] data/ policy decided: generators+seeds | download+checksums | LFS
[ ] experiment runner calls require_clean_worktree() and stamps rows
[ ] manifests directory + environment_snapshot wired into the runner
[ ] global ignore for *.lic and editor noise (core.excludesFile)

PER-EXPERIMENT LOOP CHECKLIST (every iteration)
[ ] one logical change -> one commit, subject "<area>: <change>"
[ ] behavior-changing fixes flagged in the message ("objectives change!")
[ ] run launched from clean worktree; rows stamped with commit+seed
[ ] anomalies cross-checked against the commit that produced them

PAPER SNAPSHOT CHECKLIST (per submission / revision round)
[ ] full results section regenerated from ONE commit
[ ] audit_provenance(): zero dirty rows, all hashes resolve
[ ] annotated tag paper-<venue>-<round> created AND pushed
[ ] git archive zip exported; archived (Zenodo/release) if venue requires
[ ] LaTeX tables generated from the stamped results file, not hand-typed
[ ] tag name + commit hash recorded next to each table in the paper source
```

Deliverables to hand the user: the `.gitignore` template, the guard + stamping + audit functions as a small `provenance.py` module in their project, the hook with its install snippet, and the tag-naming scheme filled in with their venue. When reporting on an existing repo, give a status table: repo size, largest blobs (`git rev-list --objects --all` piped through sort), dirty-row count in their results, and which checklist items are unmet.

## Questions to Ask

- Is this solo work or shared? Does a remote exist, and is the repo (or will it become) public?
- What artifacts does one run produce, and roughly how large are they?
- Are benchmark instances generated, downloaded, or licensed - and how big?
- Do existing result tables carry any provenance (commit, seed, config) today?
- Has anything large or secret already been committed (repo size vs source size)?
- What is the reproducibility horizon - conference camera-ready, journal revisions, thesis defense?
- Which solver and Python packages can change numerics, and are versions pinned anywhere?
- Do experiments run where development happens, or on a cluster with a separate checkout?
- Is the paper in the same repository as the code?

## Related Skills

- **optimization-project-structure** — when the question is the repository layout itself: src/scripts/configs/results separation, config systems, and seeding discipline that this git workflow assumes.
- **pandas-experiment-management** — when designing the tidy result tables (one row per run with metadata) that the stamping and audit patterns here read and write.
- **algorithm-benchmarking-statistics** — when the commit-pinned result tables feed an actual comparison: instance/seed protocols, statistical tests, and reporting standards.
