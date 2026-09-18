---
name: w-api-test
description: Add API tests that exercise public HTTP behavior against existing harnesses.
disable-model-invocation: true
---

Test endpoints through the public interface using this repo's API or Playwright harness. Do not hit production. Do not hardcode secrets.

1. Read the API testing MDX and existing `*.test.ts` or e2e specs.
2. Cover the requested operations, authz denials, and contract-shaped responses.
3. Use sandbox or local servers from package scripts. Clean up created resources.
4. Run the documented API or e2e command for those tests.
5. Docs: `/w-docs` if behavior or commands changed.
