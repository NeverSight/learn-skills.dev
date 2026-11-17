---
name: follow-arcgis-authentication-patterns
description: Use when designing ArcGIS applications, selecting ArcGIS products, or choosing and implementing API key, user, or app authentication based on app audience, ArcGIS foundational product, and resources and operations the app uses.
license: Apache-2.0
---

# ArcGIS authentication and development patterns

Understand authentication in ArcGIS and provide guidance on the correct type of authentication to use in different situations. Application requirements, ArcGIS product selection, and authentication strategy are closely connected and should be considered together when designing an application. Treat audience, technology stack, services, and foundational ArcGIS product as related but independent design dimensions. Do not infer authentication from the platform or SDK alone.

## Application requirements

If the application's development requirements are unclear, use the `gather-arcgis-application-requirements` skill to review project context and clarify consequential unknowns before proceeding. Then apply this skill's technology-specific guidance, reusing requirements already clear from the request or project.

## Workflow

Follow this sequence and record any assumptions:

1. **Identify the audience explicitly.** Ask whether the app is for anyone, members of an organization, or only its owner. If this is not stated by the user or clearly documented as a requirement, treat it as unknown and ask before recommending or implementing authentication.
2. **Identify sign-in behavior.** Ask whether users must sign in. Do not infer a public audience from the absence of a stated sign-in requirement, a public URL, public data, or the choice of SDK.
3. **Identify the foundational product.** ArcGIS Location Platform is developer-focused; ArcGIS Online or ArcGIS Enterprise is generally used for multi-user private access, organization governance, or when protected portal content is required. Enterprise deployment also depends on network boundaries, identity provider, licensing, and policy.
4. **Identify required resources and operations.** List public or protected items, data and location services, user-specific content, editing, analysis, and administrative actions.
5. **Verify sharing and privileges.** Ensure item sharing and service access match the audience. If confidentiality is uncertain, choose a more secure server-side or user-authenticated design rather than weakening sharing.
6. **Assess the execution environment.** Browser and mobile credentials are exposed to users, while a trusted server can keep confidential app credentials secure.
7. **Choose authentication.** Use API keys for suitable public or personal access, user authentication for individual identity and private user access, and app authentication for trusted server-side application identity. Verify service requirements and product support.
8. **Implement authentication**: Instruct the users to create developer credentials for their chosen authentication type, state any privileges or configurations required for the developer credentials, and implement authentication using the appropriate ArcGIS Maps SDK or API. Use the MCP to look up the SDK/API documentation on how to implement authentication correctly.

### Types of applications and use cases

Classify by audience first, then use the examples to connect that classification to a suitable authentication direction.

| Types of application | Audience | Use cases | Authentication direction |
| --- | --- | --- | --- |
| Public | Anyone may use the app anonymously, without signing in with an ArcGIS account. | A public-facing map that uses location services or public data | Use API key authentication when requests are made directly to ArcGIS (without a backend service), or use app authentication when making requests through a custom backend. |
| Private | Users must sign in with ArcGIS accounts and be authorized, commonly as members of an ArcGIS organization. | An internal tool analyzes secure data or supports editing and user-specific workflows. | User authentication; the signed-in user's user type, role, privileges, and resource sharing determine access. |
| Personal | Only the owner uses the app; it is not distributed to others. | A local script, notebook, automation, or developer tool/MCP server performs work for its owner. | User authentication when it must act as the owner; app authentication or an API key may fit other tasks. |

Note: A public application is not the same as public data. Decide separately whether the app can be used anonymously and whether each item or service may be shared with **Everyone (public)**. Public apps must not expose confidential or personally identifying information. Third-party sign-in to an app does not, by itself, authenticate users to ArcGIS or grant access to protected ArcGIS resources; verify the complete identity and authorization design.

## Product selection guidance

- ArcGIS Location Platform is developer-focused and commonly used for public-facing applications and location services. Confirm current commercial deployment terms and service availability for the specific use case.
- ArcGIS Online provides hosted organization identities, portal content, groups, roles, and sharing controls.
- ArcGIS Enterprise provides portal and services in infrastructure controlled by the organization; deployment also depends on network boundaries, identity providers, licensing, and organizational policy.
- ArcGIS Experience Builder, Instant Apps, and similar app builders are tools used with a foundational ArcGIS product, such as ArcGIS Online and ArcGIS Enterprise, not standalone foundational products.

## Application type, ArcGIS product, and authentication matrix

Use this matrix as an initial direction, not as a substitute for checking product configuration, service-specific requirements, or current documentation.

| Foundational product | Public application | Private application | Personal application |
| --- | --- | --- | --- |
| ArcGIS Online | App authentication or API key authentication. A public app using only publicly shared items and resources may omit ArcGIS authentication. | User authentication for organization members and secure hosted data. | User authentication, app authentication, or API key authentication. |
| ArcGIS Enterprise | App authentication or API key authentication. A public app using only publicly shared items and resources may omit ArcGIS authentication. | User authentication for organization members and secure hosted data. | User authentication, app authentication, or API key authentication. If using web-tier auth or SAML-based SSO, the requirements may differ. |
| ArcGIS Location Platform | App authentication or API key authentication for public-facing applications and location services. | Not shown as a private-organization application pattern in this guide; assess whether ArcGIS Online or Enterprise is needed for organizational identities and protected portal content. | User authentication, app authentication, or API key authentication. |

If an application does not implement authentication and then attempts to access secure resources, some products may prompt users to sign in using an automatic authentication flow. This is non-standard and is not recommended for production applications. If users need to sign in to an application, implement OAuth 2.0 user authentication instead.

