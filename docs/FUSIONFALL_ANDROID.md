# FusionFall Android v0.1 — fork development

This is a **development fork of [OpenFusion:Pocket](https://github.com/rsigristc/OpenFusion-Pocket)**, initially targeting native Android play on a Retroid Pocket G2 Gen 2 and the Retrobution server. It is **not** a separate server and is not affiliated with Cartoon Network, OpenFusion or Retrobution.

## Status

- Branch: `fusionfall-android-v0.1`; upstream baseline: `1941918bc697c9ff8ebea18ec8339de1bb44330d`.
- Android application ID: `com.bat221k.fusionfall.android`, separate from upstream's `com.openfusion.android`.
- App title: **FusionFall Android**; version `0.1.0`, build code `1`.
- Update checks: scoped to `bat221k-creator/OpenFusion-Pocket`. No in-app updates will be available until this fork has its own signed, correctly named release and valid update manifest.
- Frame rate settings: 30 / **40** / 60 / unlimited, accessible from launcher and in-game Advanced Graphics. Mobile default remains 30 FPS. A 40 FPS *cap* does not guarantee the device can sustain 40 FPS.
- Native gamepad features, Retrobution networking, launcher and game content loading remain inherited from upstream. Device support and compatibility are **not yet verified** for the Retroid G2 Gen 2.
- **No Unity compile, APK build, performance benchmark or hardware test has been completed for this fork.**

## Local build

1. Install **Unity Hub** and **Unity 2022.3.62f3** with **Android Build Support**, SDK, NDK and OpenJDK.
2. Clone this fork and check out `fusionfall-android-v0.1`.
3. Before Unity, run `python tools/check-fork-config.py` (or `python3`) to check configuration consistency; this is not a Unity compilation test.
4. From PowerShell in the project root, run `.\tools\unity-build.ps1 compile` to validate C# compilation and then `.\tools\unity-build.ps1 release` for `Builds/OpenFusion-release.apk`. The filename is inherited from upstream.
5. Check `Logs/unity-release.log` for errors. Verify the signed APK's Android package is `com.bat221k.fusionfall.android` before installation.
6. Install through ADB with `adb install -r Builds/OpenFusion-release.apk` and launch through the Android app icon.

The existing upstream PowerShell build script is Windows-oriented. A full native APK build requires an installed Unity editor and an appropriately licensed build environment; a GitHub source commit alone does not produce an APK.

## Retroid G2 Gen 2 test plan

- Launch and resource download using Retrobution, then verify login, world entry, movement, camera, combat and logout.
- Confirm the built-in gamepad handles both sticks, shoulder buttons, A/B, D-pad and the in-game UI cursor without phantom inputs.
- Try 30, 40 and 60 FPS caps; measure actual device frame time, heat, CPU/GPU load and battery impact. A 60 Hz display may not pace 40 FPS evenly.
- Confirm graphics changes persist and the app does not interfere with the original OpenFusion:Pocket installation or its cache.
- Check that About and Update links go to the fork and that there is no accidental automatic installation of upstream releases.
- Collect Unity `logcat` and app diagnostics for crashes. Never upload account credentials, secret tokens or private logs.

## Release and attribution

Keep the original `LICENSE`, `NOTICE` and `CREDITS.md`. The source project's MIT licensing **does not** cover all game artwork, legacy resources, third-party materials or trademarks. Do not bundle additional proprietary game resources into the repository. Use a private signing key, never commit it, and verify the matching signing certificate for future Android updates.

The initial configuration CI only checks source alignment and **does not prove a successful Unity build**. Publishing a release must wait for a compiled, signed and device-tested APK.
