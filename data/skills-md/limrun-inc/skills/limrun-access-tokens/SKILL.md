---
name: limrun-access-tokens
description: "Create and revoke Limrun access tokens through the CLI or TypeScript SDK. Use when delegating temporary instance control, interactive streaming, asset access, device installation, or service access, or choosing permissions and token lifetimes."
---

# Limrun access tokens

Mint an access token to give another client temporary access without sharing an
organization API key. Use the permission and lifetime needed for the requested
task. Creating a token does not create an instance or asset.

## Authentication

Use `lim login` or an existing `LIM_API_KEY`. Install the CLI if needed with
`npm install --global lim`. If a command or flag is unavailable, check
`lim access-token create --help` or `lim access-token revoke --help` and the
installed CLI version.

The caller needs `accesstoken:*:all` and must hold every permission it delegates.
An access token cannot expand the caller's permissions. Permission strings use
`resource:target:action`; the action wildcard is `all`, not `*`.

## Choose permissions

For an existing instance, use its returned ID exactly:

| Instance | Resource and ID prefix | Accepted actions |
| --- | --- | --- |
| iOS simulator | `ios`, `ios_` | `stream`, `all` |
| Android emulator | `android`, `android_` | `stream`, `all` |
| Xcode sandbox | `xcode`, `sandbox_` | `all` |
| Gradle sandbox | `gradle`, `gradle_` | `all` |

`stream` permits interactive streaming, including touch and typing. Give the
client the token and `status.endpointWebSocketUrl`. It cannot install or
explicitly launch apps, use the device API or ADB, or fetch the instance record.

`all` permits full control through the instance's endpoints, including streaming
where supported. Give a device or build client the token and `status.apiUrl`.
Have the trusted backend supply the endpoint URL alongside either token; access
tokens are not a replacement for an API key across all SDK methods.

Instance grants require a concrete ID. They do not grant organization-wide
listing, instance creation, deletion, or role updates. Access-token create
rejects instance `read`, `work`, and `tunnel` actions; the latter two belong to
specialized build and private-tunnel flows.

Other accepted grants include:

| Permission | Purpose |
| --- | --- |
| `asset:<target>:<action>` | Asset access. Targets can be an asset ID, `name/<name-or-pattern>`, or `*`. Actions are `read`, `create`, `upload`, `update`, `delete`, and `all`; `create` requires a name target or `*`. |
| `device:*:install` | Physical-device installation; also needs `asset:<target>:read` for the asset. |
| `applerelay:*:connect` | Apple Account authentication relay access. |
| `remotecache:*:read` or `remotecache:*:all` | Read the organization's Bazel cache, or read and write it. |
| `remoteexecution:*:all` | Execute actions through the organization's Bazel service. |

For asset pattern delegation, organization roles, or workload-role permissions,
consult [Permissions and access tokens](https://docs.limrun.com/docs/reference/permissions).
Workload roles grant asset access from inside an instance; they do not grant
another client control of it.

## Create and revoke with the CLI

```bash
lim access-token create \
  --permission "ios:$INSTANCE_ID:stream" \
  --ttl-seconds 900 \
  --json
```

Use `all` for full instance control. Repeat `--permission` to combine grants,
for example an asset read permission and `device:*:install`.

The JSON response includes `id`, `token`, `permissions`, and `expiresAt`.
Save `id` for revocation and pass `token` to the intended client.
`--quiet` prints only the token; `--quiet --json` keeps the JSON response.

```bash
lim access-token revoke "$TOKEN_ID"
# Or pass the token itself:
lim access-token revoke "$ACCESS_TOKEN"
```

CLI revocation accepts the returned ID or the `lim_st_...` token value. It
extracts the token's JWT `jti` and sends only that ID, authenticated with your
API key or login. Tokens without a `jti`, including `status.token` and
`status.streamToken`, cannot be revoked this way. Output contains the resolved
ID, not the supplied token. Repeating a revoke call is safe. A failed request
is not confirmation of revocation.

## TypeScript SDK

```ts
import Limrun from '@limrun/api';

const lim = new Limrun(); // Reads LIM_API_KEY.
const access = await lim.accessTokens.create({
  permissions: [`xcode:${instance.metadata.id}:all`],
  ttlSeconds: 900,
});

// Give the build client instance.status.apiUrl and access.token.
// When the credential is no longer needed:
await lim.accessTokens.revoke(access.id);
```

The SDK revoke method takes an ID. Use `accessTokens` and `permissions` in new integrations. For REST, the matching
routes are `POST /v1/access_tokens` and `DELETE /v1/access_tokens/{id}`;
authenticate with the API key in the Authorization Bearer header.

## Lifetime and revocation

Tokens created with an API key or CLI login default to one hour.
`--ttl-seconds` and `ttlSeconds` accept integers from 1 through 14,400.

The management and registry APIs check revocation after it propagates. Instance
endpoints verify tokens offline and continue accepting them until expiry or
instance termination. Revocation does not close existing connections or
terminate the instance. Choose the lifetime with these limits in mind.