## Authentication scenarios

Use these scenarios as starting points when matching the application's audience to the kind of secure resource and operation it needs. 

| Resource or operation | Public application | Private application | Personal application |
| --- | --- | --- | --- |
| **Private data** | Use caution. App authentication may be appropriate only through a trusted backend that limits and authorizes requests; do not expose confidential data to an uncontrolled public audience. If users need protected access as themselves, make the app private and use user authentication. | Use user authentication so access reflects the signed-in user's privileges and the item's sharing settings. | Any supported flow may fit owner-controlled data, depending on the required identity and runtime. API keys or app authentication can access some owner-owned private items, but do not use them to protect confidential or sensitive data. |
| **ArcGIS services** | API key authentication is a common choice for suitable client-side access. App authentication can be used through a trusted backend. Check the exact service's authentication and usage requirements. | Use user authentication when requests must run as the signed-in user; otherwise, choose a supported method based on the service and product. | Use a supported method appropriate to the service and operation; API key authentication is often suitable for owner-directed workflows. |
| **Portal management** | Not recommended for an anonymously usable app. Keep administrative credentials on a trusted server, restrict and authorize access to that server, or require user sign-in. | Use user authentication so operations run with the signed-in user's privileges; verify that the user has the required administrative privileges. | API key authentication may support owner-directed portal operations when the credential has the required privileges and the operation supports it. Protect the key as a highly sensitive credential; user or app authentication may be more appropriate for some workflows. |

Treat "private data" carefully: an authentication token does not make sensitive data safe to expose. API key or app authentication against owner-owned items is not a substitute for user-specific authorization or a properly secured backend.

When a pattern does not clearly fit, ask about audience, identity, protected data, operations, runtime, and product before recommending credentials.

## Security best practices

- Never place app secrets or other confidential credentials in browser or mobile client code. Client-distributed values should be considered exposed.
- For API keys used by client applications, use the smallest required privileges, configure referrer restrictions where supported, and rotate keys as needed.
- Prefer a trusted server-side component for operations that require confidential app credentials. Protect the server and validate requests before brokering access.
- Use user authentication when access must reflect an individual user's identity, privileges, or private organization content. For personal applications for the owner-only, an API key that impersonates their identity may also be used.
- Align item and service sharing with the intended audience. Do not put confidential or personally identifying data in a public app or make protected resources public as a workaround
- For private applications, account roles and privileges govern what users can do; do not imply that signing in alone grants access to every resource.

## Recommendation format

When advising on an application design, summarize:

- **Classification:** public, private, or personal, and why.
- **Authentication direction:** API key, user authentication, or server-side app authentication.
- **Data access:** which items/services must be public, organization-only, or owner-only.
- **Credential safeguards:** where credentials live, applicable restrictions, and rotation or server-side handling.

## Verification checklist

Before finalizing an authentication recommendation or implementation, verify:

- [ ] The audience is classified as public, private, or personal based on who can use the app and whether ArcGIS sign-in is required.
- [ ] The foundational ArcGIS product, target runtime, accessed services and items, and required operations are identified; authentication was not inferred from the SDK alone.
- [ ] The authentication method is supported by the selected product, portal version, service, and client library, and matches the identity the requests must use.
- [ ] Item and service sharing, user privileges, and credential privileges are limited to the intended audience and required operations; protected content was not made public as a workaround.
- [ ] API keys use least privilege and applicable referrer restrictions, expiration, monitoring, and rotation.
- [ ] User authentication uses the appropriate OAuth flow for the client, with registered redirect URIs and SDK/library-recommended session handling.
- [ ] Assumptions, unresolved questions, and relevant Enterprise identity/version constraints are stated.

## Documentation access

Installing this skill individually does not configure **Esri MCP server for developer documentation** (`esri-mcp-server-for-developer-documentation`). Add that server at `https://developers-mcp.arcgis.com/mcp` using your client's MCP settings, or install the full **ArcGIS SDKs and APIs** plugin (`arcgis-sdks-and-apis-plugin`). If the MCP server is unavailable, consult the linked official Esri documentation.

## References

- [Security and authentication guide](https://developers.arcgis.com/documentation/security-and-authentication/)
- [Introduction: types of applications and secure resources](https://developers.arcgis.com/documentation/security-and-authentication/introduction/)
- [Public application](https://developers.arcgis.com/documentation/glossary/public-application/), [private application](https://developers.arcgis.com/documentation/glossary/private-application/), and [personal application](https://developers.arcgis.com/documentation/glossary/personal-application/)
- [Types of authentication and selection guidance](https://developers.arcgis.com/documentation/security-and-authentication/types-of-authentication/)
- [How to use authentication](https://developers.arcgis.com/documentation/security-and-authentication/how-to-use-authentication/)
- [API key authentication](https://developers.arcgis.com/documentation/security-and-authentication/api-key-authentication/) and [API key credentials](https://developers.arcgis.com/documentation/security-and-authentication/api-key-authentication/api-key-credentials/)
- [User authentication](https://developers.arcgis.com/documentation/security-and-authentication/user-authentication/) and [authorization code flow with PKCE](https://developers.arcgis.com/documentation/security-and-authentication/user-authentication/flows/authorization-code-with-pkce/)
- [App authentication](https://developers.arcgis.com/documentation/security-and-authentication/app-authentication/) and [client credentials flow](https://developers.arcgis.com/documentation/security-and-authentication/app-authentication/client-credentials-flow/)