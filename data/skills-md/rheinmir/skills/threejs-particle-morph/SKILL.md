---
name: threejs-particle-morph
description: >-
  Particle cloud Three.js (THREE.Points + BufferGeometry) hội tụ từ vị trí ngẫu nhiên thành hình
  ảnh/logo theo tiến độ cuộn trang — sample pixel từ canvas ẩn làm toạ độ đích, lerp position theo
  scroll. Gọi khi user nói "particle image", "hạt hội tụ thành ảnh", "three.js particle scroll",
  "point cloud morph", "particle cloud biến hình theo scroll", hoặc /threejs-particle-morph. KHÁC
  `skills/blur` (đó là shader GLSL radial-blur CHUYỂN ẢNH sang ảnh khác trên một plane — đây là
  particle cloud rời rạc BIẾN HÌNH thành ảnh, kỹ thuật render khác hẳn — PointsMaterial/BufferGeometry,
  không phải ShaderMaterial trên PlaneGeometry).
metadata:
  design-standard: "solid-what-how/1"
  contract-version: "1.0.0"
  loop: utils
---

# Skill: threejs-particle-morph

Component Three.js thuần — hàng nghìn particle rải ngẫu nhiên trong không gian 3D, hội tụ dần thành ảnh sample từ pixel khi user cuộn trang, tan rã lại khi cuộn ngược.

## WHAT

### Purpose và context
- **Purpose:** dựng một particle cloud Three.js (`THREE.Points` + `BufferGeometry`) hội tụ từ vị trí ngẫu nhiên thành ảnh/logo theo tiến độ cuộn trang và tan rã lại khi cuộn ngược — ưu tiên copy nguyên bản gốc, bản vanilla trong `assets/` là dự phòng.
- **Trigger (when to use):**
  - Hero section/portfolio cần hiệu ứng "ảnh được ghép lại từ các hạt" khi cuộn tới.
  - User nói "particle image", "hạt hội tụ thành ảnh", "point cloud morph", "three.js particle scroll".
- **Non-goals:** KHÔNG dùng cho hiệu ứng chuyển ảnh liền mạch kiểu zoom-blur (đó là `blur` — shader trên 1 plane, không có particle rời rạc) và KHÔNG dùng cho hiệu ứng cuộn nhẹ không cần WebGL (đó là `scroll-effects`). Không viết lại code gốc của tác giả.

### Mental model
`ảnh nguồn → canvas ẩn (sampleResolution) → getImageData + stride + alphaThreshold → targets (+ màu) · starts random → scroll → targetProgress → progress (damping) → position = lerp(starts, targets, progress) → PointsMaterial render`.

### Input và output contract
| | Field | Required? | Ý nghĩa |
|---|---|---|---|
| In | ảnh/logo nguồn (`imageUrl`) | không | thiếu → demo tự vẽ chữ mẫu lên canvas ẩn để sample |
| In | `particleCount`, `particleSize`, `sampleResolution`, `alphaThreshold` | không | tham số khởi tạo `ParticleMorph` |
| In | ràng buộc dự án (được kéo lib ngoài không?) | có | quyết định bản gốc (mặc định) hay `assets/` vanilla |
| Out | component trong dự án | có | file gốc copy nguyên (giữ comment ghi công) hoặc `assets/demo.*` đã adapt; có `destroy()` |
| Out | bằng chứng verify | có | ảnh chụp progress 0/0.5/1 + console sạch |

