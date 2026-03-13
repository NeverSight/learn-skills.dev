---
name: ue-ui-umg-slate
description: "Use this skill when working with UMG, UI, widget, UserWidget, Slate, HUD, BindWidget, Common UI, menu, or UMG binding in Unreal Engine. See references/widget-types.md for widget type reference and references/common-ui-setup.md for Common UI plugin setup. For Slate in editor tools, see ue-editor-tools. For input mode management, see ue-input-system."
metadata:
  version: 1.0.0
---

# UE UI: UMG, Slate, and Common UI

You are an expert in Unreal Engine's UI systems (UMG, Slate, and Common UI).

## Context Check

Read `.agents/ue-project-context.md` to determine: which UI plugins are enabled (CommonUI, MVVM), target platforms (affects input method), whether this is multiplayer (widget ownership per player), and existing UI base class conventions.

## Information Gathering

Before writing UI code, confirm: UI type (HUD, full-screen menu, modal, in-world WidgetComponent), input requirements (mouse, gamepad, keyboard), target platforms, and widget lifecycle (persistent, transient, or pooled).

---

## 1. UUserWidget in C++

```cpp
// MyWidget.h
UCLASS()
class MYGAME_API UMyWidget : public UUserWidget
{
    GENERATED_BODY()
protected:
    virtual void NativeConstruct() override; // Bind delegates here — BindWidget refs valid
    virtual void NativeDestruct() override;
    virtual void NativeTick(const FGeometry& MyGeometry, float InDeltaTime) override;
};

// MyWidget.cpp
void UMyWidget::NativeConstruct()
{
    Super::NativeConstruct();
    if (PlayButton)
        PlayButton->OnClicked.AddDynamic(this, &UMyWidget::HandlePlayClicked);
}
```

### Lifecycle and GC

```cpp
// Creation — always pass the owning PlayerController for player-UI
UMyWidget* Widget = CreateWidget<UMyWidget>(GetOwningPlayer(), MyWidgetClass);
Widget->AddToViewport(0);          // ZOrder: higher = on top. Roots the widget (won't GC).
Widget->AddToPlayerScreen(0);      // Split-screen: ties to a specific player's viewport region
Widget->RemoveFromParent();        // Un-roots — may be GC'd if no UPROPERTY holds it.

UPROPERTY() TObjectPtr<UMyWidget> CachedWidget; // Strong ref keeps alive after RemoveFromParent

// Visibility
Widget->SetVisibility(ESlateVisibility::Collapsed); // Not drawn, takes no space
Widget->SetVisibility(ESlateVisibility::Hidden);    // Not drawn, takes space
Widget->SetVisibility(ESlateVisibility::Visible);   // Drawn, receives input
// HitTestInvisible: drawn, passes input through; SelfHitTestInvisible: children receive input
```

---

## 2. BindWidget Pattern

```cpp
UCLASS()
class MYGAME_API UMyWidget : public UUserWidget
{
    GENERATED_BODY()
protected:
    UPROPERTY(meta=(BindWidget))             // Required — compiler warning if absent in UMG BP
    TObjectPtr<UButton> PlayButton;

    UPROPERTY(meta=(BindWidgetOptional))     // Optional — always null-check before use
    TObjectPtr<UTextBlock> SubtitleText;

    UPROPERTY(meta=(BindWidgetAnim), Transient) // Transient is required for anim bindings
    TObjectPtr<UWidgetAnimation> IntroAnim;

    UPROPERTY(meta=(BindWidget)) TObjectPtr<UTextBlock> ScoreText;
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UImage> PlayerAvatar;
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UProgressBar> HealthBar;
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UListView> ItemList;
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UScrollBox> ContentScroll; // Scrollable container
};
```

Name must match the UMG Blueprint widget name exactly (case-sensitive). Always null-check optional bindings.

---

## 3. Widget Interaction

### UButton (Button.h)

```cpp
// Delegates: OnClicked, OnPressed, OnReleased, OnHovered, OnUnhovered
PlayButton->OnClicked.AddDynamic(this, &UMyWidget::HandlePlayClicked);
PlayButton->OnHovered.AddDynamic(this, &UMyWidget::HandlePlayHovered);
PlayButton->SetColorAndOpacity(FLinearColor(1.f, 0.8f, 0.f, 1.f));
PlayButton->SetIsEnabled(false);
// UE5.2+: WidgetStyle, ColorAndOpacity, ClickMethod direct access deprecated — use setters
```

### UTextBlock (TextBlock.h)

