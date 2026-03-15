---
name: swiftui-webkit
description: Native SwiftUI WebKit integration with the new WebView struct and WebPage observable class. Covers WebView creation from URLs, WebPage for navigation control and state management, JavaScript execution (callJavaScript with arguments and content worlds), custom URL scheme handlers, navigation management (load, reload, back/forward), navigation decisions, text search (findNavigator), content capture (snapshots, PDF generation, web archives), and configuration (data stores, user agents, JS permissions). Use when embedding web content in SwiftUI apps instead of the old WKWebView + UIViewRepresentable/NSViewRepresentable bridge pattern. This is a brand new API — do NOT use the old WKWebView wrapping approach.
---

# SwiftUI WebKit Integration

Native `WebView` struct for SwiftUI. Replaces the old `WKWebView` + Representable bridge pattern.

## Critical Constraints

- ❌ DO NOT use `WKWebView` + `UIViewRepresentable` or `NSViewRepresentable` → ✅ Use `WebView` struct directly
- ❌ DO NOT use `WKWebViewConfiguration` → ✅ Use `WebPage.Configuration`
- ❌ DO NOT use `WKNavigationDelegate` → ✅ Use `WebPage.NavigationDeciding` protocol
- ❌ DO NOT use `evaluateJavaScript(_:)` → ✅ Use `page.callJavaScript(_:)` (async/await)
- ❌ DO NOT use `WKUserContentController` for message passing → ✅ Use `callJavaScript` with arguments

## Basic WebView
```swift
import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        WebView(url: URL(string: "https://www.apple.com"))
            .frame(height: 400)
    }
}
```

## WebView with WebPage (Full Control)
```swift
struct BrowserView: View {
    @State private var page = WebPage()

    var body: some View {
        NavigationStack {
            WebView(page)
                .navigationTitle(page.title)
        }
        .onAppear {
            if let url = URL(string: "https://www.apple.com") {
                let _ = page.load(URLRequest(url: url))
            }
        }
    }
}
```

## Text Search
```swift
struct SearchableWebView: View {
    @State private var searchVisible = true

    var body: some View {
        WebView(url: URL(string: "https://www.apple.com"))
            .findNavigator(isPresented: $searchVisible)
    }
}
```

## WebPage Configuration
```swift
var config = WebPage.Configuration()
config.loadsSubresources = true
config.defaultNavigationPreferences.allowsContentJavaScript = true
config.websiteDataStore = .default()          // Persistent
// config.websiteDataStore = .nonPersistent() // Ephemeral

let page = WebPage(configuration: config)
page.customUserAgent = "MyApp/1.0"
```

## Loading Content
```swift
// URL
page.load(URLRequest(url: url))

// HTML string
page.load(html: "<h1>Hello</h1>", baseURL: URL(string: "https://example.com")!)

// Data
page.load(data, mimeType: "text/html", characterEncoding: .utf8, baseURL: baseURL)

// Navigation
page.reload(fromOrigin: false)
page.stopLoading()

// Back/Forward
if let backItem = page.backForwardList.backItem {
    page.load(backItem)
}
```

## JavaScript Execution
```swift
// Basic
let title = try await page.callJavaScript("document.title")

// With arguments
let script = """
function findElement(selector) {
    return document.querySelector(selector)?.textContent;
}
return findElement(selector);
"""
let result = try await page.callJavaScript(script, arguments: ["selector": ".main-content h1"])

// In specific content world
import WebKit
let result = try await page.callJavaScript("document.title", contentWorld: .page)
```

## Navigation Events
```swift
.onChange(of: page.currentNavigationEvent) { _, newEvent in
    if let event = newEvent {
        switch event.state {
        case .started: isLoading = true
        case .finished, .failed: isLoading = false
        default: break
        }
    }
}
```

## Custom Navigation Decisions
```swift
struct MyNavigationDecider: WebPage.NavigationDeciding {
    func decidePolicyFor(navigationAction: WebPage.NavigationAction) async -> WebPage.NavigationPreferences? {
        if let url = navigationAction.request.url, url.host == "blocked.com" {
            return nil  // Block navigation
        }
        var prefs = WebPage.NavigationPreferences()
        prefs.allowsContentJavaScript = true
        return prefs
    }

    func decidePolicyFor(navigationResponse: WebPage.NavigationResponse) async -> Bool {
        if let http = navigationResponse.response as? HTTPURLResponse {
            return http.statusCode == 200
        }
        return true
    }
}

let page = WebPage(configuration: config, navigationDecider: MyNavigationDecider())
```

## Custom URL Scheme Handler
```swift
struct MySchemeHandler: URLSchemeHandler {
    func start(task: URLSchemeTask) {
        guard let url = task.request.url, url.scheme == "myapp" else {
            task.didFailWithError(URLError(.badURL)); return
        }
        let html = "<html><body><h1>Custom Content</h1></body></html>"
        let response = URLResponse(url: url, mimeType: "text/html",
                                  expectedContentLength: -1, textEncodingName: "utf-8")
        task.didReceive(response)
        task.didReceive(Data(html.utf8))
        task.didFinish()
    }
    func stop(task: URLSchemeTask) { }
}

var config = WebPage.Configuration()
config.setURLSchemeHandler(MySchemeHandler(), forURLScheme: "myapp")
```

## Content Capture
```swift
// Snapshot
let image = try await page.snapshot(WKSnapshotConfiguration())

// PDF
let pdfData = try await page.pdf(configuration: WKPDFConfiguration())

// Web Archive
let archiveData = try await page.webArchiveData()
```

## View Modifiers
```swift
WebView(url: url)
    .webViewBackForwardNavigationGestures(.disabled)
    .webViewMagnificationGestures(.enabled)
    .webViewLinkPreviews(.disabled)
    .webViewTextSelection(.enabled)
    .webViewContentBackground(.color(.systemBackground))
    .webViewElementFullscreenBehavior(.enabled)
```

## References

- [WebKit for SwiftUI](https://developer.apple.com/documentation/WebKit/webkit-for-swiftui)
- [WebView](https://developer.apple.com/documentation/WebKit/WebView-swift.struct)
- [WebPage](https://developer.apple.com/documentation/WebKit/WebPage)
