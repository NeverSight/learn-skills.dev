---
name: joule-a2a-agent
description: |
  Generate and deploy a pro-code AI agent using LangGraph and SAP GenAI Hub, deploy it to SAP BTP Cloud Foundry, create a Joule capability with A2A (Agent-to-Agent) action, and deploy it to Joule. Supports TypeScript (Express or CAP) and Python. Use this skill whenever the user mentions: building a custom agent for Joule, deploying an AI agent to BTP Cloud Foundry, A2A protocol integration with Joule, pro-code agent extensibility, LangGraph agent on SAP BTP, connecting an external agent to Joule, "bring your own agent" for Joule, creating a Joule capability with A2A action, CAP agent, MTA deployment, or any combination of LangGraph/A2A/Joule/BTP/Cloud Foundry/CAP in an agent development context. Also trigger when the user wants to scaffold, modify, or redeploy an existing A2A agent project.
---

# Joule A2A Agent on SAP BTP Cloud Foundry

This skill generates a complete pro-code AI agent project that:
1. Implements an agent with **A2A protocol v0.3.0** support using **LangGraph + @a2a-js/sdk 0.3.10** and **SAP GenAI Hub** (OrchestrationClient) as the LLM provider
2. Deploys to **SAP BTP Cloud Foundry** as a REST API (via `cf push` or MTA)
3. Creates a **Joule capability** with an A2A action using the multi-file DTA format
4. Provides CLI commands to compile and deploy the capability to Joule

## How This Works — The Big Picture

SAP Joule can orchestrate external agents using the A2A (Agent-to-Agent) protocol. The flow is:

1. **Your agent** runs as a TypeScript or Python web service on Cloud Foundry, exposing an A2A-compatible endpoint
2. **Joule discovers your agent** by reading its Agent Card at `/.well-known/agent.json`
3. When a user's prompt matches your agent's capability, **Joule sends an A2A task** to your agent
4. Your agent processes the request using LangGraph (with tools, LLM reasoning via SAP GenAI Hub, etc.) and returns the result
5. **Joule presents the result** to the user in the chat

The connection between Joule and your agent uses a BTP Destination + a Joule capability YAML that defines an `agent-request` action type.

## Prerequisites

**Joule DTA Schema Version 3.28.0+ Required:** Code-based agents (BYOA) using the `agent-request` action type are supported as of DTA schema version 3.28.0. The `capability.sapdas.yaml` must specify `schema_version: "3.28.0"`.

If your Joule tenant runs an older schema version, the compile will succeed but deploy will fail with: *"Schema version defined in config file is greater than the current schema version of Joule"*.

**How to check your tenant's version:**
1. Login: `joule login --use-env` (or `joule login `)
2. Check status: `joule status`
3. Try deploying — if you get the schema error, your tenant needs an update
4. Contact your BTP admin to request a Joule service update

