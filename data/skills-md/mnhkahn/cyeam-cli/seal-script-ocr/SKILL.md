---
name: seal-script-ocr
metadata:
  version: "0.1.18"
description: Recognize Chinese seal-script characters in images using OCR. Use when asked to identify or transcribe seal-script glyphs, seal impressions, or inscription images. Read this skill for exact CLI syntax before running commands.
---

# Seal Script OCR

Upload a user-selected image to cyeam.com to recognize Chinese seal-script characters (篆字). For finding calligraphy glyphs or assembling text from copybook images, use the separate `calligraphy-composition` skill.

## Command

```bash
cyeam mo ocr image.png
```

Pass the local image path as the positional argument. The command reads the file, uploads its filename and contents to `https://www.cyeam.com/mo/api/ocr`, and writes the recognition response as JSON to stdout.

## Results and scope

- Report the recognized characters and any alternatives or confidence information actually returned by the service. Preserve uncertainty when a glyph is ambiguous.
- Image formats are not restricted by this workflow; PNG or JPG is recommended.
- Run OCR only for the image the user asks to recognize.
- No login or Microsoft authorization is required.

## Installation


Review the commands before installing. These examples pin **v1.1.4**, rather than latest, and download an executable archive.
Install only when the CLI is needed; do not reinstall for every command.

### macOS / Linux: verify and install in the user directory

Run in Bash or Zsh with `curl`, `tar`, `install`, and either `shasum` or `sha256sum`.
The script selects macOS / Linux on arm64 or x86_64 and stops on other platforms.

```bash
(
  set -eu
  version='v1.1.4'
  case "$(uname -s)/$(uname -m)" in
    Darwin/arm64)
      asset='cyeam_Darwin_arm64.tar.gz'
      sha256='06b5af004ab4f0f05d5829ea6bd18b97c4449c262af7df14c67175f7d3cb29db' ;;
    Darwin/x86_64)
      asset='cyeam_Darwin_x86_64.tar.gz'
      sha256='107342bb9d2fa444b96155c468e71b8cc63e0f5ad0acc784698afe221548efa6' ;;
    Linux/aarch64|Linux/arm64)
      asset='cyeam_Linux_arm64.tar.gz'
      sha256='ed87697f3948bead67b585e9881c3bef20e8d2d903beb5b125587281a5091c5b' ;;
    Linux/x86_64)
      asset='cyeam_Linux_x86_64.tar.gz'
      sha256='873d6805fab8ab56540bb034aaf2f57f12eb672fcabd322ebe401e8250a5966d' ;;
    *) echo 'Unsupported platform; see the pinned release.' >&2; exit 1 ;;
  esac
  workdir=$(mktemp -d)
  trap 'rm -rf "$workdir"' EXIT
  cd "$workdir"
  curl --fail --show-error --silent --location --proto '=https' --proto-redir '=https' \
    --output "$asset" "https://github.com/mnhkahn/cyeam-cli/releases/download/$version/$asset"
  printf '%s  %s\n' "$sha256" "$asset" > expected.sha256
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum -c expected.sha256
  else
    shasum -a 256 -c expected.sha256
  fi
  # set -e prevents extraction or installation if download or verification fails.
  tar -xzf "$asset" cyeam
  mkdir -p "$HOME/.local/bin"
  install -m 0755 cyeam "$HOME/.local/bin/cyeam"
  CYEAM_CLI_NO_UPDATE_NOTIFIER=1 "$HOME/.local/bin/cyeam" --no-analytics version
)
```

This writes only to a temporary directory and `~/.local/bin/cyeam` (replacing an existing binary).
No administrator privileges are needed; system directories, services, and shell configuration are unchanged. For the current shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

For persistent access, add that line to your shell configuration.
Check the [v1.1.4 release page](https://github.com/mnhkahn/cyeam-cli/releases/tag/v1.1.4) and
[checksums.txt](https://github.com/mnhkahn/cyeam-cli/releases/download/v1.1.4/checksums.txt)
for checksums. When changing the pinned version, verify and replace both the version and its SHA-256 values.
Checksums confirm release-file consistency; they are not an independent signature or security audit.

### External requests and local state

- **Installation:** Downloads the selected archive from a pinned GitHub release, which may redirect to GitHub's asset CDN. Verifies the pinned SHA-256 before extracting only `cyeam`. Installation verification disables analytics and update checks.
- **OCR:** `mo ocr <image>` reads the selected local file and uploads its filename and contents to `https://www.cyeam.com/mo/api/ocr` for recognition. Run only when the user requests recognition of that image; Microsoft login is not required.
- **Analytics:** By default, sends command names, CLI version, system information, and a random installation ID to `https://us.i.posthog.com`. The server may infer location from the outgoing IP. Command arguments, image contents, and credentials are not included. The ID is stored in `~/.cyeam/analytics-id`; disable with `--no-analytics` or `CYEAM_CLI_NO_ANALYTICS=1`.
- **Update notices:** Checks GitHub for the latest release at most once every 24 hours and caches state in `~/.cyeam/update-state.json`. Notices do not replace the executable. Set `CYEAM_CLI_NO_UPDATE_NOTIFIER=1` to disable. The explicit `cyeam update` command downloads and verifies the latest release, replaces the executable, and then attempts to sync skills through `npx skills add`. To remain on a pinned version, use the installation steps above instead.

To keep only the network requests required for this skill in the current shell:

```bash
export CYEAM_CLI_NO_ANALYTICS=1
export CYEAM_CLI_NO_UPDATE_NOTIFIER=1
```
