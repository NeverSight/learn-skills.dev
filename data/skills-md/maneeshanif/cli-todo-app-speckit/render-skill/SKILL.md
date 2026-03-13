---
name: render-skill
description: Create beautiful Rich terminal output with tables, panels, progress bars, and styled text. Use when building terminal UI components.
allowed-tools: Write, Read
---

# Render Skill

## Purpose
Create stunning terminal output using the Rich library.

## Instructions

### Console Setup
```python
from rich.console import Console
from rich.theme import Theme

# Custom theme
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "title": "bold magenta",
    "dim": "dim white",
})

console = Console(theme=custom_theme)
```

### Task Table
```python
from rich.table import Table
from rich.text import Text
from rich.box import ROUNDED, DOUBLE, HEAVY

def render_task_table(tasks: list) -> Table:
    """Render tasks in a beautiful table."""
    
    table = Table(
        title="📋 Your Tasks",
        title_style="bold cyan",
        border_style="bright_blue",
        header_style="bold magenta",
        box=ROUNDED,
        show_lines=True,
        padding=(0, 1),
        expand=True
    )
    
    # Define columns
    table.add_column("ID", style="dim", width=4, justify="right")
    table.add_column("Title", style="bold white", min_width=20, max_width=40)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Status", justify="center", width=12)
    table.add_column("Tags", style="cyan", width=15)
    table.add_column("Due", style="yellow", width=12)
    
    # Priority styling
    priority_styles = {
        "urgent": ("🔴", "bold red"),
        "high": ("🟠", "bold orange1"),
        "medium": ("🟡", "bold yellow"),
        "low": ("🟢", "bold green"),
    }
    
    # Status icons
    status_display = {
        "pending": ("⏳", "white"),
        "completed": ("✅", "green"),
        "overdue": ("⚠️", "bold red"),
    }
    
    for task in tasks:
        priority = task.get('priority', 'medium')
        status = task.get('status', 'pending')
        tags = ", ".join(task.get('tags', [])) or "-"
        due = task.get('due_date', '-')
        if due and due != '-':
            due = due[:10]  # Just the date part
        
        p_icon, p_style = priority_styles.get(priority, ("", ""))
        s_icon, s_style = status_display.get(status, ("", ""))
        
        table.add_row(
            str(task['id']),
            task['title'],
            Text(f"{p_icon} {priority.upper()}", style=p_style),
            Text(f"{s_icon} {status.title()}", style=s_style),
            tags,
            due if due else "-"
        )
    
    return table
```

### Panels
```python
from rich.panel import Panel
from rich.align import Align

def render_task_detail(task: dict) -> Panel:
    """Render task details in a panel."""
    from rich.text import Text
    
    content = Text()
    content.append(f"Title: ", style="bold")
    content.append(f"{task['title']}\n", style="cyan")
    content.append(f"Priority: ", style="bold")
    content.append(f"{task.get('priority', 'medium').upper()}\n", style="yellow")
    content.append(f"Status: ", style="bold")
    content.append(f"{task.get('status', 'pending').title()}\n", style="green")
    
    if task.get('description'):
        content.append(f"\nDescription:\n", style="bold")
        content.append(f"{task['description']}\n", style="dim")
    
    if task.get('tags'):
        content.append(f"\nTags: ", style="bold")
        content.append(f"{', '.join(task['tags'])}\n", style="cyan")
    
    return Panel(
        content,
        title=f"[bold]Task #{task['id']}[/bold]",
        border_style="bright_blue",
        padding=(1, 2)
    )
```

### Progress Bars
```python
from rich.progress import (
    Progress, SpinnerColumn, TextColumn, 
    BarColumn, TaskProgressColumn, TimeRemainingColumn
)
import time

def show_loading():
    """Show loading spinner."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        transient=True
    ) as progress:
        progress.add_task("Loading...", total=None)
        time.sleep(2)

def show_progress(items: list, description: str = "Processing"):
    """Show progress bar for operations."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task(description, total=len(items))
        for item in items:
            # Process item...
            progress.update(task, advance=1)
            time.sleep(0.1)
```

### Status Messages
```python
def print_success(message: str):
    """Print success message."""
    console.print(f"✅ {message}", style="success")

def print_error(message: str):
    """Print error message."""
    console.print(f"❌ {message}", style="error")

def print_warning(message: str):
    """Print warning message."""
    console.print(f"⚠️ {message}", style="warning")

def print_info(message: str):
    """Print info message."""
    console.print(f"ℹ️ {message}", style="info")
```

### Dashboard Layout
```python
from rich.columns import Columns
from rich.panel import Panel

def render_dashboard(stats: dict) -> None:
    """Render a dashboard with statistics."""
    
    panels = [
        Panel(
            f"[bold cyan]{stats['total']}[/]",
            title="Total Tasks",
            border_style="cyan"
        ),
        Panel(
            f"[bold green]{stats['completed']}[/]",
            title="Completed",
            border_style="green"
        ),
        Panel(
            f"[bold yellow]{stats['pending']}[/]",
            title="Pending",
            border_style="yellow"
        ),
        Panel(
            f"[bold red]{stats['overdue']}[/]",
            title="Overdue",
            border_style="red"
        ),
    ]
    
    console.print(Columns(panels, equal=True))
```

### Empty State
```python
def render_empty_state():
    """Render empty state message."""
    console.print(
        Panel(
            Align.center(
                "[dim]No tasks found.\n\n"
                "[cyan]Create your first task with:[/]\n"
                "[bold white]todo add[/]"
            ),
            title="📋 Empty",
            border_style="dim"
        )
    )
```

## Best Practices

- Use consistent styling throughout the app
- Include icons for visual cues
- Handle empty states gracefully
- Use color to convey meaning (red=error, green=success)
- Add padding and spacing for readability
- Use panels to group related content
- Keep tables readable with proper column widths
