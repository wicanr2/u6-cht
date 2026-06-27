@echo off
REM Ultima VI 繁體中文版 v1.5.1 — Windows launcher (free / data-bring-your-own)
REM 用法：拖一個含 Ultima VI 原版資料 (CONVERSE.A, BOOK.DAT 等) 的目錄到 run.bat 上

if "%~1"=="" (
    echo Ultima VI 繁體中文版 v1.5.1
    echo.
    echo 用法：拖含原版遊戲資料的資料夾到 run.bat 上
    echo 例：把 C:\ultima6 拖到 run.bat
    echo.
    echo 請自備 Ultima VI 原版遊戲檔。
    echo GitHub: https://github.com/wicanr2/u6-cht
    pause
    exit /b 1
)

set GAMEDIR=%~1
if not exist "%GAMEDIR%\CONVERSE.A" (
    echo ERROR: %GAMEDIR% 找不到 CONVERSE.A
    echo 請確認該目錄含 Ultima VI 原版遊戲檔
    pause
    exit /b 1
)

REM Copy CHT data into game dir if not present
if not exist "%GAMEDIR%\cht_strings.tab" copy "%~dp0u6cht-data\cht_strings.tab" "%GAMEDIR%\" >nul
if not exist "%GAMEDIR%\big5_u6_12x12.fnt" copy "%~dp0u6cht-data\big5_u6_12x12.fnt" "%GAMEDIR%\" >nul

"%~dp0scummvm.exe" --extrapath="%~dp0engine-data" --path="%GAMEDIR%" ultima6
