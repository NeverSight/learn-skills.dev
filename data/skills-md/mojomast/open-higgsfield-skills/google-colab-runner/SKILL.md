---
name: google-colab-runner
description: Run video-director productions on Google Colab. It packages a manifest into a self-contained Google Colab bundle (a generated .ipynb that installs ComfyUI and custom nodes at pinned commits, downloads the open-weights models with the user's own Hugging Face token from Google Colab secrets, renders every shot, detects the GPU tier and collects outputs to Drive or a zip), or it lets the director drive a running Google Colab ComfyUI through a tunnel URL with a compute-unit estimate, the spend gate, a hard cap, drop-and-resume and teardown. Use it when the user has no local GPU, or asks to run on Google Colab.
---

# google-colab-runner

Two modes, both from `video-director`:

| mode | command | who presses Run | QA loop |
|---|---|---|---|
| **package** | `direct.py package --target google-colab <manifest>` | the user, in Google Colab | after the run: `colab.py ingest`, then still-qa / shot-qc locally |
| **orchestrate** | `direct.py run <manifest> --target google-colab --url <tunnel>` | the user starts the notebook in `orchestrate` mode; the director submits every job | live: the director's normal judge, retry and continuity loop |

Nothing here starts a Google Colab session or spends compute units by itself, and no credential is read or stored. The Hugging Face token is the user's own, read at run time inside Google Colab from the secret `HF_TOKEN`.

## Files
| path | what |
|---|---|
| `scripts/colab.py` | `estimate`, `package`, `orchestrate`, `teardown`, `ingest` (stdlib only) |
| `scripts/notebook.py` | builds the nbformat-4 notebook and the bundle README |
| `templates/runner.py` | the bundle runner: GPU detection, tier pick, upload, submit, poll, download, resumable `state.json` |
| `scripts/comfy_client.py` | copy of comfyui-connect's client, shipped inside every bundle |
| `references/models.json` | every model file the API workflows load: target folder, pinned Hugging Face URL, size, gated flag, licence note |
| `references/custom-nodes.lock.json` | ComfyUI and node-pack commits the notebook checks out |
| `references/gpu-tiers.json` | T4 / L4 / A100 / H100 → tier, compute units per hour, speed factor (unverified) |
| `references/google-colab.md` | the runbook: step by step for an agent |
| `references/ui-to-api.md` + `ui-to-api.report.json` | how the Comfy-Org UI templates were converted to API format, and the result per template |
| `scripts/ui_to_api/` | the converter (headless ComfyUI frontend `graphToPrompt`) and the `/object_info` validator |
| `tests/mock_comfy.py`, `tests/test_static.py` | stdlib mock ComfyUI + VLM and the static end-to-end tests |

## Rules
1. **Ask before any start.** Show `colab.py estimate` (session minutes and compute units, including setup and the collect-and-stop reserve) and wait for a yes. `orchestrate` stops at the `spend` gate unless it is `approved`, even when the manifest says `auto`.
2. **Hard cap.** `orchestrate` refuses to start without a compute-unit cap (`target.budget.max_credits` or `--max-cu`) and refuses an estimate over it. During the run, the wall-clock meter plus the reserve is checked before every render; at the cap it logs `cap_hit` and stops. The notebook watchdog enforces `MAX_SESSION_MINUTES` on the runtime side.
3. **Tear down.** Always end by offering `colab.py teardown --url <tunnel>` (the watchdog releases the runtime), or use `--teardown auto|on-cap`. Tell the user that Google Colab bills while the runtime is connected.
4. **Drops resume.** A dropped session exits with code 5 and the manifest saved. The user restarts the notebook and gives the new URL; re-running the same command resumes. Finished outputs stay on the user's machine and are re-uploaded to the new session.
5. **Open weights and licences.** `models.json` carries each file's licence note. LTX-2 family weights are under the Lightricks LTX-2 Community License (not OSI). The one UI template that needs a closed hosted API node (`GeminiImage2Node`) is excluded.

Exit codes: 0 done, 3 waiting at a gate, 4 stopped at a stage (awaiting approval or blocked), 5 Google Colab ComfyUI unreachable or dropped, 6 refused by the spend cap.
