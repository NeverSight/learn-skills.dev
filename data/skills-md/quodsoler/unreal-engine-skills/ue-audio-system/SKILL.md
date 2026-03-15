---
name: ue-audio-system
description: "Use this skill when working with audio, sound, music, UAudioComponent, PlaySoundAtLocation, SoundCue, MetaSound, attenuation, submix, concurrency, SFX, or spatial audio in Unreal Engine. See references/audio-setup-patterns.md for music system and ambient soundscape architectures. For VFX audio synchronization, see ue-niagara-effects."
metadata:
  version: 1.0.0
---

# UE Audio System

You are an expert in Unreal Engine's audio systems, covering UAudioComponent, sound asset types,
spatial attenuation, concurrency management, submix routing, MetaSounds, and runtime audio analysis.

## Context Check

Before implementing audio, read `.agents/ue-project-context.md` for:

- **Audio plugins** enabled (Resonance Audio, Steam Audio, Wwise, FMOD, MetaSound plugin version)
- **Target platforms** — mobile has strict voice limits; consoles differ from PC
- **Dedicated server** flag — audio must be skipped server-side or it will crash/log errors
- **VR flag** — VR projects require binaural spatialization settings

## Information Gathering

Ask about:

1. One-shot SFX, looping ambient, music, UI feedback, or dialogue?
2. Spatialized (follows actor) or global 2D?
3. Concurrency concern (gunshots, footsteps, explosions)?
4. Runtime control needed (fade, pause, parameter changes)?
5. MetaSound procedural or pre-authored SoundCue/SoundWave?

---

## Sound Asset Hierarchy

```
USoundBase                    // abstract base (SoundBase.h)
  ├── USoundWave              // raw PCM/compressed audio asset
  ├── USoundCue               // node-graph: random, modulator, mixer, attenuator nodes
  └── UMetaSoundSource        // procedural audio graph (MetaSound plugin)
```

**USoundWave** — Import .wav/.ogg/.flac. Set `SoundClassObject` and `AttenuationSettings` on asset.

**USoundCue** — Node graph combining multiple waves. Key nodes:
`USoundNodeRandom`, `USoundNodeModulator`, `USoundNodeMixer`, `USoundNodeAttenuation`,
`USoundNodeLooping`, `USoundNodeDelay`, `USoundNodeDistanceCrossFade`.

**UMetaSoundSource** — Procedural audio graph. Declare typed inputs (float, bool, int32, trigger).
Set parameters at runtime via `UAudioComponent::SetFloatParameter`, `SetBoolParameter`, `SetIntParameter`.

### Streaming Long Audio

For music and ambient tracks exceeding ~30 seconds, set `USoundWave::LoadingBehavior`:
`ESoundWaveLoadingBehavior::ForceInline` for short SFX, `RetainOnLoad` for music loaded at level start.
Long files should use `LoadOnDemand` to avoid loading the full waveform into memory.
In the editor: SoundWave asset → Details → Loading → Loading Behavior.

---

## Playing Sounds from C++

### Fire-and-Forget

```cpp
#include "Kismet/GameplayStatics.h"

// 2D — not spatialized (UI, music)
UGameplayStatics::PlaySound2D(
    this, ImpactSound, 1.0f /*Vol*/, 1.0f /*Pitch*/, 0.0f /*StartTime*/,
    ConcurrencySettings, OwningActor
);

// 3D — spatialized, requires AttenuationSettings on the sound asset
UGameplayStatics::PlaySoundAtLocation(
    this, GunShotSound, GetActorLocation(), FRotator::ZeroRotator,
    1.0f, 1.0f, 0.0f,
    AttenuationOverride,    // USoundAttenuation* (nullptr = use asset default)
    ConcurrencyOverride,    // USoundConcurrency* (nullptr = use asset default)
    this                    // OwningActor for per-owner concurrency
);
```

### Spawn with Handle

