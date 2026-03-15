---
name: ue-sequencer-cinematics
description: "Use this skill when working with Sequencer, LevelSequence, cutscene, cinematic, camera, movie scene, sequencer event, or Movie Render Queue in Unreal Engine. See references/sequencer-patterns.md for dialogue cutscene, in-game camera, and scripted event patterns. For animation playback, see ue-animation-system."
metadata:
  version: 1.0.0
---

# Skill: ue-sequencer-cinematics

You are an expert in Unreal Engine's Sequencer and cinematic systems.

## Context Check

Read `.agents/ue-project-context.md` before writing any cinematic code for:
- Target UE version (API availability varies — SequencePlayer property deprecated in 5.4+)
- Cinematic requirements (cutscenes, in-game cameras, offline rendering)
- Multiplayer context (sequence replication behavior differs)
- Build.cs modules already declared

## Information Gathering

Ask for:
1. Cinematic type: full-screen cutscene, in-game camera, or background ambient sequence
2. Whether actors bind at runtime or are pre-placed in the level
3. Whether camera control must return to the player after playback
4. One-shot or looping sequence
5. Real-time gameplay or offline Movie Render Queue output

---

## Build.cs Modules

```csharp
PublicDependencyModuleNames.AddRange(new string[]
{
    "LevelSequence", "MovieScene", "CinematicCamera",
});
// Offline rendering only:
PrivateDependencyModuleNames.Add("MovieRenderPipelineCore");
```

---

## Playing Level Sequences

### ALevelSequenceActor — World-Placed

`ALevelSequenceActor` owns the player. Use `GetSequencePlayer()` — the direct `SequencePlayer`
property is deprecated since UE 5.4.

```cpp
// LevelSequenceActor.h: ULevelSequencePlayer* GetSequencePlayer() const;
ULevelSequencePlayer* Player = SeqActor->GetSequencePlayer();
if (Player) { Player->Play(); }
```

### ULevelSequencePlayer::CreateLevelSequencePlayer — Runtime Spawn

```cpp
// LevelSequencePlayer.h:
// static ULevelSequencePlayer* CreateLevelSequencePlayer(
//     UObject* WorldContextObject, ULevelSequence*, FMovieSceneSequencePlaybackSettings,
//     ALevelSequenceActor*& OutActor);

FMovieSceneSequencePlaybackSettings Settings;
Settings.bAutoPlay              = false;
Settings.PlayRate               = 1.0f;
Settings.LoopCount.Value        = 0;       // 0=once, -1=infinite
Settings.bDisableMovementInput  = true;
Settings.bDisableLookAtInput    = true;
Settings.bHidePlayer            = false;
Settings.bHideHud               = false;
Settings.bDisableCameraCuts     = false;
Settings.bPauseAtEnd            = false;
Settings.FinishCompletionStateOverride =
    EMovieSceneCompletionModeOverride::ForceRestoreState; // safe for skippable cutscenes

ALevelSequenceActor* OutActor = nullptr;
ULevelSequencePlayer* Player  = ULevelSequencePlayer::CreateLevelSequencePlayer(
    this, Sequence, Settings, OutActor);

// Store OutActor in a UPROPERTY to prevent GC
ActiveSequenceActor = OutActor;

if (Player)
{
    Player->OnFinished.AddDynamic(this, &AMyClass::OnCutsceneFinished);
    Player->Play();
}
```

### Play Control (UMovieSceneSequencePlayer base)

