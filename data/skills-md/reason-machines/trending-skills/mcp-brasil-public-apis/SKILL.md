---
name: mcp-brasil-public-apis
description: MCP Server connecting AI agents to 28 Brazilian public APIs covering economy, legislation, transparency, judiciary, elections, environment, health, and more
triggers:
  - "use mcp-brasil"
  - "connect to Brazilian government APIs"
  - "query Brazilian public data"
  - "add mcp brasil to my agent"
  - "access Brazilian transparency portal"
  - "query IBGE or Banco Central data"
  - "Brazilian legislative data with MCP"
  - "setup mcp server for Brazil APIs"
---

# mcp-brasil: MCP Server for 28 Brazilian Public APIs

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

`mcp-brasil` is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that exposes 213 tools, 55 resources, and 45 prompts across 28 Brazilian public APIs — letting AI agents (Claude, GPT, Copilot, Cursor, etc.) query government data in natural language. 26 APIs require no key; only 2 need free registrations.

---

## Installation

```bash
# pip
pip install mcp-brasil

# uv (recommended)
uv add mcp-brasil
```

---

## Quick Setup by Client

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "mcp-brasil": {
      "command": "uvx",
      "args": ["--from", "mcp-brasil", "python", "-m", "mcp_brasil.server"],
      "env": {
        "TRANSPARENCIA_API_KEY": "$TRANSPARENCIA_API_KEY",
        "DATAJUD_API_KEY": "$DATAJUD_API_KEY"
      }
    }
  }
}
```

### VS Code / Cursor

Create `.vscode/mcp.json` in your project root:

```json
{
  "servers": {
    "mcp-brasil": {
      "command": "uvx",
      "args": ["--from", "mcp-brasil", "python", "-m", "mcp_brasil.server"],
      "env": {
        "TRANSPARENCIA_API_KEY": "$TRANSPARENCIA_API_KEY",
        "DATAJUD_API_KEY": "$DATAJUD_API_KEY"
      }
    }
  }
}
```

### Claude Code CLI

```bash
claude mcp add mcp-brasil -- uvx --from mcp-brasil python -m mcp_brasil.server
```

### HTTP Transport (other clients)

```bash
fastmcp run mcp_brasil.server:mcp --transport http --port 8000
# Server at http://localhost:8000/mcp
```

---

## Environment Variables

Create a `.env` file or export in your shell:

```bash
# Optional — 26 other APIs work without any keys
TRANSPARENCIA_API_KEY=your_key_here    # https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email
DATAJUD_API_KEY=your_key_here          # https://datajud-wiki.cnj.jus.br/api-publica/acesso

# Tuning
MCP_BRASIL_TOOL_SEARCH=bm25            # bm25 | code_mode | none (default: bm25)
MCP_BRASIL_HTTP_TIMEOUT=30.0           # seconds
MCP_BRASIL_HTTP_MAX_RETRIES=3
```

---

## API Coverage (28 Features, 213 Tools)

| Category | Feature Key | API | Tools |
|---|---|---|---|
| Economic | `ibge` | IBGE — states, municipalities, statistics | 9 |
| Economic | `bacen` | Banco Central — Selic, IPCA, FX, PIB, 190+ series | 9 |
| Legislative | `camara` | Câmara dos Deputados — deputies, bills, votes, expenses | 10 |
| Legislative | `senado` | Senado Federal — senators, bills, votes, committees | 26 |
| Transparency | `transparencia` | Portal da Transparência — contracts, spending, sanctions | 18 |
| Transparency | `tcu` | TCU — rulings, ineligible bidders | 8 |
| TCE (states) | `tce_sp/rj/rs/sc/pe/ce/rn/pi/to` | 9 State audit courts | 39 |
| Judiciary | `datajud` | DataJud/CNJ — court cases, movements | 7 |
| Judiciary | `jurisprudencia` | STF, STJ, TST — rulings, precedents | 6 |
| Electoral | `tse` | TSE — elections, candidates, campaign finance | 15 |
| Environment | `inpe` | INPE — wildfires, deforestation | 4 |
| Environment | `ana` | ANA — hydrological stations, reservoirs | 3 |
| Health | `saude` | CNES/DataSUS — facilities, professionals, beds | 4 |
| Oceanography | `tabua_mares` | Tide tables for Brazilian ports | 7 |
| Procurement | `pncp` | PNCP — public contracts (Lei 14.133/2021) | 6 |
| Procurement | `dadosabertos` | ComprasNet/SIASG | 8 |
| Utilities | `brasilapi` | CEP, CNPJ, DDD, banks, FX, FIPE, PIX | 16 |
| Utilities | `dados_abertos` | dados.gov.br — dataset catalog | 4 |
| Utilities | `diario_oficial` | Official gazettes from 5,000+ cities | 4 |
| Utilities | `transferegov` | Parliamentary PIX transfers | 5 |
| AI Agent | `redator` | Draft official documents with real data | 5 |

---

## Meta-Tools (Root Server)

Four special tools are always available regardless of feature:

| Tool | Description |
|---|---|
| `listar_features` | List all 28 features with descriptions |
| `recomendar_tools` | BM25 search — get relevant tools for a query |
| `planejar_consulta` | Build multi-API execution plan for a complex query |
| `executar_lote` | Run multiple tool calls in parallel in one request |

---

## Development Commands

```bash
git clone https://github.com/jxnxts/mcp-brasil.git
cd mcp-brasil

