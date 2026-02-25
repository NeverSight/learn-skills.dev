---
name: generate-media
description: 短剧媒体生成技能。根据已生成的单部作品目录，调用 Google Gemini API（单一可配置图片模型生成角色图/分镜图），将生成的图片存放到对应各集目录下。支持视觉风格预设配置。关键词：图片生成、Gemini、Google API、分镜图片、角色参考图、media generation、视觉风格。
---

# 短剧媒体生成技能 (Generate Media)

## 概述

本技能用于将 `produce-anime` 技能生成的作品脚本**转化为实际的参考图片**。生成时会读取作品的视觉风格配置（`visual_style`），将摄影机/镜头/胶片等参数自动注入到 AI 提示词中。当前标准流程：

1. **风格选择**：在生成前，使用 `ask_questions` 工具让用户从 `visual_styles.json` 中选择视觉风格
2. **生成角色参考图**：根据 `character_bible.md` 中每个角色的 `AI绘图关键词`，使用配置图片模型批量生成角色参考图
3. **生成场景四宫格图**：根据 `scenes/scene_bible.md` 中每个场景的 `AI绘图关键词`，生成**一张四宫格合成图**（2×2布局：正面/左45°/右45°/背面），保存为 `{场景ID}_ref.png`
4. **生成道具三视图**：根据 `props/prop_bible.md` 中每个道具的 `AI绘图关键词`，生成**一张三视图合成图**（1×3布局：正面/侧面/俯视），保存为 `{道具ID}_ref.png`
5. **生成分镜图片**：按“两集一批”生成分镜图（每集A/B两张，共最多4张/批），角色一致性由同模型多模态提示保证，9宫格布局（3×3，16:9比例）
6. **维护索引文件**：media_index.json、ref_index.json 等

生成的媒体文件存放到对应各集的 `EP{xx}/` 目录下。

> **注意**：视频由 Seedance 平台生成，不在本技能中处理。分镜图片作为参考图提交到 Seedance。

---

## 前置条件

### 1. API 配置

需要配置 Google Gemini API Key 和 Base URL，从 `/data/dongman/.config/api_keys.json` 读取：

```json
// /data/dongman/.config/api_keys.json
{
  "gemini_api_key": "AIza...",
    "gemini_base_url": "https://generativelanguage.googleapis.com/",
    "gemini_image_model": "gemini-2.5-flash-image-preview"
}
```

**字段说明**：
- `gemini_api_key`：Google Gemini API Key（必填）
- `gemini_base_url`：API 端点地址（可选，留空则使用 SDK 默认值；代理/自定义端点时配置）
- `gemini_image_model`：全局图片模型（必填推荐）
    - 默认：`gemini-2.5-flash-image-preview`
    - 可选：`gemini-3-pro-image-preview`

也支持环境变量覆盖（优先级高于配置文件）：
- `GEMINI_API_KEY`
- `GEMINI_BASE_URL`
- `GEMINI_IMAGE_MODEL`

### 2. Python 依赖

需要安装 Google Generative AI SDK：

```bash
pip install google-genai Pillow requests
```

### 3. 已有作品目录

目标作品目录必须已由 `produce-anime` 技能生成完毕，包含：
- `characters/character_bible.md`（角色设定，含 AI 绘图关键词）
- `scenes/scene_bible.md`（场景设定，含 AI 绘图关键词）——可选，无则跳过场景生成
- `props/prop_bible.md`（道具设定，含 AI 绘图关键词）——可选，无则跳过道具生成
- 各集 `storyboard_config.json`（含 `visual_style` 视觉风格配置）

---

## 执行流程

### 第一步：确定目标作品

1. 如用户指定了作品编号（如 `DM-001`），直接定位到 `/data/dongman/projects/` 下对应目录
2. 如用户未指定，读取 `/data/dongman/projects/index.json`，选择最新的作品
3. 验证目标目录存在且包含 `characters/character_bible.md` 和 `episodes/` 子目录

### 第二步：生成 Python 脚本并执行

