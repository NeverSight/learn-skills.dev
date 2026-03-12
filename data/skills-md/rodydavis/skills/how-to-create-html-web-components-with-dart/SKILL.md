---
name: how-to-create-html-web-components-with-dart
description: Discover the power of Web Components and how to build them with both JavaScript and Dart for reusable, framework-agnostic UI elements.
metadata:
  url: https://rodydavis.com/posts/dart-html-web-components
  last_modified: Tue, 03 Feb 2026 20:04:14 GMT
---

# How to create HTML Web Components with Dart


I am a long time [Web Components](https://developer.mozilla.org/en-US/docs/Web/API/Web_components) fan (since helping DevRel [lit.dev](https://lit.dev/) and [Material Web Components](https://github.com/material-components/material-web)) and have also loved writing [Dart](https://dart.dev/) in both [Flutter](https://flutter.dev/) applications and full stack apps.  
  
Despite being [used at so many companies](https://arewebcomponentsathingyet.com/), Web Components have faced a lot of pushback from JavaScript developers that use frameworks to target the web. ☹️  
  
What you may not realize is that the web has a way to create new HTML tags that can be used in **ANY** JS framework or place that returns HTML and you can progressively enchance applications. 🤩

Since they are custom HTML tags, if you swap implementations, you do not need to update where it is used and you can ship components a separate files [instead of one big bundle](https://world.hey.com/dhh/modern-web-apps-without-javascript-bundling-or-transpiling-a20f2755).  
  
Dart [used to support Web Components](https://github.com/dart-archive/web-components) at one point and was even used by a precursor to Lit in a product call [Polymer](https://github.com/polymer-dart).

## Creating a Web Component in Javascript

To create a web component in Javascript you just need to extend HTML element and provide callbacks for when the component is mounted.

```
class HelloWorld extends HTMLElement {
  static observedAttributes = ["name"];

  constructor() {
    super();
  }

  update() {
    this.innerHTML = `Hello: ${this.getAttribute('name')}`;
  }

  connectedCallback() {
    console.log("Custom element added to page.");
    this. update();
  }

  disconnectedCallback() {
    console.log("Custom element removed from page.");
  }

  adoptedCallback() {
    console.log("Custom element moved to new page.");
  }

  attributeChangedCallback(name, oldValue, newValue) {
    console.log(`Attribute ${name} has changed.`);
    if (name === 'name') {
      this. update();
    }
  }
}

customElements.define("hello-world", HelloWorld);
```

We can then use it in HTML like the following:

```
<html>
  <body>
    <hello-world name="Rody"></hello-world>
    <script src="./index.js"></script>
  </body>
</html>
```

This works really well, and we don't even need a build step to create them!

## Creating Web Components with Dart

To create them on the Dart side we need to use the [js\_interop package](https://dart.dev/interop/js-interop/usage) and the new [web package](https://pub.dev/packages/web).  
  
We need to create a factory on the dart side that can create these JS classes without actually being able to create a class in the normal way (since JS and Dart classes are different).  
  
There is a great API [`Reflect.construct()`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Reflect/construct) which allows us to take a normal function and invoke it class a class constructor. JavaScript did not always support native classes and was only added with [ES6](https://www.w3schools.com/js/js_es6.asp).

By using this built in API, we can create the classes with just pure Dart:

```
import 'dart:js_interop';
import 'dart:js_interop_unsafe';

import 'package:web/web.dart';

class WebComponent<T extends HTMLElement> {
  late T element;
  final String extendsType = 'HTMLElement';

  void connectedCallback() {}

  void disconnectedCallback() {}

  void adoptedCallback() {}

  void attributeChangedCallback(
    String name,
    String? oldValue,
    String? newValue,
  ) {}

  Iterable<String> get observedAttributes => [];

  bool get formAssociated => false;

  ElementInternals? get internals => element['_internals'] as ElementInternals?;
  set internals(ElementInternals? value) {
    element['_internals'] = value;
  }

  R getRoot<R extends JSObject>() {
    final hasShadow = element.shadowRoot != null;
    return (hasShadow ? element.shadowRoot! : element) as R;
  }

  static void define(String tag, WebComponent Function() create) {
    final obj = _factory(create);
    window.customElements.define(tag, obj);
  }
}

@JS('Reflect.construct')
external JSAny _reflectConstruct(
  JSObject target,
  JSAny args,
  JSFunction constructor,
);

final _instances = <HTMLElement, WebComponent>{};

JSFunction _factory(WebComponent Function() create) {
  final base = create();
  final elemProto = globalContext[base.extendsType] as JSObject;
  late JSAny obj;

  JSAny constructor() {
    final args = <String>[].jsify()!;
    final self = _reflectConstruct(elemProto, args, obj as JSFunction);
    final el = self as HTMLElement;
    _instances.putIfAbsent(el, () => create()..element = el);
    return self;
  }

  obj = constructor.toJS;
  obj = obj as JSObject;

  final observedAttributes = base.observedAttributes;
  final formAssociated = base.formAssociated;

  obj['prototype'] = elemProto['prototype'];
  obj['observedAttributes'] = observedAttributes.toList().jsify()!;
  obj['formAssociated'] = formAssociated.jsify()!;

  final prototype = obj['prototype'] as JSObject;
  prototype['connectedCallback'] = (HTMLElement instance) {
    _instances[instance]?.connectedCallback();
  }.toJSCaptureThis;
  prototype['disconnectedCallback'] = (HTMLElement instance) {
    _instances[instance]?.disconnectedCallback();
    _instances.remove(instance);
  }.toJSCaptureThis;
  prototype['adoptedCallback'] = (HTMLElement instance) {
    _instances[instance]?.adoptedCallback();
  }.toJSCaptureThis;
  prototype['attributeChangedCallback'] = (
    HTMLElement instance,
    String name,
    String? oldName,
    String? newName,
  ) {
    _instances[instance]?.attributeChangedCallback(name, oldName, newName);
  }.toJSCaptureThis;

  return obj as JSFunction;
}
```

This may seem like a lot to digest, but that is ok. It simply does some JS magic to upgrade functions to classes and provide the correct callbacks to create the web components.

> If you want a package that does this for you, [html\_web\_components](https://pub.dev/packages/html_web_components) is on pub.dev.

To create a Web Component like we did before, we can just extend the class and define the component.

```
import 'package:html_web_components/html_web_components.dart';

class HelloWorld extends WebComponent {
  @override
  List<String> observedAttributes = ['name'];

  void update() {
    element.innerText = "Hello: ${element.getAttribute('name')}!";
  }

  @override
  void connectedCallback() {
    super.connectedCallback();
    update();
  }

  @override
  void attributeChangedCallback(
    String name,
    String? oldValue,
    String? newValue,
  ) {
    super.attributeChangedCallback(name, oldValue, newValue);
    if (observedAttributes.contains(name)) {
      update();
    }
  }
}

void main() {
  WebComponent.define('hello-world', HelloWorld.new);
}
```

This should look very similar (that is the goal) and makes it so easy to publish the compoents or build a full web application with it.

## Conclusion

Web Components allow you to upgrade your client side interactivity while having the freedom to use server rendering to create the template files or just use a SPA on the frontend. You can take these components and use them in **ANY** JS frameworks! 🤯  
  
I would highly suggest that you try it out for yourself before you write off Web Components. This is especially true for Flutter developers wanting an alternative to Flutter web (and even use with [Jaspr](https://pub.dev/packages/jaspr)).

You can take advantage of Dart's great ecosystem of packages on [pub.dev](https://pub.dev/) and the ability to compile to WASM and JS. If you use a builder like [peanut](https://pub.dev/packages/peanut) it will even create the script that tries to load WASM and can fallback to JS for you 🔥  
  
If you want to see the code, you can [find it on GitHub](https://github.com/rodydavis/dart-web-components). Reach out if you have any questions or want to show off something cool you built with them!