---
name: appium-python-expert
description: >
  Specialist skill for mobile E2E testing with Appium 2.x + Python (pytest) for Android and iOS.
  Use this skill whenever the user asks about: setting up Appium with Python, writing mobile test cases,
  configuring Android/iOS drivers (UIAutomator2, XCUITest), implementing Page Object Model for mobile,
  running tests with pytest, integrating Appium tests with GitHub Actions or Jenkins, troubleshooting
  Appium sessions, capabilities configuration, or any question about mobile test automation in Python.
  Always invoke this skill for phrases like "test móvil", "appium python", "automatización android/ios",
  "pytest appium", "mobile E2E", "capabilities appium", "page object mobile", or any variation.
metadata:
  author: https://github.com/jmr85
  role: specialist
  scope: testing
  output-format: code
---

# Appium Python Expert

Specialist in mobile E2E test automation using **Appium 2.x + Python + pytest**.
Covers Android (UIAutomator2) and iOS (XCUITest), Page Object Model, Allure reports, gestures táctiles, Appium Inspector y CI/CD integration.

---

## Stack de referencia

| Layer | Tool |
|---|---|
| Appium | 2.x (drivers plugin-based) |
| Client | `Appium-Python-Client` >= 3.x |
| Test runner | `pytest` + `pytest-html` |
| Reporting | `allure-pytest` + Allure CLI |
| Android driver | `uiautomator2` |
| iOS driver | `xcuitest` |
| CI/CD | GitHub Actions, Jenkins |
| Utilities | `python-dotenv` |
| Inspector | Appium Inspector (desktop app) |

---

## Project Structure (reference)

```
project/
├── tests/
│   ├── android/
│   │   └── test_login_android.py
│   ├── ios/
│   │   └── test_login_ios.py
│   └── conftest.py
├── pages/
│   ├── base_page.py       ← gestures incluidos aquí
│   ├── login_page.py
│   └── home_page.py
├── config/
│   ├── capabilities_android.py
│   └── capabilities_ios.py
├── utils/
│   └── helpers.py
├── allure-results/        ← generado por pytest
├── allure-report/         ← generado por allure CLI
├── .env
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Quick-start guide

### 1. Install Appium 2.x and drivers

```bash
npm install -g appium@latest
appium driver install uiautomator2
appium driver install xcuitest
appium driver list --installed   # verify
```

### 2. Python dependencies (`requirements.txt`)

```
Appium-Python-Client>=3.1.0
pytest>=8.0.0
pytest-html>=4.0.0
python-dotenv>=1.0.0
allure-pytest>=2.13.0
```

> Allure también requiere el CLI separado: ver sección **Allure Reports** más abajo.

```bash
pip install -r requirements.txt
```

### 3. Environment variables (`.env`)

```env
ANDROID_APP_PATH=/abs/path/to/app.apk
IOS_APP_PATH=/abs/path/to/app.ipa
APPIUM_HOST=127.0.0.1
APPIUM_PORT=4723
ANDROID_DEVICE_NAME=emulator-5554
IOS_DEVICE_NAME=iPhone 15
IOS_PLATFORM_VERSION=17.0
```

---

## Capabilities

### Android (`config/capabilities_android.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()

ANDROID_CAPS = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": os.getenv("ANDROID_DEVICE_NAME", "emulator-5554"),
    "appium:app": os.getenv("ANDROID_APP_PATH"),
    "appium:noReset": False,
    "appium:newCommandTimeout": 120,
    "appium:autoGrantPermissions": True,
}
```

### iOS (`config/capabilities_ios.py`)

```python
import os
from dotenv import load_dotenv

load_dotenv()

IOS_CAPS = {
    "platformName": "iOS",
    "appium:automationName": "XCUITest",
    "appium:deviceName": os.getenv("IOS_DEVICE_NAME", "iPhone 15"),
    "appium:platformVersion": os.getenv("IOS_PLATFORM_VERSION", "17.0"),
    "appium:app": os.getenv("IOS_APP_PATH"),
    "appium:noReset": False,
    "appium:newCommandTimeout": 120,
    "appium:autoAcceptAlerts": True,
}
```

---

## conftest.py (driver fixture)

```python
import pytest
from appium import webdriver
from appium.options import AppiumOptions
from config.capabilities_android import ANDROID_CAPS
from config.capabilities_ios import IOS_CAPS
import os

APPIUM_URL = f"http://{os.getenv('APPIUM_HOST','127.0.0.1')}:{os.getenv('APPIUM_PORT','4723')}"

