---
name: applesauce-common
description: This skill should be used when working with applesauce-common library for social/NIP-specific helpers, casting system, blueprints, and operations. New in applesauce v5 - contains helpers that moved from applesauce-core.
---

# applesauce-common Skill (v5)

This skill provides comprehensive knowledge for working with applesauce-common, a new package in applesauce v5 that contains social/NIP-specific utilities, the casting system, blueprints, and operations.

**Note**: applesauce-common was introduced in v5. Many helpers that were previously in `applesauce-core/helpers` have moved here.

## When to Use This Skill

Use this skill when:
- Working with article, highlight, threading, zap, or reaction helpers
- Using the casting system for typed event access
- Creating events with blueprints
- Modifying events with operations
- Working with NIP-specific social features

## Package Structure

```
applesauce-common/
├── helpers/          # Social/NIP-specific helpers
│   ├── article.js    # NIP-23 article helpers
│   ├── highlight.js  # NIP-84 highlight helpers
│   ├── threading.js  # NIP-10 thread helpers
│   ├── comment.js    # NIP-22 comment helpers
│   ├── zap.js        # NIP-57 zap helpers
│   ├── reaction.js   # NIP-25 reaction helpers
│   ├── lists.js      # NIP-51 list helpers
│   └── ...
├── casts/            # Typed event classes
│   ├── Note.js
│   ├── User.js
│   ├── Profile.js
│   ├── Article.js
│   └── ...
├── blueprints/       # Event creation blueprints
└── operations/       # Event modification operations
```

## Helpers (Migrated from applesauce-core)

### Article Helpers (NIP-23)

```typescript
import {
  getArticleTitle,
  getArticleSummary,
  getArticleImage,
  getArticlePublished
} from 'applesauce-common/helpers/article';

// All helpers cache internally - no useMemo needed
const title = getArticleTitle(event);
const summary = getArticleSummary(event);
const image = getArticleImage(event);
const publishedAt = getArticlePublished(event);
```

### Highlight Helpers (NIP-84)

```typescript
import {
  getHighlightText,
  getHighlightSourceUrl,
  getHighlightSourceEventPointer,
  getHighlightSourceAddressPointer,
  getHighlightContext,
  getHighlightComment
} from 'applesauce-common/helpers/highlight';

const text = getHighlightText(event);
const sourceUrl = getHighlightSourceUrl(event);
const eventPointer = getHighlightSourceEventPointer(event);
const addressPointer = getHighlightSourceAddressPointer(event);
const context = getHighlightContext(event);
const comment = getHighlightComment(event);
```

### Threading Helpers (NIP-10)

```typescript
import { getNip10References } from 'applesauce-common/helpers/threading';

// Parse NIP-10 thread structure
const refs = getNip10References(event);

if (refs.root) {
  console.log('Root event:', refs.root.e);
  console.log('Root address:', refs.root.a);
}

if (refs.reply) {
  console.log('Reply to:', refs.reply.e);
}
```

### Comment Helpers (NIP-22)

```typescript
import { getCommentReplyPointer } from 'applesauce-common/helpers/comment';

const pointer = getCommentReplyPointer(event);
if (pointer) {
  // Handle reply target
}
```

### Zap Helpers (NIP-57)

```typescript
import {
  getZapAmount,
  getZapSender,
  getZapRecipient,
  getZapComment
} from 'applesauce-common/helpers/zap';

const amount = getZapAmount(event);     // In millisats
const sender = getZapSender(event);     // Pubkey
const recipient = getZapRecipient(event);
const comment = getZapComment(event);
```

### List Helpers (NIP-51)

```typescript
import { getRelaysFromList } from 'applesauce-common/helpers/lists';

const relays = getRelaysFromList(event);
```

## Casting System

The casting system transforms raw Nostr events into typed classes with both synchronous properties and reactive observables.

### Basic Usage

```typescript
import { castEvent, Note, User, Profile } from 'applesauce-common/casts';

// Cast an event to a typed class
const note = castEvent(event, Note, eventStore);

// Access synchronous properties
console.log(note.id);
console.log(note.createdAt);
console.log(note.isReply);

// Subscribe to reactive observables
note.author.profile$.subscribe(profile => {
  console.log('Author name:', profile?.name);
});
```

### Available Casts

- **Note** - Kind 1 short text notes
- **User** - User with profile and social graph
- **Profile** - Kind 0 profile metadata
- **Article** - Kind 30023 long-form articles
- **Reaction** - Kind 7 reactions
- **Zap** - Kind 9735 zap receipts
- **Comment** - NIP-22 comments
- **Share** - Reposts/quotes
- **Bookmarks** - NIP-51 bookmarks
- **Mutes** - NIP-51 mute lists

### With React

