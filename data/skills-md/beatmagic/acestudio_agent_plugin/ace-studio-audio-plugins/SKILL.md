---
name: ace-studio-audio-plugins
description: "How to drive the audio plugins ACE Studio hosts — third-party VST3/AU instruments and effects, and Studio's own built-in effects — through Studio's built-in computer use for a plugin's own interface, alongside the parameter and state/preset tools. Load whenever the user wants to load, tweak, preset or otherwise control a plugin, asks for computer use on one, or a job needs a control that exists only inside a plugin's UI. Pair with `ace-studio-features` for choosing a sound source."
---

# ACE Studio audio plugins

A hosted plugin is as drivable by you as it is by the user's hand.

ACE Studio hosts third-party instruments (VST3/AU) on MIDI tracks and
third-party or built-in effects in any track's chain. Loading one onto a track
is `ace-studio-features`' territory; this is about touching it once it is there.

Three ways in, and the choice is yours:

- **Parameters and state/presets** are the exact reach: the plugin's host
  parameters read and write directly, its preset library is yours, and whole
  state moves as bytes.
- **The plugin's own interface** is the complete reach. Studio provides
  computer use for plugins: it captures the plugin's own editor — not the
  screen — and delivers real gestures to it, with no screen-recording or
  accessibility permission and without moving the user's cursor. This is what
  reaches controls that live only in the UI — loading a Kontakt library, mic
  positions, a deep menu, a plugin's internal preset browser.

Prefer Studio's channel over a general computer-use tool your harness may
offer: it is scoped to the plugin's editor rather than the whole desktop, and
it is the surface the plugin was hosted into.

Per-plugin knowledge — which controls matter, canonical editor sizes, UI quirks
— is a worked recipe under this skill's `references/` folder. Read the plugin's
recipe when one exists before driving the plugin.

The surface's docs carry the exact verbs, arguments and errors.
