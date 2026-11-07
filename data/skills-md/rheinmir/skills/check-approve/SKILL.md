---
name: check-approve
disable-model-invocation: true
description: Sinh sẵn 1-liner để trace 1 lệnh approve/return/reject của DMS trên log BE (docker) + FE proxy, ghi ra file .sh cho user copy-paste lên product server. Dùng khi user nói "viết lệnh check approve", "check duyệt request <CODE>", "approve treo / không thấy lệnh duyệt", "/check-approve".
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
  requires:
    bin: [docker]
---

# Skill: check-approve

## WHAT

### Purpose và context
- **Purpose:** Khi 1 request DMS "ấn approve mà bị treo" / không rõ lệnh duyệt có tới BE chưa, user cần **1 lệnh 1 dòng** để paste lên **product server** (`ubuntu@hcm-bonbon-sv03`) — agent KHÔNG có SSH tới product nên KHÔNG tự chạy, chỉ sinh lệnh ([[feedback_product_server_debug]]). Skill này sinh sẵn lệnh BE + FE, ghi ra file `.sh` (tránh lỗi xuống dòng khi copy) và in inline.
- **Trigger (when to use):**
  - `/check-approve <REQ-CODE> [--since 120m]`
  - User: "viết lệnh check (approve/duyệt)", "request <CODE> approve bị treo", "không thấy lệnh duyệt trong log", "check duyệt ở be/fe"
- **Non-goals:** không SSH/chạy lệnh trên product, không sửa bug approve (sự cố cần repro/fix → `/orca-issue`), không trace trên local mặc định.

### Mental model
`REQ-CODE (+ SUM-ID, since, container, user) → template BE + FE → one-liner 1 dòng → file .sh + in inline → user tự chạy trên product → đọc kết quả (có POST approve hay không)`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | `<REQ-CODE>` | có | mã request, vd `BAF-CTD-26050043`; thiếu → hỏi user |
| In | `--since` | không | khoảng docker logs, default `120m` |
| In | `--be-container` / `--user` | không | thiếu → để placeholder `<BE_CONTAINER>` / `<FE_USER>` |
| In | `SUM-ID` | không | lọc hẹp hơn, hỏi user nếu cần |
| Out | `scratchpad/check-approve-<REQ-CODE>.sh` | có | 2 one-liner BE + FE (hoặc path user chỉ định) |
| Out | lệnh inline trong câu trả lời | có | để user copy nhanh; "xong" = user có lệnh chạy được, KHÔNG phải agent đã chạy |

### Rules và capabilities
- RULE-01 (MUST): KHÔNG tự SSH/chạy lệnh trên product — chỉ sinh lệnh ([[feedback_product_server_debug]]).
- RULE-02 (MUST): Mặc định trace trên **product** (hcm-bonbon-sv03), không phải local.
- RULE-03 (MUST): Mỗi lệnh **giữ trên 1 dòng** (không xuống dòng).
- RULE-04 (MUST): Nếu user nói "ghi vào folder log của wiki" → ghi `.sh`/`.txt`, KHÔNG `.md` (tránh OKF frontmatter hook).
- Capabilities: ghi file lệnh cục bộ; không truy cập server, không mạng.

### Failure boundaries
- Thiếu `<REQ-CODE>` → **clarify**, không sinh lệnh với mã đoán.
- Không biết container/user → **partial** hợp lệ: sinh lệnh với placeholder, dặn user thay bằng `docker ps`.
- User yêu cầu agent tự chạy trên product → **blocked** theo RULE-01, chỉ đưa lệnh.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | lời user | Resolve tham số, còn lại để placeholder | bộ tham số | thiếu REQ-CODE → clarify |
| W02 | deterministic | tham số | Generate 2 one-liner BE + FE theo template, 1 dòng | 2 lệnh | — |
| W03 | effect | lệnh | Write vào `scratchpad/check-approve-<REQ-CODE>.sh` (hoặc path user chỉ định) | file `.sh` | — |
| W04 | deterministic | lệnh | Show inline; KHÔNG tự chạy | user có lệnh | — |

Chi tiết từng bước (nguồn chân lý cho W01–W04):

