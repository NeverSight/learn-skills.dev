---
name: meishe-server-end-json-generate
description: Generate compact cloud-rendering business JSON for backend Meishe synthesis from video, audio, caption, sticker, visual/audio effect, mask, transition, beauty, makeup, AR-prop, and crop requirements. Build and validate a timelines/timeline XML project as an intermediate state, and output XML only when explicitly requested. Also validate, repair, or convert existing backend-synthesis XML. Use for 云端合成 JSON、后端合成 JSON、云剪 XML 转 JSON、云剪辑工程 XML 校验修复、蒙版或区域效果，以及内建或资源包特效相关请求。不支持业务 JSON 转 XML、无损节点 JSON、前端宽松规范、interactpro、主题模板、交换 XML 或其他 XML 方言。
---

# 美摄服务端视频合成json生成

## 执行边界

1. 默认交付云端合成业务 JSON。先构建并校验根节点为 `<timelines>`、子节点为 `<timeline>` 的后端合成工程 XML，XML 仅作为中间状态；只有用户明确要求生成或保留 XML 时才把 XML 作为交付文件。
2. 不虚构素材路径、真实云资源 ID、包 UUID、字体文件、工程 URL 或业务时间点。生产必需值缺失时列出缺项；只有用户明确要求示例或模板时才使用显眼占位值。
3. `video.isTimelineClip=true` 时必须显式写 `path=""` 并包含唯一直接子 `<timeline>`；生成、修复、校验和 XML→JSON 都不得为该空路径补造 URL、本地路径或占位内容。
4. 把 references 作为领域知识唯一来源。SKILL.md 只规定资料路由和执行流程；不要凭记忆补充字段、默认值、参数、公式或映射。
5. 把确定性处理交给 `scripts/editor_xml.py`。不要手算裁剪、手写业务 JSON 或绕过脚本校验。

## Reference 路由

除“SDK 内建参数”先经过总索引一次外，只从本节直接打开任务命中的文件和章节，不先读取全部 references，也不要把 reference 内链接当作必须继续追踪的下一层。资料冲突时按“专项文档 > 当前协议 > 当前特效资料 > SDK 内建参数”处理并说明差异。

### 工程 XML

| 请求特征 | 直接读取 |
| --- | --- |
| 任意生成、校验或修复；根节点、时间线、资产、轨道、视频、音频 | [工程协议：基础结构与媒体](references/工程协议-基础结构与媒体.md) 的目标标签章节 |
| `videoFx/audioFx/transition/fxParam/keyFrame/objectValue`、挂载位置或特效顺序 | [工程协议：特效与参数](references/工程协议-特效与参数.md) 和 [效果：公共规则](references/效果-公共规则.md) |
| 字幕、富文本、组合字幕、贴纸或唱词结构 | [工程协议：字幕贴纸与唱词](references/工程协议-字幕贴纸与唱词.md) 和 [效果：字幕与贴纸](references/效果-字幕与贴纸.md) |
| 完整工程示例、生成检查、错误排查或协议维护依据 | [工程协议：示例校验与维护](references/工程协议-示例校验与维护.md)；只有确需效果完整示例或兼容排查时再读 [效果：示例兼容与验收](references/效果-示例兼容与验收.md) |
| 视觉特效、美颜、美型、美妆或 AR 道具 | [效果：公共规则](references/效果-公共规则.md)、[效果：视觉与人物](references/效果-视觉与人物.md) 和 [工程协议：特效与参数](references/工程协议-特效与参数.md) |
| 裁剪生成、校验、修复或带裁剪的 XML→JSON | [裁剪逻辑说明](references/裁剪逻辑说明.md)、[效果：裁剪](references/效果-裁剪.md)、[工程协议：特效与参数](references/工程协议-特效与参数.md)；涉及视图或方位时再读坐标文档 |
| 蒙版载体、效果类型、公共属性或最小结构 | [蒙版：载体与效果](references/蒙版-载体与效果.md)、[蒙版：区域结构与 XML](references/蒙版-区域结构与XML.md) 和 [工程协议：特效与参数](references/工程协议-特效与参数.md) |
| 蒙版位置、尺寸、形状、羽化或效果强度 | [蒙版：坐标与形状](references/蒙版-坐标与形状.md) 和 [视图坐标与时间线坐标转换关系](references/美摄云剪辑视图坐标与时间线坐标转换关系.md)；raw 视频蒙版再读 [视频局部归一化参考框计算说明](references/视频局部归一化参考框计算说明.md) |
| 文字蒙版、蒙版关键帧、旧结构修复或验收 | [蒙版：文字与关键帧](references/蒙版-文字与关键帧.md) 和 [蒙版：兼容与验收](references/蒙版-兼容与验收.md) |
| 音频特效或视频转场 | [效果：公共规则](references/效果-公共规则.md)、[效果：音频与转场](references/效果-音频与转场.md) 和 [工程协议：特效与参数](references/工程协议-特效与参数.md) |
| 位置、平移、锚点、边界、顶点、遮罩、区域对象或方向描述 | [视图坐标与时间线坐标转换关系](references/美摄云剪辑视图坐标与时间线坐标转换关系.md) |
| 生成/修改字幕字体，或明确检查字体与 `<assets>` 映射 | [字体映射与 XML Asset 生成说明](references/字体映射与XML资产生成说明.md) 和 [systemFonts.json](assets/systemFonts.json) |