```cpp
// MovieSceneSequencePlayer.h
Player->Play();
Player->PlayReverse();
Player->PlayLooping(-1);       // -1 = infinite loops
Player->Pause();
Player->Stop();                // moves cursor to end, fires OnStop
Player->StopAtCurrentTime();
Player->GoToEndAndStop();
Player->SetPlayRate(0.5f);     // negative = reverse

// Jump to frame (skips events between current and target)
// Blueprint exposes this as GoToFrame. In C++, use SetPlaybackPosition with Jump.
Player->SetPlaybackPosition(
    FMovieSceneSequencePlaybackParams(FFrameTime(120), EUpdatePositionMethod::Jump));

// Play through to frame (triggers all events along the way)
Player->PlayTo(
    FMovieSceneSequencePlaybackParams(FFrameTime(240), EUpdatePositionMethod::Play),
    FMovieSceneSequencePlayToParams());

// Restrict play range
Player->SetFrameRange(0, 60);           // frames 0–60
Player->SetTimeRange(0.0f, 2.5f);       // seconds

// State query
bool bPlaying = Player->IsPlaying();
FQualifiedFrameTime Now = Player->GetCurrentTime();
FQualifiedFrameTime Dur = Player->GetDuration();

// Delegates (bind before Play)
Player->OnFinished.AddDynamic(this, &UMyClass::OnSeqFinished);
Player->OnPlay.AddDynamic(this, &UMyClass::OnSeqPlay);
Player->OnStop.AddDynamic(this, &UMyClass::OnSeqStop);
Player->OnNativeFinished.BindUObject(this, &UMyClass::OnNativeFinished); // non-dynamic

// Camera cut event (LevelSequencePlayer.h)
// DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnLevelSequencePlayerCameraCutEvent, UCameraComponent*, CameraComponent)
LsPlayer->OnCameraCut.AddDynamic(this, &UMyClass::OnCameraCut);

// Restore state on early stop (skippable cutscene)
Player->SetCompletionModeOverride(EMovieSceneCompletionModeOverride::ForceRestoreState);
Player->Stop();

// Sub-sequence snapshot
FLevelSequencePlayerSnapshot Snap;
Player->TakeFrameSnapshot(Snap);
// Snap.CurrentShotName, Snap.RootTime, Snap.CameraComponent, Snap.ActiveShot
```

---

## Actor Binding

Tag bindings in Sequencer (right-click object binding -> Tags...) then override at runtime.
**Always bind before calling `Play()`.**

### Spawnables vs Possessables

**Possessables** bind to pre-existing world actors (placed in level or spawned by gameplay). **Spawnables** are actors the sequence itself creates and destroys.

```cpp
// Spawnable: sequence owns the actor lifecycle
// Set in Sequencer editor: right-click actor track → "Change to Spawnable"
// At runtime, actor spawns when sequence reaches its range, despawns when exiting

// Dynamic possessable: bind a gameplay-spawned actor to a sequence track
// Create the binding ID in the editor, then override at runtime:
FMovieSceneObjectBindingID BindingID = /* from sequence editor */;
ALevelSequenceActor* SeqActor = /* your sequence actor */;
SeqActor->SetBinding(BindingID, {SpawnedActor});
```

**Why this matters**: Use possessables for persistent world actors (doors, elevators) and spawnables for transient cutscene-only actors (cinematic-only characters, props). Possessables survive sequence end; spawnables are cleaned up automatically.

```cpp
// LevelSequenceActor.h — all binding API lives here

// Replace bound actors (preferred: tag-based, resilient to GUID changes)
SeqActor->SetBindingByTag(FName("Hero"), TArray<AActor*>{ HeroActor },
    /*bAllowBindingsFromAsset=*/ false);

// GUID-based (expose FMovieSceneObjectBindingID via UPROPERTY for editor assignment)
// UPROPERTY(EditAnywhere) FMovieSceneObjectBindingID HeroBindingID;
SeqActor->SetBinding(HeroBindingID, TArray<AActor*>{ HeroActor }, false);

// Append without removing existing bindings
SeqActor->AddBindingByTag(FName("NPC"), NpcActor, /*bAllowBindingsFromAsset=*/ true);

// Remove / reset
SeqActor->RemoveBindingByTag(FName("NPC"), NpcActor);
SeqActor->ResetBinding(HeroBindingID);  // revert to asset binding
SeqActor->ResetBindings();              // revert all overrides

// Lookup by tag
FMovieSceneObjectBindingID ID = SeqActor->FindNamedBinding(FName("Hero"));
const TArray<FMovieSceneObjectBindingID>& All = SeqActor->FindNamedBindings(FName("NPC"));

// Inspect what is currently bound
TArray<UObject*> Bound = Player->GetBoundObjects(HeroBindingID);

// FMovieSceneObjectBindingID (MovieSceneObjectBindingID.h):
//   Access via public accessors — internal fields are private:
//     GetGuid()              — FGuid identifying the binding track
//     GetRelativeSequenceID() — which sub-sequence holds it (0 = local)
```

---

## Camera System

### ACineCameraActor / UCineCameraComponent

