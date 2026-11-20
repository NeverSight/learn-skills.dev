---
description: "Use when adding or auditing direct touch support in a macOS app (e.g. an iPad through Sidecar) alongside mouse and trackpad. That includes anything that behaves differently with touch than with a mouse, such as taps, hover, long-press menus, drags, scrolling, pinch and text selection, and bug fixes in existing event handlers. Replaces mouse-only handling (mouseDown/mouseDragged/mouseUp overrides, tracking loops, event monitors) with gesture recognizers, and resolves recognizer conflicts, click counting, hit targets, popover dismissal. Primarily covering AppKit, with SwiftUI and Mac Catalyst sections."
name: macos-touch-gestures
---
# macOS Touch Gestures Skill

## Read This First

Before editing any file, read the whole reference file for the active task from start to finish. Each reference starts with a Detection patterns section, and the patterns assume it. When a site matches more than one task, read each matching reference before the first edit.

## When to Use

Use this skill whenever the request is about any of the following, whether or not it names an API:

- Making a Mac app work with direct touch, including a touch display connected through Sidecar.
- Adopting `NSGestureRecognizer` in place of `mouseDown:`, `mouseDragged:`, `mouseUp:` overrides or `nextEvent(matching:)` loops.
- Taps, scrolling, long presses, drags, pinch, rotate, context menus, drag and drop, hover-revealed controls, popovers or outside-click dismissal that misbehave with touch.
- Gesture recognizers that block each other, never fire, or fire twice.

## Scope

Targeted changes in Swift and Objective-C AppKit code. Examples are in Swift; the Detection lists give Objective-C spellings (for example `shouldReceiveTouch:` for `gestureRecognizer(_:shouldReceive:)`).

SwiftUI and Mac Catalyst (UIKit) sections inside the task files apply only in files already in that framework. Do not convert AppKit code to SwiftUI or UIKit or mix their patterns into AppKit classes; when a framework has no equivalent for a pattern, leave the code in place and do not invent an API.

Apps built on other toolkits or engines (Electron, Qt, Java, game engines, custom Metal views) are outside this skill, except for AppKit views they host and for general design guidance that is not specific to AppKit, such as enlarging the hit area instead of changing how a view is drawn.

## Core Principles

1. **Choose the migration path before replacing mouse handling.** Keep the responder methods and add touch-only recognizers (the choice for an app that back-deploys before macOS 27 and for a framework), use one recognizer for mouse and touch, or use separate ones when they differ. Agree on the path with the user first (`references/recognizers-task.md`, "Choose the migration path").
2. **Keep mouse behavior unchanged.** Larger hit areas, longer press durations and wider movement tolerances belong to touch only. Keep the mouse values as they were.
3. **Leave framework-provided controls alone.** Framework-provided AppKit controls (`NSButton`, `NSSegmentedControl`, `NSSlider`, `NSStepper`, `NSTextField`), table, outline and collection views, scroll views, split views, text views and popovers handle touch themselves. Avoid adding recognizers to them. Change custom views and code that interferes with the framework behavior, such as a `mouseDown:` override on a subclass of a view that handles touch itself. Replace mouse-method overrides on a control subclass (`mouseDown:` and the like): prefer moving the behavior into the control's action or tracking callbacks, and add a recognizer only when there is no other option, for example when you must back-deploy (Principle 1). No question is needed when the behavior is preserved.
4. **Ask before changing selection, focus, click-count or drag behavior.** If a change could alter any of these, or removes a mouse override other code relies on, ask the user first.
5. **Keep each view's drawn size as it is when enlarging it for touch.** The only exception is a transient expansion on interaction, such as a taller menu or an expandable control.
6. **Decide touch-specific behavior from the recognizer or event you are handling.** Touch can happen at the same time as keyboard or mouse input, and a touch recognizer can complete before the emulated mouse events arrive, so a flag set from one event path is stale by the time another path reads it.

