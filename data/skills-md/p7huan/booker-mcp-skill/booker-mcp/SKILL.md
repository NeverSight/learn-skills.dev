---
name: booker-mcp
description: Cẩm nang điều phối Booker MCP Server (11 công cụ) dành cho Nhân viên Booker & AI Travel Assistant hỗ trợ tìm kiếm homestay/villa, check phòng trống, báo giá chuẩn server (Room/Whole/Villa), quản lý Yêu cầu đặt phòng (Leads), tạo/cập nhật Booking, quản lý giao dịch thanh toán (BookingTransaction), VietQR (Khách & Host), áp Voucher, gửi Email Hợp đồng và xử lý hủy/xác nhận đơn trên Ohdidi.
---

# Booker MCP — Cẩm nang Trợ lý & Điều phối Đặt phòng Ohdidi (11 Công cụ Chuẩn Nghiệp vụ)

Hệ thống **Booker MCP Server** cung cấp **11 công cụ** chuẩn JSON-RPC 2.0, khớp 100% với nghiệp vụ thực tế của `BookingController`, `BookingRequestController`, `BookingService`, và `VillaQuoteService` trên hệ thống Ohdidi.

---

## ⚡ Thông tin Kết nối Server

| Giao thức | Địa chỉ / Lệnh thực thi | Ghi chú |
| :--- | :--- | :--- |
| **Remote HTTP/SSE** | `https://ohdidi.vn/api/mcp/booker` | Header: `Authorization: Bearer <MCP_KEY>` |
| **Local Stdio CLI** | `/opt/homebrew/opt/php@7.3/bin/php scripts/mcp-booker.php --key=<MCP_KEY>` | Hoặc set env `OHDIDI_MCP_KEY` |

> Khóa API Key được quản trị tập trung tại: `https://ohdidi.dev/admin/mcp-key/index` (Tab **Booker MCP (11 tools)**).

---

## 🛠️ Danh mục 11 Công cụ Booker MCP

| STT | Tool Name | Nghiệp vụ chuẩn Ohdidi | Tham số chính |
| :---: | :--- | :--- | :--- |
| 1 | `booker_search_hostings` | Tìm kiếm chỗ nghỉ theo tên tỉnh (`province_name`), mã tỉnh, loại hình (`room`, `whole`, `villa`), kèm thông tin Host, % hoa hồng, `price_origin`, cấu hình thuế đối tác | `keyword`, `province_name`, `province_code`, `rental_type`, `min_price`, `max_price`, `page`, `limit` |
| 2 | `booker_hosting_detail` | Xem chi tiết chỗ nghỉ: danh sách phòng lẻ (`price_origin`, `physical_units`), nguyên căn (`wholes`), biệt thự (`villas` & `villa_items`), thông tin Host, thuế VAT và tài khoản ngân hàng chính của Chủ nhà (`HostBankModel`) | `hosting_id` |
| 3 | `booker_check_availability` | Kiểm tra lịch trống & báo giá chuẩn Server cho cả 3 loại hình (`room`, `whole`, `villa` qua `VillaQuoteService`), trả về `total_price_origin`, `total_price`, `benefit`, thuế VAT và danh sách phòng vật lý con | `hosting_id`, `checkin`, `checkout`, `adults`, `children`, `rental_type`, `room_id`, `is_whole`, `villa_items` |
| 4 | `booker_create_booking` | Tạo mới hoặc Cập nhật đơn đặt phòng (`room`, `whole`, `villa`). Tự động tính `total_price_origin`, `benefit`, `surcharge`, thuế VAT đối tác Doanh nghiệp (`tax_rate`, `tax_amount`, `net_price`), tự động tìm `user_id`, gắn `member_id`, áp Voucher tốt nhất và bắn Telegram *(Hỗ trợ Dry-Run)* | `booking_id`/`booking_code` *(khi sửa)*, `hosting_id`, `rental_type`, `checkin`, `checkout`, `guest_name`, `guest_phone`, `guest_email`, `rooms`, `whole_id`, `villas`, `surcharge`, `confirm` |
| 5 | `booker_payment_intent` | Quản lý các đợt thanh toán (`BookingTransactionModel`) và sinh mã VietQR: (1) `summary`: xem `total_payment`, `sum_recharge`, `sum_need`, danh sách tài khoản nhận của Ohdidi (`BankAccountModel` `[DN]`/`[CN]`), VietQR cho khách & VietQR chuyển cọc cho Host (`HostBankModel`); (2) `save_transaction`: Tạo/Sửa đợt thanh toán (kiểm tra chặt chẽ tài khoản `[DN]` cho đối tác doanh nghiệp); (3) `delete_transaction`: Xóa đợt thanh toán *(Hỗ trợ Dry-Run)* | `action` (`summary`, `save_transaction`, `delete_transaction`), `booking_code`, `transaction_id`, `bank_account_id`, `recharge`, `host_receive`, `benefit`, `payment_date`, `description`, `confirm` |
| 6 | `booker_confirm_booking` | Xác nhận đơn đặt phòng (`CONFIRMED`) qua `BookingService::confirmBookingByHost`. Kiểm tra bắt buộc có ít nhất 1 giao dịch thanh toán, khóa lịch Room/Whole/Villa, gán phòng vật lý (`room_assignments`) và đẩy 5 job vào Beanstalkd Queue *(Hỗ trợ Dry-Run)* | `booking_code`, `room_assignments`, `allow_without_transaction`, `note`, `confirm` |
| 7 | `booker_lookup_booking` | Xem chi tiết 1 đơn đặt phòng (đầy đủ phòng/villa, bảng tính tài chính, giao dịch, ngân hàng Host) HOẶC lọc danh sách nhiều đơn theo SĐT, tên khách, tên chỗ nghỉ, trạng thái, kênh bán, Booker phụ trách | `booking_code`, `booking_id`, `phone`, `guest_name`, `hosting_name`, `status`, `channel`, `member_id`, `start_date`, `end_date` |
| 8 | `booker_cancel_booking` | Hủy đơn đặt phòng (`CANCELLED`) qua `BookingService::cancelBookingByHost`: giải phóng mã Affiliate, lưu `BookingCancelModel`, mở lại quỹ phòng Room/Whole/Villa/Unit và đẩy thông báo vào Queue *(Hỗ trợ Dry-Run)* | `booking_code`, `phone`, `reason`, `confirm` |
| 9 | `booker_complete_booking` | Đánh dấu hoàn thành đơn (`COMPLETED`) sau khi khách check-out *(Hỗ trợ Dry-Run)* | `booking_code`, `note`, `confirm` |
| 10 | `booker_manage_requests` | Quản lý Yêu cầu đặt phòng / Leads (`BookingRequestModel`): lọc danh sách (`list`), xem chi tiết (`detail`), chuyển đổi thành Booking chính thức (`convert_to_booking` qua `BookingRequestService::createBookingFromRequest`), đánh dấu đã xử lý (`mark_processed`) hoặc hủy (`cancel`) *(Hỗ trợ Dry-Run)* | `action`, `request_id`, `status`, `phone`, `guest_name`, `hosting_name`, `member_id`, `confirm` |
| 11 | `booker_voucher_and_email` | Quản lý Voucher & Email Hợp đồng: liệt kê voucher khả dụng (`list_vouchers`), áp dụng voucher hoặc mức giảm tùy chỉnh (`apply_voucher` với `custom_discount`), gửi Email Hợp đồng xác nhận đặt phòng cho khách (`send_contract_email`) *(Hỗ trợ Dry-Run)* | `action`, `booking_code`, `voucher_id`, `voucher_code`, `custom_discount`, `confirm` |

