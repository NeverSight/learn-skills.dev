---
name: android-compose-architecture
description: |
  Compose screen architecture for a feature module - the Screen / ScreenContent split, State / Action / Event contract, ViewModel shape, one-time events, overlay vs full-screen loading, navigation routes, and the paged-list ViewModel variant. Use this skill whenever creating a Compose screen or ViewModel, defining screen state, or structuring a feature's presentation layer. Trigger on phrases like "create a screen", "add a ViewModel", "screen state", "MVI", "action", "event", "ScreenContent", "paged list screen", or "NavHost inside a feature".
---

# Skill: Compose Screen Architecture

> Apply **android-working-discipline** (verification, self-attack, final gate) while executing this skill.
> Pair with **android-compose-best-practices** — MVI/UDF rules, ViewModel constraints, state hoisting, and the error-proofing checklist.

## When to use this skill

Whenever creating a new Compose screen inside any feature presentation module.

---

## Architecture overview

Unidirectional data flow:

```
UI Action → ViewModel → State / Event → UI Update
```

Every screen consists of:

- `[FeatureName]Screen` — entry-point composable
- `[FeatureName]ScreenContent` — stateless content composable
- `[FeatureName]ViewModel` — state + action + event handler
- `[FeatureName]State` — UI state
- `[FeatureName]Action` — user intents
- `[FeatureName]Event` — one-time effects

---

## File structure

### Single screen (no sub-screens)

```
screens/
└── [FeatureName]Screen.kt   ← Screen + ScreenContent + Loading + OverlayLoading
viewmodels/
└── [FeatureName]ViewModel.kt
```

### Feature with sub-screens

```
navigation/
└── NavigationRoutes.kt
screens/
├── [FeatureName]Screen.kt
├── [SubFeature]Screen.kt
viewmodels/
└── [FeatureName]ViewModel.kt
```

---

## Screen file: `[FeatureName]Screen.kt`

```kotlin
package com.example.feature.[featurename].presentation.screens

import android.widget.Toast
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import kotlinx.coroutines.flow.collectLatest

@Composable
fun [FeatureName]Screen(
    viewModel: [FeatureName]ViewModel = viewModel(),   // your DI framework's Compose accessor
    onBackClick: () -> Unit,
    // add other navigation callbacks as needed
) {
    val state by viewModel.state.collectAsStateWithLifecycle()
    val context = LocalContext.current

    LaunchedEffect(Unit) {
        viewModel.event.collectLatest { event ->
            when (event) {
                is [FeatureName]Event.ShowToast ->
                    Toast.makeText(context, event.message, Toast.LENGTH_SHORT).show()
                [FeatureName]Event.NavigateBack -> onBackClick()
            }
        }
    }

    Scaffold(
        topBar = { /* the project's shared app bar */ }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            when (state.screenState) {
                is [FeatureName]State.ScreenState.Loading -> LoadingScreen()
                is [FeatureName]State.ScreenState.Success ->
                    [FeatureName]ScreenContent(
                        state = state,
                        onAction = viewModel::onAction
                    )
            }

            if (state.showOverlayLoader) OverlayLoading()
        }
    }
}

@Composable
private fun [FeatureName]ScreenContent(
    state: [FeatureName]State,
    onAction: ([FeatureName]Action) -> Unit
) {
    // Main UI content here
}

@Composable
private fun LoadingScreen() {
    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        CircularProgressIndicator()
    }
}

@Composable
private fun OverlayLoading() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .clickable(enabled = false) {},   // swallows taps while work is in flight
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator()
    }
}
```

---

## ViewModel file: `[FeatureName]ViewModel.kt`

```kotlin
package com.example.feature.[featurename].presentation

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.receiveAsFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class [FeatureName]ViewModel : ViewModel() {

    private val _state = MutableStateFlow([FeatureName]State())
    val state = _state.asStateFlow()

    private val _event = Channel<[FeatureName]Event>(Channel.BUFFERED)
    val event = _event.receiveAsFlow()

    fun onAction(action: [FeatureName]Action) {
        when (action) {
            is [FeatureName]Action.OnBackClick -> sendEvent([FeatureName]Event.NavigateBack)
            // handle other actions here
        }
    }

    private fun sendEvent(event: [FeatureName]Event) {
        viewModelScope.launch { _event.send(event) }
    }
}

// ─── State ───────────────────────────────────────────────────────────────────

data class [FeatureName]State(
    val screenState: ScreenState = ScreenState.Loading,
    val showOverlayLoader: Boolean = false,
    // add feature-specific fields here
) {
    sealed interface ScreenState {
        data object Loading : ScreenState
        data object Success : ScreenState
    }
}

// ─── Action ──────────────────────────────────────────────────────────────────

sealed interface [FeatureName]Action {
    data object OnBackClick : [FeatureName]Action
}

// ─── Event ───────────────────────────────────────────────────────────────────

sealed interface [FeatureName]Event {
    data object NavigateBack : [FeatureName]Event
    data class ShowToast(val message: String) : [FeatureName]Event
}
```

