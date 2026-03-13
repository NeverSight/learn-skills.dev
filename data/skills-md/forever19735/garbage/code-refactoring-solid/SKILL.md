---
name: code-refactoring-solid
description: Guide for refactoring Python code to follow SOLID principles and improve maintainability
---

# 🏗️ Code Refactoring with SOLID Principles

## When to use this skill

Use this skill when:
- Refactoring existing code to improve maintainability
- Code has grown complex and difficult to modify
- Adding new features requires changing multiple unrelated parts
- Unit testing is difficult due to tight coupling
- Code violates SOLID principles
- Planning architectural improvements

## How to use it

### 🎯 SOLID Principles Overview

#### S - Single Responsibility Principle (SRP)
**Definition**: A class should have only one reason to change.

**Violations in current codebase**:
```python
# ❌ BAD: DataManager does too much
class DataManager:
    def load_data(self, data_type):
        # Loading logic
    def save_data(self, data_type, data):
        # Saving logic
    def delete_data(self, data_type):
        # Deletion logic
    # Also handles Firebase connection, validation, etc.
```

**Refactored**:
```python
# ✅ GOOD: Separate responsibilities
class FirebaseConnection:
    """Handles Firebase connection only"""
    def connect(self): pass
    def is_available(self): pass

class DataRepository:
    """Handles data CRUD operations only"""
    def __init__(self, connection: FirebaseConnection):
        self.connection = connection
    
    def load(self, data_type): pass
    def save(self, data_type, data): pass
    def delete(self, data_type): pass

class DataValidator:
    """Handles data validation only"""
    def validate_group_ids(self, ids): pass
    def validate_schedule(self, schedule): pass
```

---

#### O - Open/Closed Principle (OCP)
**Definition**: Software entities should be open for extension but closed for modification.

**Violations**:
```python
# ❌ BAD: Must modify function to add new command
def handle_message(event):
    if event.text.startswith("@time"):
        # handle time
    elif event.text.startswith("@day"):
        # handle day
    elif event.text.startswith("@week"):
        # handle week
    # Adding new command requires modifying this function
```

**Refactored**:
```python
# ✅ GOOD: Command pattern - add new commands without modifying handler
class Command(ABC):
    @abstractmethod
    def can_handle(self, text: str) -> bool:
        pass
    
    @abstractmethod
    def execute(self, event) -> str:
        pass

class TimeCommand(Command):
    def can_handle(self, text: str) -> bool:
        return text.startswith("@time")
    
    def execute(self, event) -> str:
        # Handle time command
        pass

class CommandHandler:
    def __init__(self):
        self.commands: List[Command] = []
    
    def register(self, command: Command):
        self.commands.append(command)
    
    def handle(self, event):
        for command in self.commands:
            if command.can_handle(event.text):
                return command.execute(event)
```

---

#### L - Liskov Substitution Principle (LSP)
**Definition**: Objects of a superclass should be replaceable with objects of its subclasses.

**Application**:
```python
# ✅ GOOD: Storage abstraction
class Storage(ABC):
    @abstractmethod
    def save(self, key: str, value: Any) -> bool:
        pass
    
    @abstractmethod
    def load(self, key: str) -> Any:
        pass

class FirebaseStorage(Storage):
    def save(self, key: str, value: Any) -> bool:
        # Firebase implementation
        pass
    
    def load(self, key: str) -> Any:
        # Firebase implementation
        pass

class LocalFileStorage(Storage):
    def save(self, key: str, value: Any) -> bool:
        # File implementation
        pass
    
    def load(self, key: str) -> Any:
        # File implementation
        pass

# Can swap implementations without changing client code
def save_schedule(storage: Storage, schedule):
    storage.save("schedule", schedule)
```

---

#### I - Interface Segregation Principle (ISP)
**Definition**: Clients should not be forced to depend on interfaces they don't use.

**Violations**:
```python
# ❌ BAD: Fat interface
class BotService:
    def handle_message(self): pass
    def handle_join(self): pass
    def handle_leave(self): pass
    def send_broadcast(self): pass
    def schedule_task(self): pass
    def validate_input(self): pass
    # Too many responsibilities
```

**Refactored**:
```python
# ✅ GOOD: Segregated interfaces
class MessageHandler(ABC):
    @abstractmethod
    def handle_message(self, event): pass

class GroupEventHandler(ABC):
    @abstractmethod
    def handle_join(self, event): pass
    @abstractmethod
    def handle_leave(self, event): pass

class BroadcastService(ABC):
    @abstractmethod
    def send_broadcast(self, group_id: str, message: str): pass

class ScheduleService(ABC):
    @abstractmethod
    def schedule_task(self, task): pass
```

---

#### D - Dependency Inversion Principle (DIP)
**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

**Violations**:
```python
# ❌ BAD: Direct dependency on concrete class
class ScheduleManager:
    def __init__(self):
        self.firebase = firebase_service.firebase_service_instance  # Tight coupling
    
    def save_schedule(self, schedule):
        self.firebase.save_group_schedules(schedule)
```

**Refactored**:
```python
# ✅ GOOD: Depend on abstraction
class ScheduleRepository(ABC):
    @abstractmethod
    def save(self, schedule): pass
    @abstractmethod
    def load(self): pass

class ScheduleManager:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository  # Depends on abstraction
    
    def save_schedule(self, schedule):
        self.repository.save(schedule)

# Concrete implementation
class FirebaseScheduleRepository(ScheduleRepository):
    def __init__(self, firebase_service):
        self.firebase = firebase_service
    
    def save(self, schedule):
        return self.firebase.save_group_schedules(schedule)
    
    def load(self):
        return self.firebase.load_group_schedules()
```

