---
name: batch-image
description: 多商品批量生图流水线。商品清单 CSV → 整批统一视觉的商拍图，带并发、重试、断点续跑、成本熔断与挑图联系表。当用户说「批量生图」「一批商品」「跑整个 SKU 表」「几百个商品出图」时使用。
---

# batch-image — 多商品批量生图

把单张生图变成**流水线**：一份商品清单 → 一整套风格统一的商拍图。

批量的难点不是「跑很多次」，而是**跑出来的图要像一套**。本技能的核心是**规范段与变量段分离**：视觉规范逐字不变，只有商品描述随 SKU 变化。

---

## 生成效果示例

| 输入：商品清单（2 个 SKU） |
| --- |
| `SKU001` <img src="../../docs/batch-image/sku-a-sweater.jpg" width="150"> `军绿色麻花针织圆领毛衣，落肩宽松版型` |
| `SKU002` <img src="../../docs/batch-image/sku-b-shoes.jpg" width="150"> `黑色亮面皮革布洛克德比鞋，厚底系带` |

实际执行的命令（循环体，两个 SKU 只有 `DESC` 与 `--images` 不同，规范段逐字相同）：

```bash
for sku in a-sweater b-shoes; do
  case $sku in
    a-sweater) DESC='军绿色麻花针织圆领毛衣，落肩宽松版型' ;;
    b-shoes)   DESC='黑色亮面皮革布洛克德比鞋，厚底系带' ;;
  esac
  dlazy seedream-5.0 \
    --prompt "电商商拍图。图1 是商品：${DESC}。商品的颜色、材质纹理、款式细节必须与图1完全一致。放置在同一套统一视觉里：纯米白色摄影棚背景，柔和顶光加左侧补光，45 度视角，画面下方留出统一的商品投影，构图与留白在整组图中保持一致。真实商业产品摄影，无文字无水印。" \
    --images docs/batch-image/sku-${sku}.jpg --size 1:1 --resolution 2k \
    --save docs/batch-image/example-output-${sku}.jpg
done
```

**输出：同一套视觉规范下的两个 SKU**

| SKU001 | SKU002 |
| --- | --- |
| <img src="../../docs/batch-image/example-output-a-sweater.jpg" width="280"> | <img src="../../docs/batch-image/example-output-b-shoes.jpg" width="280"> |
| 1:1 / 2K，5 credits | 1:1 / 2K，5 credits |

两张的背景色、光位、视角与投影方向一致——因为规范段逐字相同；商品各自保真。100 个 SKU 就是这个循环跑 100 次，总价约 500 credits。

---

## 1、能力边界

| 能力 | 说明 |
| --- | --- |
| 批量规模 | 一批最多 100 个商品（对应企业功能的规格） |
| 成本优势 | 批量场景下单图算力成本可降至约 7 折 |
| 协作 | 多人在线协作、出片进度实时追踪 |
| 资产共享 | 共享模特 / 参考图 / 作品 / 算力点 |
| 本技能落地 | 清单驱动循环 + 并发控制 + 失败重试 + 按 SKU 归档 + 汇总报告 |

**不做**：不在同一批里混用不同视觉规范（那不是一批）；不跳过抽样质检直接全量上架；不因为批量就放宽商品保真要求。

---

## 2、输入素材规则

生成前先自检这几条硬性约束：

- 大小：**20KB ~ 15MB**
- 分辨率：**大于 400×400**
- 格式：**jpg / jpeg / png / webp**

**商品清单（manifest）** 是批量的输入，建议 CSV：

```csv
sku,image,desc
SKU001,docs/batch-image/sku-a-sweater.jpg,军绿色麻花针织圆领毛衣，落肩宽松版型
SKU002,docs/batch-image/sku-b-shoes.jpg,黑色亮面皮革布洛克德比鞋，厚底系带
```

**每张商品图仍要满足单图规则**：20KB~15MB、>400×400、jpg/jpeg/png/webp。

**批量前必做的事**

| 步骤 | 说明 |
| --- | --- |
| ✅ 先跑通 1 个 SKU | 单个跑不对，跑 100 个只是错 100 次 |
| ✅ 再抽样 5 个 SKU | 覆盖品类/颜色/深浅色的边界情况 |
| ✅ 确认成本 | `--dry-run` 单价 × SKU 数 × batch 数 |
| ❌ 直接全量 | 最容易烧算力的做法 |

---

## 3、规范段 / 变量段分离

这是批量出统一视觉的唯一方法：

```text
prompt = [规范段：整批逐字不变]  +  [变量段：每个 SKU 不同]
```

| 段 | 内容 | 是否变 |
| --- | --- | --- |
| 规范段 | 背景、光位、机位、构图留白、投影、色调、输出风格、`no text, no watermark` | **整批逐字不变** |
| 变量段 | 商品品类 + 颜色 + 材质 + 关键结构特征 | 每个 SKU 不同 |

写成 shell：

