---
name: ue-editor-tools
description: "Use when extending the Unreal Editor with editor tool, editor utility widget, Blutility, detail customization, property customization, editor mode, asset editor, editor subsystem, editor extension, UToolMenus, or scripted asset operations. For Slate fundamentals, see ue-ui-umg-slate. For module build config, see ue-module-build-system."
metadata:
  version: 1.0.0
---

# UE Editor Tools

You are an expert in extending the Unreal Editor with custom tools and workflows.

## Context

Read `.agents/ue-project-context.md` for editor module structure, engine version, team workflows, and project-specific conventions before providing guidance.

## Before You Start

Ask which area the user needs if not clear:
- **Editor Utility Widget** — UMG panel run from editor right-click
- **Blutility** — UAssetActionUtility or UActorActionUtility scripted actions
- **Detail Customization** — Custom property panel (IDetailCustomization / IPropertyTypeCustomization)
- **Custom Editor Mode** — Viewport mode with specialized interaction (FEdMode)
- **Asset Type Actions** — Content Browser integration for a custom asset type
- **Editor Subsystem** — Editor-lifetime singleton (UEditorSubsystem)
- **Menu / Toolbar Extension** — UToolMenus additions to main menu, toolbars, context menus

---

## Editor Module Setup

All editor-extending code must live in a module with `"Type": "Editor"`. Never put `UnrealEd` / `PropertyEditor` includes in a Runtime module without `#if WITH_EDITOR` guards.

```json
{ "Name": "MyGameEditor", "Type": "Editor", "LoadingPhase": "PostEngineInit" }
```

```csharp
// MyGameEditor.Build.cs — key dependencies
PrivateDependencyModuleNames.AddRange(new string[] {
    "Core", "CoreUObject", "Engine", "UnrealEd",
    "Slate", "SlateCore", "EditorStyle",
    "PropertyEditor",   // IDetailCustomization, IPropertyTypeCustomization
    "EditorSubsystem",  // UEditorSubsystem
    "Blutility",        // UEditorUtilityWidget, UAssetActionUtility
    "ToolMenus",        // UToolMenus
    "AssetTools",       // FAssetTypeActions_Base
    "MyGame"
});
```
Module skeleton — every registration in `StartupModule` must be mirrored in `ShutdownModule`:
```cpp
IMPLEMENT_MODULE(FMyGameEditorModule, MyGameEditor)

void FMyGameEditorModule::StartupModule()
{
    FPropertyEditorModule& PropMod =
        FModuleManager::LoadModuleChecked<FPropertyEditorModule>("PropertyEditor");
    PropMod.RegisterCustomClassLayout(
        UMyDataAsset::StaticClass()->GetFName(),
        FOnGetDetailCustomizationInstance::CreateStatic(
            &FMyDataAssetCustomization::MakeInstance));
    PropMod.NotifyCustomizationModuleChanged();

    UToolMenus::RegisterStartupCallback(
        FSimpleMulticastDelegate::FDelegate::CreateRaw(
            this, &FMyGameEditorModule::RegisterMenus));
}

void FMyGameEditorModule::ShutdownModule()
{
    if (FModuleManager::Get().IsModuleLoaded("PropertyEditor"))
    {
        FModuleManager::GetModuleChecked<FPropertyEditorModule>("PropertyEditor")
            .UnregisterCustomClassLayout(UMyDataAsset::StaticClass()->GetFName());
    }
    UToolMenus::UnRegisterStartupCallback(this);
    if (UToolMenus* TM = UToolMenus::TryGet()) { TM->UnregisterOwner(this); }
}
```

> Full boilerplate with asset type actions, editor modes, and factory: `references/editor-module-setup.md`

---

## Editor Utility Widgets

`UEditorUtilityWidget` (from `EditorUtilityWidget.h`) extends `UUserWidget` for editor-only UMG panels. Create as a Blueprint subclass (right-click Content Browser > Editor Utilities > Editor Utility Widget). **Run**: right-click the widget asset > Run Editor Utility Widget. Or subclass in C++:

```cpp
#pragma once
#include "EditorUtilityWidget.h"
#include "MyEditorUtilityWidget.generated.h"

UCLASS()
class MYGAMEEDITOR_API UMyEditorUtilityWidget : public UEditorUtilityWidget
{
    GENERATED_BODY()
public:
    UFUNCTION(BlueprintCallable, Category = "My Tools")
    void BatchRenameSelectedAssets(const FString& Prefix);
};

// .cpp
void UMyEditorUtilityWidget::BatchRenameSelectedAssets(const FString& Prefix)
{
    for (UObject* Asset : UEditorUtilityLibrary::GetSelectedAssets())
    {
        if (Asset)
        {
            const FString Src = Asset->GetOutermost()->GetName(); // e.g. /Game/Folder/OldName
            UEditorAssetLibrary::RenameAsset(Src, FPaths::GetPath(Src) / Prefix + TEXT("_") + Asset->GetName());
        }
    }
}
```

Key `UEditorUtilityLibrary` functions (from `EditorUtilityLibrary.h`):

| Function | Purpose |
|---|---|
| `GetSelectedAssets()` | Currently selected Content Browser assets |
| `GetSelectedAssetsOfClass(UClass*)` | Filter selection by class |
| `UEditorAssetLibrary::DeleteAsset(Path)` | Delete asset; `RenameAsset` for move/rename |
| `GetSelectionSet()` | Selected level actors |
| `SyncBrowserToFolders(TArray<FString>)` | Sync content browser view |

**Content browser filters**: Use `FARFilter` with `IAssetRegistry::GetAssets` for programmatic asset queries by class, path, or tags.

Open a widget programmatically:

```cpp
GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>()
    ->SpawnAndRegisterTab(LoadObject<UEditorUtilityWidgetBlueprint>(
        nullptr, TEXT("/Game/EditorWidgets/BP_MyTool")));
```

---

## Blutility: Scripted Actions

### UAssetActionUtility — Asset Right-Click Actions

Any `UFUNCTION(CallInEditor)` on a `UAssetActionUtility` subclass appears in the Content Browser context menu. Set `SupportedClasses` in Class Defaults to filter by asset type.

```cpp
#pragma once
#include "AssetActionUtility.h"   // Engine/Source/Editor/Blutility/Classes/AssetActionUtility.h
#include "MyAssetActionUtility.generated.h"

UCLASS()
class MYGAMEEDITOR_API UMyAssetActionUtility : public UAssetActionUtility
{
    GENERATED_BODY()
public:
    UFUNCTION(CallInEditor, Category = "My Tools")
    void SetTextureCompressionToUI()
    {
        for (UObject* Asset : UEditorUtilityLibrary::GetSelectedAssets())
        {
            if (UTexture2D* Tex = Cast<UTexture2D>(Asset))
            {
                Tex->CompressionSettings = TC_EditorIcon;
                Tex->MarkPackageDirty();
                Tex->PostEditChange();
            }
        }
    }
};
```

### UActorActionUtility — Actor Right-Click Actions

Same pattern for level actors. Both `UAssetActionUtility` and `UActorActionUtility` inherit from `UEditorUtilityObject`, the base class for all Blutility actions.

---

## Detail Customizations

### Class Customization — IDetailCustomization

```cpp
class FMyDataAssetCustomization : public IDetailCustomization
{
public:
    static TSharedRef<IDetailCustomization> MakeInstance();
    virtual void CustomizeDetails(IDetailLayoutBuilder& DetailBuilder) override;
    // Override the TSharedPtr overload too — store WeakBuilder for async ForceRefreshDetails
    virtual void CustomizeDetails(const TSharedPtr<IDetailLayoutBuilder>& DetailBuilder) override;
private:
    TWeakPtr<IDetailLayoutBuilder> WeakBuilder;
};
// In CustomizeDetails: EditCategory, AddProperty, AddCustomRow, HideCategory
// Register: PropMod.RegisterCustomClassLayout(UMyClass::StaticClass()->GetFName(), ...MakeInstance)
// Unregister in ShutdownModule: PropMod.UnregisterCustomClassLayout(...)
```

