---
name: new-skill
disable-model-invocation: true
description: Scaffold (tạo) một skill mới — new skill — into the Rheinmir/skills checkout (skills/<name>/SKILL.md, frontmatter metadata.loop + metadata.requires) via fdk/tools/new-skill.py of the setup repo, then run the skills-repo gate (requires · provenance · catalog · tools/check.sh). Use when the user says "create a skill", "add a new skill", "scaffold a skill", "make a new skill", "new skill", or invokes /new-skill.
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.1.0"
  loop: dev-loop
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [fdk/tools/skill-reuse.py]
    framework_scripts: [fdk/tools/new-skill.py]
---

# Skill: new-skill

Từ 14/10/2026 skill sống ở repo riêng **Rheinmir/skills** (`skills/<name>/`), engine ở **Rheinmir/setup** (cài global `~/.claude/harness`). Thêm một skill là: khung SKILL.md đúng `solid-what-how/1` → khai `metadata.loop` + `metadata.requires` (sinh bằng grep) → marketplace → provenance → catalog/version → `tools/check.sh` xanh → push `main`. Không còn mirror `llmwiki/skills/`, không còn LOOP_MAP, không còn bảng AGENT.md/CLAUDE.md. Skill này lái `fdk/tools/new-skill.py` (repo setup) ghi khung vào checkout skills, rồi đi qua đúng các cổng của repo skills.

## WHAT

### Purpose và context
- **Purpose:** tạo một skill mới trong checkout Rheinmir/skills theo khung `solid-what-how/1`, khai đủ hợp đồng phụ thuộc, và để CI repo skills (≈10 s) xanh — không chạy CI framework.
- **Trigger (when to use):**
- The user asks to create / add / scaffold a new skill, or invokes `/new-skill`.
- You are about to hand-create a `skills/<name>/SKILL.md` and would otherwise forget `metadata.loop`, `requires`, marketplace or provenance.

> **Viết cho đúng nghề — đọc `[[skill-craft]]` trước.** Bộ từ vựng để một skill đoán được: hai loại phí (context load ↔ cognitive load — skill chỉ-gọi-tay thì khai `disable-model-invocation: true`, khỏi tốn context), completion criterion cho mỗi bước, leading word thay ba câu, và năm failure mode phải tránh (duplication/sediment/sprawl/no-op/negation). `/lint` bước 8b đo các thứ này bằng máy.
- **Non-goals:** không sửa engine (repo setup) để phục vụ một skill — skill cần script mới thì đó là PR ở setup trước, rồi nâng sàn `requires.harness`; không migrate skill đã có (sửa tại chỗ); không tạo skill kéo từ upstream bằng tool này (thứ đó vào `skills/external/` + `skill-provenance.py record --source <url>`).

### Mental model
`tên + loop + description (trigger) → new-skill.py --skills-dir <skills>/skills → skills/<tên>/SKILL.md (khung WHAT/HOW, metadata.loop) → điền TODO → swh-lint → skill-requires gen --write (requires từ grep) → marketplace.json → provenance record → catalog --update → tools/check.sh → push main`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | checkout `Rheinmir/skills` (`OVERSTACK_SKILLS_DIR=<checkout>/skills`) và checkout/bản global `Rheinmir/setup` (`<setup>`) | có | tool ở setup, dữ liệu ở skills |
| In | `<name>` | có | kebab-case, chưa tồn tại trong `skills/` |
| In | `--loop` | có | `dev-loop` · `orchestrate` · `wiki-loop` · `utils` → ghi vào `metadata.loop` |
| In | `--desc` | có | một dòng giàu trigger phrase (router BM25 khớp theo nó) |
| Out | `skills/<name>/SKILL.md` | có | khung SWH đã điền xong TODO, frontmatter có `metadata.loop` + `metadata.requires` |
| Out | marketplace + provenance + catalog/version | có | `bash tools/check.sh <setup>` 7/7 PASS |