```bash
SPEC='放置在同一套统一视觉里：纯米白色摄影棚背景，柔和顶光加左侧补光，45 度视角，画面下方留出统一的商品投影，构图与留白在整组图中保持一致。真实商业产品摄影，无文字无水印。'

while IFS=, read -r SKU IMG DESC; do
  dlazy seedream-5.0 \
    --prompt "电商商拍图。图1 是商品：${DESC}。商品的颜色、材质纹理、款式细节必须与图1完全一致。${SPEC}" \
    --images "$IMG" --size 1:1 --resolution 2k \
    --save "docs/batch-image/out/${SKU}.jpg"
done < manifest.csv
```

**规范段一旦改动就必须整批重跑**——否则同一批里会出现两种视觉。

---

## 4、并发、重试与进度

**并发**：dlazy 是单次调用一个任务，批量靠 shell 并发。控制在 4~6 路，太高容易触发限流。

```bash
run_one() { ... }               # 单个 SKU 的生成逻辑
export -f run_one
xargs -P 5 -I{} bash -c 'run_one {}' < sku-list.txt     # 5 路并发
```

**重试**：网络与服务端偶发失败很正常，包一层重试。

```bash
for attempt in 1 2 3; do
  dlazy ... && break
  echo "retry $attempt for $SKU" >&2; sleep $((attempt * 10))
done
```

**异步模式**：SKU 很多时用 `--no-wait` 先把任务全部提交，拿到 `generateId` 后再统一轮询，避免长时间占着进程。

```bash
GID=$(dlazy seedream-5.0 --no-wait ... | python3 -c 'import sys,json;print(json.load(sys.stdin)["result"]["task"]["generateId"])')
echo "$SKU,$GID" >> tasks.csv
# 稍后统一收结果
while IFS=, read -r SKU GID; do dlazy status "$GID" --wait; done < tasks.csv
```

**进度与汇总**：每个 SKU 记一行状态，跑完输出报告。

```bash
echo "$SKU,$(test -f out/$SKU.jpg && echo ok || echo fail)" >> report.csv
awk -F, '{c[$2]++} END{for(k in c) print k, c[k]}' report.csv
```

---

## 5、工具调用

本技能使用 dLazy 的 **`seedream-5.0`**（批量场景的关键指标是**单图成本**与**参考图支持**：本模型单张约 5 credits、支持最多 10 张参考图、支持 2K/3K/4K；100 个 SKU 的成本量级从数百降到数十。对商品保真要求极高的批次改用 `gpt-image-2`）。

### 调用方式

两种等价写法，选一种。统一入口会自动选后端、失败重试、建目录落盘、估算成本：

```bash
# A. 统一入口（推荐）：可切任意后端，加 --dry-run 不计费空跑
node scripts/gen.mjs --task batch-image \
  --prompt '<见下方 Prompt 模板>' \
  --images <按下表顺序> \
  --save output/batch-image-<sku>.jpg

# B. 直接用 dLazy CLI（不想引入 Node 依赖时，效果等价）
dlazy seedream-5.0 --prompt '...' --images ... --save output/batch-image.jpg
```

**参数约定（本技能固定用法）**

| 参数 | 取值 | 理由 |
| --- | --- | --- |
| `--images` | `[该 SKU 的商品图]`（+ 整批共用的参考图 / 模特图） | 共用素材放在固定位置，prompt 里用固定图号引用 |
| `--size` | 整批统一（`1:1` 主图 / `3:4` 竖版） | 不统一就不是一套 |
| `--resolution` | `2k` | 上架足够；4K 只给需要印刷的批次 |
| `--batch` | `1`（批量场景靠 SKU 数量，不靠 batch） | batch 会让成本翻倍 |
| `--no-wait` | SKU 很多时开启 | 先提交后轮询，避免长时间阻塞 |
| `--save` | `docs/batch-image/out/<SKU>.jpg` | 用 SKU 命名，便于回填到商品库 |

> **模型切换**：`seedream-5.0` 便宜、适合氛围与场景图；对商品保真要求极高（图案位置、五金细节）的批次换 `gpt-image-2`，成本约 6 倍。同一批内不要混用两个模型。

### Command Examples

