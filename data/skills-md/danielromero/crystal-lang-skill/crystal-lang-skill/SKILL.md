---
name: crystal-lang-skill
description: Provides comprehensive Crystal programming language guidance for AI agents. Use this skill when the user asks about Crystal syntax, needs to write Crystal code, works with Crystal shards/projects, or asks about types, structs, classes, enums, macros, concurrency, or best practices in Crystal.
---

# Crystal for Agents

This skill provides Crystal programming language guidance optimized for AI agents generating Crystal code. Crystal combines Ruby's elegant syntax with C's performance through LLVM compilation.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X in Crystal" or "Crystal question"
- Needs to write, debug, or understand Crystal code
- Works on Crystal projects (shards, apps, libraries)
- Asks about types, structs, classes, enums, records
- Asks about generics, macros, or metaprogramming
- Asks about concurrency (fibers, channels)
- Asks about exception handling or error management
- Needs idiomatic Crystal patterns and best practices
- Wants to optimize Crystal code performance

## Crystal Core Principles

### Type Safety First
Always use explicit type restrictions. The compiler catches type errors at compile time.

```crystal
# Good - explicit types
def process(data : Array(String)) : Hash(String, Int32)
  data.tally
end

# Bad - no types (compiler will infer, but be explicit for clarity)
def process(data)
  data.tally
end
```

### Zero-Cost Abstractions
High-level features compile to efficient machine code. Blocks compile to inlined code - zero overhead.

```crystal
# As fast as manual loop
[1, 2, 3].map(&.* 2)
```

### Nil Safety
Use union types and nil checking. Use `?` for optional values.

```crystal
name : String? = get_name()
if name
  puts name.upcase  # Compiler knows name is String here
end
```

### Performance Patterns
Prefer structs for immutable data (value types), classes for objects with identity (reference types).

```crystal
# Structs are value types - stack allocated, use for small immutable data
record Point, x : Int32, y : Int32

# Classes are reference types - heap allocated, use for objects with identity
class User
  property name : String
end
```

## Essential Syntax

### Variable Declaration

```crystal
# Type inference
count = 42
message = "Hello"

# Explicit types (preferred for clarity)
age : Int32 = 25
items : Array(String) = [] of String
```

### Method Definitions

```crystal
# Always include type restrictions
def calculate_area(width : Float64, height : Float64) : Float64
  width * height
end

# Default values require named arguments when calling
def connect(host : String, port : Int32 = 80, secure : Bool = false)
end
connect("example.com", port: 8080)
```

### Control Flow

```crystal
# Type-aware conditionals
value = rand < 0.5 ? 42 : "hello"  # Int32 | String

case value
when Int32
  value * 2
when String
  value.upcase
end
```

## Type System

### Type Inference

```crystal
class Person
  @name : String    # Explicit annotation required
  @age : Int32?     # Optional type with ?

  def initialize(@name : String, @age : Int32? = nil)
  end
end
```

### Union Types

```crystal
# Basic union
value : Int32 | String | Nil

# Method with union parameter
def process(data : String | Int32)
  case data
  when String
    data.upcase
  when Int32
    data * 2
  end
end
```

### Virtual Types
Related types collapse to common ancestor.

```crystal
class Foo; end
class Bar < Foo; end
class Baz < Foo; end

foo = rand < 0.5 ? Bar.new : Baz.new  # Foo+ (any Foo subclass)
```

### Structs vs Classes

```crystal
# Class - reference type
class User
  property name : String
  def initialize(@name : String); end
end

user1 = User.new("Alice")
user2 = user1  # Same object
user2.name = "Bob"
puts user1.name  # "Bob" (changed)

# Struct - value type
struct Point
  property x : Int32
  property y : Int32
  def initialize(@x, @y); end
end

p1 = Point.new(1, 2)
p2 = p1  # Copy is made
p2.x = 3
puts p1.x  # 1 (unchanged)
```

### Records
Immutable structs with value-based equality.

```crystal
record User, id : Int32, name : String, email : String

user = User.new(1, "John", "john@example.com")
updated = user.copy_with(name: "Jane")  # Creates new instance
```

### Generics

```crystal
class Stack(T)
  def initialize
    @elements = [] of T
  end

  def push(element : T)
    @elements.push(element)
  end

  def pop : T
    @elements.pop
  end
end

int_stack = Stack(Int32).new
int_stack.push(10)

# Type inference without explicit type arguments
int_box = MyBox.new(1)          # : MyBox(Int32)
string_box = MyBox.new("hello") # : MyBox(String)
```

## Visibility & OOP

