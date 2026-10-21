#!/usr/bin/env bash

set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 1
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)" || exit 1
cd "$SCRIPT_DIR" || exit 1

install_python_packages() {
    echo "Python 3, pip, and virtual-environment support are required to continue."
    echo "Administrator permission is requested only to install these missing system packages."

    if ! command -v sudo >/dev/null 2>&1; then
        echo "sudo is required to install the missing packages. Install Python 3, pip, and venv with your distribution package manager, then run this script again."
        exit 1
    fi

    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3 python3-pip
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --needed python python-pip
    elif command -v zypper >/dev/null 2>&1; then
        sudo zypper --non-interactive install python3 python3-pip
    else
        echo "No supported package manager was found. Install Python 3, pip, and venv with your distribution package manager, then run this script again."
        exit 1
    fi
}

if ! command -v python3 >/dev/null 2>&1; then
    install_python_packages || exit 1
fi

if ! python3 -m venv --help >/dev/null 2>&1; then
    install_python_packages || exit 1
fi

if ! python3 -c 'import sys; raise SystemExit(sys.version_info < (3, 9))'; then
    echo "Python 3.9 or newer is required. Install a supported Python version with your distribution package manager, then run this script again."
    exit 1
fi

if [ ! -d .venv ]; then
    echo "Creating .venv..."
    python3 -m venv .venv || exit 1
fi

VENV_PYTHON=".venv/bin/python"
DIST_ROOT="$PROJECT_ROOT/dist/CubicLantern_linux"
BUILD_ROOT="$SCRIPT_DIR/build"
ICON_PATH="$PROJECT_ROOT/icon-CL-icon-pack/icon-CL.ico"

if [ ! -x "$VENV_PYTHON" ]; then
    echo "The virtual environment is incomplete. Remove Linux/.venv and run this script again."
    exit 1
fi

echo "Upgrading pip..."
"$VENV_PYTHON" -m pip install --upgrade pip || exit 1

echo "Installing dependencies from requirements.txt..."
"$VENV_PYTHON" -m pip install -r requirements.txt || exit 1

read -r -p "Build an executable now? [y/N]: " BUILD
case "$BUILD" in
    [Yy]|[Yy][Ee][Ss]) ;;
    *) echo "Setup complete. No executable was built."; exit 0 ;;
esac

read -r -p "Choose build type: [1] normal windowed, [2] debug console: " BUILD_TYPE
case "$BUILD_TYPE" in
    1)
        BUILD_NAME="CubicLantern"
        BUILD_MODE="--windowed"
        ;;
    2)
        BUILD_NAME="CubicLantern-Debug"
        BUILD_MODE="--console"
        ;;
    *)
        echo "Invalid build type. No executable was built."
        exit 1
        ;;
esac

"$VENV_PYTHON" -m PyInstaller --noconfirm --clean --onedir "$BUILD_MODE" --icon="$ICON_PATH" --name "$BUILD_NAME" --distpath "$DIST_ROOT" --workpath "$BUILD_ROOT" --specpath "$BUILD_ROOT" main_linux.py || exit 1

echo "Build complete: $DIST_ROOT/$BUILD_NAME"