### Rules và capabilities
- RULE-01 (MUST): `metadata.requires` là thứ SINH bằng `skill-requires.py gen --write` (grep tất định script engine + binary ở vị trí lệnh), không viết tay — CI `gen --check` bắt lệch.
- RULE-02 (MUST): skill gọi script engine thì sàn `requires.harness` phải ≥ bản setup có script đó; script chưa có trong setup HEAD → CI đỏ (`check --repo-root`), làm PR setup trước.
- RULE-03 (MUST): A vague `--desc` is a skill that never fires. Put concrete trigger phrases and `/`-commands in it.
- RULE-04 (MUST): Never overwrite an existing skill — if the name is taken, edit `skills/<name>/SKILL.md` in place or pick another name.
- RULE-05 (MUST): Mọi đổi file trong `skills/<name>/` → `skill-provenance.py record` lại và `tools/catalog.py --update` (bump version) — máy người dùng và MCP so bản qua `version.json`.
- Capabilities: ghi một thư mục skill trong checkout skills; đọc chỉ mục skill hiện có (BM25) để cảnh báo trùng; sửa marketplace.json; ghi sổ provenance + catalog của repo skills.

### Failure boundaries
- Tên đã tồn tại → **blocked** (tool từ chối), sửa tại chỗ hoặc đổi tên.
- Trùng năng lực trên ngưỡng BM25 → cảnh báo; với `--strict` thì **blocked**.
- Không có checkout setup (không `<setup>` và không `~/.claude/harness`) → **blocked**: `tools/check.sh` cần engine.
- `tools/check.sh` đỏ → chưa xong, sửa đúng cổng đỏ rồi chạy lại.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | yêu cầu user | chốt `<name>`, `--loop`, `--desc` giàu trigger | 3 input | mơ hồ → hỏi |
| W02 | effect | 3 input | `new-skill.py --skills-dir … --dry-run` rồi chạy thật — có mẫu hợp thì `--from <asset_id> --params p.json` | `skills/<name>/SKILL.md` + recipe `reuse_decision` | tên trùng → blocked · tham số sai → INVALID_PARAMETER |
| W03 | judgment | khung | điền mọi TODO của WHAT/HOW, chạy `swh-lint --root <skills>` | skill đạt cấu trúc | đỏ → sửa, lặp W03 |
| W04 | deterministic | skill | `skill-requires.py gen --write` → `metadata.requires` | frontmatter khai đủ | script không có ở setup → PR setup trước |
| W05 | effect | skill | thêm `./skills/<name>` vào `.claude-plugin/marketplace.json`; `skill-provenance.py record`; `tools/catalog.py --update` | 3 bề mặt + version bump | — |
| W06 | deterministic | repo skills | `bash tools/check.sh <setup>` | 7/7 PASS → push `main` | đỏ → sửa cổng lệch |

Chi tiết từng bước (nguồn chân lý cho W01–W06; `<setup>` = checkout Rheinmir/setup hoặc `~/.claude/harness`; chạy trong gốc checkout Rheinmir/skills):

1. Settle three inputs: a kebab-case `<name>`, a `--loop` (`dev-loop` | `orchestrate` | `wiki-loop` | `utils`), and a `--desc` that is **rich with trigger phrases**. Skill chỉ-gọi-tay (chỉ user gõ) → thêm `disable-model-invocation: true`, `--desc` rút thành một dòng người-đọc (xem `[[skill-craft]]`).
2. Preview first, then create (tool ở setup, ghi vào checkout skills):
   ```bash
   export OVERSTACK_SKILLS_DIR="$PWD/skills"
   python3 <setup>/fdk/tools/new-skill.py <name> --loop <loop> --desc "<description>" --dry-run   # preview body + next steps
   python3 <setup>/fdk/tools/new-skill.py <name> --loop <loop> --desc "<description>"             # write skills/<name>/SKILL.md
   ```
   It refuses if `skills/<name>/` already exists. Khung đã có `metadata.loop: <loop>`.
