---
name: os-use
description: Cross-platform operating system automation and screen control toolkit. Use when users need screenshots, mouse/keyboard control, visual recognition, window management, browser automation, or desktop automation tasks. Supports macOS 12+ and Windows 10+. On macOS, uses AppleScript, pyautogui, and OpenCV. On Windows, uses pywinauto, pyautogui, and OpenCV (no Hammerspoon equivalent).
---

# OS Use - Cross-Platform OS Automation

A comprehensive cross-platform toolkit for OS automation, screenshot capture, visual recognition, mouse/keyboard control, and window management. Supports **macOS 12+** and **Windows 10+**.

## Platform Support Matrix

| Feature | macOS Implementation | Windows Implementation |
|---------|---------------------|----------------------|
| **Screenshot** | `pyautogui` + `PIL` | `pyautogui` + `PIL` |
| **Visual Recognition** | `opencv-python` + `pyautogui` | `opencv-python` + `pyautogui` |
| **Mouse/Keyboard** | `pyautogui` | `pyautogui` |
| **Window Management** | `AppleScript` (native) | `pywinauto` / `pygetwindow` |
| **Application Control** | `AppleScript` / `subprocess` | `subprocess` / `pywinauto` |
| **Browser Automation** | Chrome DevTools MCP | Chrome DevTools MCP |

## Capabilities

### 1. Screenshot Capture 📸

**Universal (macOS & Windows):**
- Full screen capture
- Region capture (specified coordinates)
- Window capture (specific application window)
- Clipboard screenshot access

**Implementation:** `pyautogui.screenshot()` + `PIL.Image`

### 2. Visual Recognition 👁️

**Universal (macOS & Windows):**
- Image matching/locating on screen
- Template matching with confidence threshold
- Multi-scale matching (handle different resolutions)
- Color detection and region extraction

**Optional OCR:**
- Text recognition from screenshots (requires `pytesseract` + Tesseract OCR engine)

**Implementation:** `opencv-python` + `pyautogui.locateOnScreen()`

### 3. Mouse & Keyboard Control 🖱️⌨️

**Universal (macOS & Windows):**
- Mouse movement (absolute and relative coordinates)
- Mouse clicking (left, right, middle, double-click)
- Mouse dragging and dropping
- Scroll wheel operations
- Keyboard text input
- Keyboard shortcuts and hotkeys
- Special key combinations

**Implementation:** `pyautogui`

### 4. Window Management 🪟

**macOS Implementation:**
- List all application windows
- Get window position, size, title
- Activate/minimize/close windows
- Move and resize windows
- Launch/quit applications

**Implementation:** `AppleScript` via `subprocess`

**Windows Implementation:**
- Same capabilities as macOS
- Additional: Get window handle (HWND), process information
- Better integration with Windows window manager

**Implementation:** `pywinauto` or `pygetwindow`

### 5. Browser Automation 🌐

**Universal (macOS & Windows):**
- Webpage screenshots
- Element screenshots
- Page navigation
- Form filling and clicking
- Network monitoring
- Performance analysis

**Implementation:** Chrome DevTools MCP (separate tool)

### 6. System Integration 🔧

**Clipboard Operations:**
- Read/write clipboard content
- Support images and text

**Implementation:** `pyperclip` + `pyautogui`

## Technical Implementation Details

### Python Environment Setup

```bash
# Create virtual environment
python3 -m venv ~/.nanobot/workspace/macos-automation/.venv

# Activate
source ~/.nanobot/workspace/macos-automation/.venv/bin/activate

# Install dependencies
pip install pyautogui opencv-python-headless numpy Pillow pyperclip

# macOS specific
# (AppleScript is built-in, no installation needed)

# Windows specific
pip install pywinauto pygetwindow
```

### Key Libraries Reference

| Library | Version | Purpose |
|---------|---------|---------|
| `pyautogui` | 0.9.54+ | Screenshot, mouse/keyboard control |
| `opencv-python-headless` | 4.11.0.84+ | Image recognition, computer vision |
| `numpy` | 2.4.2+ | Numerical operations for OpenCV |
| `Pillow` | 12.1.1+ | Image processing |
| `pyperclip` | Latest | Clipboard operations |
| `pywinauto` | Latest | Windows window management |
| `pygetwindow` | Latest | Cross-platform window control |

