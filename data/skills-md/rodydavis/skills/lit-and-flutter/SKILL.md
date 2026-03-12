---
name: lit-and-flutter
description: Learn how to embed a Lit web component directly within your Flutter app to leverage web-based UIs and features while accessing native device APIs for a powerful hybrid development approach.
metadata:
  url: https://rodydavis.com/posts/flutter-and-lit
  last_modified: Tue, 03 Feb 2026 20:04:19 GMT
---

# Lit and Flutter


In this article I will go over how to set up a [Lit](https://lit.dev/) web component and use it inline in the Flutter widget tree.

> **TLDR** You can find the final source [here](https://github.com/rodydavis/flutter_hybrid_template).

The reason you would want this integration is so you can take an existing web app, or just a single part of it and embed it in the widget tree.

With it wrapped in Flutter you can call device APIs from event listeners on your web component.

For example you may have an app that handles purchases, and now you can call the in app purchase API or other device specific features not available on the web.

You also get a cross platform app that can be delivered to both Google Play and the App Store.

The web component will receive new code each time you update your site, so you do not have to ship an update each time the web component changes.

## Prerequisites 

*   Flutter SDK
*   Xcode and Command Line Tools
*   Android SDK
*   Vscode
*   Node
*   Typescript

## Getting Started 

We can start off by creating a empty directory and naming it with `snake_case` whatever we want.

```
mkdir flutter_lit_example
cd flutter_lit_example
```

### Web Setup 

Now we are in the `flutter_lit_example` directory and can setup Flutter and Lit. Let's start with node.

```
npm init -y
npm i lit
npm i -D typescript vite @types/node
```

This will setup the basics for a node project and install the packages we need. Now lets add some config files.

```
touch tsconfig.json
touch vite.config.ts
```

This will create 2 files. Now open up `tsconfig.json` and paste the following:

```
{
  "compilerOptions": {
    "module": "esnext",
    "lib": [
      "es2017",
      "dom",
      "dom.iterable"
    ],
    "types": [
      "vite/client"
    ],
    "declaration": true,
    "emitDeclarationOnly": true,
    "outDir": "./types",
    "rootDir": "./src",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "experimentalDecorators": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": [
    "src/**/*.ts"
  ],
  "exclude": []
}
```

This is a basic typescript config. Now open up `vite.config.ts` and paste the following:

```
import { defineConfig } from "vite";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig({
  base: "/flutter_lit_example/", // TODO: Name of your github repo
  build: {
    outDir: "build/web",
    rollupOptions: {
      output: {
        entryFileNames: `assets/[name].js`,
        chunkFileNames: `assets/[name].js`,
        assetFileNames: `assets/[name].[ext]`,
      },
      input: {
        main: resolve(__dirname, "index.html"),
        // TODO: Create a new module for each component you want to embed
      },
    },
  },
});
```

Now we need to create our web component:

```
mkdir src
cd src
touch my-app.ts
cd ..
```

Open `my-app.ts` and paste the following:

```
import { html, css, LitElement } from "lit";
import { customElement, property } from "lit/decorators.js";

@customElement("my-app")
export class MyApp extends LitElement {
  static styles = css`
    p {
      color: blue;
    }
  `;

  @property()
  name = "Somebody";

  render() {
    return html`<div>
      <p>Hello, ${this.name}!</p>
      <slot></slot>
    </div>`;
  }
}
```

We need to create a `index.html` for our web app.

```
touch index.html
```

Open `index.html` and paste the following:

```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Example</title>
    <script type="module" src="/src/my-app.ts"></script>
    <style>
      body {
        padding: 0;
        margin: 0;
      }
      my-app {
        width: 100%;
        height: 100vh;
      }
    </style>
  </head>
  <body>
    <my-app></my-app>
  </body>
</html>
```

### Flutter Setup 

Now that we have the basics setup for web we can move on to flutter. Let's create the project with the following:

```
flutter create --platforms=ios,android .
flutter packages get
```

Open up `pubspec.yaml` and update it with the following:

```
name: flutter_lit_example
description: A hybrid Flutter app.
publish_to: "none"
version: 1.0.0+1

environment:
  sdk: ">=2.7.0 <3.0.0"

dependencies:
  flutter:
    sdk: flutter
  flutter_inappwebview: ^5.3.2

dev_dependencies:
  flutter_test:
    sdk: flutter

flutter:
  uses-material-design: true
```

Make sure to get the packages again:

```
flutter packages get
```

Now we need to create the file that will wrap the web component.

```
cd lib
touch web_component.dart
cd ..
```

Open `web_component.dart` and paste the following:

```
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class WebComponent extends StatefulWidget {
  const WebComponent({
    Key key,
    @required this.name,
    @required this.bundle,
    this.attributes = const {},
    this.slot = '',
    this.events = const [],
  }) : super(key: key);
  final String name, bundle;
  final Map<String, String> attributes;
  final String slot;
  final List<EventCallback> events;

  @override
  _WebComponentState createState() => _WebComponentState();
}

class _WebComponentState extends State<WebComponent> {
  InAppWebViewController controller;
  final Map<String, List<EventCallback>> _events = {};

  String get source {
    return '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      body {
        padding: 0;
        margin: 0;
      }
      ${widget.name} {
        width: 100%;
        height: 100vh;
      }
    </style>
  <script type="module" crossorigin src="${widget.bundle}"></script>
</head>
  <body>
    <${widget.name} ${widget.attributes.entries.map((e) => '${e.key}="${e.value}"').join(' ')}>
      ${widget.slot}
    </${widget.name}>
    <script>
    window.addEventListener("flutterInAppWebViewPlatformReady", (event) => {
      ${widget.events.join('\n')}
    });
    </script>
  </body>
</html> 
''';
  }

  void _setup(InAppWebViewController controller) {
    this.controller = controller;
    this._setupEvents();
  }

  void _setupEvents() {
    for (final event in _events.keys) {
      controller.removeJavaScriptHandler(handlerName: event);
    }
    for (final event in widget.events) {
      _addEvent(event);
    }
  }

  void _addEvent(EventCallback event) {
    controller.addJavaScriptHandler(
      handlerName: event.query,
      callback: event.onPressed,
    );
    _events[event.event] ??= [];
    _events[event.event].add(event);
  }

  @override
  void didUpdateWidget(covariant WebComponent oldWidget) {
    if (oldWidget.events != widget.events) {
      _setupEvents();
    }
    if (oldWidget.slot != widget.slot ||
        oldWidget.bundle != widget.bundle ||
        oldWidget.name != widget.name) {
      controller.loadData(data: source);
    }
    super.didUpdateWidget(oldWidget);
  }

  @override
  Widget build(BuildContext context) {
    return InAppWebView(
      initialData: InAppWebViewInitialData(data: source),
      onWebViewCreated: _setup,
    );
  }
}

class EventCallback {
  EventCallback({
    @required this.onPressed,
    @required this.event,
    this.query,
  });
  final String query, event;
  final dynamic Function(List<dynamic> args) onPressed;

  @override
  String toString() => _source;

  String get _prefix => query != null && query.isNotEmpty
      ? 'document.querySelector("$query")'
      : 'document.body';

  String get _source => [
        '$_prefix.addEventListener("$event", (e) => {',
        '  window.flutter_inappwebview.callHandler("$query", e);',
        '}, false);',
      ].join('\n');
}
```

Open `main.dart` and paste it with th following:

```
import 'package:flutter/material.dart';

import 'web_component.dart';

const WEBSITE_URL = 'https://rodydavis.github.io/flutter_lit_example/';
const BUNDLE_PATH = 'assets/main.js';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final title = 'Flutter Hybrid App';
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: title,
      theme: ThemeData(primarySwatch: Colors.blue),
      home: MyHomePage(title: title),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Builder(
        builder: (context) => WebComponent(
          name: 'my-app',
          bundle: '$WEBSITE_URL/$BUNDLE_PATH',
          attributes: {
            'name': widget.title,
          },
          slot: '<button id="my-button">Talk back!</button>',
          events: [
            EventCallback(
              event: 'click',
              query: '#my-button',
              onPressed: (_) {
                ScaffoldMessenger.of(context)
                    .showSnackBar(SnackBar(content: Text('Clicked!')));
              },
            ),
          ],
        ),
      ),
    );
  }
}
```

You will need to update `WEBSITE_URL` to have the url of the website where you will be deploying and `BUNDLE_URL` to the relative path to the js bundle.

This will ensure auto updates with a new version rolls out and the cache it stale. This will also allow for offline support after the first time it is downloaded.

## Running 

Now we can run our application but it requires a few steps to get it all setup.

To test and build our web app locally we will use [vite](https://github.com/vitejs/vite) and render the `index.html`

```
npm i
npm run dev
```

You should see the following:

```
vite v2.2.3 dev server running at:

Local:    http://localhost:3000/flutter_lit_example/
Network:  http://192.168.1.143:3000/flutter_lit_example/

ready in 311ms.
```

We can open the link `http://localhost:3000/flutter_lit_example/` to see our running web app and hot reload changes from `my-app.ts`.

If you want to learn more about Lit you can read the docs [here](https://lit.dev/).

Once you are happy with how it looks we can move on to Flutter to wrap it in a native app. This will give us access to native code if we wanted to use the in app purchase api or push notifications.

Kill the terminal and run the following:

```
flutter packages get
flutter build ios
flutter build appbundle
flutter run
```

This should select a running device or prompt you to select one. Now that it is running on the device you can see we have two way communication with the Flutter app and the web component.

## Conclusion 

If you want to find the source code you can check it out [here](https://github.com/rodydavis/flutter_hybrid_template) otherwise thanks for reading and let me know if you have any questions!