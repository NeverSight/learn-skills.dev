---
name: crawl-shopping-product
description: |
  Cào thông tin sản phẩm (tiêu đề, ảnh, mô tả, giá) từ link Shopee, TikTok Shop, hoặc Lazada.
  Sử dụng thư viện crawl4ai kết hợp custom LLM extraction strategy qua OpenAI-compatible endpoint cấu hình trong .env.
---

# crawl-shopping-product

Skill cào dữ liệu có cấu trúc từ link sản phẩm trên các sàn thương mại điện tử (**Shopee**, **TikTok Shop**, **Lazada**), hỗ trợ cả link rút gọn (`vn.shp.ee`, `vt.tiktok.com`).

Skill phục vụ trực tiếp cho quy trình **Bước 1 & Bước 2 (SOP)**: Thu thập thông tin sản phẩm thực tế và tải ảnh sản phẩm độ phân giải cao để tạo **Product Dossier** trước khi triệu tập Hội đồng Đạo diễn.

## Quy Chuẩn Bắt Buộc Về Thư Mục Phiên Làm Việc (Session Dir)

> [!IMPORTANT]
> **QUY TẮC CÔ LẬP DỮ LIỆU & BẢO VỆ MÃ NGUỒN**:
> Tuyệt đối **KHÔNG** xả file `product_data.json` hay ảnh cào được trực tiếp ra root repo hoặc thư mục chung. Mọi dữ liệu cào sản phẩm bắt buộc phải lưu trong thư mục session chuẩn hóa.

- **Thư mục gốc:** `./.scratch/`
- **Cú pháp đặt tên:** `./.scratch/yyyy-mm-dd_crawl-shopping-product_công-việc-viết-không-dấu`
  - Ví dụ: `./.scratch/2026-09-22_crawl-shopping-product_cao-dam-da-hoi`
- **Cấu trúc phân vùng thư mục con bắt buộc:**
  ```text
  ./.scratch/yyyy-mm-dd_crawl-shopping-product_công-việc-viết-không-dấu/
  ├── downloads/  # (hoặc input/, raw/) Chứa toàn bộ ảnh sản phẩm độ phân giải cao tải về
  ├── output/     # (hoặc generated/) Chứa tệp dữ liệu có cấu trúc `product_data.json`
  ├── scripts/    # Chứa script trích xuất bổ trợ riêng cho session (tuyệt đối không sửa src/)
  └── temp/       # Chứa tệp HTML cache, raw responses trung gian
  ```
- **Tự động phân phối tài nguyên bằng tham số `--session-dir`:**
  - Khi truyền `--session-dir <đường_dẫn_session>`, script `crawl_product.py` sẽ **tự động**:
    1. Tạo đầy đủ các thư mục con cần thiết nếu chưa có.
    2. Xuất kết quả JSON vào `<session_dir>/output/product_data.json`.
    3. Tải và lưu toàn bộ ảnh sản phẩm vào `<session_dir>/downloads/`.

## Tính năng chính

- **Cào tự động đa sàn**: Hỗ trợ Shopee, TikTok Shop, Lazada (tự động phân giải link rút gọn di động).
- **Trích xuất thông minh (LLM-powered)**: Sử dụng `crawl4ai` (`AsyncWebCrawler`) tích hợp `LLMExtractionStrategy` gọi qua OpenAI-compatible gateway (mặc định `https://api.openai.com/v1`).
- **Fallback tự động**: Dự phòng bóc tách nhanh qua HTML tags, JSON-LD (`@type: Product`), và OpenGraph metadata.
- **Tải ảnh tự động**: Tùy chọn `--download-images` tự động tải ảnh gốc về thư mục đích phục vụ Vision/OCR.
- **Bảo đảm chuẩn KOC**: Giá tiền và mã SKU chỉ lưu trong tệp JSON hồ sơ kỹ thuật, không đưa vào kịch bản voiceover.

## Cấu hình Môi trường (.env)

Skill tự động nhận diện cấu hình từ file `.env` dự án:
```env
# Endpoint tương thích OpenAI Chat Completions
AI_AGENT_3_ENDPOINT_URL=https://api.openai.com/v1/chat/completions
AI_AGENT_3_API_KEY=<YOUR_API_KEY>
AI_AGENT_3_MODELS=gpt-4o
```
*(Hoặc fallback về `AI_AGENT_1_ENDPOINT_URL`, `AI_AGENT_1_API_KEY`, `AI_AGENT_1_MODELS`).*

## Hướng dẫn Sử dụng (CLI)

```bash
# Thiết lập biến session_dir chuẩn hóa
SESSION_DIR="./.scratch/2026-09-22_crawl-shopping-product_cao-dam-da-hoi"

# 1. Cào tự động kèm tải ảnh với tham số --session-dir (Khuyến nghị hàng đầu)
# (Script tự động lưu output/product_data.json và tải ảnh vào downloads/)
python .agents/skills/crawl-shopping-product/scripts/crawl_product.py \
  --url "https://shopee.vn/product/123/456" \
  --session-dir "$SESSION_DIR" \
  --download-images

# 2. Cào bằng Fallback nhanh (DOM & JSON-LD, không tốn token LLM)
python .agents/skills/crawl-shopping-product/scripts/crawl_product.py \
  --url "https://vn.shp.ee/xyz" \
  --method fallback \
  --session-dir "$SESSION_DIR"

# 3. Chỉ định phương thức LLM và đường dẫn đích trong session
python .agents/skills/crawl-shopping-product/scripts/crawl_product.py \
  --url "https://vt.tiktok.com/ZS.../" \
  --method llm \
  --session-dir "$SESSION_DIR" \
  --output "$SESSION_DIR/output/product_data.json" \
  --download-images "$SESSION_DIR/downloads"
```

### Tham số dòng lệnh:
- `--session-dir`: (Khuyến nghị) Đường dẫn thư mục session. Tự động lưu JSON vào `output/product_data.json` và ảnh vào `downloads/`.
- `--url`: (Bắt buộc) Đường dẫn sản phẩm Shopee, TikTok Shop, hoặc Lazada.
- `--output`: Đường dẫn tệp JSON đầu ra (nếu không dùng `--session-dir`, bắt buộc phải chỉ định đường dẫn bên trong thư mục session, tuyệt đối không xả ra root).
- `--download-images`: Thư mục lưu ảnh sản phẩm tải về (khi có `--session-dir`, tự động lưu vào `downloads/`).
- `--method`: Phương thức cào (`auto`, `llm`, `fallback`) — mặc định: `auto`.

## Định dạng Dữ liệu Đầu ra (`product_data.json`)

```json
{
  "title": "Đầm Dạ Hội Voan Tơ Bồng Bềnh Xẻ Tà",
  "images": [
    "https://cf.shopee.vn/file/img_front.jpg",
    "https://cf.shopee.vn/file/img_detail.jpg"
  ],
  "description": "Chất liệu voan tơ mềm mại, cổ trễ vai gợi cảm, đính hoa thủ công...",
  "price": {
    "current_price": 289000.0,
    "currency": "VND"
  },
  "platform": "shopee",
  "source_url": "https://shopee.vn/..."
}
```
### Cấu hình LLM bắt buộc

Đặt các biến sau trong `.env` trước khi crawl. Skill không có endpoint, API key hoặc model mặc định:

```env
CRAWL_PRODUCT_ENDPOINT_URL=https://your-provider.example/v1
CRAWL_PRODUCT_API_KEY=your_api_key
CRAWL_PRODUCT_MODEL=your_model
```
