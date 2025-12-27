@echo off
REM Build script for Windows standalone executable
echo ================================================
echo  Building Blackjack Story Mode Standalone
echo ================================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo.
echo [2/4] Installing dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/4] Building executable with PyInstaller...
python -m PyInstaller blackjack_web.spec --clean
if errorlevel 1 (
    echo ERROR: Build failed
    pause
    exit /b 1
)

echo.
echo [4/4] Build complete!
echo.
echo ================================================
echo  Executable created in: dist\BlackjackStoryMode.exe
echo ================================================
echo.
echo Test the executable by running:
echo   cd dist
echo   BlackjackStoryMode.exe
echo.
pause
