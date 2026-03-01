---
name: distributing-tauri-for-ios
description: Guides users through distributing Tauri applications to the iOS App Store, including Apple Developer enrollment, Xcode configuration, provisioning profiles, code signing, TestFlight beta testing, and App Store submission processes.
---

# Distributing Tauri Apps for iOS

This skill covers the complete process of distributing Tauri v2 applications to Apple's iOS App Store.

## Prerequisites

Before distributing a Tauri iOS app, ensure:

1. macOS development machine (required for iOS builds)
2. Xcode installed with iOS SDK
3. Apple Developer Program enrollment ($99/year)
4. Tauri project initialized for iOS (`tauri ios init`)

## Apple Developer Program Enrollment

Enroll at [developer.apple.com/programs](https://developer.apple.com/programs):

1. Sign in with Apple ID
2. Accept the Apple Developer Agreement
3. Complete enrollment (individual or organization)
4. Wait for approval (typically 24-48 hours)

## Bundle Identifier Configuration

The bundle identifier must be unique and match across all configurations.

### tauri.conf.json

```json
{
  "identifier": "com.yourcompany.yourapp",
  "version": "1.0.0",
  "bundle": {
    "iOS": {
      "bundleVersion": "1"
    }
  }
}
```

**Configuration notes:**

- `identifier`: Reverse-domain format, must match App Store Connect
- `version`: Becomes `CFBundleShortVersionString` (user-visible version)
- `bundleVersion`: Becomes `CFBundleVersion` (build number, must increment for each upload)

### Register Bundle ID in App Store Connect

1. Go to [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/identifiers/list)
2. Click "+" to register a new identifier
3. Select "App IDs" then "App"
4. Enter description and explicit Bundle ID matching `tauri.conf.json`
5. Select required capabilities
6. Click "Register"

## Code Signing Setup

### Create Certificates

**Distribution Certificate (required for App Store):**

1. Open Keychain Access on macOS
2. Keychain Access > Certificate Assistant > Request a Certificate from a Certificate Authority
3. Enter email, select "Saved to disk"
4. Go to [Certificates](https://developer.apple.com/account/resources/certificates/list)
5. Click "+" and select "Apple Distribution"
6. Upload the certificate signing request
7. Download and double-click to install

### Create Provisioning Profile

**App Store Distribution Profile:**

1. Go to [Profiles](https://developer.apple.com/account/resources/profiles/list)
2. Click "+" to create new profile
3. Select "App Store Connect" under Distribution
4. Select your App ID
5. Select your distribution certificate
6. Name and generate the profile
7. Download the `.mobileprovision` file

### Install Provisioning Profile

```bash
# Copy to Xcode provisioning profiles directory
cp ~/Downloads/YourApp_AppStore.mobileprovision \
   ~/Library/MobileDevice/Provisioning\ Profiles/
```

Or double-click the file to install automatically.

## Xcode Project Configuration

Open the Tauri iOS project in Xcode:

```bash
tauri ios build --open
```

### Configure Signing in Xcode

1. Select the project in the navigator
2. Select your app target
3. Go to "Signing & Capabilities" tab
4. Uncheck "Automatically manage signing" for manual control
5. Select your Team
6. Select the App Store provisioning profile

### Required Capabilities

Add capabilities based on app requirements:

| Capability | When Required |
|------------|---------------|
| Push Notifications | If using APNs |
| Background Modes | For background tasks |
| App Groups | For sharing data between extensions |
| Associated Domains | For universal links |

### Info.plist Configuration

Located at `src-tauri/gen/apple/[AppName]_iOS/Info.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDisplayName</key>
    <string>Your App Name</string>
    <key>CFBundleName</key>
    <string>YourApp</string>
    <key>CFBundleIdentifier</key>
    <string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>
    <key>CFBundleVersion</key>
    <string>$(CURRENT_PROJECT_VERSION)</string>
    <key>CFBundleShortVersionString</key>
    <string>$(MARKETING_VERSION)</string>
    <key>UILaunchStoryboardName</key>
    <string>LaunchScreen</string>
    <key>UISupportedInterfaceOrientations</key>
    <array>
        <string>UIInterfaceOrientationPortrait</string>
        <string>UIInterfaceOrientationLandscapeLeft</string>
        <string>UIInterfaceOrientationLandscapeRight</string>
    </array>
    <key>NSCameraUsageDescription</key>
    <string>This app requires camera access for...</string>
    <key>NSPhotoLibraryUsageDescription</key>
    <string>This app requires photo library access for...</string>
</dict>
</plist>
```

**Required usage descriptions** (add only if your app uses these features):

- `NSCameraUsageDescription`: Camera access
- `NSPhotoLibraryUsageDescription`: Photo library
- `NSLocationWhenInUseUsageDescription`: Location services
- `NSMicrophoneUsageDescription`: Microphone access

## App Icons

Generate iOS app icons from a source image (1024x1024 recommended):

```bash
tauri icon /path/to/app-icon.png --ios-color '#ffffff'
```

This generates all required icon sizes in `src-tauri/gen/apple/Assets.xcassets/AppIcon.appiconset/`.

## Building for App Store

### Command Line Build

```bash
# Build IPA for App Store Connect
tauri ios build --export-method app-store-connect
```

The IPA is generated at:
```
src-tauri/gen/apple/build/arm64/[AppName].ipa
```

### Build Options

```bash
# Build with specific target
tauri ios build --target aarch64-apple-ios --export-method app-store-connect

# Build in release mode (default for export-method)
tauri ios build --release --export-method app-store-connect

# Build and open in Xcode for manual archive
tauri ios build --open
```

### Archive via Xcode (Alternative)

1. Open project: `tauri ios build --open`
2. Select "Any iOS Device" as destination
3. Product > Archive
4. Window > Organizer to view archives
5. Click "Distribute App"
6. Select "App Store Connect"
7. Follow the wizard

## App Store Connect API Key Setup

Create an API key for automated uploads:

1. Go to [App Store Connect > Users and Access](https://appstoreconnect.apple.com/access/users)
2. Select "Integrations" tab
3. Click "App Store Connect API" then "+"
4. Name the key and select "Admin" or "Developer" role
5. Click "Generate"
6. Download the `.p8` file (only available once)
7. Note the Key ID and Issuer ID

### Store the API Key

```bash
# Create directory
mkdir -p ~/.appstoreconnect/private_keys

# Move the key file (rename to include Key ID)
mv ~/Downloads/AuthKey_XXXXXXXXXX.p8 ~/.appstoreconnect/private_keys/

# Alternative location
mkdir -p ~/private_keys
mv ~/Downloads/AuthKey_XXXXXXXXXX.p8 ~/private_keys/
```

### Environment Variables (Optional)

```bash
export APPLE_API_KEY_ID="XXXXXXXXXX"
export APPLE_API_ISSUER="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

## Uploading to App Store Connect

### Using altool

```bash
xcrun altool --upload-app \
  --type ios \
  --file "src-tauri/gen/apple/build/arm64/YourApp.ipa" \
  --apiKey "$APPLE_API_KEY_ID" \
  --apiIssuer "$APPLE_API_ISSUER"
```

### Using Transporter App

1. Download Transporter from Mac App Store
2. Sign in with Apple ID
3. Drag and drop the IPA file
4. Click "Deliver"

### Using Xcode Organizer

1. Window > Organizer
2. Select your archive
3. Click "Distribute App"
4. Select "App Store Connect"
5. Choose "Upload" or "Export"
6. Follow prompts

## TestFlight Beta Testing

After upload processing (typically 15-30 minutes):

### Internal Testing

1. App Store Connect > Your App > TestFlight
2. Add internal testers (up to 100, must be App Store Connect users)
3. Testers receive email invitation

### External Testing

1. Create a test group
2. Add build to the group
3. Submit for Beta App Review (required for external testers)
4. Add external testers (up to 10,000)
5. Testers install via TestFlight app

## App Store Submission

### Create App in App Store Connect

1. Go to [App Store Connect](https://appstoreconnect.apple.com)
2. My Apps > "+" > New App
3. Select iOS platform
4. Enter app name, primary language, bundle ID, SKU
5. Click "Create"

### Prepare App Store Listing

Required assets:

| Asset | Specification |
|-------|---------------|
| Screenshots | 6.7" (1290x2796), 6.5" (1284x2778), 5.5" (1242x2208) |
| App Icon | 1024x1024 PNG (no alpha) |
| Description | Up to 4000 characters |
| Keywords | Up to 100 characters |
| Support URL | Required |
| Privacy Policy URL | Required |

### App Privacy

Complete the App Privacy questionnaire:

1. App Store Connect > Your App > App Privacy
2. Answer questions about data collection
3. Specify data types collected
4. Indicate data usage purposes

### Submit for Review

1. Select your build in App Store Connect
2. Complete all required metadata
3. Answer export compliance questions
4. Click "Submit for Review"

Review typically takes 24-48 hours.

## Common Issues and Solutions

### Code Signing Errors

**"No signing certificate found"**
```bash
# List available certificates
security find-identity -v -p codesigning

# Verify certificate is valid
security find-certificate -c "Apple Distribution" -p
```

**"Provisioning profile doesn't match"**
- Ensure bundle ID matches exactly in all locations
- Regenerate provisioning profile if certificates changed

### Build Failures

**"Unsupported architecture"**
```bash
# Ensure building for correct target
tauri ios build --target aarch64-apple-ios --export-method app-store-connect
```

**"Missing entitlements"**
- Check capabilities in Xcode match App ID capabilities
- Regenerate provisioning profile after capability changes

### Upload Errors

**"Invalid binary"**
- Ensure minimum iOS version is set correctly
- Verify all required icons are present
- Check Info.plist has required keys

**"Missing compliance"**
Add to Info.plist if not using encryption:
```xml
<key>ITSAppUsesNonExemptEncryption</key>
<false/>
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: iOS Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Rust
        uses: dtolnay/rust-action@stable
        with:
          targets: aarch64-apple-ios

      - name: Install dependencies
        run: npm ci

      - name: Install certificate
        env:
          CERTIFICATE_BASE64: ${{ secrets.APPLE_CERTIFICATE_BASE64 }}
          CERTIFICATE_PASSWORD: ${{ secrets.APPLE_CERTIFICATE_PASSWORD }}
        run: |
          CERTIFICATE_PATH=$RUNNER_TEMP/certificate.p12
          KEYCHAIN_PATH=$RUNNER_TEMP/app-signing.keychain-db

          echo -n "$CERTIFICATE_BASE64" | base64 --decode > $CERTIFICATE_PATH

          security create-keychain -p "" $KEYCHAIN_PATH
          security set-keychain-settings -lut 21600 $KEYCHAIN_PATH
          security unlock-keychain -p "" $KEYCHAIN_PATH

          security import $CERTIFICATE_PATH -P "$CERTIFICATE_PASSWORD" \
            -A -t cert -f pkcs12 -k $KEYCHAIN_PATH

          security list-keychain -d user -s $KEYCHAIN_PATH

      - name: Install provisioning profile
        env:
          PROVISIONING_PROFILE_BASE64: ${{ secrets.PROVISIONING_PROFILE_BASE64 }}
        run: |
          PP_PATH=$RUNNER_TEMP/profile.mobileprovision
          echo -n "$PROVISIONING_PROFILE_BASE64" | base64 --decode > $PP_PATH
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          cp $PP_PATH ~/Library/MobileDevice/Provisioning\ Profiles/

      - name: Build iOS
        run: npm run tauri ios build -- --export-method app-store-connect

      - name: Upload to App Store Connect
        env:
          APPLE_API_KEY_ID: ${{ secrets.APPLE_API_KEY_ID }}
          APPLE_API_ISSUER: ${{ secrets.APPLE_API_ISSUER }}
          APPLE_API_KEY: ${{ secrets.APPLE_API_KEY }}
        run: |
          mkdir -p ~/.appstoreconnect/private_keys
          echo "$APPLE_API_KEY" > ~/.appstoreconnect/private_keys/AuthKey_$APPLE_API_KEY_ID.p8

          xcrun altool --upload-app --type ios \
            --file src-tauri/gen/apple/build/arm64/*.ipa \
            --apiKey $APPLE_API_KEY_ID \
            --apiIssuer $APPLE_API_ISSUER
```

## Version Management

### Incrementing Versions

For each App Store submission, increment appropriately:

```json
{
  "version": "1.0.0",
  "bundle": {
    "iOS": {
      "bundleVersion": "1"
    }
  }
}
```

- `version`: Increment for user-visible changes (1.0.0 -> 1.0.1 or 1.1.0)
- `bundleVersion`: Must increment for every upload (1 -> 2 -> 3)

### Version Script Example

```bash
#!/bin/bash
# increment-build.sh
CONFIG="src-tauri/tauri.conf.json"
CURRENT=$(jq -r '.bundle.iOS.bundleVersion' $CONFIG)
NEW=$((CURRENT + 1))
jq ".bundle.iOS.bundleVersion = \"$NEW\"" $CONFIG > tmp.json && mv tmp.json $CONFIG
echo "Bundle version incremented to $NEW"
```

## Reference Links

- [Apple Developer Program](https://developer.apple.com/programs/)
- [App Store Connect](https://appstoreconnect.apple.com)
- [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Tauri iOS Documentation](https://v2.tauri.app/develop/ios/)
- [Tauri Distribution Guide](https://v2.tauri.app/distribute/app-store)
