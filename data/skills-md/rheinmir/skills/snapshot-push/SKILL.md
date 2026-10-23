---
name: snapshot-push
disable-model-invocation: true
description: Push bonbon-ai outer repo as full snapshot, including be/ and fe/ content
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: snapshot-push

## WHAT

### Purpose và context
- **Purpose:** Push toàn bộ outer repo `bonbon-ai` lên GitLab như một snapshot — kể cả content của `be/` và `fe/` (các sub-repos có `.git` riêng). Dùng script `scripts/snapshot-push.sh` để tự động hide/restore `.git` dirs.
- **Trigger (when to use):** "push snapshot", "snapshot push", "đẩy snapshot", "push outer repo".
- **Non-goals:** không push riêng từng sub-repo `be/`/`fe/`, không áp dụng cho repo khác ngoài `bonbon-ai`.

### Mental model
`repo root bonbon-ai → snapshot-push.sh (hide .git của be/ fe/ → commit + push → restore .git) → commit hash + số files changed`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | message | không | commit message tuỳ chọn, truyền cho script |
| Out | kết quả push | có | commit hash + số files changed báo cho user |

### Rules và capabilities
- RULE-01 (MUST): Verify đang ở đúng repo root (`/Volumes/giatbhSSD(APFS)/workspace/bonbon-ai`) trước khi chạy script.
- Capabilities: đọc/ghi git của outer repo qua script có sẵn; ghi remote GitLab (push).

### Failure boundaries
- Không ở đúng repo root → **blocked**, không chạy script.
- Script lỗi (push fail) → **failed**, báo nguyên output lỗi cho user.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | deterministic | cwd | Verify repo root | đúng root | sai → blocked |
| W02 | effect | message | Chạy script snapshot-push | commit + push | lỗi → failed |
| W03 | deterministic | output script | Report commit hash + số files changed | báo cáo | — |

Chi tiết từng bước (nguồn chân lý cho W01–W03):

1. Verify đang ở đúng repo root (`/Volumes/giatbhSSD(APFS)/workspace/bonbon-ai`)
2. Chạy: `bash scripts/snapshot-push.sh "<optional message>"`
3. Report kết quả: commit hash + số files changed

### Branches
Không có nhánh phụ trong version này.

### Validation và stopping
Thành công = script trả rc 0 và in commit hash. Không retry tự động khi push lỗi.

### Examples
- **Positive:** "đẩy snapshot" tại `/Volumes/giatbhSSD(APFS)/workspace/bonbon-ai` → `bash scripts/snapshot-push.sh "snapshot"` → báo commit hash + số files changed, gồm cả file trong `be/` và `fe/`.
- **Boundary/failure:** gọi khi cwd là `be/` → W01 thấy không phải repo root → dừng, báo user chuyển về root, không chạy script.
