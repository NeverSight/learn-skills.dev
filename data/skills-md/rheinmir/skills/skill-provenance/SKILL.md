---
name: skill-provenance
disable-model-invocation: true
description: Ghi và kiểm provenance (nguồn + sha256 checksum) cho skill — dùng khi 'cài skill từ ngoài', 'skill này từ đâu', 'audit nguồn skill', 'checksum skill', 'supply-chain skill', phát hiện skill bị sửa lén; bổ trợ orca-sec-scans. Chạy fdk/tools/skill-provenance.py. /skill-provenance
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: dev-loop
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [fdk/tools/skill-provenance.py]
---

# Skill: skill-provenance

Sổ nguồn gốc + toàn vẹn cho từng skill. `orca-sec-scans` quét vuln/secret trong NỘI DUNG;
skill này trả lời hai câu hỏi khác của chuỗi cung ứng (supply-chain): skill **từ đâu tới**
và **có bị sửa lén sau khi cài không**. Store là `fdk/skills.provenance.json` (nguồn +
ngày ghi + sha256 mọi file trong `skills/<name>/`). Verify bằng cách tính lại checksum và
so với sổ — lệch = MODIFIED, có skill trên đĩa mà chưa ghi sổ = UNTRACKED.

## WHAT

### Purpose và context
- **Purpose:** trả lời hai câu hỏi supply-chain cho từng skill — **từ đâu tới** và **có bị sửa lén sau khi cài không** — bằng sổ `fdk/skills.provenance.json` (nguồn + ngày ghi + sha256 mọi file) và lệnh verify tính lại checksum.
- **Trigger (when to use):**
  - Vừa **cài / chưng cất một skill từ nguồn ngoài** (marketplace, repo khác, distill trong phiên dự án khác) → `record` để chốt nguồn + checksum.
  - Nghi ngờ / muốn kiểm **skill có bị sửa ngoài luồng** không → `check`.
  - Hỏi "skill này **từ đâu** ra", "audit nguồn skill", "checksum skill", "supply-chain skill".
  - CI muốn chặn skill lạ hoặc skill bị sửa mà chưa cập nhật sổ.
- **Non-goals:** không quét vuln/secret trong nội dung skill (việc của `orca-sec-scans`); không tự đoán nguồn skill.

### Mental model
`skills/<name>/ (file trên đĩa) → sha256 mỗi file → so với sổ fdk/skills.provenance.json → OK | MODIFIED (lệch) | UNTRACKED (trên đĩa chưa ghi sổ) | MISSING (trong sổ, không còn trên đĩa)`. `record` = ghi/ghi đè mục sổ; `check` = đọc so.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | `<name>` hoặc `--all` | có với `record` | skill cần ghi sổ |
| In | `--source` | có với `record` | URL, `repo#ref` thật, hoặc `local-authored` |
| In | `--ci` | không | `check` trả exit 1 khi có MODIFIED/UNTRACKED |
| Out | mục sổ trong `fdk/skills.provenance.json` | sau `record` | nguồn + ngày ghi + sha256 |
| Out | trạng thái từng skill | sau `check` | OK / MODIFIED / UNTRACKED / MISSING + exit code |

### Rules và capabilities
- RULE-01 (MUST): **Không tự bịa nguồn.** `--source` phải là URL/ref thật hoặc `local-authored`; provenance sai còn tệ hơn không có.
- RULE-02 (MUST): **record sau MỌI lần cài/sửa hợp lệ** — sổ là nguồn chân lý; skill sửa mà không re-record sẽ bị CI chặn như sửa đổi lạ (đúng ý đồ).
- RULE-03 (MUST): **Không thay `orca-sec-scans`** — skill này lo provenance/toàn vẹn, không quét vuln/secret nội dung; dùng cả hai.
- RULE-04 (MUST): `check --ci` coi MISSING (skill đã gỡ) là không-phải-lỗi; chỉ MODIFIED/UNTRACKED mới chặn.
- RULE-05 (MUST): Store `fdk/skills.provenance.json` là file curated — commit cùng thay đổi skill, đừng để drift.
- Capabilities: đọc file skill + tính hash; ghi sổ provenance cục bộ. Không mạng.

### Failure boundaries
- Không biết nguồn thật của skill → **clarify** với user, không ghi `--source` đoán.
- `check --ci` thấy MODIFIED/UNTRACKED → **failed** (exit 1); sửa có chủ đích → re-record, sửa lạ → điều tra.
- MISSING → báo, không chặn.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | effect | sổ trống | Backfill một lần `record --all --source local-authored` | sổ đầy đủ | sổ đã có → skip |
| W02 | effect | skill mới + nguồn thật | `record <name> --source …` | mục sổ | nguồn không rõ → clarify |
| W03 | deterministic | sổ + đĩa | `check` (tất cả hoặc một skill) | OK/MODIFIED/UNTRACKED/MISSING | — |
| W04 | deterministic | sổ + đĩa | Gate CI `check --ci` | exit 0/1 | MODIFIED/UNTRACKED → exit 1 |
| W05 | effect | skill đã cố ý sửa | re-record với nguồn cũ | checksum mới | không re-record → W04 đỏ |

Chi tiết từng bước (nguồn chân lý cho W01–W05):

1. **Backfill một lần** (nếu sổ trống) — ghi mọi skill hiện có là tự viết:
   ```bash
   python3 fdk/tools/skill-provenance.py record --all --source local-authored
   ```
2. **Khi cài / thêm skill mới** — ghi nguồn thật (URL, `repo#ref`, hoặc `local-authored`):
   ```bash
   python3 fdk/tools/skill-provenance.py record <name> --source "https://github.com/<owner>/<repo>#<ref>"
   ```
3. **Kiểm toàn vẹn** bất cứ lúc nào (in OK / MODIFIED / UNTRACKED / MISSING):
   ```bash
   python3 fdk/tools/skill-provenance.py check          # xem tất cả
   python3 fdk/tools/skill-provenance.py check <name>   # một skill
   ```
4. **Gate CI** — exit 1 nếu có MODIFIED hoặc UNTRACKED (đã gắn trong `.github/workflows/skills-sync.yml`):
   ```bash
   python3 fdk/tools/skill-provenance.py check --ci
   ```
5. Sau khi **cố ý sửa** một skill, chạy lại `record <name> --source <nguồn cũ>` để cập nhật checksum — nếu không, `check --ci` sẽ báo MODIFIED (đúng: mọi thay đổi phải qua sổ).


### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | sổ trống | backfill W01 | sổ đã có → skip | W03 |
| B02 | recovery | `check` báo MODIFIED | sửa có chủ đích → W05 re-record; không rõ ai sửa → điều tra như sửa lạ | — | W03 |
| B03 | recovery | `check` báo UNTRACKED | skill mới hợp lệ → W02 record với nguồn thật | nguồn không rõ → clarify | W03 |

### Validation và stopping
Hoàn toàn tất định: checksum + exit code của `skill-provenance.py`. Phần cần người: nguồn `--source` có thật không. Dừng khi `check` in toàn OK (MISSING chấp nhận).

### Examples
- **Positive:** vừa kéo skill từ `https://github.com/acme/skills#v1.2` → `python3 fdk/tools/skill-provenance.py record foo --source "https://github.com/acme/skills#v1.2"` → `check foo` in OK.
- **Boundary/failure:** sửa `skills/foo/SKILL.md` mà không re-record → `check --ci` in MODIFIED foo, exit 1; user hỏi "foo từ đâu" nhưng không ai biết → không ghi `--source` đoán, hỏi lại.