1. **Resolve** — lấy `<REQ-CODE>`, `--since`, container/user nếu user cung cấp; còn lại để placeholder cho user tự điền.
2. **Generate** — dựng 2 one-liner (BE + FE) theo template dưới, **giữ trên 1 dòng** (không xuống dòng).
3. **Write** — ghi vào `scratchpad/check-approve-<REQ-CODE>.sh` (hoặc path user chỉ định). Nếu user nói "ghi vào folder log của wiki" → ghi `.sh`/`.txt`, KHÔNG `.md` (tránh OKF frontmatter hook).
4. **Show** — in cả 2 lệnh inline trong câu trả lời để user copy nhanh. **KHÔNG tự chạy trên product.**

#### Input

| Tham số | Ý nghĩa | Default |
|---------|---------|---------|
| `<REQ-CODE>` | Mã request, vd `BAF-CTD-26050043` | bắt buộc |
| `--since` | Khoảng thời gian docker logs | `120m` |
| `--be-container` | Container backend (nếu user biết) | placeholder `<BE_CONTAINER>` |
| `--user` | Username FE để lọc proxy log | placeholder `<FE_USER>` (vd `trangntt`) |

`<REQ-CODE>` thường gắn `SUM-ID` (vd `1010228`) — hỏi user nếu cần lọc hẹp hơn.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | user_optional | user nói "ghi vào folder log của wiki" | ghi `.sh`/`.txt` vào đó thay vì `scratchpad/`, không `.md` | không nói → path mặc định | W04 |
| B02 | user_optional | user chỉ cần lọc theo mã request | dùng bản BE gọn thay bản tổng hợp | — | W03 |

### Validation và stopping
Kiểm bằng mắt: mỗi lệnh đúng 1 dòng, mã request đã thay đúng chỗ, placeholder còn lại được nêu rõ. Dừng sau W04 — bước đọc log là của user (mục "Đọc kết quả" dùng khi user dán log về).

### Examples
- **Positive:** `/check-approve BAF-CTD-26050043 --since 6h` → ghi `scratchpad/check-approve-BAF-CTD-26050043.sh` chứa lệnh BE + FE `--since 6h`, container để `<BE_CONTAINER>`/`<FE_CONTAINER>`, in inline, không chạy.
- **Boundary/failure:** "check approve treo giúp, tự ssh vào xem" không có mã request → hỏi mã request; từ chối SSH, chỉ sinh lệnh.

### Reference — Command templates

**BE (docker logs trên product) — lệnh tổng hợp các endpoint approve:**
```bash
docker logs <BE_CONTAINER> --since 120m 2>&1 | grep -i -B2 -A2 -e BAF-CTD-26050043 -e <SUM_ID> | grep -i -e POST -e Action -e Approve -e Reject -e Return -e UpdateGenTask -e GetGenTaskById -e UpdateTask -e "ApproveSummary/Approve" -e QuickApprove -e UpdateRequestByApproveGroup
```

**BE — bản gọn (chỉ lọc theo mã request):**
```bash
docker logs <BE_CONTAINER> --since 120m 2>&1 | grep -i -e POST -e approve -e UpdateGenTask -e ApproveSummary -e UpdateRequestByApproveGroup -e BAF-CTD-26050043
```

**FE (dms-proxy log) — lọc theo user + request:**
```bash
docker logs <FE_CONTAINER> --since 120m 2>&1 | grep -i -e "dms-proxy" -e BAF-CTD-26050043 -e <FE_USER> -e Approve -e Action
```

> Thay `<BE_CONTAINER>` / `<FE_CONTAINER>` bằng container thật (`docker ps`). Đổi `--since` nếu duyệt đã lâu (vd `6h`). Đổi `BAF-CTD-26050043` thành mã request cần check.

### Reference — Đọc kết quả

- **Có** `POST /api/ApproveSummary/Approve` (hoặc `UpdateGenTask`, `UpdateRequestByApproveGroup`) kèm mã request → lệnh duyệt ĐÃ tới BE.
- **Không có** dòng POST nào dù FE báo đã ấn → request treo ở FE / proxy, chưa gọi BE → soi tiếp [[concepts/approve-action-flow]] và proxy.
- Endpoint per-module xem [[entities/dms-modules]] (BAF/VEN01/CashAdv… khác nhau).

### Reference — Giới hạn

- KHÔNG tự SSH/chạy lệnh trên product — chỉ sinh lệnh ([[feedback_product_server_debug]]).
- Mặc định trace trên **product** (hcm-bonbon-sv03), không phải local.

## Origin
- **Raw:** distill từ session 6902c846 / c2f1149e (2026-06-25, debug approve treo BAF-CTD-26050043/30/26060030)
- **Generated by:** /orca-eval finding #3 (250626-eval-report)
