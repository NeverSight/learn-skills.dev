---
name: pyautogui-automation
description: 基于 PyAutoGUI 的桌面自动化工具。支持截图、鼠标键盘控制、图像识别、颜色检测等操作。当用户需要自动化操作桌面应用、执行 UI 测试或重复性任务时触发。
---

# PyAutoGUI 自动化操作

## 功能概览

| 功能类别 | 支持的操作                                           |
| -------- | ---------------------------------------------------- |
| 截图     | 全屏截图、区域截图、截图到剪贴板                     |
| 鼠标控制 | 点击、双击、移动、相对移动、拖拽、滚动、按下/释放    |
| 颜色操作 | 获取像素颜色、查找颜色位置                           |
| 键盘操作 | 输入文本、按键、组合键、快捷操作（复制/粘贴/全选等） |
| 图像识别 | 在屏幕上查找图片位置、等待图片出现/消失              |
| 对话框   | 警告、确认、输入对话框                               |
| 系统信息 | 屏幕分辨率、鼠标位置、窗口信息                       |
| 工具     | 等待、暂停                                           |

## 快速开始

### 基本使用模式

```bash
python scripts/automation.py <action> [参数...]
```

所有操作返回 JSON 格式结果。

**脚本位置**: [scripts/automation.py](scripts/automation.py)

## 操作详解

### 截图

```bash
# 全屏截图（自动生成文件名）
python scripts/automation.py screenshot

# 指定输出路径
python scripts/automation.py screenshot --output my_screenshot.png

# 区域截图
python scripts/automation.py screenshot --output region.png --region 100,100,400,300

# 截图到剪贴板（需要安装 pywin32）
python scripts/automation.py screenshot_to_clipboard
python scripts/automation.py screenshot_to_clipboard --region 100,100,400,300
```

### 鼠标点击

```bash
# 左键单击坐标 (100, 200)
python scripts/automation.py click --x 100 --y 200

# 右键双击
python scripts/automation.py click --x 100 --y 200 --button right --clicks 2

# 快捷双击
python scripts/automation.py double_click --x 100 --y 200
```

### 颜色操作

```bash
# 获取指定坐标的颜色
python scripts/automation.py get_pixel_color --x 100 --y 200
# 返回: {"rgb": [255, 255, 255], "hex": "#ffffff"}

# 查找颜色位置（精确匹配）
python scripts/automation.py find_color --rgb 255,255,255

# 查找颜色（带容差）
python scripts/automation.py find_color --rgb 255,255,255 --tolerance 10

# 在指定区域查找
python scripts/automation.py find_color --rgb 255,0,0 --region 0,0,800,600
```

### 鼠标控制

```bash
# 获取当前鼠标位置
python scripts/automation.py get_mouse_position

# 移动鼠标（瞬间）
python scripts/automation.py move_mouse --x 500 --y 300

# 移动鼠标（动画效果，0.5秒）
python scripts/automation.py move_mouse --x 500 --y 300 --duration 0.5

# 相对当前位置移动鼠标
python scripts/automation.py move_mouse_rel --x 100 --y -50
python scripts/automation.py move_mouse_rel --x 100 --y -50 --duration 0.5

# 拖拽鼠标
python scripts/automation.py drag_mouse --x 800 --y 600 --duration 1.0

# 鼠标按下（不释放）
python scripts/automation.py mouse_down --button left

# 鼠标释放
python scripts/automation.py mouse_up --button left

# 滚动（正数向上，负数向下）
python scripts/automation.py scroll --amount 500
python scripts/automation.py scroll --amount -500 --x 500 --y 300
```

### 屏幕信息

```bash
# 获取屏幕分辨率
python scripts/automation.py get_screen_size
# 返回: {"width": 1920, "height": 1080}

# 获取当前活动窗口信息（需要安装 pywin32）
python scripts/automation.py get_active_window
# 返回: {"title": "窗口标题", "left": 100, "top": 100, "width": 800, "height": 600}

# 获取所有可见窗口列表（需要安装 pywin32）
python scripts/automation.py get_all_windows
# 返回: {"count": 5, "windows": [...]}
```

### 等待

```bash
# 等待 2 秒
python scripts/automation.py sleep --seconds 2
```

### 键盘操作