纯 XML 校验、修复和 XML→JSON 不读取字体资料，除非用户明确要求检查字体映射。

### XML 转业务 JSON

| XML 内容或目的 | 直接读取 |
| --- | --- |
| 任意 XML→JSON | [XML→JSON：边界与通用规则](references/XML转JSON-边界与通用规则.md) |
| 时间线、资产、视频轨、视频片段 | [XML→JSON：工程与媒体](references/XML转JSON-工程与媒体.md) |
| 视觉/音频特效、参数、关键帧、转场、时间线特效 | [XML→JSON：特效与音频](references/XML转JSON-特效与音频.md) |
| 字幕、富文本、组合字幕、贴纸、唱词、水印 | [XML→JSON：字幕贴纸与唱词](references/XML转JSON-字幕贴纸与唱词.md) |
| 最小示例、验收、官方不一致或维护 | [XML→JSON：示例校验与维护](references/XML转JSON-示例校验与维护.md) |

### SDK 内建参数

仅当当前协议和主题效果资料没有覆盖目标 SDK 内建参数时，读取 [内建特效参数索引](references/内建特效参数索引.md)。已知特效名称时，先在索引中定位，再只打开对应的 `references/effects/` 单特效文件。只知道参数名称时运行：

```powershell
rg -n -g "*.md" "目标参数名" "references/effects"
```

只打开命中文件；条目按索引中的原始分类和顺序保留，不合并参数。

## 大型 reference 的定向检索

不要完整读取超过 10k 中英文混合估算词元的文件。直接运行最接近请求的检索；把“目标标签”“目标属性”替换为用户给出的精确名称：

```powershell
rg -n "^## |完整 XML|兼容|常见问题|验收|源码|目标标签|目标属性" "references/效果-示例兼容与验收.md"
```

## 工作流

### 生成业务 JSON（默认）

1. 按路由只读取相关主题章节，把用户输入规范化为协议数据；缺少 reference 明确要求的输入时停止并列出缺项，不猜测。
2. 根据协议构建候选中间 XML。用户表述存在对象、资源类型、包目标、坐标系或字体映射歧义时，执行对应 reference 的停止条件，确认后再继续。
3. 涉及裁剪时，先按裁剪专项文档准备 JSON 输入，再运行：

   ```powershell
   python scripts/editor_xml.py crop-params INPUT.json -o OUTPUT.json
   ```

   只把脚本结果写入 reference 指定的 XML 对象；输入 JSON 不是业务 JSON，也不构成 JSON→XML 支持。
4. 涉及蒙版时，先确定载体、效果与形状；视频同时存在 Crop 时先完成上一步，再准备蒙版 JSON 并运行：

   ```powershell
   python scripts/editor_xml.py mask-params INPUT.json -o OUTPUT.json
   ```

   `referenceBox` 与视频专用 `videoReference` 二选一，只用于预览位置转换。非文字视频蒙版必须另外提供当前视频原始宽高 `geometryReference`；时间线特效和字幕由脚本使用 `timeline.width/height`。不得从 Stage、Crop、填充模式、property 或 `videoReference.source` 推断视频几何尺寸，也不得手算区域点、文字 storyboard 或关键帧时间换算。只把脚本返回的 carrier attributes、`fxParams` 和 `keyFrames` 合并到目标载体，不覆盖其无关字段。
