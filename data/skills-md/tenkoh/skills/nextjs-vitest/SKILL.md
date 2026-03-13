---
name: nextjs-vitest
description: Set up Vitest testing environment for Next.js projects
disable-model-invocation: true
---

Set up Vitest testing environment for a Next.js project.

## Steps

### 1. Install required packages

Run the following command:

```bash
npm install -D vitest @vitejs/plugin-react jsdom @testing-library/react @testing-library/dom vite-tsconfig-paths @testing-library/jest-dom @testing-library/user-event
```

### 2. Create vitest.config.mts

Create `vitest.config.mts` in the project root:

```typescript
import react from "@vitejs/plugin-react";
import tsconfigPaths from "vite-tsconfig-paths";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [tsconfigPaths(), react()],
  test: {
    environment: "jsdom",
    globals: true,
    clearMocks: true,
    setupFiles: ["./vitest.setup.ts"],
  },
});
```

### 3. Create vitest.setup.ts

Create `vitest.setup.ts` in the project root:

```typescript
import "@testing-library/jest-dom/vitest";
```

### 4. Verify completion

Confirm all files have been created correctly.
