---
name: juce-plugin
description: Build JUCE audio plugins (VST3, AU, AAX, Standalone, LV2) in C++ with CMake. Covers the full development workflow from project scaffolding to multi-format builds, including AudioProcessor lifecycle, parameter management with APVTS, DSP module chains, custom editor GUIs, Three.js/GLB WebView interfaces, state serialization, real-time audio safety, and cross-platform CI/CD. Use this skill whenever the user mentions JUCE, audio plugins, VST plugins, AU plugins, audio effects, synthesizers, MIDI processors, AudioProcessor, AudioProcessorEditor, Projucer, or wants to create audio software — even if they just say "make a plugin" or "audio plugin". Also applies when users are working in an existing JUCE codebase (files like PluginProcessor.cpp, PluginEditor.cpp, CMakeLists.txt with juce_add_plugin), or investigating a plugin's CPU usage in a host, porting a plugin to Windows or Linux, or code signing, notarizing or packaging plugin releases.
---

# JUCE Audio Plugin Development

You are helping build an audio plugin using JUCE — a cross-platform C++ framework for audio applications and plugins. Plugins compile to VST3, AU, AAX, LV2, and Standalone formats from a single codebase.

## How JUCE Plugins Work

A JUCE plugin has two core classes that are always paired:

- **AudioProcessor** (engine) — the DSP core. Owns parameters, processes audio in `processBlock()`, handles state save/load. Runs on the real-time audio thread.
- **AudioProcessorEditor** (GUI) — the visual interface. Connected to parameters via APVTS attachments. Runs on the message thread.

`AudioProcessorValueTreeState` (APVTS) bridges both: thread-safe parameter access for the audio thread, UI attachments for the editor, and XML serialization for presets/state.

## Project Structure

```
MyPlugin/
  CMakeLists.txt           # Build configuration with juce_add_plugin()
  Source/
    PluginProcessor.h      # AudioProcessor subclass declaration
    PluginProcessor.cpp    # AudioProcessor implementation
    PluginEditor.h         # AudioProcessorEditor subclass declaration
    PluginEditor.cpp       # Editor GUI implementation
    dsp/                   # Custom DSP classes (filters, oscillators, etc.)
    components/            # Custom UI components (spectrum displays, etc.)
  resources/               # Assets (images, impulse responses, fonts)
```

## Workflow: Creating a New Plugin

### 1. Set Up the Project

Decide how to include JUCE:

```cmake
# Option A: JUCE as subdirectory (most common for plugins)
add_subdirectory(JUCE)

# Option B: System-installed JUCE
find_package(JUCE CONFIG REQUIRED)
```

### 2. Write CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.22)
project(MyPlugin VERSION 1.0.0)

add_subdirectory(JUCE)

juce_add_plugin(MyPlugin
    COMPANY_NAME "YourCompany"
    PLUGIN_MANUFACTURER_CODE Yco1    # 4 chars, at least 1 uppercase
    PLUGIN_CODE Mp01                  # 4 chars, exactly 1 uppercase
    FORMATS VST3 AU Standalone        # Build targets
    PRODUCT_NAME "My Plugin"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE)     # Auto-install on build

target_sources(MyPlugin PRIVATE
    Source/PluginProcessor.cpp
    Source/PluginEditor.cpp)

target_compile_definitions(MyPlugin PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0)

target_link_libraries(MyPlugin
    PRIVATE juce::juce_audio_utils
    PUBLIC
        juce::juce_recommended_config_flags
        juce::juce_recommended_lto_flags
        juce::juce_recommended_warning_flags)
```

For the full CMake API (SDK paths, binary data, bundle resources, iOS/macOS specifics), read `references/cmake-reference.md`.

### 3. Create the Processor

The AudioProcessor subclass must override specific methods. Read `references/plugin-lifecycle.md` for the complete contract.

**Minimal processor skeleton:**

```cpp
// PluginProcessor.h
#pragma once
#include <juce_audio_processors/juce_audio_processors.h>

class MyPluginProcessor : public juce::AudioProcessor
{
public:
    MyPluginProcessor();
    ~MyPluginProcessor() override;

    // Audio processing
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    // Editor
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    // Info
    const juce::String getName() const override;
    bool acceptsMidi() const override;
    bool producesMidi() const override;
    double getTailLengthSeconds() const override;
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    // State
    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    // Bus layout
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;