def get_driver(platform: str):
    caps = ANDROID_CAPS if platform == "android" else IOS_CAPS
    options = AppiumOptions().load_capabilities(caps)
    return webdriver.Remote(APPIUM_URL, options=options)

@pytest.fixture(scope="function")
def android_driver():
    driver = get_driver("android")
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def ios_driver():
    driver = get_driver("ios")
    yield driver
    driver.quit()
```

---

## Page Object Model

### `pages/base_page.py`

```python
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        self.find(by, value).click()

    def type_text(self, by, value, text):
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)

    def get_text(self, by, value) -> str:
        return self.find(by, value).text

    def is_visible(self, by, value) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except Exception:
            return False

    def swipe_up(self):
        size = self.driver.get_window_size()
        self.driver.swipe(
            size["width"] // 2, int(size["height"] * 0.8),
            size["width"] // 2, int(size["height"] * 0.2),
            duration=500
        )
```

### `pages/login_page.py`

```python
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Android locators (UIAutomator2)
    USERNAME_FIELD  = (AppiumBy.ACCESSIBILITY_ID, "username_input")
    PASSWORD_FIELD  = (AppiumBy.ACCESSIBILITY_ID, "password_input")
    LOGIN_BUTTON    = (AppiumBy.ACCESSIBILITY_ID, "login_button")
    ERROR_MESSAGE   = (AppiumBy.ID, "com.example.app:id/error_text")

    def login(self, username: str, password: str):
        self.type_text(*self.USERNAME_FIELD, username)
        self.type_text(*self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)

    def get_error(self) -> str:
        return self.get_text(*self.ERROR_MESSAGE)

    def is_login_visible(self) -> bool:
        return self.is_visible(*self.LOGIN_BUTTON)
```

---

## Test example

### `tests/android/test_login_android.py`

```python
import pytest
from pages.login_page import LoginPage
from pages.home_page import HomePage

class TestLoginAndroid:

    def test_valid_login(self, android_driver):
        login = LoginPage(android_driver)
        home  = HomePage(android_driver)

        assert login.is_login_visible(), "Login screen not displayed"
        login.login("user@example.com", "ValidPass123")
        assert home.is_home_visible(), "Home screen not displayed after login"

    def test_invalid_login(self, android_driver):
        login = LoginPage(android_driver)

        login.login("wrong@example.com", "badpass")
        error = login.get_error()
        assert "Invalid" in error, f"Expected error message, got: {error}"

    @pytest.mark.parametrize("user,pwd", [
        ("", "pass123"),
        ("user@test.com", ""),
        ("", ""),
    ])
    def test_empty_fields(self, android_driver, user, pwd):
        login = LoginPage(android_driver)
        login.login(user, pwd)
        assert login.is_login_visible(), "Should remain on login screen"
```

---

## pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --html=reports/report.html
    --self-contained-html
    --alluredir=allure-results
markers =
    android: marks tests as android-only
    ios: marks tests as ios-only
    smoke: smoke test suite
    regression: full regression suite
```

---

## Allure Reports

### Instalación del CLI

```bash
# macOS
brew install allure

# Linux (via npm)
npm install -g allure-commandline

# Windows (via scoop)
scoop install allure
```

### Decorators en tests

```python
import allure
import pytest
from pages.login_page import LoginPage

@allure.epic("Autenticación")
@allure.feature("Login")
class TestLoginAndroid:

    @allure.story("Login exitoso")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Usuario válido puede ingresar a la app")
    def test_valid_login(self, android_driver):
        with allure.step("Abrir pantalla de login"):
            login = LoginPage(android_driver)
            assert login.is_login_visible()

        with allure.step("Ingresar credenciales válidas"):
            login.login("user@example.com", "ValidPass123")

        with allure.step("Verificar redirección a home"):
            from pages.home_page import HomePage
            assert HomePage(android_driver).is_home_visible()

    @allure.story("Login fallido")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, android_driver):
        login = LoginPage(android_driver)
        with allure.step("Intentar login con credenciales inválidas"):
            login.login("wrong@test.com", "badpass")
        with allure.step("Verificar mensaje de error"):
            assert "Invalid" in login.get_error()
```

### Screenshot automático en fallo (`conftest.py`)

```python
import allure
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("android_driver") or item.funcargs.get("ios_driver")
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG
            )
```

### Generar y abrir reporte

```bash
# Correr tests
pytest tests/android/ -m smoke

# Generar reporte HTML
allure generate allure-results --clean -o allure-report

# Abrir en browser
allure open allure-report

# Modo serve (live)
allure serve allure-results
```

---

## Appium Inspector

Para detalles completos de configuración y uso → `references/appium_inspector.md`

### Conexión rápida

