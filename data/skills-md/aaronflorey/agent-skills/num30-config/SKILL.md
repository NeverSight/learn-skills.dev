---
name: num30-config
description: Write, debug, and explain Go configuration code using the github.com/num30/config library. Use this skill when the user asks to set up config structs, read from files/env vars/CLI flags, validate config, watch for changes, or use the num30/config package in Go applications.
source: local
license: MIT
---

This skill provides comprehensive knowledge of **num30/config** (`github.com/num30/config`), a declarative Go configuration library that reads config from YAML/JSON/TOML files, environment variables, and command-line flags in a single call.

## Quick Reference

**Install:**
```sh
go get github.com/num30/config
```

**Minimal usage:**
```go
import "github.com/num30/config"

type Config struct {
    Host string `default:"localhost" validate:"required"`
    Port int    `default:"8080"`
}

func main() {
    var cfg Config
    err := config.NewConfReader("myapp").Read(&cfg)
    if err != nil {
        panic(err)
    }
}
```

## Configuration Sources & Priority

Values are merged in this order (highest priority wins):
1. **Command-line flags** (`--host=localhost`)
2. **Environment variables** (`HOST=localhost`)
3. **Config file** (`myapp.yaml`)
4. **Struct tag defaults** (`default:"localhost"`)

## Struct Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `default:"val"` | Default value | `default:"localhost"` |
| `validate:"rule"` | Validation rule (go-playground/validator) | `validate:"required"` |
| `flag:"name"` | Override CLI flag name | `flag:"debug"` |
| `envvar:"NAME"` | Override env var name | `envvar:"DB_PASS"` |
| `usage:"text"` | Flag usage/help text | `usage:"enable debug logging"` |
| `mapstructure:",squash"` | Squash embedded struct fields to parent level | see below |

## ConfReader Builder API

```go
config.NewConfReader("myapp")             // create reader (config name = file name + env prefix base)
    .WithSearchDirs("/etc/conf", "./")    // override config file search dirs (default: home + current dir)
    .WithPrefix("MYAPP")                 // prefix for env vars: MYAPP_DB_HOST
    .Read(&cfg)                          // read and populate struct (returns error)
```

**Watch for live config changes:**
```go
reader := config.NewConfReader("myapp")
err := reader.Read(&cfg)

mutex := reader.Watch() // call AFTER Read(); panics if called before

// thread-safe access:
mutex.RLock()
val := cfg.SomeField
mutex.RUnlock()
```

## Config File

- File name: `<configName>.yaml` (or `.json`, `.toml`, `.hcl`, `.ini`, `.env`, `.properties`)
- Search order: home directory, then current directory (override with `WithSearchDirs`)
- Field name mapping: camelCase → lower camelCase YAML key

```yaml
# For struct field DB.DbName:
db:
  dbName: "mydb"
```

## Environment Variables

- Default pattern: `FIELD_PATH` with dots replaced by `_`, uppercased
  - `App.Server.Port` → `APP_SERVER_PORT`
- With prefix: `NewConfReader("x").WithPrefix("MYAPP")` → `MYAPP_APP_SERVER_PORT`
- Override with `envvar` tag: `Password string \`envvar:"DB_PASS"\`` → reads from `DB_PASS`

## Command-Line Flags

- Default pattern: lowercase dotted path with `--` prefix
  - `App.Server.Port` → `--app.server.port=8080`
- Boolean flags: pass flag alone (no value needed): `--verbose`
- Override with `flag` tag: `Debug bool \`flag:"debug"\`` → `--debug`
- Slices: repeat the flag: `--slice a --slice b`
- Byte slices: base64-encoded: `--bytes dGVzdA==`

## Complete Example

```go
package main

import (
    "fmt"
    "time"
    "github.com/num30/config"
)

type Config struct {
    GlobalConfig `mapstructure:",squash"` // squash: fields promoted to top level
    Debug        bool
    DB           DatabaseConfig
    DefaultVal   string   `default:"default value"`
    Tags         []string `default:"[\"a\",\"b\"]"`
}

type GlobalConfig struct {
    Verbose bool `flag:"verbose" usage:"enable verbose logging"`
}

type DatabaseConfig struct {
    Host     string        `default:"localhost" validate:"required"`
    Password string        `validate:"required" envvar:"DB_PASS"`
    DbName   string        `default:"mydb"`
    Username string        `default:"root"`
    Port     int           `default:"5432"`
    Timeout  time.Duration `default:"30s"`
}

func main() {
    var cfg Config
    err := config.NewConfReader("myapp").
        WithSearchDirs("/etc/myapp", "./").
        WithPrefix("MYAPP").
        Read(&cfg)
    if err != nil {
        panic(err)
    }
    fmt.Printf("%+v\n", cfg)
}
```

## Squash Embedding

Use `mapstructure:",squash"` on an embedded struct to promote its fields to the parent level in config files and env vars:

```go
type GlobalConfig struct { Verbose bool }

type AppConfig struct {
    GlobalConfig `mapstructure:",squash"` // access as `verbose`, not `globalConfig.verbose`
    Name string
}
```

Config file: `verbose: true` (not `globalConfig.verbose: true`)
Env var: `VERBOSE=true` (not `GLOBAL_CONFIG_VERBOSE=true`)

## Supported Go Types

All primitive types are supported as config fields:
`bool`, `int`/`int8`/`int16`/`int32`/`int64`, `uint`/`uint8`/`uint16`/`uint32`/`uint64`, `float32`/`float64`, `string`, `[]string`, `[]byte` (base64 in flags/env), `time.Duration`

## Validation

Uses `go-playground/validator` tags on struct fields:

```go
type Config struct {
    Host  string `validate:"required"`
    Port  int    `validate:"min=1,max=65535"`
    Email string `validate:"required,email"`
}
```

`Read()` returns a validation error if constraints are violated. See [validator docs](https://github.com/go-playground/validator#baked-in-validations) for full tag list.

## Built-in Config Structs (lib package)

```go
import "github.com/num30/config/lib"

type Config struct {
    DB lib.PostgresqlDb // provides Host, Password, DbName, Username, Port, SslEnabled with sane defaults
}

// Get connection string:
connStr := cfg.DB.GetConnString()
// → "host=localhost user=postgres password=pass database= port=5432 sslmode=disable"
```

`lib.PostgresqlDb` defaults: `Host:"localhost"`, `Password:"pass"`, `Username:"postgres"`, `Port:5432`, `SslEnabled:false`

## Slices

```go
type Config struct {
    Slice []string
}
```

| Source | Format |
|--------|--------|
| Env var | `SLICE=a,b,c` |
| Config file | `slice: ["a", "b", "c"]` |
| CLI flags | `--slice a --slice b` |

## Error Handling

`Read()` returns errors for:
- Nil or non-pointer config struct
- Config file parse failures (`"failed to unmarshal struct"`)
- Default value failures (`"failed to set default values"`)
- Validation failures (`"validation error: Key: '...' Error:..."`)

`Watch()` panics if called before `Read()`.

## Additional References

- [references/api.md](references/api.md) — Full API reference
- [references/examples.md](references/examples.md) — Real-world usage examples