在作品目录下生成 `generate_media.py` 脚本，然后执行。脚本逻辑如下：

#### 2.1 脚本结构

```python
#!/usr/bin/env python3
"""
短剧媒体生成脚本
Phase 1: 生成角色参考图
Phase 2: 参考角色图生成分镜图片
"""
import os
import re
import json
import time
import sys
from pathlib import Path

from google import genai
from google.genai import types
from PIL import Image

# ========== 配置 ==========
PROJECT_DIR = Path(__file__).parent
EPISODES_DIR = PROJECT_DIR / "episodes"
CHARACTERS_DIR = PROJECT_DIR / "characters"

# API 配置
def load_api_config():
    """从配置文件和环境变量加载 API Key 和 Base URL"""
    api_key = None
    base_url = None
    
    # 先从配置文件读取
    config_path = Path("/data/dongman/.config/api_keys.json")
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        api_key = config.get("gemini_api_key")
        base_url = config.get("gemini_base_url")
    
    # 环境变量优先覆盖
    api_key = os.environ.get("GEMINI_API_KEY", api_key)
    base_url = os.environ.get("GEMINI_BASE_URL", base_url)
    
    if not api_key:
        raise RuntimeError("未找到 GEMINI_API_KEY，请配置 api_keys.json 或设置环境变量")
    
    return api_key, base_url

api_key, base_url = load_api_config()

# 构建 Client（支持自定义 base_url）
http_options = types.HttpOptions(base_url=base_url) if base_url else None
client = genai.Client(api_key=api_key, http_options=http_options)
print(f"🔑 API 已配置 | Base URL: {base_url or '默认'}")

# ========== Phase 1: 角色参考图生成 ==========

def parse_character_bible(bible_path: str) -> list:
    """解析 character_bible.md，提取角色名和 AI 绘图关键词"""
    with open(bible_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    characters = []
    # 匹配 ### 角色X：名字（英文名）或 ### 角色X：名字
    blocks = re.split(r'### 角色\d+[：:]', content)
    names_pattern = re.findall(r'### 角色\d+[：:]\s*(.+)', content)
    
    for i, block in enumerate(blocks[1:]):  # 跳过第一个空块
        name = names_pattern[i].strip().split('（')[0].strip() if i < len(names_pattern) else f"角色{i+1}"
        
        # 提取 AI 绘图关键词
        prompt_match = re.search(r'AI绘图关键词（英文）[：:]\s*(.+)', block)
        if prompt_match:
            ai_prompt = prompt_match.group(1).strip()
        else:
            continue
        
        characters.append({
            "name": name,
            "ai_prompt": ai_prompt
        })
    
    return characters

def generate_character_ref(char_name: str, char_prompt: str, output_dir: Path):
    """为单个角色生成3张参考图（正面、侧面、表情）"""
    views = [
        {
            "suffix": "front",
            "label": "正面全身",
            "extra": "full body front view, standing pose, white background, character reference sheet style, clear details"
        },
        {
            "suffix": "face",
            "label": "面部特写",
            "extra": "face close-up portrait, front view, white background, detailed facial features, expressive eyes"
        },
        {
            "suffix": "side",
            "label": "侧面半身",
            "extra": "upper body side view, three quarter angle, white background, character reference sheet"
        }
    ]
    
    results = []
    for view in views:
        filename = f"{char_name}_{view['suffix']}.png"
        output_path = output_dir / filename
        
        if output_path.exists():
            print(f"  ⏭️ 角色图已存在，跳过: {filename}")
            results.append(str(output_path))
            continue
        
        full_prompt = f"{char_prompt}, {view['extra']}"
        
        try:
            response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=full_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="3:4",
                    safety_filter_level="BLOCK_ONLY_HIGH",
                    person_generation="ALLOW_ADULT",
                ),
            )
            if response.generated_images:
                response.generated_images[0].image.save(str(output_path))
                print(f"  ✅ 角色{view['label']}图: {filename}")
                results.append(str(output_path))
            else:
                print(f"  ⚠️ 角色{view['label']}图无结果: {filename}")
        except Exception as e:
            print(f"  ❌ 角色{view['label']}图失败: {e}")
        
        time.sleep(2)
    
    return results

def phase1_generate_characters():
    """Phase 1: 生成所有角色参考图"""
    bible_path = CHARACTERS_DIR / "character_bible.md"
    if not bible_path.exists():
        print("❌ character_bible.md 不存在，跳过角色参考图生成")
        return {}
    
    print("\n" + "=" * 60)
    print("🎨 Phase 1: 生成角色参考图")
    print("=" * 60)
    
    characters = parse_character_bible(str(bible_path))
    print(f"📋 发现 {len(characters)} 个角色")
    
    char_ref_map = {}  # name -> [image_paths]
    
    for char in characters:
        print(f"\n👤 生成角色: {char['name']}")
        ref_images = generate_character_ref(char["name"], char["ai_prompt"], CHARACTERS_DIR)
        char_ref_map[char["name"]] = ref_images
    
    # 保存角色参考图索引
    ref_index = {name: paths for name, paths in char_ref_map.items()}
    index_path = CHARACTERS_DIR / "ref_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(ref_index, f, ensure_ascii=False, indent=2)
    print(f"\n📋 角色参考图索引: {index_path}")
    
    return char_ref_map

# ========== Phase 2: 分镜图片生成（参考角色图） ==========

def upload_character_refs(char_ref_map: dict) -> dict:
    """将角色参考图上传到 Gemini，返回 name -> [uploaded_file] 映射"""
    uploaded = {}
    for name, paths in char_ref_map.items():
        files = []
        for p in paths:
            if os.path.exists(p):
                try:
                    f = client.files.upload(file=p)
                    files.append(f)
                except Exception as e:
                    print(f"  ⚠️ 上传 {p} 失败: {e}")
        uploaded[name] = files
    return uploaded

def generate_storyboard_image_with_refs(
    grid_prompt: str,
    grid_characters: list,
    char_uploaded: dict,
    output_path: str
) -> bool:
    """使用 Gemini 原生图片生成（参考角色图生成分镜图）"""
    try:
        # 构建包含角色参考图的 prompt
        # 收集本格涉及的角色参考图
        ref_parts = []
        char_names = []
        for char_info in grid_characters:
            char_name = char_info.get("name", "")
            if char_name and char_name in char_uploaded:
                char_names.append(char_name)
                for uploaded_file in char_uploaded[char_name]:
                    ref_parts.append(uploaded_file)
        
        # 如果有角色参考图，使用 Gemini 多模态生成
        if ref_parts:
            ref_desc = "、".join(char_names)
            combined_prompt = (
                f"Based on these character reference images for {ref_desc}, "
                f"generate a new cinematic scene image: {grid_prompt}. "
                f"Keep the characters' appearance consistent with the reference images. "
                f"16:9 aspect ratio, high quality cinematic style."
            )
            
            contents = []
            for ref_file in ref_parts:
                contents.append(ref_file)
            contents.append(combined_prompt)
            
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )
            
            # 提取生成的图片
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        image = Image.open(io.BytesIO(part.inline_data.data))
                        image.save(output_path)
                        print(f"  ✅ 分镜图（参考角色）: {Path(output_path).name}")
                        return True
        
        # 无角色参考图或 Gemini 生成失败，降级为 Imagen 直接生成
        return generate_image_imagen(grid_prompt, output_path)
    
    except Exception as e:
        print(f"  ⚠️ Gemini 参考生成失败 ({e})，降级为 Imagen...")
        return generate_image_imagen(grid_prompt, output_path)

def generate_image_imagen(prompt: str, output_path: str) -> bool:
    """降级方案：直接使用 Imagen 生成图片（无角色参考）"""
    try:
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="BLOCK_ONLY_HIGH",
                person_generation="ALLOW_ADULT",
            ),
        )
        if response.generated_images:
            response.generated_images[0].image.save(output_path)
            print(f"  ✅ 分镜图（Imagen）: {Path(output_path).name}")
            return True
        else:
            print(f"  ⚠️ Imagen 无结果: {Path(output_path).name}")
            return False
    except Exception as e:
        print(f"  ❌ Imagen 失败: {e}")
        return False

# ========== 逐集处理 ==========

def process_episode(ep_dir: Path, ep_num: str, char_uploaded: dict):
    """处理单集：生成分镜图片（参考角色）"""
    config_path = ep_dir / "storyboard_config.json"
    if not config_path.exists():
        print(f"⚠️ {ep_num}: storyboard_config.json 不存在，跳过")
        return None

    with open(config_path) as f:
        config = json.load(f)

    print(f"\n{'='*50}")
    print(f"📺 处理 {ep_num}: {config.get('episode_title', '未知')}")
    print(f"{'='*50}")

    results = {"images": 0, "failed": 0}

    for part_key, part_label in [("part_a", "上"), ("part_b", "下")]:
        part = config.get(part_key)
        if not part:
            continue

        video_id = part["video_id"]
        print(f"\n--- {part_label}半部分 ({video_id}) ---")

        # 生成6宫格分镜图片（参考角色图）
        grids = part.get("storyboard_9grid", [])
        
        for grid in grids:
            grid_num = grid["grid_number"]
            prompt = grid.get("ai_image_prompt", "")
            if not prompt:
                continue

            img_filename = f"{video_id}_grid{grid_num}.png"
            img_path = str(ep_dir / img_filename)

            if os.path.exists(img_path):
                print(f"  ⏭️ 已存在: {img_filename}")
                results["images"] += 1
                continue

            # 获取本格涉及的角色列表
            grid_characters = grid.get("characters", [])
            
            if grid_characters and char_uploaded:
                # 有角色 → 使用 Gemini 参考角色图生成
                success = generate_storyboard_image_with_refs(
                    prompt, grid_characters, char_uploaded, img_path
                )
            else:
                # 无角色（纯场景） → 直接 Imagen
                success = generate_image_imagen(prompt, img_path)
            
            if success:
                results["images"] += 1
            else:
                results["failed"] += 1

            time.sleep(2)

    return results

# ========== 主流程 ==========

def main():
    import io  # for BytesIO in Gemini image generation
    
    start_ep = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end_ep = int(sys.argv[2]) if len(sys.argv) > 2 else 25
    skip_chars = "--skip-chars" in sys.argv  # 跳过角色生成（已有时）

    print(f"🎬 短剧媒体生成")
    print(f"📁 项目: {PROJECT_DIR}")
    print(f"📺 范围: EP{start_ep:02d} - EP{end_ep:02d}")

    # ===== Phase 1: 角色参考图 =====
    if skip_chars:
        print("\n⏭️ 跳过角色参考图生成（使用已有）")
        ref_index_path = CHARACTERS_DIR / "ref_index.json"
        if ref_index_path.exists():
            with open(ref_index_path) as f:
                char_ref_map = json.load(f)
        else:
            char_ref_map = {}
    else:
        char_ref_map = phase1_generate_characters()

    # ===== 上传角色图到 Gemini =====
    print("\n📤 上传角色参考图到 Gemini...")
    char_uploaded = upload_character_refs(char_ref_map) if char_ref_map else {}
    print(f"   已上传 {sum(len(v) for v in char_uploaded.values())} 张角色参考图")

    # ===== Phase 2: 逐集生成分镜图片 =====
    total = {"images": 0, "failed": 0}
    
    for ep in range(start_ep, end_ep + 1):
        ep_num = f"EP{ep:02d}"
        ep_dir = EPISODES_DIR / ep_num
        if not ep_dir.exists():
            print(f"⚠️ {ep_num} 不存在，跳过")
            continue
        
        result = process_episode(ep_dir, ep_num, char_uploaded)
        if result:
            for k in total:
                total[k] += result[k]

    # ===== 媒体索引 =====
    generate_media_index(start_ep, end_ep)

    print(f"\n{'='*60}")
    print(f"🏁 全部完成!")
    print(f"🎨 角色参考图: {sum(len(v) for v in char_ref_map.values())} 张")
    print(f"🖼️ 分镜图片: {total['images']} 张")
    print(f"❌ 失败: {total['failed']} 个")
    print(f"{'='*60}")

def generate_media_index(start_ep, end_ep):
    """生成媒体文件索引"""
    index = {
        "characters": [],
        "episodes": []
    }
    
    # 角色图索引
    for f in sorted(CHARACTERS_DIR.iterdir()):
        if f.suffix == ".png":
            index["characters"].append({
                "filename": f.name,
                "size_bytes": f.stat().st_size
            })
    
    # 各集媒体索引
    for ep in range(start_ep, end_ep + 1):
        ep_num = f"EP{ep:02d}"
        ep_dir = EPISODES_DIR / ep_num
        if not ep_dir.exists():
            continue
        
        ep_entry = {"episode": ep_num, "files": []}
        for f in sorted(ep_dir.iterdir()):
            if f.suffix in (".png", ".mp4"):
                ep_entry["files"].append({
                    "filename": f.name,
                    "type": "image" if f.suffix == ".png" else "video",
                    "size_bytes": f.stat().st_size
                })
        index["episodes"].append(ep_entry)

    index_path = PROJECT_DIR / "media_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f"\n📋 媒体索引: {index_path}")

if __name__ == "__main__":
    main()
```

