---
name: fastmint-fcfs
description: Use when the user says "mint free jam HH:MM", "fcfs", "gas", "gausah riset", "mint cepat", or wants a free/paid FCFS mint, claim, or share sale fired the moment it opens from the Binance Agentic Wallet (baw) on BSC, with broadcast inside 5 seconds of the open. Fast recon -> bench -> fire -> report, no long research.
---

# Fast FCFS mint (Binance Agentic Wallet, BSC 56) — target: broadcast < T+5s

`SKILL_DIR` = the folder holding this file (on this machine `~/Claude/.agents/skills/fastmint-fcfs`).
Everything runs through `./fastmint.sh` from `SKILL_DIR`: `bench`, `recon`, `fire`, `logs`, `locks`.
Full docs: `README.md` (English) | `README.id.md` (Bahasa Indonesia).
Speed matters, so skip deep risk research unless the user asks. The safety rails below are never skipped.

## Safety rails (never skip)
- Fire only on the user's explicit command for this mint ("mint free jam 23:00", "gas", "ok"). A link alone is not a go-ahead.
- Free mint = `--value 0`. A paid mint needs an amount the user stated. Pass it as `--value` and `--maxValue` (cap). fire.js refuses value > maxValue and refuses value > 0 without a cap.
- One broadcast only. fire.js writes `runs/lock_<hash>.json` before execute and refuses the same call again. Never auto-retry after execute, even on an execute error or a reverted tx. Delete a lock only on the user's explicit new command.
- Never run `baw auth signin` yourself. If status is not CONNECTED, stop and ask the user. Never ask for a private key, seed phrase, or website session token.
- Never work around Binance risk blocks (351803), RISK flags, or allowance/authority changes in the preview. Stop and report.
- Use only the connected wallet. `bench --live` and any real execute cost gas: only on the user's explicit OK.

## How the < 5s path works (measured on this machine, 2026-11-11)
| step | cost | note |
|---|---|---|
| block with ts ≥ start is sealed and seen | ≈0.4–0.9s after ts | BSC blocks ≈0.5s; WS newHeads from publicnode/drpc + HTTP head poll on the 3 fastest RPCs |
| `baw contract-call preview` | ≈0.55–0.75s | backend simulates; fails with 351805 until the mint is open; requestId lives 300s |
| `baw contract-call execute` | ≈0.7s (measured 707ms) | signs and broadcasts; returns txHash |
| inclusion | ≈0.4–0.5s | next block (measured: block ts 0.36s after execute was sent, receipt 0.54s after broadcast) |

fire.js does not wait for one thing to confirm before trying the next. Three triggers all launch previews, spaced `--gap` 350ms, max `--inflight` 3:
1. **clock**: at the NTP-corrected start time (`--clockFire 0`), before any block confirms. If the backend's state is not open yet the preview fails cheaply (351805) and the next trigger retries.
2. **head**: a block with timestamp ≥ start (WS or poll).
3. **eth_call OK**: a pre-simulation from the wallet succeeds on any of the 4 fastest RPCs (`latest` and `pending`, every 100ms).
Clock and head only run during the `--burst` window (3s after start, ≈8 previews). After that only eth_call OK launches a preview, so a sale that opens late is not spammed into `--maxPreviews`; the eth_call spin keeps watching until `--timeout`.
The first preview with `simulationCode 000000000` is executed once; others are ignored. Measured 2026-11-11 (dry-run + one live 0-value tx): clock trigger T+0.01–0.08s, head trigger T+0.25–0.55s, preview 0.45–0.8s, execute 0.7s, inclusion 0.4–0.5s. Expected when the backend's node sees the open state on the first block: broadcast ≈ T+1.3–2.0s, included ≈ T+1.8–2.5s. Old sequential flow was T+5–6s.

