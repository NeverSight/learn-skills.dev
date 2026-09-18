---
name: estimate-effort
description: Estimate khối lượng công việc của một dự án phần mềm bằng man-day. Dùng khi user cung cấp functional requirements (danh sách công việc) + techstacks và muốn ước lượng effort. Quy trình 3 bước (Sizing FE/BE → Manday Build → Full SDLC) cho Mid-level dev, output bảng markdown.
---

# Estimate Man-day cho dự án phần mềm

Skill này estimate khối lượng công việc của một dự án phần mềm bằng **man-day**, dựa trên danh sách functional requirements và techstacks.

## Giả định cố định

- **Level dev:** Mid-level developer
- **1 manday = 8 giờ làm việc thực tế**
- Estimate cho **full SDLC**, không chỉ riêng phần code

## Input cần có

1. **Functional requirements** — danh sách các đầu việc cần làm.
2. **Techstacks** — các stack sẽ dùng (FE / BE / DB / third-party...).

Nếu thiếu một trong hai, hỏi user trước khi estimate. Nếu một đầu việc mô tả mơ hồ, ghi rõ giả định đã đặt ra ở cột Ghi chú.

---

## Quy trình estimate (làm cho TỪNG đầu việc)

### Bước 1 — Sizing

Với mỗi requirement, mô tả rõ:

- Phần công việc **Frontend** phải làm (nếu có).
- Phần công việc **Backend** phải làm (nếu có).

Sau đó chấm điểm theo 2 trục cho mỗi role.

#### FE — 2 trục

**UI Complexity** — Giao diện phức tạp đến đâu?

- **1:** Static content, layout đơn giản, ít state. (FAQ page, static links)
- **2:** Form có validation, conditional rendering, responsive phức tạp. (Address toggle, contact form)
- **3:** Nhiều state combinations, real-time update, animation/interaction nặng. (Calculator, gamification, plan selector với nhiều conditions)

**Integration** — FE phụ thuộc bên ngoài nhiều không?

- **1:** Self-contained, không gọi API. (Static banner, video playback)
- **2:** Gọi 1–2 API đơn giản, handle vài error states. (Promo code validate, preference submit)
- **3:** Nhiều API, third-party SDK, real-time data, CMS-driven content. (OneMap + smart meter logic, MessageBird, Google Tag + Meta Pixel combo)

#### BE — 2 trục

**Business Logic** — Logic nghiệp vụ phức tạp đến đâu?

- **1:** CRUD đơn giản, ít rules. (Serve FAQ content, static config)
- **2:** Conditional logic rõ ràng, vài business rules, validation. (SD amount theo housing type, retailer detection "93")
- **3:** Rule engine, configurable bởi non-dev, nhiều edge cases, stacking logic. (Stackable promo codes, configurable pop-up rules, plan visibility per page)

**Integration** — BE kết nối ra ngoài nhiều không?

- **1:** Database nội bộ, không external service. (CRUD plans, save preferences)
- **2:** 1–2 external APIs hoặc services. (OneMap proxy, email routing)
- **3:** Nhiều external systems, webhook, queue, sync data phức tạp. (Third-party retailer verification, CMS + multi-channel banner delivery)

#### Tổng hợp size (mỗi role tính RIÊNG)

Cộng 2 trục của role đó:

- **S = 2–3 điểm**
- **M = 4–5 điểm**
- **L = 6 điểm**

> Một đầu việc có cả FE và BE → có 2 size riêng (size FE và size BE).

### Bước 2 — Quy đổi sang Man-day (Build effort)

Quy đổi size → man-day. Đây là effort của **riêng phase Build (≈ chiếm 40% SDLC, xem bước 3)**:

| Size | Điểm | Man-day (Build)               |
| ---- | ---- | ----------------------------- |
| S    | 2–3  | ~0.5–1.5                      |
| M    | 4–5  | ~2–4                          |
| L    | 6    | ~5–8+ (nên cân nhắc tách nhỏ) |

- Chọn 1 con số đại diện trong khoảng (không để dạng range ở bảng tổng hợp; range chỉ là guideline).
- Nếu đầu việc có cả FE và BE → cộng man-day Build của FE + BE.
- Nếu size = L → ghi chú "nên tách nhỏ".

### Bước 3 — Bổ sung Full SDLC

Man-day ở bước 2 mới chỉ là phase **Build**. Một đầu việc thực tế gồm 3 phase:

| Phase        | Bao gồm                               | Trọng số |
| ------------ | ------------------------------------- | -------- |
| Prepare      | Create Requirement + UI/UX            | 30%      |
| Build        | Dev + Unit Test + Self Test + Fix bug | 40%      |
| Verification | Acceptance Test + E2E Test + manual   | 30%      |

Build = 40% → quy đổi full SDLC:

```
Manday_FullSDLC = Manday_Build / 0.40 = Manday_Build × 2.5
```

Đây là cột **estimate cuối cùng** cần xuất ra.

---

## Output

Xuất ra **bảng markdown** cho từng đầu việc + phần tổng hợp. Dùng đúng format dưới đây.

### Bảng chi tiết từng đầu việc

| #   | Đầu việc | Mô tả FE | Mô tả BE | FE (UI/Intg → Size) | BE (Logic/Intg → Size) | MD Build (FE+BE) | MD Full SDLC (×2.5) | Ghi chú |
| --- | -------- | -------- | -------- | ------------------- | ---------------------- | ---------------- | ------------------- | ------- |
| 1   | ...      | ...      | ...      | 2/2 → M             | 1/1 → S                | 2.5 + 1 = 3.5    | 8.75                | ...     |

Quy ước cột:

- **FE / BE size:** ghi `<điểm trục 1>/<điểm trục 2> → <S/M/L>`. Nếu role không có việc, ghi `—`.
- **MD Build:** hiển thị phép cộng FE+BE rồi ra tổng.
- **MD Full SDLC:** `MD Build × 2.5`, làm tròn 2 chữ số thập phân hoặc 0.25.
- **Ghi chú:** giả định, rủi ro, hoặc cờ "nên tách nhỏ" (size L).

### Bảng tổng hợp

| Hạng mục              | Giá trị                |
| --------------------- | ---------------------- |
| Tổng MD Build         | ...                    |
| Tổng MD Full SDLC     | ...                    |
| Quy đổi giờ (×6.5h)   | ...                    |
| Số đầu việc           | ... (S: x, M: y, L: z) |
| Đầu việc nên tách nhỏ | ...                    |

Sau bảng, thêm phần **Giả định & Lưu ý**:

- Liệt kê các giả định đã đặt khi requirement mơ hồ.
- Cảnh báo các đầu việc size L cần tách.
- Nêu rủi ro phụ thuộc third-party / integration cao (trục Integration = 3).
- Nhắc rằng đây là estimate cho 1 Mid-level dev; chưa tính buffer quản lý dự án, meeting, hay thời gian onboard.

---

## Nguyên tắc khi estimate

- Chấm điểm **bảo thủ nhưng trung thực** — đừng cố ép xuống thấp. Khi phân vân giữa 2 mức, chọn mức cao hơn và ghi chú lý do.
- Mỗi điểm số phải **bám vào mô tả công việc thật** — không chấm điểm chung chung. Tham chiếu techstack: stack lạ/mới với team → tăng Integration hoặc thêm ghi chú rủi ro.
- Tách đầu việc size L thành các sub-task nhỏ hơn khi có thể, rồi estimate lại từng cái.
- Tổng man-day ra số cụ thể, không để range trong bảng cuối (range chỉ dùng để suy luận nội bộ).
