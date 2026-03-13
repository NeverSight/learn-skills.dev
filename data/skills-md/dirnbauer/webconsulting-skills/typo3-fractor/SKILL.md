---
name: typo3-fractor
description: >-
  Automated non-PHP migrations for TYPO3 upgrades using Fractor. Handles
  FlexForms, TypoScript, Fluid, YAML, Htaccess, and composer.json changes.
  Use when working with fractor, flexform, typoscript migration, fluid migration,
  non-php upgrade, yaml migration.
compatibility: TYPO3 13.0 - 14.x
metadata:
  version: "1.1.0"
---

# TYPO3 Fractor Skill

Fractor is a generic file refactoring tool that automates non-PHP migrations for TYPO3 upgrades. It complements [Rector](https://github.com/sabbelasichon/typo3-rector) (which handles PHP) by migrating FlexForms, TypoScript, Fluid templates, YAML, Htaccess files, and composer.json.

> **TYPO3 API First:** Always use TYPO3's built-in APIs, core features, and established conventions before creating custom implementations. Always verify that the APIs and methods you use exist and are not deprecated in your target TYPO3 version (v13 or v14) by checking the official TYPO3 documentation.

> **Safety:** Never run Fractor on production. Always run on a development environment with version control. Review and test changes before releasing.

## Fractor vs Rector

| Tool | Handles | Package |
|------|---------|---------|
| **Rector** | PHP code (classes, TCA PHP, ext_localconf, etc.) | `ssch/typo3-rector` |
| **Fractor** | Non-PHP files (FlexForms, TypoScript, Fluid, YAML, Htaccess, composer.json) | `a9f/typo3-fractor` |

Use both together for complete TYPO3 upgrades. See the `typo3-extension-upgrade` skill for the full workflow.

## 1. Installation

```bash
composer require --dev a9f/typo3-fractor
# or with DDEV:
ddev composer require --dev a9f/typo3-fractor
```

> **Important:** Like Rector, Fractor loads the project autoloader and requires a PHP version
> that can parse the installed TYPO3 packages. For TYPO3 v14 targets, run Fractor with
> PHP 8.2+. Use DDEV or a container if your local PHP is older.

> **Always run Fractor, never skip it.** Non-PHP files (FlexForms, TypoScript, Fluid) contain
> version-specific patterns that are easy to miss in manual review. Fractor rules are
> maintained by the TYPO3 community and cover edge cases.

This meta-package installs all TYPO3-specific file processors:
- `a9f/fractor` (core engine)
- `a9f/fractor-xml` (FlexForm/XML processing)
- `a9f/fractor-fluid` (Fluid template processing)
- `a9f/fractor-typoscript` (TypoScript/TSconfig processing)
- `a9f/fractor-yaml` (YAML processing)
- `a9f/fractor-htaccess` (Htaccess processing)
- `a9f/fractor-composer-json` (composer.json processing)

## 2. Configuration

### Quick Start

Generate a default config:

```bash
vendor/bin/typo3-fractor-init
```

### Manual Configuration

Create `fractor.php` in your project root:

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/packages/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_13,
    ]);
```

### Configuration for v14

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/Configuration/',
        __DIR__ . '/Resources/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

### Skip Rules or Files

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;
use a9f\Typo3Fractor\TYPO3v12\FlexForm\MigrateRequiredFlagFlexFormFractor;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withSkip([
        MigrateRequiredFlagFlexFormFractor::class,
        __DIR__ . '/packages/legacy_ext/',
        __DIR__ . '/packages/my_ext/Resources/Private/Templates/Old.html' => [
            \a9f\Typo3Fractor\TYPO3v14\Fluid\ChangeLogoutHandlingInFeLoginFractor::class,
        ],
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_14,
    ]);
```

### Apply Single Rules

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\TYPO3v12\FlexForm\MigrateItemsIndexedKeysToAssociativeFractor;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withRules([
        MigrateItemsIndexedKeysToAssociativeFractor::class,
    ]);