```cpp
// Returns UAudioComponent* — auto-destroyed when sound finishes if bAutoDestroy=true
UAudioComponent* Comp = UGameplayStatics::SpawnSoundAtLocation(
    this, ExplosionSound, Location, FRotator::ZeroRotator,
    1.0f, 1.0f, 0.0f, AttenuationSettings, nullptr, /*bAutoDestroy=*/true
);

// Attach to a moving component (vehicle engine)
UAudioComponent* EngineAudio = UGameplayStatics::SpawnSoundAttached(
    EngineLoopSound, GetMesh(), NAME_None,
    FVector::ZeroVector, FRotator::ZeroRotator,
    EAttachLocation::SnapToTargetIncludingScale,
    /*bStopWhenAttachedToDestroyed=*/true,
    1.0f, 1.0f, 0.0f, AttenuationSettings, nullptr,
    /*bAutoDestroy=*/false   // keep alive for looping
);
```

### UAudioComponent as Permanent Actor Component

```cpp
// In constructor:
AudioComponent = CreateDefaultSubobject<UAudioComponent>(TEXT("AudioComponent"));
AudioComponent->SetupAttachment(RootComponent);
AudioComponent->bAutoActivate = false;
AudioComponent->bStopWhenOwnerDestroyed = true;
```

### Playback Control

```cpp
AudioComponent->SetSound(EngineLoopSound);
AudioComponent->Play(/*StartTime=*/0.0f);
AudioComponent->Stop();
AudioComponent->SetPaused(true);
AudioComponent->FadeIn(0.5f, 1.0f, 0.0f, EAudioFaderCurve::Linear);
AudioComponent->FadeOut(1.0f, 0.0f, EAudioFaderCurve::Linear);
AudioComponent->SetVolumeMultiplier(0.5f);
AudioComponent->SetPitchMultiplier(1.2f);

// Query play state (EAudioComponentPlayState: Playing, Stopped, Paused, FadingIn, FadingOut)
EAudioComponentPlayState State = AudioComponent->GetPlayState();
```

### Delegates (AudioComponent.h)

```cpp
// Declared in AudioComponent.h:
// DECLARE_DYNAMIC_MULTICAST_DELEGATE(FOnAudioFinished)
// DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FOnAudioPlaybackPercent, const USoundWave*, PlayingSoundWave, const float, PlaybackPercent)
// DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FOnAudioPlayStateChanged, EAudioComponentPlayState, PlayState)

AudioComponent->OnAudioFinished.AddDynamic(this, &AMyActor::OnSoundFinished);
AudioComponent->OnAudioPlaybackPercent.AddDynamic(this, &AMyActor::OnPlaybackPercent);
AudioComponent->OnAudioPlayStateChanged.AddDynamic(this, &AMyActor::OnPlayStateChanged);

// Native (non-UObject) binding — no GC overhead:
// DECLARE_MULTICAST_DELEGATE_OneParam(FOnAudioFinishedNative, UAudioComponent*)
// DECLARE_MULTICAST_DELEGATE_ThreeParams(FOnAudioPlaybackPercentNative, const UAudioComponent*, const USoundWave*, const float)
AudioComponent->OnAudioFinishedNative.AddUObject(this, &AMyActor::OnSoundFinishedNative);
AudioComponent->OnAudioPlaybackPercentNative.AddUObject(this, &AMyActor::OnPlaybackPercentNative);
```

---

## Sound Attenuation (SoundAttenuation.h)

Defined in `USoundAttenuation` assets (wrapping `FSoundAttenuationSettings`).
Assign via `USoundBase::AttenuationSettings` or pass as override to play functions.

**Attenuation shapes** (`EAttenuationShape`): `Sphere` (default, omnidirectional), `Capsule` (elongated sources), `Box` (room-shaped), `Cone` (directional like spotlights).

**Distance model** (`EAttenuationDistanceModel`): `Linear`, `Logarithmic` (realistic), `NaturalSound` (perception-matched, recommended), `Inverse`, `LogReverse`, `Custom` (curve-driven).

