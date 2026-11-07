---
name: clear-appui
description: Build, migrate, or review Flutter product interfaces using the Clear AppUI component library. Resolve the installed package, reuse its real App* and Foss* APIs, and apply Apple HIG principles through shared themes, layouts, and presentation hosts.
---

# Clear AppUI

Use the installed Clear AppUI library to compose the requested interface.
The repository is `ycy-0510/clear-appui`; its Dart package identifier is `fossui`.
Product imports use `package:fossui/app_ui.dart`; lower-level components use
`package:fossui/fossui.dart`. Preserve the project's behavior, data, and local
instructions when migrating an existing application.

## Resolve the implementation first

Run `node <this-skill>/scripts/doctor.mjs <flutter-project>` after dependency
resolution. It locates the actual package through `.dart_tool/package_config.json`,
checks the API contract, and prints the matching source paths, design guide and Git revision.
If dependencies are missing, install the Git dependency shown in
[the integration reference](references/integration.md), then run the doctor again.

Read the returned entrypoint and the constructors for the components needed by
the task. Parameter names, enum values, controllers, and behavior must come from
those installed files or their examples. Check existing components before writing
a replacement. Read `lib/src/components/` when an App* wrapper does not exist.

The package carries its matching skill. If `skillMatchesPackage` is false, read
the `bundledSkill` reported by the doctor before editing UI. A different API
contract is an error: use the package's bundled skill rather than guessing.

## Compose with the library

- For migrations, map the maintained app's destinations, settings entry points,
  search modes and scroll boundaries before composing screens. Preserve that
  information architecture; adopting the library does not authorize a redesign.
- Put `AppTheme` below the application's shell. Read semantic values from
  `context.appTheme.tokens`; use `dimensions`, `motion`, and `sheet` for product
  overrides. AppTheme adapts FossTheme; keep this single token source.
- When migrating a branded app, inspect its maintained palette, logos, functional
  icons, launcher icons and launch screen first. Map those colors once with
  `AppThemeData.light/dark.copyWith(tokens: base.tokens.retheme(FossThemeSpec(...)))`;
  retain the package's typography, spacing and controls. Brand color is an
  emphasis role, not permission to tint the canvas, text, cards, fields and every
  secondary surface. Preserve neutral library surfaces unless the user explicitly
  requests branded backgrounds; scope overrides to primary/on-primary/focus roles.
  The blue presets are
  fallbacks, not a replacement for the host brand. Reuse original artwork and
  synchronize Cupertino/Material shell colors with the same semantic tokens.
- Use AppButton, AppText, AppCard, AppTextField, AppBadge, AppCheckbox,
  AppSwitch and AppListTile where they fit. Use existing Foss* variants for
  lower-level selection, dialogs, menus, progress, or feedback.
  A callback that opens a sheet/route should return immediately; handle its
  eventual result in an unawaited continuation. Await actual saving/network work
  so button loading describes work rather than a user's open dialog. Capture
  the Navigator before a mutation that can remove the initiating widget.
  Use AppCard.onTap for an actionable summary card; it shares button feedback
  without adding a second content inset. Nested footer buttons keep their own
  action. Preserve original page wording and section/action order when migrating.
- Read the package's `doc/app_ui/DESIGN_STYLE.md` before styling. Shared design
  changes belong in the package and this skill, followed by upgrading consumers;
  do not fork typography, spacing or navigation materials inside each app.
- Use AppTopBar for top navigation: Back/Close has one floating leading surface;
  all trailing actions share one floating capsule. Keep titles in page content,
  retain the library's grouped capsule surfaces. AppScaffold owns the top backdrop:
  transparent at rest, progressively frosted when page content scrolls behind it.
  Do not implement per-screen blur or a separate tile for every trailing icon.
- Use AppScaffold and AppNavigationBar for product page chrome. Preserve the
  scaffold's MediaQuery top/bottom padding as leading/trailing scroll content;
  obtain these insets from a context inside the scaffold body. Default ListView
  padding consumes them; explicit padding and slivers must retain them. Do not shrink the viewport above floating navigation or
  use bottom SafeArea to cut off scrolling content. Put scrolling headers,
  search/filter controls and lazy results in one CustomScrollView when the
  original page scrolls as a unit; use SliverToBoxAdapter and AppSliverListGroup.
  Compact iOS navigation sits near the physical bottom edge with the theme's
  8-point default margin; do not add another bottom SafeArea around it. The
  scaffold reserves scroll clearance from the actual bar height and gap. Keep
  the capsule and its inset selection surface concentric; verify Home indicator
  clearance and edge taps on the phone rather than guessing screen corner radii.
- Wrap a scrolling title/brandmark in AppCollapsingTitle(collapsed: compact,
  child: expanded). The nearest AppScaffold/AppTopBar measures when it passes
  behind top chrome and reveals a compact copy continuously. Use original host
  artwork for both sizes. Do not add a per-page scroll threshold, opacity timer
  or replacement app bar. Retained inactive destinations must not publish a title;
  verify scrolling back, tab changes, large text and Reduce Motion.
