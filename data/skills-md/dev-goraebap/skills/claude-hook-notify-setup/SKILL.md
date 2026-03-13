---
name: claude-hook-notify-setup
description: >
  Claude Code hook에 OS 네이티브 토스트 알림을 연결하는 세팅 스킬.
  node-notifier 기반으로 Windows(SnoreToast), macOS(알림 센터), Linux(libnotify) 모두 지원.
  작업 완료·권한 요청·질문 등 세 가지 상황에서 토스트를 띄운다.
  트리거: "작업 완료 알림 설정", "claude 알림 받고 싶어", "hook 알림", "끝나면 알려줘", "토스트 알림 설정"
license: Apache-2.0
compatibility: Claude Code
metadata:
  author: dev-goraebap
  version: "1.2"
---

# claude-hook-notify-setup

Claude Code가 작업을 끝내거나 입력이 필요할 때 OS 네이티브 토스트를 띄운다.

## 동작 방식

| hook | 발화 시점 | 토스트 내용 |
|------|-----------|-------------|
| `Stop` | Claude 턴 종료 | 프로젝트명 / 마지막 응답 요약 (300자) |
| `PermissionRequest` | 도구 실행 권한 요청 시 | Bash 명령어 또는 AskUserQuestion 질문 텍스트 |
| `Notification` | Claude Code 시스템 알림 | 알림 메시지 |

> `AskUserQuestion`도 PermissionRequest로 발화하며, 질문 텍스트가 토스트에 바로 표시된다.

## 설치 절차

### 1. 스크립트 배포

```bash
mkdir -p ~/.claude/skills/claude-hook-notify-setup/scripts
mkdir -p ~/.claude/skills/claude-hook-notify-setup/assets
cp <skill-path>/scripts/notify.js ~/.claude/skills/claude-hook-notify-setup/scripts/
cp <skill-path>/scripts/package.json ~/.claude/skills/claude-hook-notify-setup/scripts/
cp <skill-path>/assets/toast_img.jpg ~/.claude/skills/claude-hook-notify-setup/assets/
cd ~/.claude/skills/claude-hook-notify-setup/scripts && npm install
```

### 2. ~/.claude/settings.json에 hooks 등록

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node /Users/<username>/.claude/skills/claude-hook-notify-setup/scripts/notify.js stop"
          }
        ]
      }
    ],
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node /Users/<username>/.claude/skills/claude-hook-notify-setup/scripts/notify.js notification"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "node /Users/<username>/.claude/skills/claude-hook-notify-setup/scripts/notify.js permission"
          }
        ]
      }
    ]
  }
}
```

> `<username>`을 실제 사용자명으로 교체. Windows는 `C:/Users/<username>/...` 형식 사용.

## 제거

```bash
rm -rf ~/.claude/skills/claude-hook-notify-setup
```

`~/.claude/settings.json`에서 hooks 블록도 함께 삭제.
