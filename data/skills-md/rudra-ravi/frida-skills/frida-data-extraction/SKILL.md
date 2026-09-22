---
name: frida-data-extraction
description: Use Frida to observe and extract runtime data such as HTTP, headers, tokens, JSON, crypto values, preferences, SQLite, files, memory, and byte arrays.
---

# Frida Data Extraction

Use this skill when the goal is to observe runtime data rather than bypass a check.

## Rules

- Only extract data from systems the user is authorized to test.
- Avoid printing secrets into shared logs unless the user explicitly needs them.
- Prefer structured logs with redaction for tokens, cookies, passwords, and private keys.
- Copy pointer and retval data inside callbacks; Frida may recycle callback objects.

## Android Boundaries

```js
Java.perform(() => {
  const Base64 = Java.use("android.util.Base64");
  Base64.encodeToString.overload("[B", "int").implementation = function (bytes, flags) {
    const out = this.encodeToString(bytes, flags);
    console.log("Base64.encodeToString ->", out);
    return out;
  };
});
```

High-signal targets: request builders, JSON serializers, `SharedPreferences`, SQLite APIs, keystore wrappers, crypto APIs, WebView bridges, file I/O.

## iOS Boundaries

High-signal targets: `NSURLRequest`, `NSURLSession`, `NSJSONSerialization`, Keychain wrappers, `NSUserDefaults`, SQLite, CommonCrypto, file APIs, pasteboard.

## Native Buffers

```js
function dump(ptr, len) {
  if (ptr.isNull() || len <= 0) return;
  console.log(hexdump(ptr, { length: Math.min(len, 256), ansi: false }));
}
```

Use both hex and text only when the data is valid text. Binary crypto material often is not.

## Verification

- Logs are tied to a user action or request.
- The source and encoding of each value is clear.
- Sensitive values are redacted unless needed.
- The hook does not change the target behavior unless explicitly requested.

## References

- Frida JavaScript API: https://frida.re/docs/javascript-api/
- Frida messages: https://frida.re/docs/messages/
- OWASP MASTG Frida: https://mas.owasp.org/MASTG/tools/generic/MASTG-TOOL-0031/