```cpp
// CineCameraActor.h: UCineCameraComponent* GetCineCameraComponent() const;
// CineCameraComponent.h / CineCameraSettings.h:
//   FCameraFilmbackSettings Filmback  (SensorWidth, SensorHeight in mm, read-only SensorAspectRatio)
//   FCameraLensSettings LensSettings  (MinFocalLength, MaxFocalLength, MinFStop, MaxFStop mm)
//   FCameraFocusSettings FocusSettings (FocusMethod, ManualFocusDistance cm, bSmoothFocusChanges)
//   float CurrentFocalLength  — Interp, animatable in Sequencer
//   float CurrentAperture     — f-stop, Interp-animatable

ACineCameraActor* Cam = GetWorld()->SpawnActor<ACineCameraActor>(SpawnTransform);
UCineCameraComponent* CC = Cam->GetCineCameraComponent();

FCameraFilmbackSettings FB;
FB.SensorWidth = 36.0f; FB.SensorHeight = 24.0f;  // full-frame 35mm
CC->SetFilmback(FB);

CC->SetCurrentFocalLength(50.0f);   // mm
CC->SetCurrentAperture(2.0f);       // f-stop

FCameraFocusSettings FS;
FS.FocusMethod         = ECameraFocusMethod::Manual;  // Manual | Tracking | Disable | DoNotOverride
FS.ManualFocusDistance = 500.0f;    // cm
FS.bSmoothFocusChanges = true;
CC->SetFocusSettings(FS);

// Lookat tracking (CineCameraActor.h: FCameraLookatTrackingSettings LookatTrackingSettings)
Cam->LookatTrackingSettings.bEnableLookAtTracking     = true;
Cam->LookatTrackingSettings.ActorToTrack              = TargetActor;
Cam->LookatTrackingSettings.LookAtTrackingInterpSpeed = 5.0f;
Cam->LookatTrackingSettings.RelativeOffset            = FVector(0, 0, 90.f);

// Prevent sequence from overriding gameplay camera (set before Play)
SeqActor->PlaybackSettings.bDisableCameraCuts = true;

// Restore player camera after cutscene (call from OnFinished delegate)
APlayerController* PC = GetWorld()->GetFirstPlayerController();
PC->SetViewTargetWithBlend(PC->GetPawn(), 0.5f, VTBlend_Cubic);
PC->SetIgnoreMoveInput(false);
PC->SetIgnoreLookInput(false);
```

### APlayerCameraManager

`APlayerCameraManager` (accessed via `PlayerController->PlayerCameraManager`) manages camera
blending and view target selection for the local player. After a cutscene ends, restore the
gameplay camera explicitly — Sequencer does not do this automatically:

```cpp
APlayerController* PC = GetWorld()->GetFirstPlayerController();
// PlayerCameraManager handles blend state; SetViewTargetWithBlend triggers it.
PC->SetViewTargetWithBlend(PC->GetPawn(), 0.5f, VTBlend_Cubic);
// The blend is processed each tick inside APlayerCameraManager::UpdateCamera.
```

---

## Sequencer Events

Event tracks call `UFUNCTION`s on objects in the event context.
Default event context: `UWorld` + `ALevelScriptActor`.

```cpp
// Function must be UFUNCTION(BlueprintCallable) on a context object
UFUNCTION(BlueprintCallable, Category = "Cinematics")
void TriggerExplosion()
{
    ExplosionSystem->SpawnExplosion(ExplosionLocation);
}

// Trigger C++ code at a specific frame by playing to it (fires all events in range)
Player->PlayTo(
    FMovieSceneSequencePlaybackParams(FFrameTime(60), EUpdatePositionMethod::Play),
    FMovieSceneSequencePlayToParams());
```

### FMovieSceneEvent

`FMovieSceneEvent` holds the event endpoint data — the bound function to call when the event
fires. Event tracks are structured as:

- `UMovieSceneEventTrack` — the master track added to a binding or as a master track
- `UMovieSceneEventTriggerSection` — a section containing one or more trigger entries
- `FMovieSceneEvent` — each entry inside the trigger section, pointing to the endpoint function

The endpoint function is resolved at runtime against the event context objects (by default
`UWorld` and `ALevelScriptActor`). Director-based events resolve against a
`ULevelSequenceDirector` subclass instance.

### ULevelSequenceDirector — Custom Event Context

`ULevelSequenceDirector` provides a per-sequence scripting context that receives event track
calls. Subclass it (Blueprint or C++) and assign to the LevelSequence asset's Director Class
property. The Director instance is created when the sequence begins playing and destroyed
when it stops — its lifetime matches the sequence player.