3. Fill in `skills/<name>/SKILL.md` — the skeleton is the compact `solid-what-how/1` template (`## WHAT` purpose/contract/rules/failure + `## HOW` main workflow table/branches/examples, see `[[solid-what-how]]`). Replace every TODO with real, verifiable content, then check the shape:
   ```bash
   python3 <setup>/fdk/tools/swh-lint.py --root "$PWD" --skills <name> --ci
   ```
4. Sinh hợp đồng phụ thuộc từ chính nội dung skill (script engine được nhắc + binary ở vị trí lệnh trong khối code):
   ```bash
   python3 <setup>/harness/scripts/skill-requires.py gen --write --skills-dir skills --repo-root <setup>
   python3 <setup>/harness/scripts/skill-requires.py check --skills-dir skills --repo-root <setup> --ci   # script có ở setup HEAD?
   ```
5. Đăng ký + ghi sổ + đóng dấu:
   ```bash
   # thêm "./skills/<name>" vào plugin phù hợp trong .claude-plugin/marketplace.json (tay)
   python3 <setup>/fdk/tools/skill-provenance.py --skills-dir skills --store skills.provenance.json record <name> --source local-authored
   python3 tools/catalog.py --update          # bump version.json + catalog.json
   ```
6. Verify every surface agrees — một lệnh, 7 cổng, ≈1 s cục bộ (CI GitHub ≈10 s):
   ```bash
   bash tools/check.sh <setup>
   ```
   Xanh → commit + push `main`. Máy người dùng cập nhật bằng `npx -y skills add rheinmir/skills#main --global --all` (hoặc bootstrap `--skills-only`).

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | skill chỉ-gọi-tay | thêm `disable-model-invocation: true`, rút `--desc` thành một dòng người đọc | skill model-invoked → skip | W02 |
| B02 | recovery | BM25 báo trùng năng lực | đổi tên dạng biến thể + làm description khác biệt, hoặc sửa skill có sẵn | `--strict` → dừng | W01 |
| B03 | user_optional | catalog có template khớp contract (lọc effect trước, xếp hạng sau) | `--from` render template typed + pin sha256 vào `fdk/skill-catalog/recipes/<name>.recipe.json` (repo setup); không hợp thì scratch kèm `--reason` | catalog không đọc được → decision `catalog_unavailable`, vẫn sinh khung compact | W03 |
| B04 | conditional_required | skill cần script engine CHƯA có ở setup | làm PR setup thêm script (kèm test), phát hành bản setup mới, rồi nâng `harness_floor` trong `version.json` của repo skills và chạy lại W04 | script đã có → skip | W05 |

### Validation và stopping
Mỗi lần chạy đều ghi `reuse_decision` (reuse · scratch · catalog_unavailable) — Reuse Layer SWH v1.1, catalog `fdk/skill-catalog/`, tool `fdk/tools/skill-reuse.py` (repo setup). Reuse không miễn cổng nào: skill sinh từ template vẫn phải qua `swh-lint`.
Xong khi `bash tools/check.sh <setup>` in `7 PASS · 0 FAIL` (registry · requires khớp grep · requires đủ ở setup HEAD · swh-lint · provenance · golden router · catalog/version). Hành vi thật (skill có được gọi đúng không) thử bằng 1–2 câu mẫu trong một phiên `claude -p`, lint không chứng minh được.

### Examples
- **Positive:** `new-skill.py csv-preview --loop utils --desc "Xem trước CSV… Trigger: 'preview csv'"` → `skills/csv-preview/SKILL.md`, điền WHAT/HOW, `gen --write` ra `requires: {bin: [python3]}`, marketplace + provenance + catalog, `check.sh` 7/7.
- **Boundary/failure:** `new-skill.py ship …` → tool từ chối vì `skills/ship/` đã tồn tại; sửa `skills/ship/SKILL.md` tại chỗ rồi `record ship` + `catalog --update`.
