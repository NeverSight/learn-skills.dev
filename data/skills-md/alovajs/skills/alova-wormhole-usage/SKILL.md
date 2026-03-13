---
name: alova-wormhole-usage
description: devtools usage for alova. Use this skill whenever the user mentions alova openapi configuration, @alova/wormhole, API code generation, OpenAPI/Swagger with alova integration, alova devtools, or the alova VSCode extension. Trigger even for questions like "how do I use OpenAPI with alova" or "how do I generate API code with alova".
---

![alova banner](https://alova.js.org/img/cover.jpg)

# Alova OpenAPI Integration

> For client-side usage, see `alova-client` skill.
> For server-side (Node/Bun/Deno), see `alova-server` skill.

Alova integrates with OpenAPI/Swagger specs via `@alova/wormhole` to auto-generate API request functions and TypeScript types.

## Workflow

```plaintext
Install → Create alova.config → Run alova gen → Customize alova instance → Use generated APIs
```

## Alova Configuration

### Configuration File

Supported formats:

- `alova.config.cjs`: CommonJS configuration file
- `alova.config.js`: ESModule configuration file
- `alova.config.ts`: TypeScript configuration file

Use the `alova init` command to quickly create a configuration template.

```js
import { defineConfig } from '@alova/wormhole';

export default defineConfig({
  // API generation settings array
  generator: [
    {
      // OpenAPI file URL or local path
      input: 'http://localhost:3000/openapi.json',

      // Output path
      output: 'src/api',

      // Platform type (swagger)
      platform: 'swagger',

      // Plugin configuration
      plugins: [],

      // Response data media type (default: application/json)
      responseMediaType: 'application/json',

      // Request body media type (default: application/json)
      bodyMediaType: 'application/json',

      // API version (default: auto)
      version: 'auto',

      // Code type: auto/ts/typescript/module/commonjs
      type: 'auto',

      // Global API export name (default: Apis)
      global: 'Apis',

      // Global mount object (default: globalThis)
      globalHost: 'globalThis',

      // Filter/transform API interface functions
      handleApi: (apiDescriptor) => apiDescriptor,
    },
  ],

  // Auto-update configuration
  autoUpdate: true, // or { launchEditor: true, interval: 5 * 60 * 1000 }
});
```

> The `defineConfig` can also accept a sync or async function to allow for more dynamic configuration.

### Preset Wormhole Plugins

| Plugin            | Description                                                             | Documentation                                                          |
| ----------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `rename`          | Rename API functions and parameter names, supports camelCase/snake_case | [Docs](https://alova.js.org/resource/devtool-plugins/rename)           |
| `tagModifier`     | Modify API tag names                                                    | [Docs](https://alova.js.org/resource/devtool-plugins/tag-modifier)     |
| `payloadModifier` | Add/remove/modify API parameter types                                   | [Docs](https://alova.js.org/resource/devtool-plugins/payload-modifier) |
| `filterApi`       | Filter APIs by URL and tag matching                                     | [Docs](https://alova.js.org/resource/devtool-plugins/filter-api)       |
| `apifox`          | Auto-import Apifox projects                                             | [Docs](https://alova.js.org/resource/devtool-plugins/apifox)           |
| `importType`      | Exclude types that need customization                                   | [Docs](https://alova.js.org/resource/devtool-plugins/import-type)      |

**Usage Example**:

```js
import { rename, tagModifier } from '@alova/wormhole/plugin';

export default defineConfig({
  generator: [
    {
      plugins: [
        rename({ style: 'camelCase' }),
        tagModifier({ ... })
      ]
    }
  ]
});
```

### The handleApi Hook

Used to customize API configuration. Called before each API is generated. Can modify parameter names, types, or return types.

**Note**: The `apiDescriptor` parameter contains information for each API in the OpenAPI file. For details, refer to [OpenAPI Spec Operation Object](https://spec.openapis.org/oas/latest.html#operation-object).

**Rename function (snake_case → camelCase)**:

```js
handleApi: (apiDescriptor) => {
  apiDescriptor.operationId = apiDescriptor.operationId.replace(/_([a-z])/g, (match, group) =>
    group.toUpperCase()
  );
  return apiDescriptor;
};
```

**Modify Tags**:

```js
handleApi: (apiDescriptor) => {
  if (apiDescriptor.url.includes('/user')) {
    apiDescriptor.tags = ['userTag'];
  }
  return apiDescriptor;
};
```

**Filter APIs**:

```js
handleApi: (apiDescriptor) => {
  // Return falsy value to filter this API
  if (!apiDescriptor.path.startsWith('/user')) {
    return;
  }
  return apiDescriptor;
};
```

**Modify response data type generation**:

```js
handleApi: (apiDescriptor) => {
  apiDescriptor.responses = apiDescriptor.responses?.properties?.data;
  return apiDescriptor;
};
```

**Prefer using Wormhole plugins** over `handleApi` for modifying generated data. Plugins simplify the logic and execute in configuration order.

## Features & Reference Docs

| Feature                                     | Reference                                                     |
| ------------------------------------------- | ------------------------------------------------------------- |
| Installation & setup                        | [references/INSTALLATION](references/INSTALLATION.md)         |
| CLI usage (`alova gen`, `alova init`)       | [references/CLI](references/CLI.md)                           |
| Programmatic API (`generate`, `readConfig`) | [references/PROGRAMMATIC-API](references/PROGRAMMATIC_API.md) |
| Customizing the alova instance (`index.ts`) | [references/ALOVA-INSTANCE](references/ALOVA_INSTANCE.md)     |
| Troubleshooting                             | [references/TROUBLESHOOTING](references/TROUBLESHOOTING.md)   |
