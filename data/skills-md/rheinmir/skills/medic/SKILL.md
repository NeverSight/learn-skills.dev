---
name: medic
description: >-
  Cổng sức khoẻ tổng / tuyến phòng thủ cuối của framework overstack — gõ /medic
  (hoặc `medic` ở CLI) để CHỨNG MINH hệ còn khoẻ trong MỘT lệnh: luật còn cắn
  (harness-doctor fire-drill), validator không lệch bản (drift), docs khớp đĩa,
  code compile, eval không regress, backstop git sống. Hub 1-tên — mô tả PHẠM VI
  thay vì nhớ subcommand (`medic` = all · `medic rules` · `medic docs eval`).
  Dùng trước commit/PR, sau khi pull/đổi máy, khi nghi một rule không chặn nữa,
  hoặc vừa thêm skill/rule/generator (medic tự báo nếu quên hàng rào). Trigger:
  /medic, "medic", "chạy medic", "hệ còn khoẻ không", "rà luật có cắn không",
  "cổng phòng thủ cuối", "health gate", "last line of defense".
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
  requires:
    harness: ">=1.3.127"
    bin: [python3]
    scripts: [fdk/tools/medic.py]
---

# Skill: medic

> Chìa vạn năng: một lệnh = tuyến phòng thủ cuối. Nó KHÔNG sửa gì — chỉ **chứng minh** hệ còn khoẻ và, nếu không, in đúng chỗ hở + 1 dòng lệnh sửa.

## WHAT

### Purpose và context
- **Purpose:** chứng minh bằng MỘT lệnh rằng framework overstack còn khoẻ (luật cắn, không drift, docs khớp đĩa, code compile, eval không regress, backstop git sống); hỏng thì chỉ đúng chỗ hở + lệnh sửa.
- **Trigger (when to use):**
  - Trước khi commit / mở PR — chốt: đỏ thì đừng đẩy.
  - Sau khi kéo bản mới / đổi máy — xem overstack còn nguyên vẹn.
  - Nghi một rule "có vẻ không chặn nữa" — rà riêng tầng luật.
  - Vừa thêm skill / rule / generator — medic tự báo nếu quên hàng rào cho nó (tự-mở-coverage).
  - Chỉ muốn coi cấu trúc phòng thủ đang có — `medic --list`.
- **Non-goals:** không sửa gì, không vá nợ lớn (việc của proposal `030726-medic`), không thay `/fdk-uat` (đường cài remote).

### Mental model
`phạm vi (user mô tả) → probe (rules · coverage · docs · code · eval · backstop) → ✓/⚠/✗ + detail + ↳ sửa → verdict`. Probe là đơn vị kiểm; `medic.py` là hub duy nhất — thêm kiểm tra = thêm probe, không đẻ tool lẻ.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | phạm vi | không (mặc định = all) | từ khoá khớp tên/tag probe, nhiều phạm vi cách nhau khoảng trắng |
| In | `--ci` | không | cần exit-code để chốt (pre-commit/CI) |
| Out | báo cáo | có | mỗi probe ✓/⚠/✗ + detail + `↳ sửa`, verdict, recap, cấu trúc thư mục — chuyển NGUYÊN cho user |
| Out | exit code | khi `--ci` | FAIL → exit 1; không FAIL → 0 |

### Rules và capabilities
- RULE-01 (MUST): **Không sửa gì trong lúc rà** — medic chỉ chẩn đoán; sửa là bước riêng, có chủ đích.
- RULE-02 (MUST): **Tôn trọng fail-open**: một probe lỗi → SKIP, không kết luận "hệ hỏng".
- RULE-03 (MUST): **Mô tả phạm vi, đừng đẻ lệnh** — user cần kiểm tra chưa có thì thêm probe vào `medic.py` (một chỗ), đừng tạo tool lẻ mới.
- RULE-04 (MUST): Self-contained: `medic.py` chỉ stdlib; compose tool đã có, không dependency ngoài.
- RULE-05 (MUST): drift/stale chỉ regen/sync, KHÔNG sửa logic; **xác minh hướng** trước khi sync validator — bản đang CẮN mới là bản đúng (bài học 030726: sync sai hướng làm rail thành đen).
- Capabilities: đọc repo framework + chạy probe cục bộ (read-only); không ghi, không mạng bắt buộc.

### Failure boundaries
- Có ✗ → verdict FAIL (exit 1 với `--ci`); đề nghị đúng 1 dòng `↳ sửa`, không tự chạy.
- Chỉ ⚠ → nợ đã biết, báo user, không tự vá lớn.
- Probe crash → SKIP (fail-open), không tính là FAIL.
- Phạm vi không khớp probe nào → báo lại danh sách probe (`medic --list`), không đoán.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | lời user | **Chọn phạm vi theo mô tả user** (không bắt nhớ subcommand): toàn bộ → không tham số; một phần → từ khoá khớp tên/tag probe (`rules`, `coverage`, `docs`, `code`, `eval`, `backstop`) | danh sách phạm vi | mơ hồ → all |
| W02 | deterministic | phạm vi | **Chạy** `python3 fdk/tools/medic.py [phạm vi]` (hoặc `medic [phạm vi]` nếu symlink `~/.local/bin/medic` đã có); thêm `--ci` khi cần exit-code | báo cáo + rc | → W03 |
| W03 | deterministic | báo cáo | **Chuyển cho user NGUYÊN output** — medic đã in cô đọng; đừng cắt gọn phần này | user thấy đủ | có ✗ → B01; chỉ ⚠ → B02; sạch → xong |

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | recovery | có ✗ (fail) | đề nghị chạy đúng 1 dòng `↳ sửa` medic gợi ý; drift/stale thì chỉ regen/sync (RULE-05) | user từ chối → dừng, verdict vẫn FAIL | chạy lại W02 sau khi sửa |
| B02 | conditional_required | có ⚠ (warn), vd coverage 5/17, pre-commit chưa cài | báo user là nợ đã biết; không tự ý vá lớn — đó là việc của proposal `030726-medic` | — | kết thúc |

### Validation và stopping
Verdict do `medic.py` quyết (tất định), không do model tự kết luận. Tối đa một vòng B01 → W02 mỗi lần gọi; còn đỏ thì dừng và báo.

### Examples
- **Positive:** "chạy medic trước khi commit" → `python3 fdk/tools/medic.py --ci` → mọi probe ✓ → exit 0, báo "hệ khoẻ, commit được".
- **Boundary/failure:** "medic docs" khi CAPABILITIES lệch đĩa → probe docs ✗ kèm `↳ sửa` regen → đề nghị đúng lệnh đó, không tự sửa; `--ci` trả exit 1.