```cpp
// SetText wipes any Blueprint binding on Text
ScoreText->SetText(FText::Format(NSLOCTEXT("HUD", "ScoreFmt", "Score: {0}"), FText::AsNumber(Score)));
ScoreText->SetColorAndOpacity(FSlateColor(FLinearColor::White));
ScoreText->SetTextTransformPolicy(ETextTransformPolicy::ToUpper);
ScoreText->SetTextOverflowPolicy(ETextOverflowPolicy::Ellipsis);
```

### UImage (Image.h)

```cpp
PlayerAvatar->SetBrushFromTexture(AvatarTexture, /*bMatchSize=*/false);
PlayerAvatar->SetBrushFromMaterial(IconMaterial);
UMaterialInstanceDynamic* MID = PlayerAvatar->GetDynamicMaterial();
MID->SetScalarParameterValue(TEXT("Opacity"), 0.5f);
PlayerAvatar->SetBrushFromSoftTexture(SoftTextureRef, false); // Async stream
PlayerAvatar->SetColorAndOpacity(FLinearColor(1.f, 1.f, 1.f, 0.5f));
```

### UProgressBar (ProgressBar.h)

```cpp
HealthBar->SetPercent(CurrentHealth / MaxHealth); // 0.0–1.0
HealthBar->SetFillColorAndOpacity(FLinearColor(0.f, 1.f, 0.f, 1.f));
LoadingBar->SetIsMarquee(true); // Indeterminate animation
```

### UScrollBox (ScrollBox.h)

`UScrollBox` is a BindWidget-compatible container for scrollable content. Supports vertical and horizontal scroll. Add child widgets in Blueprint; query or modify scroll offset in C++:

```cpp
ContentScroll->ScrollToEnd();
ContentScroll->SetScrollOffset(0.f);
ContentScroll->SetOrientation(Orient_Vertical); // default
```

### UListView + UTileView + IUserObjectListEntry (ListView.h, TileView.h, IUserObjectListEntry.h)

`UListView` — virtualised vertical list. `UTileView` — same interface, displays items in a grid layout (set tile width/height in the widget Designer panel). Both use `IUserObjectListEntry`.

```cpp
// Entry widget must implement the interface
UCLASS()
class UItemEntryWidget : public UUserWidget, public IUserObjectListEntry
{
    GENERATED_BODY()
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UTextBlock> NameText;
protected:
    virtual void NativeOnListItemObjectSet(UObject* ListItemObject) override
    {
        IUserObjectListEntry::NativeOnListItemObjectSet(ListItemObject);
        if (UItemData* Data = Cast<UItemData>(ListItemObject))
            NameText->SetText(FText::FromString(Data->ItemName));
    }
};

// Populate
ItemList->ClearListItems();
for (const FItemInfo& Info : Items)
{
    UItemData* Data = NewObject<UItemData>(this);
    Data->ItemName = Info.Name;
    ItemList->AddItem(Data);
}
// Selection — NOTE: BP_OnItemClicked is Blueprint-only and private.
// For C++: override NativeOnItemClicked in a UListView subclass, or bind
// OnItemClickedInternal (protected delegate on UListViewBase).
UItemData* Selected = ItemList->GetSelectedItem<UItemData>();
```

---

## 4. Input Mode Management

```cpp
// UI-only — full-screen menus. Game input blocked.
FInputModeUIOnly UIMode;
UIMode.SetWidgetToFocus(Widget->TakeWidget());
GetOwningPlayer()->SetInputMode(UIMode);
GetOwningPlayer()->SetShowMouseCursor(true);

// Game-only — restore gameplay.
GetOwningPlayer()->SetInputMode(FInputModeGameOnly());
GetOwningPlayer()->SetShowMouseCursor(false);

// Game and UI — HUD tooltips, keeps game input active.
FInputModeGameAndUI GameUIMode;
GameUIMode.SetLockMouseToViewportBehavior(EMouseLockMode::LockOnCapture);
GetOwningPlayer()->SetInputMode(GameUIMode);
GetOwningPlayer()->SetShowMouseCursor(true);
```

Set input mode from calling code (HUD/GameMode) after `AddToViewport`, not from `NativeConstruct`.

---

## 5. Common UI (Plugin)

See `references/common-ui-setup.md` for full plugin setup, GameViewportClient config, and layer architecture. Enable `CommonUI` and `CommonInput` plugins. Set viewport client to `UCommonGameViewportClient` in Project Settings > Maps & Modes > Game Viewport Client Class. `UCommonGameViewportClient` detects input method changes (gamepad vs mouse vs touch) and broadcasts them via `UCommonInputSubsystem` — this drives automatic gamepad/keyboard navigation and button prompt switching.

### UCommonActivatableWidget (CommonActivatableWidget.h)

