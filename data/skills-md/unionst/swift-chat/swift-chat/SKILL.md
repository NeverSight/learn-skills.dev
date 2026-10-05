---
name: swift-chat
description: Add an iMessage-faithful chat screen to an iOS app with Swift Chat, the free SwiftUI package from Union St. Use when the user asks for a chat UI, a messages screen, a conversation view, an AI assistant thread, iMessage-style bubbles, typing indicators, read receipts, or a chat input bar in SwiftUI. Covers installation, the Chat and Message API, every modifier, attachments, the assistant style for AI threads, and the mistakes agents make most.
---

# Swift Chat

One SwiftUI view that renders a conversation the way the Messages app does: collated bubble tails, typing dots, delivery and read receipts, photos and files, tapbacks, group chats, pagination, and a keyboard that follows the finger. A UIKit collection view does the work underneath; SwiftUI is the only API you touch.

Free to use in any app. Closed source, shipped as a binary Swift package. iOS 18 or later, Xcode 26.1 or later.

Full reference: https://unionst.com/swiftchat/llms-full.txt. Runnable examples: `Examples/SwiftChatDemo` in https://github.com/unionst/swift-chat.

## Install

Swift Package Manager, product `SwiftChat`:

```swift
dependencies: [
    .package(url: "https://github.com/unionst/swift-chat.git", from: "1.0.0")
],
targets: [
    .target(name: "MyApp", dependencies: [
        .product(name: "SwiftChat", package: "swift-chat")
    ])
]
```

In Xcode: File › Add Package Dependencies › paste the URL. No other dependencies to add. Then `import SwiftChat`.

## Minimal screen

```swift
import SwiftUI
import SwiftChat

struct ConversationView: View {
    @State private var conversation = Conversation()

    var body: some View {
        Chat(conversation.messages) { message in
            Message(message.text, role: message.role, timestamp: message.sentAt)
                .messageStatus(message.status)
        }
        .chatTypingIndicators(conversation.typing)
        .chatInputPlaceholder("Message")
        .chatInputCapabilities([.photoLibrary, .files])
        .onChatSend { text, media in
            await conversation.send(text, media)
        }
    }
}

@MainActor @Observable
final class Conversation {
    var messages: [ChatMessage] = []
    var typing: [ChatRole] = []

    func send(_ text: String?, _ media: [MessageMedia]) async {
        let message = ChatMessage(text: text ?? "", role: .me, sentAt: .now, status: .sending)
        messages.append(message)
        await api.deliver(message, attachments: media)
    }
}

struct ChatMessage: Identifiable {
    let id = UUID()
    var text: String
    var role: ChatRole
    var sentAt: Date
    var status: ChatDeliveryStatus?
}
```

`Chat` takes any `RandomAccessCollection` of `Identifiable` values and a closure that turns each one into a `Message`. The user's model stays theirs; nothing conforms to a protocol. Rows are keyed by the element's `id`, so keep ids stable.

## Roles

- `.me`: outgoing bubble on the right.
- `.user(id:displayName:)`: incoming bubble on the left; avatar and name appear automatically once three people are in the thread.
- `.system`: centered gray text, no bubble.

## Message modifiers

| Modifier | Effect |
|---|---|
| `messageStatus(_:)` | `.sending`, `.sent`, `.delivered`, `.read`, `.failed` under the bubble |
| `messageMedia(_:)` | One `MessageMedia` or an array; several images draw as one collage |
| `messageReactions(_:)` | Tapbacks drawn on the bubble |
| `messageAttachment { }` | Any SwiftUI view as the attachment |
| `messageHeader { }` / `messageFooter { }` | Views above or below the bubble |
| `messageAvatar { }` | Custom avatar for incoming messages |
| `messageStyle(_:)` | `.default` bubbles or `.plain` bare text |
| `font(_:)` | Bubble text font |
| `contextMenu { }` | Long-press menu for that message |
| `contentVersion(_:)` | Re-render when content changes but the id does not |