### 第三步：执行脚本

运行脚本，支持多种模式：

```bash
# 完整流程：角色参考图 → 分镜图片（全25集）
python3 generate_media.py

# 指定集数范围（如 EP01-EP05）
python3 generate_media.py 1 5

# 跳过角色参考图生成（已有角色图时，直接生成分镜）
python3 generate_media.py 1 25 --skip-chars
```

### 第四步：验证生成结果

脚本执行完成后，验证：
1. `characters/` 目录包含角色参考图（每角色1张：`{角色名}_ref.png`）
2. `scenes/` 目录包含场景四宫格图（每场景1张：`{场景ID}_ref.png`，含4视角合成）
3. `props/` 目录包含道具三视图（每道具1张：`{道具ID}_ref.png`，含3视角合成）
4. 每集目录包含 2 张分镜 PNG（A/B）
5. 各 `ref_index.json` 已生成

---

## 两阶段生成流程详解

### Phase 1: 角色参考图生成（当前标准）

| 步骤 | 说明 |
|------|------|
| 解析 `character_bible.md` | 提取每个角色的名字和 `AI绘图关键词（英文）` |
| 生成方式 | 单次请求多图（最多7张），按角色顺序落盘 |
| 模型 | 单一配置模型：`gemini_image_model` |
| 存放位置 | `characters/{角色名}_ref.png` |
| 索引文件 | `characters/ref_index.json`（角色名 → 图片路径映射） |
| 失败策略 | **不做单张兜底**（返回不足只记失败） |

