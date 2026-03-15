---
name: vim-motions
description: Vim keybindings, motions, text objects, and operators for efficient text editing. Use when user asks about "vim commands", "vim motions", "text objects", "vim keybindings", "vim cheat sheet", "learn vim", "vim in VS Code", or any Vim editing tasks.
---

# Vim Motions

Motions, operators, text objects for efficient editing.

## Modes

```
Normal    ESC or Ctrl-[    Navigate and manipulate
Insert    i, a, o, etc.    Type text
Visual    v, V, Ctrl-v     Select text
Command   :                Execute commands
```

## Basic Motions

### Character/Line

```
h j k l       Left, Down, Up, Right
0             Start of line
^             First non-blank character
$             End of line
g_            Last non-blank character
```

### Word

```
w             Next word start
W             Next WORD start (space-delimited)
b             Previous word start
B             Previous WORD start
e             Next word end
E             Next WORD end
ge            Previous word end
```

### Line Navigation

```
gg            First line
G             Last line
5G            Go to line 5
:42           Go to line 42
H             Top of screen
M             Middle of screen
L             Bottom of screen
```

### Search

```
f{char}       Find char forward (on line)
F{char}       Find char backward
t{char}       Till char forward (before char)
T{char}       Till char backward
;             Repeat last f/F/t/T
,             Repeat last f/F/t/T (reverse)
/{pattern}    Search forward
?{pattern}    Search backward
n             Next match
N             Previous match
*             Search word under cursor
#             Search word under cursor (backward)
```

### Scrolling

```
Ctrl-d        Scroll half page down
Ctrl-u        Scroll half page up
Ctrl-f        Scroll full page down
Ctrl-b        Scroll full page up
zz            Center current line
zt            Current line to top
zb            Current line to bottom
```

## Operators

```
d             Delete
c             Change (delete + insert mode)
y             Yank (copy)
>             Indent right
<             Indent left
=             Auto-indent
gu            Lowercase
gU            Uppercase
g~            Toggle case
```

### Operator + Motion = Action

```
dw            Delete word
d$            Delete to end of line
d0            Delete to start of line
dG            Delete to end of file
dgg           Delete to start of file
d3j           Delete 3 lines down

cw            Change word
ci"           Change inside quotes
ca)           Change around parentheses

yy            Yank (copy) line
yw            Yank word
y$            Yank to end of line

>>            Indent line
3>>           Indent 3 lines
```

## Text Objects

```
i = inner (inside)
a = around (including delimiters)

iw / aw       Word
iW / aW       WORD
is / as       Sentence
ip / ap       Paragraph
i" / a"       Double quotes
i' / a'       Single quotes
i` / a`       Backticks
i( / a(       Parentheses
i[ / a[       Brackets
i{ / a{       Braces
i< / a<       Angle brackets
it / at       HTML/XML tag
```

### Common Text Object Actions

```
diw           Delete inner word
ciw           Change inner word
yi"           Yank inside quotes
da"           Delete around quotes (including quotes)
ci(           Change inside parentheses
dit           Delete inside HTML tag
vit           Select inside HTML tag
yap           Yank around paragraph
>ip           Indent paragraph
```

## Insert Mode Entry

```
i             Insert before cursor
I             Insert at line start
a             Append after cursor
A             Append at line end
o             Open line below
O             Open line above
s             Delete char and insert
S             Delete line and insert
C             Delete to end of line and insert
```

## Visual Mode

```
v             Character-wise visual
V             Line-wise visual
Ctrl-v        Block (column) visual

# In visual mode:
o             Jump to other end of selection
gv            Reselect last selection

# Visual block operations
Ctrl-v → select → I → type → ESC    Insert in all lines
Ctrl-v → select → A → type → ESC    Append to all lines
Ctrl-v → select → c → type → ESC    Change all lines
Ctrl-v → select → d                  Delete column
```

## Editing Commands

```
x             Delete character
X             Delete character before
dd            Delete line
D             Delete to end of line
cc            Change line
C             Change to end of line
J             Join lines
u             Undo
Ctrl-r        Redo
.             Repeat last command
~             Toggle case of character
```

## Registers

```
"ay           Yank into register 'a'
"ap           Paste from register 'a'
"+y           Yank to system clipboard
"+p           Paste from system clipboard
"0p           Paste last yank (not delete)
:registers    Show all registers
```

## Macros

```
qa            Start recording macro 'a'
q             Stop recording
@a            Play macro 'a'
@@            Replay last macro
5@a           Play macro 'a' 5 times
```

## Marks

```
ma            Set mark 'a'
'a            Jump to mark 'a' (line)
`a            Jump to mark 'a' (exact position)
''            Jump to last position
`.            Jump to last edit
```

## Essential Commands

```
:w            Save
:q            Quit
:wq           Save and quit
:q!           Quit without saving
:e file       Open file
:%s/old/new/g Replace all in file
:s/old/new/g  Replace all in line
:noh          Clear search highlight
```

## Reference

For quick reference card: `references/cheatsheet.md`
