---
name: rector-developer
description: Build Rector PHP rules that transform PHP code via AST. Use when asked to create, modify, or explain Rector rules for PHP code transformations. Rector rules use the PHP-Parser AST and PHPStan type analysis. Triggers on requests like "write a Rector rule to...", "create a Rector rule that...", "add a Rector rule for...", or when working in a rector-src or rector-based project and asked to implement code transformation logic.
---

# Rector PHP Rule Builder

Rector transforms PHP code by traversing the PHP-Parser AST, matching node types, and returning modified nodes from `refactor()`.

## Workflow

1. **Check for an existing configurable rule first** — see references/configurable-rules.md. Renaming functions/methods/classes, converting call types, and removing arguments are all covered. Prefer `->withConfiguredRule()` over writing a custom rule for these cases.
2. Identify the PHP-Parser node type(s) to target (see references/node-types.md)
3. Write the rule class extending `AbstractRector`
4. If PHP version gated, implement `MinPhpVersionInterface`
5. If configurable, implement `ConfigurableRectorInterface`
6. Register the rule in rector.php config

## Rule Skeleton

```php
<?php

declare(strict_types=1);

namespace Rector\[Category]\Rector\[NodeType];

use PhpParser\Node;
use PhpParser\Node\Expr\FuncCall; // target node type
use Rector\Rector\AbstractRector;
use Symplify\RuleDocGenerator\ValueObject\CodeSample\CodeSample;
use Symplify\RuleDocGenerator\ValueObject\RuleDefinition;

/**
 * @see \Rector\Tests\[Category]\Rector\[NodeType]\[RuleName]\[RuleName]Test
 */
final class [RuleName]Rector extends AbstractRector
{
    public function getRuleDefinition(): RuleDefinition
    {
        return new RuleDefinition('[Description]', [
            new CodeSample(
                <<<'CODE_SAMPLE'
// before
CODE_SAMPLE
                ,
                <<<'CODE_SAMPLE'
// after
CODE_SAMPLE
            ),
        ]);
    }

    /** @return array<class-string<Node>> */
    public function getNodeTypes(): array
    {
        return [FuncCall::class];
    }

    /** @param FuncCall $node */
    public function refactor(Node $node): ?Node
    {
        if (! $this->isName($node, 'target_function')) {
            return null;
        }

        // transform and return modified $node, or return null for no change
        return $node;
    }
}
```

## `refactor()` Return Values

| Return | Effect |
|--------|--------|
| `null` | No change, continue traversal |
| `$node` (modified) | Replace with modified node |
| `Node[]` (non-empty) | Replace with multiple nodes |
| `NodeVisitor::REMOVE_NODE` | Delete the node |

**Never return an empty array** — throws `ShouldNotHappenException`.

## Protected Methods on AbstractRector

```php
// Name checking
$this->isName($node, 'functionName')         // exact name match
$this->isNames($node, ['name1', 'name2'])    // match any
$this->getName($node)                         // get name string or null

// Type checking (PHPStan-powered)
$this->getType($node)                         // returns PHPStan Type
$this->isObjectType($node, new ObjectType('ClassName'))

// Traversal
$this->traverseNodesWithCallable($nodes, function (Node $node): int|Node|null {
    return null; // continue
    // or return NodeVisitor::STOP_TRAVERSAL;
    // or return NodeVisitor::DONT_TRAVERSE_CURRENT_AND_CHILDREN;
});

// Misc
$this->mirrorComments($newNode, $oldNode);    // copy comments
```

## Injected Services

Inject via constructor (autowired by DI container):

```php
public function __construct(
    private readonly BetterNodeFinder $betterNodeFinder,
    // ... other services
) {}
```

- **`$this->nodeFactory`** — create nodes (see references/helpers.md)
- **`$this->nodeComparator`** — compare nodes structurally
- **`$this->betterNodeFinder`** — search within nodes (inject via constructor)
- PHPDoc manipulation: inject `PhpDocInfoFactory` + `DocBlockUpdater`

## Configurable Rules