1. Descargar desde [https://github.com/appium/appium-inspector/releases](https://github.com/appium/appium-inspector/releases)
2. Appium Server URL: `http://127.0.0.1:4723`
3. Pegar capabilities JSON y hacer click en **Start Session**

### Capabilities JSON para Inspector (Android)

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:deviceName": "emulator-5554",
  "appium:app": "/abs/path/to/app.apk",
  "appium:noReset": true
}
```

### Estrategias de localización en Inspector

| Estrategia | Usar cuando |
|---|---|
| Accessibility ID | El elemento tiene `content-desc` (Android) o `accessibilityIdentifier` (iOS) |
| ID | `resource-id` en Android |
| XPath | Último recurso; copiar desde Inspector y simplificar |
| `-android uiautomator` | Búsquedas complejas en Android (texto, clase, índice) |
| `-ios predicate string` | iOS: `label`, `name`, `value`, `type` |
| `-ios class chain` | iOS: jerarquía de elementos |

---

## Gestures táctiles

Para referencia completa con todos los gestures → `references/gestures.md`

### W3C Actions API (recomendado, Appium 2.x)

```python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

def _touch_action(driver):
    """Helper: devuelve un PointerInput táctil."""
    return PointerInput(interaction.POINTER_TOUCH, "touch")
```

### Gestures en `pages/base_page.py` (extendido)

```python
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction

class BasePage:
    DEFAULT_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ── Métodos básicos ──────────────────────────────────────────────

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def click(self, by, value):
        self.find(by, value).click()

    def type_text(self, by, value, text):
        el = self.find(by, value)
        el.clear()
        el.send_keys(text)

    def get_text(self, by, value) -> str:
        return self.find(by, value).text

    def is_visible(self, by, value) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except Exception:
            return False

    # ── Gestures W3C ────────────────────────────────────────────────

    def _get_size(self):
        return self.driver.get_window_size()

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int = 500):
        """Swipe genérico de un punto a otro."""
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=touch)
        (actions.w3c_actions
            .pointer_action
            .move_to_location(start_x, start_y)
            .pointer_down()
            .pause(duration_ms / 1000)
            .move_to_location(end_x, end_y)
            .pointer_up())
        actions.perform()

    def swipe_up(self, percent: float = 0.6):
        """Scroll hacia arriba (descubrir contenido debajo)."""
        size = self._get_size()
        cx = size["width"] // 2
        self.swipe(cx, int(size["height"] * 0.8), cx, int(size["height"] * (0.8 - percent)))

    def swipe_down(self, percent: float = 0.6):
        """Scroll hacia abajo (pull-to-refresh o volver arriba)."""
        size = self._get_size()
        cx = size["width"] // 2
        self.swipe(cx, int(size["height"] * 0.2), cx, int(size["height"] * (0.2 + percent)))

    def swipe_left(self, percent: float = 0.6):
        """Swipe a la izquierda (carousels, tabs, delete)."""
        size = self._get_size()
        cy = size["height"] // 2
        self.swipe(int(size["width"] * 0.8), cy, int(size["width"] * (0.8 - percent)), cy)

    def swipe_right(self, percent: float = 0.6):
        """Swipe a la derecha (volver, abrir drawer)."""
        size = self._get_size()
        cy = size["height"] // 2
        self.swipe(int(size["width"] * 0.2), cy, int(size["width"] * (0.2 + percent)), cy)

    def swipe_on_element(self, element, direction: str = "up"):
        """Swipe dentro de un elemento (listas, sliders)."""
        loc = element.location
        sz  = element.size
        cx  = loc["x"] + sz["width"] // 2
        if direction == "up":
            self.swipe(cx, loc["y"] + int(sz["height"] * 0.8),
                       cx, loc["y"] + int(sz["height"] * 0.2))
        elif direction == "down":
            self.swipe(cx, loc["y"] + int(sz["height"] * 0.2),
                       cx, loc["y"] + int(sz["height"] * 0.8))

    def long_press(self, by, value, duration_ms: int = 1500):
        """Long press sobre un elemento."""
        el = self.find(by, value)
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=touch)
        (actions.w3c_actions
            .pointer_action
            .move_to_location(el.location["x"] + el.size["width"] // 2,
                              el.location["y"] + el.size["height"] // 2)
            .pointer_down()
            .pause(duration_ms / 1000)
            .pointer_up())
        actions.perform()

    def double_tap(self, by, value):
        """Doble tap sobre un elemento."""
        el = self.find(by, value)
        cx = el.location["x"] + el.size["width"] // 2
        cy = el.location["y"] + el.size["height"] // 2
        touch = PointerInput(interaction.POINTER_TOUCH, "touch")
        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=touch)
        (actions.w3c_actions
            .pointer_action
            .move_to_location(cx, cy)
            .pointer_down().pointer_up()
            .pause(0.1)
            .pointer_down().pointer_up())
        actions.perform()

    def pinch_zoom(self, scale: float = 2.0):
        """
        Pinch (scale < 1.0) o zoom (scale > 1.0) en el centro de la pantalla.
        Requiere dos dedos simultáneos.
        """
        size   = self._get_size()
        cx, cy = size["width"] // 2, size["height"] // 2
        offset = int(min(cx, cy) * 0.3)

        f1 = PointerInput(interaction.POINTER_TOUCH, "finger1")
        f2 = PointerInput(interaction.POINTER_TOUCH, "finger2")

        if scale >= 1.0:   # zoom in
            f1_start, f1_end = cx - offset, cx - int(offset * scale)
            f2_start, f2_end = cx + offset, cx + int(offset * scale)
        else:              # pinch out
            f1_start, f1_end = cx - int(offset * scale), cx - offset
            f2_start, f2_end = cx + int(offset * scale), cx + offset

        actions = ActionChains(self.driver)
        actions.w3c_actions = ActionBuilder(self.driver, mouse=f1, wheel=f2)
        (actions.w3c_actions.pointer_action
            .move_to_location(f1_start, cy).pointer_down()
            .move_to_location(f1_end, cy).pointer_up())
        actions.perform()

    def scroll_to_element(self, by, value, max_swipes: int = 5) -> bool:
        """Hace swipe_up hasta encontrar el elemento. Retorna True si lo encontró."""
        for _ in range(max_swipes):
            try:
                el = self.driver.find_element(by, value)
                if el.is_displayed():
                    return True
            except Exception:
                pass
            self.swipe_up()
        return False

    def drag_and_drop(self, source_by, source_val, target_by, target_val):
        """Arrastra un elemento sobre otro."""
        src = self.find(source_by, source_val)
        tgt = self.find(target_by, target_val)
        sx = src.location["x"] + src.size["width"] // 2
        sy = src.location["y"] + src.size["height"] // 2
        tx = tgt.location["x"] + tgt.size["width"] // 2
        ty = tgt.location["y"] + tgt.size["height"] // 2
        self.swipe(sx, sy, tx, ty, duration_ms=1000)