### Platform-Specific Notes

#### macOS Specifics

**Permissions Required:**
- **Accessibility**: System Settings > Privacy & Security > Accessibility
- **Screen Recording**: System Settings > Privacy & Security > Screen Recording

**AppleScript Quirks:**
- Some modern apps (e.g., Chrome) may have limited AppleScript support
- Window titles may be truncated or localized
- Some operations require app to be frontmost

**Coordinate System:**
- Origin (0, 0) at top-left
- Retina displays: pyautogui automatically handles scaling

#### Windows Specifics

**Administrator Privileges:**
- Some operations (e.g., interacting with elevated windows) may require admin rights

**High DPI Displays:**
- Windows scaling may affect coordinate accuracy
- Use `pyautogui.size()` to get actual screen dimensions

**Window Handle (HWND):**
- Windows provides low-level window handles for precise control
- `pywinauto` provides both high-level and low-level access

### Error Handling Patterns

```python
import pyautogui
import time

# Pattern 1: Retry with backoff
def retry_with_backoff(func, max_retries=3, base_delay=1):
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if i == max_retries - 1:
                raise
            delay = base_delay * (2 ** i)
            print(f"Retry {i+1}/{max_retries} after {delay}s: {e}")
            time.sleep(delay)

# Pattern 2: Safe operations with fallback
def safe_screenshot(output_path):
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(output_path)
        return output_path
    except Exception as e:
        print(f"Screenshot failed: {e}")
        return None

# Pattern 3: Coordinate boundary checking
def safe_click(x, y, max_x=None, max_y=None):
    """安全点击，确保坐标在屏幕范围内"""
    if max_x is None or max_y is None:
        max_x, max_y = pyautogui.size()
    
    x = max(0, min(x, max_x - 1))
    y = max(0, min(y, max_y - 1))
    
    pyautogui.click(x, y)
```

## Usage Examples by Scenario

### Scenario 1: Automated Testing

```python
"""
自动化 UI 测试示例
测试一个假设的登录页面
"""
import pyautogui
import time

def test_login_flow():
    # 1. 截取初始状态
    initial_screenshot = pyautogui.screenshot()
    initial_screenshot.save("test_01_initial.png")
    
    # 2. 查找并点击登录按钮
    button_location = pyautogui.locateOnScreen(
        "login_button.png",
        confidence=0.9
    )
    if button_location:
        center = pyautogui.center(button_location)
        pyautogui.click(center.x, center.y)
        time.sleep(1)
    
    # 3. 输入用户名
    pyautogui.typewrite("testuser@example.com", interval=0.01)
    pyautogui.press('tab')
    
    # 4. 输入密码
    pyautogui.typewrite("TestPassword123", interval=0.01)
    
    # 5. 点击提交
    pyautogui.press('return')
    time.sleep(2)
    
    # 6. 验证结果
    result_screenshot = pyautogui.screenshot()
    result_screenshot.save("test_02_result.png")
    
    # 检查是否出现成功提示
    success_indicator = pyautogui.locateOnScreen(
        "success_message.png",
        confidence=0.8
    )
    
    if success_indicator:
        print("✅ 测试通过：登录成功")
        return True
    else:
        print("❌ 测试失败：未找到成功提示")
        return False

# 运行测试
if __name__ == "__main__":
    test_login_flow()
```

### Scenario 2: Data Entry Automation

