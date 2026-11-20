---
name: ramda
description: >
  Ramda is a practical functional programming library for JavaScript with 272 auto-curried,
  data-last functions. Use this skill whenever the user mentions Ramda, asks about Ramda
  functions (R.map, R.filter, R.pipe, R.compose, R.lens, R.mergeDeepRight, etc.), wants to
  write point-free/functional JavaScript, needs help picking the right Ramda function for a
  task, or is migrating imperative code to Ramda-style functional code. Also trigger when the
  user asks about functional concepts like currying, composition, lenses, transducers in the
  context of JavaScript/TypeScript, or when they mention common Ramda patterns like
  data-last parameter order.
---

# Ramda Skill

Version note: examples and function names in this skill target Ramda `0.31.3`.

## Design philosophy

Ramda is built around a few core ideas. Understanding these is more important than memorizing functions.

**Data-last**: The data to operate on always comes last. This enables partial application — you supply the "how" first, the "what" later. `R.map(fn)` returns a function waiting for data; `R.map(fn, data)` executes immediately.

**Auto-currying**: Every function is curried. If you call a 2-argument function with 1 argument, you get back a function expecting the remaining argument. This is what makes point-free composition work without glue code.

**Pure**: No mutations. Every function that "changes" data returns a new copy. Ramda never modifies its inputs.

**Dispatch**: Many functions check if the data argument has a method with the same name (e.g., `arr.map(f)`) and delegate to it. This means Ramda functions work with arrays, objects, and any custom type that implements the relevant method — including Fantasy-Land compatible types like Maybe, Either, or Task.

## Function selection by task

When a user describes what they want to do, use this reference to find the right function.

### Transforming data

| Task | Function | Example |
|---|---|---|
| Transform every element | `map(fn, list)` | `R.map(R.inc, [1,2,3])` → `[2,3,4]` |
| Keep matching elements | `filter(pred, list)` | `R.filter(R.lt(2), [1,2,3])` → `[3]` |
| Remove matching elements | `reject(pred, list)` | `R.reject(R.lt(2), [1,2,3])` → `[1,2]` |
| Transform and flatten | `chain(fn, list)` | `R.chain(x => [x, x*2], [1,2])` → `[1,2,2,4]` |
| Reduce to a value | `reduce(fn, init, list)` | `R.reduce(R.add, 0, [1,2,3])` → `6` |
| Reduce while condition holds | `reduceWhile(pred, fn, init, list)` | stops early when pred fails |
| Transform object values | `map(fn, obj)` | `R.map(R.inc, {a:1, b:2})` → `{a:2, b:3}` |
| Map over object keys+values | `mapObjIndexed(fn, obj)` | fn receives `(val, key, obj)` |
| Apply functions to elements at indices | `adjust(fn, idx, list)` | `R.adjust(R.inc, 1, [1,2,3])` → `[1,3,3]` |
| Replace element at index | `update(idx, val, list)` | `R.update(1, 99, [1,2,3])` → `[1,99,3]` |

### Composing functions

| Task | Function | Notes |
|---|---|---|
| Right-to-left composition | `compose(f, g, h)` | `compose(f,g,h)(x)` = `f(g(h(x)))` |
| Left-to-right pipeline | `pipe(f, g, h)` | `pipe(f,g,h)(x)` = `h(g(f(x)))` — often more readable |
| Two-function compose | `o(f, g)` | `o(f,g)` = `compose(f,g)` — shorter for simple cases |
| Compose with transformer chaining | `composeWith(chainFn, fns)` | Custom chain between composed functions |
| Pipe with transformer chaining | `pipeWith(chainFn, fns)` | Custom chain between piped functions |
| Apply multiple fns to same args | `juxt([f, g, h])` | `juxt([R.inc, R.dec])(3)` → `[4, 2]` |
| Apply spec object to input | `applySpec({a: f, b: g})` | Returns `{a: f(input), b: g(input)}` |
| Pass value to fn, return value | `tap(fn, val)` | Side-effect in a pipeline without breaking flow |
| Converge: apply fns, then combine | `converge(combine, [f, g])` | `converge(R.add, [R.inc, R.dec])(5)` → `6+4=10` |
| Apply fn to nth argument | `nthArg(n)` | `nthArg(0)` returns a fn that returns its 1st arg |
| Call a function | `call(fn, x)` | `call(fn, 5)` = `fn(5)` |
| Apply fn to a value | `apply(fn, [a, b])` | `apply(R.add, [1,2])` → `3` |
| Apply fn to a single value | `applyTo(val, fn)` | `applyTo(5, R.inc)` → `6` — flipped `call` |