    // APVTS — the parameter manager
    juce::AudioProcessorValueTreeState apvts;

private:
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (MyPluginProcessor)
};
```

### 4. Set Up Parameters with APVTS

Define all parameters statically in a free function, then initialize APVTS in the constructor. Read `references/parameter-management.md` for the full patterns (attachments, dynamic-ish parameters, non-parameter state).

```cpp
// In PluginProcessor.cpp

juce::AudioProcessorValueTreeState::ParameterLayout createParameterLayout()
{
    return {
        std::make_unique<juce::AudioParameterFloat>(
            juce::ParameterID { "gain", 1 },
            "Gain",
            juce::NormalisableRange<float> (0.0f, 1.0f, 0.001f),
            0.5f),
        std::make_unique<juce::AudioParameterChoice>(
            juce::ParameterID { "filterType", 1 },
            "Filter Type",
            juce::StringArray { "Low Pass", "High Pass", "Band Pass" },
            0),
        std::make_unique<juce::AudioParameterBool>(
            juce::ParameterID { "bypass", 1 },
            "Bypass",
            false)
    };
}

MyPluginProcessor::MyPluginProcessor()
    : AudioProcessor (BusesProperties()
        .withInput  ("Input",  juce::AudioChannelSet::stereo())
        .withOutput ("Output", juce::AudioChannelSet::stereo())),
      apvts (*this, nullptr, "Parameters", createParameterLayout())
{
}
```

### 5. Implement processBlock

This is where audio processing happens. It runs on the real-time thread — follow strict rules. Read `references/audio-thread-safety.md` for the full safety guide.

```cpp
void MyPluginProcessor::processBlock (juce::AudioBuffer<float>& buffer,
                                       juce::MidiBuffer& midiMessages)
{
    juce::ScopedNoDenormals noDenormals;

    // Read parameter values (thread-safe via atomics)
    auto gainValue = apvts.getRawParameterValue("gain")->load();

    for (int channel = 0; channel < buffer.getNumChannels(); ++channel)
    {
        auto* channelData = buffer.getWritePointer (channel);
        for (int sample = 0; sample < buffer.getNumSamples(); ++sample)
        {
            channelData[sample] *= gainValue;
        }
    }
}
```

For DSP module patterns (filters, oscillators, effects chains, convolution), read `references/dsp-patterns.md`.

### 6. Implement State Save/Load

```cpp
void MyPluginProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    auto state = apvts.copyState();
    if (auto xml = state.createXml())
        copyXmlToBinary (*xml, destData);
}

void MyPluginProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    if (auto xml = getXmlFromBinary (data, sizeInBytes))
        if (xml->hasTagName (apvts.state.getType()))
            apvts.replaceState (juce::ValueTree::fromXml (*xml));
}
```

### 7. Create the Editor

The editor connects UI controls to APVTS parameters via attachments. Read `references/ui-patterns.md` for custom components, layout strategies, and LookAndFeel customization.

```cpp
// PluginEditor.h
#pragma once
#include <juce_audio_processors/juce_audio_processors.h>
#include "PluginProcessor.h"

class MyPluginEditor : public juce::AudioProcessorEditor
{
public:
    MyPluginEditor (MyPluginProcessor&);
    ~MyPluginEditor() override;

    void paint (juce::Graphics&) override;
    void resized() override;

private:
    MyPluginProcessor& processorRef;

    juce::Slider gainSlider;
    juce::AudioProcessorValueTreeState::SliderAttachment gainAttachment;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (MyPluginEditor)
};
```

```cpp
// PluginEditor.cpp
MyPluginEditor::MyPluginEditor (MyPluginProcessor& p)
    : AudioProcessorEditor (&p),
      processorRef (p),
      gainAttachment (p.apvts, "gain", gainSlider)
{
    addAndMakeVisible (gainSlider);
    gainSlider.setSliderStyle (juce::Slider::RotaryHorizontalVerticalDrag);
    gainSlider.setTextBoxStyle (juce::Slider::TextBoxBelow, false, 80, 20);

    setResizeLimits (200, 150, 800, 600);
    setResizable (true, true);
    setSize (400, 300);
}

void MyPluginEditor::resized()
{
    auto bounds = getLocalBounds().reduced (10);
    gainSlider.setBounds (bounds.removeFromTop (100));
}
```

### 8. Build and Test

```bash
# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build all formats
cmake --build build --config Release

