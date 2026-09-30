---
name: ipad-headless-display
description: Set up an Apple Silicon Mac mini as a headless computer whose only usable display is an iPad or iPhone over one USB-C or Lightning data cable, using the free OpenDisplay sender and iPad/iPhone receiver.
metadata:
  short-description: Use an iPad or iPhone as the only display for a headless Mac mini
---

# iPad/iPhone headless Mac display

Use this workflow when a user wants to operate a Mac mini with no permanent monitor and an iPad or iPhone as the sole visible display. The preferred free solution is OpenDisplay: its Mac sender creates a `CGVirtualDisplay`, captures that virtual surface, and streams it to the iPad or iPhone receiver over USB. It is not a native monitor connection.

## Requirements

- Mac running macOS 14 or newer (Apple Silicon is preferred).
- iPad or iPhone running iPadOS or iOS 15 or newer.
- OpenDisplay sender on the Mac and receiver on the iPad or iPhone. Use the App Store receiver when available; otherwise use the official TestFlight invitation or build from source with the user's Apple ID.
- A USB-C/Lightning cable that supports data and trust pairing. Do not use a charge-only cable, hub, or unreliable adapter.
- macOS Screen Recording permission for OpenDisplay. Grant Accessibility permission if touch and scroll input are wanted.

## Fast start for a new user

Give the user both receiver paths immediately:

- App Store receiver: https://apps.apple.com/app/id6754265378
- Official TestFlight invitation: https://testflight.apple.com/join/3NYaY11c

If the App Store reports that the app is unavailable in the user's country, use the TestFlight link. If TestFlight is unavailable too, use the project's Xcode build instructions with the user's Apple ID; do not tell the user to change their Apple Account region just for this setup.

## Setup sequence

1. Keep a physical monitor connected for initial setup and recovery.
2. Install an OpenDisplay sender from an operator-approved, immutable release artifact. Verify its checksum and Apple signature before placing it in `/Applications`; do not run an unverified download.
3. Open OpenDisplay on the iPad or iPhone, connect the data cable directly, unlock the iPad or iPhone, accept “Trust This Computer,” and keep the receiver in the foreground.
4. Grant Screen Recording and Accessibility permissions on the Mac. If macOS does not show a prompt, open System Settings → Privacy & Security and add/enable OpenDisplay in Screen Recording and Accessibility.
5. In the OpenDisplay connection menu select the iPad or iPhone, then choose **Extend**. Confirm the status says `Extending to iPad` and the log contains `virtual display created` followed by `mode extend`.
6. Test moving a window onto the iPad and confirm the iPad or iPhone updates live.
7. Configure the sender to launch at login if needed. Keep FileVault and pre-boot authentication enabled by default. Do not enable automatic login or weaken disk protection as part of this workflow; treat any exception as a separately approved security decision. Prevent sleep while the display is off.
8. Unplug only the physical monitor cable. Keep the iPad or iPhone data cable connected. The Mac's virtual OpenDisplay monitor is now the sole usable display.

## Critical distinction

Never use **Mirror** for the headless final state. Mirror captures the physical monitor; when that monitor is unplugged, ScreenCaptureKit can fail with `Failed to find any displays or windows to capture` and the iPad or iPhone freezes on its last frame. Extend creates an independent virtual monitor and survives removal of the physical monitor.

The USB-C cable must remain connected after the monitor is removed. The cable carries the OpenDisplay stream; it does not make the iPad appear as a native monitor in System Settings.

## Verification

Verify the actual end state rather than relying on a successful connection message:

- OpenDisplay log shows `Extending to iPad`, not `Mirroring to iPad`.
- The iPad updates after a new window is opened or moved.
- With the physical monitor unplugged, the iPad or iPhone remains live and macOS continues to create the OpenDisplay virtual surface.
- A reconnect does not repeatedly show `Network is down`, `Connection lost`, or `Failed to find any displays or windows to capture`.

If USB repeatedly connects and drops, reconnect directly with a known-good data cable, avoid hubs, unlock the iPad or iPhone, reopen the receiver, and restart OpenDisplay. Wi-Fi is a fallback only on a private network where Bonjour/local-device traffic is allowed; café Wi-Fi commonly blocks that traffic.

For a frozen iPad, reconnect the physical monitor temporarily, reconnect the iPad cable, reopen both OpenDisplay apps, select **Extend** again, and wait for `Extending to iPad` before removing the monitor. Never unplug the iPad cable when the Mac is headless.

## References

- OpenDisplay project and requirements: https://opendisplay.app/
- OpenDisplay implementation and quick start: https://github.com/peetzweg/opendisplay
- Apple Sidecar is a separate extend/mirror feature and is not the headless mechanism: https://support.apple.com/guide/ipad/use-your-ipad-as-a-second-display-ipad2b1aa3be/27/ipados/27
