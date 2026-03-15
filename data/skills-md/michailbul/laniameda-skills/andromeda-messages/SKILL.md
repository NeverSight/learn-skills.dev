---
name: andromeda-messages
description: >
  Add, update, delete, or list nodes in the Andromeda Galaxy page (mishabuloichyk.com).
  Also lock/unlock galaxies programmatically.

  Use when Michael asks to add a message/thought/record to any galaxy (Dreams, Life,
  Partner, Family, Antidreams), or to list/edit/delete nodes, unlock a galaxy, or check
  galaxy status.

  Keywords: add to andromeda, save to galaxy, add to dreams, add to жизнь,
  unlock your life, разблокируй семью, delete node, update node.
---

# Andromeda Messages

Full CRUD API for the Andromeda galaxy page + galaxy lock/unlock control.

**Base URL:** `https://www.mishabuloichyk.com`  
**Auth:** `Authorization: Bearer andromeda25`

---

## Galaxy Name Aliases

The `galaxy` field accepts any of these (API resolves internally):

| Send this | Resolves to |
|---|---|
| `"Your Dreams"` / `"dreams"` / `"мечты"` | sagittarius |
| `"Your Partner"` / `"partner"` / `"laniakea"` / `"партнёр"` | wormhole |
| `"Your Family"` / `"family"` / `"семья"` | carina |
| `"Your Life"` / `"life"` / `"жизнь"` | andromeda |
| `"Your Antidreams"` / `"antidreams"` / `"антимечты"` | kepler |
| Raw IDs (`sagittarius`, `wormhole`, etc.) | ✅ also work |

Always confirm with the canonical name (e.g. "Your Dreams"), never the internal ID.

---

## Node Routes (`/api/andromeda`)

### POST — Create a node
```bash
curl -s -X POST "https://www.mishabuloichyk.com/api/andromeda" \
  -H "Authorization: Bearer andromeda25" \
  -H "Content-Type: application/json" \
  -d '{"galaxy":"Your Life","title":"Short title","content":"Full message text","nodeType":"STATION"}'
```
Response: `{ success, nodeId, galaxy, title, content, nodeType }`

### GET — List nodes in a galaxy
```bash
curl -s "https://www.mishabuloichyk.com/api/andromeda?galaxy=Your+Life" \
  -H "Authorization: Bearer andromeda25"
```

### PATCH — Update a node
```bash
curl -s -X PATCH "https://www.mishabuloichyk.com/api/andromeda" \
  -H "Authorization: Bearer andromeda25" \
  -H "Content-Type: application/json" \
  -d '{"nodeId":"<id>","title":"New title","content":"New content"}'
```
All fields except `nodeId` are optional.

### DELETE — Delete a node
```bash
curl -s -X DELETE "https://www.mishabuloichyk.com/api/andromeda?nodeId=<id>" \
  -H "Authorization: Bearer andromeda25"
```

---

## Galaxy Lock Routes (`/api/andromeda/galaxy`)

### GET — List all galaxy lock states
```bash
curl -s "https://www.mishabuloichyk.com/api/andromeda/galaxy" \
  -H "Authorization: Bearer andromeda25"
```
Returns: `{ success, galaxies: [{ galaxyId, name, locked }] }`

### POST — Lock or unlock a galaxy
```bash
curl -s -X POST "https://www.mishabuloichyk.com/api/andromeda/galaxy" \
  -H "Authorization: Bearer andromeda25" \
  -H "Content-Type: application/json" \
  -d '{"galaxy":"Your Life","locked":false}'
```
Set `locked: false` to unlock, `locked: true` to lock. Changes are live immediately.

---

## nodeType options
- `STATION` (default) — main message node
- `RELAY` — connecting/transition node
- `SENSOR` — observation/detail node

---

## Workflow examples

**"Add to Your Dreams: title 'Morning Light', content '...'"**  
→ POST to `/api/andromeda`, confirm: "✅ Added to **Your Dreams** galaxy."

**"Unlock Your Life"**  
→ POST to `/api/andromeda/galaxy` with `{"galaxy":"Your Life","locked":false}`

**"List all nodes in Your Family"**  
→ GET `/api/andromeda?galaxy=Your+Family`, present as list

**"Delete the node with id X"**  
→ DELETE `/api/andromeda?nodeId=X`

**"Update title of node X to '...'"**  
→ PATCH `/api/andromeda` with `{ nodeId, title }`

---

## Notes
- Changes are live immediately — Convex realtime, no reload needed
- Galaxy lock state is now stored in Convex (`galaxySettings` table), not hardcoded
- Node positions auto-randomized across 3D sphere shell (radius 8–18 units)
- Admin UI: `/admin/andromeda` on the site