```cpp
// MySequenceDirector.h
#include "LevelSequenceDirector.h"
#include "MySequenceDirector.generated.h"

UCLASS(Blueprintable)
class UMySequenceDirector : public ULevelSequenceDirector
{
    GENERATED_BODY()
public:
    // Called from Sequencer event tracks — bind to event key in the Sequencer editor
    UFUNCTION(BlueprintCallable, Category = "Cinematics")
    void OnDialogueStart(FName SpeakerTag);

    UFUNCTION(BlueprintCallable, Category = "Cinematics")
    void OnCutsceneChoice(int32 ChoiceIndex);
};

// MySequenceDirector.cpp
void UMySequenceDirector::OnDialogueStart(FName SpeakerTag)
{
    // Access the sequence player and bound actors from within the Director.
    // ULevelSequenceDirector.h: UPROPERTY ULevelSequencePlayer* Player (direct field, no getter)
    TArray<UObject*> Bound = Player->GetBoundObjects(SpeakerBindingID);
    // Trigger gameplay logic: UI, dialogue system, camera focus, etc.
}
```

**Why Director over Level Script**: The Director travels with the sequence asset, not the level.
Reusable across maps. Supports per-sequence state (member variables). Level Script events
only work when the sequence is placed in that specific level.

---

## MovieScene Tracks

```cpp
// MovieScene.h — get from the LevelSequence asset
UMovieScene* MS = SeqActor->GetSequence()->GetMovieScene();

// Possessables (world actors) — iterate by index
for (int32 i = 0; i < MS->GetPossessableCount(); ++i)
{
    const FMovieScenePossessable& P = MS->GetPossessable(i);
}
// Spawnables (sequence-owned actors) — iterate by index
for (int32 i = 0; i < MS->GetSpawnableCount(); ++i)
{
    const FMovieSceneSpawnable& S = MS->GetSpawnable(i);
}

// Master tracks (not bound to any actor)
const TArray<UMovieSceneTrack*>& Masters = MS->GetTracks();

// Tracks on a specific binding
const FMovieSceneBinding* B = MS->FindBinding(SomeGuid);
if (B) { for (UMovieSceneTrack* T : B->GetTracks()) { /* cast to subtype */ } }
```

| Track Class | Purpose |
|---|---|
| `UMovieScene3DTransformTrack` | Transform animation |
| `UMovieSceneSkeletalAnimationTrack` | Skeletal mesh animation |
| `UMovieSceneEventTrack` | Event triggers |
| `UMovieSceneAudioTrack` | Audio |
| `UMovieSceneFadeTrack` | Screen fade |
| `UMovieSceneCameraCutTrack` | Camera cuts |
| `UMovieSceneSubTrack` | Sub-sequences |
| `UMovieScenePropertyTrack` | Arbitrary UPROPERTY animation (base class) |

All track types require `MovieSceneTracks` in Build.cs.

**Custom tracks**: subclass `UMovieSceneTrack` + `UMovieSceneSection` for domain-specific
animation data. Register via `ISequencerModule::RegisterTrackEditor`. This is an advanced
pattern — most needs are met by `UMovieScenePropertyTrack` subclasses.

`UMovieScenePropertyTrack` animates arbitrary `UPROPERTY` values on bound objects. Common
concrete subclasses: `UMovieSceneFloatTrack` (float properties), `UMovieSceneBoolTrack`
(bool properties), `UMovieSceneColorTrack` (FLinearColor / FColor properties). Each creates
sections of the matching type (e.g., `UMovieSceneFloatSection`) that store a `FMovieSceneFloatChannel`.

### Sub-Sequences

```cpp
// Add a sub-sequence track to a master UMovieScene
UMovieScene* MasterMS = MasterSequence->GetMovieScene();
UMovieSceneSubTrack* SubTrack = MasterMS->AddTrack<UMovieSceneSubTrack>();

// Add a child sequence — AddSequence(Sequence, StartFrame, Duration)
FFrameRate DisplayRate = MasterMS->GetDisplayRate();
FFrameNumber Start = (2.0 * DisplayRate).FloorToFrame(); // 2 seconds in
int32 Duration = (5.0 * DisplayRate).FloorToFrame().Value; // 5 seconds long
UMovieSceneSubSection* SubSection =
    SubTrack->AddSequence(ChildLevelSequence, Start, Duration);

// Configure sub-section timing
SubSection->Parameters.TimeScale = 1.0;   // FMovieSceneTimeWarpVariant (double), playback speed multiplier
SubSection->Parameters.bCanLoop = false;
```