---

## Navigation routes (only when the feature has sub-screens)

### `navigation/NavigationRoutes.kt`

```kotlin
package com.example.feature.[featurename].presentation.navigation

sealed class NavigationRoutes(val route: String) {
    data object [FeatureName] : NavigationRoutes("[featurename]")
    // add sub-screen routes here
}
```

### Fragment with `NavHost` (when sub-screens exist)

```kotlin
NavHost(
    navController = navController,
    startDestination = NavigationRoutes.[FeatureName].route
) {
    composable(route = NavigationRoutes.[FeatureName].route) {
        [FeatureName]Screen(onBackClick = { findNavController().popBackStack() })
    }
}
```

---

## Paged-list ViewModel variant

When the screen is a paged list, expose the paging stream **alongside** the usual `state`/`event` —
it is not part of `state`:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class [Feature]ViewModel(private val repository: [Feature]Repository) : ViewModel() {

    private val _state = MutableStateFlow([Feature]State())
    val state = _state.asStateFlow()
    private val _event = Channel<[Feature]Event>(Channel.BUFFERED)
    val event = _event.receiveAsFlow()

    // All query inputs (search / category / filters / sort) in ONE params object.
    private val _params = MutableStateFlow([Feature]Params())
    val items: Flow<PagingData<[Domain]>> = _params
        .flatMapLatest { repository.get[Feature]Stream(it) }
        .cachedIn(viewModelScope)

    // An action that changes the query updates _params, rebuilding the pager from page 0:
    // _params.update { it.copy(query = q) }
}
```

- The list collects `items` with `collectAsLazyPagingItems()`; `state` still drives the app bar,
  chips, sheets, overlay loader, and the empty/no-access branches.
- One-time navigation/toasts/downloads stay in `Event`s, consumed by the host Fragment. **The Screen
  itself does not navigate.**

---

## Key rules

- **Data access** — the ViewModel injects the feature repository **interface** and calls it directly.
  The repository implementation lives in the feature's `data` module, injects the shared API
  interface, and returns `Flow<Resource<Domain>>` via the shared network wrapper.
- **State** — `MutableStateFlow`, always updated via `_state.update { }`.
- **Events** — `Channel(Channel.BUFFERED)` + `receiveAsFlow()`. A `Channel` guarantees exactly-once
  delivery to a single collector, which is what a navigation or toast event needs. (If you prefer
  `SharedFlow`, give it `extraBufferCapacity = 1` — see **android-coroutines-flow** §6. Pick one and be
  consistent.)
- **Actions** — all user intents go through `onAction(action)`. Never expose separate ViewModel
  functions per UI interaction.
- **ScreenContent** — fully stateless: receives `state`, emits `action`. No business logic inside.
- **OverlayLoading** — use when a background action runs while the screen already has content (form
  submit, delete). Do not replace the whole screen with a spinner.
- **ScreenState** — a sealed interface. If your product rule is "errors are toasts", keep
  `Loading`/`Success` only and emit `ShowToast` + `NavigateBack`; otherwise add `Error`. Be
  consistent across features either way.
- **ViewModel file** — keep `State`, `Action` and `Event` in the same file as the ViewModel so the
  whole contract for a screen is one file.
- **Navigation routes** — only create `NavigationRoutes.kt` if the feature has more than one screen.

---

## What NOT to do

- Do NOT use `isLoading` / `isError` / `isSuccess` booleans — use a sealed `ScreenState`. Booleans
  allow impossible combinations (`isLoading && isError`); a sealed type does not.
- Do NOT put business logic inside `ScreenContent`.
- Do NOT expose multiple public functions on the ViewModel for UI actions — use `onAction`.
- Do NOT collect events with `collect` — use `collectLatest`.
- Do NOT create `NavigationRoutes` for single-screen features.
- Do NOT let the Screen composable navigate directly; it raises a callback and the host decides.