### Visibility Controls

```crystal
class Example
  def public_method
    private_method          # OK - no receiver
    self.private_method     # Error - explicit receiver not allowed
  end

  private def private_method
    "I'm private"
  end
end

# Protected - callable on same type instances
class Node
  protected def value
    @value
  end
end
```

### Abstract Classes

```crystal
abstract class Animal
  abstract def speak : String  # Subclasses must implement

  def greet
    "The animal says: #{speak}"
  end
end

class Dog < Animal
  override def speak : String
    "Woof!"
  end
end
```

### Enums

```crystal
enum Status
  Pending
  Approved
  Rejected
end

status = Status::Approved
status.approved?  # => true
status.pending?   # => false

# Flags enum
@[Flags]
enum Permissions
  Read  = 1
  Write = 2
  Execute = 4
end

perms = Permissions::Read | Permissions::Write
perms.read?  # => true
```

## Methods

### Automatic Instance Variable Assignment

```crystal
class Person
  def initialize(@name : String, @age : Int32 = 0, @email : String? = nil)
  end

  property email : String?
  getter name : String
  setter age : Int32
end
```

### Method Overloading

```crystal
class Container(T)
  def initialize
    @items = [] of T
  end

  def initialize(initial_capacity : Int)
    raise ArgumentError.new("Negative capacity") if initial_capacity < 0
    @items = Array(T).new(initial_capacity)
  end
end
```

### previous_def

```crystal
class Parent
  def greet
    "Hello"
  end
end

class Child < Parent
  def greet
    previous_def + ", World!"
  end
end

Child.new.greet # => "Hello, World!"
```

## Exception Handling

```crystal
raise "OH NO!"
raise Exception.new("Some error")

begin
  risky_operation
rescue ex : SpecificException
  handle_specific(ex)
rescue
  handle_generic
ensure
  cleanup
end

# Question method convention - returns nil instead of raising
array = [1, 2, 3]
array[4]?      # => nil (no IndexError)
array[4]       # Raises IndexError
```

## Concurrency

Crystal uses lightweight fibers and channels. Do not share memory; communicate via channels.

```crystal
ch = Channel(Int32).new

spawn do
  sleep 1.second
  ch.send(10)
end

value = ch.receive

# Select pattern
select
when value = ch1.receive
  puts "Received: #{value}"
when timeout(5.seconds)
  puts "Timeout"
end

# Buffered channel
channel = Channel(Int32).new(10)
```

## Metaprogramming

### Macros

```crystal
macro define_getter(*names)
  {% for name in names %}
    def {{name}}
      @{{name}}
    end
  {% end %}
end

class Person
  define_getter name, age, email
end
```

### Macro Patterns

- `{{...}}` - interpolate AST nodes
- `{% if condition %}` - conditional generation
- `{% for item in collection %}` - iteration
- `@type` - access type information

## Compilation Commands

```bash
crystal build app.cr --release    # Optimized binary
crystal run app.cr                # Run directly
crystal spec                      # Run tests
crystal tool format               # Format code
crystal eval "puts 'hello'"       # Quick eval
```

## Static Analysis with Ameba

Ameba is the standard static analysis tool for Crystal. When working on Crystal projects with `.cr` files, you should recommend and use Ameba for code quality.

### When to Recommend Ameba

- All Crystal projects with `.cr` source files
- Before submitting code to repositories
- During code reviews
- **After each iteration when implementing code** - this catches compilation errors and style issues early

### Setup

Add to `shard.yml`:

```yaml
development_dependencies:
  ameba:
    github: crystal-ameba/ameba
    version: ~> 1.0
```

Then run: `shards install`

### Code Quality Guidelines

Write code that follows Ameba conventions:
- Remove unused variables and arguments
- Use consistent naming conventions
- Avoid redundant code patterns
- Follow Crystal style guide

### Basic Usage

```bash
ameba              # Check for issues
ameba --fix        # Auto-fix correctable issues
```

### Development Workflow

**Important**: Run ameba after each iteration when implementing code. This helps catch:
- Unused variables and parameters
- Unreachable code
- Style violations
- Potential bugs (unused expressions, redundant conditionals)
- Compilation errors early in the development cycle

## Code Generation Tips