make dev              # Install all dependencies (prod + dev)
make test             # Run all tests
make test-feature F=ibge   # Test a single feature
make lint             # Lint + format check
make ruff             # Auto-fix lint + format
make types            # mypy strict mode
make ci               # lint + types + test (full CI)
make run              # Start server (stdio transport)
make serve            # Start server (HTTP :8000)
make inspect          # List all tools/resources/prompts
```

---

## Architecture: Package by Feature + Auto-Registry

```
src/mcp_brasil/
├── server.py              # Auto-discovers features — never edit manually
├── _shared/               # Shared HTTP client, rate limiting, BM25
├── data/                  # 27 API features
│   ├── ibge/
│   │   ├── __init__.py    # exports FEATURE_META
│   │   ├── server.py      # FastMCP instance (exports `mcp`)
│   │   ├── tools.py       # Tool implementations
│   │   ├── client.py      # Async HTTP via httpx
│   │   ├── schemas.py     # Pydantic v2 models
│   │   └── constants.py   # Base URLs, codes
│   ├── bacen/
│   └── ...
└── agentes/               # Intelligent agent features
    └── redator/
```

**Auto-registry**: The root `server.py` scans for `FEATURE_META` in `__init__.py` and `mcp: FastMCP` in `server.py` — no manual registration needed.

---

## Adding a New Feature

```bash
mkdir src/mcp_brasil/data/myfeature
touch src/mcp_brasil/data/myfeature/{__init__.py,server.py,tools.py,client.py,schemas.py,constants.py}
```

### `__init__.py` — Required export

```python
from mcp_brasil._shared.types import FeatureMeta

FEATURE_META = FeatureMeta(
    name="myfeature",
    description="Short description of the API",
    tags=["category"],
    requires_key=False,
)
```

### `server.py` — Required export

```python
from fastmcp import FastMCP
from .tools import register_tools

mcp = FastMCP("myfeature")
register_tools(mcp)
```

### `client.py` — Async HTTP pattern

```python
import httpx
from mcp_brasil._shared.http import get_client

BASE_URL = "https://api.example.gov.br"

async def fetch_data(endpoint: str, params: dict) -> dict:
    async with get_client() as client:
        response = await client.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
```

### `schemas.py` — Pydantic v2 models

```python
from pydantic import BaseModel, Field
from typing import Optional

class MyResult(BaseModel):
    id: str
    name: str
    value: Optional[float] = Field(None, description="Numeric value")
```

### `tools.py` — Tool registration

```python
from fastmcp import FastMCP
from .client import fetch_data
from .schemas import MyResult

def register_tools(mcp: FastMCP) -> None:

    @mcp.tool(description="Busca dados do endpoint X")
    async def buscar_dados(
        codigo: str,
        ano: int = 2024,
    ) -> list[MyResult]:
        """Retorna dados do endpoint X para o código fornecido."""
        raw = await fetch_data("endpoint-x", {"codigo": codigo, "ano": ano})
        return [MyResult(**item) for item in raw.get("data", [])]
```

### `tests/data/myfeature/test_tools.py` — Test pattern

```python
import pytest
from unittest.mock import AsyncMock, patch
from mcp_brasil.data.myfeature.tools import register_tools
from fastmcp import FastMCP

@pytest.fixture
def mcp():
    server = FastMCP("test-myfeature")
    register_tools(server)
    return server

@pytest.mark.asyncio
async def test_buscar_dados(mcp):
    mock_response = {"data": [{"id": "001", "name": "Test", "value": 42.0}]}
    with patch("mcp_brasil.data.myfeature.client.fetch_data", new_callable=AsyncMock) as mock:
        mock.return_value = mock_response
        # call via mcp tool invocation or directly
        from mcp_brasil.data.myfeature.tools import buscar_dados
        result = await buscar_dados(codigo="001")
        assert len(result) == 1
        assert result[0].name == "Test"
