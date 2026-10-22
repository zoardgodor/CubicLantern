# CubicLantern Server Manager Linuxra

[English version](README.md)

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
