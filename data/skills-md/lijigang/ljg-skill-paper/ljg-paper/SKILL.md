---
name: ljg-paper
description: "Paper reader. Takes an academic paper (URL, PDF, or file), runs the atom pipeline (split→squeeze→plain→feynman→博导审稿), and synthesizes a fluent analysis. Focus: what gap does it fill, and would a seasoned advisor take it seriously? Use when user shares an arxiv link, paper URL, PDF, or asks to analyze a research paper. Trigger words: '读论文', '分析论文', 'paper', or when user shares an academic paper."
user_invocable: true
version: "2.0.0"
---

# ljg-paper: 读论文

论文 = 一个增量。已有研究走到了某个边界，这篇论文声称往前推了一步。你的任务：这一步踩在哪儿，踩得稳不稳。

## 约束

### Org-mode 语法

- 加粗用 `*bold*`（单星号），禁止 `**bold**`
- 标题层级从 `*` 开始，不跳级

### ASCII Art

所有图表用纯 ASCII 字符。允许：`+ - | / \ > < v ^ * = ~ . : # [ ] ( ) _ , ; ! ' "` 和空格。禁止 Unicode 绘图符号。

### Denote 文件规范

- 时间戳：`date +%Y%m%dT%H%M%S`
- 可读时间：`date "+%Y-%m-%d %a %H:%M"`
- 文件名：`{时间戳}--paper-{简短标题}__paper.org`
- 输出目录：`~/Documents/notes/`

### Org 文件头

```
#+title:      paper-{简短标题}
#+date:       [{YYYY-MM-DD Day HH:MM}]
#+filetags:   :paper:
#+identifier: {YYYYMMDDTHHMMSS}
#+source:     {URL 或来源描述}
#+authors:    {作者列表}
#+venue:      {发表场所/年份}
```

文件写入后报告路径。

## 执行

### 1. 获取内容

- arxiv URL → ljg-fetch 或 WebFetch
- PDF → Read（注意 pages 参数限制）
- 本地文件 → Read
- 论文名称 → WebSearch

确保拿到：标题、作者、摘要、引言、方法、实验/结果、结论。

### 2. 拆

论文有固定骨架，但骨架下面藏着真正的结构：

- *缺口*：已有研究做到了哪里？哪里还没做到？这篇论文填的是哪条缝？
- *假设*：显式和隐式的假设。
- *方法*：用什么方法填缝？抓住动词结构——它在做什么操作？
- *证据*：用什么数据/实验证明方法站得住？主要结果。
- *贡献声明*：作者自己说贡献了什么。

### 3. 榨增量

Before this paper vs after this paper，世界多了什么？

- *一句话*：这篇论文让我们知道了什么以前不知道的？
- *核心机制图*：用 ASCII 图画出方法的内部结构——组件、数据流、操作关系。看完知道「它内部怎么转的」。

### 4. 白话方法

为核心机制找一个日常类比，让读者跟着走完就能复述方法逻辑。

- 抓方法的动词结构：什么作用于什么？什么流向什么？
- 在日常经验中找结构一样的东西。类比必须承重——方法的每个关键组件都能映射到类比的一个部分。
- 沿着类比把方法从头到尾走一遍。

类比紧跟 ASCII 图之后，是同一段话的延续。

### 5. 关键概念

论文中 1-3 个理解全文的钥匙概念。用费曼技巧讲：

- 假设读者完全不懂，从最基础的地方开始
- 每个概念给一个具体例子
- 讲完读者能用自己的话复述

### 6. 餐巾纸速写

在咖啡馆拿起餐巾纸给朋友画：「以前大家这么想，这篇论文说应该这么想。」

- 识别主流框架和本文框架
- 用 ASCII 图并排或上下放，标注关键结构差异
- 图下一句话点出：从 X 到 Y，核心变化是什么

画结构对比，越简洁越好。

### 7. 博导审稿

换身份：这个方向上带了二十年研究生的博导。学生拿着论文来找你，你在判断这篇东西值不值得认真对待。论文验的是体系——选题眼光、方法成熟度、实验诚意、写作功力。

用白话说，像在办公室跟学生聊：

- *选题眼光*：问题值不值得做？真缺口还是人造缺口？
- *方法成熟度*：巧劲还是蛮力？有没有更自然的做法被忽略了？
- *实验诚意*：baseline 公不公道？消融到位没有？数字经不经得起追问？
- *写作功力*：最该说清楚的地方有没有偷懒？
- *判决*：strong accept / weak accept / borderline / weak reject / strong reject，一句话理由。

好的地方说好，差的地方说差在哪儿。

### 8. 启发

论文读完，问：对我有什么用？三种方式试探：

- *迁移*：论文的某个机制/视角，能直接移植升级我体系里的某个零件吗？
- *混搭*：论文的某个组件和我已有的东西组合，能产生两者单独都没有的新东西吗？
- *反转*：论文的做法和我的默认假设相反吗？照出了什么盲区？

命中的标注类型并展开。没命中的跳过。三个都没命中，说「没有」。

### 9. 缝合与卫生

按 `references/template.org` 的结构，将以上结果编织成一篇连贯分析。

写完扫一遍：
1. 否定式排比全文不超过两处
2. 三段式改两项或四项
3. 同一段落破折号不超过两个

列修改清单确认后生成文件。

### 10. 生成 Org 文件

按 Denote 规范获取时间戳，读 `references/template.org`，写入 `~/Documents/notes/`。

## 质量标准

- *增量要锐*：一句话说出 before vs after。说不出就是没找到。
- *速写要一眼*：不看正文也能大致理解变化方向。
- *博导要像博导*：有判断力有分寸，最后一句判决。
- *零割裂感*：读完像一个人在跟你说「我读了篇论文，它干了啥、好不好、对我有什么用」。