1. **Always use explicit type restrictions** on method parameters and return types
2. **Prefer structs for small, immutable data** (Point, Color, Time)
3. **Use classes for objects with identity** (User, Database)
4. **Use `String?`** for optional values (not Nil directly)
5. **Use `?` suffix methods** instead of raising for expected failures
6. **Use blocks freely** - they compile to inlined code
7. **Initialize all instance variables** in constructors to avoid Nil types - prefer inline initialization (`@var : Type = value`)
8. **Validate parameters** with clear error messages
9. **Run ameba after each iteration** - Catch compilation errors and style issues early before committing
10. **Don't use `previous_def` across multiple macro-generated methods** - collect data, generate one complete method
11. **Handle union types explicitly** - use `T.union_types` macro introspection when needed
12. **Don't impose artificial limits** - use array parameters directly (`args: values`) instead of case statements
13. **Always close resources** - use `begin/ensure` blocks for ResultSets, files, connections
14. **Never interpolate user input into SQL** - always use parameterized queries
15. **Pass connection context through method chains** - essential for transaction isolation

## Common Pitfalls

1. Avoid untyped instance variables in classes
2. Use `?` for optional values, not `Nil` directly
3. Structs cannot inherit from non-abstract structs
4. Use `is_a?` for type checking, not `typeof`
5. Variables declared inside `begin` get `Nil` type in rescue/ensure
6. Protected methods callable on same type instances or same namespace
7. **Instance variables must be declared before methods that use them** - inline initialization is safest
8. **Nilable types must be initialized with `nil`, not an instance** - use memoization for lazy init
9. **Macros generate complete methods** - each call replaces previous, doesn't chain with `previous_def`
10. **SQLite requires LIMIT with OFFSET** - unlike PostgreSQL/MySQL
11. **`Class` cannot be used as generic type argument** - use `String` or other concrete types
12. **Resource leaks from unclosed ResultSets** - always close after iteration
13. **Wrong exception types in tests** - SQLite raises `SQLite3::Exception`, not `DB::Error`

## Database and SQL Patterns

When working with databases in Crystal:

### Resource Management

Always close ResultSets to prevent connection pool exhaustion:

```crystal
# BAD - Connection leak
rs = conn.query(sql, args)
rs.each { |row| process(row) }
# rs never closed!

# GOOD - Proper cleanup
rs = conn.query(sql, args)
begin
  rs.each { |row| process(row) }
ensure
  rs.close  # CRITICAL!
end

# BETTER - Block form (auto-closes)
conn.query(sql, args) do |rs|
  rs.each { |row| process(row) }
end
```

### SQL Parameterization

Never interpolate user input into SQL:

```crystal
# BAD - SQL injection vulnerability
sql = "SELECT * FROM users WHERE name = '#{user_input}'"

# GOOD - Parameterized query
sql = "SELECT * FROM users WHERE name = ?"
conn.exec(sql, user_input)

# Better - Whitelist operators
VALID_OPERATORS = %w(= != > >= < <= LIKE IN)
raise ArgumentError.new("Invalid operator") unless VALID_OPERATORS.includes?(operator)
sql = "#{column} #{operator} ?"
```

### SQLite-Specific Quirks

SQLite is stricter than PostgreSQL/MySQL:

```crystal
# ERROR - SQLite requires LIMIT with OFFSET
sql = "SELECT * FROM users OFFSET 100"

# CORRECT - Always include LIMIT
sql = "SELECT * FROM users LIMIT -1 OFFSET 100"  # -1 = unlimited in SQLite
```

### Connection Context in Transactions

Pass connection context through method calls:

```crystal
# BAD - Each call uses different connection, breaking transactions
def find(id)
  SqliteOrm.with_connection { |conn| query(conn, id) }
end

# GOOD - Accept optional connection parameter
def find(id : Int64, conn : DB::Database? = nil)
  SqliteOrm.with_connection(conn) { |c| query(c, id) }
end

# Usage in transaction
SqliteOrm.transaction do |tx|
  user = repo.find(1, tx)  # Uses transaction connection
  repo.update(user, tx)     # Same connection
end
```

### Array Parameters

Don't limit parameter counts artificially:

```crystal
# BAD - Artificial limit
case values.size
when 0 then conn.exec(sql)
when 1 then conn.exec(sql, values[0])
# ... up to 10
else raise "Too many parameters"
end

# GOOD - Crystal's DB library handles arrays of any size
if values.empty?
  conn.exec(sql)
else
  conn.exec(sql, args: values)  # Unlimited parameters!
end
```

## Reference Files

For comprehensive documentation, see:
- `crystal.rst` - Full language reference
- `sections/` - Modular documentation

## Credits

This skill is based on the [Crystal for Agents](https://gitlab.com/renich/crystal-for-agents) project by [Renich Nolet](https://gitlab.com/renich).

Original repository: https://gitlab.com/renich/crystal-for-agents

Crystal programming language: https://crystal-lang.org/