```cpp
// Key FSoundAttenuationSettings fields:
uint8 bAttenuate : 1;          // enable distance-based volume falloff
uint8 bSpatialize : 1;         // enable 3D spatialization
// SpatializationAlgorithm: SPATIALIZATION_Default (panning), SPATIALIZATION_HRTF (binaural plugin)

uint8 bAttenuateWithLPF : 1;   // air absorption (distance-based lowpass)
float LPFRadiusMin;            // LPF starts at this distance (cm)
float LPFRadiusMax;            // LPF fully applied at this distance
float LPFFrequencyAtMin;       // Hz at min distance (e.g. 20000.f = bypass)
float LPFFrequencyAtMax;       // Hz at max distance (e.g. 800.f = muffled)

uint8 bEnableListenerFocus : 1;
float FocusAzimuth;            // in-focus cone half-angle (degrees)
float NonFocusAzimuth;         // non-focus cone half-angle (degrees)
float FocusDistanceScale;      // < 1.0 makes focused sound seem closer
float NonFocusVolumeAttenuation;

uint8 bEnableOcclusion : 1;
TEnumAsByte<ECollisionChannel> OcclusionTraceChannel; // e.g. ECC_Visibility
float OcclusionLowPassFilterFrequency;  // Hz when fully occluded
float OcclusionVolumeAttenuation;       // 0..1 volume scale when occluded
float OcclusionInterpolationTime;       // seconds to interpolate

uint8 bEnableReverbSend : 1;
EReverbSendMethod ReverbSendMethod;     // Linear, CustomCurve, Manual
float ReverbWetLevelMin;
float ReverbWetLevelMax;
float ReverbDistanceMin;
float ReverbDistanceMax;

uint8 bEnablePriorityAttenuation : 1;  // reduce priority of distant sounds
float PriorityAttenuationMin;
float PriorityAttenuationMax;

// Override attenuation inline on a UAudioComponent:
AudioComponent->bOverrideAttenuation = true;
AudioComponent->AttenuationOverrides.bAttenuate = true;
AudioComponent->AttenuationOverrides.bSpatialize = true;
AudioComponent->AttenuationOverrides.FalloffDistance = 3000.f;
```

### Audio LOD

Distant sounds can skip processing. Use `bAttenuateWithLPF = true` with `LPFRadiusMin`/`LPFRadiusMax`
to low-pass-filter far sounds before full attenuation drops them. Set `bEnableSendToAudioLink = false`
for background ambience that does not need external routing. `USoundBase::Priority` (0.0–100.0, default 1.0, higher =
more important) determines which voices survive when hitting the max channel count set in Audio Settings.

---

## Concurrency (SoundConcurrency.h)

`USoundConcurrency` controls simultaneous voice count. Assign via
`USoundBase::ConcurrencySet` (`TSet<USoundConcurrency*>`) or `ConcurrencyOverrides`
(inline `FSoundConcurrencySettings` when `bOverrideConcurrency = true`).

```cpp
// FSoundConcurrencySettings key fields:
int32 MaxCount;               // max simultaneous voices in this group
// USoundBase::Priority (0.0–100.0, default 1.0) determines which voices survive at MaxCount
uint8 bLimitToOwner : 1;      // limit per owning actor if true
TEnumAsByte<EMaxConcurrentResolutionRule::Type> ResolutionRule;
// PreventNew | StopOldest | StopFarthestThenPreventNew | StopFarthestThenOldest
// StopLowestPriority | StopQuietest | StopLowestPriorityThenPreventNew
float RetriggerTime;          // minimum seconds between plays in this group
float VoiceStealReleaseTime;  // fade duration (s) for evicted sounds
EConcurrencyVolumeScaleMode VolumeScaleMode; // Default | Distance | Priority
float VolumeScaleAttackTime;
float VolumeScaleReleaseTime;
```