```cpp
UCLASS()
class MYGAME_API UMyMenuScreen : public UCommonActivatableWidget
{
    GENERATED_BODY()
protected:
    virtual void NativeOnActivated() override;
    virtual void NativeOnDeactivated() override;
    virtual UWidget* NativeGetDesiredFocusTarget() const override { return CloseButton; }
    virtual TOptional<FUIInputConfig> GetDesiredInputConfig() const override
    {
        return FUIInputConfig(ECommonInputMode::Menu, EMouseCaptureMode::NoCapture);
    }
    UPROPERTY(meta=(BindWidget)) TObjectPtr<UCommonButtonBase> CloseButton;
};

void UMyMenuScreen::NativeOnActivated()
{
    Super::NativeOnActivated(); // Always call Super
    CloseButton->OnClicked().AddUObject(this, &UMyMenuScreen::DeactivateWidget);
}
void UMyMenuScreen::NativeOnDeactivated()
{
    CloseButton->OnClicked().RemoveAll(this);
    Super::NativeOnDeactivated(); // Always call Super
}
```

### Widget Containers (CommonActivatableWidgetContainerBase.h)

`UCommonActivatableWidgetContainerBase` is the base class for Common UI widget containers. Two concrete subclasses:

- **`UCommonActivatableWidgetStack`** — shows only the topmost widget; deactivating reveals the previous one (stack behaviour). This is the correct stack class — do NOT use `UCommonActivatableWidgetSwitcher` here, which inherits from `UCommonAnimatedSwitcher`/`UWidgetSwitcher` and is a different widget entirely.
- **`UCommonActivatableWidgetQueue`** — FIFO queue; displays widgets sequentially, advancing to the next when the current deactivates.

```cpp
UPROPERTY(meta=(BindWidget)) TObjectPtr<UCommonActivatableWidgetStack> MenuLayer;
UPROPERTY(meta=(BindWidget)) TObjectPtr<UCommonActivatableWidgetQueue> NotificationQueue;

// Push screen onto the stack — AddWidget creates the widget internally
UMyMenuScreen* Screen = Cast<UMyMenuScreen>(MenuLayer->AddWidget(UMyMenuScreen::StaticClass()));
Screen->ActivateWidget();

// Go back — deactivate re-activates the previous widget in the stack
Screen->DeactivateWidget();

// Queue a notification — plays after the current one finishes
NotificationQueue->AddWidget(UMyNotificationWidget::StaticClass());
```

### UCommonButtonBase

Uses `FCommonButtonEvent` (declared via `DECLARE_EVENT`) — use `AddUObject`, not `AddDynamic`:
```cpp
MyButton->OnClicked().AddUObject(this, &UMyScreen::HandleClick);
MyButton->OnClicked().RemoveAll(this); // In NativeOnDeactivated
```

### UCommonUIActionRouter

Handles input routing between game and UI layers; Common UI drives it automatically via `GetDesiredInputConfig`. Access directly when you need to query the current input mode:

```cpp
#include "Input/CommonUIActionRouterBase.h"
// Get() takes a const UWidget& — call from within a widget (or pass any valid UWidget in scope):
UCommonUIActionRouterBase* Router = UCommonUIActionRouterBase::Get(*ContextWidget); // ContextWidget: const UWidget&
if (Router) { /* query active input config */ }
```

### Gamepad / Keyboard Navigation

Common UI provides automatic gamepad and keyboard navigation without extra setup. Key behaviours:

- `UCommonButtonBase` highlights automatically when it receives focus via D-pad or Tab navigation.
- `UCommonActivatableWidget::NativeGetDesiredFocusTarget()` controls which widget receives focus when the screen activates.
- When a widget deactivates, Common UI restores focus to the widget that was active before it opened — no manual focus bookkeeping required.
- Bind `GetDesiredInputConfig` to `ECommonInputMode::Menu` to suppress game input while a menu is open.

---

## 6. Slate Fundamentals

Use Slate for editor extensions, custom renderers, or when UMG doesn't expose required functionality.

`SWidget` is the abstract base of all Slate widgets. `SCompoundWidget` (shown below) is the typical subclass for custom widgets.

```cpp
// Custom widget — SMyWidget.h
class SMyWidget : public SCompoundWidget
{
public:
    SLATE_BEGIN_ARGS(SMyWidget)
        : _LabelText(FText::GetEmpty()), _OnClicked() {}
        SLATE_ATTRIBUTE(FText, LabelText)
        SLATE_EVENT(FSimpleDelegate, OnClicked)
    SLATE_END_ARGS()

    void Construct(const FArguments& InArgs);
private:
    TAttribute<FText> LabelText;
    FSimpleDelegate OnClicked;
};

// SMyWidget.cpp
void SMyWidget::Construct(const FArguments& InArgs)
{
    LabelText = InArgs._LabelText;
    OnClicked = InArgs._OnClicked;
    ChildSlot
    [
        SNew(SButton)
        .OnClicked_Lambda([this]() -> FReply { OnClicked.ExecuteIfBound(); return FReply::Handled(); })
        [ SNew(STextBlock).Text(LabelText) ]
    ];
}

// Instantiation
TSharedRef<SMyWidget> W = SNew(SMyWidget).LabelText(NSLOCTEXT("UI", "Btn", "Go"));
TSharedPtr<SButton> Btn;
SAssignNew(Btn, SButton).OnClicked(FOnClicked::CreateUObject(this, &UMyClass::Handle));
```

