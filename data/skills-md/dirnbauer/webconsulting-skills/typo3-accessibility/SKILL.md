---
name: typo3-accessibility
description: >-
  WCAG 2.2 AA accessibility audit and implementation for TYPO3 v12–v14 (v14 preferred).
  Covers Fluid template patterns, PHP middleware, JavaScript enhancements, Content Element
  accessibility, form accessibility, and a full go-live checklist. Use when working with
  accessibility, a11y, wcag, aria, screen reader, keyboard navigation, focus management,
  color contrast, alt text, semantic html, skip link, or accessible forms in TYPO3.
compatibility: TYPO3 12.4 - 14.x
metadata:
  version: "1.0.0"
---

# TYPO3 Accessibility (WCAG 2.2 AA)

> **Compatibility:** TYPO3 v14.x (primary), v13.x, v12.4 LTS (fallbacks noted).
> All code works on v14. Version-specific fallbacks are marked with `v12/v13:`.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, Fluid ViewHelpers, and core
> features before adding custom markup. Verify methods exist in your target version.

> **PHP & JS over TypoScript:** This skill provides PHP middleware, Fluid partials, and
> vanilla JavaScript solutions. TypoScript examples are avoided; use PHP-based approaches.

## 1. Accessibility Checklist (Go-Live Gate)

Run through this checklist before every deployment. Mark items as you fix them.

### Semantic Structure
- [ ] Every page has exactly one `<h1>`
- [ ] Heading hierarchy is sequential (`h1` > `h2` > `h3`, no skips)
- [ ] Landmark elements used: `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`
- [ ] Skip-to-content link is the first focusable element
- [ ] `<html lang="...">` matches page language
- [ ] Language changes within content use `lang` attribute on containing element

### Images & Media
- [ ] All `<img>` have `alt` attribute (empty `alt=""` for decorative)
- [ ] All `<img>` have explicit `width` and `height` (prevents CLS)
- [ ] Complex images (charts, infographics) have long description
- [ ] Videos have captions/subtitles
- [ ] Audio content has transcript
- [ ] No auto-playing media with sound

### Color & Contrast
- [ ] Text contrast >= 4.5:1 (normal) / 3:1 (large text >= 24px / 18.66px bold)
- [ ] UI components and graphical objects >= 3:1 contrast
- [ ] Information not conveyed by color alone (add icon, text, or pattern)
- [ ] Dark mode (if implemented) maintains contrast ratios

### Keyboard & Focus
- [ ] All interactive elements reachable via Tab
- [ ] Focus order matches visual order
- [ ] Visible focus indicator on all interactive elements (`:focus-visible`)
- [ ] No focus traps (except modals — which must trap correctly)
- [ ] Escape closes modals/overlays and returns focus to trigger
- [ ] Custom widgets have correct keyboard handlers

### Forms
- [ ] Every input has a programmatic `<label>` (explicit `for`/`id` or wrapping)
- [ ] Placeholder is not used as sole label
- [ ] Required fields indicated visually and with `required` attribute
- [ ] Error messages linked to inputs via `aria-describedby` + `aria-invalid`
- [ ] Form groups use `<fieldset>` + `<legend>`
- [ ] Correct `type` and `autocomplete` attributes on inputs

### ARIA & Dynamic Content
- [ ] Icon-only buttons have `aria-label`
- [ ] Decorative icons have `aria-hidden="true"`
- [ ] Dynamic updates use `aria-live="polite"` or `role="status"`
- [ ] Error alerts use `role="alert"`
- [ ] Active navigation links have `aria-current="page"`
- [ ] Expandable elements use `aria-expanded`

### Motion & Interaction
- [ ] `prefers-reduced-motion` respected (CSS and JS)
- [ ] No content flashes more than 3 times per second
- [ ] Touch targets >= 44x44 CSS pixels
- [ ] `user-scalable=no` is NOT set in viewport meta

