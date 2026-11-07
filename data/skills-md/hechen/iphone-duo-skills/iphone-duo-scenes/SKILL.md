---
name: iphone-duo-scenes
description: Implement or review iPhone Duo multiple windows and Split View scenes, hinge-driven interactions (onHingeChange, UIHingeInteraction), and scene accessories such as CameraCaptureAccessory on the outer display, with explicit state ownership and handling for capability changes. Use when an app opens a second window, requests new scenes, reacts to the hinge angle or fold status, or shows content on the outer display while capturing on the inner display.
license: MIT
---

# iPhone Duo scenes and interactions

Read [scenes evidence](references/scenes.md). Choose the relevant mode; an app that needs resizing does not automatically need hinge effects or a second-display experience. The hinge and camera-capture accessory APIs need the iOS 27.1 SDK.

## Multiple scenes

Map app-shared data, document state, and scene-local presentation separately. A route or selected tab in one window should not unintentionally navigate another. Two windows editing the same document need a deliberate consistency model. Do not treat an open inner display as the iPad idiom, and do not assume a size change creates a new scene or document.

Follow existing storage and synchronization boundaries. Give new-scene requests a meaningful document or route identity. New windows cannot be created from the outer display, so handle request failure without discarding the user's current work, and prefer the system activation action that hides itself when a new window is unavailable. Restore scene presentation without duplicating an in-progress operation.

## Hinge interaction

Use hinge input only for an interaction that benefits from it; use reserved regions and arrangements for layout. The hinge can be absent, and it goes away when the view leaves a hierarchy that reports it. Define a neutral state for that case and a touch or other accessible way to perform the essential task. Prefer the hinge status when closed, partially open, or fully open is all you need. Do not depend on a particular update rate or angle precision. Keep continuous input out of persistence and expensive work; bound updates and cancel obsolete effects.

## Scene accessories

A scene accessory is optional content the system presents; registration does not make it appear. Separate the person's choice to show it from the system's availability, and update the UI when either changes. Attach the camera-capture accessory to the view or view controller that shows the capture interface, keep essential controls in that interface, and share the existing capture model instead of passing messages.

Define precisely what the outward-facing display shows. Use a purpose-specific presentation model so private editor controls or unrelated document data are not mirrored to the person in front of the camera. This is a product data-boundary decision, not a reason to add a generic permission flow.

## Verify

Exercise two scenes independently, a failed scene request on the outer display, accessory availability loss and recovery, the user turning accessory content off, and an absent hinge where relevant. Record continuity and cleanup results, plus the exact SDK and runtime tested. Accessory presentation that depends on the camera needs a device. Do not infer arbitrary access to both displays from their physical existence.
