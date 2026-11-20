---
name: ghidra-decompile
description: Decompile a binary efficiently with Ghidra by targeting exact addresses in a prepared or no-analysis project, and repair the GhidraMCP bridge when its extension does not match the Ghidra version. Use when the task names Ghidra, needs decompiled C or xrefs from a persistent analyzed database, or when a lighter disassembler is not enough.
---

# Ghidra decompilation

Ghidra is the full decompiler and the persistent database. Reach for it when you need the decompiler's C, cross-references, vtables/RTTI, or a second opinion on other tooling's output.

**The cost is analysis, not decompilation.** A 114 MB stripped AArch64 image imported once, then decompiled one targeted function in 3.3 s on a reuse run with `-noanalysis`; full auto-analysis of the same image takes hours and is rarely needed to read one function.

## Choose the path

| situation | path |
|---|---|
| one or two functions, no project | headless import with `-noanalysis` + targeted script |
| repeating questions about one binary | keep the project; `-process` between runs |
| many queries, xrefs, RTTI, renaming, a human at the GUI | open project + GhidraMCP bridge |
| whole-binary pseudocode sweep | analyzed project + `decompile_tree` or a batch script |

## 1. Pin the addresses and the image base

Ghidra scripts take Ghidra virtual addresses (VAs), not file or mod offsets. Read the image base before converting:

```java
println("imageBase=" + currentProgram.getImageBase());
println("language=" + currentProgram.getLanguageID());
```

Verified on the MPC Sample firmware 1.3.0.12: `imageBase=00100000`, `language=AARCH64:LE:64:v8A`. For an ELF, the rule is **Ghidra VA = image base + ELF vaddr**. Do not carry the constant to another loader: use the printed image base.

For that binary the first `LOAD` has file offset == vaddr == 0, so a `.text`/`.rodata` file offset `X` sits at `X + 0x100000`. The second `LOAD` is file offset `0x6d43bb0` → vaddr `0x6d53bb0`, so its file offsets need `+0x110000`; Ghidra shows `.data.rel.ro.local` at `0x6e53bb0`, which is vaddr `0x6d53bb0 + 0x100000`. The mod expresses its offsets as ELF vaddrs, which is why `+0x100000` works throughout its code. Confirm the segment before converting a raw file offset.

If the function entry is unknown, decompile the containing address first (`getFunctionContaining` returns a function for an address inside its body) and locate the prologue from the disassembly. On AArch64, search backwards for `PACIASP` (`0xd503233f` as a word; bytes `3f 23 03 d5` in file order) for candidate entries; treat candidates as unconfirmed until the decompiler agrees.

**Done when:** the image base is printed and every address you are about to decompile is a VA.

## 2. Decompile exact addresses headless

```sh
GHIDRA="${GHIDRA:-$HOME/Applications/ghidra_12.2_PUBLIC}"
PROJ=/tmp/ghproj
BIN=/path/to/mpcsample.bin
mkdir -p "$PROJ"

GHIDRA_HEADLESS_MAXMEM=32G "$GHIDRA/support/analyzeHeadless" "$PROJ" target \
  -import "$BIN" -noanalysis \
  -scriptPath "$PWD/tools/ghidra/hpss" \
  -postScript ResearchDecompile.java 0x17580d0 0x153ed40
```

- Create the project directory first. Without it Ghidra aborts with `Directory not found`.
- The first run imports and saves; later runs reuse the project and are much faster:
  `... "$PROJ" target -process "$(basename "$BIN")" -noanalysis -scriptPath ... -postScript ...`
- `-noanalysis` is the efficiency lever. Drop it only when you genuinely need Ghidra's function discovery for a whole binary.
- Script output is prefixed (`INFO  ResearchDecompile.java> ...`). Grep for `=====` to find each function header; the C follows.

Minimal script — save as `ResearchDecompile.java` in the script path (the MPC Sample repo already has it in `tools/ghidra/hpss/`):

```java
import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class ResearchDecompile extends GhidraScript {
  @Override public void run() throws Exception {
    DecompInterface d = new DecompInterface();
    d.openProgram(currentProgram);
    try {
      for (String arg : getScriptArgs()) {
        Address a = toAddr(Long.decode(arg));
        Function f = getFunctionAt(a);
        if (f == null) f = getFunctionContaining(a);
        if (f == null) { disassemble(a); f = createFunction(a, null); }
        println("===== " + arg + " => " +
            (f == null ? "no function" : f.getName() + " @ " + f.getEntryPoint()) + " =====");
        if (f == null) continue;
        DecompileResults r = d.decompileFunction(f, 120, monitor);
        println(r.decompileCompleted()
            ? r.getDecompiledFunction().getC()
            : "/* decompile failed: " + r.getErrorMessage() + " */");
      }
    } finally { d.dispose(); }
  }
}
```

The script disassembles and creates a function when Ghidra has none. That edits the project database, not the binary on disk.

Verified output shape:

```text
INFO  ResearchDecompile.java> ===== 0x17580d0 => FUN_017580d0 @ 017580d0 =====
INFO  ResearchDecompile.java>
void FUN_017580d0(long param_1)
...
```

**Done when:** every requested address prints a `=====` header and either C or an explicit `decompile failed` line.

## 3. Keep it fast

- Pass many addresses to one script run; JVM startup dominates, decompilation itself is cheap.
- Import once, then reuse with `-process`. Do not re-import per question.
- Use `getFunctionContaining` on a nearby address instead of guessing an entry.
- Find targets from strings, imports, vtables, or callers before decompiling. Reading everything is slower than locating the one function that matters.
- Skip the GUI entirely for "give me the C at this address"; the bridge pays off only when you need repeated interactive queries.

## 4. Use the bridge for the persistent project

This is the path for xrefs, RTTI, vtable walks, renames, and many decompiles from an MCP client.

### Install the extension for the exact Ghidra version

The released `GhidraMCP-7.0.0.zip` is built for Ghidra 12.1.4. Against 12.2 every decompile fails with `ghidra/program/model/lang/SleighLanguageDescription`. Build the 12.2 branch instead:

```sh
git clone https://github.com/bethington/ghidra-mcp   # or reuse an existing clone
cd ghidra-mcp
git fetch --depth 1 origin chore/ghidra-12.2
git checkout -f FETCH_HEAD
./gradlew buildExtension -PGHIDRA_INSTALL_DIR="$HOME/Applications/ghidra_12.2_PUBLIC"

unzip -p build/distributions/GhidraMCP-7.0.0.zip GhidraMCP/extension.properties | grep version
# version=12.2

EXT="$HOME/Library/ghidra/ghidra_12.2_PUBLIC/Extensions"
rm -rf "$EXT/GhidraMCP"
unzip -q build/distributions/GhidraMCP-7.0.0.zip -d "$EXT"
```

Restart Ghidra. In the project window enable **File > Configure > Utility > Configure > GhidraMCPPlugin**, open the program, and check the server:

```sh
curl http://127.0.0.1:8089/check_connection
# {"status": "ok", "server_kind": "gui", "version": "7.0.0"}
```

Start Ghidra with `GHIDRA_MCP_ALLOW_SCRIPTS=1` when you need `run_ghidra_script`; since v5.4.1 that endpoint is denied by default.

On the reference build the rebuilt extension advertises 216 endpoints, `force_decompile` returns C, and a 69,271-function analysis survives a Ghidra restart. Treat those as the success checks for this install, not as portable counts.

### Install and point the bridge

```sh
uv tool install https://github.com/bethington/ghidra-mcp/releases/download/v7.0.0/ghidra_mcp_bridge-7.0.0-py3-none-any.whl
which bridge-mcp-ghidra
```

Skip the install when `which bridge-mcp-ghidra` already resolves. Point the MCP client at the absolute path (a GUI-launched client does not inherit your shell `PATH`). `connect_instance` takes a **required** `project` name on the build verified here (1.30.0); omitting it fails validation instead of auto-connecting to the running instance.

### Tool names that actually exist in 7.0.0

7.0.0 consolidated the old per-field tools. `decompile_function` is **gone**; use:

- `get_functions(function=0x17580d0, fields="decompiled_code")` — one or up to 20 functions via `functions="a,b,c"`; omit `fields` for everything.
- `force_decompile(function=...)` — fresh decompilation, stamped with language/variant.
- `find_functions`, `get_entry_points`, `list_strings`, `get_xrefs_to`, `get_function_call_graph`, `get_metadata`, `list_program_items`.
- `run_ghidra_script(script_name, args, program, timeout_seconds=300, capture_output=true)`.

Lazy loading is the default. Until `connect_instance` has attached to a live Ghidra, `tools/list` is exactly the 8 static tools — `list_instances`, `connect_instance`, `list_tool_groups`, `load_tool_group`, `unload_tool_group`, `check_tools`, `search_tools`, `import_file` — in both `--lazy` and `--no-lazy` modes, and `search_tools` returns zero matches. `--no-lazy` does not preload the rest: the groups cannot be enumerated while no instance is connected. This is not a broken bridge. Once attached, discover them with `search_tools("decompile")` and `load_tool_group("xref")`.

Call `connect_instance(project="...")` before the first program-scoped call. With several programs open, pass `program=` on every program-scoped call, or set `GHIDRA_MCP_REQUIRE_PROGRAM_SELECTORS=1` to make omissions an error instead of silently reading the active tab.

### Stdio driver when the client has no MCP tools

The bridge is MCP over stdio as well as HTTP. One session is enough for initialize, connect, and script execution:

```python
import json, shutil, subprocess, sys

p = subprocess.Popen(
    [shutil.which("bridge-mcp-ghidra"), "--transport", "stdio", "--no-lazy"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

def call(i, method, params):
    p.stdin.write(json.dumps(dict(jsonrpc="2.0", id=i, method=method, params=params)) + "\n")
    p.stdin.flush()
    while True:
        msg = json.loads(p.stdout.readline())
        if msg.get("id") == i:
            return msg

call(1, "initialize", dict(protocolVersion="2025-06-18", capabilities={},
                           clientInfo=dict(name="decompile", version="1")))
p.stdin.write(json.dumps(dict(jsonrpc="2.0", method="notifications/initialized", params={})) + "\n")
p.stdin.flush()
call(2, "tools/call", dict(name="connect_instance", arguments=dict(project="target")))
r = call(3, "tools/call", dict(name="run_ghidra_script", arguments=dict(
    script_name=sys.argv[1], args=" ".join(sys.argv[2:]), program="mpcsample.bin",
    timeout_seconds=300, capture_output=True)))

text = r.get("result", {}).get("content", [{}])[0].get("text", str(r))
try:
    print(json.loads(text).get("console_output", text))
except ValueError:
    print(text)
```

`console_output` carries the script's `println`. Treat `isError`, a missing `success`, or a top-level `error` as failure. The driver keeps one session because reconnecting for each call adds noise and can race project selection.

**Done when:** `check_connection` answers, `connect_instance` names the project, and one script or `get_functions` call returns the expected function.

## 5. Validate the decompiled C

- Argument and variable types in Ghidra are **hints** produced by the decompiler. The registers at a live call are the contract; confirm a prototype against the call site before trusting it.
- Decompiled C is pseudocode. Confirm the function entry and end from the disassembly; a function created at a mid-function address can swallow the following bytes.
- Confirm a vtable slot or global with xrefs/RTTI before naming it. On this target the vptr points at the vtable, `typeinfo` sits at `vptr-8`, and the class name at `typeinfo+8`.
- When the C references `FUN_...` or `UNK_...`, decompile the callee next rather than guessing its behaviour from the call.

The ready-made scripts in the MPC Sample firmware project (`sample-converter/tools/ghidra/hpss/`) cover the common questions:

| script | use |
|---|---|
| `ResearchDecompile` | C for explicit addresses; creates a function if missing |
| `DisasmRange` | raw instructions for a range |
| `DumpVtable` / `DumpRTTI` / `DumpWords` | vtable slots, RTTI names, raw words |
| `DumpParams` / `DumpParamNames` | parameter tables |
| `FindConst` / `FindStrings` / `FindPointerValues` | constants, string xrefs, pointers to a value |
| `FindFunctionRefs` / `FindIndirectSlot` / `FindOffsetUse` | callers and users of a slot or offset |
| `HpssEntry` | backwards scan for `PACIASP` candidates |
| `ProgramInfo` | image base, blocks, language, byte checks |

Copy them to `~/ghidra_scripts` for the GUI, or pass their directory as `-scriptPath` for headless runs.

## 6. Failures and their fixes

| symptom | cause | fix |
|---|---|---|
| `SleighLanguageDescription` on every decompile | extension built for 12.1.4, running 12.2 | rebuild the `chore/ghidra-12.2` branch; check `extension.properties` says `version=12.2` |
| `Directory not found` | project directory does not exist | `mkdir -p` the project location first |
| `file already exists` on import | program already in the project | reuse it with `-process`, or add `-overwrite` to re-import |
| no functions, only bytes | `-noanalysis` means Ghidra discovered nothing | `disassemble` + `createFunction` at the target, as the script does |
| `run_ghidra_script` returns 403 | scripts disabled | start Ghidra with `GHIDRA_MCP_ALLOW_SCRIPTS=1` |
| `list_instances` is empty | no Ghidra GUI running with a project open | start Ghidra, open the program, retry |
| `tools/list` shows only 8 tools | no live instance attached; identical in `--lazy` and `--no-lazy` | call `connect_instance(project=...)` against a running Ghidra, then load groups |
| `connect_instance` → `project Field required` | `project` is required on 1.30.0 | pass `project="..."`; there is no auto-connect |
| connect returns `{"error": "No instance matching ..."}`, yet `isError` is false | the attach failed but the call looked successful | start Ghidra with that project open; confirm with `list_instances` |
| a tool is missing from `tools/list` | lazy group not loaded | `search_tools(...)` then `load_tool_group("xref")` |
| wrong function decompiled | several programs/projects open | pass `program=`; enable `GHIDRA_MCP_REQUIRE_PROGRAM_SELECTORS=1` |
| function output looks like a continuation | address was mid-function or in data | read the disassembly around it; re-create at the real entry |

## 7. Cheaper raw-byte alternatives

- `radare2` — sections, dynamic relocations, byte reads (`iS`, `ir`, `px`).
- `nm`/`objdump` on an unstripped companion `.elf` for symbols.
- Raw ELF helpers in the same project's `tools/re/` — `.data.rel.ro` plus `.rela.dyn` resolve vtables from the file alone; `classof.py` maps a live vptr to a class name, `calls.py` lists `BL` call sites, `fwxref.py` finds `adrp/add/ldr` references to a string or global.