### Phase 1B: 场景四宫格图生成

| 步骤 | 说明 |
|------|------|
| 解析 `scenes/scene_bible.md` | 提取每个场景的 `场景ID`、`场景名` 和 `AI绘图关键词（英文）` |
| 生成方式 | 每个场景**一次API请求**，生成一张 2×2 四宫格合成图（正面/左45°/右45°/背面） |
| 模型 | 单一配置模型：`gemini_image_model` |
| 提示词结构 | 提示模型在单张图中绘制4格布局，含场景描述 + 视觉风格后缀 |
| 输出 | **每场景1张**：`scenes/{场景ID}_ref.png`（四宫格合成图） |
| 索引文件 | `scenes/ref_index.json`（场景ID → 图片路径映射） |
| 失败策略 | **不做单张兜底**（无返回只记失败） |

### Phase 1C: 道具三视图生成

| 步骤 | 说明 |
|------|------|
| 解析 `props/prop_bible.md` | 提取每个道具的 `道具ID`、`道具名` 和 `AI绘图关键词（英文）` |
| 生成方式 | 每个道具**一次API请求**，生成一张 1×3 三视图合成图（正面/侧面/俯视） |
| 模型 | 单一配置模型：`gemini_image_model` |
| 提示词结构 | 提示模型在单张图中绘制3格横排布局，含道具描述 + 视觉风格后缀 |
| 输出 | **每道具1张**：`props/{道具ID}_ref.png`（三视图合成图） |
| 索引文件 | `props/ref_index.json`（道具ID → 图片路径映射） |
| 失败策略 | **不做单张兜底**（无返回只记失败） |

