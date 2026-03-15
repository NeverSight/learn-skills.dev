---
name: animation-skill
description: Create splash screens, ASCII art banners, and terminal animations. Use when building visual effects, loading screens, and branding elements.
allowed-tools: Write, Read
---

# Animation Skill

## Purpose
Create eye-catching splash screens and animations for terminal apps.

## Instructions

### Splash Screen with PyFiglet
```python
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import pyfiglet
import time

console = Console()

def show_splash_screen():
    """Display animated splash screen with developer credit."""
    console.clear()
    
    # Generate ASCII art
    logo = pyfiglet.figlet_format("TODO", font="banner3-D")
    
    # Build content
    content = Text()
    content.append(logo, style="bold cyan")
    content.append("\n\n")
    content.append("🎮 Retro Terminal Task Manager 🎮", style="bold magenta")
    content.append("\n\n")
    content.append("━" * 40, style="dim cyan")
    content.append("\n\n")
    content.append("Developer by: ", style="dim white")
    content.append("maneeshanif", style="bold green")
    content.append("\n")
    
    # Create panel
    panel = Panel(
        Align.center(content),
        border_style="bright_cyan",
        padding=(2, 4),
        title="[bold yellow]✨ Welcome ✨[/bold yellow]",
        subtitle="[dim]Press ENTER to continue[/dim]"
    )
    
    console.print(panel)
    input()
    console.clear()
```

### Alternative Fonts
```python
# Available fonts to try:
COOL_FONTS = [
    "banner3-D",   # 3D block letters
    "slant",       # Slanted text
    "doom",        # DOOM game style
    "big",         # Large letters
    "digital",     # Digital clock style
    "standard",    # Classic figlet
    "small",       # Compact
    "smslant",     # Small slant
    "cyberlarge",  # Cyberpunk style
    "cybermedium", # Medium cyberpunk
]

def generate_banner(text: str, font: str = "slant") -> str:
    """Generate ASCII banner with specified font."""
    try:
        return pyfiglet.figlet_format(text, font=font)
    except:
        return pyfiglet.figlet_format(text, font="standard")
```

### Animated Loading
```python
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

def show_loading(message: str = "Loading", duration: float = 2.0):
    """Show animated loading spinner."""
    with Progress(
        SpinnerColumn("dots"),
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        transient=True
    ) as progress:
        task = progress.add_task(message, total=None)
        time.sleep(duration)

def show_typing_effect(text: str, delay: float = 0.03):
    """Display text with typing effect."""
    for char in text:
        console.print(char, end="", style="bold cyan")
        time.sleep(delay)
    console.print()
```

### Animated Welcome
```python
import time

def animated_welcome():
    """Animated welcome sequence."""
    console.clear()
    
    frames = [
        "🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"
    ]
    
    # Moon animation
    for _ in range(2):
        for frame in frames:
            console.print(f"\r{frame} Loading...", end="")
            time.sleep(0.1)
    
    console.print("\r✨ Ready!     ")
    time.sleep(0.5)
    
    # Show main splash
    show_splash_screen()
```

### Colorful Border Box
```python
def create_fancy_box(content: str, title: str = "") -> Panel:
    """Create a fancy box with gradient-like border."""
    return Panel(
        Align.center(Text(content)),
        title=f"[bold magenta]╔═ {title} ═╗[/bold magenta]",
        border_style="bright_cyan",
        padding=(1, 3),
        subtitle="[dim cyan]═══════════════[/dim cyan]"
    )
```

### Full Splash Module
```python
"""
splash.py - Splash screen and animations for Retro Todo CLI
"""

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import pyfiglet
import time

console = Console()

# ASCII Art alternatives if pyfiglet fails
FALLBACK_LOGO = """
████████╗ ██████╗ ██████╗  ██████╗ 
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ╚██████╔╝██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝ 
"""

def get_logo() -> str:
    """Get ASCII logo, with fallback."""
    try:
        return pyfiglet.figlet_format("TODO", font="banner3-D")
    except:
        return FALLBACK_LOGO

def show_splash():
    """Main splash screen."""
    console.clear()
    
    logo = get_logo()
    
    content = Text()
    content.append(logo, style="bold cyan")
    content.append("\n")
    content.append("🎮 ", style="")
    content.append("Retro Terminal Task Manager", style="bold magenta")
    content.append(" 🎮", style="")
    content.append("\n\n")
    content.append("─" * 45, style="dim cyan")
    content.append("\n\n")
    content.append("Developer by: ", style="white")
    content.append("maneeshanif", style="bold green underline")
    content.append("\n")
    
    panel = Panel(
        Align.center(content),
        border_style="bright_cyan",
        padding=(1, 4),
        title="[bold yellow]★ WELCOME ★[/bold yellow]",
        subtitle="[dim white][ Press ENTER to continue ][/dim white]"
    )
    
    # Animate border colors (simple version)
    console.print(panel)
    input()
    console.clear()

def show_goodbye():
    """Goodbye screen."""
    console.clear()
    
    content = Text()
    content.append("\n")
    content.append("👋 Goodbye!", style="bold cyan")
    content.append("\n\n")
    content.append("Thanks for using ", style="white")
    content.append("Retro Todo", style="bold magenta")
    content.append("\n\n")
    content.append("See you next time!", style="dim")
    content.append("\n")
    
    panel = Panel(
        Align.center(content),
        border_style="cyan",
        padding=(1, 4)
    )
    
    console.print(panel)
    time.sleep(1)

if __name__ == "__main__":
    show_splash()
```

## Best Practices

- Always include developer credit in splash
- Have fallback ASCII art if pyfiglet fails
- Keep animations short (1-3 seconds)
- Use transient progress bars for loading
- Clear screen before and after splash
- Handle KeyboardInterrupt gracefully
- Test with different terminal sizes
- Use consistent color theme