```

---

## Common Usage Patterns

### Pattern 1: Cross-reference with `planejar_consulta`

Ask the agent to plan a multi-API query:

```
"Crie um plano de consulta para analisar o deputado federal João Silva:
gastos, votações, proposições e financiamento de campanha."
```

The `planejar_consulta` meta-tool returns a structured execution plan combining `camara`, `tse`, and `transparencia` tools.

### Pattern 2: Parallel execution with `executar_lote`

```
"Execute em paralelo: taxa Selic atual, IPCA dos últimos 12 meses, 
e câmbio USD/BRL de hoje."
```

`executar_lote` fires all three `bacen` tool calls concurrently.

### Pattern 3: Smart discovery with `recomendar_tools`

```
"Quais tools devo usar para investigar contratos suspeitos em licitações municipais?"
```

BM25 search filters the 213 tools to return only relevant ones (e.g., `tce_sp`, `pncp`, `tcu`, `transparencia`).

### Pattern 4: Direct tool calls in code

```python
import asyncio
from mcp_brasil.data.bacen.tools import buscar_serie_temporal
from mcp_brasil.data.ibge.tools import buscar_municipios

async def main():
    # Selic rate last 12 months
    selic = await buscar_serie_temporal(codigo="432", ultimos=12)
    
    # All municipalities in São Paulo state
    municipios = await buscar_municipios(uf="SP")
    
    print(f"Selic entries: {len(selic)}")
    print(f"SP municipalities: {len(municipios)}")

asyncio.run(main())
```

### Pattern 5: Using brasilapi for CNPJ/CEP lookup

```python
from mcp_brasil.data.brasilapi.tools import consultar_cnpj, consultar_cep

async def lookup():
    empresa = await consultar_cnpj(cnpj="00000000000191")  # Banco do Brasil
    endereco = await consultar_cep(cep="01310100")         # Av. Paulista
```

---

## Natural Language Query Examples

Once the server is connected to your AI client:

```
# Economic analysis
"Qual a tendência da taxa Selic nos últimos 12 meses? Compare com IPCA."

# Legislative research  
"Quais projetos de lei sobre IA tramitaram na Câmara em 2024? Quem foram os autores?"

# Transparency / anti-corruption
"Quais os 10 maiores contratos do governo federal em 2024?"

# Cross-state comparison
"Compare gastos per capita com saúde em SP e MG cruzando TCE-SP e IBGE."

# Judiciary
"Busque processos sobre licitação irregular no TCU. Quais as penalidades?"

# Electoral finance
"Quais os maiores doadores da campanha do candidato X?"

# Environment
"Quantos focos de queimada foram registrados no Cerrado em agosto 2024?"

# Document generation (redator feature)
"Redija um ofício solicitando informações sobre o contrato 001/2024 
com dados reais do Portal da Transparência."
```

---

## Troubleshooting

### Server not starting
```bash
# Verify installation
python -m mcp_brasil.server --help

# Check uvx finds the package
uvx --from mcp-brasil python -c "import mcp_brasil; print(mcp_brasil.__version__)"
```

### API returning 401/403
- `transparencia` and `datajud` silently degrade without keys — set `TRANSPARENCIA_API_KEY` and `DATAJUD_API_KEY` for full access
- Keys are free: [Transparência](https://portaldatransparencia.gov.br/api-de-dados/cadastrar-email) | [DataJud](https://datajud-wiki.cnj.jus.br/api-publica/acesso)

### Too many tools visible (context overflow)
Set `MCP_BRASIL_TOOL_SEARCH=bm25` (default) — only tools relevant to the current query are surfaced. Use `code_mode` to expose all tools, or `none` to disable filtering.

### Timeout errors on slow government APIs
```bash
MCP_BRASIL_HTTP_TIMEOUT=60.0    # increase timeout
MCP_BRASIL_HTTP_MAX_RETRIES=5   # increase retries
```

### Feature not auto-discovered
Ensure your feature folder exports both:
- `FEATURE_META` in `__init__.py`
- `mcp: FastMCP` instance in `server.py`

Run `make inspect` to verify your feature appears in the tool list.

### Running tests for a specific feature
```bash
make test-feature F=bacen
make test-feature F=transparencia
```

---

## Key Design Principles

1. **Async everywhere** — `httpx` async client, all tools are `async def`
2. **Pydantic v2** — all API responses validated through typed schemas
3. **Rate limiting with backoff** — built into `_shared/http.py`, transparent to feature code
4. **Zero manual registration** — add a folder → it's discovered automatically
5. **BM25 smart filtering** — prevents context window bloat from 213 tools
6. **Graceful degradation** — APIs requiring keys still work (with reduced limits) without them
