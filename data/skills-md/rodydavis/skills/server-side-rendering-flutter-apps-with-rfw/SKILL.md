---
name: server-side-rendering-flutter-apps-with-rfw
description: Learn how to build a dynamic Flutter app using Server Side Rendering (SSR) with the rfw package, enabling UI updates driven by server logic and binary data exchange via HTTP.
metadata:
  url: https://rodydavis.com/posts/flutter-ssr-rfw
  last_modified: Tue, 03 Feb 2026 20:04:17 GMT
---

# Server Side Rendering Flutter Apps with RFW


This post will guide you how to build a Flutter app that takes advantage of Server Side Rendering (SSR) and being able to update UI dynamically.

> If you are new to flutter you can follow this [post](https://rodydavis.com/posts/first-flutter-project) on getting started

This technique will use the [rfw](https://pub.dev/packages/rfw) package on the server and client to send binary data via HTTP requests.

> **TLDR** You can find the final source [here](https://github.com/rodydavis/flutter_ssr).

## Getting started 

Create a new directory called `flutter_ssr` and navigate to it in terminal or open it up in your favorite IDE.

## Approaches to updates 

If you are in the mobile world then you know how challenging it can be to get all your users on the latest version. Even just having an API or database schema can be very hard to update because of users on older versions (sometimes due to OS limitations).

### Code Push 

[Shorebird](https://shorebird.dev/) takes an interesting approach to delivering updates to the users via Code Push and will update the apps live. This does have an advantage since it will update the UI and logic but what if the content update was only intended for a specific user or set of users?

### Latest version supported 

Another approach is to simply have an SLO/Policy that you only support X number of recent releases and that the app will not work on older versions.

For something like this on mobile you would use [upgrader](https://pub.dev/packages/upgrader) via [AppCast](https://sparkle-project.org/about/) or [in\_app\_update](https://pub.dev/packages/in_app_update) to use Google Play APIs to update the app in the background or prevent using until updated.

This has an advantage to know that users will be on the latest or no be supported and allow you to target newer APIs and roll updates easier. This does mean that users will be frustrated by updates more and that older devices may not be supported.

### Server driven updates 

Not all apps need to render data on the server and sometimes when building an offline first application you want to do everything local first, but this is for when you need to build a server first application. Here are some examples and use cases:

*   Bank accounts
*   Airline / Hotel / Car booking
*   Chat applications (Instant messaging)
*   Marketing and AB testing
*   Database first applications

Each of these examples does not mean they are server only and in many cases you want to still cache the data locally to still offer a great offline experience.

With Flutter you are building a runtime that you are shipping to the user as a Single Page Application (SPA) on the web and a mobile/desktop app on the stores. This means you need to ship all the logic and UI for every update.

This has an advantage for doing more logic on the server and potentially really heavy requests are done server side and just the rendered UI is sent to the client. The client can still cache the response and allow for offline viewing too. These disadvantage here is that the client is expected to communicate with the server at some point and may not be suitable for offline only applications.

## Remote Flutter Widgets (RFW) 

The Flutter team has a package for creating widgets on the client and server and sending data necessary to connect them. This package is called [rfw](https://pub.dev/packages/rfw).

> While it is possible to ship logic in addition to UI as WASM that is out of scope for this post

The rfw package uses a text format that can be compiled to binary and be used to represent state and dispatch events.

```
import core;
import material;

widget MaterialShop = Scaffold(
  appBar: AppBar(
    title: Text(text: ['Products']),
  ),
  body: ListView(
    children: [
      ...for product in data.server.games:
        Product(product: product)
    ],
  ),
);

widget Product = ListTile(
  title: Text(text: args.product.name),
  onTap: event 'shop.productSelect' { name: args.product.name, path: args.product.link },
);
```

Multiple widgets can be defined and it may even look similar to the Dart API you are used to in Flutter but it is not quite the same.

There are not logic branching blocks or conditional rendering but rather is a stateless format capable of updating every frame if needed.

Take the following Flutter counter app that is generated when you create a new project:

```
class MyHomePage extends StatefulWidget {
  final String title;

  const MyHomePage({
    Key? key,
    required this.title,
  }) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    setState(() {
      _counter++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              'You have pushed the button this many times:',
            ),
            Text(
              '$_counter',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Increment',
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

We could represent that in rfw like this:

```
import widgets;
import material;

widget root = Scaffold(
  appBar: AppBar(
    title: Text(text: ['Counter Example']),
    centerTitle: true,
    backgroundColor: data.colorScheme.inversePrimary,
  ),
  body: Center(
    child: Column(
      mainAxisAlignment: "center",
      children: [
        Text(text: ["You have pushed the button this many times:"]),
        Text(
          text: [data.counter.value],
          style: {
            fontSize: 20.0,
          },
        ),
      ],
    ),
  ),
  floatingActionButton: FloatingActionButton(
     onPressed: event "click" {},
     tooltip: ["Increment"],
     child: Icon(
        icon: 0xe047,
        fontFamily: 'MaterialIcons',
     ),
  ),
);
```

You may have noticed some arrays for strings and different ways of defining widgets. That is by design and the API will not be 100% with the Flutter SDK, but with the limitation comes different tradeoffs.

You can define any custom widgets in your application and only uses the UI you have defined in your design system and the server will only be able to generate UI that you expect.

It is also possible to create all the UI in the text format with rows, columns, containers and more.

## Setting up the server 

For this example we will be using [dart\_frog](https://dartfrog.vgv.dev/docs/overview) to create the server application.

In the directory that you created earlier run the following commands:

```
dart_frog create server
flutter pub add rfw
```

This will generate the server boilerplate for us and add the correct dependencies.

> Feel free to delete the test directory for now or update it later to check for the correct response.

Navigate to `/server/routes/index.dart` and update the file with the following:

```
import 'package:dart_frog/dart_frog.dart';
import 'package:rfw/formats.dart';

Response onRequest(RequestContext context) {
  var count = context.request.headers['COUNTER_VALUE'] ?? '0';

  if (context.request.method == HttpMethod.post) {
    count = (int.parse(count) + 1).toString();
  }

  return Response.bytes(
    body: encodeLibraryBlob(parseLibraryFile(template)),
    headers: {'COUNTER_VALUE': count},
  );
}

const template = '''
import widgets;
import material;

widget root = Scaffold(
  appBar: AppBar(
    title: Text(text: ['Counter Example']),
    centerTitle: true,
    backgroundColor: data.colorScheme.inversePrimary,
  ),
  body: Center(
    child: Column(
      mainAxisAlignment: "center",
      children: [
        Text(text: ["You have pushed the button this many times:"]),
        Text(
          text: [data.counter.value],
          style: {
            fontSize: 20.0,
          },
        ),
      ],
    ),
  ),
  floatingActionButton: FloatingActionButton(
     onPressed: event "click" {},
     tooltip: ["Increment"],
     child: Icon(
        icon: 0xe047,
        fontFamily: 'MaterialIcons',
     ),
  ),
);
''';
```

This takes the rfw text format we defined earlier and adds it to a string template.

Using that template we can call `encodeLibraryBlob(parseLibraryFile(template))` to create a binary representation of the text format.

We are also checking for the `COUNTER_VALUE` from the header to send state to/from the client. Since servers are stateless or easier to scale when they are this will help with not needing a type of session storage or context.

If you navigate inside the `server` directly you can start the dev server that will be needed for the next step:

```
dart_frog dev
```

You should see the following:

```
✓ Running on http://localhost:8080
```

## Setting up the client 

In a new terminal tab you can navigate to the root of the directory and run the following commands:

```
flutter create app
flutter pub add rfw http
```

This will generate the counter app boilerplate and add the correct dependencies for us.

The rfw package comes with **core** and **material** widgets but for this example we will be adding them manually to show how they are being called and created.

Create and update the following file located att `app/lib/rfw/decoders.dart`:

```
import 'package:flutter/material.dart';
import 'package:rfw/rfw.dart';

class CustomArgumentDecoders {
  static ButtonStyle? outlinedButtonStyle(
    DataSource source,
    List<Object> key,
    BuildContext context,
  ) {
    if (!source.isMap(key)) {
      return null;
    }
    return OutlinedButton.styleFrom(
      foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
      backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
      disabledForegroundColor:
          ArgumentDecoders.color(source, [...key, 'disabledForegroundColor']),
      disabledBackgroundColor:
          ArgumentDecoders.color(source, [...key, 'disabledBackgroundColor']),
      shadowColor: ArgumentDecoders.color(source, [...key, 'shadowColor']),
      surfaceTintColor:
          ArgumentDecoders.color(source, [...key, 'surfaceTintColor']),
      elevation: source.v<double>(['elevation']),
      textStyle: ArgumentDecoders.textStyle(source, [...key, 'textStyle']),
      padding: ArgumentDecoders.edgeInsets(source, [...key, 'padding']),
      minimumSize: CustomArgumentDecoders.size(source, [...key, 'minimumSize']),
      fixedSize: CustomArgumentDecoders.size(source, [...key, 'fixedSize']),
      maximumSize: CustomArgumentDecoders.size(source, [...key, 'maximumSize']),
      side: ArgumentDecoders.borderSide(source, [...key, 'side']),
      shape: CustomArgumentDecoders.outlinedBorder(source, [...key, 'shape']),
      enabledMouseCursor: CustomArgumentDecoders.mouseCursor(
          source, [...key, 'enabledMouseCursor']),
      disabledMouseCursor: CustomArgumentDecoders.mouseCursor(
          source, [...key, 'disabledMouseCursor']),
      visualDensity:
          ArgumentDecoders.visualDensity(source, [...key, 'visualDensity']),
      tapTargetSize: ArgumentDecoders.enumValue<MaterialTapTargetSize>(
              MaterialTapTargetSize.values,
              source,
              [...key, 'tapTargetSize']) ??
          MaterialTapTargetSize.shrinkWrap,
      animationDuration: ArgumentDecoders.duration(
          source, [...key, 'animationDuration'], context),
      enableFeedback: source.v<bool>([...key, 'enableFeedback']),
      alignment: ArgumentDecoders.alignment(source, [...key, 'alignment']),
    );
  }

  static ButtonStyle? filledButtonStyle(
    DataSource source,
    List<Object> key,
    BuildContext context,
  ) {
    if (!source.isMap(key)) {
      return null;
    }
    return FilledButton.styleFrom(
      foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
      backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
      disabledForegroundColor:
          ArgumentDecoders.color(source, [...key, 'disabledForegroundColor']),
      disabledBackgroundColor:
          ArgumentDecoders.color(source, [...key, 'disabledBackgroundColor']),
      shadowColor: ArgumentDecoders.color(source, [...key, 'shadowColor']),
      surfaceTintColor:
          ArgumentDecoders.color(source, [...key, 'surfaceTintColor']),
      elevation: source.v<double>(['elevation']),
      textStyle: ArgumentDecoders.textStyle(source, [...key, 'textStyle']),
      padding: ArgumentDecoders.edgeInsets(source, [...key, 'padding']),
      minimumSize: CustomArgumentDecoders.size(source, [...key, 'minimumSize']),
      fixedSize: CustomArgumentDecoders.size(source, [...key, 'fixedSize']),
      maximumSize: CustomArgumentDecoders.size(source, [...key, 'maximumSize']),
      side: ArgumentDecoders.borderSide(source, [...key, 'side']),
      shape: CustomArgumentDecoders.outlinedBorder(source, [...key, 'shape']),
      enabledMouseCursor: CustomArgumentDecoders.mouseCursor(
          source, [...key, 'enabledMouseCursor']),
      disabledMouseCursor: CustomArgumentDecoders.mouseCursor(
          source, [...key, 'disabledMouseCursor']),
      visualDensity:
          ArgumentDecoders.visualDensity(source, [...key, 'visualDensity']),
      tapTargetSize: ArgumentDecoders.enumValue<MaterialTapTargetSize>(
              MaterialTapTargetSize.values,
              source,
              [...key, 'tapTargetSize']) ??
          MaterialTapTargetSize.shrinkWrap,
      animationDuration: ArgumentDecoders.duration(
          source, [...key, 'animationDuration'], context),
      enableFeedback: source.v<bool>([...key, 'enableFeedback']),
      alignment: ArgumentDecoders.alignment(source, [...key, 'alignment']),
    );
  }

  static ButtonStyle? textButtonStyle(
    DataSource source,
    List<Object> key,
    BuildContext context,
  ) {
    if (!source.isMap(key)) {
      return null;
    }
    return TextButton.styleFrom(
      foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
      backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
      disabledForegroundColor:
          ArgumentDecoders.color(source, [...key, 'disabledForegroundColor']),
      disabledBackgroundColor:
          ArgumentDecoders.color(source, [...key, 'disabledBackgroundColor']),
      shadowColor: ArgumentDecoders.color(source, [...key, 'shadowColor']),
      surfaceTintColor:
          ArgumentDecoders.color(source, [...key, 'surfaceTintColor']),
      elevation: source.v<double>(['elevation']),
      textStyle: ArgumentDecoders.textStyle(source, [...key, 'textStyle']),
      padding: ArgumentDecoders.edgeInsets(source, [...key, 'padding']),
      minimumSize: CustomArgumentDecoders.size(source, [...key, 'minimumSize']),
      fixedSize: CustomArgumentDecoders.size(source, [...key, 'fixedSize']),
      maximumSize: CustomArgumentDecoders.size(source, [...key, 'maximumSize']),
      side: ArgumentDecoders.borderSide(source, [...key, 'side']),
      shape: CustomArgumentDecoders.outlinedBorder(source, [...key, 'shape']),
      enabledMouseCursor: CustomArgumentDecoders.mouseCursor(
          source, [...key, 'enabledMouseCursor']),
      disabledMouseCursor: CustomArgumentDecoders.mouseCursor(
          source, [...key, 'disabledMouseCursor']),
      visualDensity:
          ArgumentDecoders.visualDensity(source, [...key, 'visualDensity']),
      tapTargetSize: ArgumentDecoders.enumValue<MaterialTapTargetSize>(
              MaterialTapTargetSize.values,
              source,
              [...key, 'tapTargetSize']) ??
          MaterialTapTargetSize.shrinkWrap,
      animationDuration: ArgumentDecoders.duration(
          source, [...key, 'animationDuration'], context),
      enableFeedback: source.v<bool>([...key, 'enableFeedback']),
      alignment: ArgumentDecoders.alignment(source, [...key, 'alignment']),
    );
  }

  static EdgeInsets? edgeInsets(DataSource source, List<Object> key) {
    if (!source.isMap(key)) {
      return null;
    }
    final all = source.v<double>([...key, 'all']);
    if (all != null) return EdgeInsets.all(all);
    final vertical = source.v<double>([...key, 'vertical']);
    final horizontal = source.v<double>([...key, 'horizontal']);
    if (vertical != null || horizontal != null) {
      return EdgeInsets.symmetric(
        vertical: vertical ?? 0,
        horizontal: horizontal ?? 0,
      );
    }
    final top = source.v<double>([...key, 'top']);
    final bottom = source.v<double>([...key, 'bottom']);
    final left = source.v<double>([...key, 'left']);
    final right = source.v<double>([...key, 'right']);
    return EdgeInsets.only(
      top: top ?? 0,
      bottom: bottom ?? 0,
      left: left ?? 0,
      right: right ?? 0,
    );
  }

  static Size? size(DataSource source, List<Object> key) {
    if (!source.isMap(key)) {
      return null;
    }
    return Size(
      source.v<double>([...key, 'width']) ?? 0.0,
      source.v<double>([...key, 'height']) ?? 0.0,
    );
  }

  static MouseCursor? mouseCursor(DataSource source, List<Object> key) {
    if (!source.isMap(key)) {
      return null;
    }
    final type = source.v<String>([...key, 'type']);
    final value = source.v<String>([...key, 'value']);
    if (type == 'system') {
      switch (value) {
        case 'alias':
          return SystemMouseCursors.alias;
        case 'none':
          return SystemMouseCursors.none;
        case 'basic':
          return SystemMouseCursors.basic;
        case 'click':
          return SystemMouseCursors.click;
        case 'forbidden':
          return SystemMouseCursors.forbidden;
        case 'wait':
          return SystemMouseCursors.wait;
        case 'progress':
          return SystemMouseCursors.progress;
        case 'contextMenu':
          return SystemMouseCursors.contextMenu;
        case 'help':
          return SystemMouseCursors.help;
        case 'text':
          return SystemMouseCursors.text;
        case 'verticalText':
          return SystemMouseCursors.verticalText;
        case 'cell':
          return SystemMouseCursors.cell;
        case 'precise':
          return SystemMouseCursors.precise;
        case 'move':
          return SystemMouseCursors.move;
        case 'grab':
          return SystemMouseCursors.grab;
        case 'grabbing':
          return SystemMouseCursors.grabbing;
        case 'noDrop':
          return SystemMouseCursors.noDrop;
        case 'alias':
          return SystemMouseCursors.alias;
        case 'copy':
          return SystemMouseCursors.copy;
        case 'disappearing':
          return SystemMouseCursors.disappearing;
        case 'allScroll':
          return SystemMouseCursors.allScroll;
        case 'resizeLeftRight':
          return SystemMouseCursors.resizeLeftRight;
        case 'resizeUpDown':
          return SystemMouseCursors.resizeUpDown;
        case 'resizeUpLeftDownRight':
          return SystemMouseCursors.resizeUpLeftDownRight;
        case 'resizeUpRightDownLeft':
          return SystemMouseCursors.resizeUpRightDownLeft;
        case 'resizeUp':
          return SystemMouseCursors.resizeUp;
        case 'resizeDown':
          return SystemMouseCursors.resizeDown;
        case 'resizeLeft':
          return SystemMouseCursors.resizeLeft;
        case 'resizeRight':
          return SystemMouseCursors.resizeRight;
        case 'resizeUpLeft':
          return SystemMouseCursors.resizeUpLeft;
        case 'resizeUpRight':
          return SystemMouseCursors.resizeUpRight;
        case 'resizeDownLeft':
          return SystemMouseCursors.resizeDownLeft;
        case 'resizeDownRight':
          return SystemMouseCursors.resizeDownRight;
        case 'resizeColumn':
          return SystemMouseCursors.resizeColumn;
        case 'resizeRow':
          return SystemMouseCursors.resizeRow;
        case 'zoomIn':
          return SystemMouseCursors.zoomIn;
        case 'zoomOut':
          return SystemMouseCursors.zoomOut;
        default:
      }
    }
    return null;
  }

  static LinearBorderEdge? linearBorderEdge(
      DataSource source, List<Object> key) {
    if (!source.isMap(key)) {
      return null;
    }
    return LinearBorderEdge(
      size: source.v<double>([...key, 'size']) ?? 1.0,
      alignment: source.v<double>([...key, 'alignment']) ?? 0.0,
    );
  }

  static OutlinedBorder? outlinedBorder(DataSource source, List<Object> key) {
    if (!source.isMap(key)) {
      return null;
    }
    final type = source.v<String>([...key, 'type']);
    switch (type) {
      case "RoundedRectangleBorder":
        return RoundedRectangleBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          borderRadius:
              ArgumentDecoders.borderRadius(source, [...key, 'borderRadius']) ??
                  BorderRadius.zero,
        );
      case "BeveledRectangleBorder":
        return BeveledRectangleBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          borderRadius:
              ArgumentDecoders.borderRadius(source, [...key, 'borderRadius']) ??
                  BorderRadius.zero,
        );
      case "ContinuousRectangleBorder":
        return ContinuousRectangleBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          borderRadius:
              ArgumentDecoders.borderRadius(source, [...key, 'borderRadius']) ??
                  BorderRadius.zero,
        );
      case "CircleBorder":
        return CircleBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          eccentricity: source.v<double>([...key, 'eccentricity']) ?? 0.0,
        );
      case "LinearBorder":
        return LinearBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          start: CustomArgumentDecoders.linearBorderEdge(
              source, [...key, 'start']),
          end: CustomArgumentDecoders.linearBorderEdge(source, [...key, 'end']),
          top: CustomArgumentDecoders.linearBorderEdge(source, [...key, 'top']),
          bottom: CustomArgumentDecoders.linearBorderEdge(
              source, [...key, 'bottom']),
        );
      case "OvalBorder":
        return OvalBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          eccentricity: source.v<double>([...key, 'eccentricity']) ?? 0.0,
        );
      case "StadiumBorder":
        return StadiumBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
        );
      case "StarBorder":
        return StarBorder(
          side: ArgumentDecoders.borderSide(source, [...key, 'side']) ??
              BorderSide.none,
          points: source.v<double>([...key, 'points']) ?? 5.0,
          innerRadiusRatio:
              source.v<double>([...key, 'innerRadiusRatio']) ?? 0.4,
          pointRounding: source.v<double>([...key, 'pointRounding']) ?? 0.0,
          valleyRounding: source.v<double>([...key, 'valleyRounding']) ?? 0.0,
          rotation: source.v<double>([...key, 'rotation']) ?? 0.0,
          squash: source.v<double>([...key, 'squash']) ?? 0.0,
        );
      default:
        break;
    }
    return null;
  }
}
```

This creates the custom decoders needed for the widgets we are about to define.

### Defining the core library 

Create and update the following file located at `app/lib/rfw/core.dart`:

```
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:rfw/rfw.dart';