`UMovieSceneSubTrack` is a singleton master track — `AddTrack` returns the existing one if already present. Binding IDs inside sub-sequences carry a non-zero `SequenceID`; use `FMovieSceneObjectBindingID::ResolveParentIndex` when overriding bindings from the root player. Requires `MovieSceneTracks` module.

### Time Dilation and SlowMo

For SlowMo effects during sequences, use `Player->SetPlayRate(0.5f)` on the sequence player —
this is independent of `UGameplayStatics::SetGlobalTimeDilation` and does not affect world
physics or other gameplay systems. Combine with a post-process motion blur intensity increase
for cinematic slow motion without disrupting gameplay state.

---

## Movie Render Queue

```cpp
// MovieRenderPipelineCore module. Classes:
//   UMoviePipelineQueue           — holds jobs
//   UMoviePipelineExecutorJob     — sequence + map + config per job
//   UMoviePipelinePrimaryConfig   — root settings container
//   UMoviePipelineOutputSetting   — output path, file name format, frame rate
// Output formats: UMoviePipelineImageSequenceOutput_PNG / _EXR, UMoviePipelineAppleProResOutput
// Render passes: UMoviePipelineDeferredPassBase (final color, world normal, base color, depth)
//   Add passes to the PrimaryConfig to capture multiple AOVs per frame

UMoviePipelineQueue* Queue = NewObject<UMoviePipelineQueue>(this);
UMoviePipelineExecutorJob* Job =
    Queue->AllocateNewJob(UMoviePipelineExecutorJob::StaticClass());

Job->Sequence = FSoftObjectPath(MySequence);
Job->Map      = FSoftObjectPath(GetWorld());
Job->JobName  = TEXT("MyRender");
Job->SetConfiguration(NewObject<UMoviePipelinePrimaryConfig>(Job));
// Add pass/output settings to Job->GetConfiguration() as needed.

// Execute the render (editor only — MovieRenderPipelineEditor module)
UMoviePipelineQueueEngineSubsystem* QueueSubsystem =
    GEngine->GetEngineSubsystem<UMoviePipelineQueueEngineSubsystem>();
QueueSubsystem->RenderQueueWithExecutor(UMoviePipelineInProcessExecutor::StaticClass());
// For runtime/non-editor rendering, implement UMoviePipelineExecutorBase instead.
```

---

## Common Mistakes

**Binding after Play**: Overrides applied after `Play()` miss frame 0.
Always `SetBinding*` before `Play()`.

**Multiplayer camera cuts**: Camera cuts only affect the local client.
Use `SeqActor->SetReplicatePlayback(true)` for server-driven sync.

**Camera not returning after cutscene**: Sequencer does not auto-restore the player camera.
Subscribe to `OnFinished` and call `SetViewTargetWithBlend` + re-enable input.

**GC of spawned sequence actor**: `CreateLevelSequencePlayer` returns a raw pointer.
Store `OutActor` in a `UPROPERTY()` member to prevent garbage collection.

**Skipping mid-sequence**: Call `SetCompletionModeOverride(ForceRestoreState)` before `Stop()`
so actors return to their pre-sequence state.

**PIE timing**: Avoid wall-clock assumptions; use `GetCurrentTime()` frame numbers.

**Deprecated direct property**: `SeqActor->SequencePlayer` is deprecated since UE 5.4.
Use `SeqActor->GetSequencePlayer()`.

**Wrong player instance**: Calling `Play()` on a stale or mismatched `ULevelSequencePlayer`
pointer (e.g., from a different `ALevelSequenceActor` in the level) produces no visible effect
or animates the wrong actors. Always retrieve the player from the specific `ALevelSequenceActor`
that owns the sequence you intend to drive.

---

## Related Skills

- `ue-actor-component-architecture` — actor spawning and component setup for bound actors
- `ue-animation-system` — skeletal animation tracks, AnimMontage integration in Sequencer
- `ue-cpp-foundations` — delegate patterns, `UFUNCTION`, `UPROPERTY`
- `ue-gameplay-framework` — PlayerController camera restoration, GameMode flow
