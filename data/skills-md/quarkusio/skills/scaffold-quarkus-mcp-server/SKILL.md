---
name: scaffold-quarkus-mcp-server
description: Scaffold a new Quarkus MCP server project with greeting tools, integration tests, and README. Use when the user wants to create, scaffold, or generate a Quarkus MCP server, mentions "quarkus mcp", "quarkus mcp server", "quarkiverse mcp", or asks to generate a Quarkus project with MCP tools.
---

# Create Quarkus MCP Server

Scaffold a complete Quarkus MCP server project using the latest LTS Quarkus release and the
`quarkus-mcp-server` Quarkiverse extension.

## Prerequisite

- **JDK:** `21`
- **Maven:** `3.9`

## Fixed versions (do not change without re-verifying Maven Central)

- **Quarkus platform:** `3.40.1` (LTS, community maintenance until 2027-09-30)

---

## Step 1 — Gather project coordinates

Use `ask_followup_question` to collect:
- **groupId** — e.g. `org.acme`
- **artifactId** — e.g. `my-mcp-server`
- **version** — default `1.0.0-SNAPSHOT`
- **Target directory** — where to create the project (default: current workspace root)
- **Transport** — `stdio` (default) or `http`
  - `stdio`: the MCP server communicates over standard input/output. Packaged as an uber-jar. Best for CLI-based MCP clients (Claude Desktop, IBM Bob, etc.).
  - `http`: the MCP server communicates over HTTP/SSE. Packaged as a standard fast-jar. Best for web-based or network MCP clients.

---

## Step 2 — Bootstrap via code.quarkus.io REST API

Download the project skeleton from the `code.quarkus.io` REST endpoint.
The `e` parameter selects extensions; `nc=true` skips starter code; `S` picks
the Quarkus LTS stream.

Derive the following from the **Fixed versions** and **Prerequisite** sections above:
- `<quarkus-stream>` — strip the patch from the Quarkus platform version (e.g. `3.40.1` → `3.40`)
- `<jdk>` — the JDK version from Prerequisites

**If transport is `stdio`:**
```bash
curl -sSL -o /tmp/<artifactId>.zip \
  "https://code.quarkus.io/api/download?S=io.quarkus.platform:<quarkus-stream>&j=<jdk>&b=MAVEN&nc=true&g=<groupId>&a=<artifactId>&v=<version>&e=io.quarkiverse.mcp:quarkus-mcp-server-stdio"
```

**If transport is `http`:**
```bash
curl -sSL -o /tmp/<artifactId>.zip \
  "https://code.quarkus.io/api/download?S=io.quarkus.platform:<quarkus-stream>&j=<jdk>&b=MAVEN&nc=true&g=<groupId>&a=<artifactId>&v=<version>&e=io.quarkiverse.mcp:quarkus-mcp-server-http"
```

Then extract the archive into the target directory:

```bash
unzip -o /tmp/<artifactId>.zip -d <target-directory>
```

The generated project already includes:
- Quarkus BOM (`io.quarkus.platform:quarkus-bom` at the fixed Quarkus platform version)
- MCP server BOM (managed via the platform)
- The chosen transport dependency (`quarkus-mcp-server-stdio` or `quarkus-mcp-server-http`)
- `quarkus-junit` (test)
- Maven wrapper, Dockerfiles, Surefire & Failsafe plugins

---

## Step 3 — Patch `pom.xml`

Open `pom.xml` and apply the following:

1. **Add MCP test utilities**:
   In `<dependencies>`, add:
   ```xml
   <dependency>
       <groupId>io.quarkiverse.mcp</groupId>
       <artifactId>quarkus-mcp-server-test</artifactId>
       <scope>test</scope>
   </dependency>
   ```

2. **If transport is `stdio`** — enable über-jar packaging and ITs:
   In `<properties>`, ensure:
   ```xml
   <quarkus.package.jar.type>uber-jar</quarkus.package.jar.type>
   <skipITs>false</skipITs>
   ```

3. **If transport is `http`** — no additional properties needed (default fast-jar packaging, ITs skipped).

---

## Step 4 — Create the `GreetingTools` class

