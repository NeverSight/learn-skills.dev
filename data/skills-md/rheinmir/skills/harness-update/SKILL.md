---
name: harness-update
disable-model-invocation: true
description: >-
  TỰ BẢO TRÌ framework overstack trên máy user (self-maintain) — migrate llmwiki cũ lên harness
  (case B) hoặc update bản mới (case C). MỘT lệnh `install-harness.sh --self-heal` tự cài + tự
  backfill nợ wiki (Origin/index/OKF) + refresh bản đồ năng lực + health-check trong 1 process,
  không vòng lặp re-run. Trigger: "tự bảo trì framework", "self-maintain", "migrate harness",
  "update harness", "update overstack", "nâng cấp harness", "cài harness vào dự án cũ",
  "/harness-update".
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
  requires:
    harness: ">=1.3.127"
    bin: [curl, python3]
    scripts: [fdk/tools/build-capabilities.py]
    framework_scripts: [harness/scripts/install-harness.sh]
---

# Skill: harness-update

## WHAT

### Purpose và context
- **Purpose:** Một lệnh gọi là xong cho dự án CŨ: cài/update harness stack (L0–L4) và tự động trả nợ wiki legacy thay user.
- **Trigger (when to use):** "tự bảo trì framework", "self-maintain", "migrate harness", "update harness", "update overstack", "nâng cấp harness", "cài harness vào dự án cũ", "/harness-update" — dự án có llmwiki cũ cần migrate (case B) hoặc đã có harness cần update (case C).
- **Non-goals:** KHÔNG dùng cho project chưa có gì + cần populate wiki từ code — đó là `/new-project-setup` (case A). Không chữa lỗi hạ tầng (network, python3, validator hỏng).

**< 30s:** dùng cờ `--self-heal` — installer tự backfill nợ (Origin + index + OKF) ngay trong process rồi re-audit 1 lần. Agent chỉ gọi 1 lệnh, đọc 1 kết quả, báo cáo. KHÔNG còn vòng lặp re-run phía agent (đó là cái làm chậm bản cũ — xem [[230626-harness-update-sub30s]]).

### Mental model
`installer --self-heal (1 process: cài L0–L4 → audit → backfill → re-audit → activate + smoke) → rc (0 sạch · 3 nợ còn lại · khác = hạ tầng) → nghiệm thu + refresh CAPABILITIES + log → báo cáo 4 ý`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | dự án đích (thư mục hiện tại) | có | có llmwiki cũ (case B) hoặc harness cũ (case C) |
| In | `harness/scripts/install-harness.sh` | không | thiếu thì clone template `rheinmir/setup` nhánh `orca` |
| Out | harness L0–L4 đã cài + nợ wiki đã backfill | có | rc=0 là sạch |
| Out | `CAPABILITIES.md` sinh lại | khi có build-capabilities | bản cũ không có → bỏ qua |
| Out | dòng log `llmwiki/wiki/log.md` + báo cáo 4 ý | có | số backfill lấy từ dòng `[audit] backfill xong` |

### Rules và capabilities
- RULE-01 (MUST): Backfill là THÊM, không bao giờ sửa/xóa nội dung wiki có sẵn (self-heal trong installer giữ đúng quy tắc này).
- RULE-02 (MUST): Không đụng `raw/` dưới mọi hình thức.
- RULE-03 (MUST): rc=3 (nợ còn lại) cần user/skill xử 1 lần; rc khác (hạ tầng) là việc của user — phân biệt rõ, không cố chữa lỗi hạ tầng.
- RULE-04 (MUST): Không cờ `--self-heal` → installer chạy y hệt hành vi cũ (audit rồi exit 3 nếu nợ) — backward-compatible.
- RULE-05 (MUST): Case A (chưa có llmwiki, cần đọc code populate wiki) → chuyển hướng sang `/new-project-setup`.
- Capabilities: chạy installer cục bộ (có thể clone template qua mạng); ghi harness + wiki (chỉ thêm) + log; không ghi `raw/`.

### Failure boundaries
- `rc=3` → **partial**: danh sách nợ nằm trong output, sửa thủ công 1 lần rồi chạy lại W01.
- `rc` khác (1/4) → **blocked** (hạ tầng): DỪNG, báo user nguyên văn, không tự đoán.
- Dự án chưa có llmwiki (case A) → **cancelled** ở skill này, chuyển `/new-project-setup`.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | effect | dự án đích | Chạy installer 1 lần với `--self-heal` (thiếu nguồn thì clone template) | output + rc | — |
| W02 | deterministic | rc | Đọc exit code, KHÔNG vòng lặp re-run | rc=0 → W03 | rc=3 → B01; rc khác → blocked |
| W03 | effect | output W01 | Nghiệm thu ⛔×3 + refresh CAPABILITIES + health-check tuỳ chọn + log | log + CAPABILITIES | không có build-capabilities → bỏ qua |
| W04 | deterministic | kết quả | Báo cáo user đủ 4 ý | báo cáo | — |

Chi tiết từng bước (nguồn chân lý cho W01–W04):

**1. Chọn đường theo LAYOUT rồi chạy installer đúng 1 lần:**

- **Dự án downstream layout dot** (có `.llmwiki/.harness-stamp` — mọi máy cài từ v4): engine sống ở GLOBAL, nên cập nhật = chạy lại bootstrap. Nó refresh `~/.claude/harness` khi version lệch, kéo/cập nhật engine **orca-graph** cùng chuyến với shim, đóng lại stamp, và KHÔNG chép engine vào dự án:
```bash
curl -fsSL https://raw.githubusercontent.com/Rheinmir/setup/orca/harness/poc-vendor-neutral/bootstrap.sh | bash
```
  Gọi nhầm `install-harness.sh . --self-heal` ở layout này → script tự DỪNG rc 5 và in đúng lệnh trên (đo 20/09/2026: đường cũ không cập nhật global mà còn chép 77 script vào dự án). Agent chạy trong terminal có pty: thêm `-s -- --with-graph` để khỏi chờ checklist 60 giây.
