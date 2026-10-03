---
name: typed-structures
description: >-
  编写、迁移或审阅 Spore Notation / typed-structures 的宇宙、范畴、ADT、定律、方法、
  Self、精化、值索引与子类型示例；用 Ohm 识别设计稿的句法。
  适用于 Category、Functor/Applicative/Selective/Monad、Option 与 Sequence 的记法设计。
  不用于现有 Spore 编译器的工程实现；识别器不能核验类型、证明或结构归属。
---

# Typed structures

维护 Spore Notation 语言设计稿。理论结构与实际数据结构一起引入，并提供对应的操作和 law 证据；没有与本稿对应的类型检查器或证明内核。

## 工作方式

- 从 [examples.md](examples.md) 选择相关章节：01 定义与宇宙，02 子类型，03 精化，04 范畴与元组，05 计算结构与 Option，06 序列，07 映射，08 索引类型。它们按依赖顺序共享背景，不为小改动加载全部证明。
- 写程序时以以下规则为准，对照 [grammar.ohm](grammar.ohm) 检查表面形式。用户提出新设计时区分既有规则与提案，不为兼容旧例子恢复废弃语法。
- 新写或改写的程序先写入文件并做句法检查；另行审阅宇宙、态射起终点、泛型作用域、Self、继承字段与 law。文法不决定这些语义。
- 报告实际完成的检查。用户明确要求其他语言实现时遵从目标；该实现的运行结果不构成本稿的机器证明。

## 宇宙与参数

- 采用非累积宇宙与宇宙多态：`Universe<u>: Universe<next(u)>;`、`Prop = Universe<0>;`、`Type = Universe<1>;`。首行是背景规则模式，不是 Universe 属于自身的定义。
- 层级支持 `next/max`，数字是 next 迭代的简写；层级不是运行时 Nat。省略层级或写 `_` 产生待推断变量；声明中独立且未固定的层级可以推广，调用时实例化。不能把一次推断当成任意层级通用，不自动提升或降低宇宙。
- 依赖函数的数据层级按输入与结果的 max 计算；结果是命题时，对任意宇宙量化仍属于 Prop。区分 `A -> P` 与返回命题类型的 `A -> Prop`。不据此引入证明无关、擦除或任意从 Prop 向数据消去。
- `<u>` 用于层级，`[A: Type, n: Nat]` 用于泛型或索引，`(x, y)` 用于普通实参。`[A]` 默认绑定 `A: Type`；结构值参数也放在 `[]`，例如 `F: Functor[C,D]`。
- 普通多参数函数不自动柯里化。`(A, B) -> C` 与 `A -> B -> C` 用显式 curry / uncurry 对应。`(pair: (A,B)) -> C` 接收一个元组；调用写 `f((a,b))`，不自动拆包或引入 `<a,b>` 调用形式。

## 声明与补全

| 类型体中的形式 | 含义 |
| --- | --- |
| `field: T;` | 实例字段要求 |
| `fn f(x: A) -> B;` | 函数字段要求，核心为 `f: A -> B;` |
| `law p(x: A) -> (P);` | 证据函数要求，核心为 `p: A -> P;` |
| `law p[X] -> (P);` | 证据值族，通过 `p[X]` 取得；有 `()` 才是零参数函数 |
| `name[: T] = expression;` | 固定的类型预定义 |
| `def fn f(x: A) -> B { body }` | 固定的普通函数定义 |
| `def law p(x: A) -> (P) { evidence }` | 固定的证明定义 |
| `method m(x: A) -> B { body }` | 实例侧绑定方法，必须有 body |

- 字段、函数、证据都以 `:` 声明、`=` 定义；fn/law 是语法糖。def 只用于带大括号的 def fn / def law，不写裸 def、def method 或 `def law ... = ...`。普通函数和方法可以推断返回类型，law 明确写出目标。
- 不使用 static、独立 proof 声明、`:=` 或 `#` 方法调用。没有实例字段默认值：`step: Int = 1;` 是类型预定义，构造时不能覆盖。`=` 不引入可变赋值。
- 记录构造 `T { field = expression, ... }` 与关系补全只填写实例要求。函数和证据用值提供，不在构造块里写 def fn / def law；固定预定义和方法不参与构造补全。
- 没有 case 的数据类型是记录，有 case 时选择一个分支并提供公共字段及分支字段；分支专有字段只在匹配后使用。不能把这种数据构造规则误用于类型侧结构归属。

## 成员与 Self

- `T.name` 查找普通类型成员，`value.name` 查找实例字段或绑定方法；两域不回退。允许 T.map 与 value.map 同名，同一实例域的字段与方法不能同名，类型域没有一般重载集合。
- `.` 先选成员，`()` 再应用函数。方法取值时保存一次求值后的接收者，调用时执行 body；method 不自动产生 T.m 普通函数入口。函数字段不额外绑定接收者。
- method 省略 `self: Self`，字段显式写 self.field；裸名字查参数、局部绑定和外层词法定义。普通函数没有隐式 self，lambda 可捕获已有 self。law 可依赖此前字段，证据按最终字段实例化，不额外绑定接收者。
- Self 是当前实例化的完整类型，所在宇宙由该类型确定，不固定写成 Self: Type。在 Option[A] 的数据视图中是完整的 Option[A]，不能写 Self[B]；在 Functor[C,D] 中是完整的结构值类型，不是 obj(A)。Types 这类纯结构值不额外产生一个 Self 数据载体。
- 对抽象 Self 成立的定义与证明可在子类型下实例化。不能先将 Self 等同于父类型检查，再替换为任意子类型。仅凭父字段不能构造完整 Self：Counter.make 返回 Counter，keep 原样返回输入 Self；next 即使是 method，也不能自动承诺保持子类型的新增字段或约束。
- Self.member 可以选择继承的普通操作，但不会改变固定返回类型；Self.make 不会把 Counter 提升为 Self。向上取得 T 视图后，Self 按 T 实例化，不恢复隐藏源类型。需操作父表示时先用 `value: T = self;` 取得视图，不假定调用位置自动转换。
- 内层类型建立自己的 Self；类型体外的关系补全和 when 不因出现 self 就建立 Self。关系块的 self 是源值，when 的 self 是基础值。

