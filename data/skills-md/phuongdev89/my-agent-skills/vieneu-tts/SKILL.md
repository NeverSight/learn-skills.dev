---
name: vieneu-tts
description: Generate high-fidelity on-device Vietnamese text-to-speech with VieNeu-TTS (v3 Turbo, 48kHz). Use when creating offline/local Vietnamese voiceovers, performing instant voice cloning from reference audio (3-8s), inserting emotion tags ([cười], [thở dài]), or when user requests VieNeu-TTS.
---

# VieNeu-TTS (Vietnamese On-Device Neural TTS)

**VieNeu-TTS** (phát triển bởi Phạm Nguyễn Ngọc Bảo — [pnnbao97/VieNeu-TTS](https://github.com/pnnbao97/VieNeu-TTS)) là thế hệ mô hình Text-to-Speech tiếng Việt hiện đại nhất chạy **hoàn toàn cục bộ (on-device)**:
- **Chất lượng âm thanh 48 kHz** (kiến trúc mới v3 Turbo, codec MOSS-Audio-Tokenizer-Nano và bộ phiên âm `sea-g2p`).
- **Tốc độ cực nhanh**: Chạy mượt trên CPU qua ONNX Runtime (RTF ≈ 0.5, không phụ thuộc PyTorch) và siêu tốc trên GPU CUDA (RTF ≈ 0.02 batched).
- **Clone giọng tức thì (Instant Voice Cloning)**: Tái tạo chính xác giọng nói bất kỳ chỉ từ một đoạn audio mẫu ngắn 3–8 giây, tự động khử nhiễu nền (`denoise=True`).
- **Tag cảm xúc trực tiếp**: Hỗ trợ chèn biểu cảm vào lời thoại như `[cười]`, `[thở dài]`, `[hắng giọng]`.
- **Hơn 23 giọng dựng sẵn** phủ khắp 3 miền Bắc, Trung, Nam.

## Quy Chuẩn Bắt Buộc Về Thư Mục Phiên Làm Việc (Session Dir)

> [!IMPORTANT]
> **QUY TẮC CÔ LẬP DỮ LIỆU & BẢO VỆ MÃ NGUỒN**:
> Tuyệt đối **KHÔNG** xả file âm thanh, file clone giọng hoặc script test trực tiếp ra thư mục gốc repo hoặc `04_canh/` bừa bãi. Mọi tài nguyên vào/ra của VieNeu-TTS phải được cô lập trong thư mục session chuẩn hóa.

- **Thư mục gốc:** `./.scratch/`
- **Cú pháp đặt tên:** `./.scratch/yyyy-mm-dd_vieneu-tts_công-việc-viết-không-dấu`
  - Ví dụ: `./.scratch/2026-09-22_vieneu-tts_clone-giong-koc-doan-trang`
- **Cấu trúc phân vùng thư mục con bắt buộc:**
  ```text
  ./.scratch/yyyy-mm-dd_vieneu-tts_công-việc-viết-không-dấu/
  ├── input/      # Chứa file audio mẫu KOC (`koc_voice_sample_5s.wav`) và file kịch bản (`voice_segment.txt`)
  ├── output/     # Chứa file âm thanh chất lượng cao 48kHz xuất xưởng (`voiceover.wav`, `S01_audio.wav`)
  ├── scripts/    # Chứa script phụ trợ / batch synthesizer của session (tuyệt đối không sửa src/)
  └── temp/       # Chứa audio cache, dữ liệu trung gian trước khi denoise/chuẩn hóa
  ```
- **Tự động phân phối tài nguyên bằng tham số `--session-dir`:**
  - Script `generate_voice.py` hỗ trợ tham số `--session-dir <đường_dẫn_session>`.
  - Khi có `--session-dir` và không truyền `--output`, script tự động xuất file âm thanh vào `<session_dir>/output/voiceover.wav`.
  - Hoặc có thể truyền rõ `--output <session_dir>/output/<tên_file>.wav`.

---

## 1. Hướng dẫn Kiểm tra & Cài đặt Tự động (Dành cho Agent)

**VieNeu-TTS là một thư viện Python độc lập (`vieneu`), KHÔNG CẦN clone repo hay giữ thư mục dự án `VieNeu-TTS` đi kèm:**
- Khi nhận yêu cầu tạo giọng đọc qua VieNeu-TTS, Agent thực hiện kiểm tra và cài đặt theo quy trình 2 bước sau:

### Bước 1: Kiểm tra môi trường
```bash
python -c "import vieneu"
```
- Nếu lệnh chạy thành công (exit code 0): Thư viện đã sẵn sàng sử dụng.
- Nếu xuất hiện `ModuleNotFoundError: No module named 'vieneu'`: Tiến hành Bước 2.

### Bước 2: Cài đặt tự động vào môi trường hiện tại
```bash
# Cho CPU (chạy ONNX Runtime cực nhẹ, tối ưu, không cần GPU, không cần PyTorch):
pip install vieneu

# Hoặc cho máy có GPU NVIDIA CUDA (nếu cần tốc độ batch siêu tốc):
pip install "vieneu[cuda]"
```
*Lưu ý:* Khi chạy lần đầu tiên, thư viện tự động tải trọng số mô hình (`pnnbao-ump/VieNeu-TTS-v3-Turbo`) về thư mục cache Hugging Face (`~/.cache/huggingface/hub/`), sau đó hoạt động offline hoàn toàn.

---

## 2. Tiện ích Thực thi Có Sẵn Trong Skill (`scripts/generate_voice.py`)

Skill cung cấp sẵn script CLI thực thi hoàn chỉnh tại:
[`scripts/generate_voice.py`](scripts/generate_voice.py)

Agent có thể chạy trực tiếp bằng dòng lệnh mà không cần phải viết code Python trung gian:

```bash
# Thiết lập biến session_dir chuẩn hóa
SESSION_DIR="./.scratch/2026-09-22_vieneu-tts_clone-giong-koc-doan-trang"
```

### A. Sinh giọng đọc từ văn bản trực tiếp (Tự động xuất vào session_dir/output/)
```bash
python .agents/skills/vieneu-tts/scripts/generate_voice.py \
  --text "Chào bạn! Đây là giọng đọc thử nghiệm của Đoan Trang nhé [cười]." \
  --voice "Đoan Trang" \
  --session-dir "$SESSION_DIR"
```

### B. Sinh giọng đọc từ file kịch bản trong input/ (Chỉ định rõ file trong output/)
```bash
python .agents/skills/vieneu-tts/scripts/generate_voice.py \
  --text-file "$SESSION_DIR/input/voice_segment.txt" \
  --voice "Đoan Trang" \
  --session-dir "$SESSION_DIR" \
  --output "$SESSION_DIR/output/S01_audio.wav"
```

### C. Nhân bản giọng nói (Instant Voice Cloning) từ audio mẫu KOC trong input/
```bash
python .agents/skills/vieneu-tts/scripts/generate_voice.py \
  --text "Trời ơi, cái chất vải này nó mịn dã man luôn đó mọi người!" \
  --ref-audio "$SESSION_DIR/input/koc_voice_sample_5s.wav" \
  --session-dir "$SESSION_DIR" \
  --output "$SESSION_DIR/output/S01_audio.wav"
```

### D. Liệt kê toàn bộ 25 giọng dựng sẵn
```bash
python .agents/skills/vieneu-tts/scripts/generate_voice.py --list-voices
```

### Định dạng đầu ra (JSON Output)
Script trả về kết quả JSON chuẩn giúp Agent đối soát thời lượng thực tế (`duration_seconds`):
```json
{
  "status": "success",
  "mode": "preset_voice",
  "voice": "Đoan Trang",
  "output_file": "<session_dir>/output/voiceover.wav",
  "duration_seconds": 4.4,
  "sample_rate": 48000,
  "file_size_bytes": 422444
}
```

---

## 3. Giọng dựng sẵn (Preset Voices) Phổ biến

VieNeu-TTS v3 Turbo tích hợp sẵn các giọng đọc chuẩn không cần audio mẫu:

| Khu vực | Tên giọng (voice) | Đặc điểm |
| :--- | :--- | :--- |
| **Miền Bắc** | **`Minh Quân`** *(Mặc định)* | Giọng nam Hà Nội truyền cảm, tự nhiên, chuẩn tin tức / podcast |
| | **`Đoan Trang`** | Giọng nữ ấm áp, thanh lịch, KOC review |
| | **`Ngọc Huyền`** | Giọng nữ Hà Nội chuẩn, rõ ràng, phong cách kể chuyện |
| | **`Mai Anh`** | Giọng nữ trẻ trung, năng động, hợp Shorts/TikTok |
| | **`Phạm Tuyên`**, **`Minh Đức`**, **`Mạnh Dũng`** | Giọng nam đa dạng từ trầm ấm đến phóng khoáng |
| **Miền Nam** | **`Thái Sơn`**, **`Mỹ Duyên`**, **`Thùy Dung`** | Giọng miền Nam nhẹ nhàng, tự nhiên, gần gũi |
| **Miền Trung** | **`Quang Sơn`**, **`Ngọc Trân`** | Giọng miền Trung dịu dàng, sâu lắng |

*Có thể liệt kê toàn bộ giọng bằng `vieneu.list_preset_voices()`.*

---

## 4. Tích hợp trong Pipeline `idea_to_video_v2`

Dự án tích hợp VieNeu-TTS thông qua [`src/adapters/voice_adapter.py`](file:///d:/Affiliate/04_Tools/idea_to_video_v2%20-%20gemini/src/adapters/voice_adapter.py) và script [`scratch/voice_helper.py`](file:///d:/Affiliate/04_Tools/idea_to_video_v2%20-%20gemini/.scratch/voice_helper.py):

### Chạy qua CLI Runner / Voice Helper:
```bash
python scratch/voice_helper.py --engine vieneu --project-dir "$SESSION_DIR" --koc "<ten_koc>"
```
- **KOC mapping**:
  - `thu_trang` / `phuong` → Ánh xạ giọng `Đoan Trang`
  - `nhu_ngoc` → Ánh xạ giọng `Ngọc Huyền`
- File âm thanh đầu ra: `<session_dir>/output/voiceover.wav` (hoặc từng scene `S0X_audio.wav` trong `output/`).

---

## 5. Sử dụng Trực tiếp qua Python SDK (`vieneu`)

### A. Tạo giọng đọc cơ bản (Giọng dựng sẵn)
```python
from pathlib import Path
from vieneu import Vieneu

# Khởi tạo (tự nhận diện GPU PyTorch hoặc CPU ONNX)
vieneu = Vieneu()

session_dir = Path("./.scratch/2026-09-22_vieneu-tts_clone-giong-koc-doan-trang")
(session_dir / "output").mkdir(parents=True, exist_ok=True)

text = "Chào các bạn! Hôm nay mình sẽ chia sẻ cảm nhận thực tế về bộ sưu tập mới này nhé [cười]."

# Suy luận giọng nói
audio = vieneu.infer(
    text=text,
    voice="Đoan Trang",  # Hoặc "Minh Quân", "Mai Anh"...
)

# Lưu file WAV chất lượng 48kHz vào session output/ (không lưu vào root)
vieneu.save(audio, str(session_dir / "output" / "voiceover.wav"))
```

### B. Nhân bản giọng nói tức thì (Instant Voice Cloning)
Chỉ cần cung cấp một file âm thanh mẫu từ 3 đến 8 giây của KOC đặt trong `input/`:
```python
from pathlib import Path
from vieneu import Vieneu

vieneu = Vieneu()
session_dir = Path("./.scratch/2026-09-22_vieneu-tts_clone-giong-koc-doan-trang")

audio = vieneu.infer(
    text="Trời ơi, cái chất vải này nó mịn dã man luôn đó mọi người!",
    ref_audio=str(session_dir / "input" / "koc_sample_3_to_8s.wav"),  # Clip mẫu của KOC trong input/
    denoise=True,                                                      # Tự động lọc sạch tạp âm nền
)
vieneu.save(audio, str(session_dir / "output" / "cloned_koc_voice.wav"))
```

Nếu muốn tái sử dụng giọng clone nhiều lần trong session:
```python
# Đăng ký hồ sơ giọng một lần từ file input
vieneu.add_voice("KOC_Thu_Trang", str(session_dir / "input" / "thu_trang_sample.wav"))

# Sử dụng như giọng dựng sẵn
audio = vieneu.infer("Lời thoại cảnh 1...", voice="KOC_Thu_Trang")
vieneu.save(audio, str(session_dir / "output" / "scene_01.wav"))
```

### C. Sinh âm thanh theo lô (Batch Processing)
Tối ưu tốc độ khi render giọng cho toàn bộ các phân cảnh trong kịch bản:
```python
texts = [
    "Cảnh 1: Chiếc áo này thiết kế phom rộng cực kỳ tôn dáng.",
    "Cảnh 2: Từng đường may đều được hoàn thiện rất tỉ mỉ.",
    "Cảnh 3: Phối cùng chân váy hay quần jeans đều xinh nha."
]

# Xử lý đồng thời trong 1 lần forward (siêu tốc trên GPU)
audios = vieneu.infer_batch(texts, voice="Đoan Trang")

for i, a in enumerate(audios):
    vieneu.save(a, str(session_dir / "output" / f"scene_{i+1}.wav"))
```

---

## 6. Các Lưu ý Kỹ thuật Quan trọng

1. **Tag cảm xúc (Emotion cues)**:
   - Chèn trực tiếp vào chuỗi văn bản: `[cười]`, `[thở dài]`, `[hắng giọng]`.
   - Giúp KOC biểu cảm tự nhiên, không bị đều đều như máy đọc tin tức.
2. **Tham số `style` đã bỏ (Deprecated)**:
   - Trên v3 Turbo, phong cách đọc đi theo trực tiếp reference giọng (giọng mẫu hoặc preset), mô hình luôn đọc theo ngữ điệu tự nhiên. Không cần truyền tham số `style`.
3. **Quy tắc KOC**:
   - Lời thoại tạo ra qua VieNeu-TTS phải tuân thủ nghiêm ngặt quy tắc tại [AGENTS.md](file:///d:/Affiliate/04_Tools/idea_to_video_v2%20-%20gemini/AGENTS.md): Tuyệt đối không để KOC tự xưng là AI/người ảo, không chứa mã SKU, không chứa các từ khóa bán hàng thô thiển (`giỏ hàng`, `mua ngay`, `voucher`...).