### Accessing data

| Task | Function | Example |
|---|---|---|
| Get property | `prop('name', obj)` | `R.prop('x', {x: 1})` → `1` |
| Get nested path | `path(['a','b'], obj)` | `R.path(['a','b'], {a:{b:2}})` → `2` |
| Get property or default | `propOr(default, 'name', obj)` | returns `default` if prop is missing or nil |
| Get path or default | `pathOr(default, ['a','b'], obj)` | returns `default` if path is missing |
| Get multiple properties | `props(['a','b'], obj)` | `R.props(['x','y'], {x:1,y:2})` → `[1, 2]` |
| Get multiple paths | `paths([['a'], ['b','c']], obj)` | returns array of results |
| Check if property exists | `has('name', obj)` | returns boolean |
| Check nested path exists | `hasPath(['a','b'], obj)` | returns boolean |
| Test prop satisfies predicate | `propSatisfies(pred, 'name', obj)` | `R.propSatisfies(R.is(Number), 'x', {x:5})` |
| Test path satisfies predicate | `pathSatisfies(pred, ['a','b'], obj)` | |
| Extract values by property | `pluck('name', list)` | `R.pluck('x', [{x:1},{x:2}])` → `[1,2]` |
| Extract sub-objects | `project(['a','b'], list)` | like SQL SELECT columns from list of objects |
| First element | `head(list)` | `[1,2,3]` → `1` |
| Last element | `last(list)` | `[1,2,3]` → `3` |
| All but last | `init(list)` | `[1,2,3]` → `[1,2]` |
| All but first | `tail(list)` | `[1,2,3]` → `[2,3]` |
| Element at index | `nth(idx, list)` | `nth(1, ['a','b','c'])` → `'b'` (0-indexed) |

### Updating objects (immutable)

| Task | Function | Notes |
|---|---|---|
| Set property | `assoc('key', val, obj)` | returns new object |
| Set nested path | `assocPath(['a','b'], val, obj)` | creates intermediate objects as needed |
| Remove property | `dissoc('key', obj)` | returns new object without key |
| Remove nested path | `dissocPath(['a','b'], obj)` | |
| Apply fn to property | `modify('key', fn, obj)` | `modify('x', R.inc, {x:1})` → `{x:2}` |
| Merge right (shallow) | `mergeRight(obj1, obj2)` | obj2 keys win; same as `mergeLeft` but flipped args |
| Merge left (shallow) | `mergeLeft(obj1, obj2)` | obj1 keys win |
| Merge deep right | `mergeDeepRight(obj1, obj2)` | recursively merges, obj2 wins at leaves |
| Merge deep left | `mergeDeepLeft(obj1, obj2)` | recursively merges, obj1 wins at leaves |
| Merge with custom resolver | `mergeWith(fn, obj1, obj2)` | fn called for conflicting keys |
| Merge deep with custom resolver | `mergeDeepWith(fn, obj1, obj2)` | |
| Merge all objects in list | `mergeAll([obj1, obj2, obj3])` | |
| Transform object structure | `evolve(transformations, obj)` | `evolve({x: R.inc}, {x:1})` → `{x:2}` |
| Pick keys | `pick(['a','b'], obj)` | returns `{a: ..., b: ...}` |
| Pick by predicate | `pickBy(pred, obj)` | `pickBy((val, key) => key === 'a', {a:1,b:2})` |
| Omit keys | `omit(['a','b'], obj)` | returns everything except listed keys |
| Create object from key+value | `objOf('key', val)` | `{key: val}` |
| Invert keys and values | `invert(obj)` | `{a:'x', b:'y'}` → `{x:'a', y:'b'}` |
| Test object shape | `where({x: R.is(Number)})` | | returns boolean if all spec fns return truthy |
| Test any matching | `whereAny({x: gt(0), y: gt(0)})` | returns boolean if any spec fn returns truthy |
| Test exact equality | `whereEq({a: 1, b: 2})` | shorthand for where with `equals` |