Write the file at `src/main/java/<groupId-as-path>/GreetingTools.java`.
Use the reference file at `reference/GreetingTools.java` as the exact template —
replace the package declaration to match the actual `groupId`.

Use `write_file` to create the file. Do **not** alter the `@Tool` or `@ToolArg` annotations.

---

## Step 5 — Create the test class

The reference files are organized by transport under `reference/stdio/` and `reference/http/`.
Use the subfolder matching the transport chosen in Step 1.

**If transport is `stdio`:**

Write the file at `src/test/java/<groupId-as-path>/CheckToolsIT.java`.
Use the reference file at `reference/stdio/CheckToolsIT.java` as the exact template —
replace the package declaration and update the runner jar filename:

```java
.setCommand("java", "-jar", "target/<artifactId>-<version>-runner.jar")
```

This is a Failsafe integration test — it launches the über-jar as a subprocess and calls both
`greetHello` and `greetBye` via the MCP stdio protocol.

**If transport is `http`:**

Write the file at `src/test/java/<groupId-as-path>/CheckToolsTest.java`.
Use the reference file at `reference/http/CheckToolsTest.java` as the exact template —
replace the package declaration to match the actual `groupId`.

This is a `@QuarkusTest` — it starts the Quarkus application and calls both `greetHello` and
`greetBye` via the MCP Streamable HTTP endpoint using `McpStreamableTestClient`.

Use `write_file` to create the file.

---

## Step 6 — Create `README.md`

Use the transport-specific README template:
- **stdio**: `reference/stdio/README.md`
- **http**: `reference/http/README.md`

Replace all `{{artifactId}}` and `{{version}}` placeholders with the actual values collected
in Step 1. Write the file to the project root.

---

## Step 7 — Build the project

**If transport is `stdio`:**
```bash
cd <artifactId> && mvn package -DskipTests
```
Confirm `target/<artifactId>-<version>-runner.jar` exists after the build.

**If transport is `http`:**
```bash
cd <artifactId> && mvn package
```

---

## Step 8 — Run tests

**If transport is `stdio`:**
```bash
mvn verify
```
`CheckToolsIT` will launch the über-jar as a subprocess and call both `greetHello` and
`greetBye` via the MCP stdio protocol.

**If transport is `http`:**
```bash
mvn test
```
`CheckToolsTest` will start the Quarkus application and call both `greetHello` and
`greetBye` via the MCP SSE endpoint.

---

## Step 9 — Register with an MCP client

Present the user with the registration snippets for their preferred client.

**If transport is `stdio`:**

### IBM Bob (workspace `.bob/mcp.json`)

```json
{
  "mcpServers": {
    "<artifactId>": {
      "command": "java",
      "args": ["-jar", "<absolute-path>/target/<artifactId>-<version>-runner.jar"]
    }
  }
}
```

Write this to `.bob/mcp.json` (read-then-merge if the file already exists).

### Claude Desktop

```json
{
  "mcpServers": {
    "<artifactId>": {
      "command": "java",
      "args": ["-jar", "<absolute-path>/target/<artifactId>-<version>-runner.jar"]
    }
  }
}
```

On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

**If transport is `http`:**

### SSE endpoint

The MCP server is available at:
```
http://localhost:8080/mcp/sse
```

Start the application first:
```bash
cd <artifactId> && mvn quarkus:dev
```

### IBM Bob (workspace `.bob/mcp.json`)

```json
{
  "mcpServers": {
    "<artifactId>": {
      "url": "http://localhost:8080/mcp/sse"
    }
  }
}
```

### Claude Desktop

```json
{
  "mcpServers": {
    "<artifactId>": {
      "url": "http://localhost:8080/mcp/sse"
    }
  }
}
```

---

## Step 10 — Confirm

Tell the user:
- The project is ready at `<target-directory>/<artifactId>/`
- Transport: `stdio` or `http`
- Build command: `mvn package -DskipTests` (stdio) or `mvn package` (http)
- Test command: `mvn verify` (stdio) or `mvn test` (http)
- The MCP config has been written / show them the snippet to paste
- Available tools: `greetHello(name)` and `greetBye(name)`