```typescript
import { use$ } from 'applesauce-react/hooks';
import { castEvent, Note } from 'applesauce-common/casts';

function NoteComponent({ event }) {
  const note = castEvent(event, Note, eventStore);

  // Subscribe to author's profile
  const profile = use$(note.author.profile$);

  // Subscribe to replies
  const replies = use$(note.replies$);

  return (
    <div>
      <span>{profile?.name}</span>
      <p>{note.content}</p>
      <span>{replies?.length} replies</span>
    </div>
  );
}
```

## Blueprints

Blueprints are factory functions that create Nostr events with automatic tag extraction and proper NIP compliance. They eliminate manual tag building and reduce boilerplate code significantly.

### Key Benefits

1. **Automatic Tag Extraction**: Blueprints automatically extract hashtags (#word), mentions (nostr:npub), and event quotes (nostr:note/nevent) from text content
2. **NIP Compliance**: Each blueprint follows the correct NIP specifications for its event type
3. **Less Code**: Replace 50-100 lines of manual tag building with 5-10 lines
4. **Type Safety**: Full TypeScript support with proper types for all options
5. **Maintainable**: Centralized event building logic that's easier to update

### Using Blueprints

```typescript
import { EventFactory } from 'applesauce-core/event-factory';
import { NoteBlueprint } from 'applesauce-common/blueprints';

const factory = new EventFactory();
factory.setSigner(signer);

// Create event from blueprint
const draft = await factory.create(NoteBlueprint, content, options);
const event = await factory.sign(draft);
```

### NoteBlueprint (Kind 1)

Creates short text notes with automatic hashtag, mention, and quote extraction.

**What it handles automatically:**
- Extracts `#hashtags` from content → `t` tags
- Extracts `nostr:npub...` mentions → `p` tags
- Extracts `nostr:note...` and `nostr:nevent...` quotes → `q` tags (NIP-18)
- Adds custom emoji tags (NIP-30)

```typescript
import { NoteBlueprint } from 'applesauce-common/blueprints';

// Simple note
const draft = await factory.create(
  NoteBlueprint,
  'Hello #nostr! Check out nostr:npub1abc...',
  {}
);

// With custom emojis
const draft = await factory.create(
  NoteBlueprint,
  'Hello :rocket:!',
  {
    emojis: [{ shortcode: 'rocket', url: 'https://example.com/rocket.png' }]
  }
);

// The blueprint automatically adds:
// - ["t", "nostr"] for #nostr
// - ["p", "decoded-pubkey"] for the npub mention
// - ["emoji", "rocket", "https://example.com/rocket.png"] for custom emoji
```

**Options:**
- `emojis?: Array<{ shortcode: string; url: string }>` - Custom emojis (NIP-30)
- `contentWarning?: boolean | string` - Content warning tag

**Before/After Example:**
```typescript
// ❌ BEFORE: Manual tag building (~70 lines)
const hashtags = content.match(/#(\w+)/g)?.map(tag => tag.slice(1)) || [];
const mentionRegex = /nostr:(npub1[a-z0-9]+)/g;
const mentions = [];
let match;
while ((match = mentionRegex.exec(content)) !== null) {
  try {
    const { data } = nip19.decode(match[1]);
    mentions.push(data);
  } catch (e) { /* ignore */ }
}
// ... more extraction logic ...
draft.tags = [
  ...hashtags.map(t => ['t', t]),
  ...mentions.map(p => ['p', p]),
  // ... more tags ...
];

// ✅ AFTER: Blueprint handles everything
const draft = await factory.create(NoteBlueprint, content, { emojis });
```

### NoteReplyBlueprint (Kind 1 Reply)

Creates threaded note replies following NIP-10 conventions.

**What it handles automatically:**
- Extracts root event from parent's tags (NIP-10)
- Adds proper `e` tags with markers (root, reply)
- Copies `p` tags from parent for notifications
- Extracts hashtags, mentions, and quotes from content
- Uses `q` tags for quotes instead of `e` tags (correct semantic)

```typescript
import { NoteReplyBlueprint } from 'applesauce-common/blueprints';

// Reply to a note
const parentEvent = await eventStore.event(parentId).toPromise();

const draft = await factory.create(
  NoteReplyBlueprint,
  parentEvent,
  'Great point! #bitcoin',
  {
    emojis: [{ shortcode: 'fire', url: 'https://example.com/fire.png' }]
  }
);

// The blueprint automatically:
// 1. Finds root from parent's tags (if parent is also a reply)
// 2. Adds ["e", rootId, relay, "root"]
// 3. Adds ["e", parentId, relay, "reply"]
// 4. Copies all ["p", ...] tags from parent
// 5. Extracts #bitcoin → ["t", "bitcoin"]
// 6. Adds emoji tag
```

**Options:**
- `emojis?: Array<{ shortcode: string; url: string }>` - Custom emojis
- `contentWarning?: boolean | string` - Content warning

**Before/After Example:**
```typescript
// ❌ BEFORE: Manual NIP-10 threading (~95 lines)
const parentRefs = getNip10References(parentEvent);
const rootId = parentRefs.root?.e || parentEvent.id;
const rootRelay = parentRefs.root?.relay || '';

draft.tags = [
  ['e', rootId, rootRelay, 'root'],
  ['e', parentEvent.id, '', 'reply'],
];

// Copy p-tags from parent
const parentPTags = parentEvent.tags.filter(t => t[0] === 'p');
draft.tags.push(...parentPTags);
if (!parentPTags.some(t => t[1] === parentEvent.pubkey)) {
  draft.tags.push(['p', parentEvent.pubkey]);
}
// ... hashtag extraction ...
// ... mention extraction ...

// ✅ AFTER: Blueprint handles NIP-10 threading
const draft = await factory.create(
  NoteReplyBlueprint,
  parentEvent,
  content,
  { emojis }
);
```

### ReactionBlueprint (Kind 7)

Creates reactions to events (likes, custom emoji reactions).

**What it handles automatically:**
- Adds `e` tag pointing to reacted event
- Adds `k` tag for event kind
- Adds `p` tag for event author
- Handles custom emoji reactions (`:shortcode:` format)
- Supports both string emoji and Emoji objects

```typescript
import { ReactionBlueprint } from 'applesauce-common/blueprints';

// Simple like (+ emoji)
const draft = await factory.create(ReactionBlueprint, messageEvent, '+');

// Custom emoji reaction
const draft = await factory.create(
  ReactionBlueprint,
  messageEvent,
  {
    shortcode: 'rocket',
    url: 'https://example.com/rocket.png'
  }
);

// String emoji
const draft = await factory.create(ReactionBlueprint, messageEvent, '🚀');

// The blueprint automatically adds:
// - ["e", messageEvent.id]
// - ["k", messageEvent.kind.toString()]
// - ["p", messageEvent.pubkey]
// For custom emoji: ["emoji", "rocket", "url"]
```

**Options:**
- Second parameter: `emoji?: string | { shortcode: string; url: string }`

**Before/After Example:**
```typescript
// ❌ BEFORE: Manual reaction building (~15 lines per adapter)
draft.kind = 7;
draft.content = typeof emoji === 'string' ? emoji : `:${emoji.shortcode}:`;
draft.tags = [
  ['e', messageEvent.id],
  ['k', messageEvent.kind.toString()],
  ['p', messageEvent.pubkey],
];
if (typeof emoji === 'object') {
  draft.tags.push(['emoji', emoji.shortcode, emoji.url]);
}

// ✅ AFTER: Blueprint handles reactions
const draft = await factory.create(ReactionBlueprint, messageEvent, emoji);
```

### GroupMessageBlueprint (Kind 9 - NIP-29)

Creates NIP-29 group chat messages.

**What it handles automatically:**
- Adds `h` tag with group ID
- Extracts hashtags, mentions, and quotes from content
- Adds custom emoji tags
- Handles message threading with `previous` field

```typescript
import { GroupMessageBlueprint } from 'applesauce-common/blueprints';

// Send message to NIP-29 group
const draft = await factory.create(
  GroupMessageBlueprint,
  { id: groupId, relay: relayUrl },
  'Hello group! #welcome',
  {
    previous: [], // Array of previous message events for threading
    emojis: [{ shortcode: 'wave', url: 'https://example.com/wave.png' }]
  }
);

// The blueprint automatically adds:
// - ["h", groupId]
// - ["t", "welcome"] for #welcome hashtag
// - ["emoji", "wave", "url"] for custom emoji
```

**Options:**
- `previous?: NostrEvent[]` - Previous messages for threading (required, use `[]` if no threading)
- `emojis?: Array<{ shortcode: string; url: string }>` - Custom emojis

**Note:** The `previous` field is required by the type, but can be an empty array if you don't need threading.

### DeleteBlueprint (Kind 5 - NIP-09)

Creates event deletion requests.

**What it handles automatically:**
- Adds `e` tags for each event to delete
- Sets proper kind and content format
- Adds optional reason in content

```typescript
import { DeleteBlueprint } from 'applesauce-common/blueprints';

// Delete single event
const draft = await factory.create(
  DeleteBlueprint,
  [eventToDelete],
  'Accidental post'
);

// Delete multiple events
const draft = await factory.create(
  DeleteBlueprint,
  [event1, event2, event3],
  'Cleaning up old posts'
);

// Without reason
const draft = await factory.create(DeleteBlueprint, [event], '');

// The blueprint automatically:
// - Sets kind to 5
// - Adds ["e", eventId] for each event
// - Sets content to reason (or empty)
```

**Parameters:**
- `events: (string | NostrEvent)[]` - Events to delete (IDs or full events)
- `reason?: string` - Optional deletion reason

### Adding Custom Tags

Blueprints handle common tags automatically, but you can add custom tags afterward:

```typescript
// Create with blueprint
const draft = await factory.create(NoteBlueprint, content, { emojis });

// Add custom tags not handled by blueprint
draft.tags.push(['client', 'grimoire', '31990:...']);
draft.tags.push(['a', `${kind}:${pubkey}:${identifier}`]);

// Add NIP-92 imeta tags for blob attachments
for (const blob of blobAttachments) {
  draft.tags.push(['imeta', `url ${blob.url}`, `x ${blob.sha256}`, ...]);
}

// Sign the modified draft
const event = await factory.sign(draft);
```

### Protocol-Specific Tag Additions

Some protocols require additional tags beyond what blueprints provide:

```typescript
// NIP-29: Add q-tag for replies (not in blueprint yet)
const draft = await factory.create(GroupMessageBlueprint, group, content, options);
if (replyToId) {
  draft.tags.push(['q', replyToId]);
}

// NIP-53: Add a-tag for live activity context
const draft = await factory.create(ReactionBlueprint, messageEvent, emoji);
draft.tags.push(['a', liveActivityATag, relay]);
```

### Available Blueprints

All blueprints from `applesauce-common/blueprints`:

- **NoteBlueprint** - Kind 1 short text notes
- **NoteReplyBlueprint** - Kind 1 threaded replies (NIP-10)
- **ReactionBlueprint** - Kind 7 reactions (NIP-25)
- **GroupMessageBlueprint** - Kind 9 group messages (NIP-29)
- **DeleteBlueprint** - Kind 5 deletion requests (NIP-09)
- **MetadataBlueprint** - Kind 0 profile metadata
- **ContactsBlueprint** - Kind 3 contact lists
- **ArticleBlueprint** - Kind 30023 long-form articles (NIP-23)
- **HighlightBlueprint** - Kind 9802 highlights (NIP-84)
- **ZapRequestBlueprint** - Kind 9734 zap requests (NIP-57)
- And more - check `node_modules/applesauce-common/dist/blueprints/`

### Best Practices

1. **Always use blueprints** when creating standard event types - they handle NIPs correctly
2. **Add custom tags after** blueprint creation for app-specific metadata
3. **Don't extract tags manually** - let blueprints handle hashtags, mentions, quotes
4. **Use proper emoji format** - blueprints expect `{ shortcode, url }` objects
5. **Check blueprint source** - when in doubt, read the blueprint code for exact behavior

## Operations

Operations modify existing events.

```typescript
import { addTag, removeTag } from 'applesauce-common/operations';

// Add a tag to an event
const modified = addTag(event, ['t', 'bitcoin']);

// Remove a tag
const updated = removeTag(event, 'client');
```

## Migration from v4

### Helper Import Changes

```typescript
// ❌ Old (v4)
import { getArticleTitle } from 'applesauce-core/helpers';
import { getNip10References } from 'applesauce-core/helpers/threading';
import { getZapAmount } from 'applesauce-core/helpers/zap';

// ✅ New (v5)
import { getArticleTitle } from 'applesauce-common/helpers/article';
import { getNip10References } from 'applesauce-common/helpers/threading';
import { getZapAmount } from 'applesauce-common/helpers/zap';
```

### Helpers that stayed in applesauce-core

These protocol-level helpers remain in `applesauce-core/helpers`:
- `getTagValue`, `hasNameValueTag`
- `getProfileContent`
- `parseCoordinate`, `getEventPointerFromETag`, `getAddressPointerFromATag`
- `isFilterEqual`, `matchFilter`, `mergeFilters`
- `getSeenRelays`, `mergeRelaySets`
- `getInboxes`, `getOutboxes`
- `normalizeURL`

## Best Practices

### Helper Caching

All helpers in applesauce-common cache internally using symbols:

```typescript
// ❌ Don't memoize helper calls
const title = useMemo(() => getArticleTitle(event), [event]);

// ✅ Call helpers directly
const title = getArticleTitle(event);
```

### Casting vs Helpers

Use **helpers** when you need specific fields:
```typescript
const title = getArticleTitle(event);
const amount = getZapAmount(event);
```

Use **casts** when you need reactive data or multiple related properties:
```typescript
const note = castEvent(event, Note, eventStore);
const profile$ = note.author.profile$;
const replies$ = note.replies$;
```

## Related Skills

- **applesauce-core** - Protocol-level helpers and event store
- **applesauce-signers** - Event signing abstractions
- **nostr** - Nostr protocol fundamentals