## 范畴、结构归属与类型族

- `:` 表示归属，`<:` 表示两个类型之间的细化关系，`=` 表示定义。`type Types: LargeCategory<1> { ... }` 补全结构值；`LargeCategory<v> = Category<next(v),v>` 是透明别名，不登记转换。
- Category<u,v> 要求 Obj: Universe<u>、Hom[X,Y]: Universe<v>，结构自身在 Universe<max(next(u),next(v))>。Types.Obj = Type，Types.Hom[X,Y] = X -> Y；因此 Types 的对象层级是 2、态射层级是 1，Functor[Types,Types] 在 Universe<2>。
- 使用实际的 `Functor[C,D]` 契约及其 obj/map，检查恒等和复合律。ProductCategory 的态射按分量组合；自然变换保留 app[X] 命名。核对每个同构的正逆方向、自然性方块、幺半结构的五边形和三角形起终点。
- `type Option[A: Type]: Monad { ... }` 同时提供结构 Option 和数据类型族 Option[A]，Option.obj(A) 定义等于 Option[A]。结构补全覆盖整个类型族，不捕获某个固定 A 或实例 self；不能把 Option.Some(1) 当作函子结构。
- 四层实际声明为 `Applicative <: Functor[Types,Types]`、`Selective <: Applicative`、`Monad <: Selective`。继承同一 obj/map；pure、ap、select、bind 都通过同一个 obj 表述，具体补全统一展开为 Option。不要恢复 `Option <: Functor`、Functor[Option]、`for F`、Family 或 Self[B]。
- 检查继承的全部证据：Functor 恒等/复合；Applicative 恒等/同态/交换/复合及 map_from_ap；Selective 恒等/分配/结合；Monad 左右单位元/结合及 ap_from_bind、select_from_bind。派生配对操作也需自然性、单位和结合证据，不能写“laws 显然成立”。
- Option 的方法 map 接收 A -> B，返回 Option[B]；Self.map 选择全族操作，不把 Self 变成构造器。泛型辅助函数显式接收结构或操作，不引入隐式实例查找。函数的参数逆变、结果协变，不能用结果协变补救不匹配的输入或凭 map 推导容器子类型。

## 证明与值类型关系

- 背景采用不可变值、纯全函数、数学 Int/Nat、元组及结构递减递归。Nat 按 Zero / Succ 归纳，基本运算按构造器归约；`==` 返回 Bool，`~=` 构造命题。
- 证明使用定义归约 refl、symm、trans、congr_arg、本稿采用的 funext、match 与结构归纳；pair_congr 在 01 中定义，空 match 消去无构造器类型。仅写命题或跑有限输入不是证明。
- `S <: T` 在命题位置表达关系；关系声明用块补全目标字段与 law，证据充分时可省略块。泛型关系用 `forall[...] { ... }`，`type S <: T { ... }` 继承要求与固定成员。
- 值类型关系须给出保持源观察的规范视图。目标 law 与源观察保持是不同义务，普通转换函数不足以建立关系。带目标类型的绑定插入视图；多路径需有一致的计算解释，不按名字或导入顺序选实现，固定成员不能覆盖。
- `type Positive = Int when self > 0;` 表示基础值与条件证据，布尔条件 b 展开为 b ~= true；精化弱化须保持基础值。

## 句法验证与边界

使用可用的 `@ohm-js/cli`，从当前 `ohm --help` / `ohm match --help` 取得参数，对照本目录 grammar.ohm。缺失时优先用 pnpm 全局安装 CLI 及其 ohm-js 依赖，不向目标项目加依赖；用户指定临时运行或不安装时遵从。原样引用已有片段或只解释短名字，无需创建验证程序或安装工具。

识别单位是 Module，单独表达式需包进定义。修改文法或示例后运行 [scripts/check-syntax.mjs](scripts/check-syntax.mjs)，检查各节、顺序拼接及正反语法用例；OHM_BIN 可指定 CLI 路径。错误保留 Line / Expected 诊断。

退出码 0 只表示句法符合文法。脚本另列会被识别但必须语义拒绝的案例，包括自动升层、Self[B]、不完整的 Self 构造、错误结构归属、实参数量不匹配和错误 refl；识别它们不是成功验证其语义。不要声称旧 Ohm 文法、有限样例或行为评测 schema 检查验证了类型或 law。

`:>`、一般重载、类型推断与依赖转换算法、递归接受条件、视图核心展开与跨模块一致性、效果及存储模型仍待确定或实现。宇宙记法、四层契约和全族补全已在例子中给出，不再列为缺失的接口设计。