```python
"""
数据录入自动化示例
将 Excel 数据自动填入网页表单
"""
import pyautogui
import pandas as pd
import time

def automate_data_entry(excel_file, form_template):
    """
    从 Excel 读取数据并自动填入表单
    
    Args:
        excel_file: Excel 文件路径
        form_template: 表单字段与 Excel 列的映射
    """
    # 1. 读取 Excel 数据
    df = pd.read_excel(excel_file)
    print(f"读取到 {len(df)} 条记录")
    
    # 2. 遍历每条记录
    for index, row in df.iterrows():
        print(f"\n正在处理第 {index + 1} 条记录...")
        
        # 3. 填写每个字段
        for field_name, column_name in form_template.items():
            value = row.get(column_name, '')
            
            # 查找表单字段（需要提前准备字段截图）
            field_location = pyautogui.locateOnScreen(
                f"form_field_{field_name}.png",
                confidence=0.8
            )
            
            if field_location:
                # 点击字段
                center = pyautogui.center(field_location)
                pyautogui.click(center.x, center.y)
                time.sleep(0.2)
                
                # 输入值
                pyautogui.hotkey('ctrl', 'a')  # 全选
                pyautogui.typewrite(str(value), interval=0.01)
                time.sleep(0.2)
            else:
                print(f"  ⚠️ 未找到字段: {field_name}")
        
        # 4. 提交表单
        submit_btn = pyautogui.locateOnScreen(
            "submit_button.png",
            confidence=0.8
        )
        if submit_btn:
            center = pyautogui.center(submit_btn)
            pyautogui.click(center.x, center.y)
            print("  ✅ 已提交")
            time.sleep(2)  # 等待提交完成
        else:
            print("  ⚠️ 未找到提交按钮")
        
        # 5. 准备下一条记录
        # 可能需要点击"添加新记录"或返回列表
        time.sleep(1)
    
    print("\n🎉 所有记录处理完成！")

# 使用示例
if __name__ == "__main__":
    # 表单模板：字段名 -> Excel 列名
    form_template = {
        "name": "姓名",
        "email": "邮箱",
        "phone": "电话",
        "address": "地址"
    }
    
    automate_data_entry("data.xlsx", form_template)
```

### Scenario 3: Screen Monitoring & Alerting

```python
"""
屏幕监控与告警示例
监控特定区域变化，发现变化时发送通知
"""
import pyautogui
import cv2
import numpy as np
import time
from datetime import datetime

def monitor_screen_region(region, template_image=None, check_interval=5, callback=None):
    """
    监控屏幕特定区域的变化
    
    Args:
        region: (left, top, width, height) 监控区域
        template_image: 要查找的模板图像路径（可选）
        check_interval: 检查间隔（秒）
        callback: 发现变化时的回调函数
    
    Returns:
        监控会话对象（可调用 stop() 停止）
    """
    class MonitorSession:
        def __init__(self):
            self.running = True
            self.baseline = None
        
        def stop(self):
            self.running = False
    
    session = MonitorSession()
    
    print(f"🔍 开始监控区域: {region}")
    print(f"⏱️  检查间隔: {check_interval}秒")
    print("按 Ctrl+C 停止监控\n")
    
    try:
        while session.running:
            # 捕获当前区域
            current = pyautogui.screenshot(region=region)
            current_array = np.array(current)
            
            if template_image:
                # 模式1: 查找模板图像
                template_location = pyautogui.locateOnScreen(
                    template_image,
                    confidence=0.8
                )
                
                if template_location:
                    print(f"✅ [{datetime.now()}] 找到模板图像: {template_location}")
                    if callback:
                        callback('template_found', {
                            'location': template_location,
                            'screenshot': current
                        })
            else:
                # 模式2: 检测变化
                if session.baseline is None:
                    session.baseline = current_array
                    print(f"📸 [{datetime.now()}] 已建立基准图像")
                else:
                    # 计算差异
                    diff = cv2.absdiff(session.baseline, current_array)
                    diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                    diff_score = np.mean(diff_gray)
                    
                    if diff_score > 10:  # 阈值可调
                        print(f"⚠️  [{datetime.now()}] 检测到变化! 差异分数: {diff_score:.2f}")
                        if callback:
                            callback('change_detected', {
                                'diff_score': diff_score,
                                'screenshot': current,
                                'baseline': session.baseline
                            })
                        # 更新基准
                        session.baseline = current_array
            
            time.sleep(check_interval)
    
    except KeyboardInterrupt:
        print("\n🛑 监控已停止")
    
    return session

# 使用示例
def alert_callback(event_type, data):
    """告警回调函数示例"""
    if event_type == 'template_found':
        print(f"🎯 模板出现在: {data['location']}")
        # 可以在这里发送通知、发送邮件、执行操作等
    elif event_type == 'change_detected':
        print(f"📊 变化强度: {data['diff_score']}")
        # 保存差异图像
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data['screenshot'].save(f"change_{timestamp}.png")

if __name__ == "__main__":
    # 示例1: 监控屏幕变化
    print("=== 监控屏幕变化 ===")
    monitor = monitor_screen_region(
        region=(0, 0, 1920, 1080),  # 全屏
        check_interval=5,           # 每5秒检查一次
        callback=alert_callback
    )
    
    # 10分钟后停止（实际使用可以一直运行）
    # time.sleep(600)
    # monitor.stop()
    
    # 示例2: 查找特定图像
    # monitor = monitor_screen_region(
    #     region=(0, 0, 1920, 1080),
    #     template_image="target_button.png",  # 要查找的图像
    #     check_interval=2,
    #     callback=alert_callback
    # )
```