## Flow
0. **Env check (once per session, ~10s):** `./fastmint.sh bench`. It ranks RPCs, measures WS head delay, clock offset, baw status/devMode/session, Agent ID, and preview latency with a harmless read-only calldata. Fix anything red before promising a time:
   - `UNCONNECTED` → ask the user to sign in (`baw auth signin --json` only on their OK, then `auth verify --qrCodeId`).
   - devMode OFF/expired (351802/351804) → user enables it in Binance App (Agentic Wallet → Settings → Developer Mode).
   - Node TLS `UNABLE_TO_GET_ISSUER_CERT_LOCALLY` → `./fastmint.sh bench --ca` builds `~/.config/certs/system-ca.pem` from the macOS keychain; lib.js auto-loads it.
   - `SSL_ERROR ... altnames: internetbaik.telkomsel.com` or DNS answering `internetpositif.id` → the ISP hijacks DNS for binance.com. The user must use encrypted DNS (Cloudflare 1.1.1.1 app in DNS-only mode) or a VPN. Do not change system DNS yourself.
1. **Recon (~5–10s):** `./fastmint.sh recon <site-url>` (add `--contract 0x..` if the CA is known). It fetches HTML, JS bundles and agent docs (llms.txt, skill.md, handbook.md…), extracts addresses, chainId, mint fn names, ABI sigs and unix times, runs eth_getCode, loads the Sourcify ABI (or the site-bundle ABI filtered to selectors in the bytecode), reads the view getters (0-arg, `(wallet)`, `(agentId)`), and prints MINT CANDIDATES with guessed args, calldata, an eth_call sim and a ready `fire:` command with `--start` taken from the start getter when found (`START HINT`).
   - Read: start time, free left, price, per-wallet limit, `agentIdOf(wallet)`.
   - Arg guesses: inviter/ref → 0x0 unless the user gave one; agentId/id → `$agentId` (tokenId = uint256(keccak256(handle)) from registry 0x60B9262456dE011F7d15a54CdD8c48bAaa8B022F); qty → 1; deadline → `$now+1800`; minTokens → 0.
   - Args that change at open (`expectedStart`, `totalMinted+1`, `nextId`) → use dynamic args so they are re-read right before every preview: `{"getter":"totalMinted()","add":1}`, `{"getter":"saleStart()"}`, `"$now+1800"`, `"$agentId"`, `"$wallet"`.
   - A sim before start usually reverts `NotStarted` (fine). `SoldOut`/`FreeGone`/`AlreadyTaken`/`AgentIdRequired` → stop and tell the user.