---

## Submixes and Sound Classes (SoundSubmix.h)

```
USoundSubmixBase (abstract)
  USoundSubmixWithParentBase
    USoundSubmix           // standard submix with effects chain
    USoundfieldSubmix      // ambisonics / soundfield
  UEndpointSubmix          // external endpoint (haptics, extra device)
```

Typical tree: Master > {Music, SFX, Voice, Ambient}. Music submix uses `bMuteWhenBackgrounded = true`.

```cpp
// Runtime volume control:
MusicSubmix->SetSubmixOutputVolume(this, 0.5f);  // linear gain multiplier
MusicSubmix->SetSubmixWetLevel(this, 1.0f);
MusicSubmix->SetSubmixDryLevel(this, 0.0f);

// Dynamic parenting:
MyChildSubmix->DynamicConnect(this, MasterSubmix);
MyChildSubmix->DynamicDisconnect(this);
```

`USoundSubmix::SubmixEffectChain` holds `USoundEffectSubmixPreset` assets
(reverb `USubmixEffectReverbPreset`, EQ `USubmixEffectEQPreset`, dynamics).

### Submix Effect Chain

```cpp
// Add reverb to a submix at runtime
USoundSubmix* ReverbSubmix = LoadObject<USoundSubmix>(nullptr,
    TEXT("/Game/Audio/Submixes/ReverbSubmix"));
USubmixEffectReverbPreset* Preset = NewObject<USubmixEffectReverbPreset>();
Preset->Settings.Density = 0.85f;
Preset->Settings.Diffusion = 0.8f;
Preset->Settings.DecayTime = 2.5f;
ReverbSubmix->SubmixEffectChain.Add(Preset);
```

**Sound classes** define volume/pitch hierarchy parallel to submixes. Assign via `USoundBase::SoundClassObject`.

```cpp
// Sound Mix modifiers — layer temporary volume/pitch adjustments by sound class:
UGameplayStatics::SetBaseSoundMix(this, DefaultMix);            // set the base mix (usually once)
UGameplayStatics::PushSoundMixModifier(this, CombatMix);        // push a modifier (stacks)
// ... later, when leaving combat:
UGameplayStatics::PopSoundMixModifier(this, CombatMix);         // remove the modifier layer
// ClearSoundMixModifiers removes all pushed modifiers at once
UGameplayStatics::ClearSoundMixModifiers(this);
```

`USoundMix` assets define per-`USoundClass` volume and pitch adjustments. Push/pop lets you layer context-dependent audio profiles (combat, stealth, underwater) without manual volume bookkeeping.

---

## MetaSounds

`UMetaSoundSource` derives from `USoundBase` — plays anywhere a `USoundBase` is accepted.

```cpp
// UAudioComponent implements ISoundParameterControllerInterface:
MetaComp->SetFloatParameter(FName("Pitch"), 1.5f);
MetaComp->SetBoolParameter(FName("IsUnderwater"), true);
MetaComp->SetIntParameter(FName("SurfaceType"), 2);
MetaComp->SetTriggerParameter(FName("OnImpact"));  // impulse trigger input
MetaComp->ResetParameters();
```

| Criterion | SoundCue | MetaSound |
|---|---|---|
| Runtime parameters | Limited (wave params) | Typed inputs, full parameter system |
| Procedural audio | No | Yes (oscillators, noise, DSP filters) |
| Reactive to gameplay | Via parameter nodes | Native — bind any float/bool/trigger |
| Use when | Randomized pre-authored sounds | Adaptive music, procedural SFX, state-driven audio |

---

## Submix Spectrum Analysis and Envelope Following (SoundSubmix.h)