### Lens (composable getters and setters)

| Task | Function | Notes |
|---|---|---|
| Create lens on property | `lensProp('name')` | focuses on a single prop |
| Create lens on path | `lensPath(['a','b'])` | focuses on a nested path |
| Create lens on index | `lensIndex(0)` | focuses on an array index |
| Custom lens | `lens(getter, setter)` | `lens(R.prop('x'), R.assoc('x'))` |
| Get through lens | `view(lens, obj)` | read the focused value |
| Set through lens | `set(lens, val, obj)` | overwrite the focused value |
| Transform through lens | `over(lens, fn, obj)` | apply fn to focused value |
| Compose lenses | `compose(lensProp('a'), lensProp('b'))` | focus deeper |

### Searching and finding

| Task | Function | Notes |
|---|---|---|
| Find first match | `find(pred, list)` | returns element or undefined |
| Find last match | `findLast(pred, list)` | |
| Find index | `findIndex(pred, list)` | returns index or -1 |
| Find last index | `findLastIndex(pred, list)` | |
| Check if any match | `any(pred, list)` | returns boolean |
| Check if all match | `all(pred, list)` | returns boolean |
| Check if none match | `none(pred, list)` | returns boolean |
| Count matches | `count(pred, list)` | returns number |
| Check if element exists | `includes(val, list)` | also works for strings |
| Index of element | `indexOf(val, list)` | uses `equals` |
| Last index of element | `lastIndexOf(val, list)` | |

### Sorting and ordering

| Task | Function | Notes |
|---|---|---|
| Sort (natural) | `sort(comparator, list)` | mutates a copy, not the original |
| Sort by function | `sortBy(fn, list)` | `sortBy(R.prop('age'), people)` |
| Sort by multiple criteria | `sortWith([fn1, fn2], list)` | tie-breaking |
| Ascending comparator | `ascend(fn, a, b)` | used with `sort` |
| Descending comparator | `descend(fn, a, b)` | used with `sort` |
| Natural ascending (locale) | `ascendNatural(fn, a, b)` | |
| Natural descending (locale) | `descendNatural(fn, a, b)` | |
| Custom comparator builder | `comparator(fn)` | wraps a binary predicate as a comparator |
| Find maximum | `max(a, b)` | |
| Find minimum | `min(a, b)` | |
| Maximum by function | `maxBy(fn, a, b)` | |
| Minimum by function | `minBy(fn, a, b)` | |
| Clamp between values | `clamp(min, max, val)` | |

### Conditionals and logic

| Task | Function | Notes |
|---|---|---|
| If-then-else | `ifElse(pred, onTrue, onFalse)` | returns a function |
| When true | `when(pred, fn)` | applies fn only if pred passes |
| Unless true | `unless(pred, fn)` | applies fn only if pred fails |
| Multi-condition | `cond([[pred, fn], [pred, fn]])` | first matching predicate wins |
| Both predicates | `both(pred1, pred2)` | logical AND of two predicates |
| Either predicate | `either(pred1, pred2)` | logical OR of two predicates |
| Negate predicate | `complement(pred)` | returns a negated predicate |
| All pass (validation) | `allPass([pred1, pred2])` | all must return truthy |
| Any pass | `anyPass([pred1, pred2])` | at least one must return truthy |
| Default value | `defaultTo(default, val)` | returns default if val is nil/NaN |
| Loop until condition | `until(pred, fn, seed)` | `until(R.gt(100), R.multiply(2), 1)` → `128` |