### TYPO3-Specific
- [ ] Backend: alt text fields are filled for all images in File List
- [ ] Backend: content elements have descriptive headers (or `header_layout = 100` for hidden)
- [ ] Backend: page properties have proper `<title>` and `description`
- [ ] Fluid templates use `<f:link.page>` / `<f:link.typolink>` (not `<a>` with manual hrefs)
- [ ] Content Block / Content Element templates follow accessible patterns below

## 2. Fluid Template Patterns

### 2.1 Page Layout with Landmarks

```html
<!-- EXT:site_package/Resources/Private/Layouts/Default.html -->
<f:layout name="Default" />

<f:render section="Main" />
```

```html
<!-- EXT:site_package/Resources/Private/Templates/Default.html -->
<f:layout name="Default" />
<f:section name="Main">

<a href="#main-content" class="skip-link">
    <f:translate key="LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:skip_to_content" />
</a>

<header role="banner">
    <nav aria-label="{f:translate(key: 'LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:nav.main')}">
        <f:cObject typoscriptObjectPath="lib.mainNavigation" />
    </nav>
</header>

<main id="main-content">
    <f:render section="Content" />
</main>

<footer>
    <nav aria-label="{f:translate(key: 'LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:nav.footer')}">
        <f:cObject typoscriptObjectPath="lib.footerNavigation" />
    </nav>
</footer>

</f:section>
```

### 2.2 Skip Link CSS

```css
.skip-link {
    position: absolute;
    top: -100%;
    left: 0;
    z-index: 10000;
    padding: 0.75rem 1.5rem;
    background: var(--color-primary, #2563eb);
    color: var(--color-on-primary, #fff);
    font-weight: 600;
    text-decoration: none;
}
.skip-link:focus {
    top: 0;
}
```

### 2.3 Accessible Image Rendering

```html
<!-- Partial: Resources/Private/Partials/Media/Image.html -->
<f:if condition="{image}">
    <figure>
        <f:image
            image="{image}"
            alt="{image.alternative}"
            title="{image.title}"
            width="{dimensions.width}"
            height="{dimensions.height}"
            loading="{f:if(condition: '{lazyLoad}', then: 'lazy', else: 'eager')}"
        />
        <f:if condition="{image.description}">
            <figcaption>{image.description}</figcaption>
        </f:if>
    </figure>
</f:if>
```

For decorative images (no informational value):

```html
<f:image image="{image}" alt="" role="presentation" />
```

### 2.4 Accessible Content Element Wrapper

```html
<!-- Partial: Resources/Private/Partials/ContentElement/Header.html -->
<f:if condition="{data.header} && {data.header_layout} != 100">
    <f:switch expression="{data.header_layout}">
        <f:case value="1"><h1>{data.header}</h1></f:case>
        <f:case value="2"><h2>{data.header}</h2></f:case>
        <f:case value="3"><h3>{data.header}</h3></f:case>
        <f:case value="4"><h4>{data.header}</h4></f:case>
        <f:case value="5"><h5>{data.header}</h5></f:case>
        <f:defaultCase><h2>{data.header}</h2></f:defaultCase>
    </f:switch>
</f:if>
```

### 2.5 Accessible Navigation Partial

```html
<!-- Partial: Resources/Private/Partials/Navigation/MainMenu.html -->
<nav aria-label="{f:translate(key: 'LLL:EXT:site_package/Resources/Private/Language/locallang.xlf:nav.main')}">
    <ul role="list">
        <f:for each="{menu}" as="item">
            <li>
                <f:if condition="{item.active}">
                    <f:then>
                        <a href="{item.link}" aria-current="page">{item.title}</a>
                    </f:then>
                    <f:else>
                        <a href="{item.link}">{item.title}</a>
                    </f:else>
                </f:if>

                <f:if condition="{item.children}">
                    <ul>
                        <f:for each="{item.children}" as="child">
                            <li>
                                <a href="{child.link}"
                                   {f:if(condition: '{child.active}', then: 'aria-current="page"')}>
                                    {child.title}
                                </a>
                            </li>
                        </f:for>
                    </ul>
                </f:if>
            </li>
        </f:for>
    </ul>
</nav>
```