## Advanced Techniques

### Handling Multiple Monitors

```python
import pyautogui

def get_all_screen_sizes():
    """获取所有显示器尺寸（仅 Windows 支持多显示器详细信息）"""
    # macOS 返回主屏尺寸
    # Windows 可以使用 pygetwindow 或 win32api 获取多显示器信息
    
    primary = pyautogui.size()
    print(f"主屏幕尺寸: {primary}")
    
    # Windows 示例（需要安装 pywin32）
    try:
        import win32api
        monitors = win32api.EnumDisplayMonitors()
        for i, monitor in enumerate(monitors):
            print(f"显示器 {i+1}: {monitor[2]}")
    except ImportError:
        pass
    
    return primary

def screenshot_specific_monitor(monitor_num=0):
    """截图指定显示器（实验性功能）"""
    # 目前 pyautogui 主要支持主显示器
    # 多显示器支持需要平台特定代码
    pass
```

### Performance Optimization

```python
import cv2
import numpy as np
import pyautogui
import time
from functools import lru_cache

class ScreenCache:
    """屏幕缓存优化器"""
    
    def __init__(self, cache_duration=0.5):
        self.cache_duration = cache_duration
        self.last_capture = None
        self.last_capture_time = 0
    
    def get_screenshot(self, region=None):
        """获取截图（带缓存）"""
        current_time = time.time()
        
        # 检查缓存是否有效
        if (self.last_capture is not None and 
            current_time - self.last_capture_time < self.cache_duration and
            region is None):
            return self.last_capture
        
        # 捕获新截图
        screenshot = pyautogui.screenshot(region=region)
        
        if region is None:
            self.last_capture = screenshot
            self.last_capture_time = current_time
        
        return screenshot
    
    def clear_cache(self):
        """清除缓存"""
        self.last_capture = None
        self.last_capture_time = 0

class FastImageFinder:
    """快速图像查找器（使用多尺度金字塔）"""
    
    def __init__(self, scales=[0.8, 0.9, 1.0, 1.1, 1.2]):
        self.scales = scales
    
    def find_multi_scale(self, template_path, screenshot=None, confidence=0.8):
        """
        多尺度图像查找
        
        Returns:
            (x, y, scale) 或 None
        """
        if screenshot is None:
            screenshot = pyautogui.screenshot()
        
        template = cv2.imread(template_path)
        if template is None:
            return None
        
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        for scale in self.scales:
            # 缩放模板
            scaled_template = cv2.resize(
                template,
                None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_AREA
            )
            
            # 模板匹配
            result = cv2.matchTemplate(
                screenshot_cv,
                scaled_template,
                cv2.TM_CCOEFF_NORMED
            )
            
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= confidence:
                h, w = scaled_template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return (center_x, center_y, scale)
        
        return None

# 使用示例
cache = ScreenCache()
finder = FastImageFinder()

# 快速截图（带缓存）
screenshot = cache.get_screenshot()

# 多尺度图像查找
result = finder.find_multi_scale("button.png", screenshot)
if result:
    x, y, scale = result
    print(f"找到图像: ({x}, {y}), 缩放: {scale}")
```

### Security Considerations

