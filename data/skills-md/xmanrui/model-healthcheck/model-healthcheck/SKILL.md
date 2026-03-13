---
name: model-healthcheck
description: Test all configured models for availability. Activate when user says "test models", "check models", "model healthcheck", "测试模型", "测试所有模型", "检查模型", or "模型健康检查".
---

# Model Healthcheck Skill

When the user requests a model test, follow these steps:

## Steps

1. **Get all model list**
   Use `gateway config.get` to read the current config and extract all `provider/model` combinations from `models.providers`.

2. **Test all models concurrently**
   For each model, use `sessions_spawn` to run a test:
   - task: "Reply with exactly: model ok. Only reply these two words."
   - model: the corresponding provider/model-id
   - runTimeoutSeconds: 30
   - cleanup: "delete"

   Fire all tests concurrently (multiple `sessions_spawn` calls at once), do not test sequentially.

3. **Collect results and summarize**
   Wait for all tests to complete, then summarize as a list:

   - provider/model-id — ✅ OK / ❌ Failed (Xs) — error message if any

   Fields:
   - Status: normal reply = ✅, timeout or error = ❌
   - Duration: time from spawn to result
   - Error: if failed, show the specific error (API error, timeout, auth failure, etc.)

4. **Output results**
   Send the summary to the user, with a final tally:
   - Total models tested: X
   - Passed: X
   - Failed: X (list failed model names and reasons)

## Notes

- Skip the model currently in use (no need to test yourself)
- If the user specifies a particular model, only test that one
- Feishu/WhatsApp and similar platforms don't support markdown tables — use list format instead