### Struct Customization — IPropertyTypeCustomization

```cpp
class FMyStructCustomization : public IPropertyTypeCustomization
{
public:
    static TSharedRef<IPropertyTypeCustomization> MakeInstance();
    virtual void CustomizeHeader(TSharedRef<IPropertyHandle> Handle,
        FDetailWidgetRow& HeaderRow, IPropertyTypeCustomizationUtils& Utils) override;
    virtual void CustomizeChildren(TSharedRef<IPropertyHandle> Handle,
        IDetailChildrenBuilder& ChildBuilder, IPropertyTypeCustomizationUtils& Utils) override;
};
// Register: PropMod.RegisterCustomPropertyTypeLayout(FMyStruct::StaticStruct()->GetFName(), ...MakeInstance)
```

> Full implementations, Slate row patterns, IPropertyHandle read/write, NameContent/ValueContent: `references/detail-customization-patterns.md`

---

## Custom Editor Modes

`FEdMode` (from `EdMode.h`) provides specialized viewport interaction. Register globally; only one active per viewport at a time.

```cpp
// MyEditorMode.h
class FMyEditorMode : public FEdMode
{
public:
    static const FEditorModeID EM_MyMode;
    FMyEditorMode();
    virtual void Enter() override;
    virtual void Exit() override;
    virtual bool HandleClick(FEditorViewportClient*, HHitProxy*,
        const FViewportClick&) override;
    virtual bool MouseMove(FEditorViewportClient* ViewportClient,
        FViewport* Viewport, int32 X, int32 Y) override;
    // Use View->DeprojectFVector2D (FSceneView) for world-space ray from pixel coords
    virtual void Render(const FSceneView*, FViewport*,
        FPrimitiveDrawInterface*) override;
    virtual bool UsesToolkits() const override { return true; }
};

// MyEditorMode.cpp
const FEditorModeID FMyEditorMode::EM_MyMode = TEXT("EM_MyEditorMode");

FMyEditorMode::FMyEditorMode()
{
    Info = FEditorModeInfo(EM_MyMode,
        FText::FromString("My Editor Mode"), FSlateIcon(), /*bVisible=*/true);
}

void FMyEditorMode::Enter()
{
    FEdMode::Enter();
    if (!Toolkit.IsValid())
    {
        Toolkit = MakeShareable(new FMyEditorModeToolkit);
        Toolkit->Init(Owner->GetToolkitHost());
    }
}

void FMyEditorMode::Exit()
{
    if (Toolkit.IsValid())
        FToolkitManager::Get().CloseToolkit(Toolkit.ToSharedRef());
    FEdMode::Exit();
}

void FMyEditorMode::Render(const FSceneView* View, FViewport* Viewport,
    FPrimitiveDrawInterface* PDI)
{
    FEdMode::Render(View, Viewport, PDI);
    DrawWireSphere(PDI, FVector::ZeroVector, FLinearColor::Green, 50.f, 16, SDPG_World);
}
```

Register/unregister in module lifecycle:

```cpp
// StartupModule
FEditorModeRegistry::Get().RegisterMode<FMyEditorMode>(
    FMyEditorMode::EM_MyMode, FText::FromString("My Mode"), FSlateIcon(), true);
// ShutdownModule
FEditorModeRegistry::Get().UnregisterMode(FMyEditorMode::EM_MyMode);
```

---

## Asset Type Actions

`FAssetTypeActions_Base` (from `AssetTypeActions_Base.h`) controls Content Browser appearance and context menu for custom asset types.

```cpp
class FMyAssetTypeActions : public FAssetTypeActions_Base
{
public:
    virtual FText GetName() const override { return FText::FromString("My Asset"); }
    virtual FColor GetTypeColor() const override { return FColor(200, 100, 50); }
    virtual UClass* GetSupportedClass() const override { return UMyAsset::StaticClass(); }
    virtual uint32 GetCategories() override { return EAssetTypeCategories::Misc; }

    virtual void OpenAssetEditor(const TArray<UObject*>& InObjects,
        TSharedPtr<IToolkitHost> EditWithinLevelEditor) override
    {
        for (UObject* Obj : InObjects)
            if (UMyAsset* Asset = Cast<UMyAsset>(Obj))
                MakeShareable(new FMyAssetEditor)->InitMyEditor(
                    EToolkitMode::Standalone, EditWithinLevelEditor, Asset);
    }
};
```