**Public API only.** Never recommend or emit non-public or underscore-prefixed symbols, private headers, undocumented defaults, runtime tricks that match framework internals, or symbols that are no longer public in the current SDK. If a capability needs non-public API, file feedback to Apple with details about the use case, and offer to help construct a representative sample.

## How AppKit Routes Touch

- Framework-provided AppKit views use their own touch recognizers. When a view's class overrides legacy mouse methods (`mouseDown:`, `mouseDragged:`, `mouseUp:`), AppKit routes a touch on that view through mouse emulation instead. The view still responds to touch through mouse emulation, but the response is degraded: the view is not handled natively as touch and lacks framework touch behavior such as touch text selection and the touch handling of tables and controls. Removing even an empty override can change routing, so test after any removal.
- For each touch, AppKit gathers recognizers from the hit-tested view and all its superviews, so a new recognizer competes with those on its view, its ancestors and any descendant the touch lands on, not with siblings or unrelated views.
- On macOS 27, a gesture recognizer created in code accepts direct touch by default. Set `allowedTouchTypes` explicitly on every recognizer you create, and set it to `[]` on a recognizer meant only for the mouse.

### Mouse emulation

Mouse emulation is AppKit turning a direct touch into synthesized mouse events, so mouse code runs for touch.

- It applies when a view's class (or its view controller) overrides `mouseDown:`, `mouseDragged:` or `mouseUp:`, even with an empty override, and the view has no gesture recognizer of its own that accepts direct touch. Right-mouse, menu, magnify and rotate overrides add long-press, pinch and rotate emulation the same way.
- A tap arrives as mouse-down and mouse-up after the finger lifts. A drag inside a scroll view needs a short hold first. A long press becomes a context menu or Control-click.
- Emulated events arrive after the touch's recognizers have finished (Principle 6).
- A recognizer that accepts direct touch, added to the view itself, turns off that view's tap and drag emulation, so its `mouseDown:` stops running for touch.
- Scroll-wheel overrides do not trigger emulation, and `NSScrollView` touch scrolling bypasses `scrollWheel(_:)` (`references/scroll-and-drag-task.md`, Pattern 8).
- A view with mouse overrides already responds to touch through emulation: tap, double-tap and long-press reach it. That is a working baseline, not a defect. Recognizers improve it with feedback at touch-down, press and drag start tuned for a finger, multi-finger input and defined relationships with scrolling. When the request is only "make it work with touch" and the view already behaves correctly, say so and propose the migration instead of making it unasked.
- When the developer reports a symptom on a specific view with mouse overrides (a task that lists symptoms counts), emulation is not delivering it: look for a view stacked in front, an `allowedTouchTypes` that excludes direct touch, or mouse state that depends on hover or event order, and fix that cause or give the view recognizers.

## Workflow

Match each site to a task by the signals in the Task Registry; if the request names a file or a pattern, work only on that. Tasks are listed in the order to apply them: input-kind rules first, then mouse-tracking migration, then the rest. Before adding a recognizer, check the recognizers gathered with it and decide failure and simultaneity explicitly: read `references/recognizer-relationships-task.md`.

Touch behavior cannot be checked without a touch device. Ask the developer to run these on a Mac with a touch display (Sidecar is enough), and say which were not run:

| Check | Input |
|-------|-------|
| Tap, double tap | touch, mouse, trackpad |
| Press and hold, then release | touch, mouse |
| Hold then drag | touch, mouse |
| Swipe or scroll over the view | touch, trackpad two-finger |
| Context menu | touch long press, secondary click, control-click |
| Pinch and rotate | touch, trackpad |
| Hover-revealed controls | touch, mouse |
| Dismiss a popover or menu by clicking outside | touch, mouse |
| Cancel mid-gesture (second finger, window deactivation, Escape) | touch |

## Task Registry

Paths are relative to this skill.

