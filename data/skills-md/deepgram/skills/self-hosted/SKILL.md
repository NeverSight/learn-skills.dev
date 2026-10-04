---
name: self-hosted
description: >
  Run Deepgram in infrastructure you control. Use when a task says "self-hosted", "self hosting",
  "on-prem", "on-premise", "air-gapped", "airgapped", "private deployment", "BYOC", "docker compose
  deepgram", "podman", "kubernetes", "helm chart", "sagemaker", "license proxy", "quay.io",
  "distribution credentials", "data residency", or "FIPS". Decides whether self-hosting is even the
  right answer versus a regional endpoint or Deepgram Dedicated, walks the licensing and container
  credential bootstrap, and routes to per-target guidance for Docker/Podman, Kubernetes/Helm, and
  Amazon SageMaker.
---

# Deepgram Self-Hosted

Deepgram ships its inference stack as container images you run on your own NVIDIA GPUs. Audio never leaves your network; only small license-verification messages do. This skill decides whether you need that, gets you licensed, and routes to the deployment target.

Self-hosting is gated on an Enterprise agreement. Read [Decide before you deploy](#decide-before-you-deploy) first — a large share of "we need on-prem" requirements are actually data-residency requirements that a regional endpoint already satisfies, with none of the GPU operations.

## Decide before you deploy

Read down the table and take the first row whose requirement you actually have. If none of them apply, the hosted API is the answer.

| Requirement | Answer | What you operate |
|---|---|---|
| Audio may not leave your network, or you need bare metal, an air gap, or FIPS crypto | Full self-hosted containers | GPUs, drivers, containers, models, scaling |
| Must run inside your AWS account, and you want AWS to handle provisioning and scaling | Amazon SageMaker via AWS Marketplace | A SageMaker Endpoint |
| Dedicated capacity, regional control, or compliance isolation — but not your hardware | [Deepgram Dedicated](https://deepgram.com/dedicated) — `{SHORT_UID}.{REGION}.api.deepgram.com` | Nothing — existing API keys work |
| Data must be processed in the EU, Australia, or India | Regional endpoint: `api.eu.deepgram.com`, `api.au.deepgram.com`, `api.in.deepgram.com` | Nothing — same API keys and SDKs, change the base URL only |
| None of the above | Hosted API, `api.deepgram.com` | Nothing |

People reach for the top row first. Most requirements are satisfied by a row further down.

The three regional endpoints serve Speech-to-Text, Text-to-Speech, Voice Agent, and Text Intelligence. Confirm the current limitations at [Regional Endpoints](https://developers.deepgram.com/reference/regional-endpoints) before you promise a region to a customer.

Self-hosting is the most expensive row in engineering time. Choose it for a real network, sovereignty, or air-gap constraint — not for latency, which regional and Dedicated endpoints address without handing you a GPU fleet.

## Bootstrap licensing and credentials first

Nothing runs without both of these, and they are different things people routinely conflate.

| | Self-hosted API key | Distribution credentials |
|---|---|---|
| What it is | `DEEPGRAM_API_KEY` — licenses running containers | A Quay username and secret — pulls container images |
| Looks like | A normal Deepgram API key secret | `deepgram+6ba7b810-…` plus a 64-character secret |
| Where it goes | Container environment; `[license]` in `api.toml` / `engine.toml` | `docker login quay.io`, or a Kubernetes image-pull Secret |
| Created by | Console → API Keys, or the project keys API | Console → Self-Hosted tab, or the distribution-credentials API |

Steps:

1. **Confirm project access.** Your Console project needs a **Self-Hosted** tab. No tab means the project was never granted self-hosted products, or has managed access but not self-service. Both are resolved by Deepgram: [contact sales](https://deepgram.com/contact-us) or your account representative. You cannot self-serve past this.
2. **Create a self-hosted API key** in [Console](https://console.deepgram.com). Expand its details to see which self-hosted products it may license. All self-hosted customers get API and Engine; the License Proxy must be enabled for your project by Deepgram Support.
3. **Create distribution credentials** in the Console Self-Hosted tab. The secret is displayed **once** — record it immediately. Verify from the CLI:

   ```bash
   # List existing credential sets (read-only, safe)
   curl -s -H "Authorization: Token $DEEPGRAM_API_KEY" \
     "https://api.deepgram.com/v1/projects/$DEEPGRAM_PROJECT_ID/self-hosted/distribution/credentials"
   ```

   Returns `200` with a `distribution_credentials` array. Note the hyphen in `self-hosted` — `selfhosted` returns 404.

   **A `200` here does not mean your project has self-hosted access.** On a project with no self-hosted entitlement the endpoint still returns `200` with an empty array rather than a `403`. The Console Self-Hosted tab in step 1 is the real entitlement check; an empty list proves nothing either way.

   The `POST` variant takes a `scopes` query parameter, which accepts `self-hosted:products` (the default, meaning all) or per-product scopes: `self-hosted:product:api`, `:engine`, `:license-proxy`, `:dgtools`, `:billing`, `:hotpepper`, `:metrics-server`. Only `api`, `engine`, `license-proxy`, and `billing` map to containers documented publicly; the rest are undocumented, so scope credentials to what you actually deploy. `provider` accepts `quay`.

4. **Log in to Quay** on every deployment host: `docker login quay.io` (or `podman login`).
5. **Get the model files.** Deepgram delivers encrypted `.dg` model files as download links from your account representative (`.dgv2` files for FIPS images; the two formats are not interchangeable). They are **not** in any public repository and are not on Quay. See [Gated by a human](#gated-by-a-human).
6. **Verify runtime licensing.** Containers hold an outbound HTTPS connection to `license.deepgram.com:443` for licensing and usage reporting. That connection uses mTLS, so probing it with `curl` or an SSL scanner produces spurious errors — that is expected, not a fault. A `401` in container logs means the API key lacks self-hosted permissions; a timeout means your firewall is blocking the egress.

To rotate or revoke credentials, use the four endpoints documented in the `api` skill's `references/self-hosted.md`.

## What actually runs

| Component | Image | Role | Required |
|---|---|---|---|
| API | `quay.io/deepgram/self-hosted-api` | Accepts requests, serves `/v1/listen`, `/v1/speak`, `/v2/listen`, `/v2/speak`, `/v1/agent/converse`; delegates inference | Yes |
| Engine | `quay.io/deepgram/self-hosted-engine` | Runs inference on the GPU; loads `.dg` models (`.dgv2` on the `-fips` image) | Yes |
| License Proxy | `quay.io/deepgram/self-hosted-license-proxy` | Caches licensing so a license-server outage does not stop inference; can be the only container with egress | Recommended in production; access granted by Deepgram |
| Billing | `quay.io/deepgram/self-hosted-billing` | Validates a license file locally and journals usage — **air-gapped deployments only** | Air gap only |

Images are tagged by release date, for example `release-261001`, the tag carried across the Docker, Podman, and Helm templates and the Helm chart's `appVersion`. Check the templates for the current one. Pin an explicit tag; never rely on a floating one.

Minimum viable deployment: **one API container plus one Engine container on one GPU host**, with `api.toml`, `engine.toml`, and at least one `.dg` model. The License Proxy and Billing containers are additive.

Default ports, from the template TOML files: API `8080`; Engine `8080` for API-to-Engine traffic and `9991` for its metrics server; License Proxy `8443` for license verification and `8080` for its `/v1/status` health route.

Deepgram does not terminate TLS for you. Put your own proxy (NGINX, HAProxy, Apache) in front of the API container.

## Pick a deployment target

| Target | Use when | Reference |
|---|---|---|
| Docker / Podman Compose | Single host, a proof of concept, bare metal, or the simplest air gap | [docker-podman.md](references/docker-podman.md) |
| Kubernetes + Helm | Production, autoscaling, multi-node, air-gapped or FIPS deployments, Voice Agent | [kubernetes.md](references/kubernetes.md) |
| Amazon SageMaker | AWS-only, and you want AWS to provision and scale | [sagemaker.md](references/sagemaker.md) |
| — | Sizing hosts, choosing GPUs, drivers, OS, firewall rules | [hardware.md](references/hardware.md) |

Official templates for the first two live in [`deepgram/self-hosted-resources`](https://github.com/deepgram/self-hosted-resources) (public): `docker/`, `podman/`, `charts/deepgram-self-hosted/`, `common/` (TOML configs), plus `benchmarking/` (k6 load scripts), `monitoring/` (Grafana dashboards, Prometheus alert rules), and `diagnostics/` (log parser, NVIDIA setup validator).

FIPS images (the `-fips` tag suffix) change three things that decide the design before you pick a target. Flux STT is not supported on FIPS images and runs only on standard images. The FIPS Engine loads `.dgv2` models only; `.dgv2` and `.dg` files are not interchangeable, so request the FIPS model files specifically. The FIPS API image enforces TLS 1.3 exclusively: it rejects TLS 1.2 connections and non-FIPS cipher suites such as ChaCha20, the `[fips]` configuration flag does not control this, and any TLS 1.2-only client, SDK, or proxy in front of the API fails to connect. On FIPS images the API serves HTTPS itself with a full-chain PKI certificate you provide. Full contract at [FIPS-Compliant Deployment](https://developers.deepgram.com/docs/fips-compliant-deployment).

## Feature parity is opt-in, not automatic

Self-hosted is not a mirror of the hosted API. Newer models exist self-hosted but are **off by default**, need a minimum image release, need a model file you request by hand, and — critically — need their own dedicated Engine.

| Product | Self-hosted? | Enable with | Minimum image | Co-residency |
|---|---|---|---|---|
| Nova-3 / Nova-2 STT (`/v1/listen`) | Yes | Default | — | Shares an Engine with other Nova models |
| Aura-1 TTS (`/v1/speak`) | Yes | Default — model files only | — | Dedicated TTS node recommended |
| Aura-2 TTS (`/v1/speak`) | Yes | `aura2.enabled` plus a language block (Helm) | — | Two GPUs per Engine; dedicated TTS node |
| Flux STT (`/v2/listen`) | Yes | Engine `[flux] enabled`; API `[features] listen_v2` | `release-251015` | **Dedicated Engine.** Cannot share with any other model |
| Flux TTS (`/v2/speak`) | Yes | Engine `[flux_tts] enabled`, `uuid`, `watermarker_uuid`; API `[features] speak_v2`, `speak_v2_streaming` | `release-261001` | **Dedicated Engine.** Engine refuses to start if Aura is also configured |
| Voice Agent (`/v1/agent/converse`) | Yes | `agent.enabled` (Helm) | — | Needs STT and TTS Engines running alongside the API |

Consequences worth stating out loud before an evaluation:

- **Flux STT allocates all available GPU memory on Engine startup.** Send a Nova-3 request to that same GPU and you get CUDA out-of-memory errors. One Flux model per Engine; separate infrastructure for Flux.
- **Flux TTS needs one GPU per Engine** and allocates up to 60 GB of *system* RAM while loading, so the host needs at least 64 GB. Extra GPUs do not increase one Engine's capacity — run one Engine per GPU.
- **Voice Agent self-hosted is documented for Kubernetes/Helm only.** There is no Compose sample. The agent orchestrates your own LLM provider keys, or an in-cluster LLM (an NVIDIA NIM sample exists in the chart).
- **Do not mix STT and TTS on one node.** Deepgram recommends against it explicitly; it causes resource contention and unpredictable latency.
- **Whisper is not a self-hosted product.** "Deepgram Whisper Cloud" is a hosted managed API. Nothing in the self-hosted documentation set offers a Whisper model file. Do not plan an on-prem Whisper deployment without confirming with Deepgram.

Audio intelligence features (entity detection, redaction, NER formatting) depend on separate models being present, and are toggled under `[features]` in `api.toml`. Presence of the feature flag is not presence of the model.

## Gated by a human

Be honest with anyone planning a timeline. These cannot be self-served and are not in public documentation:

- **Project access to self-hosted products**: Enterprise agreement, via sales.
- **Every `.dg` model file**: links from your account representative. This is the hard blocker: you can pull images and write configs without one, and still serve nothing.
- **`[flux] max_streams`**: the concurrency limit per GPU. There is no published per-GPU table; the doc says to ask your account representative. Leaving it auto-calculated causes agents to hang, dropped calls, and `audio_window_end increased by more than 3 frames` in API logs.
- **`[flux_tts] max_batch_size`**: no safe default exists; Engine refuses to start while it is `0`, which is what the shipped templates set. The right value differs substantially per GPU and comes from your account representative.
- **The Flux TTS model `uuid`**: partly gated. The chart's `values.yaml` default and the docs page are empty placeholders, but the two shipped Compose templates (`common/*/engine.flux-tts.toml`) and the chart's `samples/08-flux-tts-setup.values.yaml` hardcode a real UUID, so a Compose or sample-values user already has a working value. The template comment still says to obtain it from your account representative, so confirm the UUID matches the release you are deploying rather than assuming the checked-in one is current.
- **The Flux TTS watermarker model**: `watermarker.<uuid>.dgv2`, provisioned with the Flux TTS model. From `release-261001`, Engine will not start Flux TTS without it, and `[flux_tts] watermarker_uuid` (Helm `fluxTts.watermarkerUuid`) must name it. The Compose templates and the chart's `samples/08-flux-tts-setup.values.yaml` ship `2c4e7068-5d1d-4425-a207-b2f221fabe79`; the chart's `values.yaml` default is empty, and the docs page leaves it for your account representative.
- **License Proxy entitlement**: via Support.
- **Air-gapped license file**: a one-line JSON file issued by Deepgram.
- **Pricing**: self-hosted is a sales conversation. No figure belongs in a skill; start at [deepgram.com/pricing](https://deepgram.com/pricing) and [contact us](https://deepgram.com/contact-us).

Hardware sizing beyond the published minimums is also a conversation: the docs repeatedly direct you to Support for a customized recommendation.

## Common mistakes

1. **Self-hosting to satisfy data residency that a regional endpoint already covers.** Check the EU, AU, and IN endpoints, and Deepgram Dedicated, before provisioning a single GPU.
2. **Confusing the self-hosted API key with distribution credentials.** The API key licenses running containers. The Quay credentials pull images. Swapping them gives you either a failed `docker login` or containers that pull and then die on a licensing `401`.
3. **`sudo docker compose up` without preserving the key.** The templates interpolate `${DEEPGRAM_API_KEY}`, and `sudo` drops it. Use `sudo --preserve-env=DEEPGRAM_API_KEY docker compose up -d`.
4. **A proprietary NVIDIA driver, or one older than 580.** Engine is built against CUDA 13, which needs driver `>=580` in the **open** kernel-module flavor. On Blackwell the proprietary 580 branch does not support the GPU at all, so the card is invisible to the host.
5. **Running Engine on a T4.** Nova and Aura work; Flux STT does not (needs Ampere or newer), and Flux TTS supports neither T4 nor A10.
6. **Expecting MIG or a fractional GPU to work.** Deepgram requires dedicated GPUs. MIG and fractional GPUs are unsupported.
7. **Assuming one big GPU replaces two for Aura TTS.** Aura and Aura-2 require *exactly two* dedicated GPUs per TTS Engine container. It is a device-count requirement, not a memory one.
8. **Enabling Flux next to other models.** The GPU-memory allocation is exclusive; you get CUDA OOM, not a graceful fallback.
9. **Omitting `NVIDIA_VISIBLE_DEVICES` and `NVIDIA_DRIVER_CAPABILITIES`.** Without them the nvidia-container-runtime injects no CUDA libraries and Engine dies with `libcuda.so.1: cannot open shared object file`. On GKE with Container-Optimized OS the equivalent failure needs `LD_LIBRARY_PATH` instead — chart `0.41.1`+ sets it for you.
10. **Tearing down the only License Proxy during an upgrade.** A new instance must reach `license.deepgram.com` to start. If it cannot and the old one is already gone, every container in the environment fails to license and shuts down. Use blue-green.
11. **Treating the mTLS license connection as broken** because `curl` or an SSL scanner errors against `license.deepgram.com`. That is correct behavior.
12. **Deleting the billing journal volume in an air-gapped deployment.** It holds usage data you are contractually required to return. Losing it can suspend service.
13. **Upgrading API before Engine on a TTS deployment.** `release-260115` changed API-to-Engine communication and is not backwards compatible for TTS traffic. The new Engine (`3.107.0-1`) is compatible with previous API versions, so it must be running before the updated API (`1.176.0`) serves requests: Engine first, then API. STT-only deployments are unaffected. Read the [January 15, 2026 changelog](https://developers.deepgram.com/changelog/2026/1/15) before any TTS upgrade; each self-hosted release carries its own ordering and minimum-driver requirements. Read the [chart CHANGELOG](https://github.com/deepgram/self-hosted-resources/blob/main/charts/deepgram-self-hosted/CHANGELOG.md) too. Chart `0.46.0` (`release-260915`) raised `gpu-operator.driver.version` from `550.54.15` to `580.173.02` and set `gpu-operator.driver.useOpenKernelModules` to `true`; when the GPU Operator manages your drivers, that upgrade reinstalls the driver on every GPU node and restarts the GPU workloads on it. Chart `0.47.0` (`release-261001`) watermarks Flux TTS audio: with `fluxTts.enabled: true` the chart fails to render until `fluxTts.watermarkerUuid` is set, `helm upgrade --reuse-values` included, and Engine will not start Flux TTS unless `watermarker.<uuid>.dgv2` sits in the models volume beside the Flux TTS model. Get that file from your account representative before upgrading.

## Use a different skill when

- You want the four distribution-credential endpoints in full — request bodies, scopes, responses: `api` skill, file `references/self-hosted.md`.
- You want any hosted API parameter, message shape, or response schema: `api` skill. Self-hosted serves the same contracts on your own host.
- You are choosing a model or getting a first request working: `speech-to-text`, `text-to-speech`, or `voice-agent` skill.
- You are deploying on SageMaker and want scripted subscribe, deploy, autoscale, and teardown: the dedicated `deepgram-sagemaker` skill in [`deepgram-devs/dg-sagemaker`](https://github.com/deepgram-devs/dg-sagemaker) (public). This skill's [sagemaker.md](references/sagemaker.md) covers the decision and the SDK transports; that skill covers the AWS mechanics.
- You want a runnable demo app to point at your deployment: `starters` skill.
- You want the documentation page for a topic: `docs` skill.
- You want the docs queryable from your editor: `setup-mcp` skill.

## Sources

Append `.md` to any `developers.deepgram.com` page for clean Markdown. [llms.txt](https://developers.deepgram.com/llms.txt) is the full documentation index and lists the self-hosted pages, which run to several dozen — more than this skill cites.

- Introduction: https://developers.deepgram.com/docs/self-hosted-introduction
- Deployment environments, GPU matrix, hardware minimums, firewall: https://developers.deepgram.com/docs/self-hosted-deployment-environments
- Licensing and credentials: https://developers.deepgram.com/docs/self-hosted-self-service-tutorial
- Deploy STT services: https://developers.deepgram.com/docs/deploy-stt-services
- Deploy TTS services: https://developers.deepgram.com/docs/deploy-tts-services
- Flux STT self-hosted: https://developers.deepgram.com/docs/flux-self-hosted
- Flux TTS self-hosted: https://developers.deepgram.com/docs/deploy-flux-tts
- Voice Agent self-hosted: https://developers.deepgram.com/docs/deploy-voice-agent
- License Proxy: https://developers.deepgram.com/docs/license-proxy
- Add-ons (License Proxy, SIPREC, UniMRCP): https://developers.deepgram.com/docs/self-hosted-add-ons
- Blue-green deployment: https://developers.deepgram.com/docs/blue-green-deployment
- Maintenance and model selection: https://developers.deepgram.com/docs/maintaining
- Metrics: https://developers.deepgram.com/docs/metrics-guide
- Regional, Dedicated, and self-hosted endpoints: https://developers.deepgram.com/reference/custom-endpoints and https://developers.deepgram.com/reference/regional-endpoints
- Using SDKs with self-hosted: https://developers.deepgram.com/docs/using-sdks-with-self-hosted
- FIPS-compliant deployment: https://developers.deepgram.com/docs/fips-compliant-deployment
- Official templates: https://github.com/deepgram/self-hosted-resources
- Helm chart release notes: https://github.com/deepgram/self-hosted-resources/blob/main/charts/deepgram-self-hosted/CHANGELOG.md