Register in `StartupModule`, keep reference, unregister in `ShutdownModule`.

### FAssetEditorToolkit — Tab-Based Asset Editor Window

```cpp
class FMyAssetEditor : public FAssetEditorToolkit
{
public:
    void InitMyEditor(EToolkitMode::Type Mode, TSharedPtr<IToolkitHost> Host, UMyAsset* Asset);
    virtual FName GetToolkitFName() const override { return "MyAssetEditor"; }
    virtual FText GetBaseToolkitName() const override { return INVTEXT("My Asset Editor"); }
    virtual void RegisterTabSpawners(const TSharedRef<FTabManager>& TabMgr) override;
    virtual void UnregisterTabSpawners(const TSharedRef<FTabManager>& TabMgr) override;
};
// Call InitAssetEditor() inside InitMyEditor to set up the tab layout via FTabManager::NewLayout
```

Query open editors programmatically via `IAssetEditorInstance`:

```cpp
IAssetEditorInstance* Editor = GEditor->GetEditorSubsystem<UAssetEditorSubsystem>()
    ->FindEditorForAsset(MyAsset, /*bFocusIfOpen=*/false);
if (Editor) Editor->FocusWindow(MyAsset);  // CloseWindow(EAssetEditorCloseReason::AssetEditorHostClosed) — no-arg form deprecated 5.3
```

### Asset Factories

`UFactory` subclasses allow the Content Browser's "Add" menu to create new custom assets:

```cpp
UCLASS()
class UMyDataFactory : public UFactory
{
    GENERATED_BODY()
public:
    UMyDataFactory()
    {
        SupportedClass = UMyDataAsset::StaticClass();
        bCreateNew = true;       // appears in "Add" menu
        bEditAfterNew = true;    // opens editor after creation
    }
    virtual UObject* FactoryCreateNew(UClass* InClass, UObject* InParent,
        FName InName, EObjectFlags Flags, UObject* Context,
        FFeedbackContext* Warn) override
    {
        return NewObject<UMyDataAsset>(InParent, InClass, InName, Flags);
    }
};
```

### Custom Thumbnails

```cpp
UCLASS()
class UMyThumbnailRenderer : public UThumbnailRenderer
{
    GENERATED_BODY()
    virtual void Draw(UObject* Object, int32 X, int32 Y, uint32 Width, uint32 Height,
        FRenderTarget* Target, FCanvas* Canvas, bool bAdditionalViewFamily) override;
};
// Register in module startup:
UThumbnailManager::Get().RegisterCustomRenderer(UMyDataAsset::StaticClass(),
    UMyThumbnailRenderer::StaticClass());
```

---

## Editor Subsystems

`UEditorSubsystem` (from `EditorSubsystem.h`) — editor-lifetime singletons, auto-discovered (no registration needed). Access via `GEditor->GetEditorSubsystem<T>()`.

```cpp
UCLASS()
class MYGAMEEDITOR_API UMyEditorSubsystem : public UEditorSubsystem
{
    GENERATED_BODY()
public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override
    {
        Super::Initialize(Collection);
        FEditorDelegates::PostUndoRedo.AddUObject(this, &UMyEditorSubsystem::OnPostUndoRedo);
    }
    virtual void Deinitialize() override
    {
        FEditorDelegates::PostUndoRedo.RemoveAll(this);
        Super::Deinitialize();
    }
};
```

Built-in subsystems:

| Subsystem | Purpose |
|---|---|
| `UEditorActorSubsystem` | Select, spawn, delete level actors |
| `UEditorAssetSubsystem` | Load, save, duplicate assets |
| `ULevelEditorSubsystem` | Open, save, manage levels |
| `UEditorUtilitySubsystem` | Spawn editor utility widget tabs |

---

## Menu and Toolbar Extensions (UToolMenus)

