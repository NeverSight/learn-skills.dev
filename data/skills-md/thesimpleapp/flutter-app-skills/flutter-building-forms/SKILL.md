---
name: flutter-building-forms
description: >
  Build Flutter forms with Form, TextFormField, DropdownMenuFormField, and
  custom FormField. Covers validation, AutovalidateMode, forceErrorText,
  theme-driven InputDecoration, autofillHints, keyboards, and focus traversal
  on Flutter 3.47+. Use when adding or fixing a login, signup, checkout, or
  any validate/save form; when fields jump, lose text, skip autofill, or ignore
  FormState.validate(); or when the user runs /flutter-building-forms.
license: MIT
metadata:
  version: 1.0.0
  openclaw:
    requires:
      bins: ["flutter", "dart"]
---

# Flutter building forms

Ship forms with `Form` / `FormField` on Flutter 3.47+. Do not add GetX, `flutter_form_builder`, or Expo/RN form patterns. If this repo already has a Form wrapper, shared validators, `ThemeData.inputDecorationTheme`, or an `AutofillGroup` around auth, **extend those**. If widgets already read a house `ThemeExtension` or `*Pressable`, style fields from that system — do not drop a stock Material decoration theme onto a branded surface.

Scroll the form with the project's existing `ListView` / `CustomScrollView`. A bare `Column` under the keyboard will overflow.

## References

```
references/
  recipes.md   Login/signup autofill, server errors, custom FormField, lazy lists
```

## Hard rules

1. Own `final GlobalKey<FormState> _formKey` on a `State`. Never allocate that key, a `FocusNode`, or a `TextEditingController` inside `build`. Submit path: `if (_formKey.currentState!.validate()) { _formKey.currentState!.save(); … }`. After a failed submit, `validateGranularly()` then `FocusNode.requestFocus()` on the first invalid field in **visual** order (`Set` is unordered).
2. Inside a `Form`, every value that must validate or save is a `TextFormField`, `DropdownMenuFormField`, or custom `FormField<T>` — never a bare `TextField`.
3. `validator` is `FormFieldValidator<T>?` and returns `String?` (`null` = valid). Keep it cheap and synchronous. Put API/server failures in `forceErrorText`.
4. Default `autovalidateMode` is `AutovalidateMode.disabled`. After first submit prefer `onUserInteraction` or `onUnfocus`. Do not use `always` on required-empty fields. There is no `AutovalidateMode.onFocusChange`. Also available: `onUserInteractionIfError`.
5. Style via `ThemeData.inputDecorationTheme` (`InputDecorationThemeData`). Per-field `InputDecoration` sets only `labelText` / `hintText` / `helperText` / `prefixIcon`.
6. Set `keyboardType` and `textInputAction` on every field (`next` until the last, then `done` / `go` / `send` + `onFieldSubmitted`).
7. Set `autofillHints: const [AutofillHints.…]`. Login: `username` + `password`. Signup: `newUsername` + `newPassword`. Also `email`, `oneTimeCode`. Wrap the group in `AutofillGroup`. On successful submit call `TextInput.finishAutofillContext(shouldSave: true)` once — after the last step of a multi-step form.
8. Create controllers and `FocusNode`s once on `State`; `dispose()` them. In a lazy `ListView` / `CustomScrollView`, the controller must be owned by a stateful ancestor.
9. Reserve helper/error space (`helperText: ' '` or a fixed-height parent) so showing `errorText` does not reflow the form.
10. New dropdowns in a Form: `DropdownMenuFormField`. If you still touch `DropdownButtonFormField`, pass `initialValue`, not deprecated `value`.
11. `autofocus` the first field. Wrap the form in `FocusTraversalGroup`. Use `OrderedTraversalPolicy` + `NumericFocusOrder` only when visual order ≠ reading order.
12. Interactive fields get `const ValueKey<String>('kebab-name')`.

## Own the Form