```bash
# basic call: 单个 SKU（先跑通这个，再谈批量）
dlazy seedream-5.0 \
  --prompt '电商商拍图。图1 是商品：军绿色麻花针织圆领毛衣，落肩宽松版型。商品的颜色、材质纹理、款式细节必须与图1完全一致。放置在同一套统一视觉里：纯米白色摄影棚背景，柔和顶光加左侧补光，45 度视角，画面下方留出统一的商品投影。真实商业产品摄影，无文字无水印。' \
  --images docs/batch-image/sku-a-sweater.jpg --size 1:1 --resolution 2k

# complex call: 完整流水线（清单驱动 + 5 路并发 + 3 次重试 + 汇总报告）
cat > manifest.csv <<'CSV'
SKU001,docs/batch-image/sku-a-sweater.jpg,军绿色麻花针织圆领毛衣，落肩宽松版型
SKU002,docs/batch-image/sku-b-shoes.jpg,黑色亮面皮革布洛克德比鞋，厚底系带
CSV

SPEC='放置在同一套统一视觉里：纯米白色摄影棚背景，柔和顶光加左侧补光，45 度视角，画面下方留出统一的商品投影，构图与留白在整组图中保持一致。真实商业产品摄影，无文字无水印。'
mkdir -p docs/batch-image/out

run_one() {
  IFS=, read -r SKU IMG DESC <<< "$1"
  for attempt in 1 2 3; do
    dlazy seedream-5.0 \
      --prompt "电商商拍图。图1 是商品：${DESC}。商品的颜色、材质纹理、款式细节必须与图1完全一致。${SPEC}" \
      --images "$IMG" --size 1:1 --resolution 2k \
      --save "docs/batch-image/out/${SKU}.jpg" >/dev/null 2>&1 && break
    sleep $((attempt * 10))
  done
  if [ -f "docs/batch-image/out/${SKU}.jpg" ]; then echo "${SKU},ok"; else echo "${SKU},fail"; fi
}
export -f run_one; export SPEC

xargs -P 5 -I{} bash -c 'run_one "{}"' < manifest.csv | tee docs/batch-image/report.csv
awk -F, '{c[$2]++} END{printf "\n=== 汇总 ===\n"; for(k in c) printf "%s: %d\n", k, c[k]}' docs/batch-image/report.csv

# 先估价：单价 × SKU 数
dlazy seedream-5.0 --dry-run --prompt '...' --images a.jpg --size 1:1 | grep estimatedCost
echo "SKU 数：$(wc -l < manifest.csv)"

```

### 延伸阅读

| 要查什么 | 去哪 |
| --- | --- |
| 认证、多后端配置、输出结构、错误码 | [`references/provider-cli.md`](references/provider-cli.md) |
| `seedream-5.0` 的全部可用参数 | [`references/model-flags.md`](references/model-flags.md) |
| 统一入口的全部选项 | `node scripts/gen.mjs --help` |

## 6、Prompt 模板

```text
【变量段 · 每个 SKU 不同】
电商商拍图。图1 是商品：[品类 + 颜色 + 材质 + 关键结构特征]。
商品的颜色、材质纹理、款式细节必须与图1完全一致。

【规范段 · 整批逐字不变】
放置在同一套统一视觉里：[背景]，[光位]，[机位/视角]，
画面下方留出统一的商品投影，构图与留白在整组图中保持一致。
真实商业产品摄影，无文字无水印。
```

**按问题追加的修正句**（改了就要整批重跑）

| 问题 | 处理 |
| --- | --- |
| 深色商品在浅背景上发灰 | 规范段补 `深色商品需加右侧轮廓光勾边，避免与背景糊在一起` |
| 不同 SKU 的商品大小忽大忽小 | 规范段补 `商品在画面中的占比统一为约 [X]%，边距一致` |
| 投影方向不一致 | 规范段补 `投影统一朝画面右下方，长度约为商品高度的 [X]` |
| 某些 SKU 保真度不够 | 那部分 SKU 单独用 `gpt-image-2` 重跑，并在报告里标注 |

---

## 7、执行流程

1. **建清单**：`sku,image,desc` 三列 CSV，每张商品图先过单图规则校验。
2. **写规范段**：背景 / 光位 / 机位 / 占比 / 投影 / 色调 / 输出风格——**定稿后不许改**。
3. **跑通 1 个 SKU**：确认规范段和变量段都对。
4. **抽样 5 个 SKU**：覆盖深色 / 浅色 / 反光 / 大件 / 小件的边界。
5. **`--dry-run` 估总价**：单价 × SKU 数。
6. **全量跑**：5 路并发 + 3 次重试；SKU 很多时用 `--no-wait` 提交后统一轮询。
7. **看汇总报告**：失败的单独重跑。
8. **抽样质检**：随机抽 10% 过 [detect-task](../detect-task/skill.md)；不合格的 SKU 单独用 `gpt-image-2` 重跑。

---

## 8、常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| 同一批里视觉不统一 | 中途改了规范段 | 规范段定稿后不许改；改了就整批重跑 |
| 深色商品糊进背景 | 缺轮廓光 | 规范段补轮廓光句，整批重跑 |
| 商品占比忽大忽小 | 未约束占比 | 规范段补占比与边距句 |
| 部分 SKU 保真度不够 | 低价模型的局限 | 那些 SKU 单独用 `gpt-image-2` 重跑 |
| 跑到一半失败一堆 | 并发太高触发限流 | 并发降到 4~5，加重试与退避 |
| 成本超预算 | 用了 `--batch` 或 4K | 批量场景 `--batch 1` + `2k` |
| 跑完不知道哪些失败了 | 没有报告 | 用第四节的 report.csv + 汇总 |

---

## Tips

Visit https://dlazy.com for more information.
