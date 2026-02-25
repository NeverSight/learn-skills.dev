---
name: weapp-share-timeline
description: 微信小程序分享到朋友圈开发指南。当开发朋友圈分享功能、配置 onShareTimeline、适配单页模式、处理场景值 1154、navigationBarFit 布局调整时使用。
---

# 微信小程序分享到朋友圈开发指南

基础库 2.11.3+ 支持，Android/iOS 微信 8.0.24+

## 快速配置

### 启用分享到朋友圈

页面必须同时满足两个条件才能分享到朋友圈：

1. 先启用"发送给朋友"：实现 `onShareAppMessage`
2. 再启用"分享到朋友圈"：实现 `onShareTimeline`

### 原生小程序示例

```javascript
Page({
  // 1. 必须先启用"发送给朋友"
  onShareAppMessage() {
    return {
      title: '分享标题',
      path: '/pages/article/index?id=123',
      imageUrl: '/images/share.png'
    }
  },

  // 2. 再启用"分享到朋友圈"
  onShareTimeline() {
    return {
      title: '朋友圈分享标题',
      query: 'id=123',  // 注意：不是 path，是 query
      imageUrl: '/images/timeline-share.png'
    }
  }
})
```

### Taro 示例

```tsx
import Taro, { useShareAppMessage, useShareTimeline } from '@tarojs/taro'

function ArticlePage() {
  // 1. 必须先启用"发送给朋友"
  useShareAppMessage(() => ({
    title: '分享标题',
    path: '/pages/article/index?id=123',
    imageUrl: '/images/share.png'
  }))

  // 2. 再启用"分享到朋友圈"
  useShareTimeline(() => ({
    title: '朋友圈分享标题',
    query: 'id=123',
    imageUrl: '/images/timeline-share.png'
  }))

  return <View>文章内容</View>
}

export default ArticlePage
```

## onShareTimeline 返回参数

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| title | string | 分享标题，默认为小程序名称 |
| query | string | 自定义页面路径中携带的参数，如 `id=123&type=news` |
| imageUrl | string | 分享图片 URL，支持本地或网络图片 |

**注意**：`onShareTimeline` 使用 `query` 而非 `path`，不支持自定义页面路径。

## 单页模式 (Single Page Mode)

用户从朋友圈打开分享的小程序页面时，进入"单页模式"，这是一个特殊的受限运行环境。

### 单页模式特点

1. **固定导航栏**：顶部显示页面 JSON 配置的标题，不可自定义
2. **固定操作栏**：底部有"前往小程序"按钮
3. **场景值**：`scene === 1154`
4. **无登录态**：用户未登录，无法获取用户信息
5. **存储隔离**：本地存储与普通模式不共用

### 检测单页模式

```tsx
// 原生小程序
const scene = wx.getLaunchOptionsSync().scene
const isSinglePage = scene === 1154

// Taro
import Taro from '@tarojs/taro'

const launchOptions = Taro.getLaunchOptionsSync()
const isSinglePage = launchOptions.scene === 1154

// 或使用 wx.getApiCategory (基础库 2.22.1+)
const apiCategory = wx.getApiCategory()
const isBrowseOnly = apiCategory === 'browseOnly'  // 朋友圈快照页
```

### 页面适配示例

```tsx
import Taro, { useLoad } from '@tarojs/taro'
import { View, Text, Button } from '@tarojs/components'
import { useState } from 'react'

function ArticlePage() {
  const [isSinglePage, setIsSinglePage] = useState(false)
  const [article, setArticle] = useState(null)

  useLoad(() => {
    const scene = Taro.getLaunchOptionsSync().scene
    setIsSinglePage(scene === 1154)

    // 单页模式下使用未登录访问方式获取数据
    fetchArticle()
  })

  const fetchArticle = async () => {
    // 单页模式下无登录态，需使用公开接口
    const res = await Taro.request({
      url: 'https://api.example.com/public/article',
      data: { id: articleId }
    })
    setArticle(res.data)
  }

  return (
    <View className="article-page">
      <View className="content">
        <Text>{article?.title}</Text>
        <RichText nodes={article?.content} />
      </View>

      {/* 单页模式下隐藏需要登录的交互 */}
      {!isSinglePage && (
        <View className="actions">
          <Button onClick={handleLike}>点赞</Button>
          <Button onClick={handleComment}>评论</Button>
        </View>
      )}
    </View>
  )
}
```

### navigationBarFit 配置

在页面 JSON 中配置 `navigationBarFit` 来调整顶部导航栏与页面的相交状态：

```json
{
  "navigationBarTitleText": "文章详情",
  "navigationBarFit": "squeezed"
}
```

| 值 | 说明 |
| --- | --- |
| `float` | 导航栏浮动在页面上方（默认） |
| `squeezed` | 页面被导航栏挤压，从导航栏下方开始布局 |

## 单页模式禁用能力

### 禁用的组件