# On macOS, plugins are copied to:
#   ~/Library/Audio/Plug-Ins/VST3/
#   ~/Library/Audio/Plug-Ins/Components/ (AU)
# On Linux:
#   ~/.vst3/
#   ~/.lv2/ (if LV2 format enabled)
# On Windows (64-bit; copying there needs an elevated build):
#   C:\Program Files\Common Files\VST3\
```

For CMake options and a CI matrix, read `references/cmake-reference.md`. For what differs on Windows and Linux (MSVC fixes, WebView2/WebKitGTK, glibc baseline, headless tests, x86 floating-point differences), read [platform builds](references/platform-builds.md). For signed releases (Developer ID, notarized `.pkg`, Windows Artifact Signing from GitHub Actions), read [signing and notarization](references/signing-and-notarization.md).

## Plugin Types

JUCE supports several plugin categories, configured via CMake properties:

| Type | CMake Flags | Description |
|------|-------------|-------------|
| **Audio Effect** | defaults | Processes audio input to output |
| **Synthesizer** | `IS_SYNTH TRUE`, `NEEDS_MIDI_INPUT TRUE` | Generates audio from MIDI |
| **MIDI Effect** | `IS_MIDI_EFFECT TRUE` | Processes MIDI only (no audio) |
| **Synth + MIDI Out** | Add `NEEDS_MIDI_OUTPUT TRUE` | Synth that also sends MIDI |

## JUCE Modules

Modules are the building blocks. Link the top-level module and transitive dependencies resolve automatically:

| Module | Purpose | Link |
|--------|---------|------|
| `juce_audio_utils` | Audio utilities, MIDI keyboard | `juce::juce_audio_utils` |
| `juce_dsp` | DSP: filters, oscillators, convolution, ProcessorChain | `juce::juce_dsp` |
| `juce_audio_processors` | AudioProcessor, APVTS, plugin format hosting | (auto-included) |
| `juce_graphics` | Graphics, Colour, Path, Image | (auto-included) |
| `juce_gui_basics` | Component, Slider, Button, Label | (auto-included) |
| `juce_gui_extra` | CodeEditorComponent, WebBrowserComponent | `juce::juce_gui_extra` |
| `juce_opengl` | OpenGL rendering in plugins | `juce::juce_opengl` |
| `juce_osc` | Open Sound Control (OSC) | `juce::juce_osc` |

The 24 JUCE modules are: `juce_analytics`, `juce_animation`, `juce_audio_basics`, `juce_audio_devices`, `juce_audio_formats`, `juce_audio_plugin_client`, `juce_audio_processors`, `juce_audio_processors_headless`, `juce_audio_utils`, `juce_box2d`, `juce_core`, `juce_cryptography`, `juce_data_structures`, `juce_dsp`, `juce_events`, `juce_graphics`, `juce_gui_basics`, `juce_gui_extra`, `juce_javascript`, `juce_midi_ci`, `juce_opengl`, `juce_osc`, `juce_product_unlocking`, `juce_video`.

## WebView UIs (JUCE 9)

For web-based editors, enable the browser module and use the current [WebView integration reference](references/webview-ui.md) for CMake/WebView2, relay lifetime, frontend package compatibility, offline resources and gestures. The native editor example's `JUCE_WEB_BROWSER=0` must become `1`. Verify API signatures against the installed JUCE version.

For interactive Blender-authored amps, pedals or rack gear, read [Three.js/WebView UI](references/threejs-webview-ui.md). It covers the staged Blender → semantic GLB → mock Three.js → JUCE WebView → APVTS workflow, absolute and pull/rotate controls, switches, input jacks, coupled visible state, plugin-only utility chrome, render-on-demand and host acceptance. Keep APVTS authoritative, construct relays before the browser and attachments after it, and keep all WebView work off the audio thread.

## Reference Files

Read these as needed based on what you're implementing:

- **`references/plugin-lifecycle.md`** — Complete AudioProcessor contract: all overrides, bus configurations, double precision, Synthesiser framework for synths
- **`references/parameter-management.md`** — APVTS patterns: parameter layout, attachments, raw pointers, non-parameter state, parameter groups
- **`references/dsp-patterns.md`** — DSP cookbook: ProcessorChain, filters, oscillators, waveshapers, convolution reverb, delay lines, wavetable synthesis, LFO at control rate, two-level chain architecture, per-sample vs block processing
- **`references/ui-patterns.md`** — Editor patterns: component layout, custom widgets, LookAndFeel, meters, FFT spectrum analyser, responsive resize, binary data for assets
- **`references/webview-ui.md`** — JUCE 9 WebBrowserComponent, WebView2, local resources, native functions, parameter bindings, frontend frameworks, explicit development mode, and streaming visual data (meter and repaint cost, idle acceptance)
- **`references/threejs-webview-ui.md`** — Interactive guitar-gear GLBs, mock/JUCE bindings, physical controls, derived visual state, render-on-demand, shadow-map invalidation, redraw cadence, pixel ratio, draw calls and staged host validation
- **`references/audio-thread-safety.md`** — Real-time safety rules: what you can/cannot do in processBlock, lock-free patterns, atomics, debugging audio glitches
- **`references/cmake-reference.md`** — Full CMake API: all juce_add_plugin properties, SDK paths, binary data, CI/CD, platform specifics
- **`references/platform-builds.md`** — macOS vs Windows vs Linux: formats and bundle layouts, copy folders, MSVC portability fixes, npm/CRLF/path plumbing, Linux packages and glibc baseline, test executables that compile a WebView editor, headless tests (Xvfb), Intel-only snap-to-zero and other cross-CPU float differences, CI jobs, local Linux reproduction
- **`references/signing-and-notarization.md`** — macOS Developer ID certificates, `.p12`/`.p8` credentials, keychain, `codesign`, `pkgbuild`/`productbuild`, notarytool, stapler, installer branding; Windows Artifact Signing (identity validation, certificate profile, OIDC federated credential, signing action, verification); GitHub secrets on the Free plan
- **`references/performance-investigation.md`** — A plugin "uses too much CPU": attributing audio-thread, message-thread and WebView cost before optimizing, headless versus live-callback measurement, the test matrix, stage breakdown, harness and live-host tooling, null tests, multi-instance scaling, performance gates, and the report
- **`references/production-plugin-practices.md`** — Product-shaped plugin practices: CMake presets, test/measurement targets, asset/model loading, state restore, latency/tail updates, oversampled circuit-model plugins (rate policy, integer latency, bypass parameter, model revision), host validation, and release gates

## Common Patterns

### Synthesizer Plugin

Uses the `Synthesiser` framework. Override `SynthesiserVoice::renderNextBlock()` for per-voice DSP, `SynthesiserSound` for note/channel routing. See `references/plugin-lifecycle.md` for the full pattern.

### Sidechain Effect

Add a sidechain bus in the constructor:
```cpp
BusesProperties()
    .withInput  ("Input",     juce::AudioChannelSet::stereo())
    .withInput  ("Sidechain", juce::AudioChannelSet::stereo())
    .withOutput ("Output",    juce::AudioChannelSet::stereo())
