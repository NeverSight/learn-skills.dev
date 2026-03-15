---
name: managing-macos
description: |
  This skill should be used when the user asks about macOS/nix-darwin system settings,
  Dock/Finder configuration, Homebrew Cask management, Shottr setup, or Folder Actions.
  Triggers: "darwin-rebuild", Dock/Finder settings, "/etc/bashrc conflict",
  "/etc/zshrc conflict", "killall cfprefsd", "primary user does not exist",
  "shottr 설정", "shottr 단축키", "스크린샷 저장 경로", "shottr 라이센스",
  "Folder Actions", "폴더 감시", "compress-video", "compress-rar", "upload-immich".
  For iOS Shortcuts and Cherri DSL details use managing-shortcuts.
---

# macOS 관리 (nix-darwin)

nix-darwin 및 macOS 시스템 설정 가이드입니다.

## 빠른 참조

### Rebuild 명령어

```bash
# 설정 적용 (미리보기 + 적용)
nrs

# 오프라인 rebuild (캐시만 사용, 빠름)
nrs --offline

# NO_CHANGES 스킵 우회 (activation scripts 강제 재실행)
nrs --force

# 미리보기만
nrp
```

**nrs 안전 기능:**
- launchd 에이전트 정리 (setupLaunchAgents 멈춤 방지)
- Hammerspoon 재시작 (HOME 오염 방지)

> nrs/nrp 스크립트는 `~/.local/lib/rebuild-common.sh`를 source하여 공통 함수(로깅, 인수 파싱, worktree 감지, 빌드 미리보기, 아티팩트 정리)를 사용합니다.
> 소스: `modules/shared/scripts/rebuild-common.sh`, 플랫폼별: `modules/darwin/scripts/{nrs,nrp}.sh`

**Git Worktree 지원:**

git worktree에서 `nrs`/`nrp` 실행 시 자동 감지하여 worktree의 flake를 빌드합니다.

- 감지: `detect_worktree()` (rebuild-common.sh source 시 자동 실행)
- 메커니즘: `FLAKE_PATH`만 worktree 경로로 전환 (`--flake <worktree>`로 빌드)
- 심링크 타깃(`nixosConfigPath`)은 항상 메인 레포 — worktree 빌드 후에도 심링크가 안정적

### 주요 설정 파일

| 파일 | 용도 |
|------|------|
| `modules/darwin/configuration.nix` | macOS 시스템 설정 |
| `modules/darwin/home.nix` | Home Manager (macOS) |
| `modules/darwin/programs/` | macOS 전용 프로그램 |

### Nix CLI 패키지 (darwin-only)

`libraries/packages.nix`의 `darwinOnly` 리스트에서 관리:

```nix
# 패키지 추가
darwinOnly = [ ... pkgs.패키지명 ];
```

