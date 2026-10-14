---
name: weixin-game
description: 微信小游戏开发技术限制与最佳实践指南，帮助 Claude Code 在开发微信小游戏时遵循正确的 API 和技术规范。
version: 1.0.0
author: community
tags:
  - weixin
  - minigame
  - wechat
  - game-development
  - canvas
---

# 微信小游戏开发技术限制与最佳实践

指导 Claude Code 在开发微信小游戏时遵循技术限制和实现规范。

## 触发条件

TRIGGER when:
- 用户提到"微信小游戏"、"小游戏开发"、"微信游戏"
- 代码中使用 `wx.` API（如 `wx.createCanvas`、`wx.onTouchStart` 等）
- 项目包含 `game.json` 或 `project.config.json`（微信小游戏配置文件）
- 用户询问关于 Canvas 游戏在微信环境的适配

DO NOT trigger when:
- 开发普通 Web 应用或 H5 页面
- 使用其他小程序框架（如 uni-app、taro 开发普通小程序）
- 纯浏览器环境游戏开发

---

## 核心技术限制

### 1. 运行环境差异

微信小游戏运行在 JavaScriptCore/V8 引擎中，**不是浏览器环境**：

| 特性 | 浏览器 | 微信小游戏 |
|------|--------|-----------|
| 全局对象 | `window` | `globalThis` |
| DOM | `document.*` | **不支持** |
| Canvas 创建 | `document.createElement('canvas')` | `wx.createCanvas()` |
| 图片加载 | `new Image()` | `wx.createImage()` |
| 存储 | `localStorage` | `wx.setStorageSync()` |
| 音频 | `new Audio()` | `wx.createInnerAudioContext()` |
| 网络 | `fetch()` / `XMLHttpRequest` | `wx.request()` |

### 2. 包大小限制

```
主包限制: 4MB
分包总限制: 20MB
单分包限制: 2MB（建议不超过 1.5MB）
```

**应对策略**：
- 使用分包加载（`subpackages` 配置）
- 资源远程加载（CDN）
- 图片压缩、音频压缩
- 代码混淆和压缩

### 3. Canvas API 限制

```javascript
// ❌ 不支持的 API
ctx.roundRect()           // 需手动实现圆角矩形
ctx.toDataURL()           // 部分限制
ctx.getImageData()        // 性能敏感

// ✅ 手动实现圆角矩形
function drawRoundRect(ctx, x, y, w, h, r) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + w - r, y)
  ctx.quadraticCurveTo(x + w, y, x + w, y + r)
  ctx.lineTo(x + w, y + h - r)
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
  ctx.lineTo(x + r, y + h)
  ctx.quadraticCurveTo(x, y + h, x, y + h - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}
```

### 4. 颜色格式限制

```javascript
// ❌ 部分格式不支持或不稳定
ctx.fillStyle = '#00d4ff40'        // 带透明度的简写 hex
ctx.fillStyle = 'hsl(200, 100%, 50%)'  // HSL 格式

// ✅ 推荐使用 rgba
ctx.fillStyle = 'rgba(0, 212, 255, 0.25)'
ctx.fillStyle = '#00d4ff'          // 标准 hex
```

### 5. 网络请求限制

```javascript
// 必须配置合法域名（小程序后台配置）
// 仅支持 HTTPS
// 请求超时默认 60 秒

// ❌ 不支持
fetch('https://api.example.com/data')

// ✅ 使用 wx.request
wx.request({
  url: 'https://api.example.com/data',
  method: 'GET',
  success(res) {
    console.log(res.data)
  },
  fail(err) {
    console.error(err)
  }
})

// WebSocket 限制
wx.connectSocket({
  url: 'wss://socket.example.com'  // 必须是 wss
})
```

---

## API 适配指南

### 全局变量

```javascript
// ❌ 浏览器写法
window.gameState = {}
window.myGlobal = value

// ✅ 微信小游戏写法
// 方案1: 使用 globalThis
globalThis.gameState = {}

// 方案2: 文件顶层定义
let gameState = {}  // 模块级变量

// 方案3: 创建全局管理器
// GameGlobal.js
export const GameGlobal = {
  state: {},
  config: {}
}
```

