# FusionFall Android one-click local APK build (Windows PowerShell).
# Uses the existing upstream tools/unity-build.ps1; does not require Python or Git.
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $project

$versionPath = Join-Path $project 'ProjectSettings\ProjectVersion.txt'
$buildTool = Join-Path $PSScriptRoot 'unity-build.ps1'
$releaseFile = Join-Path $project 'Assets\Scripts\OpenFusion\Api\PocketRelease.cs'
$expectedEditor = '2022.3.62f3'
Write-Host ''
Write-Host '=== FusionFall Android - Local APK Builder ===' -ForegroundColor Cyan
Write-Host "Project: $project"
if (-not (Test-Path $versionPath) -or -not (Test-Path $buildTool) -or -not (Test-Path $releaseFile)) {
    throw 'Missing Unity source project files. Run this from the extracted repository folder.'
}
$projectVersion = Get-Content -Raw -LiteralPath $versionPath
if ($projectVersion -notmatch [regex]::Escape($expectedEditor)) {
    throw "Expected Unity $expectedEditor. Check ProjectSettings/ProjectVersion.txt."
}
$source = Get-Content -Raw -LiteralPath $releaseFile
$version = [regex]::Match($source, 'public const string AppVersion = "([0-9.]+)"').Groups[1].Value
$package = [regex]::Match($source, 'public const string Package = "([^"]+)"').Groups[1].Value
if (-not $version -or $package -ne 'com.bat221k.fusionfall.android') {
    throw 'This is not the configured FusionFall Android development fork. Do not build the upstream package here.'
}
$roots = @(
    "$env:ProgramFiles\Unity\Hub\Editor\$expectedEditor\Editor\Unity.exe",
    "${env:ProgramFiles(x86)}\Unity\Hub\Editor\$expectedEditor\Editor\Unity.exe",
    "$env:LOCALAPPDATA\Unity\Hub\Editor\$expectedEditor\Editor\Unity.exe"
)
$unity = $roots | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $unity) {
    Write-Host "Unity $expectedEditor not found. Install it via Unity Hub with Android Build Support, SDK, NDK and OpenJDK." -ForegroundColor Yellow
    throw 'Unity editor missing.'
}
Write-Host "Unity: $unity"
$started = Get-Date
Write-Host ''
Write-Host '[1/2] Compiling and checking project scripts...' -ForegroundColor Cyan
& $buildTool -Task compile -Project $project -UnityPath $unity
if ($LASTEXITCODE -ne 0) { throw "Unity compile check failed ($LASTEXITCODE). See Logs\unity-compile.log." }
Write-Host ''
Write-Host '[2/2] Building Android APK (IL2CPP)...' -ForegroundColor Cyan
& $buildTool -Task release -Project $project -UnityPath $unity
if ($LASTEXITCODE -ne 0) { throw "Unity APK build failed ($LASTEXITCODE). See Logs\unity-release.log." }
$sourceApk = Join-Path $project 'Builds\OpenFusion-release.apk'
if (-not (Test-Path $sourceApk)) { throw 'Build reported success but expected Builds/OpenFusion-release.apk was not found.' }
if ((Get-Item $sourceApk).LastWriteTime -lt $started.AddSeconds(-3)) {
    throw 'The APK is older than this build attempt; refusing to treat a stale file as a new success.'
}
$targetApk = Join-Path $project "Builds\FusionFall-Android-v$version.apk"
Copy-Item -LiteralPath $sourceApk -Destination $targetApk -Force
$hash = (Get-FileHash -LiteralPath $targetApk -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host ''
Write-Host 'BUILD FINISHED - APK CREATED' -ForegroundColor Green
Write-Host "APK: $targetApk"
Write-Host "SHA-256: $hash"
Write-Host "Expected package: $package (verify with aapt before installation)"
Write-Host 'The APK is a local development build; it has NOT been tested on the Retroid yet.'