LocalWidgetLibrary createCoreWidgets() =>
    LocalWidgetLibrary(_coreWidgetsDefinitions);

Map<String, LocalWidgetBuilder> get _coreWidgetsDefinitions =>
    <String, LocalWidgetBuilder>{
      'AnimationDefaults': (BuildContext context, DataSource source) {
        return AnimationDefaults(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          child: source.child(['child']),
        );
      },
      'Align': (BuildContext context, DataSource source) {
        return AnimatedAlign(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          alignment: ArgumentDecoders.alignment(source, ['alignment']) ??
              Alignment.center,
          widthFactor: source.v<double>(['widthFactor']),
          heightFactor: source.v<double>(['heightFactor']),
          onEnd: source.voidHandler(['onEnd']),
          child: source.optionalChild(['child']),
        );
      },
      'AspectRatio': (BuildContext context, DataSource source) {
        return AspectRatio(
          aspectRatio: source.v<double>(['aspectRatio']) ?? 1.0,
          child: source.optionalChild(['child']),
        );
      },
      'Center': (BuildContext context, DataSource source) {
        return Center(
          widthFactor: source.v<double>(['widthFactor']),
          heightFactor: source.v<double>(['heightFactor']),
          child: source.optionalChild(['child']),
        );
      },
      'ColoredBox': (BuildContext context, DataSource source) {
        return ColoredBox(
          color: ArgumentDecoders.color(source, ['color']) ??
              const Color(0xFF000000),
          child: source.optionalChild(['child']),
        );
      },
      'Column': (BuildContext context, DataSource source) {
        return Column(
          mainAxisAlignment: ArgumentDecoders.enumValue<MainAxisAlignment>(
                  MainAxisAlignment.values, source, ['mainAxisAlignment']) ??
              MainAxisAlignment.start,
          mainAxisSize: ArgumentDecoders.enumValue<MainAxisSize>(
                  MainAxisSize.values, source, ['mainAxisSize']) ??
              MainAxisSize.max,
          crossAxisAlignment: ArgumentDecoders.enumValue<CrossAxisAlignment>(
                  CrossAxisAlignment.values, source, ['crossAxisAlignment']) ??
              CrossAxisAlignment.center,
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
              TextDirection.values, source, ['textDirection']),
          verticalDirection: ArgumentDecoders.enumValue<VerticalDirection>(
                  VerticalDirection.values, source, ['verticalDirection']) ??
              VerticalDirection.down,
          textBaseline: ArgumentDecoders.enumValue<TextBaseline>(
              TextBaseline.values, source, ['textBaseline']),
          children: source.childList(['children']),
        );
      },
      'Container': (BuildContext context, DataSource source) {
        return AnimatedContainer(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          alignment: ArgumentDecoders.alignment(source, ['alignment']),
          padding: ArgumentDecoders.edgeInsets(source, ['padding']),
          color: ArgumentDecoders.color(source, ['color']),
          decoration: ArgumentDecoders.decoration(source, ['decoration']),
          foregroundDecoration:
              ArgumentDecoders.decoration(source, ['foregroundDecoration']),
          width: source.v<double>(['width']),
          height: source.v<double>(['height']),
          constraints: ArgumentDecoders.boxConstraints(source, ['constraints']),
          margin: ArgumentDecoders.edgeInsets(source, ['margin']),
          transform: ArgumentDecoders.matrix(source, ['transform']),
          transformAlignment:
              ArgumentDecoders.alignment(source, ['transformAlignment']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          onEnd: source.voidHandler(['onEnd']),
          child: source.optionalChild(['child']),
        );
      },
      'DefaultTextStyle': (BuildContext context, DataSource source) {
        return AnimatedDefaultTextStyle(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          style: ArgumentDecoders.textStyle(source, ['style']) ??
              const TextStyle(),
          textAlign: ArgumentDecoders.enumValue<TextAlign>(
              TextAlign.values, source, ['textAlign']),
          softWrap: source.v<bool>(['softWrap']) ?? true,
          overflow: ArgumentDecoders.enumValue<TextOverflow>(
                  TextOverflow.values, source, ['overflow']) ??
              TextOverflow.clip,
          maxLines: source.v<int>(['maxLines']),
          textWidthBasis: ArgumentDecoders.enumValue<TextWidthBasis>(
                  TextWidthBasis.values, source, ['textWidthBasis']) ??
              TextWidthBasis.parent,
          textHeightBehavior: ArgumentDecoders.textHeightBehavior(
              source, ['textHeightBehavior']),
          onEnd: source.voidHandler(['onEnd']),
          child: source.child(['child']),
        );
      },
      'Directionality': (BuildContext context, DataSource source) {
        return Directionality(
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
                  TextDirection.values, source, ['textDirection']) ??
              TextDirection.ltr,
          child: source.child(['child']),
        );
      },
      'Expanded': (BuildContext context, DataSource source) {
        return Expanded(
          flex: source.v<int>(['flex']) ?? 1,
          child: source.child(['child']),
        );
      },
      'FittedBox': (BuildContext context, DataSource source) {
        return FittedBox(
          fit: ArgumentDecoders.enumValue<BoxFit>(
                  BoxFit.values, source, ['fit']) ??
              BoxFit.contain,
          alignment: ArgumentDecoders.alignment(source, ['alignment']) ??
              Alignment.center,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          child: source.optionalChild(['child']),
        );
      },
      'FractionallySizedBox': (BuildContext context, DataSource source) {
        return FractionallySizedBox(
          alignment: ArgumentDecoders.alignment(source, ['alignment']) ??
              Alignment.center,
          widthFactor: source.v<double>(['widthFactor']),
          heightFactor: source.v<double>(['heightFactor']),
          child: source.child(['child']),
        );
      },
      'GestureDetector': (BuildContext context, DataSource source) {
        return GestureDetector(
          onTap: source.voidHandler(['onTap']),
          onTapDown: source.handler(['onTapDown'],
              (VoidCallback trigger) => (TapDownDetails details) => trigger()),
          onTapUp: source.handler(['onTapUp'],
              (VoidCallback trigger) => (TapUpDetails details) => trigger()),
          onTapCancel: source.voidHandler(['onTapCancel']),
          onDoubleTap: source.voidHandler(['onDoubleTap']),
          onLongPress: source.voidHandler(['onLongPress']),
          behavior: ArgumentDecoders.enumValue<HitTestBehavior>(
              HitTestBehavior.values, source, ['behavior']),
          child: source.optionalChild(['child']),
        );
      },
      'GridView': (BuildContext context, DataSource source) {
        return GridView.builder(
          scrollDirection: ArgumentDecoders.enumValue<Axis>(
                  Axis.values, source, ['scrollDirection']) ??
              Axis.vertical,
          reverse: source.v<bool>(['reverse']) ?? false,
          primary: source.v<bool>(['primary']),
          shrinkWrap: source.v<bool>(['shrinkWrap']) ?? false,
          padding: ArgumentDecoders.edgeInsets(source, ['padding']),
          gridDelegate:
              ArgumentDecoders.gridDelegate(source, ['gridDelegate']) ??
                  const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2),
          itemBuilder: (BuildContext context, int index) =>
              source.child(['children', index]),
          itemCount: source.length(['children']),
          addAutomaticKeepAlives:
              source.v<bool>(['addAutomaticKeepAlives']) ?? true,
          addRepaintBoundaries:
              source.v<bool>(['addRepaintBoundaries']) ?? true,
          addSemanticIndexes: source.v<bool>(['addSemanticIndexes']) ?? true,
          cacheExtent: source.v<double>(['cacheExtent']),
          semanticChildCount: source.v<int>(['semanticChildCount']),
          dragStartBehavior: ArgumentDecoders.enumValue<DragStartBehavior>(
                  DragStartBehavior.values, source, ['dragStartBehavior']) ??
              DragStartBehavior.start,
          keyboardDismissBehavior:
              ArgumentDecoders.enumValue<ScrollViewKeyboardDismissBehavior>(
                      ScrollViewKeyboardDismissBehavior.values,
                      source,
                      ['keyboardDismissBehavior']) ??
                  ScrollViewKeyboardDismissBehavior.manual,
          restorationId: source.v<String>(['restorationId']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.hardEdge,
        );
      },
      'Icon': (BuildContext context, DataSource source) {
        return Icon(
          ArgumentDecoders.iconData(source, []) ?? Icons.flutter_dash,
          size: source.v<double>(['size']),
          color: ArgumentDecoders.color(source, ['color']),
          semanticLabel: source.v<String>(['semanticLabel']),
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
              TextDirection.values, source, ['textDirection']),
        );
      },
      'IconTheme': (BuildContext context, DataSource source) {
        return IconTheme(
          data: ArgumentDecoders.iconThemeData(source, []) ??
              const IconThemeData(),
          child: source.child(['child']),
        );
      },
      'IntrinsicHeight': (BuildContext context, DataSource source) {
        return IntrinsicHeight(
          child: source.optionalChild(['child']),
        );
      },
      'IntrinsicWidth': (BuildContext context, DataSource source) {
        return IntrinsicWidth(
          stepWidth: source.v<double>(['width']),
          stepHeight: source.v<double>(['height']),
          child: source.optionalChild(['child']),
        );
      },
      'Image': (BuildContext context, DataSource source) {
        return Image(
          image: ArgumentDecoders.imageProvider(source, []) ??
              const AssetImage('error.png'),
          semanticLabel: source.v<String>(['semanticLabel']),
          excludeFromSemantics:
              source.v<bool>(['excludeFromSemantics']) ?? false,
          width: source.v<double>(['width']),
          height: source.v<double>(['height']),
          color: ArgumentDecoders.color(source, ['color']),
          colorBlendMode: ArgumentDecoders.enumValue<BlendMode>(
              BlendMode.values, source, ['blendMode']),
          fit: ArgumentDecoders.enumValue<BoxFit>(
              BoxFit.values, source, ['fit']),
          alignment: ArgumentDecoders.alignment(source, ['alignment']) ??
              Alignment.center,
          repeat: ArgumentDecoders.enumValue<ImageRepeat>(
                  ImageRepeat.values, source, ['repeat']) ??
              ImageRepeat.noRepeat,
          centerSlice: ArgumentDecoders.rect(source, ['centerSlice']),
          matchTextDirection: source.v<bool>(['matchTextDirection']) ?? false,
          gaplessPlayback: source.v<bool>(['gaplessPlayback']) ?? false,
          isAntiAlias: source.v<bool>(['isAntiAlias']) ?? false,
          filterQuality: ArgumentDecoders.enumValue<FilterQuality>(
                  FilterQuality.values, source, ['filterQuality']) ??
              FilterQuality.low,
        );
      },
      'ListBody': (BuildContext context, DataSource source) {
        return ListBody(
          mainAxis: ArgumentDecoders.enumValue<Axis>(
                  Axis.values, source, ['mainAxis']) ??
              Axis.vertical,
          reverse: source.v<bool>(['reverse']) ?? false,
          children: source.childList(['children']),
        );
      },
      'ListView': (BuildContext context, DataSource source) {
        return ListView.builder(
          scrollDirection: ArgumentDecoders.enumValue<Axis>(
                  Axis.values, source, ['scrollDirection']) ??
              Axis.vertical,
          reverse: source.v<bool>(['reverse']) ?? false,
          primary: source.v<bool>(['primary']),
          shrinkWrap: source.v<bool>(['shrinkWrap']) ?? false,
          padding: ArgumentDecoders.edgeInsets(source, ['padding']),
          itemExtent: source.v<double>(['itemExtent']),
          prototypeItem: source.optionalChild(['prototypeItem']),
          itemCount: source.length(['children']),
          itemBuilder: (BuildContext context, int index) =>
              source.child(['children', index]),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.hardEdge,
          addAutomaticKeepAlives:
              source.v<bool>(['addAutomaticKeepAlives']) ?? true,
          addRepaintBoundaries:
              source.v<bool>(['addRepaintBoundaries']) ?? true,
          addSemanticIndexes: source.v<bool>(['addSemanticIndexes']) ?? true,
          cacheExtent: source.v<double>(['cacheExtent']),
          semanticChildCount: source.v<int>(['semanticChildCount']),
          dragStartBehavior: ArgumentDecoders.enumValue<DragStartBehavior>(
                  DragStartBehavior.values, source, ['dragStartBehavior']) ??
              DragStartBehavior.start,
          keyboardDismissBehavior:
              ArgumentDecoders.enumValue<ScrollViewKeyboardDismissBehavior>(
                      ScrollViewKeyboardDismissBehavior.values,
                      source,
                      ['keyboardDismissBehavior']) ??
                  ScrollViewKeyboardDismissBehavior.manual,
          restorationId: source.v<String>(['restorationId']),
        );
      },
      'Opacity': (BuildContext context, DataSource source) {
        return AnimatedOpacity(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          opacity: source.v<double>(['opacity']) ?? 0.0,
          onEnd: source.voidHandler(['onEnd']),
          alwaysIncludeSemantics:
              source.v<bool>(['alwaysIncludeSemantics']) ?? true,
        );
      },
      'Padding': (BuildContext context, DataSource source) {
        return AnimatedPadding(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          padding: ArgumentDecoders.edgeInsets(source, ['padding']) ??
              EdgeInsets.zero,
          onEnd: source.voidHandler(['onEnd']),
          child: source.optionalChild(['child']),
        );
      },
      'Placeholder': (BuildContext context, DataSource source) {
        return Placeholder(
          color: ArgumentDecoders.color(source, ['color']) ??
              const Color(0xFF455A64),
          strokeWidth: source.v<double>(['strokeWidth']) ?? 2.0,
          fallbackWidth: source.v<double>(['placeholderWidth']) ?? 400.0,
          fallbackHeight: source.v<double>(['placeholderHeight']) ?? 400.0,
        );
      },
      'Positioned': (BuildContext context, DataSource source) {
        return AnimatedPositionedDirectional(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          start: source.v<double>(['start']),
          top: source.v<double>(['top']),
          end: source.v<double>(['end']),
          bottom: source.v<double>(['bottom']),
          width: source.v<double>(['width']),
          height: source.v<double>(['height']),
          onEnd: source.voidHandler(['onEnd']),
          child: source.child(['child']),
        );
      },
      'Rotation': (BuildContext context, DataSource source) {
        return AnimatedRotation(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          turns: source.v<double>(['turns']) ?? 0.0,
          alignment: (ArgumentDecoders.alignment(source, ['alignment']) ??
                  Alignment.center)
              .resolve(Directionality.of(context)),
          filterQuality: ArgumentDecoders.enumValue<FilterQuality>(
              FilterQuality.values, source, ['filterQuality']),
          onEnd: source.voidHandler(['onEnd']),
          child: source.optionalChild(['child']),
        );
      },
      'Row': (BuildContext context, DataSource source) {
        return Row(
          mainAxisAlignment: ArgumentDecoders.enumValue<MainAxisAlignment>(
                  MainAxisAlignment.values, source, ['mainAxisAlignment']) ??
              MainAxisAlignment.start,
          mainAxisSize: ArgumentDecoders.enumValue<MainAxisSize>(
                  MainAxisSize.values, source, ['mainAxisSize']) ??
              MainAxisSize.max,
          crossAxisAlignment: ArgumentDecoders.enumValue<CrossAxisAlignment>(
                  CrossAxisAlignment.values, source, ['crossAxisAlignment']) ??
              CrossAxisAlignment.center,
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
              TextDirection.values, source, ['textDirection']),
          verticalDirection: ArgumentDecoders.enumValue<VerticalDirection>(
                  VerticalDirection.values, source, ['verticalDirection']) ??
              VerticalDirection.down,
          textBaseline: ArgumentDecoders.enumValue<TextBaseline>(
              TextBaseline.values, source, ['textBaseline']),
          children: source.childList(['children']),
        );
      },
      'SafeArea': (BuildContext context, DataSource source) {
        return SafeArea(
          left: source.v<bool>(['left']) ?? true,
          top: source.v<bool>(['top']) ?? true,
          right: source.v<bool>(['right']) ?? true,
          bottom: source.v<bool>(['bottom']) ?? true,
          minimum: (ArgumentDecoders.edgeInsets(source, ['minimum']) ??
                  EdgeInsets.zero)
              .resolve(Directionality.of(context)),
          maintainBottomViewPadding:
              source.v<bool>(['maintainBottomViewPadding']) ?? false,
          child: source.child(['child']),
        );
      },
      'Scale': (BuildContext context, DataSource source) {
        return AnimatedScale(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          scale: source.v<double>(['scale']) ?? 1.0,
          alignment: (ArgumentDecoders.alignment(source, ['alignment']) ??
                  Alignment.center)
              .resolve(Directionality.of(context)),
          filterQuality: ArgumentDecoders.enumValue<FilterQuality>(
              FilterQuality.values, source, ['filterQuality']),
          onEnd: source.voidHandler(['onEnd']),
          child: source.optionalChild(['child']),
        );
      },
      'SingleChildScrollView': (BuildContext context, DataSource source) {
        return SingleChildScrollView(
          scrollDirection: ArgumentDecoders.enumValue<Axis>(
                  Axis.values, source, ['scrollDirection']) ??
              Axis.vertical,
          reverse: source.v<bool>(['reverse']) ?? false,
          padding: ArgumentDecoders.edgeInsets(source, ['padding']),
          primary: source.v<bool>(['primary']) ?? true,
          dragStartBehavior: ArgumentDecoders.enumValue<DragStartBehavior>(
                  DragStartBehavior.values, source, ['dragStartBehavior']) ??
              DragStartBehavior.start,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.hardEdge,
          restorationId: source.v<String>(['restorationId']),
          keyboardDismissBehavior:
              ArgumentDecoders.enumValue<ScrollViewKeyboardDismissBehavior>(
                      ScrollViewKeyboardDismissBehavior.values,
                      source,
                      ['keyboardDismissBehavior']) ??
                  ScrollViewKeyboardDismissBehavior.manual,
          child: source.optionalChild(['child']),
        );
      },
      'SizedBox': (BuildContext context, DataSource source) {
        return SizedBox(
          width: source.v<double>(['width']),
          height: source.v<double>(['height']),
          child: source.optionalChild(['child']),
        );
      },
      'SizedBoxExpand': (BuildContext context, DataSource source) {
        return SizedBox.expand(
          child: source.optionalChild(['child']),
        );
      },
      'SizedBoxShrink': (BuildContext context, DataSource source) {
        return SizedBox.shrink(
          child: source.optionalChild(['child']),
        );
      },
      'Spacer': (BuildContext context, DataSource source) {
        return Spacer(
          flex: source.v<int>(['flex']) ?? 1,
        );
      },
      'Stack': (BuildContext context, DataSource source) {
        return Stack(
          alignment: ArgumentDecoders.alignment(source, ['alignment']) ??
              AlignmentDirectional.topStart,
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
              TextDirection.values, source, ['textDirection']),
          fit: ArgumentDecoders.enumValue<StackFit>(
                  StackFit.values, source, ['fit']) ??
              StackFit.loose,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.hardEdge,
          children: source.childList(['children']),
        );
      },
      'Text': (BuildContext context, DataSource source) {
        String? text = source.v<String>(['text']);
        if (text == null) {
          final StringBuffer builder = StringBuffer();
          final int count = source.length(['text']);
          for (int index = 0; index < count; index += 1) {
            builder.write(source.v<String>(['text', index]) ?? '');
          }
          text = builder.toString();
        }
        return Text(
          text,
          style: ArgumentDecoders.textStyle(source, ['style']),
          strutStyle: ArgumentDecoders.strutStyle(source, ['strutStyle']),
          textAlign: ArgumentDecoders.enumValue<TextAlign>(
              TextAlign.values, source, ['textAlign']),
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
              TextDirection.values, source, ['textDirection']),
          locale: ArgumentDecoders.locale(source, ['locale']),
          softWrap: source.v<bool>(['softWrap']),
          overflow: ArgumentDecoders.enumValue<TextOverflow>(
              TextOverflow.values, source, ['overflow']),
          textScaleFactor: source.v<double>(['textScaleFactor']),
          maxLines: source.v<int>(['maxLines']),
          semanticsLabel: source.v<String>(['semanticsLabel']),
          textWidthBasis: ArgumentDecoders.enumValue<TextWidthBasis>(
              TextWidthBasis.values, source, ['textWidthBasis']),
          textHeightBehavior: ArgumentDecoders.textHeightBehavior(
              source, ['textHeightBehavior']),
        );
      },
      'Wrap': (BuildContext context, DataSource source) {
        return Wrap(
          direction: ArgumentDecoders.enumValue<Axis>(
                  Axis.values, source, ['direction']) ??
              Axis.horizontal,
          alignment: ArgumentDecoders.enumValue<WrapAlignment>(
                  WrapAlignment.values, source, ['alignment']) ??
              WrapAlignment.start,
          spacing: source.v<double>(['spacing']) ?? 0.0,
          runAlignment: ArgumentDecoders.enumValue<WrapAlignment>(
                  WrapAlignment.values, source, ['runAlignment']) ??
              WrapAlignment.start,
          runSpacing: source.v<double>(['runSpacing']) ?? 0.0,
          crossAxisAlignment: ArgumentDecoders.enumValue<WrapCrossAlignment>(
                  WrapCrossAlignment.values, source, ['crossAxisAlignment']) ??
              WrapCrossAlignment.start,
          textDirection: ArgumentDecoders.enumValue<TextDirection>(
              TextDirection.values, source, ['textDirection']),
          verticalDirection: ArgumentDecoders.enumValue<VerticalDirection>(
                  VerticalDirection.values, source, ['verticalDirection']) ??
              VerticalDirection.down,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          children: source.childList(['children']),
        );
      },
    };
