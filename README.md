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

## Run from source

Python 3.9 or newer is required.

```bash
python -m venv venv
```

Activate it (`venv\Scripts\activate` on Windows or `source venv/bin/activate` on Linux/macOS), then run:

```bash
pip install -r requirements.txt
python main.py
```

## Build a binary with PyInstaller

```bash
pip install -r requirements.txt
pyinstaller --noconfirm --clean --onefile --windowed --name CubicLantern main.py
```

The result is placed in `dist/`. Build on the target operating system. Releases contain a ready Windows installer made with Inno Setup Compiler, a portable Windows ZIP binary, and a Linux `tar.gz` binary built and tested on Linux Mint. If the Linux build does not work on another distribution, build it locally with PyInstaller.

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
| Linux | `~/.local/share/MinecraftServerMaker` |
| macOS | `~/Library/Application Support/MinecraftServerMaker` |

## Releases

- [GitHub / README](https://github.com/zoardgodor/zmcservermanager)
- [Releases / downloads](https://github.com/zoardgodor/zmcservermanager/releases)
