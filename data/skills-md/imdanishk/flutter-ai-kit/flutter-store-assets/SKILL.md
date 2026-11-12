---
name: flutter-store-assets
description: Prepares the app icon, Android and iOS launcher icons and the store listing graphics (Google Play feature graphic, phone and tablet screenshots, App Store screenshots) at the sizes the stores require, and checks existing images against those rules. Use ONLY when the developer asks for an app icon or logo, launcher icons, store screenshots or listing graphics, or when a store upload rejects an image.
license: Apache-2.0
---

# Flutter store assets (on demand only)

Do not use this skill unless the request is about the icon, the logo or store listing images. The size tables are in `references/store-graphics-specs.md`; read it before producing or checking any file, because sizes change and each row carries its source and date.

## Steps

1. **Gather:** app name, niche, brand colours and type (from the project's theme or from `flutter-design`), platforms, languages for screenshots, devices to cover, whether an icon or logo already exists. If a logo or icon exists, use it as given and only fit it to the rules; design a new master only when none exists or the developer asks for one.
2. **Icon and launcher icons** (`references/icons.md`): when there is no icon to use, design one as an original vector master (SVG), keep it simple and readable at small sizes, then produce the platform files and configure `flutter_launcher_icons` if the project uses it. Ask before adding the package.
3. **Screenshots and graphics** (`references/screenshots.md`): capture real screens of the real app, add headlines or device frames if the developer wants them, and export at the required sizes per store and language. Screenshots must show the app in use.
4. **Check every file** against the specs table before handing it over: pixel size, format, no transparency where the store forbids it, file size, count. Print the dimensions you measured; do not report "correct" from memory.
5. **Hand over a list:** each file, its size, store, locale and where it goes (folder for upload with Fastlane `supply` or `deliver` through the `flutter-release` skill, or the console field for manual upload). Say what could not be checked.

## Rules

- Original artwork only. Never copy another app's icon, a known brand mark or a character. Apple's guidelines say you cannot use another developer's icon, brand or product name in your icon or name, and that you are responsible for the rights to everything in icons, screenshots and previews.
- Use fictional account data in screenshots, never real people's data.
- Do not upload to a store console; the developer does that, or a release lane does it on request.
- Do not install image tools or packages without asking. Say what is needed (an SVG exporter, ImageMagick, a design tool) and use what is already there. Without a raster tool, deliver the SVG master and the exact export commands for the developer, and say no exports were made. Without a runnable app, list the screens to capture and the sizes, and say no screenshots were made; never draw fake ones.
