---
name: crud-skill
description: Implement Create, Read, Update, Delete operations for todo tasks. Use when building data management functionality.
allowed-tools: Write, Read
---

# CRUD Skill

## Purpose
Implement robust CRUD operations for todo task management.

## Instructions

### Service Layer Pattern
```python
from typing import Optional, List
from datetime import datetime

class TodoService:
    """Service layer for todo task operations."""
    
    def __init__(self, database):
        self.db = database
    
    # CREATE
    def create_task(self, task_data: dict) -> dict:
        """Create a new task with auto-generated metadata."""
        now = datetime.now().isoformat()
        task_data['created_at'] = now
        task_data['updated_at'] = now
        task_data['status'] = task_data.get('status', 'pending')
        
        task_id = self.db.insert(task_data)
        task_data['id'] = task_id
        return task_data
    
    # READ
    def get_task(self, task_id: int) -> Optional[dict]:
        """Get a single task by ID."""
        return self.db.get(task_id)
    
    def get_all_tasks(self) -> List[dict]:
        """Get all tasks."""
        return self.db.get_all()
    
    def get_tasks_by_status(self, status: str) -> List[dict]:
        """Get tasks filtered by status."""
        return self.db.search(self.db.query.status == status)
    
    # UPDATE
    def update_task(self, task_id: int, updates: dict) -> Optional[dict]:
        """Update a task and return updated version."""
        updates['updated_at'] = datetime.now().isoformat()
        success = self.db.update(task_id, updates)
        if success:
            return self.get_task(task_id)
        return None
    
    def complete_task(self, task_id: int) -> Optional[dict]:
        """Mark a task as complete."""
        return self.update_task(task_id, {
            'status': 'completed',
            'completed_at': datetime.now().isoformat()
        })
    
    def uncomplete_task(self, task_id: int) -> Optional[dict]:
        """Mark a task as pending (uncomplete)."""
        return self.update_task(task_id, {
            'status': 'pending',
            'completed_at': None
        })
    
    def toggle_complete(self, task_id: int) -> Optional[dict]:
        """Toggle task completion status."""
        task = self.get_task(task_id)
        if not task:
            return None
        if task['status'] == 'completed':
            return self.uncomplete_task(task_id)
        return self.complete_task(task_id)
    
    # DELETE
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        return self.db.delete(task_id)
    
    def delete_completed(self) -> int:
        """Delete all completed tasks. Returns count deleted."""
        completed = self.get_tasks_by_status('completed')
        count = 0
        for task in completed:
            if self.delete_task(task['id']):
                count += 1
        return count
```

### Validation Before Operations
```python
def create_task(self, task_data: dict) -> dict:
    """Create with validation."""
    # Validate required fields
    if not task_data.get('title'):
        raise ValueError("Title is required")
    
    # Validate title length
    if len(task_data['title']) > 200:
        raise ValueError("Title must be 200 characters or less")
    
    # Validate priority
    valid_priorities = ['low', 'medium', 'high', 'urgent']
    priority = task_data.get('priority', 'medium')
    if priority not in valid_priorities:
        raise ValueError(f"Priority must be one of: {valid_priorities}")
    
    # Proceed with creation
    return self._do_create(task_data)
```

### Error Handling Pattern
```python
from typing import Union

class TaskResult:
    """Result wrapper for operations."""
    def __init__(self, success: bool, data=None, error: str = None):
        self.success = success
        self.data = data
        self.error = error

def safe_create_task(self, task_data: dict) -> TaskResult:
    """Create task with error handling."""
    try:
        task = self.create_task(task_data)
        return TaskResult(True, data=task)
    except ValueError as e:
        return TaskResult(False, error=str(e))
    except Exception as e:
        return TaskResult(False, error=f"Unexpected error: {e}")
```

## Common Operations

### Batch Operations
```python
def create_many(self, tasks: List[dict]) -> List[dict]:
    """Create multiple tasks."""
    return [self.create_task(t) for t in tasks]

def delete_many(self, task_ids: List[int]) -> int:
    """Delete multiple tasks by ID."""
    return sum(1 for id in task_ids if self.delete_task(id))
```

### Existence Checks
```python
def task_exists(self, task_id: int) -> bool:
    """Check if task exists."""
    return self.get_task(task_id) is not None

def get_task_or_raise(self, task_id: int) -> dict:
    """Get task or raise error if not found."""
    task = self.get_task(task_id)
    if not task:
        raise ValueError(f"Task {task_id} not found")
    return task
```

## Best Practices

- Always validate input before operations
- Update `updated_at` on every modification
- Return the modified object after updates
- Use result objects for error handling
- Keep operations atomic and focused
- Log important operations for debugging