### 2.6 Accessible Accordion (Content Blocks / Custom CE)

```html
<div class="accordion" data-accordion>
    <f:for each="{items}" as="item" iteration="iter">
        <div class="accordion__item">
            <h3>
                <button
                    type="button"
                    class="accordion__trigger"
                    aria-expanded="false"
                    aria-controls="accordion-panel-{data.uid}-{iter.index}"
                    id="accordion-header-{data.uid}-{iter.index}"
                    data-accordion-trigger
                >
                    {item.header}
                </button>
            </h3>
            <div
                id="accordion-panel-{data.uid}-{iter.index}"
                role="region"
                aria-labelledby="accordion-header-{data.uid}-{iter.index}"
                class="accordion__panel"
                hidden
            >
                <f:format.html>{item.bodytext}</f:format.html>
            </div>
        </div>
    </f:for>
</div>
```

### 2.7 Accessible Tab Component

```html
<div class="tabs" data-tabs>
    <div role="tablist" aria-label="{f:translate(key: 'tabs.label')}">
        <f:for each="{items}" as="item" iteration="iter">
            <button
                type="button"
                role="tab"
                id="tab-{data.uid}-{iter.index}"
                aria-controls="tabpanel-{data.uid}-{iter.index}"
                aria-selected="{f:if(condition: '{iter.isFirst}', then: 'true', else: 'false')}"
                tabindex="{f:if(condition: '{iter.isFirst}', then: '0', else: '-1')}"
            >
                {item.header}
            </button>
        </f:for>
    </div>

    <f:for each="{items}" as="item" iteration="iter">
        <div
            role="tabpanel"
            id="tabpanel-{data.uid}-{iter.index}"
            aria-labelledby="tab-{data.uid}-{iter.index}"
            tabindex="0"
            {f:if(condition: '!{iter.isFirst}', then: 'hidden')}
        >
            <f:format.html>{item.bodytext}</f:format.html>
        </div>
    </f:for>
</div>
```

## 3. PHP: Accessibility Middleware & Helpers

### 3.1 Language Attribute Middleware (PSR-15)

Ensures `<html lang="...">` is always correct based on site language config.

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\Middleware;

use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\MiddlewareInterface;
use Psr\Http\Server\RequestHandlerInterface;
use TYPO3\CMS\Core\Attribute\AsMiddleware;
use TYPO3\CMS\Core\Site\Entity\SiteLanguage;

#[AsMiddleware(
    identifier: 'vendor/site-package/accessibility-lang',
    after: 'typo3/cms-frontend/content-length-headers',
)]
final class AccessibilityLangMiddleware implements MiddlewareInterface
{
    public function process(ServerRequestInterface $request, RequestHandlerInterface $handler): ResponseInterface
    {
        $response = $handler->handle($request);

        $siteLanguage = $request->getAttribute('language');
        if (!$siteLanguage instanceof SiteLanguage) {
            return $response;
        }

        $contentType = $response->getHeaderLine('Content-Type');
        if (!str_contains($contentType, 'text/html')) {
            return $response;
        }

        $locale = $siteLanguage->getLocale();
        $langCode = $locale->getLanguageCode();
        $body = (string)$response->getBody();

        $body = preg_replace(
            '/<html([^>]*)lang="[^"]*"/',
            '<html$1lang="' . htmlspecialchars($langCode) . '"',
            $body,
            1
        );

        $response->getBody()->rewind();
        $response->getBody()->write($body);

        return $response;
    }
}
```

**v12/v13 fallback:** Register via `Configuration/RequestMiddlewares.php` instead of the `#[AsMiddleware]` attribute:

```php
<?php
// Configuration/RequestMiddlewares.php (v12/v13)
return [
    'frontend' => [
        'vendor/site-package/accessibility-lang' => [
            'target' => \Vendor\SitePackage\Middleware\AccessibilityLangMiddleware::class,
            'after' => ['typo3/cms-frontend/content-length-headers'],
        ],
    ],
];
```

### 3.2 Image Alt Text Validation (PSR-14 Event)

Warn editors when images lack alt text:

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\DataHandling\DataHandler;
use TYPO3\CMS\Core\Messaging\FlashMessage;
use TYPO3\CMS\Core\Messaging\FlashMessageService;
use TYPO3\CMS\Core\Type\ContextualFeedbackSeverity;
use TYPO3\CMS\Core\Utility\GeneralUtility;

#[AsEventListener(identifier: 'vendor/site-package/alt-text-check')]
final class ImageAltTextValidationListener
{
    public function __construct(
        private readonly FlashMessageService $flashMessageService,
    ) {}

    public function __invoke(\TYPO3\CMS\Core\DataHandling\Event\AfterRecordPublishedEvent|object $event): void
    {
        // For DataHandler processDatamap_afterDatabaseOperations hook style usage:
        // This can be adapted as a DataHandler hook or PSR-14 event depending on version.
    }

    public function processDatamap_afterDatabaseOperations(
        string $status,
        string $table,
        string|int $id,
        array $fieldArray,
        DataHandler $dataHandler,
    ): void {
        if ($table !== 'sys_file_metadata') {
            return;
        }

        if (empty($fieldArray['alternative'] ?? '')) {
            $message = GeneralUtility::makeInstance(
                FlashMessage::class,
                'Image is missing alt text. Please add descriptive alt text for accessibility (WCAG 1.1.1).',
                'Accessibility Warning',
                ContextualFeedbackSeverity::WARNING,
                true,
            );

            $this->flashMessageService
                ->getMessageQueueByIdentifier()
                ->addMessage($message);
        }
    }
}
```

Register as DataHandler hook in `ext_localconf.php`:

```php
$GLOBALS['TYPO3_CONF_VARS']['SC_OPTIONS']['t3lib/class.t3lib_tcemain.php']['processDatamapClass'][]
    = \Vendor\SitePackage\EventListener\ImageAltTextValidationListener::class;
```

### 3.3 Accessible Fluid ViewHelper: SrOnly

Renders screen-reader-only text:

```php
<?php

declare(strict_types=1);

namespace Vendor\SitePackage\ViewHelpers;

use TYPO3Fluid\Fluid\Core\ViewHelper\AbstractTagBasedViewHelper;

final class SrOnlyViewHelper extends AbstractTagBasedViewHelper
{
    protected $tagName = 'span';

    public function initializeArguments(): void
    {
        parent::initializeArguments();
        $this->registerUniversalTagAttributes();
    }

    public function render(): string
    {
        $this->tag->addAttribute('class', 'sr-only');
        $this->tag->setContent($this->renderChildren());
        return $this->tag->render();
    }
}
```

```css
/* CSS for sr-only */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}
```

Usage in Fluid:

```html
{namespace sp = Vendor\SitePackage\ViewHelpers}
<button aria-label="{f:translate(key: 'button.close')}">
    <svg aria-hidden="true"><!-- icon --></svg>
    <sp:srOnly><f:translate key="button.close" /></sp:srOnly>
</button>
```

## 4. JavaScript: Accessible Widgets

### 4.1 Accordion

```javascript
// EXT:site_package/Resources/Public/JavaScript/accordion.js
class AccessibleAccordion {
    constructor(container) {
        this.container = container;
        this.triggers = container.querySelectorAll('[data-accordion-trigger]');
        this.init();
    }

    init() {
        this.triggers.forEach((trigger) => {
            trigger.addEventListener('click', () => this.toggle(trigger));
            trigger.addEventListener('keydown', (e) => this.handleKeydown(e));
        });
    }