| Task | Read when you see | Reference |
|------|-------------------|-----------|
| Input kinds | A new `NSClickGestureRecognizer`, `NSPressGestureRecognizer` or `NSPanGestureRecognizer` without `allowedTouchTypes` or `buttonMask`; `shouldAttemptToRecognizeWith` without `shouldReceive`; "isTouch" or "touchActive" flags; `NSApp.currentEvent` or `window.currentEvent` read anywhere; the pan start point; SwiftUI `onTapGesture` or `DragGesture` that must differ for pointer and touch; SwiftUI `Button` with no pressed feedback; Catalyst recognizers with default touch types | [references/input-kinds-task.md](references/input-kinds-task.md) |
| Replace mouse tracking | `mouseDown:`, `mouseDragged:`, `mouseUp:`, `rightMouseDown:` (the menu part belongs to Context menus), `trackMouse:`, `trackKnob:`, `nextEvent(matching:)` loops, `sendAction(on:)` click-and-hold, highlight-on-press controls | [references/recognizers-task.md](references/recognizers-task.md) |
| Click counting | `clickCount`, `doubleAction`, click-to-rename, single and double click recognizers on one view, a container double-click with a clickable child | [references/click-counting-task.md](references/click-counting-task.md) |
| Text selection | An `NSTextView` subclass with mouse overrides, `NSTextInputClient` with a custom caret or selection, `clickedOnLink`, `NSTextSelectionManager` | [references/text-selection-task.md](references/text-selection-task.md) |
| Scrolling versus pressing and dragging | Controls or drags inside scroll views (a swipe scrolls rows or starts a drag), `numberOfTouchesRequired` on a pan, `minimumNumberOfTouchesForScrolling`, `scrollWheel:` momentum timers, nested scrollers, page swipes, a window that moves while the user scrolls | [references/scroll-and-drag-task.md](references/scroll-and-drag-task.md) |
| Recognizer relationships | Two or more recognizers on a view or its ancestors; `requireGestureRecognizerToFail` (UIKit files only; AppKit uses the delegate methods), `shouldRequireFailureOf`, `shouldRecognizeSimultaneouslyWith`, `delaysPrimaryMouseButtonEvents`, `exclusiveGestureBehavior`; SwiftUI `.simultaneousGesture`, `.highPriorityGesture`, `exclusively(before:)`, `sequenced(before:)`; a recognizer that never fires; a stuck press or lost touch | [references/recognizer-relationships-task.md](references/recognizer-relationships-task.md) |
| Pan, pinch and rotate | Pan, pinch and rotate on one canvas, `NSMagnificationGestureRecognizer`, `NSRotationGestureRecognizer`, `MagnifyGesture`, deprecated `MagnificationGesture` and `RotationGesture`, three- or four-finger gestures, `disablesDirectTouchSystemGestures` | [references/multitouch-task.md](references/multitouch-task.md) |
| Context menus | `menu(for:)`, `menuForEvent:`, `clickedRow` or `selectedRow` in a menu action, `popUpContextMenu`, a pop-up menu opened from `sendAction(on:)`, control-click menus that stop opening | [references/context-menus-task.md](references/context-menus-task.md) |
| Drag sources | `writeRowsWith`, `pasteboardWriterForRow`, `beginDraggingSession`, drag image or lift code, SwiftUI `.draggable` and `.onDrag`, Catalyst `UIDragInteraction` | [references/drag-sources-task.md](references/drag-sources-task.md) |
| Hit testing and target size | `hitTest(_:)`, `point(inside:with:)`, small hit rects, tiny dividers or disclosure controls, a transparent overlay in front of interactive content, SwiftUI `.contentShape` or clear tap areas | [references/hit-testing-task.md](references/hit-testing-task.md) |
| Hover-only UI | `NSTrackingArea` with `mouseEntered:` and `mouseExited:`, `mouseMoved:` that arms state, `onHover` that gates a button, Catalyst `UIHoverGestureRecognizer` | [references/hover-task.md](references/hover-task.md) |
| Outside-tap dismissal | `addLocalMonitorForEvents`, `addGlobalMonitorForEvents`, popovers, `UIPopoverPresentationController`, custom picker windows, SwiftUI overlays dismissed by an outside tap | [references/dismissal-task.md](references/dismissal-task.md) |