**Common Slate widgets:** `STextBlock`, `SButton`, `SVerticalBox`, `SHorizontalBox`, `SOverlay`, `SBorder`, `SBox`, `SScrollBox`, `SImage`, `SEditableTextBox`.

**Slate vs UMG:** Use Slate for editor tools and maximum control. Use UMG for game runtime UI, Blueprint extensibility, animations, and BindWidget.

---

## 7. MVVM (UE 5.1+, ModelViewViewModel plugin)

```cpp
// ViewModel — MyGameViewModel.h
UCLASS()
class MYGAME_API UMyGameViewModel : public UMVVMViewModelBase
{
    GENERATED_BODY()
public:
    // UE_MVVM_SET_PROPERTY_VALUE: checks equality, sets, broadcasts field change
    void SetScore(int32 NewScore) { UE_MVVM_SET_PROPERTY_VALUE(Score, NewScore); }
    void SetPlayerName(FText NewName) { UE_MVVM_SET_PROPERTY_VALUE(PlayerName, NewName); }
    int32 GetScore() const { return Score; }
    FText GetPlayerName() const { return PlayerName; }
private:
    UPROPERTY(BlueprintReadOnly, FieldNotify, Getter, meta=(AllowPrivateAccess))
    int32 Score = 0;
    UPROPERTY(BlueprintReadOnly, FieldNotify, Getter, meta=(AllowPrivateAccess))
    FText PlayerName;
};

// From game code — UI updates automatically via field notifications:
void AMyPlayerState::OnScoreChanged(int32 NewScore) { ViewModel->SetScore(NewScore); }
```

To bind a ViewModel at runtime: create with `NewObject<UMyGameViewModel>(this)`, then configure in the widget Blueprint's Bindings panel. The `UMVVMView` component on the widget handles one-way and two-way property bindings automatically once the ViewModel class is set.

---

## Common Mistakes

| Anti-pattern | Correct approach |
|---|---|
| `SetVisibility(Hidden)` to "hide" a menu | `RemoveFromParent()` to stop rendering and input |
| `CreateWidget(GetWorld(), ...)` for HUD widgets | `CreateWidget(GetOwningPlayer(), ...)` |
| `SetInputMode(FInputModeUIOnly())` for a HUD | Use `FInputModeGameAndUI` or Common UI's `GetDesiredInputConfig` |
| `AddDynamic` with `UCommonButtonBase::OnClicked()` | `AddUObject` — it's `FCommonButtonEvent` not DYNAMIC |
| Binding delegates in `NativeTick` | Bind once in `NativeConstruct`, unbind in `NativeDestruct` |
| Skipping `Super::NativeOnActivated/Deactivated` | Always call Super — it routes focus and input |
| One widget for all players in split-screen | `AddToPlayerScreen` with per-player widgets |
| No UPROPERTY reference after `RemoveFromParent` (widget leak) | Hold a `UPROPERTY() TObjectPtr<>` to prevent GC, or call `RemoveFromParent()` to allow GC when no longer needed |
| Z-order conflicts | Multiple widgets at same Z-order causes undefined draw order | Use explicit Z-order in `AddToViewport(ZOrder)` — higher values draw on top. Reserve ranges: HUD 0-9, menus 10-19, popups 20+ |
| Invisible widgets still tick | Hidden widgets with `NativeTick` consume CPU | Set `SetVisibility(ESlateVisibility::Collapsed)` (removes from layout) or call `RemoveFromParent()` for unused widgets. Override `NativeTick` with an early-out: `if (!IsVisible()) return;` |

---

## Build.cs

```csharp
PublicDependencyModuleNames.AddRange(new string[] { "UMG", "Slate", "SlateCore" });
PrivateDependencyModuleNames.Add("CommonUI");      // If using CommonUI
PrivateDependencyModuleNames.Add("CommonInput");   // If using CommonInput
PrivateDependencyModuleNames.Add("ModelViewViewModel"); // If using MVVM
```

---

## Related Skills

- `ue-cpp-foundations` — UPROPERTY meta specifiers, TObjectPtr, module setup
- `ue-input-system` — Enhanced Input, FInputModeXxx, input contexts
- `ue-editor-tools` — Slate for editor detail panels and custom tools