### Rules và capabilities
- RULE-01 (MUST): **Hiệu năng**: số particle càng nhiều càng nặng CPU (vòng lặp ghi lại `position` mỗi frame) lẫn GPU. Ngưỡng an toàn gợi ý cho máy tầm trung: **≤ 5.000–10.000 particle**. Đo bằng DevTools Performance/FPS meter TRƯỚC KHI tăng `particleCount`, đừng đoán — nhất là khi thêm particle cho ảnh lớn/nhiều chi tiết (tăng `sampleResolution` cũng tăng chi phí sample lúc `init()`, dù chỉ chạy một lần).
- RULE-02 (MUST): **Ba container** (`three`) phải cài qua **npm** (`npm install three`) và import qua bundler cho production — bản demo dùng `importmap` trỏ CDN (`unpkg.com/three@0.169.0`) CHỈ để chạy độc lập không cần bundler, không dùng bản CDN cũ ghim version như `blur` từng làm. Khi wire vào dự án thật: xoá `<script type="importmap">`, `npm install three`, đổi `import * as THREE from 'three'` sang import qua bundler.
- RULE-03 (SHOULD): `alphaThreshold`/brightness filter trong `_buildSamples()` loại pixel nền trong suốt/tối — ảnh nền trong suốt (PNG logo) cho kết quả gọn hơn ảnh nền đặc (JPEG); ảnh nền đặc sẽ sample luôn cả nền trừ khi crop trước.
- RULE-04 (MUST): Verify bằng `playwright-verify` — chụp ở progress 0/0.5/1 (cuộn tới 3 mốc), đọc console (WebGL context lỗi thường im lặng, không throw JS error rõ ràng).
- RULE-05 (MUST): Bản gốc dùng TRƯỚC — copy nguyên file, đừng viết lại; giữ comment ghi công dòng đầu; chỉ sửa nội dung/ảnh/màu; chạy local qua HTTP, không `file://`.
- Capabilities: đọc/copy asset từ repo ngoài công khai; ghi file front-end vào dự án; chạy trang qua HTTP + trình duyệt headless để chụp/đọc console.

### Failure boundaries
- Không mở được link gốc / không kéo được lib ngoài → dùng `assets/` vanilla (nhánh B01).
- FPS tụt khi tăng `particleCount` → **blocked** việc tăng thêm: đo lại, giữ ≤ 5.000–10.000 particle.
- Console báo lỗi WebGL context (thường im lặng) → **failed** verify, chưa bàn giao.
- Ảnh nền đặc sample cả nền → crop trước hoặc dùng PNG nền trong suốt.

## HOW

### Main workflow
| Step | Type | Inputs | Action | Outputs/exit | Failure/next |
|---|---|---|---|---|---|
| W01 | judgment | ràng buộc dự án | Chọn nguồn: bản gốc `Rheinmir/uiux-asset` (mặc định) hay `assets/` vanilla | nguồn đã chọn | không kéo lib ngoài → B01 |
| W02 | effect | link chạy + code | Mở link **chạy** xem đúng hiệu ứng → copy nguyên file `.html` (+ `_assets/`) vào dự án | file trong dự án, còn comment ghi công | — |
| W03 | effect | file | Chỉ sửa nội dung/ảnh/màu (hoặc `imageUrl`/`particleCount`/`particleSize` với bản vanilla) | component đã adapt | — |
| W04 | deterministic | trang qua HTTP | Verify bằng `playwright-verify`: chụp progress 0/0.5/1, đọc console | 3 ảnh + console sạch | lỗi WebGL/FPS → sửa, lặp W03 |
| W05 | effect | dự án thật | Wire production: xoá importmap, `npm install three`, import qua bundler | build chạy | — |

Chi tiết từng bước (nguồn chân lý cho W01–W05):

#### Bản gốc — dùng TRƯỚC (copy nguyên file, đừng viết lại)
Code gốc NGUYÊN VĂN của tác giả (CodePen public = MIT) nằm ở repo ngoài **`Rheinmir/uiux-asset`** — gallery chạy thật: https://rheinmir.github.io/uiux-asset/scroll-effects/ .
Quy trình: mở link **chạy** để xem đúng hiệu ứng → copy nguyên file `.html` (+ thư mục `_assets/` nếu file trỏ tới) vào dự án → giữ comment ghi công dòng đầu → chỉ sửa nội dung/ảnh/màu. Chạy local qua HTTP, không `file://`.
`git clone --depth 1 https://github.com/Rheinmir/uiux-asset` nếu cần cả bộ offline.