```

## 3. Running Fractor

### Dry Run (Preview)

```bash
vendor/bin/fractor process --dry-run
```

### Apply Changes

```bash
vendor/bin/fractor process
```

### Run Single Rule from Set

```bash
vendor/bin/fractor process --only="a9f\Typo3Fractor\TYPO3v14\TypoScript\RemoveExternalOptionFromTypoScriptFractor"
```

### With DDEV

```bash
ddev exec vendor/bin/fractor process --dry-run
ddev exec vendor/bin/fractor process
```

## 4. Available Set Lists

### Level Sets (Cumulative)

Apply all rules up to a target version:

| Set List | Includes |
|----------|----------|
| `Typo3LevelSetList::UP_TO_TYPO3_10` | v7 + v8 + v10 |
| `Typo3LevelSetList::UP_TO_TYPO3_11` | ... + v11 |
| `Typo3LevelSetList::UP_TO_TYPO3_12` | ... + v12 |
| `Typo3LevelSetList::UP_TO_TYPO3_13` | ... + v13 |
| `Typo3LevelSetList::UP_TO_TYPO3_14` | ... + v14 |

### Version-Specific Sets

Apply rules for a single version only:

| Set List | Description |
|----------|-------------|
| `Typo3SetList::TYPO3_12` | v12 rules only |
| `Typo3SetList::TYPO3_13` | v13 rules only |
| `Typo3SetList::TYPO3_14` | v14 rules only |

## 5. Rules by File Type and Version

### FlexForm Rules (v12)

| Rule | Migration |
|------|-----------|
| `MigrateEmailFlagToEmailTypeFlexFormFractor` | `eval=email` → `type=email` |
| `MigrateEvalIntAndDouble2ToTypeNumberFlexFormFractor` | `eval=int/double2` → `type=number` |
| `MigrateInternalTypeFolderToTypeFolderFlexFormFractor` | `internalType=folder` → `type=folder` |
| `MigrateItemsIndexedKeysToAssociativeFractor` | Indexed items → `label`/`value` keys |
| `MigrateNullFlagFlexFormFractor` | `eval=null` → `nullable=true` |
| `MigratePasswordAndSaltedPasswordToPasswordTypeFlexFormFractor` | Password eval → `type=password` |
| `MigrateRenderTypeColorpickerToTypeColorFlexFormFractor` | `renderType=colorPicker` → `type=color` |
| `MigrateRequiredFlagFlexFormFractor` | `eval=required` → `required=1` |
| `MigrateTypeNoneColsToSizeFlexFormFractor` | `cols` → `size` for type=none |
| `RemoveTceFormsDomElementFlexFormFractor` | Remove `<TCEforms>` wrapper |

### TypoScript Rules (v12)

| Rule | Migration |
|------|-----------|
| `MigrateTypoScriptLoginUserAndUsergroupConditionsFractor` | Legacy conditions → Symfony expressions |
| `RemoveConfigDisablePageExternalUrlFractor` | Remove `config.disablePageExternalUrl` |
| `RemoveConfigDoctypeSwitchFractor` | Remove `config.doctypeSwitch` |
| `RemoveConfigMetaCharsetFractor` | Remove `config.metaCharset` |
| `RemoveConfigSendCacheHeadersOnlyWhenLoginDeniedInBranchFractor` | Remove deprecated cache header config |
| `RemoveConfigSpamProtectEmailAddressesAsciiOptionFractor` | Remove `ascii` option |
| `RemoveNewContentElementWizardOptionsFractor` | Remove legacy CE wizard TSconfig |
| `RemoveWorkspaceModeOptionsFractor` | Remove workspace mode options |
| `RenameConfigXhtmlDoctypeToDoctypeFractor` | `xhtmlDoctype` → `doctype` |
| `RenameTcemainLinkHandlerMailKeyFractor` | Rename mail link handler key |
| `UseConfigArrayForTSFEPropertiesFractor` | TSFE properties → config array |

### Fluid Rules (v12)

| Rule | Migration |
|------|-----------|
| `AbstractMessageGetSeverityFluidFractor` | Migrate severity constants in Fluid |

### TypoScript Rules (v13)

| Rule | Migration |
|------|-----------|
| `MigrateIncludeTypoScriptSyntaxFractor` | `<INCLUDE_TYPOSCRIPT:` → `@import` |
| `RemovePageDoktypeRecyclerFromUserTsConfigFractor` | Remove recycler doktype from TSconfig |

### TypoScript Rules (v14)

| Rule | Migration |
|------|-----------|
| `MigrateTypoScriptConditionGetTSFEFractor` | `getTSFE()` conditions → new API |
| `MigrateTypoScriptGetDataPathFractor` | getData path changes |
| `RemoveDuplicateDoktypeRestrictionConfigurationFractor` | Remove duplicate doktype restrictions |
| `RemoveExposeNonexistentUserInForgotPasswordDialogSettingInFeLoginFractor` | Remove deprecated fe_login setting |
| `RemoveExternalOptionFromTypoScriptFractor` | Remove `external` option |
| `RemoveFrontendAssetConcatenationAndCompressionFractor` | Remove asset concatenation/compression settings |
| `RemoveModWebLayoutDefLangBindingFractor` | Remove `mod.web_layout.defLangBinding` |
| `RemoveUserTSConfigAuthBeRedirectToURLFractor` | Remove `auth.BE.redirectToURL` |

### Fluid Rules (v14)

| Rule | Migration |
|------|-----------|
| `ChangeLogoutHandlingInFeLoginFractor` | Migrate fe_login logout handling |

### YAML Rules (v14)

| Rule | Migration |
|------|-----------|
| `MigrateLegacyFormTemplatesFractor` | Migrate legacy EXT:form templates |

### Htaccess Rules (v14)

| Rule | Migration |
|------|-----------|
| `RemoveUploadsFromDefaultHtaccessFractor` | Remove `/uploads/` from .htaccess |

## 6. Code Style Configuration

### TypoScript Formatting

```php
<?php
use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\FractorTypoScript\Configuration\TypoScriptProcessorOption;
use Helmich\TypoScriptParser\Printer\PrettyPrinterConfiguration;
use a9f\FractorTypoScript\Configuration\PrettyPrinterConditionTermination;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/Configuration/'])
    ->withOptions([
        TypoScriptProcessorOption::INDENT_SIZE => 2,
        TypoScriptProcessorOption::INDENT_CHARACTER => PrettyPrinterConfiguration::INDENTATION_STYLE_SPACES,
        TypoScriptProcessorOption::ADD_CLOSING_GLOBAL => false,
        TypoScriptProcessorOption::INCLUDE_EMPTY_LINE_BREAKS => true,
        TypoScriptProcessorOption::INDENT_CONDITIONS => true,
        TypoScriptProcessorOption::CONDITION_TERMINATION => PrettyPrinterConditionTermination::Keep,
    ]);
