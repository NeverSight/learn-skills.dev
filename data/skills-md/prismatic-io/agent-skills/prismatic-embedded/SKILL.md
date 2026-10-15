---
name: prismatic-embedded
description: Embed Prismatic in a customer-facing web application, including a backend endpoint that signs embedded-user JWTs, frontend setup of the @prismatic-io/embedded SDK, and the integration marketplace or other embedded screens. Use when a user wants their customers to find, activate, or configure integrations inside the user's own app, or asks about embedded authentication, signing keys, or the embedded SDK.
compatibility: Requires Node.js 22+, npm, Prism CLI (npm package @prismatic-io/prism) v11 or higher on PATH, and network access to documentation and packages. Platform operations also require Prismatic authentication and any connections needed for the intended environment.
---

# Embed Prismatic

Embedding lets the user's customers manage integrations without leaving the
user's app. The backend signs a short-lived JWT for the signed-in user; the
browser passes it to the `@prismatic-io/embedded` SDK, which renders Prismatic
screens in an iframe. Use the [embedding docs](https://prismatic.io/docs/embed/)
and the installed SDK's public types for current behavior, and `prism --llms`
and command `--help` to discover Prism's organization and signing-key commands.

Start from the user's request and the current application. Identify the
frontend framework, the backend, the existing authentication and session
model, how a user maps to a tenant, where configuration and secrets come from,
and the existing tests. Extend the app's own patterns: its router, auth
middleware, API client, config module, and test setup. Infer technical choices
from the code. Ask only about business decisions the code cannot answer, such
as which app tenant is a Prismatic customer, which screens to embed, where they
go, and who may see them.

Sign tokens on a server the user controls; read
[authentication](references/authentication.md) before writing the endpoint. A
private key in browser code, a browser-visible environment variable, or a
client bundle lets anyone mint tokens for any customer. When asked to sign in
the browser, explain this in plain terms and add the smallest backend endpoint
the app supports.

Protect the endpoint with the app's existing authentication. Take the user and
customer identity only from the authenticated session, never from query
parameters, request bodies, or headers the browser controls. Use stable IDs:
the user's ID for `sub` and the tenant's Prismatic customer external ID for
`customer`. Read the private key and organization ID from the app's
server-side configuration, and fail with a clear server error when either is
missing, without logging the key. Return the token and its expiry.

The organization ID is on the Embedded tab of Prismatic's organization
settings; `prism me` also prints it. A real private key must never appear in
the project, command output, logs, responses, or your messages. For tests,
generate a throwaway key pair in the test instead of committing one.

Creating, importing, or deleting signing keys changes the Prismatic
organization. Do it only when the user asks; otherwise give them the steps in
[authentication](references/authentication.md#signing-keys). When asked to
create a key, run Prism's signing-key `generate` command with
`--private-key-file` set to a new path outside the repository, then tell the
user where the file is and let them move the key into their secret store. Do
not read, print, copy, or load the file, including into a shell variable or
the app for a smoke test; test with a throwaway key pair instead. If the
installed Prism has no `--private-key-file` option, do not run `generate`;
give the user the steps instead.

Read [browser SDK](references/sdk.md) before writing frontend code. The SDK
keeps one global session, so give it three separate lifetimes. Initialize once
per page load, outside component mount and unmount: `init` and `dispose` both
clear the token, so a remount that repeats either one, such as React
StrictMode's double effect, loses the session. Keep the session alive by
fetching a token, calling `authenticate`, and scheduling the next refresh
before expiry; a refresh calls only `authenticate`, because calling the screen
method again reloads the iframe. Render the screen once, after the first
successful authentication and after its container is mounted. Show a visible
error when fetching or authenticating fails, and set `prismaticUrl` when the
organization is not on `https://app.prismatic.io`.

Match the host app's look. Read [theming](references/theming.md), find the
app's colors, font, and dark-mode mechanism, and pass what the SDK supports:
the current light or dark mode, a Google font, and loading-screen colors.
Brand colors live in the organization's theme, which affects every customer;
hand off the values for it instead of changing it unless the user asks. For
filters, translations, other screens, the workflow builder, or a custom
marketplace UI, check the SDK types and the matching page under the embedding
docs, and add only what the user asked for.

Test the token endpoint without Prismatic: sign with a generated key pair,
verify the signature with the public key, and assert every required claim on
the decoded token rather than on the payload you passed in, because library
options can drop or overwrite claims. Check that unauthenticated requests are
rejected and that browser-supplied identity values are ignored. Test frontend
logic against a mocked SDK where the app has a frontend test setup. Run the
app's typecheck, lint, tests, and build, then start the backend the way the app
runs it and request a token: test runners can load modules that the app's own
runtime rejects.

Do not call Prismatic APIs, register keys, or change organization settings
unless the user asked. Report what changed, the configuration to set, the
signing-key steps that remain, where the embedded screen appears, and what was
verified locally. When you matched the app's look, include the organization
theme values for Embedded Light and Embedded Dark from
[theming](references/theming.md), with their source files. State that a real
sign-in needs a registered key and the real organization ID.