| 组件 | 说明 |
| --- | --- |
| `button open-type` | 开放能力按钮 |
| `camera` | 相机组件 |
| `form` | 表单组件 |
| `navigator` | 导航组件 |
| `web-view` | 网页容器 |
| `live-pusher` | 直播推流 |

### 禁用的 API

| 分类 | API |
| --- | --- |
| **登录** | `wx.login`、`wx.checkSession`、`wx.getUserInfo`、`wx.getUserProfile` |
| **路由** | `wx.navigateTo`、`wx.redirectTo`、`wx.reLaunch`、`wx.switchTab`、`wx.navigateBack` |
| **媒体** | `wx.chooseImage`、`wx.chooseMedia`、`wx.chooseVideo`、`wx.saveImageToPhotosAlbum` |
| **位置** | `wx.openLocation`、`wx.chooseLocation`、`wx.startLocationUpdate` |
| **支付** | `wx.requestPayment` |
| **分享** | `wx.showShareMenu`、`wx.hideShareMenu`、`wx.updateShareMenu`、`wx.getShareInfo` |
| **设备** | 蓝牙、Wi-Fi、NFC、剪贴板、扫码、电话 |
| **广告** | `ad` 组件、`wx.createRewardedVideoAd`、`wx.createInterstitialAd` |

### 其他限制

- 不允许横屏使用
- tabBar 不会渲染（包括自定义 tabBar）
- 本地存储与普通模式不共用
- 云开发需开启未登录访问

## 最佳实践

### 1. 内容型页面优先

分享到朋友圈适用于**纯内容展示**场景：

```tsx
// 推荐：文章、新闻、产品详情等内容页
function ArticlePage() {
  useShareTimeline(() => ({
    title: article.title,
    query: `id=${article.id}`,
    imageUrl: article.cover
  }))
  // ...
}

// 不推荐：需要大量交互的页面
function ShoppingCartPage() {
  // 购物车需要登录，不适合分享到朋友圈
}
```

### 2. 优雅降级

```tsx
function ContentPage() {
  const [isSinglePage, setIsSinglePage] = useState(false)

  useLoad(() => {
    setIsSinglePage(Taro.getLaunchOptionsSync().scene === 1154)
  })

  const handleAction = () => {
    if (isSinglePage) {
      // 单页模式下引导用户打开完整小程序
      Taro.showToast({
        title: '请点击下方"前往小程序"使用完整功能',
        icon: 'none',
        duration: 2000
      })
      return
    }
    // 正常模式下执行操作
    doSomething()
  }

  return (
    <View>
      <Button onClick={handleAction}>
        {isSinglePage ? '前往小程序操作' : '立即操作'}
      </Button>
    </View>
  )
}
```

### 3. 使用公开 API

```tsx
// 单页模式下无登录态，设计公开接口
const fetchData = async (articleId: string) => {
  // 使用不需要登录的公开接口
  const res = await Taro.request({
    url: `${API_BASE}/public/articles/${articleId}`,
    method: 'GET'
    // 不传 token
  })
  return res.data
}
```

### 4. 安全区域适配

```tsx
function ContentPage() {
  const [isSinglePage, setIsSinglePage] = useState(false)

  useLoad(() => {
    setIsSinglePage(Taro.getLaunchOptionsSync().scene === 1154)
  })

  return (
    <View
      className="page"
      style={{
        // 单页模式下底部有操作栏，需要额外 padding
        paddingBottom: isSinglePage ? '80px' : 'env(safe-area-inset-bottom)'
      }}
    >
      {/* 页面内容 */}
    </View>
  )
}
```

### 5. 云开发未登录访问

如果使用云开发，需在云函数中开启未登录访问：

```javascript
// 云函数 config.json
{
  "permissions": {
    "openapi": []
  },
  "overrideUserSecurityRules": {
    "allow": true  // 允许未登录访问
  }
}
```

## 运营注意事项

1. **禁止诱导分享**：不得强制用户分享，不得分享立即获得利益
2. **内容完整性**：单页模式应呈现完整内容，不得强制用户点击"打开小程序"
3. **合规使用**：滥用分享能力用于营销、诱导等行为将被平台打击

## 常见问题

### Q: 为什么分享到朋友圈按钮没出现？

A: 检查以下几点：
1. 是否同时实现了 `onShareAppMessage` 和 `onShareTimeline`
2. 微信版本是否 >= 8.0.24
3. 基础库版本是否 >= 2.11.3

### Q: 单页模式下如何获取用户数据？

A: 单页模式无登录态，需要：
1. 将用户相关信息通过 `query` 参数传递
2. 使用公开接口获取数据
3. 云开发需开启未登录访问

### Q: 分享图片有什么要求？

A:
- 支持本地图片或网络图片
- 建议使用正方形图片（1:1 比例）
- 图片大小建议不超过 128KB

## 完整文档

详见 [reference.md](reference.md)