Attachments: `MessageMedia.image(url:width:height:blurhash:)` and `MessageMedia.file(url:name:size:mimeType:)`. Pass width and height for images so placeholders are sized before load. `image(url:)` accepts `https:`, `file:`, and `data:` URLs. `video`, `audio`, `location`, and `poll` exist on the enum but are not drawn yet; do not promise them.

## Chat modifiers

| Modifier | Effect |
|---|---|
| `chatInputPlaceholder(_:)` | Placeholder in the input field |
| `chatInputCapabilities(_:)` | `.camera`, `.photoLibrary`, `.files`, or `[]` for text only |
| `onChatSend { text, media in }` | Async send handler. `text` may be nil, `media` is `[MessageMedia]` and may be empty |
| `onChatTypingChanged { isTyping in }` | Send typing events to your server |
| `onChatInputTextChanged { text in }` | Keep a draft per thread; seed it back with `chatInitialInputText(_:)` |
| `chatTypingIndicators(_:)` | Typing dots for `[ChatRole]` |
| `chatHeader { }` | SwiftUI view pinned above the transcript |
| `chatEmptyView { }` | Shown when there are no messages |
| `chatAutoscrollBehavior(_:)` | `.whenAtBottom` (default), `.always`, `.never` |
| `chatLoadsOlderMessages { }` | Async loader at the top; return `false` when nothing older remains |
| `onChatScrollEdge(_:perform:)` | Top or bottom edge reached |
| `onMessagesEvictable { ids in }` | Off-screen ids safe to drop in huge threads |
| `chatMessageContextMenu { id in [ChatContextMenuItem] }` | Long-press menu items as data, keyed by message id |
| `onChatMessageTap { id in }` | Tap per message |
| `chatSenderInfo(_:)` | `.automatic` (group chats only) or `.always` |
| `chatStyle(_:)` | `.messages` (default) or `.assistant` |
| `chatTypingStatus(_:)` | Status line beside the spinner in the assistant style |
| `chatInputBarHeight(_:)` | Resting height of the field |
| `chatInputControlTint(_:)` | Send button fill |
| `chatBubbleStyle(_:)` | Any `ShapeStyle` for outgoing bubbles; `.tint(_:)` also works |
| `chatBubbleTailsHidden(_:)` | Hide tails |
| `chatInputBarTint(_:)` | Translucent tint over the input bar's glass |
| `chatHapticsDisabled(_:)` | No tap on incoming messages |
| `chatPaginationAnimated(_:)` | Animate bubbles during rapid bursts |

## Assistant style, for AI threads

```swift
Chat(thread.messages, typingUsers: thread.thinking ? [assistant] : []) { message in
    Message(message.text, role: message.role, timestamp: message.sentAt)
}
.chatStyle(.assistant)
.chatTypingStatus(thread.status)
.chatInputPlaceholder("Ask anything")
.onChatSend { text, _ in
    await thread.send(text)
}
```

The user's question rises to the top and the reply streams in beneath it as bare Markdown text (headings, lists, bold, links, code blocks render). Stream a reply by appending one message and rewriting its text as tokens arrive; the row grows in place. Show the spinner by passing the assistant's role in `typingUsers` while it works, and a status like "Searching" with `chatTypingStatus(_:)`.

## Mistakes to avoid

- `chatTypingIndicators(_:)` is a method on `Chat` itself. Apply it directly to `Chat(...)` before other modifiers, or pass `typingUsers:` in the initializer.
- Do not wrap `Chat` in a `ScrollView` or `List`. It scrolls itself and owns the keyboard.
- Do not add your own keyboard avoidance or `safeAreaInset` input bar. The input bar is built in; `onChatSend` is how you receive input.
- `onChatSend` gives `media` as an array. Older docs showed a single optional; that is gone.
- Use `chatMessageContextMenu` (data) for per-row menus; a SwiftUI `contextMenu` inside a hosted cell can swallow taps.
- Keep message ids stable across renders, or rows lose their height and delivery label.
- `import SwiftChat`. The older `import UnionChat` still compiles but is deprecated.
