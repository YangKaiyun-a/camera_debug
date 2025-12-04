@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo   Thrift Multi-file Compiler for camera_debug
echo   Scanning and compiling ../thrift/*.thrift
echo ===============================================

REM Current script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%\..
set THRIFT_DIR=%PROJECT_ROOT%\thrift_interface
set OUTPUT_DIR=%THRIFT_DIR%\gen

REM Change to thrift directory
cd /d "%THRIFT_DIR%" || (
    echo [ERROR] Cannot enter thrift directory
    exit /b 1
)

REM Create gen directory
if not exist "%OUTPUT_DIR%" (
    mkdir "%OUTPUT_DIR%"
)

REM thrift.exe is placed beside this script
set THRIFT_BIN=%SCRIPT_DIR%\thrift.exe

REM Check thrift.exe exists
if not exist "%THRIFT_BIN%" (
    echo [ERROR] thrift.exe not found in script directory!
    exit /b 1
)

echo Found thrift.exe: %THRIFT_BIN%
echo.

REM Compile all .thrift files
for %%f in (*.thrift) do (
    if exist "%%f" (
        echo [Compile] %%f ...
        "%THRIFT_BIN%" -r --gen py -out "%OUTPUT_DIR%" "%%f"
        if !errorlevel! == 0 (
            echo     [OK] %%f
        ) else (
            echo     [FAILED] %%f
        )
        echo.
    )
)

REM Add __init__.py for all directories recursively
for /r "%OUTPUT_DIR%" %%d in (.) do (
    if exist "%%d" (
        if not exist "%%d\\__init__.py" (
            type nul > "%%d\\__init__.py"
        )
    )
)

echo ===============================================
echo   Thrift compile finished.
echo   Output directory:
echo   %OUTPUT_DIR%
echo ===============================================

endlocal
pause