자세한 내용: [references/features.md](references/features.md#nix-cli-패키지-darwin-only)

### macOS 시스템 설정

| 설정 | 파일 | 설명 |
|------|------|------|
| Dock | `configuration.nix` | 자동 숨김, 크기, 최근 앱 |
| Finder | `configuration.nix` | 숨김 파일, 확장자, 네트워크 .DS_Store 방지 |
| 키보드 | `configuration.nix` | 키 반복 속도 |
| 트랙패드 | `configuration.nix` | 탭 클릭, 자연스러운 스크롤 |

### Homebrew 관리

`modules/darwin/programs/homebrew.nix`에서 선언적으로 관리됩니다 (personal 호스트만 적용).

```nix
# cleanup = "none" — 선언되지 않은 앱을 삭제하지 않음 (수동 설치 cask 보호)
# upgrade = true + greedyCasks = true — 자체 업데이터 앱의 버전 드리프트 방지
homebrew.casks = [
  "codex" "ghostty" "raycast" "rectangle"
  "hammerspoon" "homerow" "docker-desktop"
  "fork" "monitorcontrol"
];
homebrew.brews = [ "laishulu/homebrew/macism" "sox" ]; # Neovim 한영 전환, 오디오 처리
# shottr → Nix 패키지로 관리 (libraries/packages.nix darwinOnly)
# figma → Homebrew에서 제거 (자체 업데이터가 버전을 변경하여 adopt 시 버전 충돌)
# slack → Homebrew에서 제거 (수동 설치 선호, 자체 업데이터에 위임)
```

**새 Mac 세팅 시**: 직접 설치된 앱은 `brew install --cask --adopt <앱>`으로 Homebrew 관리로 전환 필요.

자세한 내용: [references/features.md](references/features.md#gui-앱-homebrew-casks)

### Shottr 선언 관리 (Nix + agenix)

Shottr 설정과 라이센스를 선언적으로 관리합니다.

| 파일 | 용도 |
|------|------|
| `modules/darwin/programs/shottr/default.nix` | Shottr 앱 고유 설정 + 라이센스 pre-fill |
| `modules/darwin/configuration.nix` | symbolic hotkeys (스크린샷 단축키) + activateSettings + Shottr 재시작 |
| `libraries/constants.nix` | Shottr 기본 저장경로 상대 경로 상수 |
| `secrets/shottr-license.age` | agenix 암호화 라이센스 키 (`KC_LICENSE` + `KC_VAULT`) |
| `modules/shared/programs/secrets/default.nix` | `~/.config/shottr/license` 배포 |

> **아키텍처 노트**: symbolic hotkeys와 Shottr 재시작은 `configuration.nix`의 postActivation에서 처리합니다.
> HM activation의 `activateSettings -u`가 `launchctl asuser + sudo` 컨텍스트에서 WindowServer와 통신하지 못하기 때문입니다.

운영 순서:

```bash
# 설정 적용 (라이센스 pre-fill 포함)
nrs
# 새 맥북: Shottr 실행 후 Activate 버튼 1회 클릭
```

#### Shottr 크레덴셜 관리 (상세)

**샌드박스 앱 구조**: Shottr는 macOS 샌드박스 앱이며 plist가 `~/Library/Containers/cc.ffitch.shottr/Data/Library/Preferences/cc.ffitch.shottr.plist`에 저장됩니다. `~/Library/Preferences/`에는 존재하지 않습니다. 다만 `defaults read/write cc.ffitch.shottr ...`는 `cfprefsd`를 통해 Container plist에 투명하게 접근하므로, 추가 경로 지정 없이 정상 동작합니다.

**라이센스 이중 저장 구조**:

| 저장소 | 키 | 용도 |
|--------|---|------|
| macOS Keychain | `Shottr-license`, `Shottr-vault` | Primary (서버 검증 후 기록) |
| defaults (plist) | `kc-license`, `kc-vault` | Secondary (UI pre-fill용) |

- Keychain 삭제 → defaults에서 라이센스를 UI에 pre-fill하되, "Activate" 버튼 1회 클릭 필요
- defaults 삭제 → Keychain에서 자동 복원 (라이센스 유지)
- 양쪽 모두 삭제 → 미등록 상태
- "Registered to:" 이메일은 **Keychain** (`Shottr-vault`)에서 읽힘 — defaults의 `kc-vault`와 무관
- `kc-vault`(defaults)의 정확한 역할은 불명 (Activate 시 서버 통신 데이터 캐시로 추정). 안전을 위해 둘 다 기록

**Nix 관리 전략**: `defaults write kc-license + kc-vault`로 라이센스를 pre-fill합니다. 완전 자동 활성화는 불가능하지만(Keychain은 Nix로 관리 불가), 새 맥북에서 **라이센스 키를 기억/입력할 필요 없이 Activate 버튼 1회 클릭만으로 활성화**할 수 있습니다.

**HM activation에서의 주의사항**:
- Home Manager activation 스크립트는 최소한의 PATH로 실행 → macOS 시스템 명령어는 절대 경로 필수 (`/usr/bin/defaults`, `/usr/bin/killall`)
- `defaults write`에서 `{...}` 패턴은 plist dictionary로 해석 시도 → JSON 형태 문자열은 반드시 `-string` 플래그 명시
- 예: `/usr/bin/defaults write cc.ffitch.shottr KeyboardShortcuts_area -string '{"carbonKeyCode":20,"carbonModifiers":768}'`

**defaults 테스트 시 SIGTERM vs SIGKILL**:
- `killall Shottr`(SIGTERM)로 종료하면 Shottr가 종료 시점에 메모리 캐시를 plist에 재기록
- defaults 조작 테스트 시에는 반드시 `kill -9 $(pgrep -x Shottr)` (SIGKILL) 사용 후 `defaults delete/write` 실행

> 테스트 환경: Shottr 1.9.1 (build 128, versionCode 10901), macOS Darwin 24.6.0, 2026-02-18

### Folder Actions (launchd WatchPaths)

`modules/darwin/programs/folder-actions/default.nix`에서 launchd WatchPaths 기반 폴더 감시 자동화를 관리합니다.

| 액션 | 감시 폴더 | 용도 |
|------|-----------|------|
| compress-rar | `~/FolderActions/compress-rar` | RAR 압축 |
| compress-video | `~/FolderActions/compress-video` | FFmpeg 비디오 압축 |
| rename-asset | `~/FolderActions/rename-asset` | 파일 이름 변경 |
| convert-video-to-gif | `~/FolderActions/convert-video-to-gif` | FFmpeg 비디오→GIF 변환 |
| upload-immich | Shottr 스크린샷 폴더 | Immich 자동 업로드 (personal 전용) |

로그: `~/Library/Logs/folder-actions/`

### iOS Shortcuts / Cherri DSL

iOS Shortcuts 빌드 파이프라인(Cherri DSL), prompt-render CLI, 모바일 프롬프트 워크플로우는 `managing-shortcuts` 스킬을 참조하세요.

관련 모듈: `modules/darwin/programs/shortcuts/`

## 자주 발생하는 문제

1. **sudo 권한 필요**: darwin-rebuild는 시스템 파일 수정에 sudo 필요
2. **/etc/bashrc 충돌**: 기존 설정 파일과 nix-darwin 충돌
3. **스크롤 방향 롤백**: cfprefsd 재시작 시 설정 초기화

## 레퍼런스

- 트러블슈팅: [references/troubleshooting.md](references/troubleshooting.md)
- 기능 목록: [references/features.md](references/features.md)
