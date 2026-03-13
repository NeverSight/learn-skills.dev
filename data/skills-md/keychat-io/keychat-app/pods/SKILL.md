---
name: pods
description: Update and install CocoaPods dependencies for iOS and macOS
disable-model-invocation: true
allowed-tools: Bash(pod *), Bash(cd *)
---

Update and install CocoaPods dependencies for iOS and macOS builds.

## Command

Run the melos pods script:
```bash
melos run pod:install
```

This will:
1. Navigate to `packages/app/ios`
2. Run `pod update && pod install --repo-update`
3. Navigate to `packages/app/macos`
4. Run `pod update && pod install --repo-update`

## When to use

- After adding new native iOS/macOS dependencies
- When Podfile.lock is out of sync
- After upgrading Flutter or plugins
- When getting "pod not found" errors

## Troubleshooting

If pods fail to install:
1. Try cleaning first: `cd packages/app/ios && rm -rf Pods Podfile.lock`
2. Update CocoaPods: `gem install cocoapods`
3. Clear pod cache: `pod cache clean --all`
