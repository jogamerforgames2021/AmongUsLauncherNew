@echo off
setlocal enabledelayedexpansion
title Patch Toggler

set "META_DIR=Among Us_Data\il2cpp_data\Metadata"
set "ACTIVE_FILE=%META_DIR%\global-metadata.dat"
set "VANILLA_FILE=%META_DIR%\global-metadata.dat.vanilla"
set "PATCHED_FILE=%META_DIR%\global-metadata.dat.patched"

if not exist "%META_DIR%" (
    echo [ERROR] Metadata directory not found.
    echo Please place this file in the main Among Us game folder.
    echo.
    pause
    exit /b
)

:MENU
cls
echo ========================================================================
echo                             PATCH TOGGLER (For Among Us v19)
echo ========================================================================
echo Use Shadow Slime's patch to fix the itch.io login error,
echo or use vanilla if you want to play the game with untouched files.
echo ========================================================================

call :CHECK_STATUS

echo.
echo  Currently Selected: [ %CURRENT_STATUS% ]
echo.
echo  [1] Switch to Shadow Slime Patch (Itch.io Fix)
echo  [2] Switch to Vanilla (Untouched)
echo  [3] Toggle Between Both
echo  [4] Launch Among Us
echo  [5] Exit
echo.
echo ========================================================================
set /p CHOICE="Select an option (1-5): "

if "%CHOICE%"=="1" goto SET_PATCHED
if "%CHOICE%"=="2" goto SET_VANILLA
if "%CHOICE%"=="3" goto TOGGLE
if "%CHOICE%"=="4" goto LAUNCH
if "%CHOICE%"=="5" exit /b

goto MENU

:CHECK_STATUS
if not exist "%ACTIVE_FILE%" (
    set "CURRENT_STATUS=NONE / MISSING"
    exit /b
)
for %%A in ("%ACTIVE_FILE%") do set SIZE=%%~zA
if %SIZE% GTR 16700000 (
    set "CURRENT_STATUS=SHADOW SLIME PATCH (ITCH FIX)"
) else (
    set "CURRENT_STATUS=VANILLA (UNTOUCHED)"
)
exit /b

:SET_PATCHED
if not exist "%PATCHED_FILE%" (
    echo.
    echo [ERROR] global-metadata.dat.patched is missing!
    timeout /t 3 >nul
    goto MENU
)
copy /y "%PATCHED_FILE%" "%ACTIVE_FILE%" >nul
echo.
echo [+] Switched to Shadow Slime Patch.
timeout /t 2 >nul
goto MENU

:SET_VANILLA
if not exist "%VANILLA_FILE%" (
    echo.
    echo [ERROR] global-metadata.dat.vanilla is missing!
    timeout /t 3 >nul
    goto MENU
)
copy /y "%VANILLA_FILE%" "%ACTIVE_FILE%" >nul
echo.
echo [+] Switched to Vanilla Metadata.
timeout /t 2 >nul
goto MENU

:TOGGLE
call :CHECK_STATUS
if "%CURRENT_STATUS%"=="SHADOW SLIME PATCH (ITCH FIX)" (
    goto SET_VANILLA
) else (
    goto SET_PATCHED
)

:LAUNCH
echo.
echo [^>] Starting Among Us...
if exist "Among Us.exe" (
    start "" "Among Us.exe"
) else (
    echo [ERROR] Among Us.exe not found in this folder.
    pause
)
exit /b