---

## 💡 Quy tắc Nghiệp vụ Quan trọng cho Booker AI

1. **Quy tắc Tài chính & Thuế VAT Đối tác Doanh nghiệp:**
   - Công thức chuẩn: `total_price = total_price_origin + benefit` (trước thuế VAT).
   - Nếu Chủ nhà (Host) là đối tác doanh nghiệp (`host_type = 'business'` và `cooperation_status` thuộc `['partner', 'partner_no_contract']`):
     - Nếu `tax_included == 1`: chỉ cộng thêm VAT trên phần chênh lệch `benefit` (`total_price - total_price_origin`).
     - Nếu `tax_included == 0`: cộng toàn bộ VAT (`tax_rate`, mặc định `8%`) vào `total_price`.
   - Khi tạo giao dịch thanh toán (`booker_payment_intent` với `action: "save_transaction"`), đơn của đối tác doanh nghiệp/hộ kinh doanh hợp tác **bắt buộc** phải chọn tài khoản ngân hàng nhận thuộc loại `business` (`[DN]`).
2. **Quy tắc Xác nhận Đơn (`booker_confirm_booking`):**
   - Đơn đặt phòng bắt buộc phải có ít nhất **1 đợt giao dịch thanh toán (`BookingTransactionModel`)** trước khi xác nhận sang `CONFIRMED` để khóa lịch phòng và gửi hợp đồng cho khách.
3. **Kỷ luật Dry-Run (An toàn Dữ liệu):**
   - Toàn bộ các công cụ ghi dữ liệu (`booker_create_booking`, `booker_payment_intent`, `booker_confirm_booking`, `booker_cancel_booking`, `booker_complete_booking`, `booker_manage_requests`, `booker_voucher_and_email`) đều mặc định chạy ở chế độ **Dry-Run (`confirm: false`)**.
   - AI luôn trình bày bản xem trước (`preview_data`) cho người dùng kiểm tra, sau khi người dùng đồng ý mới gọi lại với `confirm: true`.