### Math

| Task | Function | Notes |
|---|---|---|
| Add | `add(a, b)` | coerces to Number |
| Subtract | `subtract(a, b)` | |
| Multiply | `multiply(a, b)` | |
| Divide | `divide(a, b)` | |
| Modulo | `modulo(a, b)` | remainder (sign matches divisor) |
| Math modulo | `mathMod(a, b)` | mathematical modulo (always non-negative) |
| Increment | `inc(n)` | |
| Decrement | `dec(n)` | |
| Negate | `negate(n)` | |
| Sum list | `sum(list)` | |
| Product of list | `product(list)` | |
| Mean | `mean(list)` | |
| Median | `median(list)` | |

### List operations

| Task | Function | Notes |
|---|---|---|
| Take first n | `take(n, list)` | |
| Take last n | `takeLast(n, list)` | |
| Take while predicate | `takeWhile(pred, list)` | |
| Take last while predicate | `takeLastWhile(pred, list)` | |
| Drop first n | `drop(n, list)` | |
| Drop last n | `dropLast(n, list)` | |
| Drop while predicate | `dropWhile(pred, list)` | |
| Drop last while predicate | `dropLastWhile(pred, list)` | |
| Drop consecutive dupes | `dropRepeats(list)` | uses `equals` |
| Drop consecutive dupes by fn | `dropRepeatsBy(fn, list)` | |
| Slice | `slice(start, end, list)` | |
| Split at index | `splitAt(idx, list)` | `[before, after]` |
| Split every n | `splitEvery(n, list)` | chunks |
| Split when predicate | `splitWhen(pred, list)` | split at first match |
| Split whenever predicate | `splitWhenever(pred, list)` | split at every match |

### Adding and removing

| Task | Function | Notes |
|---|---|---|
| Append | `append(el, list)` | non-mutating |
| Prepend | `prepend(el, list)` | non-mutating |
| Insert at index | `insert(idx, el, list)` | |
| Insert all at index | `insertAll(idx, els, list)` | |
| Remove by index | `remove(idx, count, list)` | |
| Without elements | `without(elsToRemove, list)` | uses `equals` for comparison |
| Concatenate | `concat(a, b)` | works on lists and strings |
| Reverse | `reverse(list)` | |
| Move element | `move(from, to, list)` | |
| Swap elements | `swap(idx1, idx2, list)` | |

### Set operations

| Task | Function | Notes |
|---|---|---|
| Unique elements | `uniq(list)` | uses `equals` |
| Unique by function | `uniqBy(fn, list)` | |
| Unique with comparator | `uniqWith(pred, list)` | |
| Difference | `difference(list1, list2)` | elements in list1 not in list2 |
| Difference with fn | `differenceWith(pred, list1, list2)` | custom equality |
| Union | `union(list1, list2)` | combines unique elements |
| Union with fn | `unionWith(pred, list1, list2)` | |
| Intersection | `intersection(list1, list2)` | |
| Symmetric difference | `symmetricDifference(list1, list2)` | elements in either but not both |
| Inner join | `innerJoin(pred, list1, list2)` | `innerJoin(R.eqProps('id'), xs, ys)` |

### Grouping

| Task | Function | Notes |
|---|---|---|
| Group by function | `groupBy(fn, list)` | returns object `{key: [items]}` |
| Group consecutive | `groupWith(pred, list)` | groups adjacent matches |
| Index by function | `indexBy(fn, list)` | returns object `{key: item}` |
| Count by function | `countBy(fn, list)` | returns object `{key: count}` |
| Collect by function | `collectBy(fn, list)` | like groupBy but for sorted input |
| Partition | `partition(pred, list)` | `[matching, notMatching]` |

