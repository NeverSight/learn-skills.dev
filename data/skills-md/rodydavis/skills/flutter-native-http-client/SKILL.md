---
name: flutter-native-http-client
description: This blog post explores how to optimize HTTP client selection in Flutter applications based on the platform, using Cronet on Android and Cupertino's native client on iOS for improved performance and caching.
metadata:
  url: https://rodydavis.com/posts/snippets/flutter-native-http-client
  last_modified: Tue, 03 Feb 2026 20:04:29 GMT
---

# Flutter Native HTTP Client


```
import 'package:cronet_http/cronet_http.dart';
import 'package:cupertino_http/cupertino_http.dart';
import 'package:device_info_plus/device_info_plus.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:platform_info/platform_info.dart';

void main() async {
  var clientFactory = Client.new;
  final device = DeviceInfoPlugin();
  if (platform.isAndroid) {
    final engine = CronetEngine.build(
      cacheMode: CacheMode.memory,
      userAgent: (await device.androidInfo).model,
    );
    clientFactory = () => CronetClient.fromCronetEngine(engine);
  } else if (platform.isCupertino) {
    clientFactory = CupertinoClient.defaultSessionConfiguration.call;
  }
  runWithClient(() => runApp(const MyApp()),clientFactory);
}
```