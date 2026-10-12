---
name: adder
description: Use when adding or editing config structs/YAML for projects that use lwlee2608/adder. Prevents silent zero-value binding from snake_case keys, env var mismatches, and missing defaults.
user-invocable: true
---

# Working with lwlee2608/adder

Adder reads YAML into Go structs and overlays env vars. It does **case-insensitive** key matching only — it does **not** fold snake_case ↔ CamelCase. Every rule below exists to avoid fields silently binding to their zero value.

## Rules

1. **Prefer YAML keys that already match the lowercased Go field name.** Adder looks up `strings.ToLower(field.Name)`, so a field `SessionTtl` is resolved against the YAML key `sessionttl`. Both lowercase and camelCase keys work because adder lowercases both sides — camelCase is just easier to read.

   ```yaml
   # good — matches field name when lowercased
   auth:
     username: admin
     sessionTtl: 24h
   ```

   ```go
   type AuthConfig struct {
       Username   string
       SessionTtl time.Duration  // no tag required
   }
   ```

   **Idiomatic Go vs. tag-free binding is a tension.** Go style says initialisms should be all-caps (`SessionTTL`). But `strings.ToLower("SessionTTL")` is `"sessionttl"`, which forces either an ugly YAML key (`sessionttl: 24h`) or a `mapstructure` tag. Pick your poison: idiomatic Go + tag, or non-idiomatic field name + no tag. This skill leans toward the latter to minimize tags, but either is defensible — be consistent within a project.

   This applies recursively at every nesting level — `auth.session.ttl` resolves each segment the same way.

2. **Prefer not to use snake_case in YAML.** A snake_case key like `session_ttl` will **never** bind to `SessionTTL` automatically — adder compares `sessionttl` to `session_ttl` and finds no match, so the field silently stays at its zero value (e.g. `time.Duration(0)`, which means "expires immediately" for TTLs). If you must use snake_case for readability, every such field requires an explicit `mapstructure` tag:

   ```go
   // only if you insist on snake_case YAML
   SessionTTL time.Duration `mapstructure:"session_ttl"`
   ```

   Prefer rule 1 over this — fewer tags, fewer ways to forget one.

3. **Put defaults in `application.yml`, not in code.** `application.yml` is the canonical source of default values. Code should not paper over missing config with hard-coded fallbacks (e.g. `if cfg.SessionTTL == 0 { cfg.SessionTTL = 24*time.Hour }`) — that hides genuine misconfiguration. If a value is required, validate at startup and panic with a clear message.

   **List every field, with local dev values.** `application.yml` is the config for running locally and the maintainer's bird's-eye view of all available config. Give every field a value that works for local dev (`localhost`, a docker-compose password, `10s`); env vars override them per deployment. Only secrets with no safe dev value (third-party API keys) get `""`. Never commit real credentials. If a non-string field truly has no default, use a bare key (`timeout:`), not `""` — `""` fails to parse for `time.Duration`.

   Keep `application.yml` free of comments — with every field listed, per-field comments drown out the config.

   ```yaml
   auth:
     sessionTtl: 24h
     smtp:
       host: localhost
       port: 1025
       password: ""
       from: dev@localhost
   ```

   **If the code calls `godotenv.Overload()`, document overrides in `.env.example`.** List the env vars a deployment needs to set — secrets and anything whose dev default is wrong in prod — with a comment explaining each. Use placeholder values only. Without `godotenv.Overload()`, don't add `.env` files.

   ```sh
   # SMTP relay for outgoing auth emails
   AUTH_SMTP_HOST=smtp.example.com
   AUTH_SMTP_PORT=587
   # App password from the mail provider, not the account password
   AUTH_SMTP_PASSWORD=changeme
   AUTH_SMTP_FROM=no-reply@example.com
   ```

4. **Rely on `AutomaticEnv()` for the standard env var pattern.** A *keyPath* is the dotted path adder uses internally — struct field `Auth.SessionTtl` becomes keyPath `auth.sessionttl`. With `SetEnvKeyReplacer(strings.NewReplacer(".", "_"))` and `AutomaticEnv()`, adder derives the env var as `strings.ToUpper(keyPath)` with dots replaced by underscores. Don't add `BindEnv` calls for env vars that already follow this pattern — they're noise.

   ```
   keyPath: openrouter.apikey  →  env: OPENROUTER_APIKEY   (auto, no BindEnv needed)
   keyPath: db.url             →  env: DB_URL              (auto)
   ```