### String operations

| Task | Function | Notes |
|---|---|---|
| Test regex | `test(regex, str)` | returns boolean |
| Match regex | `match(regex, str)` | returns array of matches |
| Replace | `replace(pattern, replacement, str)` | pattern can be regex or string |
| Split | `split(separator, str)` | |
| To lower | `toLower(str)` | |
| To upper | `toUpper(str)` | |
| Trim | `trim(str)` | |
| Starts with | `startsWith(prefix, str)` | |
| Ends with | `endsWith(suffix, str)` | |
| Join | `join(separator, list)` | |

### Type checking

| Task | Function | Notes |
|---|---|---|
| Type name | `type(val)` | returns `'Array'`, `'Object'`, `'String'`, etc. |
| Is type | `is(Type, val)` | `R.is(Array, [])` → `true` |
| Is nil | `isNil(val)` | null or undefined |
| Is empty | `isEmpty(val)` | works on arrays, objects, strings |
| Invoke method | `invoker(arity, method)` | `invoker(0, 'toLowerCase')` |

### Function utilities

| Task | Function | Notes |
|---|---|---|
| Curry | `curry(fn)` | auto-curries a function |
| Curry with explicit arity | `curryN(n, fn)` | |
| Flip argument order | `flip(fn)` | `flip(R.subtract)(1, 5)` → `4` |
| Fix arity to n | `nAry(n, fn)` | restrict to n arguments |
| Fix arity to 1 | `unary(fn)` | |
| Fix arity to 2 | `binary(fn)` | |
| Un-curry | `uncurryN(n, fn)` | returns uncurried function |
| Return value | `always(val)` | `always(5)()` → `5` |
| Return input | `identity(val)` | pass-through |
| Placeholder | `__` | skip argument in partial application |
| Partial application | `partial(fn, [a, __, b])` | |
| Partial from right | `partialRight(fn, [a, b])` | apply rightmost args |
| Partial with object | `partialObject(fn, {key: val})` | named partial application |
| Run once | `once(fn)` | subsequent calls return first result |
| Memoize | `memoizeWith(keyFn, fn)` | cache by key |
| Try-catch as expression | `tryCatch(tryFn, catchFn)` | returns a fn that won't throw |
| Lift to arrays | `lift(fn)` | `lift(R.add)([1,2], [3,4])` → `[4,5,5,6]` |
| Lift with arity | `liftN(n, fn)` | |

### Relation

| Task | Function | Notes |
|---|---|---|
| Value equality | `equals(a, b)` | deep structural equality |
| Reference equality | `identical(a, b)` | strict `===` |
| Greater than | `gt(a, b)` | |
| Greater or equal | `gte(a, b)` | |
| Less than | `lt(a, b)` | |
| Less or equal | `lte(a, b)` | |
| Equality by function | `eqBy(fn, a, b)` | `eqBy(R.prop('id'), obj1, obj2)` |
| Props equal | `eqProps('key', obj1, obj2)` | |

## Common patterns

### Data transformation pipeline

```js
const processUsers = R.pipe(
  R.filter(R.propSatisfies(R.lte(18), 'age')),     // keep adults (age >= 18)
  R.map(R.pick(['id', 'name', 'email'])),           // select fields
  R.sortBy(R.prop('name'))                           // sort alphabetically
);
processUsers(users);
```

### Conditional value in a pipeline

```js
const describeUser = R.pipe(
  R.when(
    R.propSatisfies(R.lte(65), 'age'),  // 65 <= age
    R.assoc('status', 'senior')
  ),
  R.ifElse(
    R.propSatisfies(R.lte(18), 'age'),  // 18 <= age
    R.assoc('category', 'adult'),
    R.assoc('category', 'minor')
  )
);
```

### Validating input with allPass