### Canvas 管理

```javascript
// 主 Canvas（屏幕 Canvas）
const mainCanvas = wx.createCanvas()
const ctx = mainCanvas.getContext('2d')

// 离屏 Canvas（用于缓存、预渲染）
const offCanvas = wx.createOffscreenCanvas({
  type: '2d',
  width: 512,
  height: 512
})

// 获取实际显示尺寸
const { windowWidth, windowHeight } = wx.getSystemInfoSync()
mainCanvas.width = windowWidth
mainCanvas.height = windowHeight
```

### 图片加载

```javascript
// ✅ 微信小游戏图片加载
function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = wx.createImage()
    img.onload = () => resolve(img)
    img.onerror = (err) => reject(err)
    img.src = src  // 相对路径或配置的 CDN 域名
  })
}

// 加载多张图片
async function loadAssets() {
  const assets = {
    player: await loadImage('images/player.png'),
    enemy: await loadImage('images/enemy.png'),
    bg: await loadImage('images/background.png')
  }
  return assets
}
```

### 触摸事件

```javascript
// 微信使用全局触摸事件，不是 Canvas 上的事件
class TouchManager {
  constructor() {
    this.touches = new Map()
    this.callbacks = {
      start: [],
      move: [],
      end: []
    }
    this.init()
  }

  init() {
    wx.onTouchStart(e => this.handleTouch('start', e))
    wx.onTouchMove(e => this.handleTouch('move', e))
    wx.onTouchEnd(e => this.handleTouch('end', e))
    wx.onTouchCancel(e => this.handleTouch('end', e))
  }

  handleTouch(type, e) {
    e.touches.forEach(touch => {
      this.callbacks[type].forEach(cb => cb(touch))
    })
  }

  on(type, callback) {
    this.callbacks[type].push(callback)
  }
}

// 使用
const touchManager = new TouchManager()
touchManager.on('start', (touch) => {
  console.log('Touch at:', touch.clientX, touch.clientY)
})
```

### 音频播放

```javascript
// 音频管理器
class AudioManager {
  constructor() {
    this.sounds = new Map()
    this.music = null
    this.muted = false
  }

  // 加载音效
  loadSound(name, src) {
    const audio = wx.createInnerAudioContext()
    audio.src = src
    this.sounds.set(name, audio)
    return audio
  }

  // 播放音效
  playSound(name, volume = 1.0) {
    if (this.muted) return
    const audio = this.sounds.get(name)
    if (audio) {
      audio.volume = volume
      audio.stop()
      audio.play()
    }
  }

  // 播放背景音乐
  playMusic(src, loop = true) {
    if (this.music) {
      this.music.stop()
      this.music.destroy()
    }
    this.music = wx.createInnerAudioContext()
    this.music.src = src
    this.music.loop = loop
    this.music.play()
  }

  // 销毁所有音频
  destroy() {
    this.sounds.forEach(audio => audio.destroy())
    this.sounds.clear()
    if (this.music) {
      this.music.destroy()
      this.music = null
    }
  }
}
```

### 本地存储

```javascript
// ✅ 微信存储 API
// 同步存储
wx.setStorageSync('playerData', { level: 5, score: 1000 })
const data = wx.getStorageSync('playerData') || {}

// 异步存储（推荐用于大数据）
wx.setStorage({
  key: 'largeData',
  data: largeObject,
  success() { console.log('Saved') },
  fail(err) { console.error(err) }
})

// 删除
wx.removeStorageSync('key')
wx.clearStorageSync()  // 清空所有
```

---

## 布局注意事项

### 1. 右上角菜单按钮区域

微信小游戏右上角有固定的操作菜单按钮（"..."按钮），点击后显示菜单选项。**必须避开此区域**放置关键UI元素。