```

### Ejemplo de uso en test

```python
@allure.story("Carrusel de productos")
def test_carousel_swipe(self, android_driver):
    page = ProductPage(android_driver)
    with allure.step("Hacer swipe left en el carrusel"):
        page.swipe_left()
    with allure.step("Verificar segundo item visible"):
        assert page.is_second_item_visible()

@allure.story("Lista de items")
def test_scroll_to_bottom(self, android_driver):
    page = ListPage(android_driver)
    with allure.step("Scroll hasta el último elemento"):
        found = page.scroll_to_element(AppiumBy.ACCESSIBILITY_ID, "last_item")
    assert found, "No se encontró el último elemento tras 5 swipes"
```

---

## CI/CD Integration

For detailed CI/CD pipeline code, read the reference files:

- **GitHub Actions** → `references/ci_github_actions.md` (incluye paso de Allure)
- **Jenkins** → `references/ci_jenkins.md` (incluye publicación de Allure)
- **Appium Inspector** → `references/appium_inspector.md`
- **Gestures avanzados** → `references/gestures.md`

---

## Common troubleshooting

| Error | Likely cause | Fix |
|---|---|---|
| `Could not find a connected Android device` | ADB not seeing device | `adb devices`, enable USB debugging |
| `An unknown server-side error occurred` | Driver not installed | `appium driver install uiautomator2` |
| `Session not created: No matching capabilities` | Wrong caps key | Use `appium:` prefix for non-W3C caps |
| `Element not found` / timeout | Locator wrong or timing | Use Appium Inspector to re-check locator |
| `WebDriverException: Message: unknown error` | App crashed | Check device logs: `adb logcat` |
| iOS `xcodebuild` fails | Provisioning/Xcode mismatch | Check Xcode version + `appium driver update xcuitest` |

---

## Locator strategy priority (best practice)

1. `ACCESSIBILITY_ID` — most stable, cross-platform
2. `ID` (resource-id on Android, accessibility id on iOS)
3. `XPATH` — last resort, fragile
4. `-android uiautomator` / `-ios predicate string` — platform-specific power locators

---

## Key imports cheatsheet

```python
from appium import webdriver
from appium.options import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Gestures W3C
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
# Allure
import allure
```