# CubicLantern Server Manager

[English version](README.md)

A CubicLantern Server Manager egy PySide6-alapú alkalmazás Minecraft Java-, Bedrock- és PumpkinMC-szerverek létrehozásához, beállításához és futtatásához.

## Funkciók

- Vanilla, Paper, Purpur, Fabric, Forge, NeoForge, Bedrock és PumpkinMC szerver létrehozása.
- Java-, szerver- és Bedrock-fájlok automatikus letöltése.
- `server.properties` szerkesztő, világkezelő, játékoskezelő, mod- és pluginkezelés.
- A PumpkinMC a gyenge gépekre javasolt szervertípusként jelenik meg.
- Playit és Pinggy tunnel külön vagy egyszerre is futtatható.
- A Playit címe stabilan megmarad. Az ingyenes verziónál több ping fordulhat elő; hosszú ideig futó szerverhez az előfizetés való.
- A Pinggy fiók nélkül, egyszerűen használható rövid alkalmakhoz. Ingyenesen egyszerre három tunnel futtatható, de 60 percenként új cím készül.
- Pinggy TCP-, UDP/Bedrock- és HTTP-tunnel, szerkeszthető helyi porttal. Mindegyik jelszó nélkül indul.
- Minden kiválasztott Pinggy-tunnel saját CMD- vagy terminálablakban indul, interaktív megerősítés nélkül.
- A Pinggy-folyamatot az alkalmazás felügyeli a 60 perces ingyenes limit miatt. Leálláskor automatikusan újraindul, opcionálisan `/say` üzenetet küld 10 és 5 perccel a lejárat előtt, és van kézi újraindító gomb is, amely visszaállítja az időzítőt.
- A Simple Voice Chat beállításához útmutató mutatja, hová kell beírni a nyilvános UDP-címet és portot. SVC-hez kényelmes a Playit, mert a címe stabil.
- Angol (alapértelmezett) és magyar felület.

## Futtatás forrásból

Python 3.9 vagy újabb szükséges.

```bash
python -m venv venv
```

Aktiváld a környezetet (`venv\Scripts\activate` Windowson vagy `source venv/bin/activate` Linuxon/macOS-en), majd:

```bash
pip install -r requirements.txt
python main.py
```

## Bináris készítése PyInstallerrel

```bash
pip install -r requirements.txt
pyinstaller --noconfirm --clean --onefile --windowed --name CubicLantern main.py
```

Az eredmény a `dist/` mappába kerül. A fordítást azon az operációs rendszeren végezd, ahol használni fogod. A Releases oldalon letölthető egy Inno Setup Compilerrel készített Windows-telepítő, egy telepítés nélküli Windows-bináris ZIP-ben, valamint egy Linux Minten elkészített és tesztelt `tar.gz` bináris. Ha a Linux-változat más disztribúción nem működik, ott helyben készíts binárist PyInstallerrel.

## Tunnel kiválasztása

A Playit és a Pinggy külön állítható be, ezért egyszerre is használhatók. A Pinggy szerkesztője három sort tartalmaz, így több TCP-, UDP- vagy HTTP-tunnel is létrehozható. Az alapértelmezett Java-tunnel TCP a 25565-ös porton, az alapértelmezett Bedrock-tunnel UDP a 19133-as porton. A HTTP alapértelmezett helyi portja 8000. A helyi portnak egyeznie kell a megosztani kívánt szerver vagy webszolgáltatás portjával.

Simple Voice Chathez külön UDP-tunnelt használj, majd írd be a nyilvános címet és portot a mod/plugin konfigurációjának `voice_host` és `port` mezőibe, vagy a verziódnak megfelelő mezőkbe. Pinggy esetén új cím generálásakor a konfigurációt frissíteni és a szervert újraindítani kell. Stabil SVC-címhez a Playit praktikusabb.

## Külső szolgáltatások és jogi tájékoztató

A CubicLantern képes elindítani a [Playitet](https://playit.gg/) és a [Pinggyt](https://pinggy.io/), de független, nem hivatalos projekt. A CubicLantern nem áll kapcsolatban a Playittel vagy a Pinggyvel, nem hivatalos partnerük, nem támogatják és nem szponzorálják. A szolgáltatások külső szolgáltatások, neveik és védjegyeik a saját tulajdonosaikhoz tartoznak. Ez az integráció nem reklám.

A Playit agentet a hivatalos `playit-cloud/playit-agent` kiadási tárhelyről tölti le az alkalmazás. A Pinggy nincs beépítve a CubicLanternbe; a felhasználó a hivatalos [Pinggy CLI oldalról](https://pinggy.io/cli/) tölti le a megfelelő klienst, majd importálja az alkalmazásba. Mindkét szolgáltatást a saját felhasználási feltételeik és elfogadható használati szabályaik szerint használd.

## Adatok helye

| Rendszer | Útvonal |
|---|---|
| Windows | `%APPDATA%\MinecraftServerMaker` |
| Linux | `~/.local/share/MinecraftServerMaker` |
| macOS | `~/Library/Application Support/MinecraftServerMaker` |

## Letöltések

- [GitHub / README](https://github.com/zoardgodor/zmcservermanager)
- [Releases / letöltések](https://github.com/zoardgodor/zmcservermanager/releases)
