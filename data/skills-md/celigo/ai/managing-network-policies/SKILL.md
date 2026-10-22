---
name: managing-network-policies
description: Manage Celigo network policies -- named IP allow and deny lists that restrict where API tokens, MCP servers, and workspace-user or end-user sign-in may connect from. Covers how a policy decides, the four places one is assigned, patch versus full-replace edits, deleting a policy that is still assigned, and avoiding locking yourself out. Use when restricting an MCP server, a token, or sign-in to known networks, editing or deleting a policy, or checking whether a policy explains a refused caller.
---

<!-- TIER:1 -->

# Managing Network Policies

A network policy is a **named pair of IP lists** -- addresses allowed to connect and addresses always refused -- kept per environment and assigned wherever access should be limited by source address. One policy can guard many things, and a policy guards nothing until it is assigned. Concerns when managing network policies:

- **What a policy decides** -- deny beats allow, and an empty allow list admits everything the deny list doesn't name
- **Where it applies** -- an MCP server, an account API token, workspace-user sign-in, or end-user sign-in
- **Editing safely** -- a patch changes only what you name; a full replace empties every list it leaves out
- **Deleting** -- an assigned policy is refused unless forced, and forcing lifts every restriction it imposed
- **Lockout** -- a policy on the token or sign-in you are using applies to you

Only the account owner and administrators manage network policies, and the feature must be enabled for the account. Each environment (production, a sandbox) keeps its own library: a policy is visible and assignable only in the environment that created it.

## How to Run the Steps

This skill names each step by what it reads or changes; the exact calls depend on how you reach the account. Read the one reference that matches your tools -- both follow the step numbers of How to Manage Network Policies below:

- **Celigo MCP tools** -- [references/mcp.md](references/mcp.md). The deployed server has no network-policy tools: it can only assign or clear a policy on an MCP server, so most steps go to the CLI or the integrator.io UI.
- **The `celigo` CLI** -- [references/cli.md](references/cli.md)

Assigning a policy to an API token or to sign-in happens only in the integrator.io UI, on either surface.

## How a Policy Decides

- **Entries** are IPv4 or IPv6 addresses or CIDR ranges (`203.0.113.5`, `10.0.0.0/8`, `2001:db8::/32`), at most 200 per list. A bare address is stored as `/32` or `/128` and IPv6 is compressed and lowercased, so compare against the stored form a read returns, not what you sent.
- **Deny always wins.** An address on `ipDenyList` is refused even when `ipAllowList` covers it.
- **An empty allow list admits every address the deny list doesn't block.** A deny-only policy blocks a few addresses and lets everything else through; a policy with both lists empty restricts nothing, even when assigned.
- **The address checked is where the request comes from**, so list a VPN's or proxy's egress range rather than people's own machines.

## Where a Policy Applies

| Assigned to | Where it's set | What it restricts |
|---|---|---|
| An MCP server | The server's `_networkPolicyId` -- CLI or MCP | Every MCP protocol request to that server |
| An account API token | The token's network policy, in the integrator.io UI (the token API refuses bearer callers) | Every request authenticated with that token |
| Workspace-user sign-in | Account security settings, UI only | Workspace users signing in to that environment. Personal access tokens have no policy of their own and follow this one |
| End-user sign-in | Account security settings, UI only | MCP end users signing in |

A policy's assignments are listed by its dependencies read: the MCP servers and API tokens that carry it, and whether it restricts workspace-user or end-user sign-in, per environment. An empty result means the policy restricts nothing and deletes without force.

## Quick Reference

### Decision Matrix