- **Chỉ cập nhật bộ skill** (từ 141026 skill ở repo riêng [Rheinmir/skills](https://github.com/Rheinmir/skills), cài global `~/.claude/skills`): không đụng harness/llmwiki, ~45 s:
```bash
curl -fsSL https://raw.githubusercontent.com/Rheinmir/setup/orca/harness/poc-vendor-neutral/bootstrap.sh | bash -s -- --skills-only
# tương đương: npx -y skills add rheinmir/skills#main --global --all ; rồi python3 ~/.claude/harness/harness/scripts/skill-requires.py check --installed
```
  Lệnh ghi dấu `~/.claude/harness/skills-version.json` và in skill nào thiếu binary/script/sàn harness. Hook SessionStart tự nhắc một dòng `⬆ [version]` khi máy cũ hơn bản chuẩn (harness hoặc skill) — thấy dòng đó thì chạy đúng lệnh nó in.
- **Repo framework** (`repo_role: framework`): KHÔNG chạy installer vào đây — installer tự từ chối rc 3. Cập nhật framework = `git pull`.
- **Layout cũ trần** (`llmwiki/` + `harness/` nằm trong dự án, chưa có stamp) — đường `--self-heal` (tự detect migrate/update; thiếu nguồn thì clone template):
```bash
test -f harness/scripts/install-harness.sh \
  && bash harness/scripts/install-harness.sh . --self-heal \
  || { git clone -q --depth 1 -b orca git@github.com:rheinmir/setup.git /tmp/llmwiki-tpl \
       && bash /tmp/llmwiki-tpl/harness/scripts/install-harness.sh . --self-heal ; rm -rf /tmp/llmwiki-tpl; }
```
Installer tự làm trọn gói: cài L0–L4 → audit (Origin/index/OKF gộp 1 process qua `audit.py`) → nếu có nợ thì TỰ backfill (Origin lấy hash bằng 1 lượt `git log` cho cả lô; index thêm row thiếu; OKF migrate bold `**Type:**` → YAML) → re-audit 1 lần → activate + smoke.

**2. Đọc exit code (KHÔNG vòng lặp re-run — self-heal đã chạy bên trong):**
- `rc=0` → sạch (đã tự backfill xong). Sang bước 3.
- `rc=3` → còn nợ self-heal KHÔNG tự sửa được (vd file conflict, type OKF không suy được): danh sách nằm ngay trong output. Sửa thủ công 1 lần rồi chạy lại bước 1.
- `rc khác` (1/4) → lỗi hạ tầng (network, python3, validator hỏng) — DỪNG, báo user nguyên văn, không tự đoán.

**3. Nghiệm thu + log:**
- Xác nhận bảng "Harness tự kiểm" có **⛔×3 BỊ CHẶN ✓** trong output bước 1 (installer đã chạy `pre-commit install` nếu có pre-commit; chưa có thì nhắc user `pipx install pre-commit`).
- **Refresh bản đồ năng lực** (để agent thấy đúng đồ nghề sau update — ADR-005): `python3 ~/.claude/harness/hooks/build-capabilities.py --root .` (bản deploy cạnh hooks) HOẶC `python3 fdk/tools/build-capabilities.py` (nếu đang trong repo framework) → sinh lại `CAPABILITIES.md`. Không có file build-capabilities (bản cũ) → bỏ qua, không lỗi.
- **Health-check** (tuỳ chọn, xác nhận rào còn cắn sau update): `/health-check` hoặc `python3 ~/.claude/harness/hooks/health-check.py`.
- Append vào `llmwiki/wiki/log.md`: `## YYYY-MM-DD — harness-update — migrate/update xong (--self-heal), nợ đã backfill: <n> file`. Số liệu lấy từ dòng `[audit] backfill xong — Origin:<a> index:<b> OKF:<c>` trong output.

**4. Báo cáo cho user (bắt buộc đủ 4 ý):**
- Mode đã chạy (migrate hay update) + số nợ self-heal đã backfill (Origin/index/OKF từ dòng `[audit] backfill xong`)
- Settings root: file backup `.bak.*` nếu có merge
- Nhắc: **mở session mới thì hooks mới load**
- Mời: `/harness-tour` để xem hàng rào cắn trực quan

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | recovery | `rc=3` | sửa thủ công 1 lần các nợ self-heal không tự sửa được (danh sách trong output) | vẫn rc=3 → báo user | W01 |
| B02 | capability_optional | có `build-capabilities.py` (bản deploy hoặc repo framework) | sinh lại `CAPABILITIES.md` | bản cũ không có → bỏ qua, không lỗi | W03 |
| B03 | user_optional | muốn xác nhận rào còn cắn | `/health-check` | bỏ qua | W03 |

### Validation và stopping
Verdict do rc của installer (tất định) + bảng "Harness tự kiểm" có ⛔×3. Tối đa một vòng B01 → W01; rc khác 0/3 dừng ngay.

### Examples
- **Positive:** dự án có llmwiki cũ thiếu `## Origin` ở 12 trang → `install-harness.sh . --self-heal` → `[audit] backfill xong — Origin:12 index:0 OKF:0`, rc=0 → log + báo cáo "migrate, backfill 12 file, mở session mới để hooks load".
- **Boundary/failure:** máy không có `python3` → rc=1 → DỪNG, báo user nguyên văn lỗi, không tự cài hay chạy lại.