```js
const isValidUser = R.allPass([
  R.propSatisfies(R.is(String), 'name'),
  R.propSatisfies(R.is(Number), 'age'),
  R.propSatisfies(R.lte(0), 'age'),   // non-negative (0 <= age)
  R.has('email')
]);
```

### Deep object update with lens

```js
const nameLens = R.lensPath(['user', 'profile', 'name']);
const capitalized = R.over(nameLens, R.toUpper, state);
```

### Safe nested access

```js
// Instead of: obj && obj.a && obj.a.b && obj.a.b.c
const getCity = R.pathOr('Unknown', ['address', 'city']);
getCity(user); // never throws
```

### Point-free comparison for sorting

```js
const byAgeDesc = R.sortWith([
  R.descend(R.prop('age')),
  R.ascend(R.prop('name'))  // tie-break by name
]);
byAgeDesc(people);
```

### Merging configs with precedence

```js
// Defaults (left) get overridden by user config (right)
const withDefaults = R.mergeDeepRight(defaultConfig);
const finalConfig = withDefaults(userConfig);
```

### Uniq by property

```js
const uniqById = R.uniqBy(R.prop('id'));
uniqById([{id:1}, {id:2}, {id:1}]); // [{id:1}, {id:2}]
```

## Anti-patterns to flag

When reviewing code that uses Ramda, watch for these and suggest alternatives.

### Calling functions with too many arguments passed manually

```js
// Bad: manually passing data defeats currying
const result = R.map(x => x * 2, data);

// Good: take advantage of currying
const double = R.map(x => x * 2);
const result = double(data);
// Or inline:
const result = R.map(x => x * 2)(data);
```

### Using Ramda for things native JS does well

```js
// Unnecessary: Ramda wrapping native operations
R.add(1, 2)        // just use 1 + 2 when known values
R.equals(a, b)     // OK — deep structural, better than === for objects

// Worth it: composition, currying, deep operations
const incrementAll = R.map(R.add(1));  // R.add is curried and composable
```

### Over-composing when a simple function would do

```js
// Over-composed: hard to read, hard to debug
const fn = R.compose(R.prop('x'), R.head, R.filter(R.gt(0)), R.map(R.inc));

// Better: break into named steps or use pipe for readability
const fn = R.pipe(
  R.map(R.inc),
  R.filter(R.gt(0)),
  R.head,
  R.prop('x')
);
```

### Forgetting that map works on objects too

```js
// Unnecessary: converting object to entries just to map
const result = R.pipe(R.toPairs, R.map(([k, v]) => [k, v * 2]), R.fromPairs);

// Better: R.map works directly on objects
const result = R.map(R.multiply(2), obj);
```

### Using reduce when a specialized function exists

```js
// Reinventing: implementing groupBy with reduce
R.reduce((acc, x) => { const k = f(x); acc[k] = [...(acc[k]||[]), x]; return acc; }, {})

// Better: Ramda has it built in
R.groupBy(f, list)
```

## Placeholder patterns

The `R.__` placeholder lets you skip arguments in partial application.

```js
const divideBy2 = R.divide(R.__, 2);  // creates fn: (x) => x / 2
divideBy2(10); // 5

const half = R.divide(R.__, 2);

const greet = R.concat('Hello, ');
const greetWithName = R.concat(R.__, '!');
```

## When NOT to use Ramda

- **Simple operations on known values**: `R.add(1, 2)` is overkill when `1 + 2` works
- **Single property access**: `obj.a` is clearer than `R.prop('a', obj)` unless you need the curried form
- **Performance-critical hot loops**: The currying and copying overhead adds up. Use native methods in tight loops
- **TypeScript-heavy codebases without good types**: Ramda's heavy currying can produce complex TypeScript types. The `@types/ramda` package helps but can be complex for advanced patterns. Consider `ts-toolbelt` or `fp-ts` if type ergonomics are a priority
- **Projects that already use lodash/fp**: Lodash/fp has a similar API. Don't mix both without good reason
