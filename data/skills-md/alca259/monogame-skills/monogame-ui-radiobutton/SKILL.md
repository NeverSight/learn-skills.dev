---
name: monogame-ui-radiobutton
description: MonoGame UI RadioButton and RadioGroup controls — mutually exclusive option selectors where selecting one button deselects all others in the same group. Use this skill whenever the user asks about radio buttons, mutually exclusive options, option groups, "only one can be selected", "how do I make only one choice selectable at a time" in MonoGame UI, or any grouped selection control.
---

# MonoGame UI RadioButton

RadioButtons provide mutually exclusive selection within a named group. Selecting any button in a group automatically deselects all others. For complete code templates, read `references/ui-radiobutton.md`.

## Assumed Contract

Extends `UIElement` from `monogame-ui-core`. Receives pointer events from `monogame-ui-interaction`. Participates in focus via `monogame-ui-focus` — arrow keys navigate between options in the same group.

## RadioGroup

`RadioGroup` is the source of truth for selection — it is not a visual element. It:
- Holds a list of `RadioButton` instances belonging to it
- Tracks `SelectedButton` (the currently checked one)
- Provides `Select(button)` which deselects all others and selects the given one
- Fires `SelectionChanged(RadioGroup, RadioButton)`

**Registration:** Pass the group to the button's constructor — buttons register themselves automatically. Never manage selection state inside individual buttons — always delegate to the group.

```csharp
var group = new RadioGroup();

var optA = new RadioButton(font, pixel, "Option A", group);
var optB = new RadioButton(font, pixel, "Option B", group);
var optC = new RadioButton(font, pixel, "Option C", group);

group.SelectionChanged += (g, btn) => ApplyOption(btn.Label);

// Pre-select option A:
group.Select(optA);
```

## RadioButton Anatomy

```
(●) Option A label     ← checked state (filled circle)
( ) Option B label     ← unchecked state (empty circle)
```

Visual: two textures (`_emptyCircle`, `_filledCircle`) drawn at the left of the element, followed by the label text to the right. Or draw circles procedurally using a pixel texture (not recommended for quality — use pre-made sprites).

## Keyboard Navigation Within a Group

When a `RadioButton` is focused, Up/Down arrows should move focus to the adjacent button **and immediately select it** (standard radio button behavior):

```csharp
public override void HandleKeyboardInput(UIKeyboardEventArgs args)
{
    if (args.Key == Keys.Down || args.Key == Keys.Right)
    {
        var next = _group.NextAfter(this);
        if (next != null) { _group.Select(next); UIFocusManager.SetFocus(next); }
        args.Handled = true;
    }
    if (args.Key == Keys.Up || args.Key == Keys.Left)
    {
        var prev = _group.PrevBefore(this);
        if (prev != null) { _group.Select(prev); UIFocusManager.SetFocus(prev); }
        args.Handled = true;
    }
    if (args.Key == Keys.Space || args.Key == Keys.Enter)
    {
        _group.Select(this);
        args.Handled = true;
    }
}
```

## TabIndex Within a Group

Only the **selected** radio button (or the first if none are selected) should be in `UIFocusManager.TabOrder`. Tabbing into the group lands on the selected option; arrow keys then move within the group. When tabbing out, focus moves to the next focusable element outside the group.

Implement by:
- Registering only the selected button with `UIFocusManager` at any given time
- On `SelectionChanged`, unregister old selected button, register new one

## Measure/Arrange

`RadioButton.Measure`:
- `DesiredSize.X` = `circleSize + spacing + labelWidth`
- `DesiredSize.Y` = `max(circleSize, fontLineSpacing)`

Lay multiple radio buttons out using a `StackPanel` (vertical) from `monogame-ui-layout`.

## Anti-Patterns

- Never manage mutual exclusion inside individual buttons — always delegate to `RadioGroup.Select()`.
- Never put radio buttons from different groups in the same `RadioGroup`.
- Do not allow a radio button to be deselected by clicking it again (standard UX: clicking a selected radio button does nothing).
- Never bind keyboard Up/Down to `UIFocusManager.MoveFocus` for radio buttons — use the group's `NextAfter`/`PrevBefore` instead to keep selection in sync with focus.

## Reference

Complete `RadioGroup`, `RadioButton`, and tab-integration patterns: `references/ui-radiobutton.md`.
