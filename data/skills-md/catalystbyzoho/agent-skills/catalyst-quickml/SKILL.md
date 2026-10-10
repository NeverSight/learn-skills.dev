---
name: catalyst-quickml
description: "Catalyst QuickML — no/low-code ML, Generative AI, and ready-to-use AI platform. Covers (1) Prediction: ML pipelines, classification/regression, text analytics, recommendation, forecasting, clustering, anomaly detection, AutoML, prediction endpoints; (2) Generative AI: LLM Serving (chat, VLM), RAG, Knowledge Base, GenAI endpoints; (3) Zia Model Library: pre-built no-training models; (4) QuickML pricing — subscription plans and pay-as-you-go rates. Trigger on 'QuickML', 'AutoML', 'ML pipeline', 'train a model', 'model endpoint', 'LLM Serving', 'RAG', 'Knowledge Base', 'no-code ML', 'MLOps', or QuickML pricing/cost/billing/plan questions. DC availability: Prediction models all DCs; Generative AI (LLM Serving, RAG, Knowledge Base) NOT in AU, SA, or CA; Zia Model Library IN only."
metadata:
  version: "2.0.0"
---

## Prerequisites

Before using QuickML, activate it once per project in the console:
> Console → your project → **QuickML** (left sidebar) → click **"Start Exploring"**

Skipping this step prevents access to Data connectors, Pipelines, Models, Endpoints, LLM Serving, RAG, and Knowledge Base. This is a one-time activation per project.

---

## How It Works

1. **Check data-center availability first.** ML models: build & publish in US, IN, EU, AU, JP, SA, CA. Generative AI (LLM Serving, RAG, Knowledge Base): US, IN, EU, JP only — not AU, SA, or CA. Zia Model Library inside the QuickML console: IN only. If the feature is regional and the user's DC is unknown, ask before confirming it is available.

2. **Classify the task and load only the matching reference** (load several if the query spans domains):
   - Build, train, evaluate, or call a **trained ML model** (classification, regression, forecasting, clustering, anomaly detection, text analytics, recommendation, AutoML) → load `references/prediction-basics.md`.
   - **LLM chat, vision (VLM), RAG, or Knowledge Base** → load `references/generative-ai-basics.md`.
   - **Plans, rates, free tier, trial, or billing** → load `references/quickml-pricing-basics.md`.
   - A **pre-built model with no dataset or training** (OCR, face analytics, image moderation, object recognition, barcode, pre-built sentiment/NER/keywords) → STOP and load the **`catalyst-zia`** skill. The standalone Zia Services APIs have their own DC rules, separate from the QuickML-console Zia Model Library.

3. **Tool-first, then SDK, then console.** If a connected Catalyst MCP tool fits the action (pipelines, endpoints, datasets, metrics, LLM/RAG configs), discover it at runtime by name/description and read its schema before calling — do not hardcode tool names. Otherwise use the SDK: the **JavaScript SDK** (`new QuickML(app)`) is current; Node.js SDK v2 (`app.quickML()`) is deprecated. In every published SDK the prediction call is **`predict(endpointKey, inputData)`** — the `runInference` / `run_inference` names on the docs pages do not exist. The agent cannot see the console, so ask the user for UI-only values.

4. **Never fabricate QuickML specifics.** Use only the REST paths, headers, scope (`QuickML.deployment.READ`), and response shapes in the references (verified live). Do not invent response fields — there is no `likelihood_score` or `confidence` — and take anything else from the endpoint's sample in Console → QuickML → Endpoints. Do not invent pricing values the pricing reference does not list.

5. **Console steps must be exhaustive.** For every step, name the exact field, the dropdown/condition to select, the value, and any checkbox — generic steps cause silent misconfiguration (e.g. a Fill Columns rule needs its **condition** set to "missing values", not only a fill value). For anything the references do not cover, fetch the page under <https://docs.catalyst.zoho.com/en/quickml/> as Markdown (`<page-url>/index.md`); if the fetch fails, say so and give the user the URL.

## Triggers

Use this skill for: "QuickML", "Catalyst QuickML", "a QuickML endpoint", "training/predicting with a Catalyst model", "no-code ML", "no-code machine learning", "deploy a model", "model endpoint", "MLOps", "AutoML", "ML pipeline", "LLM Serving", "RAG", "pre-built model / Zia model", "OCR / face / image / text model", "QuickML pricing", "QuickML cost", "how much" (for QuickML usage), "billing", "subscription plan", "pay-as-you-go", or "Catalyst plan".

## References

| Reference | Load when the query is about… |
|-----------|-------------------------------|
| `references/prediction-basics.md` | Trained ML models — pipeline types and when to pick each, data connectors, preprocessing and operations, building and training pipelines, AutoML, evaluation metrics, SHAP, creating/publishing endpoints, prediction SDK calls (Java, Python, JavaScript, Node.js v2), limits |
| `references/generative-ai-basics.md` | Generative AI — LLM Serving (models, parameters, interaction modes, tool calling), VLM, RAG (modes, retrieval scope, agentic RAG), Knowledge Base uploads (local, WorkDrive, Zoho Learn), GenAI endpoint REST calls (no GenAI SDK methods exist) |
| `references/quickml-pricing-basics.md` | QuickML pricing — Catalyst subscription plans, pay-as-you-go unit rates, monthly free tier, add-ons, free trial, billing controls, and the rules for answering pricing questions |
