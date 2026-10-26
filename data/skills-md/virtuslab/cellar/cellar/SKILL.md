---
name: cellar
description: >
  Look up the public API of any JVM dependency (Scala 3, Scala 2, Java) from
  the terminal — type signatures, members, docs, and source as Markdown, no
  JAR unpacking needed. Use this skill whenever you need to call an unfamiliar
  library method, explore a package's types, or check a dependency's API.
  Prefer cellar over Metals MCP only for looking up external dependency APIs
  (`cellar get-external` vs Metals `inspect`/`get-docs`) — cellar needs no
  project import and queries any published Maven artifact.
---

# Cellar

Use cellar to look up the API of JVM dependencies instead of guessing or manually downloading, unpacking, and searching JAR files for type signatures.

## Prerequisites

Run `cellar --version` to verify cellar is on PATH. If not found, the user
needs to install it: https://github.com/VirtusLab/cellar#installation

## Project-aware commands (run from project root)

Query the current project's code and all its dependencies. Cellar auto-detects the build tool (Mill, sbt, scala-cli).

    cellar get [--module <name>] <fqn>       # single symbol (signature, members, docs)
    cellar list [--module <name>] <package>  # list symbols in a package or class
    cellar search [--module <name>] <query>  # case-insensitive substring search

- Mill/sbt projects: `--module` is required (e.g. `--module lib`, `--module core`)
- scala-cli projects: omit `--module`
- `--test`: query the test-scope classpath (sbt/scala-cli; for Mill, use the test module directly, e.g. `--module foo.test`)
- `--no-cache`: skip classpath cache, re-extract from build tool
- `--java-home <path>`: override JRE classpath
- `-l`, `--limit <N>`: max results for `list`/`search` (default: 50)
- `--hide-inherited`: show only members declared on the type itself (`get` commands)
- `--group-inherited`: group members by declaring type with section headers (`get` commands)
- `-v`, `--verbose` / `--debug`: diagnostics to stderr. Use when a symbol you expect is reported as
  not found: `--verbose` on the `get` commands lists which lookup strategies were tried, and
  `--debug` adds the resolved classpath and build-tool detection on any command.

## External commands (query arbitrary Maven coordinates)

Query any published artifact by explicit coordinate (`group:artifact:version`):

    cellar get-external <coordinate> <fqn>       # single symbol
    cellar list-external <coordinate> <package>  # list symbols
    cellar search-external <coordinate> <query>  # search by name
    cellar get-source <coordinate> <fqn>         # fetch source code
    cellar deps <coordinate>                     # dependency tree

- Coordinates must be explicit: `group:artifact_3:version` (no `::` shorthand)
- For sbt plugins, use the full Scala and sbt suffix: `group:artifact_2.12_1.0:version` (e.g. `org.scala-native:sbt-scala-native_2.12_1.0:latest`)
- For compiler plugins and other artifacts with full Scala version suffixes, use the full version: `group:artifact_3.3.8:version`
- Use `latest` as the version to resolve the most recent release
- `-r`, `--repository <url>`: extra Maven repository (repeatable), appended to the repositories
  configured under `maven.repositories` in `~/.cellar/cellar.conf` or `.cellar/cellar.conf`

## Workflow

1. **Don't know the package?** → `cellar search` / `cellar search-external`
2. **Know the package, not the type?** → `cellar list` / `cellar list-external`
3. **Know the type?** → `cellar get` / `cellar get-external`
4. **Need the implementation?** → `cellar get-source`

## Examples

```sh
# Look up a Scala 3 trait
cellar get-external org.typelevel:cats-core_3:2.10.0 cats.Monad

# Look up a Java class
cellar get-external org.apache.commons:commons-lang3:3.14.0 org.apache.commons.lang3.StringUtils

# List a package
cellar list-external io.circe:circe-core_3:0.14.6 io.circe

# Search for a method
cellar search-external org.typelevel:cats-core_3:2.10.0 flatMap

# Get source code
cellar get-source org.typelevel:cats-core_3:2.10.0 cats.Monad

# Dependency tree
cellar deps org.typelevel:cats-effect_3:3.5.4

# sbt plugin (use full Scala + sbt suffix)
cellar deps org.scala-native:sbt-scala-native_2.12_1.0:latest

# Project-aware (from a Mill project root)
cellar get --module lib cats.Monad
cellar list --module core cats
cellar search --module lib flatMap
```

## Example output

`cellar get-external --hide-inherited org.typelevel:cats-core_3:2.10.0 cats.Monad`

````markdown
## cats.Monad
```scala
trait Monad[F[_]] extends FlatMap[F] with Applicative[F]
```
**Supertypes:** cats.Applicative, cats.InvariantMonoidal, cats.FlatMap, cats.FlatMapArityFunctions, cats.Apply, cats.ApplyArityFunctions, cats.InvariantSemigroupal, cats.Semigroupal, cats.Functor, cats.Invariant, java.io.Serializable

Monad.
Allows composition of dependent effectful functions.
See: [[http://homepages.inf.ed.ac.uk/wadler/papers/marktoberdorf/baastad.pdf Monads for functional programming]]
Must obey the laws defined in cats.laws.MonadLaws.

**Origin:** cats.Monad
**Members:**
```scala
def iterateWhile[A](f: F[A])(p: A => Boolean): F[A]
def untilM[G[_], A](f: F[A])(cond: => F[Boolean])(implicit G: Alternative[G]): F[G[A]]
def ifElseM[A](branches: (F[Boolean], F[A])*)(els: F[A]): F[A]
def iterateUntilM[A](init: A)(f: A => F[A])(p: A => Boolean): F[A]
def map[A, B](fa: F[A])(f: A => B): F[B]
def whileM_[A](p: F[Boolean])(body: => F[A]): F[Unit]
def whileM[G[_], A](p: F[Boolean])(body: => F[A])(implicit G: Alternative[G]): F[G[A]]
def untilM_[A](f: F[A])(cond: => F[Boolean]): F[Unit]
def iterateUntil[A](f: F[A])(p: A => Boolean): F[A]
def iterateWhileM[A](init: A)(f: A => F[A])(p: A => Boolean): F[A]
```
**Companion members:**
```scala
trait Ops[F[_], A] extends Serializable
object ops
def apply[F[_]](implicit instance: Monad[F]): Monad[F]
trait ToMonadOps extends Serializable
object nonInheritedOps extends ToMonadOps
trait AllOps[F[_], A] extends Ops[F, A] with FlatMap.AllOps[F, A] with Applicative.AllOps[F, A]
```
````

`**Supertypes:**` lists every ancestor in linearization order, the order member lookup follows.

### Choosing member output

- Default: every member callable on the type, inherited ones included. Use it to find what you can call.
- `--hide-inherited`: only what the type itself declares. Use it for what a subtype adds, or when the full output is too large.
- `--group-inherited`: members under `// Declared on` / `// Inherited from` headers. Use it when you need the declaring parent, e.g. to read its docs or find what to override.

## When Metals MCP is also available

Prefer cellar **only** for external dependency API lookups (`cellar get-external` vs Metals `inspect`/`get-docs`): cellar requires no project import and works with any published Maven coordinate. For all other tasks — goto definition, find references, rename, diagnostics, compilation — use Metals.

## Output

- **stdout**: Markdown — ready to consume directly
- **stderr**: diagnostics (warnings, truncation notices)
- **Exit 0**: success, **Exit 1**: error