5. 把候选 XML 写入临时文件并运行：

   ```powershell
   python scripts/editor_xml.py validate CANDIDATE.xml
   ```

6. 修复全部 error 后重新校验。逐条说明 warning；不要把素材可达性、资源包安装状态或编码器能力描述为已验证。
7. 只有退出码为 `0` 时才运行 `python scripts/editor_xml.py xml-to-json CANDIDATE.xml -o OUTPUT.json`。用户未指定文件名时使用 `云端合成.json`；默认不交付中间 XML。

### 明确要求生成 XML

沿用默认流程构建并校验中间 XML，但不执行 XML→JSON。只有校验退出码为 `0` 时才用 `validate --output` 写出 XML；用户未指定文件名时使用 `云剪辑工程.xml`。用户同时要求 JSON 和 XML 时，两者都交付，并保证 JSON 由同一份已通过校验的 XML 转换得到。

### 校验或修复 XML

1. 保留原文件，先运行只读校验，不直接覆盖。
2. 只修复 reference 允许且能从现有结构唯一推导的内容；不得补造路径、ID、包、参数、文本、输出规格或业务时间点。
3. 修改后运行完整校验。只有零 error 才输出“符合规范”并写目标文件。

```powershell
python scripts/editor_xml.py validate INPUT.xml
python scripts/editor_xml.py validate INPUT.xml --report-json REPORT.json
python scripts/editor_xml.py validate INPUT.xml --output VALIDATED.xml
```

退出码：`0` 为无 error，`1` 为协议校验失败，`2` 为命令、文件、JSON 或 XML 无法读取。

### XML 转业务 JSON

1. 按 XML 中实际存在的对象读取对应 JSON 主题文件，不加载无关对象映射。
2. 先完成后端工程校验，再运行：

   ```powershell
   python scripts/editor_xml.py xml-to-json INPUT.xml -o OUTPUT.json
   ```

3. 有 error 时不写 JSON。带裁剪的请求先通过 `crop-params` 生成临时工程 XML，零 error 后再转换；不得直接手写裁剪业务 JSON。
4. 内嵌时间线视频必须把 `path=""`、`isTimelineClip=true` 和唯一直接子 `<timeline>` 作为一组成组结构；转换结果保留 `path: ""`、boolean 标志，并把子节点递归映射为单个 `timeline` 对象。
5. 遇到业务 JSON→XML、无损节点 JSON 或无损往返请求时说明不支持，不用其他格式近似实现。

## 安全与交付

- 拒绝包含 DTD 或实体声明的 XML，不解析外部实体。
- 不联网探测素材地址，不宣称包已安装、服务可用或编码器可用。
- 不因校验或转换请求修改应用源码、源资料、Git 暂存状态或原始输入文件。
- 最终答复列出生成文件、后端工程约束、error/warning 数量和仍需环境确认的事项。

## 技能维护与升级

把 `doc/` 下的所有文件视为只读原始资料。升级时只从 `doc/skill-references/` 读取；集成在 NvBsWeb 时，可读取其 `doc/editor-xml/skill-references/`。不得在 `doc/` 中拆分、规范化、添加目录、删除或回写文件，所有整理结果只写入本技能的 `references/`。

维护 references 时沿用本节的主题边界和直接路由，避免重复知识。普通 reference 必须由 SKILL.md 直接路由；`references/effects/` 中的单特效文件只允许通过 `内建特效参数索引.md` 路由，不得继续嵌套。

每次升级都以只读的 `doc/skill-references/内建特效参数索引.md` 和 `doc/skill-references/effects/` 为输入，完整镜像总索引和单特效文件。公共参数只保留在总索引中；单特效文件按索引中的四个原始分类、原始名称和顺序保留，并移除源目录已删除的旧文件。不得创建快速导航区块或 references 优化脚本。更新后验证 SKILL.md 不超过 500 行、索引与单文件一一对应，并运行 `scripts/editor_xml.py` 的核心回归检查。
