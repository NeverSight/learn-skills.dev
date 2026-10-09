---
name: asset-access-control
description: "Share or revoke access on ImageKit files, folders, and media collections via DAM MCP. Use when the user asks who can see an asset, to grant READ/CONTRIBUTE/MANAGE, or to add/remove a user or group from an ACL."
---

# Asset access control

Use the **DAM MCP** tools. Two surfaces — do not mix their tools.

| Target | Read ACL | Write ACL |
|--------|----------|-----------|
| File or folder | `build_access_list` | `update_asset_acl` |
| Media collection | `get_collection_access_list` | `update_media_collection` (`acl`) |

`list_associated_media_collections` only answers "which collections contain this file/folder?". It does not change membership; use `add_assets_to_media_collection` / `remove_assets_from_media_collection`.

Restricted users can only change access on assets they can manage.

## Workflow

1. Resolve the asset with `search_media_library` if you only have a name or path.
2. Read the current ACL. Use `userId` / `groupId` from that response — never invent ids.
3. Write the change. Then re-read if you need to confirm.

`build_access_list` also returns `users` and `userGroups` for the account. Match the person the user named against `userName` / `userEmail` / `label`.

## `update_asset_acl`

- Always send **both** `acl.addOrModify` and `acl.remove`. Use `[]` on the unused side.
- `entity.type` is only `USER` or `USER_GROUP`. `MEDIA_COLLECTION` may appear on read (inherited membership); do not send it on write.
- Do not change the asset owner's entry.
- Do not grant less than a parent folder already grants that same entity.

```json
{
  "assetId": "<file-or-folder-id>",
  "acl": {
    "addOrModify": [{ "entity": { "id": "<userId>", "type": "USER" }, "permission": "READ" }],
    "remove": []
  }
}
```

## `list_associated_media_collections`

`permission` is a **string**, not an array. Send `'["MANAGE"]'` or `'["READ","CONTRIBUTE"]'`. Omit it unless you are filtering for a restricted user.