    toggle(trigger) {
        const expanded = trigger.getAttribute('aria-expanded') === 'true';
        const panelId = trigger.getAttribute('aria-controls');
        const panel = document.getElementById(panelId);

        trigger.setAttribute('aria-expanded', String(!expanded));
        panel.hidden = expanded;
    }

    handleKeydown(e) {
        const triggers = [...this.triggers];
        const index = triggers.indexOf(e.currentTarget);

        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                triggers[(index + 1) % triggers.length].focus();
                break;
            case 'ArrowUp':
                e.preventDefault();
                triggers[(index - 1 + triggers.length) % triggers.length].focus();
                break;
            case 'Home':
                e.preventDefault();
                triggers[0].focus();
                break;
            case 'End':
                e.preventDefault();
                triggers[triggers.length - 1].focus();
                break;
        }
    }
}

document.querySelectorAll('[data-accordion]').forEach((el) => new AccessibleAccordion(el));
```

### 4.2 Tabs

```javascript
// EXT:site_package/Resources/Public/JavaScript/tabs.js
class AccessibleTabs {
    constructor(container) {
        this.tablist = container.querySelector('[role="tablist"]');
        this.tabs = [...this.tablist.querySelectorAll('[role="tab"]')];
        this.panels = this.tabs.map(
            (tab) => document.getElementById(tab.getAttribute('aria-controls'))
        );
        this.init();
    }

    init() {
        this.tabs.forEach((tab) => {
            tab.addEventListener('click', () => this.selectTab(tab));
            tab.addEventListener('keydown', (e) => this.handleKeydown(e));
        });
    }

    selectTab(selectedTab) {
        this.tabs.forEach((tab, i) => {
            const selected = tab === selectedTab;
            tab.setAttribute('aria-selected', String(selected));
            tab.tabIndex = selected ? 0 : -1;
            this.panels[i].hidden = !selected;
        });
        selectedTab.focus();
    }

    handleKeydown(e) {
        const index = this.tabs.indexOf(e.currentTarget);
        let next;

        switch (e.key) {
            case 'ArrowRight':
                next = (index + 1) % this.tabs.length;
                break;
            case 'ArrowLeft':
                next = (index - 1 + this.tabs.length) % this.tabs.length;
                break;
            case 'Home':
                next = 0;
                break;
            case 'End':
                next = this.tabs.length - 1;
                break;
            default:
                return;
        }
        e.preventDefault();
        this.selectTab(this.tabs[next]);
    }
}

document.querySelectorAll('[data-tabs]').forEach((el) => new AccessibleTabs(el));
```

### 4.3 Modal / Dialog

```javascript
// EXT:site_package/Resources/Public/JavaScript/dialog.js
class AccessibleDialog {
    constructor(dialog) {
        this.dialog = dialog;
        this.previousFocus = null;
        this.init();
    }

    init() {
        this.dialog.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') this.close();
            if (e.key === 'Tab') this.trapFocus(e);
        });

        this.dialog.addEventListener('click', (e) => {
            if (e.target === this.dialog) this.close();
        });
    }

    open() {
        this.previousFocus = document.activeElement;
        this.dialog.showModal();

        const firstFocusable = this.dialog.querySelector(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        firstFocusable?.focus();
    }

    close() {
        this.dialog.close();
        this.previousFocus?.focus();
    }

    trapFocus(e) {
        const focusable = this.dialog.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
        }
    }
}
```

Use the native `<dialog>` element in Fluid:

```html
<dialog id="my-dialog" aria-labelledby="dialog-title" aria-modal="true">
    <h2 id="dialog-title">{dialogTitle}</h2>
    <div>{dialogContent}</div>
    <button type="button" data-close-dialog>
        <f:translate key="button.close" />
    </button>
</dialog>
```

### 4.4 Reduced Motion Check

```javascript
// EXT:site_package/Resources/Public/JavaScript/motion.js
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function getTransitionDuration() {
    return prefersReducedMotion.matches ? 0 : 300;
}