- Use AppNavigationBody to retain destination state during a crossfade. The
  bar has one persistent sliding selection surface. Destinations retain brief
  press-scale feedback for quick taps and keyboard activation without painting a
  second selected-looking fill. Floating control groups animate size changes.
  Keep callbacks immediate and support rapid reversal.
  Keep the content's press compression visible: product buttons default to 0.95,
  navigation content to 0.88 with a short return spring. The navigation surface
  itself keeps sliding independently. Do not remove press feedback while styling
  selected backgrounds; preserve cancellation and Reduce Motion.
- Use AppListGroup for small groups and AppSliverListGroup for long ones, with
  AppListTile rows. Only the outer group edges are rounded; inner rows share
  the surface with dividers and no per-row corner cutouts. Interactive trailing
  controls keep an independent accessibility action; do not merge a remove/switch
  control into the row's open action. A white canvas must
  retain the library's subtle gray group/card fill: AppCard and list groups
  derive it from FossUI secondary-over-card tokens. Removing brand tint must
  not remove this grouping contrast. For segmented search
  modes, reuse FossTabs and its existing sliding indicator.
  AppCheckbox inside either list group receives the shared row insets. Do not
  place raw, edge-flush checkbox controls against the rounded group boundary or
  add a second page-specific inset around AppCheckbox.
- Put AppPresentationHost inside the relevant route. Present sheets through
  showAppSheet; connect the supplied ScrollController to the sheet body. Share
  that host's drag coordinator across page and sheet. For deferred incoming
  work, observe the current host's presentationCountListenable and wait until
  it reaches zero; exiting sheets remain counted until their animation finishes.
  Queue follow-up presentation after the frame, respect the route/account
  lifecycle and unsubscribe before the host is disposed. Do not poll for an
  empty sheet stack or replace a user's active editor. When dismissal must first
  persist a draft, pass onBeforeDismiss to showAppSheet; return false to retain
  the editor after a failure. Non-null explicit results bypass that guard.
  Backgrounding/route disposal still cancels immediately, so retain unfinished
  work independently and account-check any continuation. The host owns animated
  entry/exit and waits for exit before completing results. Keep the gesture subtree
  mounted when material changes; toggling a blur parent can cancel the first drag.
  Verify the first continuous pull from full height through translucent detents.
  Read the implementation
  before adding nested presentations or drag behaviors.
- Prefer AppAdaptiveLayout, AppAdaptiveGrid and AppConstrainedContent for
  constrained layouts. Base adaptation on available space.
- Use AppFormBody for short scrollable sheet forms, passing the sheet's supplied
  controller. It owns 16-point content insets, sibling gaps and bottom safe
  clearance; the sheet already handles keyboard resizing. Use AppFormLayout in
  an existing padded/sliver container. Fields, error messages and action buttons
  are separate children; keep an AppListGroup as one child so its rows stay
  contiguous. Do not add manual SizedBox gaps or another keyboard inset inside
  these form layouts. Check field-to-action and action-to-action spacing in
  normal, error and large-text states; control padding alone does not separate
  siblings.
- Keep feedback purposeful. FossToaster owns toast queues: only the front shows
  content; rear surfaces are previews of queued messages. Use an inline error
  when the user needs to resolve a form problem.

## Apply interface guidance

Consult the installed `doc/app_ui/APPLE_HIG_NOTES.md` for implemented decisions
and the official sources linked there. Use HIG for hierarchy, readable content,
safe areas, keyboard access, touch targets, motion and accessibility. Product
token values are configurable choices, not Apple-prescribed metrics.

Use the package's compact product type scale (15 body, 17 title, 20 heading,
22 display) and 16-point content/card insets. These are product defaults, not HIG
mandates. Preserve system text scaling; keep intentionally enlarged preview
cases separate and label them. Avoid double padding from nested cards and rows.
Maintain consistent spacing and concentric shapes. Avoid rebuilding the library's
navigation, sheet material or gesture handling in individual screens. The Flutter
sheet is an approximation of Apple's materials; verify platform-specific behavior
on the actual target when needed.

Apply HIG as interaction guidance, not an iOS skin. Preserve FossUI's themed
surfaces, depth and brief press feedback. Moving or resizing an existing object
should interpolate from its current visual state, not replace it with unrelated
flashing surfaces. Respect Reduce Motion and do not delay actions until an
animation ends. Test intermediate frames and interrupted transitions, not only
the final settled state.

## Verify the requested behavior

Use interactive Widget Preview with injected sample repositories and no native
side effects. Verify narrow/wide layouts, light/dark, larger text, error/retry,
cancellation, keyboard/focus and the interactions changed by the task. Follow
the host project's CPU, SDK, simulator and release rules. Record device-only
checks as pending until they have actually run.

Read [integration.md](references/integration.md) for dependency, API-location and
preview commands. The skill provides instructions and source inspection; the
project separately installs the Dart dependency.