```
┌─────────────────────────────────┐
│                      [≡] [•••] │  ← 右上角菜单按钮区域（约44px高度）
│                                 │
│        安全区 (safeArea)        │  ← 主要内容区域
│                                 │
│                                 │
│                                 │
│  _______________________________│  ← 底部安全区域（iPhone X系列手势条）
└─────────────────────────────────┘
```

**避开区域尺寸**：
- 右上角菜单按钮：高度约 44px，宽度约 87px（iOS）/ 48px（Android）
- 状态栏：`systemInfo.statusBarHeight`
- 底部手势条：iPhone X系列约 34px

```javascript
// 获取安全区域信息
const systemInfo = wx.getSystemInfoSync()
const { safeArea, statusBarHeight } = systemInfo

// 安全区域边界
console.log('安全区域:', {
  top: safeArea.top,           // 安全区域顶部 y 坐标
  bottom: safeArea.bottom,     // 安全区域底部 y 坐标
  left: safeArea.left,         // 安全区域左侧 x 坐标
  right: safeArea.right,       // 安全区域右侧 x 坐标
  width: safeArea.width,       // 安全区域宽度
  height: safeArea.height      // 安全区域高度
})

// 右上角按钮区域（保守估计）
const menuButtonArea = {
  top: statusBarHeight,
  height: 44,
  right: systemInfo.windowWidth,
  width: 87  // iOS 较宽，Android 较窄
}
```

### 2. 安全区域适配方案

```javascript
class SafeAreaManager {
  constructor() {
    const systemInfo = wx.getSystemInfoSync()
    this.safeArea = systemInfo.safeArea
    this.screenWidth = systemInfo.windowWidth
    this.screenHeight = systemInfo.windowHeight
    this.statusBarHeight = systemInfo.statusBarHeight

    // 计算危险区域（需要避开）
    this.dangerAreas = {
      // 顶部：状态栏 + 菜单按钮
      top: {
        y: 0,
        height: Math.max(this.safeArea.top, this.statusBarHeight + 44)
      },
      // 右上角：菜单按钮
      topRight: {
        x: this.screenWidth - 100,
        y: 0,
        width: 100,
        height: this.statusBarHeight + 44
      },
      // 底部：手势条区域（iPhone X系列）
      bottom: {
        y: this.safeArea.bottom,
        height: this.screenHeight - this.safeArea.bottom
      }
    }
  }

  // 检查坐标是否在安全区域
  isInSafeArea(x, y, width = 0, height = 0) {
    const danger = this.dangerAreas

    // 检查是否与顶部危险区域重叠
    if (y < danger.top.height) return false

    // 检查是否与右上角危险区域重叠
    if (x + width > danger.topRight.x && y < danger.topRight.height) return false

    // 检查是否与底部危险区域重叠
    if (y + height > danger.bottom.y) return false

    return true
  }

  // 获取建议的安全布局边界
  getSafeBounds() {
    return {
      top: this.dangerAreas.top.height,
      bottom: this.safeArea.bottom,
      left: this.safeArea.left,
      right: this.safeArea.right
    }
  }

  // 调整元素位置到安全区域
  adjustToSafeArea(x, y, width, height) {
    const bounds = this.getSafeBounds()

    // 调整 x 坐标
    if (x < bounds.left) x = bounds.left
    if (x + width > bounds.right) x = bounds.right - width

    // 调整 y 坐标
    if (y < bounds.top) y = bounds.top
    if (y + height > bounds.bottom) y = bounds.bottom - height

    return { x, y }
  }
}

// 使用示例
const safeArea = new SafeAreaManager()

// 放置按钮时检查
const button = { x: 10, y: 10, width: 100, height: 44 }
if (!safeArea.isInSafeArea(button.x, button.y, button.width, button.height)) {
  // 调整到安全区域
  const adjusted = safeArea.adjustToSafeArea(button.x, button.y, button.width, button.height)
  button.x = adjusted.x
  button.y = adjusted.y
}
```

### 3. 常见布局问题