```python
"""
安全最佳实践
"""

import pyautogui
import hashlib
import time

class SecureAutomation:
    """安全自动化包装器"""
    
    def __init__(self):
        self.action_log = []
        self.max_retries = 3
        self.rate_limit_delay = 0.1  # 操作间隔
    
    def log_action(self, action, details):
        """记录操作日志"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'action': action,
            'details': details,
            'hash': hashlib.md5(f"{timestamp}{action}{details}".encode()).hexdigest()[:8]
        }
        self.action_log.append(log_entry)
    
    def safe_click(self, x, y, description=""):
        """安全点击（带验证）"""
        try:
            # 验证坐标在屏幕范围内
            screen_width, screen_height = pyautogui.size()
            if not (0 <= x < screen_width and 0 <= y < screen_height):
                raise ValueError(f"坐标 ({x}, {y}) 超出屏幕范围")
            
            # 执行点击
            pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(self.rate_limit_delay)
            pyautogui.click()
            
            # 记录日志
            self.log_action('click', f"({x}, {y}) - {description}")
            
            return True
            
        except Exception as e:
            self.log_action('click_failed', f"({x}, {y}) - Error: {str(e)}")
            return False
    
    def safe_typewrite(self, text, interval=0.01):
        """安全输入（敏感信息不记录）"""
        try:
            pyautogui.typewrite(text, interval=interval)
            self.log_action('typewrite', f"输入 {len(text)} 个字符 [内容已隐藏]")
            return True
        except Exception as e:
            self.log_action('typewrite_failed', f"Error: {str(e)}")
            return False
    
    def get_action_report(self):
        """生成操作报告"""
        total = len(self.action_log)
        successful = sum(1 for log in self.action_log if 'failed' not in log['action'])
        failed = total - successful
        
        report = f"""
=== 自动化操作报告 ===
总操作数: {total}
成功: {successful}
失败: {failed}
成功率: {(successful/total*100):.1f}%

详细日志:
"""
        for log in self.action_log:
            report += f"[{log['timestamp']}] [{log['hash']}] {log['action']}: {log['details']}\n"
        
        return report

# 使用示例
secure = SecureAutomation()

# 执行安全操作
secure.safe_click(500, 400, "登录按钮")
secure.safe_typewrite("username@example.com")
secure.safe_click(500, 450, "密码输入框")
secure.safe_typewrite("********")
secure.safe_click(500, 500, "提交按钮")

# 生成报告
print(secure.get_action_report())
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Permission Errors

**Symptom:** `pyautogui` fails with permission errors or captures black screenshots.

**macOS Solution:**
1. Open System Settings > Privacy & Security > Accessibility
2. Add your terminal application (e.g., Terminal.app, iTerm.app, or the Python executable)
3. Repeat for Screen Recording permission

**Windows Solution:**
1. Run as Administrator if needed
2. Check Windows Defender or antivirus isn't blocking

#### 2. Coordinate Inaccuracy

**Symptom:** Clicks or screenshots miss the intended target.

**Possible Causes:**
- High DPI / Retina display scaling
- Multiple monitors with different resolutions
- Window decorations or taskbar affecting coordinates

**Solution:**
```python
import pyautogui

# Debug: Print screen info
print(f"Screen size: {pyautogui.size()}")
print(f"Mouse position: {pyautogui.position()}")

# Handle high DPI (Windows)
import ctypes
ctypes.windll.user32.SetProcessDPIAware()  # Windows only
```

#### 3. Image Recognition Failures

**Symptom:** `locateOnScreen` returns None even when image is visible.

**Common Causes:**
- Resolution mismatch (captured image at different scale)
- Color depth differences
- Transparency or alpha channel issues
- Confidence threshold too high

**Solutions:**
```python
import pyautogui
import cv2
import numpy as np

# Solution 1: Lower confidence
location = pyautogui.locateOnScreen('button.png', confidence=0.7)  # Default is 0.9

# Solution 2: Multi-scale matching (see FastImageFinder class in Performance section)
finder = FastImageFinder(scales=[0.5, 0.75, 1.0, 1.25, 1.5])
result = finder.find_multi_scale('button.png')

# Solution 3: Convert to grayscale for matching
screenshot = pyautogui.screenshot()
screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
template = cv2.imread('button.png', cv2.IMREAD_GRAYSCALE)

result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

if max_val >= 0.8:
    print(f"找到匹配，置信度: {max_val}")
    h, w = template.shape
    center_x = max_loc[0] + w // 2
    center_y = max_loc[1] + h // 2
    pyautogui.click(center_x, center_y)
