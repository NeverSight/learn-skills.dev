---
name: analyze-wpilog
description: Analyze WPILOG log files from FRC robots using the wpilog-parser library with TypeScript.
license: MIT
---

# wpilog-parser

WPILOG is the binary log format used by logging libraries in the FRC ecosystem. The wpilog-parser library makes it easy to read and analyze the log files using TS/JS.

## Creating a project

1. Init a project using `pnpm init` or similar
2. Add `wpilog-parser` as a dependency
3. Catalog the entries in the WPILOG file before deciding what to analyze

   ```sh
   pnpm wpilog catalog ./example.wpilog
   ```

   The default output is plaintext. Use `--json`, `--jsonl`/`--ndjson`, or `--csv` when another format is more useful.

## Analyzing logs

Use `parseDataLog` to parse DataLog bytes. Filter by `name` and narrow on `type`:

```ts
import { readFile } from 'node:fs/promises';
import { isDataRecord, parseDataLog, RecordType } from 'wpilog-parser';

const bytes = await readFile('./example.wpilog');

for (const record of parseDataLog(bytes)) {
	if (!isDataRecord(record)) continue;

	if (record.name === '/Robot/Intake/Voltage' && record.type === RecordType.Double) {
		console.log(record.timestamp, record.payload);
	}
}
```

### Decoding structs

```ts
import { parseDataLog, RecordType, structPayloadToJson } from 'wpilog-parser';

for (const record of parseDataLog(bytes)) {
	if (record.type === RecordType.Struct && record.name === '/Robot/Localization/EstimatedPose') {
		console.log(record.timestamp, structPayloadToJson(record.payload));
		// 18688018n {
		//   translation: { x: 10.289, y: 0.47 },
		//   rotation: { value: 1.5707961072652017 },
		// }
	}
}
```

### Strict mode

```ts
for (const record of parseDataLog(bytes, { strict: true })) {
	// throws on orphan data records instead of skipping
}
```

## Robot state cheatsheet

When DriverStation logging is on, every WPILOG has these `boolean` entries:

| Entry            | Meaning                                                             |
| ---------------- | ------------------------------------------------------------------- |
| `/DS:enabled`    | `true` while the robot is enabled (any mode).                       |
| `/DS:autonomous` | `true` during autonomous. `false` means teleop (unless `/DS:test`). |
| `/DS:test`       | `true` during test mode.                                            |
| `/DS:estop`      | `true` if e-stopped.                                                |

The mode flags (`autonomous`, `test`) reflect what the DS _would_ run if enabled, so check `/DS:enabled` together with them. Timestamps are microseconds (`bigint`).

### Tracking enable/mode durations

```ts
import { isDataRecord, parseDataLog, RecordType } from 'wpilog-parser';

type Mode = 'auto' | 'teleop' | 'test';
function modeOf(auto: boolean, test: boolean): Mode {
	if (test) return 'test';
	if (auto) return 'auto';
	return 'teleop';
}

let enabled = false;
let auto = false;
let test = false;
let enabledSince: bigint | null = null;
const totals = { auto: 0n, teleop: 0n, test: 0n };

for (const r of parseDataLog(bytes)) {
	if (!isDataRecord(r) || r.type !== RecordType.Boolean) continue;

	const wasEnabled = enabled;
	const prevMode = modeOf(auto, test);

	if (r.name === '/DS:enabled') enabled = r.payload;
	else if (r.name === '/DS:autonomous') auto = r.payload;
	else if (r.name === '/DS:test') test = r.payload;
	else continue;

	if (wasEnabled && (!enabled || modeOf(auto, test) !== prevMode)) {
		totals[prevMode] += r.timestamp - (enabledSince ?? r.timestamp);
		enabledSince = enabled ? r.timestamp : null;
	} else if (!wasEnabled && enabled) {
		enabledSince = r.timestamp;
	}
}

// Durations in microseconds; divide by 1_000_000n for seconds.
console.log(totals);
```