```cpp
// Envelope following:
SFXSubmix->StartEnvelopeFollowing(this);
FOnSubmixEnvelopeBP Env;
Env.BindDynamic(this, &AMyActor::OnSubmixEnvelope);
SFXSubmix->AddEnvelopeFollowerDelegate(this, Env);
SFXSubmix->StopEnvelopeFollowing(this);
// Callback: void OnSubmixEnvelope(const TArray<float>& Envelope);

// Spectrum analysis:
SFXSubmix->StartSpectralAnalysis(this,
    EFFTSize::Medium, EFFTPeakInterpolationMethod::Linear,
    EFFTWindowType::Hann, 0.0f, EAudioSpectrumType::MagnitudeSpectrum
);

TArray<FSoundSubmixSpectralAnalysisBandSettings> Bands;
FSoundSubmixSpectralAnalysisBandSettings LowBand;
LowBand.BandFrequency = 80.f; LowBand.AttackTimeMsec = 10.f; LowBand.ReleaseTimeMsec = 100.f;
Bands.Add(LowBand);

FOnSubmixSpectralAnalysisBP Spectral;
Spectral.BindDynamic(this, &AMyActor::OnSpectralAnalysis);
SFXSubmix->AddSpectralAnalysisDelegate(
    this, Bands, Spectral,
    30.f /*UpdateRateHz*/, -40.f /*DecibelFloor*/, true /*Normalize*/, false /*AutoRange*/
);
SFXSubmix->StopSpectralAnalysis(this);
// Callback: void OnSpectralAnalysis(const TArray<float>& Magnitudes);
```

---

## Module Dependencies

```csharp
// In .Build.cs:
PublicDependencyModuleNames.AddRange(new string[] { "Engine", "AudioMixer" });
PublicDependencyModuleNames.Add("MetasoundEngine");    // for MetaSound parameters
PublicDependencyModuleNames.Add("MetasoundFrontend");
```

```cpp
#include "Components/AudioComponent.h"
#include "Kismet/GameplayStatics.h"
#include "Sound/SoundBase.h"
#include "Sound/SoundCue.h"
#include "Sound/SoundWave.h"
#include "Sound/SoundAttenuation.h"
#include "Sound/SoundConcurrency.h"
#include "Sound/SoundSubmix.h"
```

---

## Audio Analysis

### Submix Spectrum and Envelope

See the existing submix analysis section above for real-time analysis via `USoundSubmix`.

### Non-Real-Time Analysis (NRT)

`UAudioAnalyzerNRT` is the abstract base class for offline analyzers. `ULoudnessNRT` and `UOnsetNRT` derive from `UAudioSynesthesiaNRT`, which in turn derives from `UAudioAnalyzerNRT`.

For offline audio analysis (e.g., beat detection for rhythmic gameplay), use the Audio Synesthesia plugin:

```cpp
// Build.cs: "AudioSynesthesia"
#include "AudioSynesthesiaModule.h"

// Create an analyzer — LoudnessNRT analyzes an entire sound asset offline
ULoudnessNRT* Analyzer = NewObject<ULoudnessNRT>();
ULoudnessNRTSettings* Settings = NewObject<ULoudnessNRTSettings>();
Settings->AnalysisPeriod = 0.01f; // 10ms windows

Analyzer->Settings = Settings;
Analyzer->Sound = MySoundWave;
Analyzer->AnalyzeAudio();  // WITH_EDITOR only; call from editor utility or cook-time code

// Query results at specific timestamps
float Loudness;
Analyzer->GetLoudnessAtTime(1.5f, Loudness);

// For beat detection, use OnsetNRT:
UOnsetNRT* OnsetAnalyzer = NewObject<UOnsetNRT>();
OnsetAnalyzer->Sound = MySoundWave;
OnsetAnalyzer->AnalyzeAudio();  // WITH_EDITOR only
TArray<float> OnsetTimestamps;
TArray<float> OnsetStrengths;
OnsetAnalyzer->GetNormalizedChannelOnsetsBetweenTimes(
    0.f, Duration, 0, OnsetTimestamps, OnsetStrengths);
```

**Why NRT**: Pre-analyze tracks to generate beat maps, loudness curves, or onset markers. Use the data at runtime for music-driven gameplay without per-frame FFT overhead.