---

### 🔧 Refactoring Patterns

#### 1. Extract Class
**When**: A class is doing too much

```python
# Before
class BotHandler:
    def parse_time(self, text): pass
    def parse_members(self, text): pass
    def validate_time(self, hour, minute): pass
    def validate_members(self, members): pass
    def format_message(self, action, details): pass
    def handle_command(self, event): pass

# After
class InputParser:
    def parse_time(self, text): pass
    def parse_members(self, text): pass

class InputValidator:
    def validate_time(self, hour, minute): pass
    def validate_members(self, members): pass

class MessageFormatter:
    def format_success(self, action, details): pass
    def format_error(self, error): pass

class BotHandler:
    def __init__(self, parser, validator, formatter):
        self.parser = parser
        self.validator = validator
        self.formatter = formatter
    
    def handle_command(self, event): pass
```

#### 2. Extract Method
**When**: A method is too long or does multiple things

```python
# Before
def handle_time_command(event):
    parts = event.text.split()
    if len(parts) < 2:
        return "Error"
    time_str = parts[1]
    patterns = [r'^(\d{1,2}):(\d{2})$', r'^(\d{2})(\d{2})$']
    hour, minute = None, None
    for pattern in patterns:
        match = re.match(pattern, time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            break
    if not (0 <= hour <= 23):
        return "Hour error"
    # ... more logic

# After
def handle_time_command(event):
    time_str = extract_time_parameter(event.text)
    if not time_str:
        return format_missing_parameter_error()
    
    hour, minute, error = parse_time_flexible(time_str)
    if error:
        return error
    
    return update_schedule_time(event.group_id, hour, minute)

def extract_time_parameter(text: str) -> Optional[str]:
    parts = text.split(maxsplit=1)
    return parts[1] if len(parts) >= 2 else None
```

#### 3. Introduce Parameter Object
**When**: Functions have too many parameters

```python
# Before
def update_schedule(group_id, days, hour, minute, timezone, enabled):
    pass

# After
@dataclass
class ScheduleConfig:
    group_id: str
    days: str
    hour: int
    minute: int
    timezone: str = "Asia/Taipei"
    enabled: bool = True

def update_schedule(config: ScheduleConfig):
    pass
```

#### 4. Replace Conditional with Polymorphism
**When**: Complex if/elif chains for different types

```python
# Before
def format_message(message_type, data):
    if message_type == "success":
        return f"✅ {data['action']}\n{data['details']}"
    elif message_type == "error":
        return f"❌ {data['error']}\n{data['suggestion']}"
    elif message_type == "warning":
        return f"⚠️ {data['warning']}"

# After
class Message(ABC):
    @abstractmethod
    def format(self) -> str:
        pass

class SuccessMessage(Message):
    def __init__(self, action: str, details: dict):
        self.action = action
        self.details = details
    
    def format(self) -> str:
        return f"✅ {self.action}\n{self.details}"

class ErrorMessage(Message):
    def __init__(self, error: str, suggestion: str):
        self.error = error
        self.suggestion = suggestion
    
    def format(self) -> str:
        return f"❌ {self.error}\n{self.suggestion}"
```

---

### 📋 Refactoring Checklist

#### Before Refactoring
- [ ] Write tests for existing functionality
- [ ] Identify code smells (long methods, large classes, duplicate code)
- [ ] Document current behavior
- [ ] Create backup/branch

#### During Refactoring
- [ ] Make small, incremental changes
- [ ] Run tests after each change
- [ ] Keep commits atomic and descriptive
- [ ] Maintain backward compatibility if needed

#### After Refactoring
- [ ] Verify all tests pass
- [ ] Check performance hasn't degraded
- [ ] Update documentation
- [ ] Code review

---

### 🚨 Code Smells to Watch For

1. **Long Method** (>20 lines) → Extract Method
2. **Large Class** (>200 lines) → Extract Class
3. **Long Parameter List** (>3 params) → Introduce Parameter Object
4. **Duplicate Code** → Extract Method/Class
5. **Feature Envy** (method uses another class more than its own) → Move Method
6. **Data Clumps** (same group of data together) → Extract Class
7. **Primitive Obsession** (using primitives instead of objects) → Introduce Value Object
8. **Switch Statements** (type checking) → Replace with Polymorphism

---

### 🎯 Refactoring Priority for Current Codebase

#### High Priority
1. **Extract Command Handlers** - Massive `handle_message()` function
2. **Separate Data Access** - DataManager does too much
3. **Introduce Storage Abstraction** - Tight coupling to Firebase

#### Medium Priority
4. **Extract Parsing Logic** - Scattered parsing code
5. **Introduce Message Formatters** - Duplicate formatting code
6. **Extract Validation** - Validation mixed with business logic

#### Low Priority
7. **Introduce Value Objects** - For ScheduleConfig, MemberGroup
8. **Extract Helper Functions** - Utility functions in main file

---

### 📚 References

- **Clean Code** by Robert C. Martin
- **Refactoring** by Martin Fowler
- **Design Patterns** by Gang of Four
- [Python SOLID Principles](https://realpython.com/solid-principles-python/)
- [Refactoring Guru](https://refactoring.guru/)

---

**Last Updated**: 2026-01-16  
**Maintainer**: Code Quality Agent
