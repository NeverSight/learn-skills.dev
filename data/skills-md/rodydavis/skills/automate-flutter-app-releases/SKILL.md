---
name: automate-flutter-app-releases
description: Automate your Flutter app releases to beta or production with this handy shell script that handles version bumping, formatting, cleaning, rebuilding, and deployment via Fastlane.
metadata:
  url: https://rodydavis.com/posts/automate-flutter-apps
  last_modified: Tue, 03 Feb 2026 20:04:27 GMT
---

# Automate Flutter App Releases


> **TLDR** You can find the script [here](https://gist.github.com/rodydavis/774b36e32d7efa882cca8dd16da6e74c).

```
#!/bin/bash

echo "App Release Automator by @rodydavis"

action="$1"
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

if [ ${action} = "build" ]; then

    echo "${green}Generating built files.. ${reset}"
    flutter packages pub run build_runner clean
    flutter packages pub run build_runner build --delete-conflicting-outputs

    pub global activate pubspec_version
    git commit -a -m "Build $(pubver bump patch)"
    
    echo "${green}Building Project...${reset}"
    find . -name "*-e" -type f -delete
    flutter format .
    flutter clean

    echo "${green}Project Size: $(find . -name "*.dart" | xargs cat | wc -c)${reset}"

    echo "${green}Building APK...${reset}"
    flutter build apk

    echo "${green}Builing IPA..${reset}"
    cd ./ios && pod install && pod repo update && cd ..
    flutter build ios

    git commit -a -m "Project Rebuilt"


elif [ ${action} = "beta" ]; then

    echo "${green}Generating built files..${reset}"
    flutter packages pub run build_runner clean
    flutter packages pub run build_runner build --delete-conflicting-outputs

    pub global activate pubspec_version
    git commit -a -m "Beta $(pubver bump patch)"
    
    echo "${green}Building Project...${reset}"
    find . -name "*-e" -type f -delete
    flutter format .
    flutter clean

    echo "${green}Project Size: $(find . -name "*.dart" | xargs cat | wc -c)${reset}"

    echo "${green}Building APK...${reset}"
    flutter build apk

    echo "${green}Sending Android to Beta...${reset}"
    cd ./android && fastlane beta && cd ..

    echo "${green}Builing IPA..${reset}"
    flutter build ios

    echo "${green}Sending iOS to Beta..${reset}"
    cd ./ios && fastlane beta && cd ..

    git commit -a -m "Sent to Beta"


elif [ ${action} = "release" ]; then

    echo "${green}Generating built files..${reset}"
    flutter packages pub run build_runner clean
    flutter packages pub run build_runner build --delete-conflicting-outputs

    pub global activate pubspec_version
    git commit -a -m "Production $(pubver bump minor)"

    echo "${green}Building Project...${reset}"
    find . -name "*-e" -type f -delete
    flutter format .
    flutter clean

    echo "${green}Project Size: $(find . -name "*.dart" | xargs cat | wc -c)${reset}"

    echo "${green}Building APK...${reset}"
    flutter build apk

    echo "${green}Sending Android to Production...${reset}"
    cd ./android && fastlane release && cd ..

    echo "${green}Builing IPA..${reset}"
    flutter build ios

    echo "${green}Sending iOS to Production...${reset}"
    cd ./ios && fastlane release && cd ..

    git commit -a -m "Sent to Production"

fi

echo "${green}Successfully completed${reset}"
```

Needed:

*   Fastlane setup in each directory
*   build\_runner as a dependency
*   Git Project in VCS

Steps to Run:

1.  Download this file and put it at the root level of your flutter project
2.  Open the terminal and navigate to your project location
3.  Enter this command: `chmod +x release.sh`

Usage

*   For beta: `./release.sh beta`
*   For production: `./release.sh release`

It will do the following:

*   Bump the version numbers if you are using the version in the `pubspec.yaml`
*   Release the apps with Fastlane
*   Format all Dart Files
*   Clean Project
*   Rebuild classes
*   Add commit message

Make your life easier and automate your builds to beta and production!

## What you need 

*   [Fastlane](https://fastlane.tools/) setup in each directory
*   [build\_runner](https://pub.dartlang.org/packages/build_runner) as a dependency
*   Git Project in VCS

## Initial Setup 

*   Download [this file](https://gist.github.com/rodydavis/774b36e32d7efa882cca8dd16da6e74c)
*   Put it at the root level of your flutter project
*   Open the terminal and navigate to your project location
*   Enter this command: chmod +x release.sh

## Usage 

Now you can call this script!

*   For beta: `./release.sh beta`
*   For production: `./release.sh release`

## Overview 

*   Bump the version numbers if you are using the version in the pubspec.yaml
*   Release the apps with Fastlane
*   Format all Dart Files
*   Clean Project
*   Rebuild classes
*   Add commit messages
*   Updates Cocoa Pods