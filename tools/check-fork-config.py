#!/usr/bin/env python3
"""Validate fork-specific configuration without Unity. Not a compile test."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []

def read(path: str) -> str:
    p = ROOT / path
    if not p.is_file():
        errors.append(f"Missing file: {path}")
        return ""
    return p.read_text(encoding="utf-8-sig")

def expect(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)

def constant(source: str, key: str) -> str:
    match = re.search(r"public const (?:string|int) " + re.escape(key) + r" = (?:\"([^\"]+)\"|(\d+));", source)
    if not match:
        errors.append(f"Missing constant: {key}")
        return ""
    return match.group(1) or match.group(2)

release = read("Assets/Scripts/OpenFusion/Api/PocketRelease.cs")
project = read("ProjectSettings/ProjectSettings.asset")
setup = read("Assets/Editor/OpenFusionProject.cs")
launcher = read("Assets/Scripts/OpenFusion/Screens/LauncherScreen.cs")
graphics = read("Assets/Scripts/OpenFusion/World/GraphicsFx.cs")
options = read("Assets/Scripts/OpenFusion/World/GameOptions.cs")
settings = read("Assets/Scripts/OpenFusion/World/SettingsWindow.cs")
updater_tests = read("Assets/Editor/UpdaterRegressionChecks.cs")
manifest = read("tests/android-panel/AndroidManifest.xml")
deploy = read("tools/deploy_apk.bat")
prepare = read("tools/prepare-release.ps1")
readme = read("README.md")
read("LICENSE")
read("NOTICE")
read("CREDITS.md")

expected_repo = "https://github.com/bat221k-creator/OpenFusion-Pocket"
expected_pkg = "com.bat221k.fusionfall.android"
expect(constant(release, "Repository") == expected_repo, "Release repository points elsewhere")
expect(constant(release, "LatestApi") == "https://api.github.com/repos/bat221k-creator/OpenFusion-Pocket/releases/latest", "Latest release API points elsewhere")
expect(constant(release, "Package") == expected_pkg, "Android package is not fork-isolated")
expect('path.StartsWith("/bat221k-creator/OpenFusion-Pocket/releases/"' in release, "Trusted update-path validation points elsewhere")
version = constant(release, "AppVersion")
code = constant(release, "BuildCode")
expect(re.fullmatch(r"\d+\.\d+(?:\.\d+)?", version) is not None, "Invalid Android version")
expect(code.isdigit() and int(code) >= 1, "Invalid Android build code")
expect(f"bundleVersion: {version}" in project, "Unity project version does not match release constants")
expect(f"AndroidBundleVersionCode: {code}" in project, "Unity Android build code does not match")
expect(f"Android: {expected_pkg}" in project, "Unity Android application ID does not match")
expect("productName: FusionFall Android" in project, "Project display name not configured")
expect('PlayerSettings.SetApplicationIdentifier(a, OpenFusion.Api.PocketRelease.Package)' in setup, "Unity build setup must use fork package constant")
expect('PlayerSettings.productName = "FusionFall Android"' in setup, "Unity build resets product name")
expect("package = $packageId" in prepare, "Release generation must use configured Android package")
expect(f"android:targetPackage=\"{expected_pkg}\"" in manifest, "Android instrumentation target points at upstream")
expect(f"monkey -p {expected_pkg}" in deploy, "ADB deploy helper launches upstream package")
expect('PocketRelease.Package + ".updates"' in updater_tests, "APK provider test uses hard-coded upstream package")
expect('"GitHub: bat221k-creator/OpenFusion-Pocket"' in launcher, "Launcher About link points elsewhere")
expect('"About FusionFall Android"' in launcher, "Launcher About title not updated")
expect("static readonly int[] FpsVals = { 30, 40, 60, -1 };" in launcher, "Launcher FPS options missing 40")
expect("static readonly int[] FpsVals = { 30, 40, 60, -1 };" in graphics, "Runtime FPS options missing 40")
expect('new[] { "30 FPS", "40 FPS", "60 FPS", "Unlimited" }' in launcher, "Launcher FPS buttons missing 40")
expect('FpsNames = { "30", "40", "60", "MAX" }' in settings, "Advanced Graphics FPS buttons missing 40")
expect("Mathf.Clamp(o.Fps, 0, 3)" in graphics, "Runtime FPS index range incorrect")
expect('PlayerPrefs.GetInt("of_set_fps", Application.isMobilePlatform ? 0 : 2), 0, 3' in options, "Saved FPS index range incorrect")
expect("Original" in readme and "NOTICE" in readme, "Upstream attribution is not documented")

if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    sys.exit(1)
print(f"PASS: FusionFall Android {version} (build {code}), {expected_pkg}, independent release channel, 40 FPS controls, source notices")
print("NOTE: Static preflight only — Unity compilation and device tests still required.")
