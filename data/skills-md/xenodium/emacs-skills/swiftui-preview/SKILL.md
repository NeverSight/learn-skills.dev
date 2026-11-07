---
name: swiftui-preview
description: 'This skill should be used when the user invokes "/swiftui-preview" to render SwiftUI code from the current context to a PNG and output the resulting image path.'
tools: Bash
disable-model-invocation: true
---

# Render a SwiftUI preview

Generate SwiftUI code from the most recent interaction context, render it to a PNG using `ImageRenderer`, and output it as a markdown image so it renders inline.

The "context" can take any form: a prose description ("show a profile card with a photo on the left and name above bio on the right"), an attached screenshot or mockup image, an ASCII layout diagram, or actual Swift code. Translate whichever the user provided into a single `ContentView`.

For example, this ASCII diagram:

```
+------------------+--------------------------------------+
|                  |           Name                       |
|                  +--------------------------------------+
|    Photo         |                                      |
|                  |           Biography                  |
|                  |                                      |
+------------------+--------------------------------------+
```

should become an `HStack` with the photo on the left and a `VStack { Name; Biography }` on the right, sized so the photo spans the full height. Match proportions and stacking direction faithfully; choose reasonable placeholder content (e.g. `Image(systemName: "person.crop.square.fill")`, sample text) when the input doesn't specify.

## How to render

1. Derive SwiftUI view code from the current context — prose, image, ASCII diagram, or existing Swift. The root view must be named `ContentView`. Helper views may be defined alongside.
2. Locate `agent-skill-swiftui.el` which lives alongside this skill file at `skills/swiftui-preview/agent-skill-swiftui.el` in the emacs-skills plugin directory.
3. Invoke the elisp function in a single Bash call. To avoid shell+elisp quoting issues with arbitrary Swift code, pipe the source through `base64` and decode it on the elisp side:
   ```sh
   emacsclient --eval "(progn (load \"/path/to/skills/swiftui-preview/agent-skill-swiftui.el\" nil t) (agent-skill-swiftui-render :swift-source (base64-decode-string \"$(base64 <<'SWIFT' | tr -d '\n'
   struct ContentView: View {
     var body: some View {
       Text("Hello, SwiftUI!")
         .font(.largeTitle)
         .padding(40)
     }
   }
   SWIFT
   )\")))"
   ```
   The `'SWIFT'` heredoc delimiter is single-quoted so the source passes through verbatim — no shell escaping needed inside.
4. The function returns the PNG path as a quoted elisp string (e.g. `"/var/folders/.../agent-swiftui-XXXX.png"`) on success, or `nil` on failure.
5. On success, output the result as a markdown image on its own line:
   ```
   ![description](/var/folders/.../agent-swiftui-XXXX.png)
   ```

## SwiftUI source template

Do NOT include `import SwiftUI` — the wrapper imports it. Provide only the view structs:

```swift
struct ContentView: View {
  var body: some View {
    VStack(spacing: 20) {
      Text("Hello, SwiftUI!")
        .font(.largeTitle)
      RoundedRectangle(cornerRadius: 12)
        .fill(Color.orange)
        .frame(width: 200, height: 100)
    }
    .padding(40)
  }
}
```

If the source contains no `struct` or `class` definitions, it is wrapped automatically as the body of a generated `ContentView`. Otherwise it must define `ContentView` itself.

## Rules

- The root view must be named `ContentView` when the source contains struct/class definitions.
- Do not include `import SwiftUI` in the source — the wrapper adds it.
- Use one Bash call. Pass the source via the `base64 | tr -d '\n'` pipe inside the single-quoted `'SWIFT'` heredoc — do not write a temp `.swift` file as an intermediate step.
- Locate `agent-skill-swiftui.el` relative to this skill file's directory.
- Run the `emacsclient --eval` command via the Bash tool.
- `emacsclient` prints the return value as an elisp literal — strip the surrounding `"` quotes from the path before emitting the markdown image link.
- On success, output a markdown image (`![description](path)`) on its own line.
- On `nil` return, inform the user that the SwiftUI render failed and show the source so they can debug.