```

#### 4. Slow Performance

**Symptom:** Operations are slow, high CPU usage, or noticeable delays.

**Optimization Strategies:**

1. **Reduce Screenshot Frequency**
   - Cache screenshots when possible
   - Use region-specific captures instead of full screen
   
2. **Optimize Image Matching**
   - Resize large images before matching
   - Use grayscale matching when color isn't important
   - Set appropriate confidence levels
   
3. **Batch Operations**
   - Group multiple actions together
   - Minimize unnecessary delays

See the "Performance Optimization" section for detailed code examples.

#### 5. Application-Specific Issues

**Browser Automation:**
- Modern browsers may block automation
- Use Chrome DevTools Protocol instead of pyautogui for web
- Consider Playwright or Selenium for complex web automation

**Game/Graphics Applications:**
- DirectX/OpenGL apps may not be capturable by standard screenshot
- May require specialized tools (e.g., OBS Studio's capture API)

**Protected Content:**
- DRM-protected content (Netflix, etc.) cannot be screenshotted
- This is a system-level restriction

## Integration with Other Tools

### With ChatGPT/AI Assistants

This skill is designed to work with AI assistants like nanobot. Here's how to integrate:

```python
# Example: AI assistant using this skill

def ai_assisted_automation(user_request):
    """
    AI 助手使用自动化技能
    
    Args:
        user_request: 用户的自然语言请求
    """
    # 1. AI 解析用户意图
    intent = parse_intent(user_request)
    
    if intent == 'screenshot':
        # 2. 执行截图
        screenshot = pyautogui.screenshot()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshot_{timestamp}.png"
        screenshot.save(path)
        return f"已截图并保存到: {path}"
    
    elif intent == 'click_button':
        # 2. 查找并点击按钮
        button_name = extract_button_name(user_request)
        location = pyautogui.locateOnScreen(f"{button_name}.png")
        if location:
            pyautogui.click(pyautogui.center(location))
            return f"已点击按钮: {button_name}"
        else:
            return f"未找到按钮: {button_name}"
    
    # ... 其他意图处理
```

### With CI/CD Pipelines

```yaml
# Example: GitHub Actions using this skill for visual testing

name: Visual Regression Tests

on: [push, pull_request]

jobs:
  visual-test:
    runs-on: macos-latest  # or windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pyautogui opencv-python-headless numpy Pillow
    
    - name: Run visual tests
      run: python tests/visual_regression.py
    
    - name: Upload screenshots
      uses: actions/upload-artifact@v3
      with:
        name: screenshots
        path: screenshots/
```

### With Monitoring Systems

```python
# Example: Integration with Prometheus/Grafana for screen monitoring

from prometheus_client import Gauge, start_http_server
import pyautogui
import time

# Define metrics
screen_change_gauge = Gauge('screen_change_score', 'Screen change detection score')
template_match_gauge = Gauge('template_match_confidence', 'Template matching confidence')

start_http_server(8000)

def monitoring_loop():
    baseline = None
    
    while True:
        # Capture screen
        current = pyautogui.screenshot()
        current_array = np.array(current)
        
        if baseline is not None:
            # Calculate change
            diff = cv2.absdiff(baseline, current_array)
            diff_score = np.mean(diff)
            screen_change_gauge.set(diff_score)
        
        baseline = current_array
        
        # Check for template
        try:
            location = pyautogui.locateOnScreen('alert_icon.png', confidence=0.8)
            if location:
                template_match_gauge.set(1.0)
            else:
                template_match_gauge.set(0.0)
        except:
            template_match_gauge.set(0.0)
        
        time.sleep(5)

monitoring_loop()
```

## Future Roadmap

### Planned Features

1. **Linux Support**
   - X11 and Wayland compatibility
   - `xdotool` and `scrot` integration
   - `mss` for multi-monitor support

2. **AI-Powered Recognition**
   - Integration with OpenAI GPT-4V or Google Gemini for visual understanding
   - Natural language element finding ("click the blue submit button")
   - OCR-free text extraction using vision models

3. **Mobile Device Support**
   - Android: ADB (Android Debug Bridge) integration
   - iOS: WebDriverAgent via Appium
   - Screenshot and touch simulation

4. **Cloud Integration**
   - AWS Lambda support for serverless automation
   - Azure Functions and GCP Cloud Functions compatibility
   - Distributed screenshot processing

5. **Advanced Analytics**
   - Built-in A/B testing framework for UI changes
   - Heatmap generation from user interactions
   - Performance regression detection

## Contributing

We welcome contributions! Please see the [Contributing Guide](CONTRIBUTING.md) for details on:

- Code style and formatting
- Testing requirements
- Documentation standards
- Pull request process

## License

This skill is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Last Updated:** 2026-03-06  
**Version:** 1.0.0  
**Maintainer:** nanobot skills team
