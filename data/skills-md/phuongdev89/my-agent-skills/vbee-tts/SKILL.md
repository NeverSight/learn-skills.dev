---
name: vbee-tts
description: Generate natural Vietnamese narration with Vbee AIVoice (vbee.vn). Use when creating Vietnamese voiceovers, when the user requests Vbee TTS, or when narration needs regional Vietnamese accents (North, South, Central).
---

# Vbee AIVoice TTS

**Vbee AIVoice** (vbee.vn) là nền tảng Cloud Text-to-Speech tiếng Việt chuyên nghiệp với ngữ điệu tự nhiên và phân hóa giọng đọc 3 miền (Bắc, Trung, Nam):
- **Chất lượng 48 kHz** (chuẩn phòng thu, giọng trong trẻo, không bị méo tiếng).
- **Hỗ trợ đầy đủ giọng KOC / Thuyết minh / Đọc báo**: Thu Trang, Ngọc Huyền, Mai Phương, Mạnh Dũng, Thảo Trinh...
- **Tốc độ linh hoạt**: Tùy chỉnh `speed` từ `0.1` đến `1.9` (mặc định `1.0`).
- **Tích hợp sẵn script CLI**: Sinh file âm thanh và đo đạc thời lượng thực tế chính xác (`duration_seconds`), trả về định dạng chuẩn JSON.

## Quy Chuẩn Bắt Buộc Về Thư Mục Phiên Làm Việc (Session Dir)

> [!IMPORTANT]
> **QUY TẮC CÔ LẬP DỮ LIỆU & BẢO VỆ MÃ NGUỒN**:
> Tuyệt đối **KHÔNG** xả file âm thanh tạo bởi Vbee hoặc file kịch bản trực tiếp ra thư mục gốc repo hoặc `04_canh/` bừa bãi. Mọi tác vụ sinh giọng đọc phải được tổ chức trong thư mục session chuẩn hóa.

- **Thư mục gốc:** `./.scratch/`
- **Cú pháp đặt tên:** `./.scratch/yyyy-mm-dd_vbee-tts_công-việc-viết-không-dấu`
  - Ví dụ: `./.scratch/2026-09-22_vbee-tts_sinh-giong-thu-trang-review`
- **Cấu trúc phân vùng thư mục con bắt buộc:**
  ```text
  ./.scratch/yyyy-mm-dd_vbee-tts_công-việc-viết-không-dấu/
  ├── input/      # Chứa file văn bản kịch bản phân cảnh (`voice_segment.txt`, `script.txt`)
  ├── output/     # Chứa file âm thanh hoàn chỉnh (`voiceover.mp3`, `voiceover.wav`, `S01_audio.mp3`)
  ├── scripts/    # Chứa script tiện ích / tinh chỉnh bổ trợ phiên làm việc (tuyệt đối không sửa src/)
  └── temp/       # Chứa audio chunks tạm, API cache
  ```
- **Tự động phân phối tài nguyên bằng tham số `--session-dir`:**
  - Script `generate_vbee_voice.py` hỗ trợ tham số `--session-dir <đường_dẫn_session>`.
  - Khi có `--session-dir` và không truyền `--output`, script tự động xuất file âm thanh vào `<session_dir>/output/voiceover.<format>`.
  - Hoặc có thể truyền rõ `--output <session_dir>/output/<tên_file>.<format>`.

---

## 1. Cấu hình Tài khoản & Biến môi trường

Vbee yêu cầu API Key / Token từ tài khoản Vbee:
Cần cấu hình trong file `.env` tại thư mục dự án. Nếu dùng file cấu hình riêng, đặt `VBEE_ENV_FILE` trỏ tới file đó:
```env
VBEE_APP_ID=your_vbee_app_id
VBEE_ACCESS_TOKEN=your_vbee_access_token
```

Script sẽ tự động tìm kiếm các file `.env` theo thứ tự:
1. `.env` tại thư mục hiện tại (`cwd`)
2. File được chỉ định bởi `VBEE_ENV_FILE`
4. Biến môi trường hệ thống (`os.environ`)

---

## 2. Tiện ích Thực thi Có Sẵn Trong Skill (`scripts/generate_vbee_voice.py`)

Skill cung cấp sẵn script CLI thực thi hoàn chỉnh tại:
[`scripts/generate_vbee_voice.py`](scripts/generate_vbee_voice.py)

Agent có thể chạy trực tiếp bằng dòng lệnh mà không cần viết thêm code Python:

```bash
# Thiết lập biến session_dir chuẩn hóa
SESSION_DIR="./.scratch/2026-09-22_vbee-tts_sinh-giong-thu-trang-review"
```

### A. Sinh giọng đọc từ văn bản trực tiếp (Tự động xuất vào session_dir/output/)
```bash
python .agents/skills/vbee-tts/scripts/generate_vbee_voice.py \
  --text "Chào bạn! Đây là giọng đọc Thu Trang của Vbee nhé." \
  --voice "thutrang" \
  --session-dir "$SESSION_DIR"
```

### B. Sinh giọng đọc từ file kịch bản trong input/ (Chỉ định rõ file trong output/)
```bash
python .agents/skills/vbee-tts/scripts/generate_vbee_voice.py \
  --text-file "$SESSION_DIR/input/voice_segment.txt" \
  --voice "ngochuyen" \
  --speed 1.05 \
  --session-dir "$SESSION_DIR" \
  --output "$SESSION_DIR/output/S01_audio.mp3"
```

### C. Liệt kê các alias và giọng đọc phổ biến
```bash
python .agents/skills/vbee-tts/scripts/generate_vbee_voice.py --list-voices
```

### Định dạng đầu ra (JSON Output)
Script trả về kết quả JSON chuẩn giúp Agent và hệ thống đối soát thời lượng thực tế (`duration_seconds`):
```json
{
  "status": "success",
  "engine": "vbee",
  "voice_code": "hn_female_thutrang_48k-fhg",
  "output_file": "<session_dir>/output/voiceover.mp3",
  "duration_seconds": 3.84,
  "file_size_bytes": 61440,
  "audio_format": "mp3"
}
```

---

## 3. Bảng Alias và Giọng đọc Phổ biến

Skill hỗ trợ truyền alias ngắn gọn (không phân biệt hoa thường) hoặc mã `voice_code` Vbee đầy đủ:

| Khu vực | Alias | Tên giọng & Đặc điểm | Vbee Voice Code |
| :--- | :--- | :--- | :--- |
| **Miền Bắc** | `thutrang` | **Thu Trang** — Nữ · Bắc (KOC Review sinh động, 48kHz) | `hn_female_thutrang_48k-fhg` |
| | `ngochuyen` | **Ngọc Huyền** — Nữ · Bắc (Chuẩn tin tức, thuyết minh) | `hn_female_ngochuyen_full_48k-fhg` |
| | `maiphuong` | **Mai Phương** — Nữ · Bắc (Truyền cảm, dịu dàng) | `hn_female_maiphuong_vdts_48k-fhg` |
| | `manhdung` | **Mạnh Dũng** — Nam · Bắc (Đọc báo, chuyên nghiệp) | `hn_male_manhdung_news_48k-fhg` |
| | `ducanh` | **Đức Anh** — Nam · Bắc (Tự nhiên, năng động) | `hn_male_ducanh_48k-fhg` |
| **Miền Nam** | `thaotrinh` | **Thảo Trinh** — Nữ · Nam (Truyền cảm, ấm áp) | `sg_female_thaotrinh_48k-fhg` |
| | `minhhoang` | **Minh Hoàng** — Nam · Nam (Ấm áp, gần gũi) | `sg_male_minhhoang_48k-fhg` |
| | `lanhuong` | **Lan Hương** — Nữ · Nam (Nhẹ nhàng, thanh thoát) | `sg_female_lanhuong_48k-fhg` |
| **Miền Trung** | `huonggiang` | **Hương Giang** — Nữ · Huế/Trung (Dịu dàng, đằm thắm) | `hue_female_huonggiang_48k-fhg` |
| | `duyphuong` | **Duy Phương** — Nam · Huế/Trung (Ấm áp, truyền cảm) | `hue_male_duyphuong_48k-fhg` |

Mọi `voice_code` khác trên thư viện Vbee (vbee.vn) đều có thể truyền trực tiếp qua tham số `--voice`.

---

## 4. Quy tắc KOC & Dynamic Duration (Bắt buộc)

1. **KOC Identity**: Lời thoại đọc voice tuyệt đối KHÔNG nhắc KOC là AI, avatar ảo hay đang làm affiliate/quảng cáo. CẤM các từ cấm bán hàng: *giỏ hàng, link bio, link affiliate, mua ngay, nhanh tay, voucher, shop...*
2. **Thời lượng linh hoạt (Dynamic Duration)**: Tuyệt đối KHÔNG cố định thời lượng video là 28s. Độ dài video được tính động từ chính trường `duration_seconds` do script trả về sau khi sinh file audio thực tế.