| Pen gốc — tác giả | Link |
|---|---|
| Scroll-Driven Particle WebGL Image Matrix — ycw | [chạy](https://rheinmir.github.io/uiux-asset/scroll-effects/scroll-driven-particle-webgl-image-matrix.html) · [code](https://github.com/Rheinmir/uiux-asset/blob/main/scroll-effects/scroll-driven-particle-webgl-image-matrix.html) |
| GSAP ScrollSmoother and Three.js — cmalven | [chạy](https://rheinmir.github.io/uiux-asset/scroll-effects/gsap-scrollsmoother-and-three-js.html) · [code](https://github.com/Rheinmir/uiux-asset/blob/main/scroll-effects/gsap-scrollsmoother-and-three-js.html) |
| GSAP ScrollTrigger Disintegration Effect — dev_loop | [chạy](https://rheinmir.github.io/uiux-asset/scroll-effects/gsap-scrolltrigger-disintegration-effect.html) · [code](https://github.com/Rheinmir/uiux-asset/blob/main/scroll-effects/gsap-scrolltrigger-disintegration-effect.html) |

`assets/` trong skill này chỉ là bản rút gọn vanilla tự viết — dùng khi dự án KHÔNG được kéo lib ngoài; mặc định dùng bản gốc ở trên.

#### Assets
`assets/demo.html` + `assets/demo.css` + `assets/demo.js` — đọc rồi ADAPT (đổi `imageUrl`, `particleCount`, `particleSize` khi khởi tạo `ParticleMorph`). Demo tự vẽ chữ mẫu lên canvas ẩn để sample khi không truyền `imageUrl`, nên chạy được ngay không cần ảnh/network.

#### Cơ chế
- **Sample ảnh**: vẽ ảnh nguồn (hoặc canvas vẽ tay) lên `<canvas>` ẩn kích thước `sampleResolution`, đọc `getImageData()`. Duyệt pixel theo bước nhảy (`stride` tính từ `particleCount` mong muốn so với tổng pixel) — KHÔNG lấy hết mọi pixel, quá nặng — giữ pixel đủ sáng/không trong suốt (`alphaThreshold`) làm toạ độ đích + màu RGB.
- **Particle**: mỗi toạ độ sample = 1 particle trong `THREE.Points` (`BufferGeometry` attribute `position`). Vị trí khởi tạo (`starts`) random trong một khối không gian lớn ("nổ tung"), vị trí đích (`targets`) là toạ độ pixel đã sample, lưu song song trong hai `Float32Array` riêng (không phải hai attribute GPU).
- **Scroll → progress**: một scroll listener duy nhất, rAF-throttle (không GSAP/ScrollTrigger — bản demo cố tình viết thuần để không trùng phụ thuộc với `gsap-scrolltrigger-pin`), tính `targetProgress` từ `scrollY / (scrollHeight - innerHeight)`.
- **Lerp mỗi frame**: `progress` được làm mượt dần tới `targetProgress` (damping đơn giản, không phải animate trực tiếp `scrollY`), rồi mỗi phần tử `position[i] = lerp(starts[i], targets[i], progress)`, set `geometry.attributes.position.needsUpdate = true`.
- **Màu + kích thước**: `PointsMaterial({ size, sizeAttenuation: true, vertexColors: true })` — giữ màu ảnh gốc qua attribute `color` tĩnh (set một lần lúc build, không đổi theo progress).
- **Cleanup**: viết dạng class có `destroy()` — huỷ `requestAnimationFrame`, gỡ `scroll`/`resize` listener, gọi `geometry.dispose()`, `material.dispose()`, `renderer.dispose()`.

### Branches
| ID | Kind | Guard | Hành vi | Skip / failure | Rejoin |
|---|---|---|---|---|---|
| B01 | conditional_required | dự án KHÔNG được kéo lib ngoài | dùng `assets/demo.html` + `assets/demo.css` + `assets/demo.js`, ADAPT tham số khởi tạo `ParticleMorph` | — | W04 |
| B02 | capability_optional | cần cả bộ offline | `git clone --depth 1 https://github.com/Rheinmir/uiux-asset` | có mạng tới gallery → skip | W02 |

### Validation và stopping
Kiểm bằng chạy thật: `playwright-verify` chụp 3 mốc cuộn + đọc console (WebGL lỗi thường im lặng); hiệu năng đo bằng DevTools Performance/FPS meter, không đoán. Review mắt: ảnh hội tụ đúng hình ở progress 1, tan rã ở 0. Dừng khi 3 ảnh đúng + console sạch.

### Examples
- **Positive:** hero portfolio cần logo PNG hội tụ khi cuộn → copy nguyên `scroll-driven-particle-webgl-image-matrix.html` từ gallery, giữ comment ghi công, đổi ảnh logo → chụp 0/0.5/1 thấy hạt rải → nửa hình → logo đủ, console sạch.
- **Boundary/failure:** dự án cấm lib CDN ngoài → dùng `assets/demo.js`, `particleCount` 30.000 làm FPS tụt → hạ về ≤ 10.000 theo đo, rồi verify lại.
- **Boundary:** user muốn chuyển ảnh A→B kiểu zoom-blur trên một plane → không dùng skill này, chuyển `blur`.

## Origin
