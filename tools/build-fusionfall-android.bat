@echo off
setlocal
cd /d "%~dp0.."
echo Starting FusionFall Android v0.1 local Unity build...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0build-fusionfall-android.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" (
  echo BUILD FAILED - Check Logs\unity-compile.log or Logs\unity-release.log.
) else (
  echo BUILD SUCCESSFUL - Open the Builds folder for the APK.
)
echo.
pause
exit /b %RESULT%