**Other prerequisites:**
- SAP BTP subaccount with Cloud Foundry enabled
- AI Core service instance with a GenAI Hub model deployed
- Joule CLI installed: `npm install -g @sap/joule-studio-cli`
- CF CLI installed and logged in (`cf login` or `cf login `)
- Joule CLI logged in (`joule login` or `joule login --use-env`)
- Joule App2App IAS flow configured for Joule Studio CLI ([assign required roles](https://help.sap.com/docs/joule/integrating-joule-with-sap/assign-roles))
- BTP roles: `extensibility_developer` + `capabilityadmin` for Joule deployments
- For CAP agents: `mbt` (MTA Build Tool): `npm install -g mbt`
- For CAP agents: MTA CF CLI plugin: `cf install-plugin multiapps` (required for `cf deploy` with `.mtar` files)

**Before you start**, make sure Claude Code is started with the toolkit plugin and you are logged in to both CLIs:
```bash
# Start Claude Code with the SAP A2A Agent Toolkit plugin
claude --plugin-dir <path-to-sap-a2a-agent-toolkit>

# Log in to Cloud Foundry
cf login -a https://api.cf.<landscape>.hana.ondemand.com 

# Log in to Joule
joule login 
```

## Workflow

When the user asks to create/modify a Joule A2A agent, follow these steps:

### Step 1: Gather Requirements

Ask the user:
- **Language** — TypeScript (default) or Python?
- **Framework** — Express (default, lightweight) or CAP (enterprise, MTA deploy)? Note: CAP is TypeScript-only.
- **Agent name and purpose** — what should this agent do?
- **Tools/APIs** — what external services or APIs should the agent call?
- **SAP GenAI Hub model** — which model deployed on AI Core? (default: `gpt-4.1`)
- **BTP landscape details** — CF API endpoint, org, space (if they know them)

If the user is unsure about BTP details, generate the project anyway with placeholder values.

### Step 2: Generate the Agent Project

The project can be generated in three configurations:

#### a) TypeScript + Express (default)

Run the scaffold script:
```bash
bash <skill-path>/scripts/scaffold-ts.sh \
  --name <agent-name> \
  --framework express \
  --namespace <company-namespace> \
  --output <output-dir> \
  --description "<agent description>" \
  --landscape <cf-landscape>
```

Or manually using `references/langgraph-a2a-agent-typescript.md` + `references/cf-deployment-typescript.md`.

```
<agent-name>/
├── src/
│   ├── index.ts              # Express + A2A server entry point
│   ├── agent.ts              # LangGraph.js ReAct agent
│   ├── executor.ts           # A2A protocol bridge
│   ├── agentCard.ts          # Agent Card definition
│   ├── tools.ts              # Agent's tools (Zod schemas)
│   └── llm.ts                # SAP GenAI Hub configuration
├── joule-capability/
│   ├── capability.sapdas.yaml
│   ├── capability_context.yaml
│   ├── da.sapdas.yaml
│   ├── functions/call_agent.yaml
│   └── scenarios/invoke_agent.yaml
├── package.json
├── tsconfig.json
├── manifest.yml
├── Procfile
├── .env.example
└── README.md
```

#### b) TypeScript + CAP

Run the scaffold script:
```bash
bash <skill-path>/scripts/scaffold-ts.sh \
  --name <agent-name> \
  --framework cap \
  --namespace <company-namespace> \
  --output <output-dir> \
  --description "<agent description>" \
  --landscape <cf-landscape>
```

Or manually using `references/langgraph-a2a-agent-cap-typescript.md` + `references/cf-deployment-cap-typescript.md`.

```
<agent-name>/
├── srv/
│   ├── server.ts              # CAP bootstrap + A2A Express endpoints
│   ├── agent-executor.ts      # LangGraph StateGraph agent orchestrator
│   ├── service.cds            # CDS service definition
│   ├── tools/
│   │   └── tools.ts           # Agent tools (Zod schemas)
│   └── utils/
│       ├── prompts.ts         # System prompt
│       ├── a2aToLangchain.ts  # A2A → LangChain converter
│       ├── a2a-operations.ts  # A2A event helpers
│       └── helpers.ts         # URL helpers
├── joule-capability/
│   ├── capability.sapdas.yaml
│   ├── capability_context.yaml
│   ├── da.sapdas.yaml
│   ├── functions/call_agent.yaml
│   └── scenarios/invoke_agent.yaml
├── package.json
├── tsconfig.json
├── mta.yaml
├── .cdsrc.sample.json
├── .env.example
└── README.md
```

#### c) Python + Express

Run the scaffold script:
```bash
python <skill-path>/scripts/scaffold.py \
  --name <agent-name> \
  --namespace <company-namespace> \
  --output <output-dir> \
  --description "<agent description>" \
  --landscape <cf-landscape>
```

Or manually using `references/langgraph-a2a-agent.md` + `references/cf-deployment.md`.

#### Key Differences

| Aspect | TS Express | TS CAP | Python |
|--------|-----------|--------|--------|
| Server | Express + jsonRpcHandler/agentCardHandler | CAP + cds.on("bootstrap") | Starlette + A2AStarletteApplication |
| A2A SDK | @a2a-js/sdk 0.3.10 | @a2a-js/sdk 0.3.10 | a2a-sdk >=0.2.7 |
| LLM | OrchestrationClient | OrchestrationClient | langchain-openai ChatOpenAI (direct AI Core endpoint) |
| Deploy | `cf push` (manifest.yml) | `mbt build && cf deploy` (mta.yaml) | `cf push` (manifest.yml) |
| Auth | Manual | Built-in CAP auth | Manual |
| Agent pattern | createReactAgent | StateGraph (manual) | create_react_agent |
| Interrupt support | Basic (question heuristic) | Full (LangGraph interrupt()) | Structured response format |
| Buildpack | nodejs_buildpack | nodejs_buildpack (via MTA) | python_buildpack |
| Reference | `langgraph-a2a-agent-typescript.md` | `langgraph-a2a-agent-cap-typescript.md` | `langgraph-a2a-agent.md` |

The **Joule capability YAML** files are identical regardless of language/framework.

### Step 3: Customize the Agent

Based on the user's requirements:

1. **Define tools** — In TypeScript: functions created with `tool()` and Zod schemas. In Python: functions decorated with `@tool`. Map each user requirement to a tool function.
   - Express TS: `src/tools.ts`
   - CAP TS: `srv/tools/tools.ts`
   - Python: `app/tools.py`

2. **Configure the agent** — Set the system instruction to match the agent's purpose.
   - Express TS: `SYSTEM_PROMPT` in `src/agent.ts`
   - CAP TS: `srv/utils/prompts.ts`
   - Python: `SYSTEM_INSTRUCTION` in `app/agent.py`

3. **Set up the Agent Card** — Name, skills, and supported modes.
   - Express TS: `src/agentCard.ts`
   - CAP TS: `agentCard` in `srv/server.ts`
   - Python: `app/agent_card.py`

4. **Configure `capability.sapdas.yaml`** — The scenario description in `scenarios/invoke_agent.yaml` must clearly describe when Joule should invoke this agent.

### Step 4: Deploy to Cloud Foundry

#### Express (TypeScript or Python)

Read `references/cf-deployment-typescript.md` or `references/cf-deployment.md`.

```bash
cd <agent-name>
npm install
npm run build  # TypeScript only — must compile before push
cf push
curl https://<app-url>/.well-known/agent.json
```

#### CAP (TypeScript)

Read `references/cf-deployment-cap-typescript.md`.

```bash
cd <agent-name>
npm install
mbt build
cf deploy mta_archives/<agent-name>_1.0.0.mtar
curl https://<agent-name>-srv.cfapps.<landscape>.hana.ondemand.com/.well-known/agent.json
```

### Step 5: Create the BTP Destination

After deployment, create a BTP Destination pointing to the agent's URL:

```bash
bash <skill-path>/scripts/create-destination.sh \
  --agent-name <agent-name> \
  --destination-name <DESTINATION_NAME> \
  --landscape <cf-landscape>
```

The destination name must match `system_aliases.<AliasName>.destination` in `capability.sapdas.yaml`.

### Step 6: Deploy the Joule Capability

Read `references/joule-capability.md` for the complete reference.

```bash
# Install Joule CLI (if not installed)
npm install -g @sap/joule-cli

# Authenticate
joule login     # or joule login --use-env

# Navigate to the joule-capability directory
cd joule-capability

# Compile + deploy
joule deploy ./da.sapdas.yaml --compile -n "<assistant_name>"
```

### Step 7: Test the Integration

1. Open Joule in your SAP system
2. Type a prompt that matches the capability's scenario description
3. Joule should route the request to your agent via A2A
4. Verify the response comes back correctly

If it doesn't work, check: destination configuration, agent card accessibility, capability scenario description matching, and CF app logs (`cf logs <app-name> --recent`).

## Modifying an Existing Agent

When the user wants to change an existing agent:

1. **Adding a new tool**: Add the tool function, register it in the agent, add a skill to the agent card. Redeploy to CF.

2. **Changing the model**: Update `MODEL_NAME` env var. The model must be deployed on your AI Core instance.

3. **Updating the Joule capability**: Edit `capability.sapdas.yaml` and scenario files, recompile and redeploy with `joule deploy ./da.sapdas.yaml --compile`.

4. **Scaling**: Adjust `instances` and `memory` in `manifest.yml` (Express) or `mta.yaml` (CAP).

## Reference Files

Read these before generating code:

### LangGraph + A2A SDK
- `references/langgraph-a2a-agent-typescript.md` — TypeScript Express templates (jsonRpcHandler, agentCardHandler, createReactAgent, OrchestrationClient)
- `references/langgraph-a2a-agent-cap-typescript.md` — TypeScript CAP templates (cds.on bootstrap, StateGraph, interrupt support)
- `references/langgraph-a2a-agent.md` — Python templates (A2AStarletteApplication, create_react_agent, langchain-openai with direct AI Core credentials)

### Cloud Foundry Deployment
- `references/cf-deployment-typescript.md` — TypeScript Express: manifest.yml, package.json, cf push
- `references/cf-deployment-cap-typescript.md` — TypeScript CAP: mta.yaml, mbt build, cf deploy
- `references/cf-deployment.md` — Python: manifest.yml, requirements.txt, Procfile

### Joule Integration
- `references/joule-capability.md` — Multi-file DTA format: capability.sapdas.yaml (schema 3.28.0), da.sapdas.yaml (schema 1.4.0), functions/, scenarios/, multi-turn contextId/taskId pattern

## Important Notes

- The A2A protocol v0.3.0 uses JSON-RPC 2.0 over HTTP(S). Your agent must handle `message/send` and optionally `message/stream` methods.
- Agent Cards must be served at `/.well-known/agent.json` for Joule's discovery.
- SAP GenAI Hub requires an AI Core service instance and a deployment of the model you want to use.
- TypeScript agents use `OrchestrationClient` from `@sap-ai-sdk/langchain` (auto-reads VCAP_SERVICES).
- Python agents use `langchain-openai` `ChatOpenAI` pointed at AI Core's OpenAI-compatible endpoint (do NOT use `generative-ai-hub-sdk` — pydantic version conflict with `a2a-sdk`).
- The Joule CLI (`@sap/joule-cli`) requires the `capabilityadmin` and `extensibility_developer` roles.
- Destinations in BTP must use NoAuthentication or OAuth2ClientCredentials.
- CAP is only available for TypeScript. Python uses Express (Starlette) only.
- The `da.sapdas.yaml` uses schema version `1.4.0`. The `capability.sapdas.yaml` uses `3.28.0`.
- **Namespace must be `joule.ext`** — the `metadata.namespace` in `capability.sapdas.yaml` must be set to `joule.ext`. Using any other namespace (e.g. `mycompany`) will cause `joule deploy` to fail with a namespace validation error. The scaffold scripts default to `joule.ext`.
- CAP agents require two extra tools: **`mbt`** (`npm install -g mbt`) for building and the **MTA CF CLI plugin** (`cf install-plugin multiapps`) for `cf deploy` to work with `.mtar` files. See [CAP deploy to CF guide](https://cap.cloud.sap/docs/guides/deploy/to-cf).