```javascript
// ❌ 错误：按钮放在右上角菜单按钮下方
const button = { x: screenWidth - 120, y: 20 }

// ✅ 正确：按钮放在安全区域内
const safeY = safeArea.top + 10
const button = { x: screenWidth - 120, y: safeY }

// ❌ 错误：忽略底部手势条
const bottomButton = { y: screenHeight - 50 }

// ✅ 正确：考虑底部安全区域
const safeBottomY = safeArea.bottom - 50 - 10
const bottomButton = { y: safeBottomY }
```

### 4. 多设备适配

```javascript
// 获取设备信息
const deviceInfo = wx.getDeviceInfo()
const isIPhoneX = deviceInfo.model.includes('iPhone X') ||
                  deviceInfo.model.includes('iPhone 1') // iPhone 11, 12, 13, 14, 15 系列

// iPhone X 系列特殊处理
if (isIPhoneX) {
  // 底部额外留白
  this.bottomPadding = 34
}
```

---

## 屏幕适配方案

```javascript
class ScreenAdapter {
  constructor(designWidth = 375, designHeight = 667) {
    this.designWidth = designWidth
    this.designHeight = designHeight

    const info = wx.getSystemInfoSync()
    this.screenWidth = info.windowWidth
    this.screenHeight = info.windowHeight
    this.pixelRatio = info.pixelRatio
    this.safeArea = info.safeArea

    // 计算缩放（保持宽高比）
    this.scale = Math.min(
      this.screenWidth / designWidth,
      this.screenHeight / designHeight
    )

    // 计算偏移（居中）
    this.offsetX = (this.screenWidth - designWidth * this.scale) / 2
    this.offsetY = (this.screenHeight - designHeight * this.scale) / 2
  }

  // 屏幕坐标 -> 游戏坐标
  screenToGame(x, y) {
    return {
      x: (x - this.offsetX) / this.scale,
      y: (y - this.offsetY) / this.scale
    }
  }

  // 游戏坐标 -> 屏幕坐标
  gameToScreen(x, y) {
    return {
      x: x * this.scale + this.offsetX,
      y: y * this.scale + this.offsetY
    }
  }

  // 获取安全区域（避开刘海屏、底部手势条）
  getSafeArea() {
    return {
      top: this.safeArea.top,
      bottom: this.safeArea.bottom,
      left: this.safeArea.left,
      right: this.safeArea.right
    }
  }
}
```

---

## 性能优化建议

### 1. 渲染优化

```javascript
// ❌ 每帧都清除整个画布
ctx.clearRect(0, 0, canvas.width, canvas.height)

// ✅ 只清除变化区域（对于静态背景）
ctx.clearRect(obj.x - 1, obj.y - 1, obj.width + 2, obj.height + 2)

// ✅ 使用离屏 Canvas 缓存静态元素
const cacheCanvas = wx.createOffscreenCanvas({ width: 200, height: 200 })
const cacheCtx = cacheCanvas.getContext('2d')
// 绘制一次
cacheCtx.drawImage(backgroundImg, 0, 0)

// 主循环中直接绘制缓存
ctx.drawImage(cacheCanvas, 0, 0)
```

### 2. 对象池

```javascript
class ObjectPool {
  constructor(createFn, initialSize = 10) {
    this.createFn = createFn
    this.pool = []
    this.active = []

    // 预创建对象
    for (let i = 0; i < initialSize; i++) {
      this.pool.push(createFn())
    }
  }

  get() {
    const obj = this.pool.pop() || this.createFn()
    this.active.push(obj)
    return obj
  }

  release(obj) {
    const index = this.active.indexOf(obj)
    if (index > -1) {
      this.active.splice(index, 1)
      this.pool.push(obj)
    }
  }

  releaseAll() {
    while (this.active.length) {
      this.pool.push(this.active.pop())
    }
  }
}

// 使用示例：子弹池
const bulletPool = new ObjectPool(() => ({ x: 0, y: 0, active: false }), 20)
```

### 3. 资源管理

