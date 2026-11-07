---
name: mdx-to-macos-dictionary
description: Convert local MDict .mdx dictionaries (optionally with companion CSS/JS/MDD files) into native macOS .dictionary bundles and install them in ~/Library/Dictionaries. Use when asked to convert, package, or install an MDX/MDict dictionary for the macOS Dictionary app.
---

# MDX to macOS Dictionary

Convert the supplied local `.mdx` source into a native, searchable macOS dictionary. Unless the user explicitly asks for an output-only conversion, install the completed `.dictionary` bundle in `~/Library/Dictionaries/` and create a DMG installer with a compatible `dmg.sh` tool. Do not create ZIP installers.

## External dependencies

- [dmg-maker](https://github.com/Jingyuan-Zheng/dmg-maker): required to create the final DMG installer. Clone it into `<work>/dmg-maker` when `DMG_MAKER_DIR` is not already set.
- [Dictionary Development Kit](https://github.com/SebastianSzturo/Dictionary-Development-Kit): required to compile the native `.dictionary` bundle.
- [`mdict-utils`](https://pypi.org/project/mdict-utils/): required to read and extract `.mdx` entries.

## Prerequisites

Run `scripts/check_requirements.sh` before processing a dictionary. It checks the required macOS tools and prints the exact missing-item remediation. Do not start conversion until it passes.

- Use macOS only. Require `git`, `python3`, `xmllint`, `xsltproc`, `plutil`, `sips`, `iconutil`, and `ditto`.
- If `xmllint` or `xsltproc` is unavailable, ask the user to install Xcode Command Line Tools with `xcode-select --install`, then rerun the check.
- If `mdict` is unavailable, create an isolated environment in `<work>/mdict-venv` with `python3 -m venv`, install `mdict-utils` there with pip after network approval, and invoke `<work>/mdict-venv/bin/mdict` for every MDX command. Do not depend on a global PATH installation.
- Require `create-dmg`. If Homebrew is already installed, install it with `brew install create-dmg` after approval. If Homebrew is unavailable, ask the user to install Homebrew or explicitly approve its installation; do not silently run an unreviewed installer.
- On Apple Silicon, the Dictionary Development Kit's build binaries require Rosetta. If the preflight check reports it missing, request approval to run `softwareupdate --install-rosetta --agree-to-license`, then rerun the check.

## Workflow

1. Inspect the source folder with `rg --files`; preserve companion CSS and use it as the dictionary stylesheet. Read MDX metadata and count keys with the preflight-selected `mdict` executable.
2. Extract records with `<mdict> -x -d <work/extracted> <source.mdx>`.
3. Run `scripts/mdx_records_to_apple_xml.py` on the extracted `.txt`. Validate with `xmllint --stream --noout`; report the entry count.
4. Ensure the open-source Dictionary Development Kit is available under `<work>/Dictionary-Development-Kit`. If absent, clone `https://github.com/SebastianSzturo/Dictionary-Development-Kit.git` after obtaining any needed network approval.
5. Start from the kit's `project_templates/MyInfo.plist`, set a unique reverse-DNS bundle identifier, the dictionary title, version, and source attribution. Remove the sample front-matter and preference keys.
6. Build with `bin/build_dict.sh -v 10.11`, setting `DICT_DEV_KIT_OBJ_DIR` inside the task's `work/` directory. Use the supplied CSS, or a small UTF-8 stylesheet if none exists.
7. Check the source directory for a supplied book-cover or logo image (`cover`, `book`, or `logo` in the filename; otherwise ask only if multiple plausible images exist). If one is found, run `scripts/set_dictionary_icon.py <bundle> <image>` before packaging; macOS image tools may require execution approval. Skip this step when no image is supplied.
8. Verify the bundle contains `Body.data`, `KeyText.index`, `EntryID.index`, `Info.plist`, and `DefaultStyle.css`. If `DMG_MAKER_DIR` is unset, clone [dmg-maker](https://github.com/Jingyuan-Zheng/dmg-maker) into `<work>/dmg-maker` (after obtaining any needed network approval) and set `DMG_MAKER_DIR` to that directory. Then run `"$DMG_MAKER_DIR/dmg.sh" <bundle> "$DMG_MAKER_DIR/Background.png"` from the desired `outputs/` directory. Validate that the resulting `.dmg` exists and contains the dictionary bundle. If `create-dmg` is unavailable, allow the script to install it only after required approval.
9. Copy the tested bundle to `~/Library/Dictionaries/<dictionary name>.dictionary` with `ditto --noextattr --norsrc`. Do not replace an existing same-name dictionary without user approval; use a versioned name instead and explain it.

## Content handling

- Keep the original entry markup where it is valid, but remove JavaScript and event-handler attributes: macOS Dictionary does not run them.
- Preserve HTML text and CSS. Ensure the generated XML is well-formed before building.
- Do not alter the original MDX, CSS, JS, or MDD files.
- If extraction or compilation fails, retain intermediate files in `work/` and report the exact failed stage.
