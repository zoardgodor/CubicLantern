# CubicLantern Server Manager

[Magyar változat](README_hu.md)

CubicLantern Server Manager is a PySide6 application for creating, configuring and running Minecraft Java, Bedrock and PumpkinMC servers.

## Features

- Vanilla, Paper, Purpur, Fabric, Forge, NeoForge, Bedrock and PumpkinMC server creation.
- Automatic Java, server and Bedrock downloads.
- Server properties editor, world manager, player management, mods and plugins.
- PumpkinMC is marked as recommended for low-end computers.
- Playit and Pinggy tunnels can run separately or at the same time.
- Playit keeps a stable address. Its free plan can have higher latency; a subscription is suited to long-running servers.
- Pinggy needs no account and is simple for short sessions. Three free tunnels can run at once, but a new address is generated every 60 minutes.
- TCP, UDP/Bedrock and HTTP Pinggy tunnels with editable local ports. All start without a password.
- Each selected Pinggy tunnel opens in its own CMD or terminal window without interactive confirmation.
- Pinggy is supervised for the 60-minute free-plan limit. It restarts automatically if the launcher or all tunnel processes stop, sends optional `/say` warnings at 10 and 5 minutes, and has a manual restart button that resets the timer.
- Simple Voice Chat guidance explains where to put the public UDP address and port. Playit is convenient for SVC because its address stays stable.
- English (default) and Hungarian interface.

## Run from source on Windows

Python 3.9 or newer is required. Create and activate a virtual environment in PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Build a Windows binary

The repository includes a Windows builder that works from a fresh Git clone. It creates a `.venv` virtual environment, upgrades pip, installs `requirements.txt`, then asks whether to build an executable. Choose a normal windowed build or a debug build with a console; choosing anything other than `y`/`yes` ends after setup.

On Windows, run `windows_build.bat` by double-clicking it, from Command Prompt, or from the VS Code integrated terminal:

```bat
windows_build.bat
```

Python 3.9 or newer must already be installed and available as `py` or `python`. Built applications are placed in `dist/CubicLantern` or `dist/CubicLantern-Debug`.

Releases contain a ready Windows installer made with Inno Setup Compiler and a portable Windows ZIP binary.

## Tunnel selection

Playit and Pinggy are configured separately, so they can be used at the same time. The Pinggy editor has three rows, allowing multiple TCP, UDP or HTTP tunnels. The default Java tunnel is TCP on port 25565; the default Bedrock tunnel is UDP on port 19133. HTTP defaults to local port 8000. The local port must match the server or web service you want to expose.

For Simple Voice Chat, use a separate UDP tunnel and enter its public host and port in the `voice_host` and `port` fields of the Simple Voice Chat mod/plugin configuration, or the equivalent fields in your version. If the Pinggy address changes, update the configuration and restart the server. Playit is preferable for SVC when a stable address is important.

## Third-party services and legal notice

CubicLantern can launch [Playit](https://playit.gg/) and [Pinggy](https://pinggy.io/), but it is an independent, unofficial project. CubicLantern is not affiliated with, endorsed by, sponsored by, or an official partner of Playit or Pinggy. These services are third-party services and their names and trademarks belong to their respective owners. This integration is not advertising.

The Playit agent is downloaded from the official `playit-cloud/playit-agent` release repository. Pinggy is not bundled with CubicLantern; users download the appropriate client from the official [Pinggy CLI page](https://pinggy.io/cli/) and import it into the application. Use both services according to their own terms and acceptable-use policies.

## Data location

| OS | Path |
|---|---|
| Windows | `%APPDATA%\MinecraftServerMaker` |

# CubicLantern Server Manager for Linux

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

## Releases

- [GitHub / README](https://github.com/zoardgodor/zmcservermanager)
- [Releases / downloads](https://github.com/zoardgodor/zmcservermanager/releases)