prefersReducedMotion.addEventListener('change', () => {
    document.documentElement.classList.toggle('reduce-motion', prefersReducedMotion.matches);
});

if (prefersReducedMotion.matches) {
    document.documentElement.classList.add('reduce-motion');
}
```

```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
```

### 4.5 Live Region Announcer

```javascript
// EXT:site_package/Resources/Public/JavaScript/announcer.js
class LiveAnnouncer {
    constructor() {
        this.region = document.createElement('div');
        this.region.setAttribute('aria-live', 'polite');
        this.region.setAttribute('aria-atomic', 'true');
        this.region.classList.add('sr-only');
        document.body.appendChild(this.region);
    }

    announce(message, priority = 'polite') {
        this.region.setAttribute('aria-live', priority);
        this.region.textContent = '';
        requestAnimationFrame(() => {
            this.region.textContent = message;
        });
    }
}

window.liveAnnouncer = new LiveAnnouncer();
```

Usage: `window.liveAnnouncer.announce('3 results found');`

## 5. CSS: Focus & Contrast Essentials

```css
/* EXT:site_package/Resources/Public/Css/accessibility.css */

/* Visible focus indicator */
:focus-visible {
    outline: 3px solid var(--focus-color, #2563eb);
    outline-offset: 2px;
}

:focus:not(:focus-visible) {
    outline: none;
}

/* Touch targets */
button, a, input, select, textarea, [role="button"] {
    min-height: 44px;
    min-width: 44px;
}

/* Ensure readable line height (WCAG 1.4.12) */
body {
    line-height: 1.6;
}

p + p {
    margin-top: 1em;
}

/* Max line length for readability */
.ce-bodytext, .frame-default .content {
    max-width: 75ch;
}

/* Scroll margin for anchored headings */
[id] {
    scroll-margin-top: 5rem;
}

/* Hover + focus parity */
a:hover, a:focus-visible,
button:hover, button:focus-visible {
    text-decoration: underline;
}
```

## 6. TYPO3-Specific Configuration

### 6.1 TCA: Require Alt Text on Images

Make the alt text field required in file metadata:

```php
<?php
// Configuration/TCA/Overrides/sys_file_metadata.php

$GLOBALS['TCA']['sys_file_metadata']['columns']['alternative']['config']['required'] = true;

// v12/v13 fallback: use eval instead
// $GLOBALS['TCA']['sys_file_metadata']['columns']['alternative']['config']['eval'] = 'required';
```

### 6.2 TCA: Header Layout Options

Provide proper heading levels and a "hidden" option for content elements:

```php
<?php
// Configuration/TCA/Overrides/tt_content.php

$GLOBALS['TCA']['tt_content']['columns']['header_layout']['config']['items'] = [
    ['label' => 'H1', 'value' => '1'],
    ['label' => 'H2', 'value' => '2'],
    ['label' => 'H3', 'value' => '3'],
    ['label' => 'H4', 'value' => '4'],
    ['label' => 'H5', 'value' => '5'],
    ['label' => 'Hidden', 'value' => '100'],
];
$GLOBALS['TCA']['tt_content']['columns']['header_layout']['config']['default'] = '2';
```

**v12 fallback:** Use numeric array keys `[0]` = label, `[1]` = value:

```php
// v12 style
$GLOBALS['TCA']['tt_content']['columns']['header_layout']['config']['items'] = [
    ['H1', '1'],
    ['H2', '2'],
    ['H3', '3'],
    ['H4', '4'],
    ['H5', '5'],
    ['Hidden', '100'],
];
```

### 6.3 Form Framework: Accessible Forms (EXT:form)

```yaml
# EXT:site_package/Configuration/Form/Overrides/AccessibleForm.yaml
TYPO3:
  CMS:
    Form:
      prototypes:
        standard:
          formElementsDefinition:
            Text:
              properties:
                fluidAdditionalAttributes:
                  autocomplete: 'on'
            Email:
              properties:
                fluidAdditionalAttributes:
                  autocomplete: 'email'
                  inputmode: 'email'
            Telephone:
              properties:
                fluidAdditionalAttributes:
                  autocomplete: 'tel'
                  inputmode: 'tel'
```

### 6.4 Content Security Policy: Allow Inline Focus Styles

If CSP is enabled, ensure focus styles via external CSS (not inline):

```php
<?php
// No inline styles needed — use the external accessibility.css
// If you must add inline styles, extend CSP via PSR-14:

declare(strict_types=1);

namespace Vendor\SitePackage\EventListener;

use TYPO3\CMS\Core\Attribute\AsEventListener;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Directive;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\Event\PolicyMutatedEvent;
use TYPO3\CMS\Core\Security\ContentSecurityPolicy\HashValue;

#[AsEventListener(identifier: 'vendor/site-package/csp-accessibility')]
final class CspAccessibilityListener
{
    public function __invoke(PolicyMutatedEvent $event): void
    {
        if ($event->getScope()->type->isFrontend()) {
            // Prefer external CSS over extending CSP for inline styles
        }
    }
}
```

## 7. Testing & Tools

### Automated Testing

| Tool | Use |
|------|-----|
| `axe-core` / `axe DevTools` | Browser extension for automated WCAG checks |
| `pa11y` | CLI accessibility testing for CI/CD |
| `Lighthouse` | Chrome DevTools audit (Accessibility score) |
| `WAVE` | Browser extension for visual feedback |

### Manual Testing Checklist

1. **Keyboard only**: Navigate entire page using Tab, Shift+Tab, Enter, Escape, Arrow keys
2. **Screen reader**: Test with VoiceOver (macOS), NVDA/JAWS (Windows)
3. **Zoom**: Verify layout at 200% and 400% zoom
4. **Color**: Use browser dev tools to simulate color blindness
5. **Reduced motion**: Enable `prefers-reduced-motion: reduce` in OS settings

### Pa11y CI Integration

```bash
# Run against local DDEV instance
npx pa11y https://mysite.ddev.site --standard WCAG2AA --reporter cli
```

```json
// .pa11yci.json
{
    "defaults": {
        "standard": "WCAG2AA",
        "timeout": 30000,
        "wait": 2000
    },
    "urls": [
        "https://mysite.ddev.site/",
        "https://mysite.ddev.site/contact",
        "https://mysite.ddev.site/news"
    ]
}
```

## 8. Accessibility Extensions

| Extension | Purpose | v12 | v13 | v14 |
|-----------|---------|-----|-----|-----|
| `typo3/cms-core` | Built-in ARIA, focus management | ✓ | ✓ | ✓ |
| `brotkrueml/schema` | Structured data (WebPage, Article) | ✓ | ✓ | ✓ |
| `wapplersystems/a11y` | Accessibility toolbar for frontend | ✓ | ✓ | — |
| `b13/container` | Accessible grid/container layouts | ✓ | ✓ | ✓ |

## 9. WCAG 2.2 Quick Reference

| Success Criterion | Level | TYPO3 Solution |
|-------------------|-------|----------------|
| 1.1.1 Non-text Content | A | `alt` attribute on `<f:image>`, TCA required field |
| 1.3.1 Info and Relationships | A | Semantic HTML in Fluid, `<fieldset>`/`<legend>` |
| 1.3.5 Identify Input Purpose | AA | `autocomplete` attributes on form fields |
| 1.4.1 Use of Color | A | Icons + text alongside color indicators |
| 1.4.3 Contrast (Minimum) | AA | CSS variables with 4.5:1 ratio |
| 1.4.4 Resize Text | AA | `rem` units, no `user-scalable=no` |
| 1.4.10 Reflow | AA | Fluid/responsive layouts |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components |
| 1.4.12 Text Spacing | AA | `line-height: 1.6`, flexible containers |
| 2.1.1 Keyboard | A | Native elements, keyboard handlers |
| 2.4.1 Bypass Blocks | A | Skip link |
| 2.4.3 Focus Order | A | Logical DOM order |
| 2.4.7 Focus Visible | AA | `:focus-visible` styles |
| 2.4.11 Focus Not Obscured | AA | `scroll-margin-top`, no sticky overlaps |
| 2.5.8 Target Size | AA | 44x44px minimum |
| 3.1.1 Language of Page | A | `<html lang>` via middleware |
| 3.1.2 Language of Parts | AA | `lang` attribute on multilingual content |
| 3.3.1 Error Identification | A | `aria-invalid`, `aria-describedby` |
| 3.3.2 Labels or Instructions | A | `<label>` on every input |
| 4.1.2 Name, Role, Value | A | ARIA attributes on custom widgets |
| 4.1.3 Status Messages | AA | `aria-live` regions |

## 10. Anti-Patterns (Flag These in Reviews)

| Anti-Pattern | Fix |
|-------------|-----|
| `<div onclick="...">` | Use `<button>` |
| `outline: none` without replacement | Use `:focus-visible` with custom outline |
| `placeholder` as sole label | Add `<label>` element |
| `tabindex > 0` | Use `tabindex="0"` or natural DOM order |
| `user-scalable=no` in viewport | Remove it |
| `font-size: 12px` (absolute) | Use `rem` units |
| Images without `alt` | Add `alt="..."` or `alt=""` for decorative |
| Color-only error indication | Add icon + text |
| `<a>` without `href` for action | Use `<button>` |
| Missing `lang` on `<html>` | Set via middleware or Fluid layout |
| Auto-playing video with sound | Add `muted` or remove `autoplay` |
| Skipped heading levels | Fix hierarchy |

## v14-Only Accessibility Changes

> The following accessibility-related changes apply **exclusively to TYPO3 v14**.

### Accessible Combobox Pattern **[v14 only]**

TYPO3 v14 introduces a new **accessible combobox pattern** (#106637) in the backend. When building custom backend UI widgets, use this pattern instead of custom autocomplete/dropdown implementations.

### Native `<dialog>` Element **[v14 only]**

Backend modals migrated from **Bootstrap Modal to native `<dialog>` element** (#107443). The native dialog provides better accessibility out of the box:
- Built-in focus trapping
- Proper `aria-modal` semantics
- `Escape` key handling
- Inert background
- No JavaScript framework dependency

Update any custom backend JavaScript that uses `Modal.show()` or `Modal.confirm()` from the Bootstrap-based API.

### Fluid 5.0 Accessibility Impact **[v14 only]**

Fluid 5.0 strict typing means ViewHelper arguments must be correctly typed. This affects accessibility-related ViewHelpers:
- `tabindex` attributes must be integers, not strings
- Boolean ARIA attributes (`aria-hidden`, `aria-expanded`) must be proper booleans

---

## Related Skills

- [web-design-guidelines](../web-design-guidelines/SKILL.md) - General web accessibility audit (non-TYPO3)
- [web-platform-design](../web-platform-design/SKILL.md) - WCAG 2.2, responsive design, forms
- [typo3-seo](../typo3-seo/SKILL.md) - SEO and structured data (overlaps with a11y for alt text, headings)
- [typo3-content-blocks](../typo3-content-blocks/SKILL.md) - Accessible Content Element templates

---

## Credits & Attribution

Accessibility patterns adapted from:
- [Vercel Web Interface Guidelines](https://github.com/vercel-labs/web-interface-guidelines) (MIT License)
- [Vercel Agent Skills: web-design-guidelines](https://github.com/vercel-labs/agent-skills) (MIT License)
- [Platform Design Skills: web-platform-design](https://github.com/ehmo/platform-design-skills) (MIT License)
- [W3C WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)

Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.
