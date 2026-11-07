---
name: share-act-config
description: Use when encoding, validating or structurally repairing a Share & Act rule JSON file against an approved App contract, then delivering an exact checked file with a working copy-content helper. Not for interpreting business tasks or executing integrations.
---

# Share & Act configuration compliance

This skill is task-neutral. Its responsibility is JSON encoding, structural compliance, version compatibility and verified file delivery.

Treat template.instruction as opaque caller-provided content. Check its encoding, size, variable syntax and renderability, not its business meaning. Do not invent, replace or specialize the user's intended behavior. Do not connect services, choose destinations or execute the configuration. Service setup, business decisions, factual claims and permissions remain the caller's responsibility and are not certified by this validator.

## 1. Load the current skill and contract

Before each validation run, use `npx skills check` and inspect its output; exit 1 can mean updates are available. Update only this skill with `npx skills update share-act-config -y`, then reread its contract. A failed update check or incompatible contract blocks a claim of current validated output.

Use the native loader if available. Otherwise read this file and its required references directly from the installer-reported installation directory. This is a file-based workflow, not native registration. Run bundled scripts from that skill directory. Node.js 20+ and Java 17+ are required by the validator; missing tools must be reported, not replaced by mental validation.

Read `contracts/current.json` and [the envelope contract](references/envelope.md). Obtain the exact selected Bot ID, App language and approved validation-contract identity from a trusted caller. Do not infer them from old messages, fixtures or the bundle merely to bypass a mismatch.

Use a separate context file:

```json
{
  "contract_id": "THE_APPROVED_APP_VALIDATION_CONTRACT_ID",
  "bot_id": "THE_CURRENT_SELECTED_BOT_ID",
  "language": "en"
}
```

The language code must be `en` or `zh-CN`. This skill's documentation, tooling and fixtures are English. A context can include non-secret App-compatible `connection` metadata; without it the oracle uses synthetic metadata only. Neither mode verifies live account availability or authorization.

Unknown versions, source drift, stale artifacts or unapproved contracts fail closed. See [upgrade maintenance](references/upgrades.md). Never guess a migration or substitute a different hash.

## 2. Encode the caller's intended configuration

Receive an existing candidate JSON or the caller's intended rule fields. If required structural input is missing, request it. Do not derive a new business task to fill gaps.

- Return exactly the supported envelope shape, not a full configuration document or runtime request.
- Use the trusted Bot ID and language. Keep explicit safe defaults and exact template references.
- Preserve the caller-provided instruction and intended conditions. Structural repair must not silently change what the rule does.
- Serialize with a JSON library rather than manually concatenating quoted strings. Newlines and quotes inside strings must be escaped. URL fields must be plain strings, not chat-generated link wrappers.
- Use a sample that matches the supplied conditions and the protocol's allowed resource identifiers. Resource names are validation metadata, not a business-template recommendation.
- Never include credentials or device authorization grants. Examples are generic protocol fixtures; their IDs are not current Bot context.

## 3. Validate the exact candidate file

```bash
node scripts/validate.mjs "/absolute/path/draft.json" --context "/absolute/path/context.json"
```

When the matching App source checkout is available, add `--source "/absolute/path/ShareAct-Android"`.

Inspect the JSON report and exit status. Validation covers the approved artifact, canonical envelope policy, actual App import diagnostics/decoder, sample matching, template rendering and core request construction. It does not execute the instruction or judge whether its business intent is correct. Supplementary case folding uses ICU4J; device-specific Unicode behavior may need on-device verification.

Repair format/structural errors while preserving the intended content, then rerun on the exact final bytes. After three failed repair attempts, report the unresolved diagnostic. Do not fabricate success, remove requested behavior to silence errors, or describe an unvalidated draft as passed.

## 4. Finalize and provide a real copy button

```bash
node scripts/finalize.mjs "/absolute/path/draft.json" --context "/absolute/path/context.json" --out "/absolute/path/config.json"
```

Choose a fresh output filename. This mandatory gate validates before and after copying, verifies file identity/bytes, and writes:

- `config.json`: the exact checked configuration.
- `config.json.page.tsx`: source for a native Grok Bot Page using `grok/canvas` (`Page`, `Section`, `Text`, `Button`, `useState`, `useGrokTheme`). It embeds the checked text as a safely encoded string; no object reserialization or browser cryptography gate is involved.
- `config.json.validation.json`: a separate hash receipt, never part of the configuration envelope.

Attach the finalized JSON unchanged. Then use Grok Bot's actual native Page creation/update tool with the generated TSX source, rather than attaching HTML or only returning a TSX download. Keep the Page private to the current user/Bot; do not publish configuration data publicly. Preserve the source's embedded text unchanged. Obtain a real created Page reference/link and verify that it rendered a Button before reporting that the copy Page is available. Do not invent a tool name, link, native control or successful publication.

The Page attempts synchronous textarea selection plus `document.execCommand("copy")` during the click gesture only when textarea.value preserves the original text; CR/CRLF normalization skips this path. If that fails, it awaits `navigator.clipboard.writeText`; only a true result shows "Copied". Both failures show selectable JSON and an explicit manual-copy/import fallback. The local receipt says `native_page_created: false`: finalization produces source, not a hosted Page. Native Page creation must be confirmed separately. If the tool is unavailable, explain that limitation and provide the validated JSON attachment without pretending an ordinary HTML page is equivalent.

Do not edit, retype, pretty-print or wrap the JSON after finalization. Verify attachment bytes when supported. If file delivery is unavailable, report that limitation rather than presenting reformatted chat content as the checked file. The user can import the JSON or click the rendered native Page's copy button to paste the original text into the App.

## Scope of a passing result

Evidence binds the exact configuration, context and approved contract. It does not prove live Bot existence, plan capacity, OAuth, destinations, external tools or remote execution. App save-time state can still block a valid file. This skill only certifies configuration compliance within its tested contract.
