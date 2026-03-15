---
name: zhy-markdown2wechat
description: Use when converting Markdown into WeChat-compatible inline HTML with theme styles for preview, copy-paste, or downstream draft publishing.
---

## 概述
这是一个用于将标准的 Markdown 文本，转换成能够直接复制粘贴给微信公众号文章编辑器的 HTML 文件的 Skill。微信公众号的 HTML 结构要求所有样式必须是内联的（Inline CSS）。

此 Skill 的核心优势是 **零部署**。只要用户的环境中安装了 Node.js，即可通过执行本 Skill 自带的转换脚本极其轻量地完成转换任务，它会自动在临时目录加载所需依赖并在完成后清理，不留任何环境垃圾，无需用户预先执行 `npm install`。

## 适用场景
当用户希望你：
- 把 md、markdown 格式的文件转为微信公众号文章。
- 根据 Markdown 生成带 CSS 样式的公众号排版 HTML。

## 详细执行步骤
当你收到用户的转换请求时，如果不指定主题，默认使用 `resources/themes/default.css`。

请你**直接**代用户执行以下命令，调用本 Skill 自带的 `scripts/convert.js`。如果你在使用工具（例如 Terminal / run_command），请直接调用即可。

### 执行转换脚本
使用 `node` 执行转换：
```bash
node <当前skill路径>/scripts/convert.js <用户指定的markdown文件> <选择的主题css文件> <输出目标html文件路径>
```

*(例如将 `input.md` 转换为带默认主题的 `output.html`：`node wechat-markdown-skill/scripts/convert.js input.md wechat-markdown-skill/resources/themes/default.css output.html`)*

脚本将会自动安全地处理 Markdown 转换、增加 `<section id="MdWechat">` 微信容器、内联注入指定的 CSS 主题。

注意：当前主题体系会在容器根节点中携带 CSS 变量（如 `--text-color`），以便多主题共享配色语义。若后续要通过 `zhy-wechat-publish` 上传到草稿箱，应使用其最新发布脚本，它会在上传前自动展开 `var(--xxx)`，避免微信后台丢失颜色样式。

### 交付输出结果
完成后，直接告诉用户："您的公众号 HTML 已生成在 `[目标文件]` 中，可直接在浏览器打开预览效果，或用编辑器/浏览器打开后全选复制，粘贴到微信公众号后台即可。"

## 主题支持 (Themes)
本目录下的 `resources/themes/` 可以存放多套不同的 CSS 主题方案。
如果用户要求更换主题风格，你可以查看并读取该目录下存在的 CSS 文件路径并传递给脚本，这使得该 Skill 天然支持“换肤”功能。