```javascript
// 资源预加载
class AssetLoader {
  constructor() {
    this.images = new Map()
    this.audios = new Map()
  }

  async loadImages(list) {
    const promises = list.map(item =>
      loadImage(item.src).then(img => {
        this.images.set(item.name, img)
        return { name: item.name, img }
      })
    )
    return Promise.all(promises)
  }

  getImage(name) {
    return this.images.get(name)
  }
}

// 使用
const loader = new AssetLoader()
await loader.loadImages([
  { name: 'player', src: 'images/player.png' },
  { name: 'enemy', src: 'images/enemy.png' }
])
```

---

## 高级功能与限制

### 1. 开放数据域（排行榜）

微信小游戏的**好友排行榜**必须在开放数据域中实现，主域无法直接访问好友数据。

```
项目结构：
├── game.js                    # 主域入口
├── open-data-context/         # 开放数据域
│   └── index.js              # 排行榜逻辑
└── game.json                 # 配置
```

**game.json 配置**：
```json
{
  "openDataContext": "open-data-context"
}
```

**主域与开放数据域通信**：
```javascript
// 主域 game.js
const openDataContext = wx.getOpenDataContext()

// 发送消息到开放数据域
openDataContext.postMessage({
  type: 'updateScore',
  score: 1000,
  level: 5
})

// 创建共享 Canvas（用于显示排行榜）
const sharedCanvas = openDataContext.canvas
sharedCanvas.width = 300
sharedCanvas.height = 400

// 在主 Canvas 上绘制共享 Canvas
const mainCtx = mainCanvas.getContext('2d')
mainCtx.drawImage(sharedCanvas, 50, 100)
```

**开放数据域 index.js**：
```javascript
// 接收主域消息
wx.onMessage(data => {
  if (data.type === 'updateScore') {
    // 更新用户数据到云端
    wx.setUserCloudStorage({
      KVDataList: [{
        key: 'score',
        value: JSON.stringify({ score: data.score, level: data.level })
      }],
      success() {
        console.log('分数上传成功')
        // 刷新排行榜
        getFriendRanking()
      }
    })
  }

  if (data.type === 'getRanking') {
    getFriendRanking()
  }
})

// 获取好友排行榜
function getFriendRanking() {
  wx.getFriendCloudStorage({
    keyList: ['score'],
    success(res) {
      // res.data 是好友数据数组
      const sorted = res.data.sort((a, b) => {
        const scoreA = JSON.parse(a.KVDataList[0].value).score
        const scoreB = JSON.parse(b.KVDataList[0].value).score
        return scoreB - scoreA
      })

      // 绘制排行榜到 Canvas
      drawRanking(sorted)
    }
  })
}

// 绘制排行榜
function drawRanking(data) {
  const canvas = wx.createCanvas()
  const ctx = canvas.getContext('2d')

  ctx.fillStyle = '#fff'
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  ctx.fillStyle = '#333'
  ctx.font = '14px Arial'

  data.forEach((player, index) => {
    const score = JSON.parse(player.KVDataList[0].value).score
    ctx.fillText(`${index + 1}. ${player.nickname}: ${score}`, 10, 30 + index * 25)
  })
}
```

**重要限制**：
- `wx.getFriendCloudStorage()` 只能在开放数据域调用
- 开放数据域无法使用大部分 `wx.` API（如网络请求受限）
- 开放数据域有独立的 Canvas，通过 `sharedCanvas` 与主域共享

### 2. 多线程 Worker

用于将耗时计算放到后台线程，避免阻塞主线程。

```javascript
// 主线程
const worker = wx.createWorker('workers/physics.js')

// 发送数据
worker.postMessage({
  type: 'calculate',
  bodies: physicsData
})

// 接收结果
worker.onMessage(res => {
  if (res.type === 'result') {
    // 更新物理状态
    updatePhysics(res.data)
  }
})

// workers/physics.js
worker.onMessage(data => {
  if (data.type === 'calculate') {
    // 执行耗时计算
    const result = heavyPhysicsCalculation(data.bodies)

    // 返回结果
    worker.postMessage({
      type: 'result',
      data: result
    })
  }
})
```

