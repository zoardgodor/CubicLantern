# CubicLantern Server Manager for Linux

[Magyar változat](README_hu.md)

This folder contains the Linux source, Linux dependencies, and Linux build tools for CubicLantern Server Manager.

## Run from source

Python 3.9 or newer is required. From this `Linux` folder, run:

```bash
./linux_build.sh
```

The script creates `Linux/.venv`, upgrades pip, and installs `Linux/requirements.txt`. Answer `n` when prompted if you only want to prepare the source environment.

## Build a Linux binary

Run `./linux_build.sh` from a terminal, including the VS Code integrated terminal. It is executable after a Git clone. The script asks whether to build, then offers a normal windowed build and a debug build with a console.

The normal build is placed in `../dist/CubicLantern_linux/CubicLantern`. The debug build is placed in `../dist/CubicLantern_linux/CubicLantern-Debug`. These separate folders never replace the Windows output in `../dist/CubicLantern`.

The builder was created and tested on Linux Mint. If the supplied Linux release does not work on another distribution, build a local binary with this script. If Python, pip, or virtual-environment support is missing, the script detects a supported distribution package manager, explains why administrator permission is needed, and then requests `sudo` only to install the missing system packages. On another distribution, install those packages with its package manager and run the script again.

## Manual build

See [make_executable_from_py.txt](make_executable_from_py.txt) for the equivalent PyInstaller commands.

## Data location

`~/.local/share/MinecraftServerMaker`, unless `XDG_DATA_HOME` is set.