```
Access in processBlock: `auto sidechain = getBusBuffer (buffer, true, 1);`

### Multiband Processing

Split into bands using `juce::dsp::LinkwitzRileyFilter<>` crossover filters, process each band independently, then sum back together.

### Custom Preset System

Store presets as XML files loaded via `juce::File` or embedded as binary data. Use `apvts.replaceState()` to load.

## Tips

- **Use `GenericAudioProcessorEditor`** for quick prototypes — it auto-generates a UI from your parameters. Just return `new GenericAudioProcessorEditor(*this)` from `createEditor()`.
- **Use `pluginval`** to validate plugins before shipping — it catches threading, state, and parameter bugs.
- **Cache `getRawParameterValue()` pointers** as members — never call it inside `processBlock()`.
- **Pre-allocate all buffers** in `prepareToPlay()`, never in `processBlock()`.
- **Use `juce::ScopedNoDenormals`** at the top of `processBlock()` to avoid performance penalties from denormal floats.
- **Attribute CPU before optimizing** — what a host's performance meter measures is host-specific. Compare the audio callback with the editor closed and open, and bypassed, before deciding whether the DSP or the UI is the problem (`references/performance-investigation.md`).
- **Set `COPY_PLUGIN_AFTER_BUILD TRUE`** in CMake for rapid iteration — plugins auto-install after each build.
- **Close your DAW before rebuilding** — DAWs lock plugin files while loaded.
