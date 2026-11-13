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

## Easiest first build — Windows PC (no Git or Python installation required)

1. Download and sign into **Unity Hub** from https://unity.com/download. Activate your Unity Personal license in Hub if eligible.
2. Install **Unity 2022.3.62f3**, not another 2022.3 build: https://unity.com/releases/editor/whats-new/2022.3.62f3
3. In Unity Hub, include **Android Build Support** with child modules **Android SDK & NDK Tools** and **OpenJDK**. Those components are required for the project.
4. Open the development branch: https://github.com/bat221k-creator/OpenFusion-Pocket/tree/fusionfall-android-v0.1 . Choose **Code → Download ZIP**, unzip to a normal local directory (for example `C:\GamesDev\FusionFallAndroid`). Do not double-click the script inside a compressed ZIP.
5. In the unzipped directory double-click `tools/build-fusionfall-android.bat`. It invokes the existing upstream Unity command-line build method for a compile check and Android release build, then copies the new APK as `Builds/FusionFall-Android-v0.1.0.apk`. The console stays open to display errors.
6. If the build fails, provide `Logs/unity-compile.log` or `Logs/unity-release.log` (review for personal data first). No account password, Unity license, game login, or signing key should be uploaded.

The script does not grant ChatGPT remote computer access; source changes are made via the connected GitHub repo, while your own PC executes Unity. A compiled APK has not yet been verified.

## Optional GitHub-hosted Unity builds

The manually triggered workflow at `.github/workflows/fusionfall-android-apk.yml` uses GameCI Unity Builder v4, Unity 2022.3.62f3, Android IL2CPP, and `OpenFusion.EditorTools.FusionFallCiBuild.BuildAndroid`. It is intentionally **not auto-triggered** to avoid accidental billable GitHub Actions runs or license errors.

GameCI's current licensing guidance: https://game.ci/docs/github/activation/ . GitHub repository **Settings → Secrets and variables → Actions** is where the account owner must enter any needed `UNITY_LICENSE` (Personal license file) or `UNITY_SERIAL` (supported Pro entitlement), plus `UNITY_EMAIL` and `UNITY_PASSWORD`. Do not put credentials in source code, screenshots, chat messages or workflows. GameCI warns that Unity Personal license file provisioning may be inconsistent; a local Unity Hub-activated Windows build is the recommended first path. Review licensing and account security before choosing third-party CI.

**GitHub caveat:** A `workflow_dispatch` workflow normally must exist on the repository's default branch before the GitHub Actions **Run workflow** control appears. This development workflow is intentionally kept in a separate branch pending review; it may therefore not be clickable in the UI yet. Do **not** merge an untested release just to start cloud builds. Local compilation and hardware testing come first.