```

This created all the core widgets that are not apart of a design system. Keeping these separate will let you update the design system separately than the core widgets.

### Defining the Material library 

Create and update the following file located at `app/lib/rfw/material.dart`:

```
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:rfw/rfw.dart';

import 'decoders.dart';

LocalWidgetLibrary createMaterialWidgets() =>
    LocalWidgetLibrary(_materialWidgetsDefinitions);

Map<String, LocalWidgetBuilder> get _materialWidgetsDefinitions =>
    <String, LocalWidgetBuilder>{
      'AboutListTile': (context, source) {
        return AboutListTile(
          icon: source.optionalChild(['icon']),
          applicationName: source.v<String>(['applicationName']),
          applicationVersion: source.v<String>(['applicationVersion']),
          applicationIcon: source.optionalChild(['applicationIcon']),
          applicationLegalese: source.v<String>(['applicationLegalese']),
          aboutBoxChildren: source.childList(['aboutBoxChildren']),
          dense: source.v<bool>(['dense']),
          child: source.optionalChild(['child']),
        );
      },
      'AppBar': (context, source) {
        return AppBar(
          leading: source.optionalChild(['leading']),
          automaticallyImplyLeading:
              source.v<bool>(['automaticallyImplyLeading']) ?? true,
          title: source.optionalChild(['title']),
          actions: source.childList(['actions']),
          elevation: source.v<double>(['elevation']),
          shadowColor: ArgumentDecoders.color(source, ['shadowColor']),
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
          iconTheme: ArgumentDecoders.iconThemeData(source, ['iconTheme']),
          actionsIconTheme:
              ArgumentDecoders.iconThemeData(source, ['actionsIconTheme']),
          primary: source.v<bool>(['primary']) ?? true,
          centerTitle: source.v<bool>(['centerTitle']),
          excludeHeaderSemantics:
              source.v<bool>(['excludeHeaderSemantics']) ?? false,
          titleSpacing: source.v<double>(['titleSpacing']),
          toolbarOpacity: source.v<double>(['toolbarOpacity']) ?? 1.0,
          toolbarHeight: source.v<double>(['toolbarHeight']),
          leadingWidth: source.v<double>(['leadingWidth']),
          toolbarTextStyle:
              ArgumentDecoders.textStyle(source, ['toolbarTextStyle']),
          titleTextStyle:
              ArgumentDecoders.textStyle(source, ['titleTextStyle']),
        );
      },
      'ButtonBar': (context, source) {
        return ButtonBar(
          alignment: ArgumentDecoders.enumValue<MainAxisAlignment>(
                  MainAxisAlignment.values, source, ['alignment']) ??
              MainAxisAlignment.start,
          mainAxisSize: ArgumentDecoders.enumValue<MainAxisSize>(
                  MainAxisSize.values, source, ['mainAxisSize']) ??
              MainAxisSize.max,
          buttonMinWidth: source.v<double>(['buttonMinWidth']),
          buttonHeight: source.v<double>(['buttonHeight']),
          buttonPadding: ArgumentDecoders.edgeInsets(source, ['buttonPadding']),
          buttonAlignedDropdown:
              source.v<bool>(['buttonAlignedDropdown']) ?? false,
          layoutBehavior: ArgumentDecoders.enumValue<ButtonBarLayoutBehavior>(
              ButtonBarLayoutBehavior.values, source, ['layoutBehavior']),
          overflowDirection: ArgumentDecoders.enumValue<VerticalDirection>(
              VerticalDirection.values, source, ['overflowDirection']),
          overflowButtonSpacing: source.v<double>(['overflowButtonSpacing']),
          children: source.childList(['children']),
        );
      },
      'Card': (context, source) {
        return Card(
          color: ArgumentDecoders.color(source, ['color']),
          shadowColor: ArgumentDecoders.color(source, ['shadowColor']),
          elevation: source.v<double>(['elevation']),
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          borderOnForeground: source.v<bool>(['borderOnForeground']) ?? true,
          margin: ArgumentDecoders.edgeInsets(source, ['margin']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          semanticContainer: source.v<bool>(['semanticContainer']) ?? true,
          child: source.optionalChild(['child']),
        );
      },
      'CircularProgressIndicator': (context, source) {
        return CircularProgressIndicator(
          value: source.v<double>(['value']),
          color: ArgumentDecoders.color(source, ['color']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          strokeWidth: source.v<double>(['strokeWidth']) ?? 4.0,
          semanticsLabel: source.v<String>(['semanticsLabel']),
          semanticsValue: source.v<String>(['semanticsValue']),
        );
      },
      'Divider': (context, source) {
        return Divider(
          height: source.v<double>(['height']),
          thickness: source.v<double>(['thickness']),
          indent: source.v<double>(['indent']),
          endIndent: source.v<double>(['endIndent']),
          color: ArgumentDecoders.color(source, ['color']),
        );
      },
      'Drawer': (context, source) {
        return Drawer(
          elevation: source.v<double>(['elevation']) ?? 16.0,
          semanticLabel: source.v<String>(['semanticLabel']),
          child: source.optionalChild(['child']),
        );
      },
      'DrawerHeader': (context, source) {
        return DrawerHeader(
          duration: ArgumentDecoders.duration(source, ['duration'], context),
          curve: ArgumentDecoders.curve(source, ['curve'], context),
          decoration: ArgumentDecoders.decoration(source, ['decoration']),
          margin: ArgumentDecoders.edgeInsets(source, ['margin']) ??
              const EdgeInsets.only(bottom: 8.0),
          padding: ArgumentDecoders.edgeInsets(source, ['padding']) ??
              const EdgeInsets.fromLTRB(16.0, 16.0, 16.0, 8.0),
          child: source.optionalChild(['child']),
        );
      },
      'ElevatedButton': (context, source) {
        return ElevatedButton(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          child: source.child(['child']),
        );
      },
      'InkWell': (context, source) {
        return InkWell(
          onTap: source.voidHandler(['onTap']),
          onDoubleTap: source.voidHandler(['onDoubleTap']),
          onLongPress: source.voidHandler(['onLongPress']),
          onTapDown: source.handler(['onTapDown'],
              (VoidCallback trigger) => (TapDownDetails details) => trigger()),
          onTapCancel: source.voidHandler(['onTapCancel']),
          radius: source.v<double>(['radius']),
          borderRadius: ArgumentDecoders.borderRadius(source, ['borderRadius'])
              ?.resolve(Directionality.of(context)),
          customBorder: ArgumentDecoders.shapeBorder(source, ['customBorder']),
          enableFeedback: source.v<bool>(['enableFeedback']) ?? true,
          excludeFromSemantics:
              source.v<bool>(['excludeFromSemantics']) ?? false,
          autofocus: source.v<bool>(['autofocus']) ?? false,
          child: source.optionalChild(['child']),
        );
      },
      'LinearProgressIndicator': (context, source) {
        return LinearProgressIndicator(
          value: source.v<double>(['value']),
          color: ArgumentDecoders.color(source, ['color']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          minHeight: source.v<double>(['minHeight']),
          semanticsLabel: source.v<String>(['semanticsLabel']),
          semanticsValue: source.v<String>(['semanticsValue']),
        );
      },
      'ListTile': (context, source) {
        return ListTile(
          leading: source.optionalChild(['leading']),
          title: source.optionalChild(['title']),
          subtitle: source.optionalChild(['subtitle']),
          trailing: source.optionalChild(['trailing']),
          isThreeLine: source.v<bool>(['isThreeLine']) ?? false,
          dense: source.v<bool>(['dense']),
          visualDensity:
              ArgumentDecoders.visualDensity(source, ['visualDensity']),
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          contentPadding:
              ArgumentDecoders.edgeInsets(source, ['contentPadding']),
          enabled: source.v<bool>(['enabled']) ?? true,
          onTap: source.voidHandler(['onTap']),
          onLongPress: source.voidHandler(['onLongPress']),
          selected: source.v<bool>(['selected']) ?? false,
          focusColor: ArgumentDecoders.color(source, ['focusColor']),
          hoverColor: ArgumentDecoders.color(source, ['hoverColor']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          tileColor: ArgumentDecoders.color(source, ['tileColor']),
          selectedTileColor:
              ArgumentDecoders.color(source, ['selectedTileColor']),
          enableFeedback: source.v<bool>(['enableFeedback']),
          horizontalTitleGap: source.v<double>(['horizontalTitleGap']),
          minVerticalPadding: source.v<double>(['minVerticalPadding']),
          minLeadingWidth: source.v<double>(['minLeadingWidth']),
        );
      },
      'Scaffold': (context, source) {
        final Widget? appBarWidget = source.optionalChild(['appBar']);
        final List<Widget> persistentFooterButtons =
            source.childList(['persistentFooterButtons']);
        return Scaffold(
          appBar: appBarWidget == null
              ? null
              : PreferredSize(
                  preferredSize: Size.fromHeight(
                      source.v<double>(['bottomHeight']) ?? 56.0),
                  child: appBarWidget,
                ),
          body: source.optionalChild(['body']),
          floatingActionButton: source.optionalChild(['floatingActionButton']),
          persistentFooterButtons:
              persistentFooterButtons.isEmpty ? null : persistentFooterButtons,
          drawer: source.optionalChild(['drawer']),
          endDrawer: source.optionalChild(['endDrawer']),
          bottomNavigationBar: source.optionalChild(['bottomNavigationBar']),
          bottomSheet: source.optionalChild(['bottomSheet']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          resizeToAvoidBottomInset:
              source.v<bool>(['resizeToAvoidBottomInset']),
          primary: source.v<bool>(['primary']) ?? true,
          drawerDragStartBehavior:
              ArgumentDecoders.enumValue<DragStartBehavior>(
                      DragStartBehavior.values,
                      source,
                      ['drawerDragStartBehavior']) ??
                  DragStartBehavior.start,
          extendBody: source.v<bool>(['extendBody']) ?? false,
          extendBodyBehindAppBar:
              source.v<bool>(['extendBodyBehindAppBar']) ?? false,
          drawerScrimColor:
              ArgumentDecoders.color(source, ['drawerScrimColor']),
          drawerEdgeDragWidth: source.v<double>(['drawerEdgeDragWidth']),
          drawerEnableOpenDragGesture:
              source.v<bool>(['drawerEnableOpenDragGesture']) ?? true,
          endDrawerEnableOpenDragGesture:
              source.v<bool>(['endDrawerEnableOpenDragGesture']) ?? true,
          restorationId: source.v<String>(['restorationId']),
        );
      },
      'VerticalDivider': (context, source) {
        return VerticalDivider(
          width: source.v<double>(['width']),
          thickness: source.v<double>(['thickness']),
          indent: source.v<double>(['indent']),
          endIndent: source.v<double>(['endIndent']),
          color: ArgumentDecoders.color(source, ['color']),
        );
      },
      'FilledButton': (context, source) {
        return FilledButton(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.filledButtonStyle(
              source, ['style'], context),
          child: source.child(['child']),
        );
      },
      'FilledButtonIcon': (context, source) {
        return FilledButton.icon(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.filledButtonStyle(
              source, ['style'], context),
          icon: source.child(['icon']),
          label: source.child(['label']),
        );
      },
      'FilledButtonTonal': (context, source) {
        return FilledButton.tonal(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.filledButtonStyle(
              source, ['style'], context),
          child: source.child(['child']),
        );
      },
      'FilledButtonTonalIcon': (context, source) {
        return FilledButton.tonalIcon(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.filledButtonStyle(
              source, ['style'], context),
          icon: source.child(['icon']),
          label: source.child(['label']),
        );
      },
      'TextButton': (context, source) {
        return TextButton(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.textButtonStyle(
              source, ['style'], context),
          child: source.child(['child']),
        );
      },
      'TextButtonIcon': (context, source) {
        return TextButton.icon(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.textButtonStyle(
              source, ['style'], context),
          icon: source.child(['icon']),
          label: source.child(['label']),
        );
      },
      'OutlinedButton': (context, source) {
        return OutlinedButton(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.outlinedButtonStyle(
              source, ['style'], context),
          child: source.child(['child']),
        );
      },
      'OutlinedButtonIcon': (context, source) {
        return OutlinedButton.icon(
          onPressed: source.voidHandler(['onPressed']),
          onLongPress: source.voidHandler(['onLongPress']),
          autofocus: source.v<bool>(['autofocus']) ?? false,
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          style: CustomArgumentDecoders.outlinedButtonStyle(
              source, ['style'], context),
          icon: source.child(['icon']),
          label: source.child(['label']),
        );
      },
      'FloatingActionButton': (context, source) {
        return FloatingActionButton(
          onPressed: source.voidHandler(['onPressed']),
          tooltip: source.v<String>(['tooltip']),
          foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          focusColor: ArgumentDecoders.color(source, ['focusColor']),
          hoverColor: ArgumentDecoders.color(source, ['hoverColor']),
          splashColor: ArgumentDecoders.color(source, ['splashColor']),
          heroTag: source.v<String>(['heroTag']),
          elevation: source.v<double>(['elevation']),
          focusElevation: source.v<double>(['focusElevation']),
          hoverElevation: source.v<double>(['hoverElevation']),
          highlightElevation: source.v<double>(['highlightElevation']),
          disabledElevation: source.v<double>(['disabledElevation']),
          mini: source.v<bool>(['mini']) ?? false,
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          autofocus: source.v<bool>(['autofocus']) ?? false,
          mouseCursor:
              CustomArgumentDecoders.mouseCursor(source, ['mouseCursor']),
          materialTapTargetSize:
              ArgumentDecoders.enumValue<MaterialTapTargetSize>(
                  MaterialTapTargetSize.values,
                  source,
                  ['materialTapTargetSize']),
          isExtended: source.v<bool>(['isExtended']) ?? false,
          enableFeedback: source.v<bool>(['enableFeedback']),
          child: source.child(['child']),
        );
      },
      'FloatingActionButtonExtended': (context, source) {
        return FloatingActionButton.extended(
          onPressed: source.voidHandler(['onPressed']),
          tooltip: source.v<String>(['tooltip']),
          foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          focusColor: ArgumentDecoders.color(source, ['focusColor']),
          hoverColor: ArgumentDecoders.color(source, ['hoverColor']),
          splashColor: ArgumentDecoders.color(source, ['splashColor']),
          heroTag: source.v<String>(['heroTag']),
          elevation: source.v<double>(['elevation']),
          focusElevation: source.v<double>(['focusElevation']),
          hoverElevation: source.v<double>(['hoverElevation']),
          highlightElevation: source.v<double>(['highlightElevation']),
          disabledElevation: source.v<double>(['disabledElevation']),
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          autofocus: source.v<bool>(['autofocus']) ?? false,
          mouseCursor:
              CustomArgumentDecoders.mouseCursor(source, ['mouseCursor']),
          materialTapTargetSize:
              ArgumentDecoders.enumValue<MaterialTapTargetSize>(
                  MaterialTapTargetSize.values,
                  source,
                  ['materialTapTargetSize']),
          isExtended: source.v<bool>(['isExtended']) ?? true,
          enableFeedback: source.v<bool>(['enableFeedback']),
          label: source.child(['label']),
          icon: source.child(['icon']),
        );
      },
      'FloatingActionButtonSmall': (context, source) {
        return FloatingActionButton.small(
          onPressed: source.voidHandler(['onPressed']),
          tooltip: source.v<String>(['tooltip']),
          foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          focusColor: ArgumentDecoders.color(source, ['focusColor']),
          hoverColor: ArgumentDecoders.color(source, ['hoverColor']),
          splashColor: ArgumentDecoders.color(source, ['splashColor']),
          heroTag: source.v<String>(['heroTag']),
          elevation: source.v<double>(['elevation']),
          focusElevation: source.v<double>(['focusElevation']),
          hoverElevation: source.v<double>(['hoverElevation']),
          highlightElevation: source.v<double>(['highlightElevation']),
          disabledElevation: source.v<double>(['disabledElevation']),
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          autofocus: source.v<bool>(['autofocus']) ?? false,
          mouseCursor:
              CustomArgumentDecoders.mouseCursor(source, ['mouseCursor']),
          materialTapTargetSize:
              ArgumentDecoders.enumValue<MaterialTapTargetSize>(
                  MaterialTapTargetSize.values,
                  source,
                  ['materialTapTargetSize']),
          enableFeedback: source.v<bool>(['enableFeedback']),
          child: source.child(['child']),
        );
      },
      'FloatingActionButtonLarge': (context, source) {
        return FloatingActionButton.large(
          onPressed: source.voidHandler(['onPressed']),
          tooltip: source.v<String>(['tooltip']),
          foregroundColor: ArgumentDecoders.color(source, ['foregroundColor']),
          backgroundColor: ArgumentDecoders.color(source, ['backgroundColor']),
          focusColor: ArgumentDecoders.color(source, ['focusColor']),
          hoverColor: ArgumentDecoders.color(source, ['hoverColor']),
          splashColor: ArgumentDecoders.color(source, ['splashColor']),
          heroTag: source.v<String>(['heroTag']),
          elevation: source.v<double>(['elevation']),
          focusElevation: source.v<double>(['focusElevation']),
          hoverElevation: source.v<double>(['hoverElevation']),
          highlightElevation: source.v<double>(['highlightElevation']),
          disabledElevation: source.v<double>(['disabledElevation']),
          shape: ArgumentDecoders.shapeBorder(source, ['shape']),
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          autofocus: source.v<bool>(['autofocus']) ?? false,
          mouseCursor:
              CustomArgumentDecoders.mouseCursor(source, ['mouseCursor']),
          materialTapTargetSize:
              ArgumentDecoders.enumValue<MaterialTapTargetSize>(
                  MaterialTapTargetSize.values,
                  source,
                  ['materialTapTargetSize']),
          enableFeedback: source.v<bool>(['enableFeedback']),
          child: source.child(['child']),
        );
      },
      'InteractiveViewer': (context, source) {
        return InteractiveViewer(
          clipBehavior: ArgumentDecoders.enumValue<Clip>(
                  Clip.values, source, ['clipBehavior']) ??
              Clip.none,
          alignPanAxis: source.v<bool>(['alignPanAxis']) ?? false,
          panAxis: ArgumentDecoders.enumValue<PanAxis>(
                  PanAxis.values, source, ['panAxis']) ??
              PanAxis.free,
          boundaryMargin:
              CustomArgumentDecoders.edgeInsets(source, ['boundaryMargin']) ??
                  EdgeInsets.zero,
          constrained: source.v<bool>(['constrained']) ?? true,
          maxScale: source.v<double>(['maxScale']) ?? 2.5,
          minScale: source.v<double>(['minScale']) ?? 0.8,
          interactionEndFrictionCoefficient:
              source.v<double>(['interactionEndFrictionCoefficient']) ??
                  0.0000135,
          panEnabled: source.v<bool>(['panEnabled']) ?? true,
          scaleEnabled: source.v<bool>(['scaleEnabled']) ?? true,
          scaleFactor: source.v<double>(['scaleFactor']) ?? 0.8,
          alignment:
              ArgumentDecoders.alignment(source, ['alignment']) as Alignment?,
          trackpadScrollCausesScale:
              source.v<bool>(['trackpadScrollCausesScale']) ?? false,
          child: source.child(['child']),
        );
      },
    };
```

In this example we are using the [Material](https://m3.material.io/) widgets but this could be the [fluent\_ui](https://pub.dev/packages/fluent_ui) or [macos\_ui](https://pub.dev/packages/macos_ui) package set of components or even your custom design system.

Now that we have defined the core of rfw we can start to add the logic and UI for our app.

> The rfw package includes material and core directly so you can simply import it directly and not need to define like this.

### Connecting to the server 

Create and update the following file located at `app/lib/main.dart`:

```
import 'package:flutter/material.dart';

import 'network.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter SSR Example',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const NetworkExample(),
    );
  }
}
```

Next create and update the following file located at `app/lib/network.dart`:

```
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'package:rfw/rfw.dart';

import 'rfw/material.dart' as m;
import 'rfw/core.dart' as c;

class NetworkExample extends StatefulWidget {
  const NetworkExample({super.key});

  @override
  State<NetworkExample> createState() => _NetworkExampleState();
}

class _NetworkExampleState extends State<NetworkExample> {
  final Runtime _runtime = Runtime();
  final DynamicContent _data = DynamicContent();
  bool loaded = false;
  int count = 0;
  final route = Uri.parse('http://localhost:8080/');

  @override
  void initState() {
    super.initState();
    _update();
  }

  @override
  void reassemble() {
    super.reassemble();
    _update();
  }

  static const coreName = LibraryName(['widgets']);
  static const materialName = LibraryName(['material']);
  static const remoteName = LibraryName(['remote']);

  void _update() async {
    _runtime.update(coreName, c.createCoreWidgets());
    _runtime.update(materialName, m.createMaterialWidgets());
    await fetchWidget();
    if (mounted) setState(() => loaded = true);
  }

  Future<void> fetchWidget() async {
    final res = await http.get(route, headers: {
      'COUNTER_VALUE': count.toString(),
    });
    if (res.statusCode == 200) {
      count = int.tryParse(res.headers['counter_value'].toString()) ?? count;
      _data.update('counter', <String, Object>{'value': '$count'});
      _runtime.update(remoteName, decodeLibraryBlob(res.bodyBytes));
    }
  }

  void onEvent(String name, DynamicMap arguments) async {
    debugPrint('user triggered event "$name" with data: $arguments');
    if (name == 'click') {
      final res = await http.post(route, headers: {
        'COUNTER_VALUE': count.toString(),
      });
      if (res.statusCode == 200) {
        count = int.tryParse(res.headers['counter_value'].toString()) ?? count;
        _data.update('counter', <String, Object>{'value': '$count'});
        _runtime.update(remoteName, decodeLibraryBlob(res.bodyBytes));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final colors = Theme.of(context).colorScheme;
    _data.update('colorScheme', <String, Object>{
      'inversePrimary': colors.inversePrimary.value,
      'inverseSurface': colors.inverseSurface.value,
      'onInverseSurface': colors.onInverseSurface.value,
      'primary': colors.primary.value,
      'onPrimary': colors.onPrimary.value,
      'primaryContainer': colors.primaryContainer.value,
      'onPrimaryContainer': colors.onPrimaryContainer.value,
      'secondary': colors.secondary.value,
      'onSecondary': colors.onSecondary.value,
      'secondaryContainer': colors.secondaryContainer.value,
      'onSecondaryContainer': colors.onSecondaryContainer.value,
      'tertiary': colors.tertiary.value,
      'onTertiary': colors.onTertiary.value,
      'tertiaryContainer': colors.tertiaryContainer.value,
      'onTertiaryContainer': colors.onTertiaryContainer.value,
      'error': colors.error.value,
      'onError': colors.onError.value,
      'errorContainer': colors.errorContainer.value,
      'onErrorContainer': colors.onErrorContainer.value,
      'background': colors.background.value,
      'onBackground': colors.onBackground.value,
      'surface': colors.surface.value,
      'onSurface': colors.onSurface.value,
      'outline': colors.outline.value,
      'outlineVariant': colors.outlineVariant.value,
      'scrim': colors.scrim.value,
      'shadow': colors.shadow.value,
    });
    if (!loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    const root = FullyQualifiedWidgetName(remoteName, 'root');
    return Container(
      color: Theme.of(context).scaffoldBackgroundColor,
      child: RemoteWidget(
        runtime: _runtime,
        data: _data,
        widget: root,
        onEvent: onEvent,
      ),
    );
  }
}
```

There is a lot going on here but simply we are connecting to our server and defining the local widgets we created and creating a local counter state that is used to send to the server and update per the response.

Because the `DynamicContent _data` can be updated every frame we are setting the local colors from the apps current theme int he build method:

```
_data.update('colorScheme', <String, Object>{
      'inversePrimary': colors.inversePrimary.value,
      'inverseSurface': colors.inverseSurface.value,
      'onInverseSurface': colors.onInverseSurface.value,
      'primary': colors.primary.value,
      'onPrimary': colors.onPrimary.value,
      'primaryContainer': colors.primaryContainer.value,
      'onPrimaryContainer': colors.onPrimaryContainer.value,
      'secondary': colors.secondary.value,
      'onSecondary': colors.onSecondary.value,
      'secondaryContainer': colors.secondaryContainer.value,
      'onSecondaryContainer': colors.onSecondaryContainer.value,
      'tertiary': colors.tertiary.value,
      'onTertiary': colors.onTertiary.value,
      'tertiaryContainer': colors.tertiaryContainer.value,
      'onTertiaryContainer': colors.onTertiaryContainer.value,
      'error': colors.error.value,
      'onError': colors.onError.value,
      'errorContainer': colors.errorContainer.value,
      'onErrorContainer': colors.onErrorContainer.value,
      'background': colors.background.value,
      'onBackground': colors.onBackground.value,
      'surface': colors.surface.value,
      'onSurface': colors.onSurface.value,
      'outline': colors.outline.value,
      'outlineVariant': colors.outlineVariant.value,
      'scrim': colors.scrim.value,
      'shadow': colors.shadow.value,
    });
```

When we first load the UI we want to make a `GET` request to get the latest from the server or fallback to the latest in cache (or even `rootBundle`):

```
Future<void> fetchWidget() async {
    final res = await http.get(route, headers: {
      'COUNTER_VALUE': count.toString(),
    });
    if (res.statusCode == 200) {
      count = int.tryParse(res.headers['counter_value'].toString()) ?? count;
      _data.update('counter', <String, Object>{'value': '$count'});
      _runtime.update(remoteName, decodeLibraryBlob(res.bodyBytes));
    }
  }
```

Setting and reading the headers will allow us to send state to the server and respond on updates.

We can also respond to events in the UI and trigger requests:

```
void onEvent(String name, DynamicMap arguments) async {
    debugPrint('user triggered event "$name" with data: $arguments');
    if (name == 'click') {
      final res = await http.post(route, headers: {
        'COUNTER_VALUE': count.toString(),
      });
      if (res.statusCode == 200) {
        count = int.tryParse(res.headers['counter_value'].toString()) ?? count;
        _data.update('counter', <String, Object>{'value': '$count'});
        _runtime.update(remoteName, decodeLibraryBlob(res.bodyBytes));
      }
    }
  }
```

Here we are using the response of the `POST` request to update the UI but we could also call the `fetchWidget` method again to get the latest and use the headers to update the data.

To run the application simply run using `flutter run` and make sure if you use MacOS desktop target to set the correct network permissions.

If all goes well you should see the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/66f9r3p1wf2d318/r_1_phzhlfqsnj.webp?thumb=)

This will trigger network requests for each button press and the UI will reflect the logic done on the server.

You could also call a database and update the UI based on the response.

## Conclusion 

There is a lot more we can do with this example but after doing a deep dive on the format I thought it would be useful for others to understand and see some examples.

The final code can be found [here](https://github.com/rodydavis/flutter_ssr).

If you have any questions reach out to me on [Twitter](https://twitter.com/rodydavis) or [Github](https://github.com/rodydavis)!