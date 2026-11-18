---
name: binance-datatool
description: List symbols and files in Binance historical archives on data.binance.vision, download datasets such as klines or funding rates, and verify local archive ZIPs against SHA256 checksums.
---

# Binance historical archives

Use `binance-datatool <command> --help` for the installed command's flags and dataset names.
If the CLI is missing, install it with `pipx install binance-datatool` using Python 3.11 or later.
Pass global options before the command. Use `-v` for progress on stderr or `-vv` for diagnostics.

For scripts, multi-symbol results, or failure details, read the bundled
[JSON field reference](references/json-results.md). With `--json`, capture stdout and the exit
code separately. Exit `2` can accompany a usable partial result. When stdout is empty,
read stderr to find out why the command produced no result.

## Discover symbols or files

Check [archive availability](references/archive-availability.md) when choosing a dataset and
partition, selecting a candle interval or COIN-M price symbol, or investigating an empty
listing. For example, one monthly ZIP can contain BTCUSDT daily candles:

```bash
binance-datatool list-files spot BTCUSDT --freq monthly --type klines --interval 1d --only-zip --json
```

Use `list-symbols` with the intended frequency and dataset to discover symbol directories.
Unfiltered output includes every listed name. Any filter flag limits output to symbols with
inferable metadata. Spot supports quote, stablecoin, and leverage filters. USDⓈ-M supports quote,
stablecoin, and contract type. COIN-M filters only by contract type. Passing an inapplicable
filter still drops uninferable names.

Use `list-files` to confirm which ZIPs exist for the exact selection. Both listing commands
work without an Archive home.

## Choose the local folder

Use the same folder for `download` and `verify` throughout the task, including dry-runs.

1. If the user specifies a folder, pass it with `--archive-home`. For example, if they ask to
   download monthly archives of BTCUSDT spot daily candles to `$HOME/binance_archive`, run

   ```bash
   binance-datatool --archive-home "$HOME/binance_archive" download spot BTCUSDT \
     --freq monthly --type klines --interval 1d --json
   ```

2. Otherwise, check `BINANCE_DATATOOL_ARCHIVE_HOME` in the current environment. If it has a
   value, omit the flag so the CLI uses that folder.
3. If the variable is unset or empty, ask in the user's language. For a download, ask
   “Which folder would you like to download the data to?” For verification alone, ask
   “Which folder did you download the data to?” You can then call that folder the Archive home.
   Wait for the user's answer and use their folder as in step 1.

## Preview and download

Both `download` and `verify` accept positional symbols or, when those are omitted, one
symbol per line on stdin.

A download covers all available dates for the selection. For a batch, save the text output
of `list-symbols` once and reuse it for preview, download, and verification. For example,
to estimate a batch of spot USDT daily candles:

```bash
binance-datatool list-symbols spot --freq monthly --type klines \
  --quote USDT --exclude-stables --exclude-leverage > symbols.txt &&
binance-datatool download spot --freq monthly --type klines \
  --interval 1d --dry-run --json < symbols.txt
```

Check listing errors before treating the plan as complete. For the transfer size, sum
`to_download[].size` in bytes. A real download with pending transfers needs `aria2c` on PATH.
To execute the planned selection, rerun the download without `--dry-run`. Account for listing
and transfer failures before reporting success. Downloaded and skipped objects count ZIPs and
checksum files separately. Use `verify` when the user requests an integrity check.

## Verify local ZIPs

Use the same symbols, frequency, dataset, and interval as the download. The command below
scans `data/spot/monthly/klines/BTCUSDT/1d/` under the selected Archive home for monthly
ZIPs of BTCUSDT daily candles.

```bash
binance-datatool verify spot BTCUSDT --freq monthly --type klines --interval 1d --json
```

`verify --dry-run` previews the local scan without hashing or cleanup. A real run deletes a
failed ZIP and its checksum by default. Use `--keep-failed` to inspect failed pairs. To recover
a deleted pair, rerun the matching download, then verify. A real run also removes orphan
checksums and keeps orphan ZIPs for repair.

Report `summary.verified` as ZIPs that passed SHA256 in this run. Report cached `skipped`
ZIPs, failures, and orphans separately. An empty scan can exit `0`, so check `total_zips`
before reporting that files passed. After Ctrl-C, exit `130` has no completed result.
Rerun the same verification to reuse saved markers.