---

## Common Mistakes and Anti-Patterns

**Spawning a new AudioComponent every fire event**
```cpp
// WRONG — leaks a component instance per call
UAudioComponent* Comp = NewObject<UAudioComponent>(this);
Comp->SetSound(FireSound); Comp->Play();

// CORRECT — fire-and-forget for one-shots
UGameplayStatics::PlaySoundAtLocation(this, FireSound, GetActorLocation());
// CORRECT — cache a single component for repeated/looping sounds
if (!CachedFireAudio) { CachedFireAudio = UGameplayStatics::SpawnSoundAttached(..., /*bAutoDestroy=*/false); }
CachedFireAudio->Play();
```

**Playing 3D sounds without attenuation**
```cpp
// WRONG — full volume at any distance
UGameplayStatics::PlaySoundAtLocation(this, FootstepSound, Location);
// CORRECT — pass or assign USoundAttenuation with sphere falloff tuned to gameplay scale
```

**Ignoring concurrency on high-frequency sounds**
```cpp
// WRONG — 20 simultaneous explosions with default concurrency
UGameplayStatics::PlaySoundAtLocation(this, ExplosionSound, Location);
// CORRECT — pass USoundConcurrency: MaxCount=4, ResolutionRule=StopFarthestThenOldest
```

**Playing audio on a dedicated server**
```cpp
// WRONG — FAudioDevice not initialized on server, causes crash/log spam
void AWeapon::Fire() { UGameplayStatics::PlaySoundAtLocation(this, FireSound, GetActorLocation()); }
// CORRECT
void AWeapon::Fire() {
    if (GetNetMode() != NM_DedicatedServer) {
        UGameplayStatics::PlaySoundAtLocation(this, FireSound, GetActorLocation());
    }
}
```

**Forgetting to unbind delegates before destruction**
```cpp
// In EndPlay:
if (AudioComponent) { AudioComponent->OnAudioFinished.RemoveAll(this); AudioComponent->Stop(); }
```

**Using PlaySound2D for in-world sounds**
```cpp
// WRONG — no attenuation or spatialization
UGameplayStatics::PlaySound2D(this, GunShot);
// CORRECT
UGameplayStatics::PlaySoundAtLocation(this, GunShot, GetActorLocation());
```

---

## Platform and Edge Case Considerations

- **Mobile** — 16–32 voice limit. Use aggressive concurrency. Prefer resident loading for SFX. Disable HRTF unless the platform supports it.
- **Dedicated servers** — Guard all audio calls with `GetNetMode() != NM_DedicatedServer`.
- **Streaming audio** — Set `LoadingBehavior = LoadOnDemand` on long music SoundWave assets. Never load minutes of music resident.
- **App focus loss** — Set `bMuteWhenBackgrounded = true` on music/SFX submixes. For custom handling:

### Focus Loss Handling

```cpp
// In your GameInstance or AudioManager
FCoreDelegates::ApplicationWillDeactivateDelegate.AddUObject(
    this, &UMyAudioManager::OnAppDeactivate);

void UMyAudioManager::OnAppDeactivate()
{
    FAudioDeviceHandle Device = GEngine->GetMainAudioDevice();
    if (Device.IsValid()) { Device->SetTransientPrimaryVolume(0.f); }
}
```

- **VR** — Enable `bSpatialize = true` and `SpatializationAlgorithm = SPATIALIZATION_HRTF` on all 3D attenuation assets.
- **Audio LOD** — Use `bEnablePriorityAttenuation` to reduce priority of distant sounds before voice-budget culling.

---

## Related Skills

- `ue-actor-component-architecture` — UAudioComponent lifetime, attachment, and replication patterns
- `ue-niagara-effects` — synchronizing audio events with particle system callbacks
- `ue-cpp-foundations` — delegate binding patterns, UPROPERTY and UFUNCTION macros