### Phase 2: 分镜图片生成（当前标准）

| 步骤 | 说明 |
|------|------|
| 生成粒度 | 两集一批（每集A/B两张，共最多4张/请求） |
| 读取配置 | 从每集 `storyboard_config.json` 读取 `storyboard_9grid` 与角色列表 |
| 角色一致性 | 将角色参考图内联到请求中，保持外观一致 |
| 布局 | 3×3 九宫格，16:9比例 |
| 输出文件 | `EPxx/{video_id}_storyboard.png`（每集2张：A/B） |
| 失败策略 | **不做单张兜底**（返回不足只记失败） |

> **视频生成**：由 Seedance 平台处理。分镜图片和角色参考图作为 `referenceFiles` 提交到 Seedance，由其生成最终视频。

---

## 生成文件命名规则

### 角色参考图

```
characters/
├── character_bible.md           # 角色设定（原有）
├── ref_index.json               # 角色参考图索引（生成）
├── 林策_ref.png
├── 沈璃_ref.png
├── 祁远_ref.png
└── ...
```

### 场景四宫格图（每场景1张合成图）

```
scenes/
├── scene_bible.md               # 场景设定（原有）
├── ref_index.json               # 场景参考图索引（生成）
├── scene_01_ref.png             # 四宫格合成图（正面/左45°/右45°/背面）
├── scene_02_ref.png
└── ...
```

