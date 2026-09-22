---
name: frida-codeshare-search
description: Search Frida CodeShare with curl, extract project metadata and script source, review snippets, and turn scripts into local agents or commands.
---

# Frida CodeShare Search

Use this skill when a user wants to find, inspect, download, adapt, or run Frida CodeShare scripts.

## Rules

- Confirm authorization and target scope before running third-party instrumentation.
- Treat CodeShare scripts as reconnaissance first. Read the source before running it.
- Prefer local review with `-l script.js` after extraction; use `frida --codeshare` only when the user accepts fetching and running public code directly.
- Verify the script matches the target platform, app version, library names, symbols, and Frida version before changing behavior.

## Search With Curl

Fetch the search page with URL-encoded query parameters:

```bash
curl -fsSL --get --data-urlencode "query=instagram" "https://codeshare.frida.re/search/" -o codeshare-search.html
```

Parse the result cards:

```bash
python3 /path/to/frida-codeshare-search/scripts/codeshare_extract.py search codeshare-search.html
```

The parser reports title, author, URL, likes, views, and description. Pick candidates by platform fit, recency/version in title, specific framework coverage, and enough source clarity to audit.

## Extract A Project Script

Fetch the project page:

```bash
curl -fsSL "https://codeshare.frida.re/@Eltion/instagram-ssl-pinning-bypass/" -o codeshare-project.html
```

Extract the embedded `projectSource` into a local script:

```bash
python3 /path/to/frida-codeshare-search/scripts/codeshare_extract.py project codeshare-project.html -o agent.js
```

Then inspect before execution:

```bash
sed -n '1,220p' agent.js
```

## Run Options

Run a reviewed local script:

```bash
frida -U -f com.instagram.android -l agent.js --no-pause
```

Run directly through CodeShare when direct execution is acceptable:

```bash
frida -U --codeshare Eltion/instagram-ssl-pinning-bypass -f com.instagram.android --no-pause
```

If the CodeShare page shows a placeholder like `${projectSlug}`, use the slug from the project URL.

## Adaptation Checklist

- Android Java hooks are inside `Java.perform()` and overloads are explicit.
- Native hooks wait for the module before resolving exports or symbols.
- iOS hooks check `ObjC.available` and confirm class/selectors or symbols exist.
- Broad SSL/root/integrity bypass bundles are reduced to the hooks that actually fire.
- Logs prove which hook changed behavior; failures include the exact command, app version, Frida version, and target architecture.

## References

- Official Frida CLI docs: https://frida.re/docs/frida-cli/
- Official Frida JavaScript API docs: https://frida.re/docs/javascript-api/
- Frida CodeShare: https://codeshare.frida.re/
- OWASP MASTG Frida CodeShare tool note: https://mas.owasp.org/MASTG/tools/generic/MASTG-TOOL-0032/