### 3. 内存管理

微信小游戏对内存敏感，需要主动管理：

```javascript
// 监听内存警告
wx.onMemoryWarning((res) => {
  console.log('内存警告，级别:', res.level)  // level: 0-5，越大越严重

  // 清理缓存
  textureCache.clear()
  audioCache.clear()

  // 释放未使用的资源
  gc()
})

// 主动触发垃圾回收（调试用）
wx.triggerGC()

// 获取内存使用情况
const performance = wx.getPerformance()
const memory = performance.getEntriesByType('memory')
console.log('内存使用:', memory)
```

**内存优化建议**：
```javascript
// 1. 及时销毁音频
const audio = wx.createInnerAudioContext()
audio.src = 'sound.mp3'
audio.play()
audio.onEnded(() => {
  audio.destroy()  // 播放完毕后销毁
})

// 2. 图片对象池
class ImagePool {
  constructor(maxSize = 20) {
    this.pool = new Map()
    this.maxSize = maxSize
  }

  get(src) {
    if (this.pool.has(src)) {
      return this.pool.get(src)
    }

    const img = wx.createImage()
    img.src = src

    if (this.pool.size >= this.maxSize) {
      // 移除最旧的
      const firstKey = this.pool.keys().next().value
      this.pool.delete(firstKey)
    }

    this.pool.set(src, img)
    return img
  }
}

// 3. 避免内存泄漏
class GameManager {
  constructor() {
    this.listeners = []
  }

  addListener(callback) {
    this.listeners.push(callback)
  }

  destroy() {
    // 清除所有监听器
    this.listeners = []
  }
}
```

### 4. 分享功能

```javascript
// 被动分享（用户点击右上角菜单）
wx.onShareAppMessage(() => {
  return {
    title: '来挑战我的高分！',
    imageUrl: 'images/share.png',
    query: 'level=5&score=1000'  // 参数会传递给被分享者
  }
})

// 主动分享
wx.shareAppMessage({
  title: '我通关了第5关！',
  imageUrl: 'images/share-level5.png',
  query: 'from=share&level=5',
  success() {
    console.log('分享成功')
  },
  fail(err) {
    console.error('分享失败', err)
  }
})

// 分享到群
wx.shareAppMessage({
  title: '一起来玩！',
  imageUrl: 'images/share.png',
  toGroup: true
})
```

### 5. 虚拟支付

```javascript
// 发起支付（需在小程序后台开通）
wx.requestMidasPayment({
  mode: 'game',
  env: 0,  // 0: 正式环境, 1: 沙箱环境
  offerId: '123456',  // 商品ID
  currencyType: 'CNY',
  buyQuantity: 10,
  success(res) {
    console.log('支付成功', res)
    // 发放道具
  },
  fail(err) {
    console.error('支付失败', err)
  }
})
```

### 6. 版本兼容

```javascript
// 检查 API 是否可用
if (wx.canIUse('getDeviceInfo')) {
  const deviceInfo = wx.getDeviceInfo()
}

// 比较基础库版本
function compareVersion(v1, v2) {
  v1 = v1.split('.')
  v2 = v2.split('.')
  const len = Math.max(v1.length, v2.length)

  while (v1.length < len) v1.push('0')
  while (v2.length < len) v2.push('0')

  for (let i = 0; i < len; i++) {
    const num1 = parseInt(v1[i])
    const num2 = parseInt(v2[i])
    if (num1 > num2) return 1
    if (num1 < num2) return -1
  }
  return 0
}

const systemInfo = wx.getSystemInfoSync()
const baseVersion = systemInfo.SDKVersion

if (compareVersion(baseVersion, '2.10.0') >= 0) {
  // 使用新 API
} else {
  // 降级处理
}
```

---

## 常见错误与解决

### 错误 1: `window is not defined`

```javascript
// ❌ 使用 window
window.myVar = value

// ✅ 使用 globalThis 或模块变量
globalThis.myVar = value
```

### 错误 2: `document is not defined`