UToolMenus (UE5+) replaces `FExtender`. Register inside the startup callback so Slate is ready:

```cpp
void FMyGameEditorModule::RegisterMenus()
{
    FToolMenuOwnerScoped OwnerScoped(this);

    // Main menu
    UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
    Menu->FindOrAddSection("MyGame").AddMenuEntry("OpenMyPanel",
        FText::FromString("My Panel"), FText::GetEmpty(),
        FSlateIcon(FAppStyle::GetAppStyleSetName(), "Icons.Settings"),
        FUIAction(FExecuteAction::CreateLambda([]() {
            GEditor->GetEditorSubsystem<UEditorUtilitySubsystem>()
                ->SpawnAndRegisterTab(/* WidgetBP */nullptr);
        })));

    // Toolbar button
    UToolMenu* TB = UToolMenus::Get()->ExtendMenu(
        "LevelEditor.LevelEditorToolBar.PlayToolBar");
    TB->FindOrAddSection("MyTools").AddEntry(
        FToolMenuEntry::InitToolBarButton("MyBtn",
            FUIAction(FExecuteAction::CreateLambda([]() {})),
            FText::FromString("My Tool"), FText::GetEmpty(),
            FSlateIcon(FAppStyle::GetAppStyleSetName(), "Icons.Toolbar.Settings")));
}
```

Always unregister: `UToolMenus::UnRegisterStartupCallback(this)` + `TryGet()->UnregisterOwner(this)`.

### Command Registration — TCommands Pattern

```cpp
class FMyCommands : public TCommands<FMyCommands>
{
public:
    FMyCommands() : TCommands("MyEditor", INVTEXT("My Editor"), NAME_None, FAppStyle::GetAppStyleSetName()) {}
    virtual void RegisterCommands() override;
    TSharedPtr<FUICommandInfo> OpenPanel;
};
void FMyCommands::RegisterCommands()
{
    UI_COMMAND(OpenPanel, "My Panel", "Opens the panel", EUserInterfaceActionType::Button, FInputChord());
}
// In StartupModule: FMyCommands::Register(); bind via CommandList->MapAction(...)
// In ShutdownModule: FMyCommands::Unregister();
```

---

## Data Validation

```cpp
// UEditorValidatorBase — auto-discovered by Editor > Tools > Validate Assets
UCLASS()
class UMyValidator : public UEditorValidatorBase
{
    GENERATED_BODY()
    virtual bool CanValidateAsset_Implementation(const FAssetData& InAssetData, UObject* InObject, FDataValidationContext& InContext) const override
    { return InObject && InObject->IsA<UMyDataAsset>(); }
    virtual EDataValidationResult ValidateLoadedAsset_Implementation(
        const FAssetData& InAssetData, UObject* InAsset, FDataValidationContext& Context) override;
};
// Also runnable via commandlet: UnrealEditor-Cmd -run=DataValidation
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Editor headers in Runtime modules | Move to Editor module; use `#if WITH_EDITOR` for runtime-side editor hooks |
| No `UnregisterCustomClassLayout` in `ShutdownModule` | Always pair register/unregister; crashes Live Coding reload |
| Raw pointer capture in Slate lambdas | Capture as `TWeakPtr`; pin before use |
| `LoadingPhase: Default` for editor extension module | Use `PostEngineInit` for modules registering menus or customizations |
| `UEditorUtilityWidget` referenced from Runtime | Editor-only; will not exist in packaged builds |
| `ForceRefreshDetails()` on every value change | Use only when layout structure changes; use handles/attributes for values |
| `RegisterMode` without `UnregisterMode` | Crashes on plugin reload |

---

## Related Skills

- **ue-ui-umg-slate** — Slate widget fundamentals (SNew, TAttribute, FReply, SBox, SHorizontalBox)
- **ue-module-build-system** — Editor module `.Build.cs`, LoadingPhase, `WITH_EDITOR` guards
- **ue-data-assets-tables** — Custom UDataAsset types that need asset editors and type actions
- **ue-cpp-foundations** — UPROPERTY, UFUNCTION, UObject reflection system