2. **Rehearse (always, ~15s):** same command with `--dry` and `--start` 10s ahead. It does everything up to preview and stops. Add `--gateSim` when the call is already mintable, so eth_call OK before start is ignored and the rehearsal shows the real timed path (3 runs 2026-11-11: clock trigger T+0.05s, head T+0.17–0.50s, previewOk T+0.62–0.76s → with measured execute 0.68s and inclusion 0.77s that is broadcast ≈T+1.3–1.5s, included ≈T+2.1–2.2s; add ≈0.4s if the backend's node sees the opening block one preview later). A preview `351805 sim failed` → wait is the normal pre-open result; `ok` means the call is already mintable. Check the `call = ...` line decodes to the intended function and args.
3. **Fire:** run in the background (Shell `run_in_background` / `block_until_ms: 0`) so the chat stays responsive, then report the log path:
   ```bash
   cd "$SKILL_DIR"
   # free mint at 23:00 WIB
   ./fastmint.sh fire --to 0xSALE --data 0x195ad114 --start 23:00 --label feg_free
   # signature encoding, static args
   ./fastmint.sh fire --to 0xSALE --sig "claimFreeShare()" --start 23:00
   # dynamic args (Agent ID + deadline re-read at every preview)
   ./fastmint.sh fire --to 0xSALE --sig "mintFree(uint256,uint256,uint256,uint256,address)" --args '["$agentId","1","0","$now+1800","0x0000000000000000000000000000000000000000"]' --start 21:00
   # arg that must equal a counter at open
   ./fastmint.sh fire --to 0xSALE --sig "mint(uint256)" --args '[{"getter":"totalMinted()","add":1}]' --start 1794330000
   # paid (user said: 2 shares at 0.005 = 0.01 BNB)
   ./fastmint.sh fire --to 0xSALE --sig "buyWithBnb(uint256,address,uint256)" --args '[2,"0x0000000000000000000000000000000000000000",0]' --value 0.01 --maxValue 0.01 --start 23:00
   ./fastmint.sh fire ... --dry          # rehearsal, stops before execute;  --noPreview stops before preview
   ```
   What fire.js does: NTP clock sync → prechecks in parallel (CONNECTED, devMode, code at `--to`, balance ≥ value+gas, no lock, ABI for revert decoding) → waits (re-checks session at T-20s, re-ranks RPCs and re-syncs clock at T-10s) → at T-3s (`--lead`) opens WS heads and spins eth_call → previews on the triggers above → one execute → receipt → `TIMELINE` line with T+ offsets for trigger/preview/execute/broadcast/included.
   - Not-started reverts (NotStarted/NotOpen/NotLive/TooEarly/Paused…) and 351805 sim failures are retried until `--timeout` (600s). Unknown reverts are retried until start+`--grace` (10s). Terminal reverts (sold out, gone, already, agent id, not eligible, expired, payment low…) stop at once; before start only the hard ones (sold/gone/already/agent/eligible/expired/ended) count.
   - Guards on the preview that is executed: `--expectNft <n>` executes only if exactly n Erc721/Erc1155 from `--to` arrive in the wallet (use it whenever the user states how many NFTs they should get). Value/cap, allowance, authority and RISK checks are always on.
   - Tune: `--waitOn`/`--fatalOn <regex>`, `--once` (one preview, one execute), `--noEager`, `--clockFire -1` (no clock trigger), `--gasLimit` only if the user asked, `FASTMINT_RPCS=` / `FASTMINT_WS=` overrides.
   - No `--start` = fire now (for a mint that is already open). Live example 2026-11-11, Pocket Moons `mint(2)` free: eth_call OK +35ms → preview 564ms → execute 683ms → BROADCASTED at +1.2s → included +0.77s later. Total 2.0s from trigger to receipt.
   - Logs: `runs/<stamp>_<label>.log` (WIB + T+ offsets), preview/exec/receipt JSON beside it. `./fastmint.sh logs` tails the latest.
4. **Report:** tx hash, status, BscScan link, the TIMELINE line, what was received (re-run recon or read the getters), and the log path. If it stopped: the decoded revert and what it means.

## Troubleshooting
- **UNCONNECTED / session error / SSL_ERROR mid-fire:** stop. Tell the user. Only on their OK run `baw auth signin --json`, then `auth verify --qrCodeId <id>` after they approve in the Binance App.
- **Developer Mode off/expired (351802/351804):** user enables it in the Binance App, then re-run.
- **NotStarted forever / 351805 forever:** start time wrong? Compare contract getter vs site. Did the team move the start? `--timeout` long enough?
- **Sold out / FreeGone / FreeSoldOut:** terminal. Do not switch to a paid mint without the user's explicit "ok paid" + amount.
- **AgentIdRequired / NotEligible:** wallet has no Agent ID (`handleOf` empty) or the contract needs the id arg → pass `"$agentId"`.
- **AlreadyTaken / AlreadyClaimed:** this wallet or Agent ID already claimed. Done.
- **Inviter args:** 0x0 or the user's ref. Often bound on first mint and immutable, so ask if unsure. Never self-invite where forbidden.
- **PaymentLow / WrongValue:** value must equal price × qty (read the price getter). Re-confirm the amount with the user.
- **Preview RISK / 351803:** stop and show the risk text. Do not bypass.
- **PENDING_CONFIRMATION:** the user must approve in the Binance App. Do not resend.
- **Execute error / no receipt:** do NOT retry. `baw wallet tx-history --json` and `baw wallet tx-lock --json`, then report.
- **"gave up after N previews":** the backend kept failing simulation while eth_call said open → state mismatch between Binance's node and public RPCs, or args wrong. Check the preview JSON in `runs/`.
- **Slow / rate-limited RPC:** `FASTMINT_RPCS="https://rpc-bsc.48.club,https://bsc.rpc.blxrbdn.com,..."` replaces the pool. drpc/ankr/llamarpc public endpoints are rate-limited or need keys; not in the default pool.
- **Premium RPC with a key:** put it in `SKILL_DIR/.env` (git-ignored, mode 600, never in SKILL.md or logs): `FASTMINT_RPCS_EXTRA=https://...` and `FASTMINT_WS_EXTRA=wss://...`. The launcher sources `.env`; the endpoint is prepended to the pool and still auto-ranked, hosts are masked in logs. On this machine a QuikNode BSC endpoint is configured there (2026-11-11: 31ms, WS head delay median 0.45s vs 0.56s publicnode, no rate limit at 20 req/s or a 60-burst).