```

**Indent character options:**
- `PrettyPrinterConfiguration::INDENTATION_STYLE_SPACES` -- use spaces
- `PrettyPrinterConfiguration::INDENTATION_STYLE_TABS` -- use tabs
- `'auto'` -- detect from file and keep existing

**Condition termination options:**
- `PrettyPrinterConditionTermination::Keep` -- keep existing
- `PrettyPrinterConditionTermination::EnforceGlobal` -- always `[global]`
- `PrettyPrinterConditionTermination::EnforceEnd` -- always `[end]`

### XML/FlexForm Formatting

```php
<?php
use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\FractorXml\Configuration\XmlProcessorOption;
use a9f\FractorXml\Configuration\Indent;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/Configuration/'])
    ->withOptions([
        XmlProcessorOption::INDENT_CHARACTER => Indent::STYLE_TAB,
        XmlProcessorOption::INDENT_SIZE => 1,
    ]);
```

### File Extension Filtering

Control which file extensions each processor handles:

```php
<?php
use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\FractorFluid\Configuration\FluidProcessorOption;
use a9f\FractorTypoScript\Configuration\TypoScriptProcessorOption;
use a9f\FractorXml\Configuration\XmlProcessorOption;
use a9f\FractorYaml\Configuration\YamlProcessorOption;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withOptions([
        FluidProcessorOption::ALLOWED_FILE_EXTENSIONS => ['html'],
        TypoScriptProcessorOption::ALLOWED_FILE_EXTENSIONS => ['typoscript', 'tsconfig'],
        XmlProcessorOption::ALLOWED_FILE_EXTENSIONS => ['xml', 'xlf'],
        YamlProcessorOption::ALLOWED_FILE_EXTENSIONS => ['yaml', 'yml'],
    ]);
```

**Default extensions:**
- Fluid: `html`, `xml`, `txt`
- TypoScript: `typoscript`, `tsconfig`, `ts`
- XML: `xml`
- YAML: `yaml`, `yml`

## 7. Writing Custom Rules

### Custom XML/FlexForm Rule

Subclass `\a9f\FractorXml\XmlFractor` for XML-based rules:

```php
<?php
declare(strict_types=1);

namespace Vendor\MyExtension\Fractor;

use a9f\FractorXml\XmlFractor;
use DOMDocument;
use DOMNode;

final class MyCustomFlexFormFractor extends XmlFractor
{
    public function canHandle(\DOMNode $node): bool
    {
        return $node->nodeName === 'config'
            && $node->parentNode?->nodeName === 'TCEforms';
    }

    public function refactor(DOMNode $node): DOMNode|int|null
    {
        // Modify the DOM node
        return $node;
    }

    public function getDescription(): string
    {
        return 'Migrate custom FlexForm configuration';
    }
}
```

### Register Custom Rule

```php
<?php
// fractor.php
use a9f\Fractor\Configuration\FractorConfiguration;
use Vendor\MyExtension\Fractor\MyCustomFlexFormFractor;

