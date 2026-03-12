---
name: using-fastlane-in-flutter-and-ci
description: Automate Flutter app builds and deployments to both the App Store and Google Play using Fastlane with this step-by-step guide.
metadata:
  url: https://rodydavis.com/posts/fastlane-and-flutter
  last_modified: Tue, 03 Feb 2026 20:04:17 GMT
---

# Using Fastlane in Flutter and CI


Prerequisites:

*   Understand what [Fastlane](https://fastlane.tools/) is and how it works
    
*   Project builds correctly following these [docs](https://flutter.dev/docs/deployment/cd)
    
*   Android app setup in [Google Play Console](https://developer.android.com/distribute/console)
    
*   iOS app setup in [AppStore Connect](https://appstoreconnect.apple.com/)
    
*   [Flutter is installed](https://flutter.dev/docs/get-started/install) and your project is created
    

### Steps

1.  Open your Flutter project
    
2.  Run: cd ios
    
3.  Run: fastlane init and follow the prompts
    
4.  Replace the Fastfile contents with this:
    

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

5.  Run: cd .. && cd android
    
6.  Run: fastlane init and follow the prompts
    
7.  Replace the Fastfile contents with this:
    

```
# Uncomment the line if you want fastlane to automatically update itself
# update_fastlane

default_platform(:android)

platform :android do
  desc "Prepare and archive app"
  lane :prepare  do |options|
    #bundle_install
    Dir.chdir "../.." do
      sh("flutter", "packages", "get")
      sh("flutter", "clean")
      sh("flutter", "build", "appbundle", "--release")
    end
  end
  
  desc "Push a new beta build to Google Play"
  lane :beta do
    prepare(release: false)
    upload_to_play_store(
      track: 'beta',
      aab: "../build/app/outputs/bundle/release/app.aab"
    )
    add_git_tag(
      grouping: "fastlane-builds",
      prefix: "v",
      build_number: android_get_version_code
    )
    push_to_git_remote
  end

  desc "Push a new release build to the Google Play"
  lane :release do
    prepare(release: true)
    upload_to_play_store(
      track: 'production',
      aab: "../build/app/outputs/bundle/release/app.aab"
    )
    add_git_tag(
      grouping: "release",
      prefix: "v",
      build_number: android_get_version_name
    )
    push_to_git_remote
  end
end
```

8.  Run: fastlane add\_plugin versioning\_android and enter your password if needed
    
9.  Run: cd ..
    

Now you are ready to launch your app to beta!

For ios run: cd ios && fastlane beta

For android run: cd android && fastlane beta

Stay tuned for an article soon where we use these fastlane sub folders for automating the releases on [Github Actions](https://github.com/features/actions) CI