---
name: deep-linking-for-flutter-web
description: Learn how to implement proper URL navigation in your Flutter application, including deep linking to specific pages, handling protected routes, and creating custom transitions for a seamless user experience.
metadata:
  url: https://rodydavis.com/posts/deep-linking-flutter-web
  last_modified: Tue, 03 Feb 2026 20:04:25 GMT
---

# Deep Linking for Flutter Web


In this article I will show you how to have proper URL navigation for your application. Open links to specific pages, protected routes and custom transitions.

> **TLDR** The final source [here](https://github.com/rodydavis/flutter_deep_linking) and an online [demo](https://rodydavis.github.io/flutter_deep_linking/).

## Setup 

Create a new flutter project called “flutter\_deep\_linking”

Open that folder up in VSCode.

Update your “pubspec.yaml” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/r43ga1tjg6p8x6i/deep_1_qbot26kikl.webp?thumb=)

## Step 1 

Create a file at “lib/ui/home/screen.dart” and add the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/7r1l1i535220rwy/deep_2_8o7bk1h6ep.webp?thumb=)

Update your “lib/main.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/h42392iez6y3m89/deep_3_u638b3ccuy.webp?thumb=)

Run your application and you should see the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/43sd7k55aq8yce8/deep_4_fk5zfnixom.webp?thumb=)

## Step 2 

Now we need to grab the url the user enters into the address bar.

Create a folder at this location “lib/plugins/navigator”

Create a file inside named: “web.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/430154j9r710g4v/deep_5_r37mgvwx5q.webp?thumb=)

Create a file inside named: “unsupported.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/dczy2vb19nv6oo8/deep_6_xogk4ly3ze.webp?thumb=)

Create a file inside named: “navigator.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/lv0141dn57c869h/deep_7_atfvh3z2tt.webp?thumb=)

Now go back to your “lib/main.dart” file and add the navigator:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/k75ny99q018o2y3/deep_8_4esmqtror6.webp?thumb=)

> It’s important to import the navigator as shown as this will have the conditional import for web compiling.

If you run the app now nothing should change.

## Step 3 

Now let’s add the proper routing.

Create a new file “lib/ui/router.dart” and add the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/0y1ro5lf7h279w9/deep_9_xae1ebw89x.webp?thumb=)

Also update “lib/main.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/p7821ykg5on9lla/deep_10_ijxwpy9f4h.webp?thumb=)

> Notice how we removed the “home” field for MaterialApp. This is because the router will handle everything. By default we will go home on “/”

## Step 4 

Now let’s add multiple screens to put this to the test! Add the following folders and files.

Create a file “lib/ui/account/screen.dart” and add the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/c081tn3331n994h/deep_11_o9tev9myvc.webp?thumb=)

Create a file “lib/ui/settings/screen.dart” and add the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/q117wlgum9kr8gn/deep_12_8gbj5hxdmq.webp?thumb=)

Create a file “lib/ui/about/screen.dart” and add the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/az34574641hrj62/deep_13_aojf2nh3fj.webp?thumb=)

Add the following to “lib/ui/router.dart”:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/8sa4176bo1f1c66/deep_14_9p3q4k5nqt.webp?thumb=)

Now when you navigate to /about, /account and /settings you will go to the new pages!

![](https://rodydavis.com/_/../api/files/pbc_2708086759/o0w52xqyj19cg2w/deep_15_lahb8r2wyw.webp?thumb=)

## Step 5 

Now let’s tie into the browser navigation buttons! Update “lib/ui/home/screen.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/eb89014ivx49f9c/deep_16_6ccpd3agpc.webp?thumb=)

Now when you run the application and click on the settings icon it will launch the new screen as expected. But if you click your browsers back button it will go back to the home screen!

![](https://rodydavis.com/_/../api/files/pbc_2708086759/192l3evo16e287e/deep_17_rovfeoa2t1.webp?thumb=)

![](https://rodydavis.com/_/../api/files/pbc_2708086759/4zzn742z7lsg454/deep_18_75rxz9598q.webp?thumb=)

## Step 6 

These urls are great but what if you want to pass data such as an ID that is not known ahead of time? No worries!

Update “lib/ui/account/screen.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/93f2yzeb7qkc089/deep_19_qyhv82wxfe.webp?thumb=)

Let’s update our “lib/ui/router.dart” with the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/ar68a9w9l596080/deep_20_i6mmwwv4bg.webp?thumb=)

Now when you run your application and navigate to “/account/40” you will see the following:

![](https://rodydavis.com/_/../api/files/pbc_2708086759/318co8rwm04s894/deep_21_ytsnzw349i.webp?thumb=)

## Conclusion 

Dynamic routes work great for Flutter web, you just need to know what to tweak! This package uses a forked version of fluro for some fixes I added but once the PRs is merged you can just use the regular package. Let me know what you think below and if there is a better way I am not seeing!

Here is the final code: [https://github.com/rodydavis/flutter\_deep\_linking](https://github.com/rodydavis/flutter_deep_linking)