```javascript
// ❌ 使用 document
const el = document.getElementById('xxx')
document.createElement('canvas')

// ✅ 使用微信 API
const canvas = wx.createCanvas()
```

### 错误 3: 图片加载失败

```javascript
// 检查路径是否正确
// 检查是否配置了 download 域名（网络图片）
// 检查图片格式（支持 png, jpg, gif）

wx.createImage()
img.onerror = (e) => {
  console.error('Image load failed:', e)
}
```

### 错误 4: 音频无法播放

```javascript
// 用户交互后才能播放音频
// 首次播放需要在 touchstart/touchend 回调中触发

let audioInitialized = false
wx.onTouchStart(() => {
  if (!audioInitialized) {
    // 初始化音频
    audioInitialized = true
  }
})
```

---

## 项目结构建议

```
my-minigame/
├── game.json              # 游戏配置
├── game.js                # 入口文件
├── project.config.json    # 项目配置
├── js/
│   ├── Game.js           # 游戏主类
│   ├── scenes/           # 场景
│   │   ├── MenuScene.js
│   │   └── GameScene.js
│   ├── entities/         # 实体类
│   │   ├── Player.js
│   │   └── Enemy.js
│   ├── managers/         # 管理器
│   │   ├── AudioManager.js
│   │   ├── InputManager.js
│   │   └── SceneManager.js
│   └── utils/            # 工具类
│       ├── ObjectPool.js
│       └── ScreenAdapter.js
├── images/               # 图片资源
├── audio/                # 音频资源
└── subpackages/          # 分包
    ├── level2/
    └── level3/
```

---

## game.json 配置示例

```json
{
  "deviceOrientation": "portrait",
  "showStatusBar": false,
  "networkTimeout": {
    "request": 10000,
    "connectSocket": 10000,
    "uploadFile": 10000,
    "downloadFile": 10000
  },
  "subpackages": [
    {
      "name": "level2",
      "root": "subpackages/level2"
    },
    {
      "name": "level3",
      "root": "subpackages/level3"
    }
  ],
  "plugins": {}
}
```

---

## 检查清单

开发微信小游戏时，Claude Code 应确保：

### 基础 API 适配
- [ ] 不使用 `window`、`document`、`DOM` API
- [ ] 使用 `wx.createCanvas()` 创建 Canvas
- [ ] 使用 `wx.createImage()` 加载图片
- [ ] 使用 `wx.createInnerAudioContext()` 播放音频
- [ ] 使用 `wx.onTouchStart/Move/End` 处理触摸
- [ ] 使用 `wx.setStorageSync/getStorageSync` 存储
- [ ] 使用 `wx.request()` 进行网络请求
- [ ] 手动实现 `roundRect()` 等不支持的 API
- [ ] 颜色使用 `rgba()` 或标准 `#RRGGBB` 格式

### 布局与安全区域
- [ ] 避开右上角菜单按钮区域（约 44px 高度）
- [ ] 使用 `wx.getSystemInfoSync().safeArea` 获取安全区域
- [ ] 处理刘海屏顶部安全区域
- [ ] 处理底部手势条（iPhone X 系列约 34px）
- [ ] 关键 UI 元素不要放置在危险区域

### 性能与资源
- [ ] 实现屏幕适配和像素比适配
- [ ] 音频资源在用户交互后才能播放
- [ ] 实现对象池优化性能
- [ ] 使用分包加载控制包大小（主包 ≤4MB）
- [ ] 及时销毁音频、图片等资源
- [ ] 监听 `wx.onMemoryWarning` 处理内存警告

### 高级功能
- [ ] 排行榜功能使用开放数据域实现
- [ ] 耗时计算使用 Worker 多线程
- [ ] 使用 `wx.canIUse()` 检查 API 兼容性
- [ ] 分享功能配置正确的图片和参数

### 测试与调试
- [ ] 真机测试（开发者工具行为可能不同）
- [ ] 测试不同机型（刘海屏、全面屏、iPhone X 系列）
- [ ] 测试弱网环境
- [ ] 测试内存占用