5. **Use `BindEnv` only when the env var name diverges from the auto pattern.** Common reason: an established external env name (e.g. `OPENROUTER_API_KEY` with an underscore between `API` and `KEY`) doesn't match the auto-derived `OPENROUTER_APIKEY`.

   ```go
   // Only because the external name is OPENROUTER_API_KEY, not OPENROUTER_APIKEY
   _ = adder.BindEnv("openrouter.apikey", "OPENROUTER_API_KEY")

   // Don't write this — DB_URL is already automatic from keyPath db.url
   // _ = adder.BindEnv("db.url", "DB_URL")
   ```

   If you can rename the env var to match the auto pattern, do that instead and drop the `BindEnv`.

6. **Address slice elements by index in env vars.** A slice field's keyPath gains the element index: `Clients []ClientConfig` → `clients.0.token` → `CLIENTS_0_TOKEN`. An index past the end of the list in `application.yml` appends a new element, so a list can come entirely from env. Appending stops at the first missing index, and an unindexed key (`CLIENTS=...`) is ignored. An unindexed key for a field inside an element (`CLIENTS_TOKEN=...`) still applies to every existing element, with the indexed key winning where both are set.

   ```
   CLIENTS_1_TOKEN=t9      → clients[1].token    (override)
   CLIENTS_2_NAME=baz      → clients[2] appended
   CLIENTS_2_AUTH_ID=id-2  → clients[2].auth.id
   PATHS_0=/one            → paths[0], no yaml entry needed
   ```

   For secrets inside a fixed-shape list, use `${NAME}` placeholders instead of `""` — the yaml still documents the shape, and named env vars survive list reordering where indexed ones don't. Use them only for string secrets: an unset var expands to empty, and there's no `${NAME:-default}` syntax. If the project has a `.env.example`, list the `${NAME}` vars there. Reach for indexed env vars when the number of elements varies per environment.

7. **Co-locate config structs with the package they configure.** Each package owns its own config type (`internal/auth/config.go` → `auth.Config`, `internal/db/config.go` → `db.Config`). The cmd-level `Config` is just composition.

   ```go
   // cmd/myapp/config.go
   type Config struct {
       Auth auth.Config
       DB   db.Config
   }
   ```

   Adder binds either way — this is for code organization: package owns its fields, masking tags, and any `Enabled()`/`Validate()` helpers, and `cmd/<app>/config.go` stays short. Config types used only by cmd wiring (e.g. `LogConfig`) can stay in `cmd/<app>/`.

## Verification procedure

After adding or changing a config field (these checks apply at every nesting level — verify the deepest field, not just the top-level struct):

1. **Lowercase-match check** — does `strings.ToLower(fieldName)` equal the YAML key exactly? If not, you need a `mapstructure` tag, or you should rename the YAML key.
2. **Default check** — does the field have a key in `application.yml` with a working local dev value? Run the binary with no env overrides and confirm the field has the expected value. Don't rely on memory — log it, e.g. `log.Printf("%+v", cfg)`.
3. **Env override check** — if the field is meant to be env-overridable, set the auto-derived env var (`UPPER_CASE_WITH_UNDERSCORES`) and confirm it overrides the YAML default. Same rule: log the loaded value, don't assume.
4. **Zero-value trap** — for `time.Duration`, `int`, `float64`, or `bool` fields, a binding miss looks identical to "configured as 0/false". Always test a non-zero default actually loads.

## Common mistakes to watch for

- **Adding a multi-word field without a `mapstructure` tag and using snake_case YAML.** This is the #1 footgun: the field silently binds to zero. `SessionTTL` + `session_ttl:` → `0`, not `24h`.
- **Adding `BindEnv` for env vars that already follow the auto pattern.** Redundant and obscures which bindings are actually needed.
- **Omitting env-only fields from `application.yml`.** They still bind from env, but maintainers reading the yaml can't see they exist.
- **Using prod values or `""` as defaults.** `application.yml` should run locally as-is; reserve `""` for secrets with no safe dev value.
- **Commenting `application.yml`.** Keep it bare; if the project uses `godotenv.Overload()`, put explanations next to the env vars in `.env.example`.
- **Hiding misconfiguration with code defaults.** A `if cfg.X == 0 { cfg.X = default }` masks the real bug (the YAML key didn't bind). Fix the binding instead.
- **Expecting an unindexed env var to replace a whole list.** `CLIENTS=...` does nothing; slice overrides must be indexed (`CLIENTS_0_NAME`).
- **Assuming case-insensitive means snake-aware.** It doesn't — `caseInsensitiveLookup` only normalizes letter case, not separators.
- **Forgetting that `time.Duration` is `int64`.** A missing duration looks like `0s`, which most code treats as "no timeout" or "expired" — almost always wrong.
