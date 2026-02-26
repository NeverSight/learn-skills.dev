---
name: qianfan
description: Use when managing products on Xiaohongshu merchant platform (ark.xiaohongshu.com) - listing new products, checking product status, managing inventory on 千帆 seller backend
---

# 小红书千帆商家后台自动化

基于 browse-use `--cdp` 模式自动化千帆商家后台 (ark.xiaohongshu.com) 操作。

## Prerequisites

- `chrome-debug` running with logged-in 千帆 session
- browse-use skill installed at `~/.claude/skills/browse-use/`

## Quick Start

```bash
QIANFAN=~/.claude/skills/qianfan/qianfan.js

# 探查页面（截图 + 提取文本和表单）
node $QIANFAN scout

# 查看商品列表
node $QIANFAN products

# 创建商品
node $QIANFAN create --json /tmp/product.json
```

## Commands

### scout [url-path]

截图并分析千帆页面。输出截图路径、页面文本、表单元素。

```bash
node $QIANFAN scout                           # 首页
node $QIANFAN scout /app-item/good/create     # 发布商品页
```

### products

通过侧栏导航进入商品管理页，截图并提取商品列表信息。

### create --json FILE

根据 JSON 配置创建商品。多步骤表单，每步截图以供确认。

```json
{
  "title": "商品标题",
  "images": ["/path/to/img1.jpg"],
  "useLibrary": true,
  "libraryKeyword": "封面",
  "category": ["电子资源", "PPT/简历/其他模板"],
  "price": "9.9",
  "marketPrice": "19.9",
  "stock": "999",
  "deliveryLink": "https://...",
  "deliveryNote": "感谢购买..."
}
```

**images**: 本地文件路径，通过 file input 上传。
**useLibrary**: true 时从素材库选图，可用 libraryKeyword 搜索过滤。

## Key URLs

| Page | Path |
|------|------|
| 首页 | `https://ark.xiaohongshu.com` |
| 发布商品 | `/app-item/good/create` |
| 商品管理 | 侧栏 → 商品 → 商品管理 |
| 草稿箱 | 商品管理页右上角 → 草稿箱 |

## Sidebar Navigation

千帆是 SPA，URL 路由不完全可靠。优先通过侧栏导航：

- 商品: 发布商品, 商品管理, 评价管理, 商品商机, 商品素材, 商品工具, 库存管理, 图片空间, 商品诊断
- 内容: 笔记管理, 笔记中心, 直播计划, 直播中控
- 私域: 购物粉丝团, 群聊经营, 用户资产
- 营销: 营销活动, 营销工具
- 店铺: 店铺装修

## Product Creation Flow

1. **Step 1 - 基本信息**: 上传商品图片 → 填写标题 → 选择类目 → 点击「信息已确认，下一步」
2. **Step 2 - 详细信息**: 填写价格/划线价 → 填写库存 → 设置自动发货（链接+说明）→ 提交

## Gotchas

- 图片上传有两种方式：本地上传（file input）或从素材库选择（点击「上传图片」打开 modal）
- 素材库 modal 中图片选择：点击图片容器选中，底部显示「已选择 N / 100 项」，点击「确认」
- 标题 input 的 placeholder 包含「品牌名称」
- 类目选择是多级级联，需要逐级点击
- 发货链接 textarea 的 placeholder 包含「baiduwangpan」
- 商品管理页的 tab：售卖中、已下架、已冻结、整改、审核中、审核驳回、审核通过
- 所有操作需要 `--cdp` 模式（千帆的 cookie/session 认证复杂）