```bash
# 输入文本
python scripts/automation.py type_text --text "Hello World"

# 输入文本（带间隔）
python scripts/automation.py type_text --text "Hello" --interval 0.1

# 按下按键
python scripts/automation.py press_key --key enter
python scripts/automation.py press_key --key esc

# 组合键
python scripts/automation.py hotkey --keys ctrl,c
python scripts/automation.py hotkey --keys ctrl,shift,esc

# 快捷操作
python scripts/automation.py copy      # Ctrl+C
python scripts/automation.py paste     # Ctrl+V
python scripts/automation.py cut       # Ctrl+X
python scripts/automation.py select_all # Ctrl+A
python scripts/automation.py undo      # Ctrl+Z
python scripts/automation.py redo      # Ctrl+Y
python scripts/automation.py save      # Ctrl+S
```

常用按键名称: `enter`, `esc`, `tab`, `space`, `backspace`, `delete`, `up`, `down`, `left`, `right`, `f1`-`f12`, `ctrl`, `alt`, `shift`, `win`

### 图像识别

需要安装 opencv-python 以使用 confidence 参数：

```bash
# 查找图片位置
python scripts/automation.py locate_on_screen --image button.png

# 使用置信度（需要 opencv-python）
python scripts/automation.py locate_on_screen --image button.png --confidence 0.9

# 在指定区域查找
python scripts/automation.py locate_on_screen --image button.png --region 0,0,800,600

# 查找所有匹配位置
python scripts/automation.py locate_all_on_screen --image icon.png

# 等待图片出现（最多等待10秒）
python scripts/automation.py wait_for_image --image button.png --timeout 10

# 等待图片出现（自定义检查间隔）
python scripts/automation.py wait_for_image --image loading.png --timeout 30 --wait_interval 1

# 等待图片消失
python scripts/automation.py wait_for_image_to_vanish --image loading.png --timeout 30
```

### 对话框

```bash
# 警告对话框
python scripts/automation.py alert --title "提示" --text "操作完成"

# 确认对话框
python scripts/automation.py confirm --title "确认" --text "是否继续？"

# 自定义按钮
python scripts/automation.py confirm --title "选择" --text "请选择操作" --buttons "保存,不保存,取消"

# 输入对话框
python scripts/automation.py prompt --title "输入" --text "请输入名称:" --default "默认值"
```

## 安全设置

脚本已启用以下安全保护：

- **FAILSAFE**: 将鼠标快速移动到屏幕左上角会触发异常停止
- **PAUSE**: 每个操作后有 0.1 秒默认暂停

## 完整示例

### 自动化登录流程

```bash
# 1. 截图记录初始状态
python scripts/automation.py screenshot --output login_start.png

# 2. 点击用户名输入框
python scripts/automation.py click --x 500 --y 300

# 3. 输入用户名
python scripts/automation.py type_text --text "myusername"

# 4. 按 Tab 切换到密码框
python scripts/automation.py press_key --key tab

# 5. 输入密码
python scripts/automation.py type_text --text "mypassword"

# 6. 点击登录按钮
python scripts/automation.py click --x 500 --y 400

# 7. 等待页面加载
python scripts/automation.py sleep --seconds 3

# 8. 截图记录结果
python scripts/automation.py screenshot --output login_end.png
```

### 颜色检测自动化

```bash
# 检测特定位置颜色并执行操作
color=$(python scripts/automation.py get_pixel_color --x 100 --y 100)
# 解析 JSON 判断颜色后执行相应操作
```

### 图像定位点击

```bash
# 查找按钮并点击
result=$(python scripts/automation.py locate_on_screen --image submit_button.png --confidence 0.9)
# 从结果中提取 center_x, center_y 并点击
```

## 依赖安装

脚本会自动安装必需的依赖：

- `pyautogui`: 核心自动化库
- `pillow`: 图像处理

可选依赖（用于图像识别置信度）：

```bash
pip install opencv-python
```

## 资源索引

- [automation.py](scripts/automation.py) - 主入口脚本
- [utils.py](scripts/utils.py) - 公共工具函数
- [mouse.py](scripts/mouse.py) - 鼠标操作
- [keyboard.py](scripts/keyboard.py) - 键盘操作
- [screen.py](scripts/screen.py) - 截图和图像识别
- [color.py](scripts/color.py) - 颜色检测
- [dialog.py](scripts/dialog.py) - 对话框操作
- [system.py](scripts/system.py) - 系统信息

## 注意事项

1. **坐标系**: 屏幕左上角为原点 (0, 0)，向右为 X 增加，向下为 Y 增加
2. **权限**: Windows 上可能需要以管理员权限运行某些操作
3. **分辨率**: 多显示器环境下，坐标可能跨越多个屏幕
4. **图像识别**: 受屏幕分辨率和缩放比例影响，建议使用 confidence 参数提高鲁棒性

## 快速参考表

| 用户输入 | AI 行动      |
| -------- | ------------ |
| "xxx"    | 直接执行 xxx |
