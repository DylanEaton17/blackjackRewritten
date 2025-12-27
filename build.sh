#!/bin/bash
# Build script for Linux/Mac standalone executable

echo "================================================"
echo " Building Blackjack Story Mode Standalone"
echo "================================================"
echo ""

echo "[1/4] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python not found. Please install Python 3.8+"
    exit 1
fi

echo ""
echo "[2/4] Installing dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[3/4] Building executable with PyInstaller..."
python3 -m PyInstaller blackjack_web.spec --clean
if [ $? -ne 0 ]; then
    echo "ERROR: Build failed"
    exit 1
fi

echo ""
echo "[4/4] Build complete!"
echo ""
echo "================================================"
echo " Executable created in: dist/BlackjackStoryMode"
echo "================================================"
echo ""
echo "Test the executable by running:"
echo "  cd dist"
echo "  ./BlackjackStoryMode"
echo ""