```php
use Rector\Contract\Rector\ConfigurableRectorInterface;
use Symplify\RuleDocGenerator\ValueObject\CodeSample\ConfiguredCodeSample;

final class MyRector extends AbstractRector implements ConfigurableRectorInterface
{
    private string $targetClass = 'OldClass';

    public function configure(array $configuration): void
    {
        $this->targetClass = $configuration['target_class'] ?? $this->targetClass;
    }

    public function getRuleDefinition(): RuleDefinition
    {
        return new RuleDefinition('...', [
            new ConfiguredCodeSample('before', 'after', ['target_class' => 'OldClass']),
        ]);
    }
}
```

## PHP Version Gating

```php
use Rector\VersionBonding\Contract\MinPhpVersionInterface;
use Rector\ValueObject\PhpVersionFeature;

final class MyRector extends AbstractRector implements MinPhpVersionInterface
{
    public function provideMinPhpVersion(): int
    {
        return PhpVersionFeature::ENUM; // PHP 8.1+
    }
}
```

See references/php-versions.md for all `PhpVersionFeature` constants.

## rector.php Registration

```php
use Rector\Config\RectorConfig;

return RectorConfig::configure()
    ->withRules([MyRector::class])
    // configurable rule:
    ->withConfiguredRule(MyConfigurableRector::class, ['key' => 'value']);
```

## Namespace Convention

Rules live at: `rules/[Category]/Rector/[NodeType]/[RuleName]Rector.php`
Tests live at: `rules-tests/[Category]/Rector/[NodeType]/[RuleName]Rector/`

Categories: `CodeQuality`, `CodingStyle`, `DeadCode`, `EarlyReturn`, `Naming`, `Php52`–`Php85`, `Privatization`, `Removing`, `Renaming`, `Strict`, `Transform`, `TypeDeclaration`

## Writing Tests

Every rule needs a test class extending `AbstractRectorTestCase` and at least one fixture file.

**Minimal test class** (`rules-tests/[Category]/Rector/[NodeType]/[RuleName]/[RuleName]RectorTest.php`):

```php
<?php

declare(strict_types=1);

namespace Rector\Tests\[Category]\Rector\[NodeType]\[RuleName];

use Iterator;
use PHPUnit\Framework\Attributes\DataProvider;
use Rector\Testing\PHPUnit\AbstractRectorTestCase;

final class [RuleName]RectorTest extends AbstractRectorTestCase
{
    #[DataProvider('provideData')]
    public function test(string $filePath): void
    {
        $this->doTestFile($filePath);
    }

    public static function provideData(): Iterator
    {
        return self::yieldFilesFromDirectory(__DIR__ . '/Fixture');
    }

    public function provideConfigFilePath(): string
    {
        return __DIR__ . '/config/configured_rule.php';
    }
}
```

**Fixture file** (`Fixture/fixture.php.inc`):

```php
<?php

namespace Rector\Tests\[Category]\Rector\[NodeType]\[RuleName]\Fixture;

// INPUT code before rule runs

?>
-----
<?php

namespace Rector\Tests\[Category]\Rector\[NodeType]\[RuleName]\Fixture;

// EXPECTED code after rule runs

?>
```

**Tip:** Write only the input section, run the test, and `FixtureFileUpdater` auto-fills the expected output.

**Skip fixtures (rule should not apply):** Create a separate file per skip scenario, named with a `skip_` prefix. Each file contains a single section only — no `-----` separator. Never put multiple skip scenarios in one file.

```php
<?php

namespace Rector\Tests\[Category]\Rector\[NodeType]\[RuleName]\Fixture;

// Code that should NOT be changed — one scenario per file

?>
```

Examples: `skip_already_correct.php.inc`, `skip_static_call.php.inc`, `skip_inside_interface.php.inc`

See **references/testing.md** for: config file formats, configurable rule variants, multi-config test classes, fixture naming, Source/ support classes, and fixture auto-update behaviour.

## Reference Files

- **references/configurable-rules.md** — All built-in configurable rules with config examples (check this before writing a custom rule)
- **references/node-types.md** — PhpParser node type quick reference (FuncCall, MethodCall, Class_, etc.)
- **references/helpers.md** — NodeFactory methods, BetterNodeFinder, NodeComparator, PhpDocInfo
- **references/php-versions.md** — PhpVersionFeature constants by PHP version
- **references/testing.md** — Full test structure, fixture format, configurable rule testing, special cases