return FractorConfiguration::configure()
    ->withPaths([__DIR__ . '/packages/'])
    ->withRules([
        MyCustomFlexFormFractor::class,
    ]);
```

## 8. Upgrade Workflow Integration

### Recommended Order

```
1. git checkout -b feature/typo3-upgrade
2. Run Rector (PHP migrations)        → vendor/bin/rector process
3. Run Fractor (non-PHP migrations)   → vendor/bin/fractor process
4. Run PHP-CS-Fixer (code style)      → vendor/bin/php-cs-fixer fix
5. Run PHPStan (static analysis)      → vendor/bin/phpstan analyse
6. Run Tests                          → vendor/bin/phpunit
7. Manual testing in target version
```

### Combined fractor.php for Extension Development

```php
<?php
declare(strict_types=1);

use a9f\Fractor\Configuration\FractorConfiguration;
use a9f\Typo3Fractor\Set\Typo3LevelSetList;
use a9f\FractorTypoScript\Configuration\TypoScriptProcessorOption;
use Helmich\TypoScriptParser\Printer\PrettyPrinterConfiguration;

return FractorConfiguration::configure()
    ->withPaths([
        __DIR__ . '/Configuration/',
        __DIR__ . '/Resources/',
    ])
    ->withSkip([
        __DIR__ . '/Resources/Public/',
    ])
    ->withSets([
        Typo3LevelSetList::UP_TO_TYPO3_13,
    ])
    ->withOptions([
        TypoScriptProcessorOption::INDENT_SIZE => 4,
        TypoScriptProcessorOption::INDENT_CHARACTER => PrettyPrinterConfiguration::INDENTATION_STYLE_SPACES,
    ]);
```

## 9. Troubleshooting

### Fractor Fails to Parse TypoScript

```bash
# Check for syntax errors in TypoScript first
# Fractor uses helmich/typo3-typoscript-parser which requires valid TypoScript

# Skip problematic files
vendor/bin/fractor process --dry-run
# Then add them to withSkip() in fractor.php
```

### FlexForm Changes Not Applied

```bash
# Ensure XML files are in the configured paths
# Check ALLOWED_FILE_EXTENSIONS includes 'xml'
# Verify the FlexForm has the expected structure (<T3DataStructure>)
```

### Formatting Changes Unexpected

```bash
# Configure code style explicitly in fractor.php
# Use 'auto' indent detection to preserve existing formatting
# Review withOptions() settings
```

### Running Fractor in CI

```yaml
# .github/workflows/fractor.yml
- name: Check Fractor
  run: vendor/bin/fractor process --dry-run
  # Fails if any rules would apply = outdated code
```

## 10. Resources

- **Fractor Repository**: https://github.com/andreaswolf/fractor
- **TYPO3 Fractor Package**: https://github.com/andreaswolf/fractor-typo3-fractor
- **Packagist**: https://packagist.org/packages/a9f/typo3-fractor
- **TYPO3 Rector** (PHP companion): https://github.com/sabbelasichon/typo3-rector
- **Related Skills**: `typo3-extension-upgrade` (full upgrade workflow), `typo3-rector` (PHP migrations)

## v14-Only Fractor Targets

> The following non-PHP migration targets are **v14-specific** and handled by Fractor `Typo3SetList::TYPO3_14` rules.

### TCA Migrations **[v14 only]**

- **`ctrl.searchFields` removed** — migrate to per-column `'searchable' => true` configuration.
- **`ctrl.is_static` removed** — remove from TCA ctrl arrays.
- **TCA `interface` settings removed** (#106412) — remove `interface` key from TCA.
- **TCA tab labels consolidated** (#107789) — use `core.form.tabs` short-form references.
- **FlexForm pointer fields removed** (#107047) — use direct TCA column references.

### TypoScript Migrations **[v14 only]**

- **`config.concatenateCss` / `config.concatenateJs` removed** — remove these settings; delegate to web server or build tools.
- **`config.compressCss` / `config.compressJs` removed** — same as above.
- **`external` property removed** for asset inclusion — remove `external = 1` from TypoScript.
- **TypoScript condition `getTSFE()` removed** — use request-based conditions.

### Htaccess Migrations **[v14 only]**

- **Updated default `.htaccess` template** (#105244) — Fractor can apply the updated template.

### FlexForm Migrations **[v14 only]**

- **FlexForm `pointer` field functionality removed** (#107047) — migrate to direct TCA references.
- **`FlexFormService` merged into `FlexFormTools`** (#107945) — update PHP references.

---

## Credits & Attribution

Thanks to [Andreas Wolf](https://github.com/andreaswolf) for creating and maintaining Fractor.
Thanks to Netresearch DTT GmbH for their contributions to the TYPO3 community.