### 道具三视图（每道具1张合成图）

```
props/
├── prop_bible.md                # 道具设定（原有）
├── ref_index.json               # 道具参考图索引（生成）
├── prop_01_ref.png              # 三视图合成图（正面/侧面/俯视）
├── prop_02_ref.png
└── ...
```

### 分镜图片

分镜图片命名格式：`{视频编号}_storyboard.png`

```
EP01/
├── DM-001-EP01-A_storyboard.png # 上半部分分镜图
├── DM-001-EP01-B_storyboard.png # 下半部分分镜图
├── dialogue.md                 # 对话脚本（原有）
├── storyboard_config.json      # 故事板配置（原有）
└── seedance_tasks.json         # Seedance提交任务（原有）
```

### 各文件说明

| 文件类型 | 数量/集 | 来源 | 格式 |
|---------|---------|------|------|
| 分镜图片 | 2张（A/B各1张） | `storyboard_6grid` + 批量提示词 | PNG |

### 全作品统计（以3个主角、4个场景、3个道具为例）

| 指标 | 数量 |
|------|------|
| 角色参考图 | 3张（3角色 × 1张，含四宫格多视角） |
| 场景四宫格图 | 4张（4场景 × 1张合成图） |
| 道具三视图 | 3张（3道具 × 1张合成图） |
| 总集数 | 25 |
| 每集分镜图片 | 2张 |
| **总分镜图片** | **50张** |
| **总媒体文件** | **60个**（3角色 + 4场景 + 3道具 + 50分镜） |

---

## Google API 模型说明

### 图片模型（统一配置）

- **配置项**：`gemini_image_model`
- **允许值**：
    - `gemini-2.5-flash-image-preview`（默认推荐）
    - `gemini-3-pro-image-preview`（可选）
- **用途**：
    - Phase 1 角色参考图批量生成
    - Phase 2 分镜图批量生成