```dart
class _SignInState extends State<SignInPage> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  late final FocusNode _emailFocus = FocusNode();
  late final TextEditingController _email = TextEditingController();
  AutovalidateMode _auto = AutovalidateMode.disabled;

  @override
  void dispose() {
    _emailFocus.dispose();
    _email.dispose();
    super.dispose();
  }

  void _submit() {
    final Set<FormFieldState<Object?>> invalid =
        _formKey.currentState!.validateGranularly();
    if (invalid.isNotEmpty) {
      setState(() => _auto = AutovalidateMode.onUserInteraction);
      _emailFocus.requestFocus(); // first invalid field in visual order
      return;
    }
    _formKey.currentState!.save();
    TextInput.finishAutofillContext(shouldSave: true);
  }
}
```

Nested widgets can call `Form.of(context)` (asserts if missing) or `Form.maybeOf` instead of threading the key. [Validate a form](https://docs.flutter.dev/cookbook/forms/validation).

`validate()` runs every descendant `validator`, rebuilds to show errors, and returns `false` if any fail. `save()` only invokes `onSaved` — it does not validate. Call `save()` after a successful `validate()` if you use `onSaved`. `reset()` restores each field to `FormField.initialValue`. `validateGranularly()` returns the `Set` of invalid `FormFieldState`s. [FormState.validate](https://api.flutter.dev/flutter/widgets/FormState/validate.html).

## Fields

`TextFormField` is a `FormField<String>` wrapping `TextField`. A `Form` ancestor is optional; without one, pass `GlobalKey<FormFieldState>` and call `validate` / `save` / `reset` on that state. Use `TextField` only when the editor must **not** participate in `FormState`. If you pass a `TextEditingController`, its `.text` is the field's `initialValue`. `FormField.initialValue` applies on first build and again on `reset()`. [TextFormField](https://api.flutter.dev/flutter/material/TextFormField-class.html).

Dropdown that must `validate` / `save` / `reset`:

```dart
DropdownMenuFormField<String>(
  key: const ValueKey<String>('country-field'),
  dropdownMenuEntries: const <DropdownMenuEntry<String>>[
    DropdownMenuEntry<String>(value: 'us', label: 'United States'),
  ],
  validator: (String? v) => v == null ? 'Pick a country' : null,
  onSaved: (String? v) { /* store */ },
)
```

Seed the selection with `initialSelection` (maps to `FormField.initialValue`). Raw `DropdownMenu` is not a `FormField`. [DropdownMenuFormField](https://api.flutter.dev/flutter/material/DropdownMenuFormField-class.html).

Custom checkbox groups, sliders, chip pickers: a `FormField<T>` whose `builder` reads `FormFieldState` and calls `state.didChange(newValue)`. [FormField](https://api.flutter.dev/flutter/widgets/FormField-class.html).

## Validation

```dart
TextFormField(
  validator: (String? v) {
    if (v == null || v.isEmpty) return 'Required';
    return null;
  },
  forceErrorText: serverEmailError, // null resumes validator
  autovalidateMode: AutovalidateMode.onUserInteractionIfError,
  decoration: const InputDecoration(
    labelText: 'Email',
    helperText: ' ',
  ),
)
```

`forceErrorText` writes `FormFieldState.errorText` without running `validator`. While it is non-null, `validator` is not called and it overrides `InputDecoration.errorText`. Clear it to resume local validation. [forceErrorText](https://api.flutter.dev/flutter/widgets/FormField/forceErrorText.html).

Use `autovalidateMode`, never the removed `autovalidate` bool. [AutovalidateMode](https://api.flutter.dev/flutter/widgets/AutovalidateMode.html):

| Value | Runs |
| --- | --- |
| `disabled` | Only `validate` / `validateGranularly` (Form/FormField default) |
| `always` | First build and every change (empty required fields scream on paint) |
| `onUserInteraction` | After the field's content changes |
| `onUnfocus` | After the field loses focus |
| `onUserInteractionIfError` | On each change only once the field already has an error |

When `errorText` is non-null the helper is hidden and the field can grow. Reserve space with `helperText: ' '` or a fixed-height parent.

## Keyboard, action, autofill

Match iOS hints to keyboards: `AutofillHints.email` + `TextInputType.emailAddress`, `AutofillHints.name` + `TextInputType.name`. [TextInputType](https://api.flutter.dev/flutter/services/TextInputType-class.html).

`TextInputAction.next` moves focus to the next focusable in the same `FocusScope`. Intermediate fields: `next`. Last field: `done` (or `go` / `search` / `send`) and handle submit in `onFieldSubmitted`. Do not use `previous` or `none` on iOS. [TextInputAction](https://api.flutter.dev/flutter/services/TextInputAction.html).

Pass `autofillHints: const [AutofillHints.email]` — not ad-hoc strings unless you branch on `defaultTargetPlatform`. Do not pass `null` (opts the field out on Android/web). iOS and web use only the first hint; Android uses the whole list.

Wrap one login / signup / checkout group in `AutofillGroup`. Clients must be **built** together — a never-laid-out `ListView` child is not registered. Call `TextInput.finishAutofillContext(shouldSave: true)` on successful submit, once per screen, after the last step. [AutofillGroup](https://api.flutter.dev/flutter/widgets/AutofillGroup-class.html).

## Focus

Create the `FocusNode` in `initState` or as a late field initialized once. `autofocus: true` on the first field. After failed validation, `myFocusNode.requestFocus()` — do not call `FocusScope.of(context).requestFocus(focusNode)`. [Focus cookbook](https://docs.flutter.dev/cookbook/forms/focus).

Default tab/reading order is `ReadingOrderTraversalPolicy`. Wrap the form in `FocusTraversalGroup`. When visual order ≠ traversal order:

```dart
FocusTraversalGroup(
  policy: OrderedTraversalPolicy(),
  child: FocusTraversalOrder(
    order: const NumericFocusOrder(1),
    child: emailField,
  ),
)
```

Mixing incomparable `FocusOrder` types in one group asserts. [Focus](https://docs.flutter.dev/ui/interactivity/focus).

## Theme

```dart
ThemeData(
  inputDecorationTheme: const InputDecorationThemeData(
    filled: true,
    border: OutlineInputBorder(),
    contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    floatingLabelBehavior: FloatingLabelBehavior.auto,
    errorMaxLines: 2,
  ),
)
```

`InputDecoration.applyDefaults` fills only null decoration fields from this theme.

## Do not

- Allocate `GlobalKey<FormState>`, `FocusNode`, or `TextEditingController` inside `build`.
- Put a bare `TextField` under `Form` and expect `FormState.validate()` to see it.
- Use deprecated `autovalidate: true`, invent `AutovalidateMode.onFocusChange`, or set `always` so empty required fields error on first paint.
- Drive errors only via `InputDecoration.errorText` while also using a `validator`.
- Omit `autofillHints`, set them to `null`, or use `AutofillHints.password` on a create-account field (`newPassword`).
- Pass `DropdownButtonFormField.value` instead of `initialValue`, or use raw `DropdownMenu` when the form must `validate()` the selection.
- Drop `TextFormField`s into a lazy `ListView` without a long-lived ancestor-owned `controller`.
- Copy-paste full `InputDecoration` borders/colors/padding on every field.
- Skip `dispose()` on controllers/focus nodes, or skip `TextInput.finishAutofillContext` after a successful credential submit.
- Let error text appear with no reserved helper line.

## Verify

1. `grep` for `TextField(` under a `Form`, `autovalidate:`, `AutovalidateMode.always`, `autofillHints: null`, `DropdownButtonFormField` + `value:`, and any `GlobalKey` / `FocusNode` / `TextEditingController(` created inside `build`.
2. Every validating field is a `FormField`. Every login/signup cluster sits in one `AutofillGroup` whose children are built together.
3. `dart analyze` / `flutter analyze` clean. Exercise empty, invalid, server-error, and keyboard-open states.
