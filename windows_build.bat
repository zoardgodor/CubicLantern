@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if not errorlevel 1 (
    set "PYTHON=py -3"
) else (
    where python >nul 2>nul
    if errorlevel 1 goto python_missing
    set "PYTHON=python"
)

%PYTHON% -c "import sys; raise SystemExit(sys.version_info < (3, 9))"
if errorlevel 1 goto python_unsupported

if not exist ".venv\Scripts\python.exe" (
    echo Creating .venv...
    %PYTHON% -m venv .venv
    if errorlevel 1 goto error
)

echo Upgrading pip...
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto error

echo Installing dependencies from requirements.txt...
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto error

set "BUILD="
set /p "BUILD=Build an executable now? [y/N]: "
if /I "%BUILD%"=="Y" goto choose_build
if /I "%BUILD%"=="YES" goto choose_build
echo Setup complete. No executable was built.
goto end

:choose_build
set "BUILD_TYPE="
set /p "BUILD_TYPE=Choose build type: [1] normal windowed, [2] debug console: "
if "%BUILD_TYPE%"=="1" goto normal_build
if "%BUILD_TYPE%"=="2" goto debug_build
echo Invalid build type. No executable was built.
goto error

:normal_build
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onedir --windowed --collect-all winpty --icon=icon-CL-icon-pack\icon-CL.ico --name CubicLantern main.py
if errorlevel 1 goto error
echo Build complete: dist\CubicLantern
goto end

:debug_build
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onedir --console --collect-all winpty --icon=icon-CL-icon-pack\icon-CL.ico --name CubicLantern-Debug main.py
if errorlevel 1 goto error
echo Build complete: dist\CubicLantern-Debug
goto end

:python_missing
echo Python 3.9 or newer was not found. Install it from https://www.python.org/downloads/ and run this script again.
goto error

:python_unsupported
echo Python 3.9 or newer is required. Install a supported version and run this script again.
goto error

:error
echo The setup or build did not complete.

:end
pause
endlocal