- **约束**：全流程只使用这一个图片模型，不混用其他图片模型

---

## API 限流与容错

### 限流策略
- 每次图片生成后 **暂停 2 秒**

### 容错机制
1. **跳过已存在文件**：如文件已存在则跳过，支持断点续传
2. **单个失败不影响全局**：某格/某集失败后继续处理下一个
3. **集数范围可指定**：支持只生成指定范围的集数，方便重试

### 重试示例

```bash
# 只重新生成第3集
python3 generate_media.py 3 3

# 重新生成第10-15集
python3 generate_media.py 10 15
```

如果某个文件需要重新生成，手动删除该文件后重新运行脚本即可。

---

## 运行指令

用户可以通过以下方式触发本技能：
- "生成分镜图片"
- "generate media"
- "生成短剧媒体"
- "调用API生成图片"
- "把分镜变成图片"
- "执行媒体生成"

可附带参数：
- **作品编号**：如 "生成 DM-001 的图片"
- **集数范围**：如 "生成第1到第5集的图片"
- **仅角色图**：`--only-chars`
- **跳过角色图**：`--skip-chars`

---

## 执行检查清单

- [ ] 确认 `GEMINI_API_KEY` 已配置（环境变量或配置文件）
- [ ] 确认 `google-genai`、`Pillow`、`requests` 已安装
- [ ] 确认 `gemini_image_model` 已配置且合法
- [ ] 确认目标作品目录存在且 `character_bible.md` 和 `storyboard_config.json` 完整
- [ ] 生成 `generate_media.py` 脚本到作品目录
- [ ] **风格选择**：已通过 `ask_questions` 让用户选择视觉风格
- [ ] **Phase 1**：角色参考图已生成到 `characters/` 目录
- [ ] **Phase 1B**：场景四宫格图已生成到 `scenes/` 目录（每场景1张 `{场景ID}_ref.png`）
- [ ] **Phase 1C**：道具三视图已生成到 `props/` 目录（每道具1张 `{道具ID}_ref.png`）
- [ ] **Phase 2**：分镜图片已生成且参考了角色外观
- [ ] 每集 `seedance_tasks.json` 已存在（2条任务：Part-A/B）
- [ ] 验证 `characters/ref_index.json` 已生成
- [ ] 验证每集目录包含 2 张分镜 PNG（A/B）
- [ ] 验证 `media_index.json` 已生成
- [ ] 检查是否有失败项需要重试

---

## 输出示例

生成完成后，向用户报告：

```
✅ 短剧媒体生成完成！

📋 作品信息
- 作品编号：DM-001
- 作品名称：《灯火归途》
- 视觉风格：Dark Thriller（暗黑悬疑）

📁 项目目录：/data/dongman/projects/DM-001_dhgt/

📊 生成统计
🎨 Phase 1 - 角色参考图
    - 林策_ref.png, 沈璃_ref.png, 祁远_ref.png
    - 小计: 3 张

🏙️ Phase 1B - 场景四宫格图
    - scene_01_ref.png (办公室): 四宫格合成图
    - scene_02_ref.png (车间): 四宫格合成图
    - 小计: 2 张（每张含4视角）

🔧 Phase 1C - 道具三视图
    - prop_01_ref.png (画作): 三视图合成图
    - 小计: 1 张（每张含3视角）

🖼️ Phase 2 - 分镜图片（参考角色）
    - 50 张（25集 × A/B各1张）

❌ 失败: 0 个

📂 文件结构
characters/
├── 林策_ref.png
├── ref_index.json

scenes/
├── scene_01_ref.png              # 四宫格合成图
├── scene_02_ref.png
├── ref_index.json

props/
├── prop_01_ref.png               # 三视图合成图
├── ref_index.json

EP01/
├── DM-001-EP01-A_storyboard.png
├── DM-001-EP01-B_storyboard.png
├── dialogue.md
└── storyboard_config.json

📋 媒体索引：media_index.json

💡 提示：使用 submit_project.py 提交任务到 Seedance 生成视频
```