| You need to... | Do this |
|---|---|
| Limit one MCP server to known networks | Assign an allow-list policy to the server |
| Limit a service token (CI, a partner's script) | Assign a policy to the token in the UI |
| Limit where people can sign in from | Assign a policy to workspace-user sign-in in the UI; personal access tokens follow it |
| Limit where MCP end users can sign in from | Assign a policy to end-user sign-in in the UI |
| Refuse a few known-bad addresses, admit the rest | A deny-only policy (empty `ipAllowList`) |
| Change a range on every place a policy guards | Edit the policy once -- the change applies everywhere it's assigned |

### Minimum Fields

- `name` -- required, at most 150 characters, unique among the environment's live policies. Name it after the network ("Corporate VPN egress"), not after what it guards: one policy serves many assignments.
- `ipAllowList`, `ipDenyList` -- at most 200 entries each; omit a list only on create.
- `description` -- optional, at most 500 characters: what the ranges are and where they come from.

### Field Reference

The full request, response and assignment shapes are in the API reference's [Network Policies](https://developer.celigo.com/api/api-reference/account-and-admin/network-policies.md) page (agent-readable markdown). The assignments read returns `mcpservers` and `accesstokens` (each `{_id, name}`) and `account` -- `workspaceUsers` and `endUsers` flags with the environments each applies to.

## Related Skills

- [managing-api-tokens > Where Tokens Are Managed](../managing-api-tokens/SKILL.md#where-tokens-are-managed) -- a token's network policy is set in the UI with its other settings
- [building-mcp-servers > Authentication and Scoping](../building-mcp-servers/SKILL.md#authentication-and-scoping) -- the server's `_networkPolicyId` sits beside its sign-in and grants
- [managing-users > Access Strategies](../managing-users/SKILL.md#access-strategies) -- workspace users, whose sign-in (and personal access tokens) a policy can restrict
- [managing-end-users > How Access Composes](../managing-end-users/SKILL.md#how-access-composes) -- MCP end users, whose sign-in a policy can restrict

<!-- TIER:2 -->

## How to Manage Network Policies

### 1. Check what exists and where it's assigned

List the environment's policies, then read the assignments of any you might change. A policy assigned to nothing restricts nothing -- it isn't the reason a caller is refused, and it deletes without force.

### 2. Decide the lists -- and check for lockout

Allow the networks that should reach the thing you're guarding; deny addresses to refuse even inside an allowed range.

Before you assign a policy, or edit one already assigned, check whether it covers **your own access**: the API token your CLI profile, script or MCP client signs in with, or workspace-user sign-in (which personal access tokens follow). If it does, keep the address you connect from on the allow list. An allow list that leaves it out locks that caller -- and every script using the same token -- out until someone repairs the policy from the UI or with another token.

### 3. Create the policy

Create it with a name, a description, and both lists. Read the response: entries come back in stored form. A live policy with the same name is refused with 409 `conflict`; an entry that isn't an address or CIDR range (a hostname, an empty string, a prefix longer than the address family allows) with 400 `invalid_cidr`; a list over 200 entries with 400 `max_cidr_entries_exceeded`.

### 4. Assign it

- **MCP server** -- set the server's `_networkPolicyId` to the policy's `_id`. It must be a policy from the same environment (otherwise 422 `invalid_ref`).
- **API token or sign-in** -- in the integrator.io UI: give the user the policy's name and where to pick it.

Then read the policy's assignments to confirm.

### 5. Edit a policy

An edit applies at once to everything the policy is assigned to.

- **Patch** the fields you're changing -- `name`, `description`, `ipAllowList`, `ipDenyList`. A list you send replaces that whole list; the other fields keep their values.
- **A full replace clears whatever it omits**, with no error: a list left out comes back empty -- lifting every restriction it imposed -- and a description left out is removed. If you replace, read the policy first and send `name`, `description` and both lists.
- **To drop one entry**, send the whole list without it; removing a single entry by index is refused (422).

### 6. Unassign or delete

- **Unassign from an MCP server** by removing its `_networkPolicyId` (a patch `remove`, or `null` on a full update). A full update that leaves `_networkPolicyId` out keeps it.
- **Delete** an unassigned policy and it's gone from reads (404); its name is free to reuse. An assigned policy is refused with 409 `network_policy_in_use`, listing every assignment, and nothing changes. **Forcing** the delete clears the policy from every MCP server, token and sign-in setting first, so each of them loses the restriction -- read the assignments before you force, and keep that list: the clear leaves no entry in an MCP server's own change history.
- **Keep the lists before deleting.** A deleted policy is meant to wait 30 days in the recycle bin, but the bin can't find deleted policies today (see Gotchas), so treat a delete as final and recreate the policy from the copy if needed. Its change history stays in the account audit log under resource type `networkpolicy`, though the policy's own audit route answers 404 once it's deleted.

### 7. Check whether a policy explains a refused caller

Work out which policies apply to the call -- the MCP server's `_networkPolicyId`, the token's policy (shown in the UI), the sign-in settings -- read their lists, and compare them with the address the caller connects from (for someone on a VPN, its egress). Remember that deny wins and that every applicable policy has to admit the caller. A caller refused while no assigned policy covers its address is refused for another reason: see the guarding resource's own skill.

<!-- TIER:3 -->

## Pre-Submit Checklist

Before creating, assigning, editing, or deleting a policy, verify:

- [ ] Every entry is an IPv4/IPv6 address or CIDR range, and neither list exceeds 200 entries
- [ ] The name isn't used by another live policy in this environment, and it names the network, not the resource
- [ ] Nothing it covers is your own access -- the token your profile, script or client uses, or workspace-user sign-in -- or your egress address is on its allow list
- [ ] An edit is a patch of the fields you mean, or a full replace that carries `name`, `description` and both lists
- [ ] An MCP server assignment uses a policy from the same environment, and the policy's assignments show it afterwards
- [ ] Before deleting: the assignments are read; force only when every one of them should lose the restriction; the lists are saved somewhere

## Gotchas

1. **A policy restricts nothing until it's assigned.** Creating one changes no access. And an assigned policy whose lists are both empty restricts nothing either.
2. **A full replace empties what it omits.** A rename sent as a full replace with only `name` comes back with both lists empty and no description -- 200, no warning -- silently lifting every restriction everywhere the policy is assigned. Patch instead.
3. **Deny wins, and an empty allow list means "everyone else".** One deny entry inside an allowed range blocks it; a deny-only policy admits every other address.
4. **You can lock yourself out.** A policy on the token your CLI profile or script uses applies to it, and workspace-user sign-in policy binds personal access tokens too. Keep your own egress address allowed, and check a policy's assignments before editing it.
5. **Names match exactly.** Uniqueness is per environment, among live policies, and case-sensitive: "Corp VPN" and "CORP VPN" can both exist. A deleted policy's name can be reused at once.
6. **A forced delete lifts every restriction, quietly.** Each former assignee is unrestricted afterwards, and the clear isn't recorded on the MCP servers it touched -- only the policy's delete appears in the account audit log.
7. **The recycle bin can't restore a deleted policy today.** Its listing holds the environment's *live* policies and leaves the deleted ones out, so a deleted policy can't be found there to restore or purge, and restore and purge refuse the live ones (live-verified 2026-10-21). Don't act on the bin's network-policy entries; keep a copy of a policy's lists before deleting it.
8. **An MCP server keeps its policy through a full update that omits it.** Unlike the server's arrays, an omitted `_networkPolicyId` keeps its stored value; clear it with a patch `remove` or by sending `null`.
9. **Environments don't share policies.** A policy from production can't be assigned to a sandbox resource (422 `invalid_ref`); create one in each environment.

## Common Errors

| Error | Likely Cause | Fix |
|---|---|---|
| 409 `conflict` "A network policy with this name already exists in the account." | A live policy in this environment has exactly that name | Pick another name, or edit the existing policy |
| 400 `invalid_cidr` "Enter a valid IP address or CIDR range (e.g., 192.168.1.0/24)." | A hostname, empty string, number, or a prefix longer than the address family allows | Write each entry as an address or CIDR range |
| 400 `max_cidr_entries_exceeded` "A list can contain at most 200 entries." | More than 200 entries in one list | Consolidate addresses into CIDR ranges |
| 409 `network_policy_in_use` "This policy is assigned to N resources. Deleting it removes those restrictions." | Deleting a policy that is still assigned | Read its assignments; unassign it, or force the delete if every assignee should lose the restriction |
| 422 `invalid_ref` on `_networkPolicyId` | The policy belongs to another environment, or doesn't exist | Use a policy from the server's own environment |
| 422 "Remove at array index is not supported" | A patch `remove` on one list entry | Replace the whole list without that entry |
| 422 "missing 'value' property" | A patch `replace` of `_networkPolicyId` with `null` | Use a patch `remove` to unassign |
| 404 "NetworkPolicy not found" | The policy was deleted, or belongs to another environment | List the environment's policies; recreate a deleted one from its saved lists |
| A policy's lists came back empty after an edit | A full replace left them out | Patch the lists back from your copy or the audit log's old values |
