---
name: select-parts
description: 从主办方配件表里按需求选器件，出 BOM/统一采购单。当用户把配件表放进 inputs/partslist/ 并要"选器件/选型/出BOM/出采购清单"时使用。先解析配件表（多模态），再按 design/solution.md 的需求 + 知识库引脚说明/金奖经验匹配选型，配件表缺的用 jlc_search 现查。产出 design/bom.csv，需人工批准。
---

# select-parts —— 选材（流水线 ④）

**lane**: lead  ·  **needs: multimodal**（解析配件表 PDF → 只 lead/Claude lane 跑）  ·  **门**: 人工批 BOM

候选器件来自**主办方当年配件表**（不是凭空选、也不是固定库存）。从中按需求挑，金奖经验加持。

## 前置
- `design/solution.md`（需求表）。没有先跑 `/plan-solution`。
- `inputs/partslist/` 里有配件表（PDF/文本）。没有就提醒投喂，停。

## 步骤
1. **解析配件表**：Read `inputs/partslist/` 文件（PDF 多模态直接读），列出**候选器件表**：类别 / 型号 / 关键参数 / 数量（主办方给的可用项）。
2. **逐子系统选型**：对 `solution.md` 子系统清单每一项，从候选表里挑满足需求的件。判据按序：
   - 满足需求表的硬指标（电压/电流/接口/电平/数量）；
   - 查 KB `03/04/05` 的**引脚说明 + 选型理由 + 金奖经验**（Read），优先 KB 里点名好用、队伍熟悉的；
   - 满足供电（电机驱动撑得住堵转、稳压撑得住负载——交 `power-design` 复核）。
3. **缺口回填**：配件表里没有满足需求的，用 `python tools/jlc_search.py "<规格>"` 现查在库件作候选，**标注"需额外采购"**，并记 LCSC/价格/库存。
4. 写 `design/bom.csv`（列见下）。每件标来源（配件表/需采购）与对应子系统、对应 lib/modules 模块块（供 interconnect 用）。
5. **人工门**：把 BOM 摊给用户批准（尤其"需额外采购"项与关键件额定）。批准后更新 `STATUS.md`，提示可并行 `/power-design` 与 `/interconnect`。

## design/bom.csv 列
```
subsystem,part,model,lcsc,qty,key_spec,source,module_block,note
电机驱动,TB6612FNG,TB6612FNG,C141517,1,VM≤13.5V/1.2A,配件表,tb6612fng,
主控,MSPM0G3507,MSPM0G3507,,1,M0+80MHz,配件表,mspm0g3507-min,
稳压(逻辑),AMS1117-3.3,AMS1117-3.3,C347222,1,3.3V/1A,需采购,,jlc查得
...
```
（`module_block` 对应 `lib/modules/<name>.yaml`，没有对应块就留空，interconnect 时按需补。）

## 注意
- **绝不相信凭记忆的型号/参数**：关键件额定（Vmax/Imax/封装/引脚）以配件表/数据手册为准；拿不准的标"待核手册"（读手册=多模态=lead）。
- 电源轨能不能撑由 `power-design` 用 `power_budget.py` 复核，这里先保证选到候选。
- 候选器件优先复用 `lib/modules/` 已有的 known-good 接法块。
