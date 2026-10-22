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

## Futtatás forrásból Windowson

Python 3.9 vagy újabb szükséges. PowerShellben hozd létre és aktiváld a virtuális környezetet:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Windowsos bináris készítése

A projekt Windowsos buildert tartalmaz, amely friss Git-klónból is használható. Létrehozza a `.venv` virtuális környezetet, frissíti a pipet, telepíti a `requirements.txt` függőségeit, majd megkérdezi, hogy készüljön-e bináris. Választhatsz normál, ablakos vagy konzolos hibakereső változatot; a `y` vagy `yes` választól eltérő válasz után csak a telepítés készül el, a script kilép.

Windowson a `windows_build.bat` dupla kattintással, Parancssorból vagy a VS Code integrált termináljából indítható:

```bat
windows_build.bat
```

Ehhez előzetesen telepített, `py` vagy `python` parancsként elérhető Python 3.9 vagy újabb szükséges. Az elkészült alkalmazás a `dist/CubicLantern` vagy a `dist/CubicLantern-Debug` mappába kerül.

A Releases oldalon letölthető egy Inno Setup Compilerrel készített Windows-telepítő és egy telepítés nélküli Windows-bináris ZIP-ben.

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


# CubicLantern Server Manager Linuxra

Ez a mappa tartalmazza a CubicLantern Server Manager Linuxos forrását, Linuxos függőségeit és buildelőeszközeit.

## Futtatás forrásból

Python 3.9 vagy újabb szükséges. Ebből a `Linux` mappából futtasd:

```bash
./linux_build.sh
```

A script létrehozza a `Linux/.venv` virtuális környezetet, frissíti a pipet, és telepíti a `Linux/requirements.txt` függőségeit. Ha csak a forráskörnyezetet szeretnéd előkészíteni, a kérdésnél válaszolj `n`-nel.

## Linuxos bináris készítése

A `./linux_build.sh` terminálból, akár a VS Code integrált termináljából is futtatható. Git-klónozás után futtatható jogosultsággal rendelkezik. A script megkérdezi, készüljön-e build, majd normál ablakos és konzolos hibakereső változatot ajánl fel.

A normál build a `../dist/CubicLantern_linux/CubicLantern`, a debug build a `../dist/CubicLantern_linux/CubicLantern-Debug` mappába kerül. Ezek külön mappák, ezért nem írják felül a `../dist/CubicLantern` Windowsos kimenetét.

A builder Linux Minten készült és azon lett tesztelve. Ha a mellékelt Linux-kiadás más disztribúción nem működik, készíts helyi binárist ezzel a scripttel. Ha hiányzik a Python, a pip vagy a virtuális környezet támogatása, a script megkeresi a támogatott disztribúciós csomagkezelőt, elmagyarázza, miért kell rendszergazdai jogosultság, majd csak a hiányzó rendszercsomagok telepítéséhez kér `sudo` jelszót. Más disztribúción a hiányzó csomagokat a saját csomagkezelővel telepítsd, majd futtasd újra a scriptet.

## Kézi build

Az ennek megfelelő PyInstaller-parancsokat a [make_executable_from_py.txt](make_executable_from_py.txt) fájl tartalmazza.

## Adatok helye

`~/.local/share/MinecraftServerMaker`, kivéve ha az `XDG_DATA_HOME` más értékre van állítva.

## Letöltések

- [GitHub / README](https://github.com/zoardgodor/zmcservermanager)
- [Releases / letöltések](https://github.com/zoardgodor/zmcservermanager/releases)
