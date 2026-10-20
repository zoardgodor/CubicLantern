import sys
import os
import re
import json
import time
import shutil
import socket
import struct
import zipfile
import tarfile
import hashlib
import uuid
import platform
import secrets
import subprocess
import shlex
import threading
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QProcess, QProcessEnvironment, QTimer, QUrl, QObject, QSize
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QStackedWidget, QDialog, QDialogButtonBox, QLineEdit,
    QComboBox, QCheckBox, QSpinBox, QTabWidget, QScrollArea, QFormLayout, QPlainTextEdit,
    QProgressBar, QMessageBox, QFileDialog, QFrame, QGroupBox, QButtonGroup
)

try:
    import psutil
except ImportError:
    psutil = None


def adatmappakeresese():
    if os.name == "nt":
        alap = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
    elif sys.platform == "darwin":
        alap = str(Path.home() / "Library" / "Application Support")
    else:
        alap = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(alap) / "MinecraftServerMaker"


adatmappa = adatmappakeresese()
szerverekmappa = adatmappa / "servers"
javamappa = adatmappa / "java"
playitmappa = adatmappa / "playit"
pinggymappa = adatmappa / "pinggy"
beallitasfajl = adatmappa / "config.json"

allapot = {"nyelv": "en"}

javatipusok = ("vanilla", "paper", "purpur", "fabric", "forge", "neoforge")
tipusnevek = {
    "vanilla": "Vanilla",
    "paper": "Paper",
    "purpur": "Purpur",
    "fabric": "Fabric",
    "forge": "Forge",
    "neoforge": "NeoForge",
    "bedrock": "Bedrock",
    "pumpkin": "PumpkinMC",
}

szovegek = {
    "en": {
        "cim": "CubicLantern Server Manager",
        "szerver_letrehozasa": "Create server",
        "nincs_szerver": "You don't have any servers yet. Create one first!",
        "fut": "Running",
        "all": "Stopped",
        "vissza": "Back",
        "menu_iranyitas": "Control",
        "menu_vilag": "World manager",
        "menu_jatekosok": "Players",
        "menu_modok": "Mods",
        "menu_pluginek": "Plugins",
        "menu_beallitasok": "Settings",
        "mappa_megnyitas": "Open server folder",
        "nem_elerheto": "Not available for this server type",
        "start": "Start",
        "stop": "Stop",
        "restart": "Restart",
        "konzol_bevitel": "Type a command...",
        "kuldes": "Send",
        "memoria": "Memory usage",
        "nincs_psutil": "Install psutil to see memory usage (pip install psutil)",
        "playit_doboz": "playit.gg tunnel",
        "playit_be": "Enable playit",
        "playit_ki": "Disable playit",
        "playit_nincs": "Not running",
        "playit_letoltes": "Downloading playit agent...",
        "playit_kapcsolas": "Approve the playit connection in your browser...",
        "playit_fut": "Running",
        "playit_leallt": "Stopped",
        "playit_hiba": "Error: {hiba}",
        "playit_claim": "Click here to link playit to your account",
        "playit_cim": "Server address:",
        "playit_cim_tipp": "playit address (e.g. name.joinmc.link)",
        "masolas": "Copy",
        "playit_tipp": "After linking, create a tunnel on playit.gg for local port {port}. The address appears here automatically, or paste it manually.",
        "ping_doboz": "Latency test (through playit)",
        "ping_gomb": "Test ping",
        "ping_nincs_cim": "Enable playit and set the playit address first.",
        "ping_mero": "Measuring...",
        "ping_eredmeny": "Latency: {atlag} ms (min {legkisebb} ms, max {legnagyobb} ms)",
        "ping_hiba": "Ping failed: {hiba}",
        "pumpkin_fejlesztes": "PumpkinMC is still under development!",
        "pumpkin_kezi": "With PumpkinMC the settings must be edited manually.",
        "pumpkin_mappa": "Open the folder of the PumpkinMC binary",
        "fejlesztes_alatt": "in development",
        "legfrissebb": "latest",
        "nev": "Name",
        "tipus": "Server type",
        "verzio": "Version",
        "verzio_betoltes": "Loading versions...",
        "verzio_hiba": "Could not load versions: {hiba}",
        "eula_elfogadas": "I accept the Minecraft EULA (https://aka.ms/MinecraftEULA)",
        "letrehozas": "Create",
        "megse": "Cancel",
        "hiba": "Error",
        "figyelem": "Warning",
        "kesz": "Done",
        "nev_hianyzik": "Please enter a server name.",
        "nev_foglalt": "A server with this name already exists.",
        "eula_kell": "You must accept the EULA.",
        "keszul": "Creating server...",
        "java_letoltes": "Downloading Java {verzio}...",
        "jar_letoltes": "Downloading server files...",
        "telepites": "Running installer...",
        "konfig_iras": "Writing configuration...",
        "kesz_szerver": "Server created!",
        "telepito_hiba": "The installer failed:",
        "bedrock_nem_tamogatott": "The Bedrock server is not available for this platform.",
        "hiba_inditas": "Could not start the server (launch files are missing).",
        "szerver_leallt": "[Process exited with code {kod}]",
        "ram": "RAM",
        "g_general": "General",
        "g_gameplay": "Gameplay",
        "g_world": "World",
        "g_performance": "Performance",
        "g_network": "Network",
        "g_permissions": "Permissions",
        "p_motd": "Server description (MOTD)",
        "p_server-port": "Port",
        "p_max-players": "Max players",
        "p_online-mode": "Online mode (premium accounts only)",
        "p_gamemode": "Game mode",
        "p_force-gamemode": "Enforce game mode",
        "p_difficulty": "Difficulty",
        "p_hardcore": "Hardcore",
        "p_pvp": "PvP",
        "p_allow-flight": "Allow flight",
        "p_enable-command-block": "Command blocks",
        "p_spawn-protection": "Spawn protection (radius)",
        "p_level-seed": "World seed",
        "p_level-name": "World folder name",
        "p_level-type": "World type",
        "p_generate-structures": "Generate structures",
        "p_allow-nether": "Allow Nether",
        "p_max-tick-time": "Max tick time (ms)",
        "p_view-distance": "View distance",
        "p_simulation-distance": "Simulation distance",
        "p_white-list": "Whitelist",
        "p_op-permission-level": "OP permission level",
        "p_player-idle-timeout": "Idle timeout (minutes)",
        "p_spawn-monsters": "Spawn monsters",
        "p_spawn-animals": "Spawn animals",
        "p_spawn-npcs": "Spawn villagers",
        "p_server-name": "Server name",
        "p_allow-cheats": "Allow cheats",
        "p_allow-list": "Allowlist",
        "p_default-player-permission-level": "Default permission level",
        "p_tick-distance": "Tick distance",
        "mentes": "Save",
        "mentve": "Settings saved.",
        "ujrainditas_kell": "Restart the server to apply the changes.",
        "szerver_torlese": "Delete server",
        "torles_kerdes": "Delete this server and all of its files permanently?",
        "elobb_alljon_le": "Stop the server first.",
        "java_info": "Java {verzio} (downloaded automatically)",
        "vilag_nev": "World folder: {nev}",
        "vilag_seed": "World seed (empty = random)",
        "vilag_ujra": "Regenerate world",
        "vilag_ujra_kerdes": "The current world will be deleted. Continue?",
        "vilag_ujra_kesz": "The world was deleted. A new one is generated on the next start.",
        "vilag_mappa_feltoltes": "Upload world (folder)",
        "vilag_zip_feltoltes": "Upload world (zip)",
        "vilag_mentes": "Backup world",
        "vilag_megnyitas": "Open world folder",
        "vilag_csere_kerdes": "This replaces the current world. Continue?",
        "vilag_nem_talalt": "No world found in the selection.",
        "vilag_feltoltve": "The world was uploaded.",
        "vilag_mentve": "Backup saved: {fajl}",
        "vilag_nincs_mit_menteni": "There is no world to back up yet.",
        "dolgozom": "Working...",
        "kivalasztas": "Select",
        "online_jatekosok": "Players",
        "nincs_jatekos": "No players have joined yet.",
        "nem_fut_szerver": "The server is not running.",
        "ban": "Ban",
        "ipban": "IP ban",
        "op": "OP",
        "adat_torles": "Delete player data",
        "adat_torles_kerdes": "Delete all saved data of {nev}?",
        "adat_torolve": "Deleted files: {db}",
        "uuid_nincs": "Could not determine the UUID of the player.",
        "whitelist_be": "Whitelist enabled",
        "whitelist_kezeles": "Whitelist",
        "jatekos_nev": "Player name",
        "hozzaadas": "Add",
        "eltavolitas": "Remove",
        "hibas_nev": "Invalid player name.",
        "nincs_ilyen_jatekos": "Player not found.",
        "modok_cim": "Mods",
        "pluginek_cim": "Plugins",
        "import_gomb": "Import files...",
        "importalt": "Imported",
        "ures_lista": "Nothing here yet.",
        "bekapcsolva": "Enabled",
        "kikapcsolva": "Disabled",
        "kikapcsol": "Disable",
        "bekapcsol": "Enable",
        "torles": "Delete",
        "torles_fajl_kerdes": "Delete {nev}?",
        "frissites": "Refresh",
        "mod_tipp": "Drop .jar files here or use the import button. Restart the server after changes.",
        "fajl_valasztas": "Select files",
        "nyelv_leallitas": "All running servers will be stopped and the app will restart. Continue?",
        "kilepes_cim": "Exit",
        "kilepes_szoveg": "One or more servers are still running. Closing the program now may corrupt files. Stop all servers and exit?",
        "leallitas_folyamatban": "Stopping servers...",
        "fut_szerverek": "{db} server(s) running",
        "pumpkin_gep": "Recommended for low-end computers.",
        "alagut_valaszto": "Tunnel information",
        "alagut_kikapcsolva": "Disabled",
        "alagut_mindketto": "Playit + Pinggy",
        "pinggy_doboz": "Pinggy tunnels",
        "pinggy_indit": "Start Pinggy",
        "pinggy_leallit": "Stop Pinggy",
        "pinggy_fut": "Running in a separate terminal window",
        "pinggy_all": "Stopped",
        "pinggy_tipp": "Pinggy has three free tunnels at the same time. The tunnels start without a password or interactive confirmation. HTTP is also started without a password.",
        "pinggy_tipus": "Tunnel {db} type",
        "pinggy_port": "Local port",
        "pinggy_jelszo": "HTTP password (optional)",
        "pinggy_info": "Pinggy's free service is often faster and simpler, needs no account, and is useful for short sessions with friends. Its disadvantage is that it creates a new address every 60 minutes. Playit may have higher latency on its free plan, but its address is stable and stays the same. A Playit subscription is the best choice for a long-running server. You can run Playit and Pinggy together, for example Playit for Simple Voice Chat and Pinggy for Minecraft.",
        "svc_info": "Simple Voice Chat: create a separate UDP tunnel for the voice-chat port, then enter its public address and port in the mod/plugin config (voice_host and port, or the equivalent fields). If the public address changes, update the config and restart the server. Playit is convenient for SVC because its address is stable.",
        "pinggy_parancs": "Command preview",
        "pinggy_parancsok": "Command preview",
        "pinggy_window": "Each selected tunnel opens in its own separate terminal window without asking for a password or interactive confirmation.",
        "backup_menu": "Backups",
        "backup_title": "Automatic backups",
        "backup_enabled": "Enable automatic backups",
        "backup_location": "Backup location",
        "backup_browse": "Browse...",
        "backup_startup": "Create a backup when the server starts",
        "backup_interval": "Create a backup every",
        "backup_disabled": "0 = disabled",
        "backup_keep": "Backups to keep",
        "backup_prefix": "Filename prefix",
        "backup_now": "Create backup now",
        "backup_open": "Open backup folder",
        "backup_saved": "Backup saved: {fajl}",
        "backup_error": "Backup failed: {hiba}",
        "backup_tip": "Backups contain the server worlds and are stored as timestamped ZIP files.",
        "pinggy_ertesites": "Send Pinggy status and expiry messages to the server console",
        "pinggy_elindult": "Pinggy started.",
        "pinggy_leallt_uzenet": "Pinggy stopped.",
        "pinggy_ujraindul": "Pinggy is restarting.",
        "pinggy_ujraindult": "Pinggy restarted.",
        "pinggy_ujra": "Restart Pinggy now",
        "pinggy_allapot": "Status",
        "pinggy_hianyzik": "Pinggy UDP needs pinggy.exe. Put it next to the app or add it to PATH.",
        "pinggy_binaris": "Pinggy binary",
        "pinggy_letoltes": "Download Pinggy from pinggy.io/cli",
        "pinggy_import": "Import binary",
        "pinggy_torles": "Delete imported binary",
        "pinggy_nincs": "No imported binary. UDP requires pinggy.exe.",
        "pinggy_import_ok": "Pinggy binary imported as {fajl}.",
        "pinggy_torles_ok": "Imported Pinggy binary deleted.",
        "pinggy_lejar_10": "Pinggy expires in 10 minutes. It will restart automatically.",
        "pinggy_lejar_5": "Pinggy expires in 5 minutes. It will restart automatically.",
        "pinggy_ujra_info": "Manual restart resets the 60-minute timer.",
    },
    "hu": {
        "cim": "CubicLantern Server Manager",
        "szerver_letrehozasa": "Szerver létrehozása",
        "nincs_szerver": "Még nincs szervered. Előbb hozz létre egyet!",
        "fut": "Fut",
        "all": "Leállítva",
        "vissza": "Vissza",
        "menu_iranyitas": "Vezérlés",
        "menu_vilag": "Világkezelő",
        "menu_jatekosok": "Játékosok",
        "menu_modok": "Modok",
        "menu_pluginek": "Pluginok",
        "menu_beallitasok": "Beállítások",
        "mappa_megnyitas": "Szerver mappa megnyitása",
        "nem_elerheto": "Ennél a szervertípusnál nem elérhető",
        "start": "Indítás",
        "stop": "Leállítás",
        "restart": "Újraindítás",
        "konzol_bevitel": "Írj be egy parancsot...",
        "kuldes": "Küldés",
        "memoria": "Memóriahasználat",
        "nincs_psutil": "A memóriahasználat megjelenítéséhez telepítsd a psutil csomagot (pip install psutil)",
        "playit_doboz": "playit.gg alagút",
        "playit_be": "playit bekapcsolása",
        "playit_ki": "playit kikapcsolása",
        "playit_nincs": "Nem fut",
        "playit_letoltes": "playit ügynök letöltése...",
        "playit_kapcsolas": "Engedélyezd a playit-kapcsolatot a böngészőben...",
        "playit_fut": "Fut",
        "playit_leallt": "Leállt",
        "playit_hiba": "Hiba: {hiba}",
        "playit_claim": "Kattints ide a playit fiókodhoz kapcsolásához",
        "playit_cim": "Szerver cím:",
        "playit_cim_tipp": "playit cím (pl. nev.joinmc.link)",
        "masolas": "Másolás",
        "playit_tipp": "Összekapcsolás után hozz létre egy alagutat a playit.gg oldalon a(z) {port} helyi portra. A cím automatikusan megjelenik itt, vagy beillesztheted kézzel.",
        "ping_doboz": "Késés tesztelése (playiten keresztül)",
        "ping_gomb": "Ping teszt",
        "ping_nincs_cim": "Előbb kapcsold be a playitet és add meg a playit címet.",
        "ping_mero": "Mérés...",
        "ping_eredmeny": "Késés: {atlag} ms (min {legkisebb} ms, max {legnagyobb} ms)",
        "ping_hiba": "A ping sikertelen: {hiba}",
        "pumpkin_fejlesztes": "A PumpkinMC még fejlesztés alatt áll!",
        "pumpkin_kezi": "PumpkinMC-nél a beállításokat kézzel kell szerkeszteni.",
        "pumpkin_mappa": "A PumpkinMC bináris mappájának megnyitása",
        "fejlesztes_alatt": "fejlesztés alatt",
        "legfrissebb": "legfrissebb",
        "nev": "Név",
        "tipus": "Szerver típusa",
        "verzio": "Verzió",
        "verzio_betoltes": "Verziók betöltése...",
        "verzio_hiba": "A verziók betöltése sikertelen: {hiba}",
        "eula_elfogadas": "Elfogadom a Minecraft EULA-t (https://aka.ms/MinecraftEULA)",
        "letrehozas": "Létrehozás",
        "megse": "Mégse",
        "hiba": "Hiba",
        "figyelem": "Figyelem",
        "kesz": "Kész",
        "nev_hianyzik": "Adj meg egy szervernevet.",
        "nev_foglalt": "Már van ilyen nevű szerver.",
        "eula_kell": "El kell fogadnod az EULA-t.",
        "keszul": "Szerver létrehozása...",
        "java_letoltes": "Java {verzio} letöltése...",
        "jar_letoltes": "Szerverfájlok letöltése...",
        "telepites": "Telepítő futtatása...",
        "konfig_iras": "Beállítások írása...",
        "kesz_szerver": "A szerver elkészült!",
        "telepito_hiba": "A telepítő hibával leállt:",
        "bedrock_nem_tamogatott": "A Bedrock szerver ezen a platformon nem érhető el.",
        "hiba_inditas": "A szerver nem indítható (hiányoznak az indító fájlok).",
        "szerver_leallt": "[A folyamat leállt, kilépési kód: {kod}]",
        "ram": "RAM",
        "g_general": "Általános",
        "g_gameplay": "Játékmenet",
        "g_world": "Világ",
        "g_performance": "Teljesítmény",
        "g_network": "Hálózat",
        "g_permissions": "Jogosultságok",
        "p_motd": "Szerver leírása (MOTD)",
        "p_server-port": "Port",
        "p_max-players": "Max játékosok",
        "p_online-mode": "Online mód (csak eredeti fiókok)",
        "p_gamemode": "Játékmód",
        "p_force-gamemode": "Játékmód kényszerítése",
        "p_difficulty": "Nehézség",
        "p_hardcore": "Hardcore",
        "p_pvp": "PvP",
        "p_allow-flight": "Repülés engedélyezése",
        "p_enable-command-block": "Command blockok",
        "p_spawn-protection": "Spawn védelem (sugár)",
        "p_level-seed": "Világ seed",
        "p_level-name": "Világ mappa neve",
        "p_level-type": "Világ típusa",
        "p_generate-structures": "Struktúrák generálása",
        "p_allow-nether": "Nether engedélyezése",
        "p_max-tick-time": "Max tick idő (ms)",
        "p_view-distance": "Látótávolság",
        "p_simulation-distance": "Szimulációs távolság",
        "p_white-list": "Whitelist",
        "p_op-permission-level": "OP jogosultsági szint",
        "p_player-idle-timeout": "Tétlenségi időkorlát (perc)",
        "p_spawn-monsters": "Szörnyek spawnolása",
        "p_spawn-animals": "Állatok spawnolása",
        "p_spawn-npcs": "Falusiak spawnolása",
        "p_server-name": "Szerver neve",
        "p_allow-cheats": "Csalások engedélyezése",
        "p_allow-list": "Allowlist",
        "p_default-player-permission-level": "Alap jogosultsági szint",
        "p_tick-distance": "Tick távolság",
        "mentes": "Mentés",
        "mentve": "A beállítások elmentve.",
        "ujrainditas_kell": "A változtatások érvényesítéséhez indítsd újra a szervert.",
        "szerver_torlese": "Szerver törlése",
        "torles_kerdes": "Véglegesen törlöd ezt a szervert és az összes fájlját?",
        "elobb_alljon_le": "Előbb állítsd le a szervert.",
        "java_info": "Java {verzio} (automatikusan letöltve)",
        "vilag_nev": "Világ mappa: {nev}",
        "vilag_seed": "Világ seed (üres = véletlen)",
        "vilag_ujra": "Világ újragenerálása",
        "vilag_ujra_kerdes": "A jelenlegi világ törlődik. Folytatod?",
        "vilag_ujra_kesz": "A világ törölve lett. A következő indításkor új generálódik.",
        "vilag_mappa_feltoltes": "Világ feltöltése (mappa)",
        "vilag_zip_feltoltes": "Világ feltöltése (zip)",
        "vilag_mentes": "Világ mentése",
        "vilag_megnyitas": "Világ mappa megnyitása",
        "vilag_csere_kerdes": "Ez lecseréli a jelenlegi világot. Folytatod?",
        "vilag_nem_talalt": "A kijelölésben nem található világ.",
        "vilag_feltoltve": "A világ feltöltve.",
        "vilag_mentve": "Mentés elkészült: {fajl}",
        "vilag_nincs_mit_menteni": "Még nincs mit menteni.",
        "dolgozom": "Dolgozom...",
        "kivalasztas": "Kiválasztás",
        "online_jatekosok": "Felcsatlakozott játékosok",
        "nincs_jatekos": "Nincs felcsatlakozott játékos.",
        "nem_fut_szerver": "A szerver nem fut.",
        "ban": "Ban",
        "ipban": "IP ban",
        "op": "OP",
        "adat_torles": "Játékosadatok törlése",
        "adat_torles_kerdes": "Törlöd {nev} összes mentett adatát?",
        "adat_torolve": "Törölt fájlok: {db}",
        "uuid_nincs": "A játékos UUID-ja nem állapítható meg.",
        "whitelist_be": "Whitelist bekapcsolva",
        "whitelist_kezeles": "Whitelist",
        "jatekos_nev": "Játékos neve",
        "hozzaadas": "Hozzáadás",
        "eltavolitas": "Eltávolítás",
        "hibas_nev": "Érvénytelen játékosnév.",
        "nincs_ilyen_jatekos": "A játékos nem található.",
        "modok_cim": "Modok",
        "pluginek_cim": "Pluginok",
        "import_gomb": "Fájlok importálása...",
        "importalt": "Importált",
        "ures_lista": "Itt még nincs semmi.",
        "bekapcsolva": "Bekapcsolva",
        "kikapcsolva": "Kikapcsolva",
        "kikapcsol": "Kikapcsolás",
        "bekapcsol": "Bekapcsolás",
        "torles": "Törlés",
        "torles_fajl_kerdes": "Törlöd ezt: {nev}?",
        "frissites": "Frissítés",
        "mod_tipp": "Húzd ide a .jar fájlokat vagy használd az import gombot. Változtatás után indítsd újra a szervert.",
        "fajl_valasztas": "Fájlok kiválasztása",
        "nyelv_leallitas": "Minden futó szerver leáll és az alkalmazás újraindul. Folytatod?",
        "kilepes_cim": "Kilépés",
        "kilepes_szoveg": "Egy vagy több szerver még fut. Ha most bezárod a programot, a fájlok megsérülhetnek. Leállítod az összes szervert és kilépsz?",
        "leallitas_folyamatban": "Szerverek leállítása...",
        "fut_szerverek": "{db} szerver fut",
        "pumpkin_gep": "Gyenge gépekre javasolt.",
        "alagut_valaszto": "Alagút információ",
        "alagut_kikapcsolva": "Kikapcsolva",
        "alagut_mindketto": "Playit + Pinggy",
        "pinggy_doboz": "Pinggy alagutak",
        "pinggy_indit": "Pinggy indítása",
        "pinggy_leallit": "Pinggy leállítása",
        "pinggy_fut": "Külön terminálablakban fut",
        "pinggy_all": "Leállítva",
        "pinggy_tipp": "A Pinggy ingyenesen egyszerre három tunnelt tud futtatni. A tunnelek jelszó és interaktív megerősítés nélkül indulnak. A HTTP is jelszó nélkül indul.",
        "pinggy_tipus": "{db}. tunnel típusa",
        "pinggy_port": "Helyi port",
        "pinggy_jelszo": "HTTP-jelszó (opcionális)",
        "pinggy_info": "A Pinggy ingyenes változata gyorsabb és egyszerűbben beállítható lehet, nem kell hozzá fiók, és rövid, barátokkal játszott alkalmakhoz praktikus. Hátránya, hogy 60 percenként új címet generál. A Playit ingyenes verzióján több ping fordulhat elő, viszont a cím stabil és megmarad. Hosszú ideig futó szerverhez Playit-előfizetés javasolt. A Playit és a Pinggy egyszerre is futhat, például Playit a Simple Voice Chathez, Pinggy pedig a Minecrafthoz.",
        "svc_info": "Simple Voice Chat: hozz létre külön UDP tunnelt a voice-chat portjához, majd írd be a nyilvános címet és portot a mod/plugin konfigurációjába (voice_host és port, vagy az ezeknek megfelelő mezők). Ha a nyilvános cím megváltozik, írd át a konfigurációt és indítsd újra a szervert. Az SVC-hez kényelmesebb a Playit, mert stabil címet ad.",
        "pinggy_parancsok": "Parancs előnézete",
        "pinggy_window": "Minden kiválasztott tunnel saját külön terminálablakban indul, jelszó és interaktív megerősítés nélkül.",
        "backup_menu": "Biztonsági mentések",
        "backup_title": "Automatikus biztonsági mentések",
        "backup_enabled": "Automatikus mentések engedélyezése",
        "backup_location": "Mentések helye",
        "backup_browse": "Tallózás...",
        "backup_startup": "Mentés a szerver indításakor",
        "backup_interval": "Mentés ennyi percenként",
        "backup_disabled": "0 = kikapcsolva",
        "backup_keep": "Megtartandó mentések száma",
        "backup_prefix": "Fájlnév előtagja",
        "backup_now": "Mentés készítése most",
        "backup_open": "Mentésmappa megnyitása",
        "backup_saved": "Mentés elkészült: {fajl}",
        "backup_error": "A mentés sikertelen: {hiba}",
        "backup_tip": "A mentések a szerver világait időbélyeges ZIP-fájlokba mentik.",
        "pinggy_ertesites": "Pinggy állapot- és lejárási üzenetek küldése a szerverkonzolba",
        "pinggy_elindult": "A Pinggy elindult.",
        "pinggy_leallt_uzenet": "A Pinggy leállt.",
        "pinggy_ujraindul": "A Pinggy újraindul.",
        "pinggy_ujraindult": "A Pinggy újraindult.",
        "pinggy_ujra": "Pinggy újraindítása most",
        "pinggy_allapot": "Állapot",
        "pinggy_hianyzik": "A Pinggy UDP-hez szükség van a pinggy.exe fájlra. Tedd az alkalmazás mellé, vagy add hozzá a PATH-hoz.",
        "pinggy_binaris": "Pinggy bináris",
        "pinggy_letoltes": "Pinggy letöltése a pinggy.io/cli oldalról",
        "pinggy_import": "Bináris importálása",
        "pinggy_torles": "Importált bináris törlése",
        "pinggy_nincs": "Nincs importált bináris. UDP-hez pinggy szükséges.",
        "pinggy_import_ok": "A Pinggy bináris importálva: {fajl}.",
        "pinggy_torles_ok": "Az importált Pinggy bináris törölve.",
        "pinggy_lejar_10": "A Pinggy 10 perc múlva lejár. Automatikusan újraindul.",
        "pinggy_lejar_5": "A Pinggy 5 perc múlva lejár. Automatikusan újraindul.",
        "pinggy_ujra_info": "A kézi újraindítás visszaállítja a 60 perces időzítőt.",
    },
}


def t(kulcs, **adatok):
    szotar = szovegek.get(allapot["nyelv"], szovegek["en"])
    szoveg = szotar.get(kulcs) or szovegek["en"].get(kulcs) or kulcs
    if adatok:
        return szoveg.format(**adatok)
    return szoveg


def mezofelirat(kulcs):
    nev = "p_" + kulcs
    szoveg = szovegek.get(allapot["nyelv"], {}).get(nev) or szovegek["en"].get(nev)
    return szoveg or kulcs


def tipusfelirat(kulcs):
    if kulcs == "pumpkin":
        return "PumpkinMC (" + t("fejlesztes_alatt") + ")"
    if kulcs == "bedrock":
        return "Bedrock"
    return tipusnevek[kulcs] + " (Java)"


def mappakeszites():
    for mappa in (adatmappa, szerverekmappa, javamappa, playitmappa, pinggymappa):
        mappa.mkdir(parents=True, exist_ok=True)


def beallitasbetoltes():
    try:
        return json.loads(beallitasfajl.read_text(encoding="utf-8"))
    except Exception:
        return {}


def beallitasmentes(adat):
    beallitasfajl.write_text(json.dumps(adat, indent=2), encoding="utf-8")


def metabetoltes(mappa):
    adat = json.loads((Path(mappa) / "mcmaker.json").read_text(encoding="utf-8"))
    alapport = 19133 if adat.get("tipus") == "bedrock" else 25565
    adat.setdefault("alagut", "off")
    adat.setdefault("pinggy", [{"engedelyezve": True, "tipus": "udp" if adat.get("tipus") == "bedrock" else "tcp", "port": alapport, "jelszo": ""}, {"engedelyezve": False, "tipus": "udp", "port": alapport, "jelszo": ""}, {"engedelyezve": False, "tipus": "http", "port": 8000, "jelszo": ""}])
    if adat.get("tipus") == "bedrock":
        for tunnel in adat["pinggy"][:2]:
            if int(tunnel.get("port") or 0) == 19132:
                tunnel["port"] = 19133
    adat.setdefault("pinggyertesites", True)
    adat.setdefault("jatekosok", [])
    if not isinstance(adat["jatekosok"], list):
        adat["jatekosok"] = []
    adat["jatekosok"] = [str(nev).strip() for nev in adat["jatekosok"] if str(nev).strip()]
    try:
        gyorsitotar = json.loads((Path(mappa) / "usercache.json").read_text(encoding="utf-8"))
        for elem in gyorsitotar:
            nev = str(elem.get("name", "")).strip()
            if nev and nev not in adat["jatekosok"]:
                adat["jatekosok"].append(nev)
    except Exception:
        pass
    adat.setdefault("backup", {})
    backup = adat["backup"]
    backup.setdefault("engedelyezve", True)
    backup.setdefault("mappa", str(Path(mappa) / "backups"))
    backup.setdefault("indulaskor", True)
    backup.setdefault("intervallum", 30)
    backup.setdefault("megtart", 10)
    backup.setdefault("elo_tag", "backup")
    return adat


def metamentes(mappa, adat):
    (Path(mappa) / "mcmaker.json").write_text(json.dumps(adat, indent=2), encoding="utf-8")


def mappamegnyitas(ut):
    ut = Path(ut)
    ut.mkdir(parents=True, exist_ok=True)
    QDesktopServices.openUrl(QUrl.fromLocalFile(str(ut)))


def backupvilagmappak(mappa, tipus):
    mappa = Path(mappa)
    alap = "Bedrock level" if tipus == "bedrock" else "world"
    tulajdonsagok = tulajdonsagolvasas(mappa / "server.properties", tipus != "bedrock")
    nev = tulajdonsagok.get("level-name", alap)
    if tipus == "bedrock":
        return [mappa / "worlds" / nev]
    return [mappa / nev, mappa / (nev + "_nether"), mappa / (nev + "_the_end")]


def backupkeszites(mappa, tipus, adat):
    mappa = Path(mappa)
    cel = Path(adat.get("mappa") or (mappa / "backups"))
    cel.mkdir(parents=True, exist_ok=True)
    vilagok = [ut for ut in backupvilagmappak(mappa, tipus) if ut.exists()]
    if not vilagok:
        raise RuntimeError(t("vilag_nincs_mit_menteni"))
    elo_tag = re.sub(r"[^A-Za-z0-9_-]+", "_", str(adat.get("elo_tag") or "backup")).strip("_") or "backup"
    fajl = cel / (elo_tag + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".zip")
    with zipfile.ZipFile(fajl, "w", zipfile.ZIP_DEFLATED) as archivum:
        for vilagmappa in vilagok:
            for gyoker, almappak, fajlok in os.walk(vilagmappa):
                for nev in fajlok:
                    teljes = Path(gyoker) / nev
                    try:
                        archivum.write(teljes, teljes.relative_to(mappa))
                    except OSError:
                        pass
    megtart = max(1, int(adat.get("megtart") or 1))
    regi = sorted(cel.glob(elo_tag + "_*.zip"), key=lambda ut: ut.stat().st_mtime, reverse=True)
    for regi_fajl in regi[megtart:]:
        try:
            regi_fajl.unlink()
        except OSError:
            pass
    return fajl


ugynok = "Mozilla/5.0 (compatible; MinecraftServerMaker/1.0)"
ansiminta = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
csatlakozasminta = re.compile(r"\]: (?:\[Not Secure\] )?(\w{1,16}) joined the game\s*$|Player connected: ([^,\r\n]+),")
kilepesminta = re.compile(r"\]: (\w{1,16}) left the game\s*$|Player disconnected: ([^,\r\n]+),")
claimminta = re.compile(r"https://playit\.gg/claim/[A-Za-z0-9_\-]+")
playitcimminta = re.compile(r"\b([a-z0-9][a-z0-9\-\.]*\.(?:ply\.gg|joinmc\.link|playit\.plus)(?::\d+)?)", re.IGNORECASE)


def keres(url, idokorlat=30):
    kerelem = urllib.request.Request(url, headers={"User-Agent": ugynok})
    return urllib.request.urlopen(kerelem, timeout=idokorlat)


def jsonlekeres(url):
    with keres(url) as valasz:
        return json.loads(valasz.read().decode("utf-8"))


def szovegletoltes(url):
    with keres(url) as valasz:
        return valasz.read().decode("utf-8", errors="replace")


def fajlletoltes(url, cel, haladas=None):
    cel = Path(cel)
    cel.parent.mkdir(parents=True, exist_ok=True)
    resz = cel.with_name(cel.name + ".resz")
    with keres(url, 60) as valasz, open(resz, "wb") as kimenet:
        osszes = int(valasz.headers.get("Content-Length") or 0)
        kesz = 0
        while True:
            blokk = valasz.read(65536)
            if not blokk:
                break
            kimenet.write(blokk)
            kesz += len(blokk)
            if haladas and osszes:
                haladas(int(kesz * 100 / osszes))
    resz.replace(cel)


def verzioszamok(szoveg):
    return tuple(int(szam) for szam in re.findall(r"\d+", szoveg))


def stabilverzio(szoveg):
    return re.fullmatch(r"\d+(\.\d+)+", szoveg) is not None


def rendezes(lista):
    return sorted(set(lista), key=verzioszamok, reverse=True)


def platformnev():
    if os.name == "nt":
        return "windows"
    if sys.platform == "darwin":
        return "mac"
    return "linux"


def architektura():
    gep = platform.machine().lower()
    if gep in ("arm64", "aarch64"):
        return "arm64"
    return "x86_64"


def eszkozvalasztas(eszkozok):
    oszavak = {"windows": ("windows", "win"), "linux": ("linux",), "mac": ("macos", "darwin", "apple", "osx")}[platformnev()]
    archszavak = ("arm64", "aarch64") if architektura() == "arm64" else ("x86_64", "x64", "amd64")
    tiltott = (".sha256", ".sha1", ".md5", ".zip", ".tar.gz", ".txt", ".sig", ".pdb", ".json", ".deb", ".rpm", ".msi")
    jeloltek = []
    for eszkoz in eszkozok:
        nev = eszkoz["name"].lower()
        if nev.endswith(tiltott):
            continue
        if not any(szo in nev for szo in oszavak):
            continue
        if platformnev() == "windows" and not nev.endswith(".exe"):
            continue
        jeloltek.append(eszkoz)
    for eszkoz in jeloltek:
        if any(szo in eszkoz["name"].lower() for szo in archszavak):
            return eszkoz
    if jeloltek:
        return jeloltek[0]
    return None


mojangcache = {}


def mojangjegyzek():
    if "jegyzek" not in mojangcache:
        mojangcache["jegyzek"] = jsonlekeres("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")
    return mojangcache["jegyzek"]


def mojangverzioadat(verzio):
    for elem in mojangjegyzek()["versions"]:
        if elem["id"] == verzio:
            return jsonlekeres(elem["url"])
    return None


def javafoverzio(verzio):
    try:
        adat = mojangverzioadat(verzio)
        if adat and "javaVersion" in adat:
            return int(adat["javaVersion"]["majorVersion"])
    except Exception:
        pass
    szamok = verzioszamok(verzio)
    if szamok and szamok[0] >= 26:
        return 25
    if szamok >= (1, 20, 5):
        return 21
    if szamok >= (1, 17):
        return 17
    return 8


def forgepromok():
    return jsonlekeres("https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json")["promos"]


def forgeverzio(mc):
    promok = forgepromok()
    return promok.get(mc + "-recommended") or promok.get(mc + "-latest")


def neoforgetermekek():
    xml = szovegletoltes("https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml")
    terkep = {}
    for ver in re.findall(r"<version>([^<]+)</version>", xml):
        if "alpha" in ver or "snapshot" in ver:
            continue
        szamok = ver.split("-")[0].split(".")
        try:
            elso = int(szamok[0])
            masodik = int(szamok[1])
        except (ValueError, IndexError):
            continue
        if elso < 20:
            continue
        if elso < 26:
            mc = "1.%d" % elso if masodik == 0 else "1.%d.%d" % (elso, masodik)
        else:
            mc = "%d.%d" % (elso, masodik)
        terkep.setdefault(mc, []).append(ver)
    return terkep


def neoforgeverzio(mc):
    lista = neoforgetermekek().get(mc, [])
    stabil = [ver for ver in lista if "beta" not in ver]
    if stabil:
        return stabil[-1]
    if lista:
        return lista[-1]
    return None


def bedrockadat():
    adat = jsonlekeres("https://net-secondary.web.minecraft-services.net/api/v1.0/download/links")
    if os.name == "nt":
        cel = "serverBedrockWindows"
    elif sys.platform == "darwin":
        raise RuntimeError(t("bedrock_nem_tamogatott"))
    else:
        cel = "serverBedrockLinux"
    for elem in adat["result"]["links"]:
        if elem["downloadType"] == cel:
            url = elem["downloadUrl"]
            talalat = re.search(r"bedrock-server-([\d\.]+)\.zip", url)
            return url, (talalat.group(1) if talalat else "latest")
    raise RuntimeError(t("bedrock_nem_tamogatott"))


def pumpkinkiadas():
    try:
        return jsonlekeres("https://api.github.com/repos/Pumpkin-MC/Pumpkin/releases/latest")
    except Exception:
        return jsonlekeres("https://api.github.com/repos/Pumpkin-MC/Pumpkin/releases")[0]


def verziolista(tipus):
    if tipus == "vanilla":
        return [elem["id"] for elem in mojangjegyzek()["versions"] if elem["type"] == "release"]
    if tipus == "paper":
        adat = jsonlekeres("https://fill.papermc.io/v3/projects/paper")["versions"]
        if isinstance(adat, dict):
            osszes = [ver for csoport in adat.values() for ver in csoport]
        else:
            osszes = adat
        return rendezes([ver for ver in osszes if stabilverzio(ver)])
    if tipus == "purpur":
        adat = jsonlekeres("https://api.purpurmc.org/v2/purpur")["versions"]
        return rendezes([ver for ver in adat if stabilverzio(ver)])
    if tipus == "fabric":
        adat = jsonlekeres("https://meta.fabricmc.net/v2/versions/game")
        return [elem["version"] for elem in adat if elem.get("stable")]
    if tipus == "forge":
        verziok = set()
        for kulcs in forgepromok():
            if kulcs.endswith("-latest") or kulcs.endswith("-recommended"):
                mc = kulcs.rsplit("-", 1)[0]
                if stabilverzio(mc) and verzioszamok(mc) >= (1, 12, 2):
                    verziok.add(mc)
        return rendezes(verziok)
    if tipus == "neoforge":
        return rendezes(neoforgetermekek().keys())
    return []


def paperjar(mc, cel, haladas):
    try:
        adat = jsonlekeres("https://fill.papermc.io/v3/projects/paper/versions/%s/builds/latest" % mc)
        url = adat["downloads"]["server:default"]["url"]
    except Exception:
        epitesek = jsonlekeres("https://api.papermc.io/v2/projects/paper/versions/%s/builds" % mc)["builds"]
        utolso = epitesek[-1]
        nev = utolso["downloads"]["application"]["name"]
        url = "https://api.papermc.io/v2/projects/paper/versions/%s/builds/%s/downloads/%s" % (mc, utolso["build"], nev)
    fajlletoltes(url, cel, haladas)


def purpurjar(mc, cel, haladas):
    epites = jsonlekeres("https://api.purpurmc.org/v2/purpur/%s/latest" % mc)["build"]
    fajlletoltes("https://api.purpurmc.org/v2/purpur/%s/%s/download" % (mc, epites), cel, haladas)


def fabricjar(mc, cel, haladas):
    betolto = [elem["version"] for elem in jsonlekeres("https://meta.fabricmc.net/v2/versions/loader") if elem.get("stable")][0]
    telepito = [elem["version"] for elem in jsonlekeres("https://meta.fabricmc.net/v2/versions/installer") if elem.get("stable")][0]
    fajlletoltes("https://meta.fabricmc.net/v2/versions/loader/%s/%s/%s/server/jar" % (mc, betolto, telepito), cel, haladas)


def javautvonal(foverzio):
    mappa = javamappa / str(foverzio)
    nev = "java.exe" if os.name == "nt" else "java"
    if mappa.exists():
        for ut in mappa.rglob(nev):
            if ut.parent.name == "bin" and ut.is_file():
                return ut
    return None


def javaletoltes(foverzio, haladas=None):
    letezo = javautvonal(foverzio)
    if letezo:
        return letezo
    arch = "aarch64" if architektura() == "arm64" else "x64"
    url = "https://api.adoptium.net/v3/binary/latest/%d/ga/%s/%s/jre/hotspot/normal/eclipse" % (foverzio, platformnev(), arch)
    ideiglenes = javamappa / ("letoltes_%d.pkg" % foverzio)
    fajlletoltes(url, ideiglenes, haladas)
    cel = javamappa / str(foverzio)
    if cel.exists():
        shutil.rmtree(cel, ignore_errors=True)
    cel.mkdir(parents=True)
    try:
        if zipfile.is_zipfile(ideiglenes):
            with zipfile.ZipFile(ideiglenes) as archivum:
                archivum.extractall(cel)
        else:
            with tarfile.open(ideiglenes) as archivum:
                if hasattr(tarfile, "data_filter"):
                    archivum.extractall(cel, filter="data")
                else:
                    archivum.extractall(cel)
    finally:
        ideiglenes.unlink(missing_ok=True)
    ut = javautvonal(foverzio)
    if not ut:
        raise RuntimeError("Java")
    if os.name != "nt":
        ut.chmod(0o755)
    return ut


def playitletoltes(haladas=None):
    nev = "playit.exe" if os.name == "nt" else "playit"
    cel = playitmappa / nev
    if cel.exists():
        return cel
    url = None
    try:
        kiadas = jsonlekeres("https://api.github.com/repos/playit-cloud/playit-agent/releases/latest")
        eszkoznev = {
            ("windows", "x86_64"): "playit-windows-x86_64-signed.exe",
            ("linux", "x86_64"): "playit-linux-amd64",
            ("linux", "arm64"): "playit-linux-aarch64",
        }.get((platformnev(), architektura()))
        eszkoz = next(
            (elem for elem in kiadas["assets"] if elem["name"] == eszkoznev),
            None,
        ) if eszkoznev else eszkozvalasztas(kiadas["assets"])
        if eszkoz:
            url = eszkoz["browser_download_url"]
    except Exception:
        url = None
    if not url:
        if os.name == "nt":
            url = "https://github.com/playit-cloud/playit-agent/releases/latest/download/playit-windows-x86_64-signed.exe"
        else:
            url = "https://github.com/playit-cloud/playit-agent/releases/latest/download/playit-linux-amd64"
    fajlletoltes(url, cel, haladas)
    if os.name != "nt":
        cel.chmod(0o755)
    return cel


def kulonterminal(program, argumentumok, munkamappa, cim):
    munkamappa = str(munkamappa)
    if os.name == "nt":
        return subprocess.Popen([str(program)] + [str(x) for x in argumentumok], cwd=munkamappa, creationflags=subprocess.CREATE_NEW_CONSOLE)
    parancs = [str(program)] + [str(x) for x in argumentumok]
    terminal = shutil.which("gnome-terminal") or shutil.which("konsole") or shutil.which("xterm") or shutil.which("x-terminal-emulator")
    if terminal and Path(terminal).name == "gnome-terminal":
        parancs = [terminal, "--title", cim, "--"] + parancs
    elif terminal and Path(terminal).name == "konsole":
        parancs = [terminal, "--workdir", munkamappa, "-e"] + parancs
    elif terminal:
        parancs = [terminal, "-T", cim, "-e"] + parancs
    else:
        return subprocess.Popen(parancs, cwd=munkamappa)
    return subprocess.Popen(parancs, cwd=munkamappa)


def pinggyprogram():
    nev = "pinggy.exe" if os.name == "nt" else "pinggy"
    jeloltek = [pinggymappa / nev, Path.cwd() / nev, Path(__file__).resolve().parent / nev]
    if getattr(sys, "frozen", False):
        jeloltek.insert(0, Path(sys.executable).resolve().parent / nev)
    for jelolt in jeloltek:
        if jelolt.is_file():
            return str(jelolt)
    return shutil.which(nev)


def pinggyimportal(forras):
    mappakeszites()
    cel = pinggymappa / ("pinggy.exe" if os.name == "nt" else "pinggy")
    shutil.copy2(forras, cel)
    if os.name != "nt":
        cel.chmod(cel.stat().st_mode | 0o111)
    return cel


def pinggyimportalttorles():
    cel = pinggymappa / ("pinggy.exe" if os.name == "nt" else "pinggy")
    try:
        cel.unlink()
    except FileNotFoundError:
        return False
    return True


def pinggyparancs(tunnel):
    tipus = tunnel.get("tipus", "tcp")
    port = int(tunnel.get("port") or 25565)
    cel = "127.0.0.1:%d" % port
    if tipus == "udp":
        program = pinggyprogram() or ("pinggy.exe" if os.name == "nt" else "pinggy")
        return program, ["-p", "443", "-R0:" + cel, "udp@free.pinggy.io"]
    if tipus == "http":
        return "ssh", ["-p", "443", "-R0:" + cel, "free.pinggy.io"]
    return "ssh", ["-p", "443", "-R0:" + cel, "tcp@free.pinggy.io"]


def pinggyparancsszoveg(program, argumentumok):
    if os.name == "nt":
        return subprocess.list2cmdline([program] + argumentumok)
    return shlex.join([program] + argumentumok)


def powershellszoveg(szoveg):
    return "'" + str(szoveg).replace("'", "''") + "'"


def pinggysegitoprogram(program, argumentumok):
    if getattr(sys, "frozen", False):
        elo = [sys.executable, "--cubiclantern-pinggy-tunnel"]
    else:
        elo = [sys.executable, str(Path(__file__).resolve()), "--cubiclantern-pinggy-tunnel"]
    return elo + [str(program)] + [str(x) for x in argumentumok]


def pinggyterminal(tunnel, mappa, cim):
    mappa = Path(mappa)
    if os.name == "nt":
        launcher = mappa / (".cubiclantern_pinggy_%s.ps1" % uuid.uuid4().hex)
        program, argumentumok = pinggyparancs(tunnel)
        segito = pinggysegitoprogram(program, argumentumok)
        lista = ", ".join(powershellszoveg(x) for x in segito[1:])
        sorok = ["Write-Host 'CubicLantern Pinggy tunnel'", "Write-Host 'No password or interactive confirmation is required.'", "$program = %s" % powershellszoveg(segito[0]), "Write-Host 'The tunnel is running in this window.'", "while ($true) {", "Start-Process -FilePath $program -ArgumentList @(%s) -NoNewWindow -Wait" % lista, "Start-Sleep -Seconds 2", "}"]
        launcher.write_text("\r\n".join(sorok) + "\r\n", encoding="utf-8")
        return subprocess.Popen(["cmd.exe", "/d", "/c", "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(launcher)], cwd=str(mappa), creationflags=subprocess.CREATE_NEW_CONSOLE)
    launcher = mappa / (".cubiclantern_pinggy_%s.sh" % uuid.uuid4().hex)
    program, argumentumok = pinggyparancs(tunnel)
    segito = pinggysegitoprogram(program, argumentumok)
    parancs = pinggyparancsszoveg(segito[0], segito[1:])
    sorok = ["#!/bin/sh", "trap 'kill 0 2>/dev/null; exit 0' INT TERM EXIT", "printf '%s\\n' 'CubicLantern Pinggy tunnels: no password or interactive confirmation is required.'"]
    sorok += ["while true; do " + parancs + "; sleep 1; done"]
    launcher.write_text("\n".join(sorok) + "\n", encoding="utf-8")
    launcher.chmod(0o755)
    terminal = shutil.which("gnome-terminal") or shutil.which("konsole") or shutil.which("xterm") or shutil.which("x-terminal-emulator")
    if terminal and Path(terminal).name == "gnome-terminal":
        parancs = [terminal, "--title", cim, "--", "sh", str(launcher)]
    elif terminal and Path(terminal).name == "konsole":
        parancs = [terminal, "--workdir", str(mappa), "-e", "sh", str(launcher)]
    elif terminal:
        parancs = [terminal, "-T", cim, "-e", "sh", str(launcher)]
    else:
        raise RuntimeError("No graphical terminal emulator was found.")
    return subprocess.Popen(parancs, cwd=str(mappa), start_new_session=True)


def playitapipost(utvonal, adatok):
    kerelem = urllib.request.Request(
        "https://api.playit.gg" + utvonal,
        data=json.dumps(adatok).encode("utf-8"),
        headers={"User-Agent": ugynok, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(kerelem, timeout=15) as valasz:
        eredmeny = json.loads(valasz.read().decode("utf-8"))
    if eredmeny.get("status") != "success":
        hiba = eredmeny.get("data") or eredmeny.get("error") or eredmeny
        raise RuntimeError(json.dumps(hiba, ensure_ascii=True))
    return eredmeny.get("data")


def playitkulcsigenyles(kod):
    hatarido = time.monotonic() + 300
    kerelem = {
        "code": kod,
        "agent_type": "self-managed",
        "version": "Minecraft Server Maker",
    }
    while time.monotonic() < hatarido:
        allapot = playitapipost("/claim/setup", kerelem)
        if allapot == "UserAccepted":
            break
        if allapot == "UserRejected":
            raise RuntimeError("The playit agent claim was rejected.")
        if allapot not in ("WaitingForUserVisit", "WaitingForUser"):
            raise RuntimeError("Unexpected playit claim response: " + str(allapot))
        time.sleep(2)
    else:
        raise RuntimeError("Timed out waiting for playit account approval.")
    while time.monotonic() < hatarido:
        try:
            return playitapipost("/claim/exchange", {"code": kod})["secret_key"]
        except RuntimeError as hiba:
            if "NotAccepted" not in str(hiba):
                raise
            time.sleep(2)
    raise RuntimeError("Timed out while receiving the playit agent key.")


def propkodolas(ertek):
    kimenet = []
    for jel in ertek:
        kod = ord(jel)
        if jel == "\\":
            kimenet.append("\\\\")
        elif kod > 126:
            if kod > 0xFFFF:
                kod -= 0x10000
                kimenet.append("\\u%04x\\u%04x" % (0xD800 + (kod >> 10), 0xDC00 + (kod & 0x3FF)))
            else:
                kimenet.append("\\u%04x" % kod)
        else:
            kimenet.append(jel)
    return "".join(kimenet)


def propdekodolas(ertek):
    def csere(talalat):
        resz = talalat.group(1)
        if len(resz) == 5:
            return chr(int(resz[1:], 16))
        return resz

    szoveg = re.sub(r"\\(u[0-9a-fA-F]{4}|.)", csere, ertek)
    try:
        return szoveg.encode("utf-16", "surrogatepass").decode("utf-16")
    except Exception:
        return szoveg


def tulajdonsagolvasas(ut, escape=True):
    adat = {}
    ut = Path(ut)
    if ut.exists():
        for sor in ut.read_text(encoding="utf-8", errors="replace").splitlines():
            sor = sor.strip()
            if not sor or sor.startswith("#") or "=" not in sor:
                continue
            kulcs, ertek = sor.split("=", 1)
            ertek = ertek.strip()
            adat[kulcs.strip()] = propdekodolas(ertek) if escape else ertek
    return adat


def tulajdonsagiras(ut, ertekek, escape=True):
    ut = Path(ut)
    sorok = ut.read_text(encoding="utf-8", errors="replace").splitlines() if ut.exists() else []
    kesz = set()
    uj = []
    for sor in sorok:
        resz = sor.strip()
        if resz and not resz.startswith("#") and "=" in resz:
            kulcs = resz.split("=", 1)[0].strip()
            if kulcs in ertekek:
                ertek = propkodolas(ertekek[kulcs]) if escape else ertekek[kulcs]
                uj.append("%s=%s" % (kulcs, ertek))
                kesz.add(kulcs)
                continue
        uj.append(sor)
    for kulcs, ertek in ertekek.items():
        if kulcs not in kesz:
            ertek = propkodolas(ertek) if escape else ertek
            uj.append("%s=%s" % (kulcs, ertek))
    ut.write_text("\n".join(uj) + "\n", encoding="utf-8")


def leveltipus(ertek, verzio):
    uj = {
        "default": "minecraft:normal",
        "normal": "minecraft:normal",
        "flat": "minecraft:flat",
        "largebiomes": "minecraft:large_biomes",
        "large_biomes": "minecraft:large_biomes",
        "amplified": "minecraft:amplified",
    }
    tiszta = ertek.replace("\\", "").lower().replace("minecraft:", "")
    nev = uj.get(tiszta, ertek)
    szamok = verzioszamok(verzio)
    if szamok and szamok < (1, 19, 3):
        regi = {
            "minecraft:normal": "default",
            "minecraft:flat": "flat",
            "minecraft:large_biomes": "largeBiomes",
            "minecraft:amplified": "amplified",
        }
        return regi.get(nev, nev)
    return nev


javaschema = [
    ("motd", "s", "A Minecraft Server", None, "general"),
    ("server-port", "i", 25565, (1, 65535), "general"),
    ("max-players", "i", 20, (1, 100000), "general"),
    ("online-mode", "b", True, None, "general"),
    ("gamemode", "c", "survival", ["survival", "creative", "adventure", "spectator"], "gameplay"),
    ("force-gamemode", "b", False, None, "gameplay"),
    ("difficulty", "c", "easy", ["peaceful", "easy", "normal", "hard"], "gameplay"),
    ("hardcore", "b", False, None, "gameplay"),
    ("pvp", "b", True, None, "gameplay"),
    ("allow-flight", "b", False, None, "gameplay"),
    ("enable-command-block", "b", False, None, "gameplay"),
    ("spawn-protection", "i", 16, (0, 1000), "gameplay"),
    ("spawn-monsters", "b", True, None, "gameplay"),
    ("spawn-animals", "b", True, None, "gameplay"),
    ("spawn-npcs", "b", True, None, "gameplay"),
    ("player-idle-timeout", "i", 0, (0, 100000), "gameplay"),
    ("level-name", "s", "world", None, "world"),
    ("level-seed", "s", "", None, "world"),
    ("level-type", "c", "minecraft:normal", ["minecraft:normal", "minecraft:flat", "minecraft:large_biomes", "minecraft:amplified"], "world"),
    ("generate-structures", "b", True, None, "world"),
    ("allow-nether", "b", True, None, "world"),
    ("max-world-size", "i", 29999984, (1, 29999984), "world"),
    ("view-distance", "i", 10, (2, 32), "performance"),
    ("simulation-distance", "i", 10, (3, 32), "performance"),
    ("max-tick-time", "i", 60000, (-1, 2147483647), "performance"),
    ("network-compression-threshold", "i", 256, (-1, 65535), "performance"),
    ("entity-broadcast-range-percentage", "i", 100, (10, 500), "performance"),
    ("sync-chunk-writes", "b", True, None, "performance"),
    ("use-native-transport", "b", True, None, "performance"),
    ("enable-status", "b", True, None, "network"),
    ("hide-online-players", "b", False, None, "network"),
    ("enable-query", "b", False, None, "network"),
    ("enforce-secure-profile", "b", True, None, "network"),
    ("prevent-proxy-connections", "b", False, None, "network"),
    ("rate-limit", "i", 0, (0, 100000), "network"),
    ("white-list", "b", False, None, "permissions"),
    ("enforce-whitelist", "b", False, None, "permissions"),
    ("op-permission-level", "i", 4, (0, 4), "permissions"),
    ("function-permission-level", "i", 2, (1, 4), "permissions"),
]

bedrockschema = [
    ("server-name", "s", "Dedicated Server", None, "general"),
    ("server-port", "i", 19132, (1, 65535), "general"),
    ("server-portv6", "i", 19133, (1, 65535), "general"),
    ("max-players", "i", 10, (1, 100000), "general"),
    ("online-mode", "b", True, None, "general"),
    ("allow-list", "b", False, None, "general"),
    ("gamemode", "c", "survival", ["survival", "creative", "adventure"], "gameplay"),
    ("force-gamemode", "b", False, None, "gameplay"),
    ("difficulty", "c", "easy", ["peaceful", "easy", "normal", "hard"], "gameplay"),
    ("allow-cheats", "b", False, None, "gameplay"),
    ("default-player-permission-level", "c", "member", ["visitor", "member", "operator"], "gameplay"),
    ("player-idle-timeout", "i", 30, (0, 100000), "gameplay"),
    ("level-name", "s", "Bedrock level", None, "world"),
    ("level-seed", "s", "", None, "world"),
    ("view-distance", "i", 32, (5, 96), "performance"),
    ("tick-distance", "i", 4, (4, 12), "performance"),
    ("max-threads", "i", 8, (0, 256), "performance"),
    ("compression-threshold", "i", 1, (0, 65535), "performance"),
    ("compression-algorithm", "c", "zlib", ["zlib", "snappy"], "performance"),
    ("server-authoritative-movement", "c", "server-auth", ["client-auth", "server-auth", "server-auth-with-rewind"], "network"),
    ("texturepack-required", "b", False, None, "network"),
    ("content-log-file-enabled", "b", False, None, "network"),
    ("emit-server-telemetry", "b", False, None, "network"),
]


def varint(szam):
    kimenet = b""
    while True:
        bajt = szam & 0x7F
        szam >>= 7
        if szam:
            kimenet += bytes([bajt | 0x80])
        else:
            kimenet += bytes([bajt])
            return kimenet


def csomagepites(azonosito, tartalom):
    torzs = varint(azonosito) + tartalom
    return varint(len(torzs)) + torzs


def szovegkodolas(szoveg):
    adat = szoveg.encode("utf-8")
    return varint(len(adat)) + adat


def varintolvasas(foglalat):
    ertek = 0
    for hely in range(5):
        bajt = foglalat.recv(1)
        if not bajt:
            raise ConnectionError("closed")
        ertek |= (bajt[0] & 0x7F) << (7 * hely)
        if not bajt[0] & 0x80:
            return ertek
    raise ValueError("varint")


def pontosolvasas(foglalat, hossz):
    adat = b""
    while len(adat) < hossz:
        resz = foglalat.recv(hossz - len(adat))
        if not resz:
            raise ConnectionError("closed")
        adat += resz
    return adat


def javaping(host, port):
    foglalat = socket.create_connection((host, port), timeout=6)
    try:
        foglalat.settimeout(6)
        foglalat.sendall(csomagepites(0, varint(0) + szovegkodolas(host) + struct.pack(">H", port) + varint(1)))
        foglalat.sendall(csomagepites(0, b""))
        hossz = varintolvasas(foglalat)
        pontosolvasas(foglalat, hossz)
        kezdet = time.perf_counter()
        foglalat.sendall(csomagepites(1, struct.pack(">q", int(time.time() * 1000))))
        hossz = varintolvasas(foglalat)
        pontosolvasas(foglalat, hossz)
        return (time.perf_counter() - kezdet) * 1000
    finally:
        foglalat.close()


def bedrockping(host, port):
    cim = socket.getaddrinfo(host, port, type=socket.SOCK_DGRAM)[0]
    foglalat = socket.socket(cim[0], cim[1], cim[2])
    try:
        foglalat.settimeout(6)
        varazs = bytes.fromhex("00ffff00fefefefefdfdfdfd12345678")
        csomag = b"\x01" + struct.pack(">q", int(time.time() * 1000)) + varazs + struct.pack(">q", 2)
        kezdet = time.perf_counter()
        foglalat.sendto(csomag, cim[4])
        adat, _ = foglalat.recvfrom(4096)
        ido = (time.perf_counter() - kezdet) * 1000
        if not adat or adat[0] != 0x1C:
            raise ConnectionError("bedrock")
        return ido
    finally:
        foglalat.close()


def pingmeres(host, port, bedrock):
    eredmenyek = []
    utolsohiba = None
    for kor in range(3):
        try:
            eredmenyek.append(bedrockping(host, port) if bedrock else javaping(host, port))
        except Exception as hiba:
            utolsohiba = hiba
        time.sleep(0.2)
    if not eredmenyek:
        raise utolsohiba or RuntimeError("ping")
    return sum(eredmenyek) / len(eredmenyek), min(eredmenyek), max(eredmenyek)


def cimfelbontas(szoveg, alapport):
    szoveg = szoveg.strip()
    for elotag in ("tcp://", "udp://", "http://", "https://"):
        if szoveg.lower().startswith(elotag):
            szoveg = szoveg[len(elotag):]
    szoveg = szoveg.strip("/ ")
    if szoveg.count(":") == 1:
        host, port = szoveg.split(":")
        try:
            return host, int(port)
        except ValueError:
            return host, alapport
    return szoveg, alapport


def uuidkeres(nev, online):
    if not online:
        kivonat = hashlib.md5(("OfflinePlayer:" + nev).encode("utf-8")).digest()
        return str(uuid.UUID(bytes=kivonat, version=3))
    try:
        adat = jsonlekeres("https://api.mojang.com/users/profiles/minecraft/" + urllib.parse.quote(nev))
        return str(uuid.UUID(adat["id"]))
    except urllib.error.HTTPError as hiba:
        if hiba.code in (204, 404):
            raise RuntimeError(t("nincs_ilyen_jatekos"))
        raise
    except (ValueError, KeyError):
        raise RuntimeError(t("nincs_ilyen_jatekos"))


aktivszalak = []


class futtato(QThread):
    kesz = Signal()

    def __init__(self, fuggveny, sikerfv=None, hibafv=None):
        super().__init__()
        self.fuggveny = fuggveny
        self.sikerfv = sikerfv
        self.hibafv = hibafv
        self.eredmeny = None
        self.hibauzenet = None
        self.kesz.connect(self.lezaras)

    def run(self):
        try:
            self.eredmeny = self.fuggveny()
        except Exception as hiba:
            self.hibauzenet = str(hiba) or repr(hiba)
        self.kesz.emit()

    def lezaras(self):
        if self.hibauzenet is not None:
            if self.hibafv:
                self.hibafv(self.hibauzenet)
        elif self.sikerfv:
            self.sikerfv(self.eredmeny)

    def torles(self):
        if self in aktivszalak:
            aktivszalak.remove(self)
        self.deleteLater()


def hatterfeladat(fuggveny, sikerfv=None, hibafv=None):
    szal = futtato(fuggveny, sikerfv, hibafv)
    aktivszalak.append(szal)
    szal.finished.connect(szal.torles)
    szal.start()
    return szal


class szerverfolyamat(QObject):
    sorkesz = Signal(str)
    allapotvaltozas = Signal()
    jatekosvaltozas = Signal()
    playitvaltozas = Signal()

    def __init__(self, mappa):
        super().__init__()
        self.mappa = Path(mappa)
        self.meta = metabetoltes(self.mappa)
        self.folyamat = None
        self.sorok = []
        self.puffer = ""
        self.jatekosok = []
        self.leallitasjel = 0
        self.ujrakeres = False
        self.javafoglalt = False
        self.playitfolyamat = None
        self.playitut = ""
        self.playitpuffer = ""
        self.playitsorok = []
        self.playitclaim = ""
        self.playitallapot = ""
        self.playitprobalkozas = 0
        self.playitindult = 0.0
        self.playitkilepes = False
        self.playitfoglalt = False
        self.pinggyfolyamatok = []
        self.pinggyallapot = ""
        self.pinggyaktiv = False
        self.pinggyujraindul = False
        self.pinggyhatarido = 0.0
        self.pinggyfigyelmeztetes10 = False
        self.pinggyfigyelmeztetes5 = False
        self.backupfolyamatban = False
        self.backupkovetkezo = 0.0
        self.pinggyidozito = QTimer(self)
        self.pinggyidozito.setInterval(1000)
        self.pinggyidozito.timeout.connect(self.pinggyfigyelo)
        self.pinggyidozito.timeout.connect(self.backupfigyelo)
        self.pinggyidozito.start()
        playitazonosito = hashlib.sha256(str(self.mappa.resolve()).encode("utf-8")).hexdigest()[:16]
        self.playitkulcsfajl = playitmappa / ("agent_" + playitazonosito + ".secret")
        if os.name == "nt":
            self.playitsocket = r"\\.\pipe\MinecraftServerMaker-" + playitazonosito
        else:
            self.playitsocket = str(playitmappa / ("playitd-" + playitazonosito + ".sock"))
        self.playitujrahitelesites = False

    def tipus(self):
        return self.meta.get("tipus", "")

    def fut(self):
        return self.folyamat is not None and self.folyamat.state() != QProcess.ProcessState.NotRunning

    def playitfut(self):
        return self.playitfolyamat is not None and self.playitfolyamat.poll() is None

    def metamentese(self):
        metamentes(self.mappa, self.meta)

    def portszam(self):
        alap = "19132" if self.tipus() == "bedrock" else "25565"
        return tulajdonsagolvasas(self.mappa / "server.properties", self.tipus() != "bedrock").get("server-port", alap)

    def kiir(self, szoveg):
        self.sorok.append(szoveg)
        if len(self.sorok) > 5000:
            del self.sorok[:1000]
        self.sorkesz.emit(szoveg)

    def argsfajl(self):
        nev = "win_args.txt" if os.name == "nt" else "unix_args.txt"
        if self.tipus() == "forge":
            minta = "libraries/net/minecraftforge/forge/*/" + nev
        else:
            minta = "libraries/net/neoforged/neoforge/*/" + nev
        talalatok = sorted(self.mappa.glob(minta))
        if talalatok:
            return talalatok[-1].relative_to(self.mappa).as_posix()
        return None

    def forgejar(self):
        for ut in sorted(self.mappa.glob("forge-*.jar")):
            if "installer" not in ut.name.lower():
                return ut.name
        return None

    def parancsepites(self):
        tipus = self.tipus()
        if tipus == "bedrock":
            return str(self.mappa / ("bedrock_server.exe" if os.name == "nt" else "bedrock_server")), []
        if tipus == "pumpkin":
            return str(self.mappa / self.meta["fajl"]), []
        java = javautvonal(int(self.meta["java"]))
        if not java:
            return None
        ram = int(self.meta.get("ram") or 2048)
        memoria = ["-Xms%dM" % ram, "-Xmx%dM" % ram]
        if tipus in ("forge", "neoforge"):
            argumentumok = self.argsfajl()
            if argumentumok:
                (self.mappa / "user_jvm_args.txt").write_text("\n".join(memoria) + "\n", encoding="utf-8")
                return str(java), ["@user_jvm_args.txt", "@" + argumentumok, "nogui"]
            jar = self.forgejar()
            if jar:
                return str(java), memoria + ["-jar", jar, "nogui"]
            return None
        return str(java), memoria + ["-jar", self.meta["fajl"], "nogui"]

    def inditas(self):
        if self.fut() or self.javafoglalt:
            return
        self.meta = metabetoltes(self.mappa)
        tipus = self.tipus()
        if tipus in ("bedrock", "pumpkin"):
            self.folyamatinditas()
            return
        foverzio = int(self.meta["java"])
        if javautvonal(foverzio):
            self.folyamatinditas()
            return
        self.javafoglalt = True
        self.kiir(t("java_letoltes", verzio=foverzio))
        self.allapotvaltozas.emit()
        hatterfeladat(lambda: javaletoltes(foverzio), self.javakesz, self.javahiba)

    def javakesz(self, ut):
        self.javafoglalt = False
        self.folyamatinditas()

    def javahiba(self, uzenet):
        self.javafoglalt = False
        self.kiir(t("hiba") + ": " + uzenet)
        self.allapotvaltozas.emit()

    def folyamatinditas(self):
        try:
            parancs = self.parancsepites()
        except Exception as hiba:
            self.kiir(t("hiba") + ": " + str(hiba))
            self.allapotvaltozas.emit()
            return
        if parancs is None:
            self.kiir(t("hiba_inditas"))
            self.allapotvaltozas.emit()
            return
        program, argumentumok = parancs
        if self.folyamat is not None:
            self.folyamat.deleteLater()
        self.leallitasjel += 1
        self.folyamat = QProcess(self)
        self.folyamat.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.folyamat.setWorkingDirectory(str(self.mappa))
        if self.tipus() == "bedrock" and os.name != "nt":
            kornyezet = QProcessEnvironment.systemEnvironment()
            kornyezet.insert("LD_LIBRARY_PATH", ".")
            self.folyamat.setProcessEnvironment(kornyezet)
        self.folyamat.readyReadStandardOutput.connect(self.kimenetolvasas)
        self.folyamat.finished.connect(self.folyamatvege)
        self.folyamat.errorOccurred.connect(self.folyamathiba)
        self.puffer = ""
        self.jatekosok = []
        self.jatekosvaltozas.emit()
        self.folyamat.start(program, argumentumok)
        backup = self.meta.get("backup", {})
        self.backupkovetkezo = time.monotonic() + max(1, int(backup.get("intervallum") or 30)) * 60
        if backup.get("engedelyezve", True) and backup.get("indulaskor", True):
            self.backupinditas()
        self.allapotvaltozas.emit()

    def kimenetolvasas(self):
        adat = bytes(self.folyamat.readAllStandardOutput()).decode("utf-8", errors="replace")
        self.puffer += adat
        sorok = self.puffer.split("\n")
        self.puffer = sorok.pop()
        for sor in sorok:
            self.sorfeldolgozas(sor)

    def sorfeldolgozas(self, sor):
        sor = ansiminta.sub("", sor).rstrip("\r")
        if not sor.strip():
            return
        self.kiir(sor)
        talalat = csatlakozasminta.search(sor)
        if talalat:
            nev = (talalat.group(1) or talalat.group(2) or "").strip()
            if nev and nev not in self.jatekosok:
                self.jatekosok.append(nev)
                if nev not in self.meta["jatekosok"]:
                    self.meta["jatekosok"].append(nev)
                    self.metamentese()
                self.jatekosvaltozas.emit()
            return
        talalat = kilepesminta.search(sor)
        if talalat:
            nev = (talalat.group(1) or talalat.group(2) or "").strip()
            if nev in self.jatekosok:
                self.jatekosok.remove(nev)
                self.jatekosvaltozas.emit()

    def folyamatvege(self, kod, kilepes):
        if self.puffer.strip():
            self.sorfeldolgozas(self.puffer)
        self.puffer = ""
        self.kiir(t("szerver_leallt", kod=kod))
        self.jatekosok = []
        self.jatekosvaltozas.emit()
        self.allapotvaltozas.emit()
        if self.ujrakeres:
            self.ujrakeres = False
            QTimer.singleShot(800, self.inditas)

    def folyamathiba(self, hiba):
        if hiba == QProcess.ProcessError.FailedToStart:
            self.kiir(t("hiba_inditas"))
            self.allapotvaltozas.emit()

    def parancs(self, szoveg):
        if self.fut():
            self.kiir("> " + szoveg)
            self.folyamat.write((szoveg + "\n").encode("utf-8"))

    def leallitas(self):
        if not self.fut():
            return
        self.leallitasjel += 1
        jel = self.leallitasjel
        self.folyamat.write(b"stop\n")
        ido = 15000 if self.tipus() == "pumpkin" else 45000
        QTimer.singleShot(ido, lambda: self.kenyszerleallitas(jel))

    def kenyszerleallitas(self, jel):
        if jel == self.leallitasjel and self.fut():
            self.folyamat.kill()

    def ujrainditas(self):
        if self.fut():
            self.ujrakeres = True
            self.leallitas()
        else:
            self.inditas()

    def memoria(self):
        if psutil is None or not self.fut():
            return 0
        azonosito = int(self.folyamat.processId())
        if azonosito <= 0:
            return 0
        try:
            folyamat = psutil.Process(azonosito)
            osszes = folyamat.memory_info().rss
            for gyerek in folyamat.children(recursive=True):
                try:
                    osszes += gyerek.memory_info().rss
                except Exception:
                    pass
            return int(osszes // (1024 * 1024))
        except Exception:
            return 0

    def playitkiir(self, szoveg):
        self.playitsorok.append(szoveg)
        if len(self.playitsorok) > 300:
            del self.playitsorok[:100]

    def playitinditas(self):
        if self.playitfut() or self.playitfoglalt:
            return
        self.playitfoglalt = True
        self.playitkilepes = False
        self.playitallapot = t("playit_letoltes")
        self.playitvaltozas.emit()
        hatterfeladat(playitletoltes, self.playitkesz, self.playithiba)

    def playitkesz(self, ut):
        self.playitfoglalt = False
        self.playitut = str(ut)
        self.playitfolyamatinditas()

    def playitclaiminditas(self):
        if self.playitfoglalt or self.playitkilepes:
            return
        kod = secrets.token_hex(5)
        self.playitclaim = "https://playit.gg/claim/" + kod
        self.playitfoglalt = True
        self.playitallapot = t("playit_kapcsolas")
        self.playitvaltozas.emit()
        QDesktopServices.openUrl(QUrl(self.playitclaim))
        hatterfeladat(
            lambda: playitkulcsigenyles(kod),
            self.playitkulcskesz,
            self.playithiba,
        )

    def playitkulcskesz(self, kulcs):
        if self.playitkilepes:
            self.playitfoglalt = False
            return
        try:
            self.playitkulcsfajl.parent.mkdir(parents=True, exist_ok=True)
            ideiglenes = self.playitkulcsfajl.with_suffix(".secret.tmp")
            ideiglenes.write_text(kulcs.strip() + "\n", encoding="utf-8")
            ideiglenes.replace(self.playitkulcsfajl)
        except OSError as hiba:
            self.playithiba(str(hiba))
            return
        self.playitclaim = ""
        self.playitfoglalt = False
        self.playitfolyamatinditas()

    def playithiba(self, uzenet):
        self.playitfoglalt = False
        self.playitallapot = t("playit_hiba", hiba=uzenet)
        self.playitvaltozas.emit()

    def playitfolyamatinditas(self):
        if self.playitfolyamat is not None and self.playitfut():
            return
        self.playitfolyamat = kulonterminal(
            self.playitut,
            ["--secret-path", str(self.playitkulcsfajl), "--socket-path", self.playitsocket],
            playitmappa,
            "Playit - " + self.meta.get("nev", "Minecraft server"),
        )
        self.playitallapot = t("playit_fut")
        self.playitvaltozas.emit()

    def playitolvasas(self):
        adat = bytes(self.playitfolyamat.readAllStandardOutput()).decode("utf-8", errors="replace")
        self.playitpuffer += adat
        sorok = re.split(r"[\r\n]+", self.playitpuffer)
        self.playitpuffer = sorok.pop()
        for sor in sorok:
            self.playitsorfeldolgozas(sor)
        self.playitvaltozas.emit()

    def playitsorfeldolgozas(self, sor):
        sor = ansiminta.sub("", sor).strip()
        if not sor:
            return
        self.playitkiir(sor)
        if "configured agent secret is no longer valid" in sor.lower():
            self.playitujrahitelesites = True
            if self.playitfolyamat is not None:
                self.playitfolyamat.kill()
        talalat = claimminta.search(sor)
        if talalat and talalat.group(0) != self.playitclaim:
            self.playitclaim = talalat.group(0)
            QDesktopServices.openUrl(QUrl(self.playitclaim))
        for cim in playitcimminta.findall(sor):
            cim = cim.lower()
            if cim.startswith("playit.") or cim.startswith("www."):
                continue
            self.playitclaim = ""
            if self.meta.get("playitcim") != cim:
                self.meta["playitcim"] = cim
                self.metamentese()
            break

    def playitvege(self, kod, kilepes):
        if self.playitujrahitelesites and not self.playitkilepes:
            self.playitujrahitelesites = False
            try:
                self.playitkulcsfajl.unlink(missing_ok=True)
            except OSError as hiba:
                self.playithiba(str(hiba))
                return
            self.playitclaiminditas()
            return
        self.playitallapot = t("playit_leallt")
        self.playitvaltozas.emit()

    def playitleallitas(self):
        self.playitkilepes = True
        if self.playitfut():
            self.playitfolyamat.terminate()
            try:
                self.playitfolyamat.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.playitfolyamat.kill()
        self.playitallapot = t("playit_leallt")
        self.playitvaltozas.emit()

    def playitcimmentes(self, szoveg):
        self.meta["playitcim"] = szoveg.strip()
        self.metamentese()

    def pinggyfut(self):
        return bool(self.pinggyfolyamatok) and all(folyamat.poll() is None for folyamat in self.pinggyfolyamatok)

    def pinggyszerveruzenet(self, kulcs):
        if self.meta.get("pinggyertesites", True):
            self.parancs("say " + t(kulcs))

    def pinggyinditas(self, tunnelek, ujrainditas=False):
        self.pinggyujraindul = False
        aktiv = [tunnel for tunnel in tunnelek if tunnel.get("engedelyezve")]
        if not aktiv:
            self.pinggyaktiv = False
            self.pinggyallapot = t("pinggy_all")
            self.playitvaltozas.emit()
            return
        if any(tunnel.get("tipus") == "udp" for tunnel in aktiv) and not pinggyprogram():
            self.pinggyaktiv = False
            self.pinggyallapot = t("pinggy_hianyzik")
            self.playitvaltozas.emit()
            return
        self.pinggyfolyamatleallitas()
        try:
            self.pinggyfolyamatok = []
            for index, tunnel in enumerate(aktiv):
                self.pinggyfolyamatok.append(pinggyterminal(tunnel, self.mappa, "Pinggy %d - %s" % (index + 1, self.meta.get("nev", "Minecraft server"))))
        except (OSError, RuntimeError) as hiba:
            self.pinggyfolyamatleallitas()
            self.pinggyaktiv = False
            self.pinggyallapot = t("playit_hiba", hiba=str(hiba))
            self.playitvaltozas.emit()
            return
        self.pinggyaktiv = True
        self.pinggyujraindul = False
        self.pinggyhatarido = time.monotonic() + 3600
        self.pinggyfigyelmeztetes10 = False
        self.pinggyfigyelmeztetes5 = False
        self.pinggyallapot = t("pinggy_fut")
        self.pinggyszerveruzenet("pinggy_ujraindult" if ujrainditas else "pinggy_elindult")
        self.playitvaltozas.emit()

    def pinggyfolyamatleallitas(self):
        for folyamat in self.pinggyfolyamatok:
            if folyamat.poll() is None:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(folyamat.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
                else:
                    try:
                        os.killpg(folyamat.pid, 15)
                    except (OSError, ProcessLookupError):
                        folyamat.terminate()
        self.pinggyfolyamatok = []

    def pinggyleallitas(self, kezi=True, uzenet=True):
        if kezi:
            self.pinggyaktiv = False
        self.pinggyfolyamatleallitas()
        self.pinggyallapot = t("pinggy_all")
        if uzenet:
            self.pinggyszerveruzenet("pinggy_leallt_uzenet")
        self.playitvaltozas.emit()

    def pinggyujrainditas(self):
        if self.pinggyujraindul:
            return
        self.pinggyujraindul = True
        self.pinggyaktiv = True
        self.pinggyszerveruzenet("pinggy_ujraindul")
        self.pinggyleallitas(False, False)
        tunnelek = self.meta.get("pinggy", [])
        QTimer.singleShot(1500, lambda: self.pinggyinditas(tunnelek, True) if self.pinggyaktiv else None)

    def pinggyfigyelo(self):
        if not self.pinggyaktiv:
            return
        if not self.pinggyfut():
            self.pinggyszerveruzenet("pinggy_leallt_uzenet")
            self.pinggyujrainditas()
            return
        hatralevo = self.pinggyhatarido - time.monotonic()
        if hatralevo <= 0:
            self.pinggyujrainditas()
            return
        if self.meta.get("pinggyertesites", True) and hatralevo <= 600 and not self.pinggyfigyelmeztetes10:
            self.parancs("say " + t("pinggy_lejar_10"))
            self.pinggyfigyelmeztetes10 = True
        if self.meta.get("pinggyertesites", True) and hatralevo <= 300 and not self.pinggyfigyelmeztetes5:
            self.parancs("say " + t("pinggy_lejar_5"))
            self.pinggyfigyelmeztetes5 = True

    def backupinditas(self, kezi=False):
        backup = self.meta.get("backup", {})
        if self.backupfolyamatban or (not kezi and not backup.get("engedelyezve", True)):
            return
        self.backupfolyamatban = True
        hatterfeladat(
            lambda: backupkeszites(self.mappa, self.tipus(), backup),
            self.backupkesz,
            self.backuphiba,
        )

    def backupkesz(self, fajl):
        self.backupfolyamatban = False
        self.backupkovetkezo = time.monotonic() + max(1, int(self.meta.get("backup", {}).get("intervallum") or 30)) * 60
        self.kiir(t("backup_kesz", fajl=Path(fajl).name))
        self.allapotvaltozas.emit()

    def backuphiba(self, uzenet):
        self.backupfolyamatban = False
        self.kiir(t("backup_hiba", hiba=uzenet))
        self.allapotvaltozas.emit()

    def backupfigyelo(self):
        backup = self.meta.get("backup", {})
        if not self.fut() or not backup.get("engedelyezve", True) or int(backup.get("intervallum") or 0) <= 0:
            return
        if time.monotonic() >= self.backupkovetkezo:
            self.backupinditas()


class beallitasszerkeszto(QWidget):
    def __init__(self, tipus, szulo=None):
        super().__init__(szulo)
        self.tipus = tipus
        self.sema = bedrockschema if tipus == "bedrock" else javaschema
        self.mezok = {}
        self.ramdoboz = None
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        tabok = QTabWidget()
        fo.addWidget(tabok)
        csoportok = []
        for elem in self.sema:
            if elem[4] not in csoportok:
                csoportok.append(elem[4])
        for csoport in csoportok:
            oldal = QWidget()
            urlap = QFormLayout(oldal)
            urlap.setContentsMargins(12, 12, 12, 12)
            if csoport == "general" and tipus != "bedrock":
                self.ramdoboz = QSpinBox()
                self.ramdoboz.setRange(512, 262144)
                self.ramdoboz.setSingleStep(256)
                self.ramdoboz.setSuffix(" MB")
                self.ramdoboz.setValue(2048)
                urlap.addRow(t("ram") + ":", self.ramdoboz)
            for kulcs, mezotipus, alap, extra, mezocsoport in self.sema:
                if mezocsoport != csoport:
                    continue
                mezo = self.mezokeszites(mezotipus, alap, extra)
                mezo.setToolTip(kulcs)
                self.mezok[kulcs] = mezo
                cimke = QLabel(mezofelirat(kulcs) + ":")
                cimke.setToolTip(kulcs)
                urlap.addRow(cimke, mezo)
            gorgeto = QScrollArea()
            gorgeto.setWidgetResizable(True)
            gorgeto.setFrameShape(QFrame.Shape.NoFrame)
            gorgeto.setWidget(oldal)
            tabok.addTab(gorgeto, t("g_" + csoport))

    def mezokeszites(self, mezotipus, alap, extra):
        if mezotipus == "b":
            mezo = QCheckBox()
            mezo.setChecked(bool(alap))
        elif mezotipus == "i":
            mezo = QSpinBox()
            mezo.setRange(extra[0], extra[1])
            mezo.setValue(alap)
        elif mezotipus == "c":
            mezo = QComboBox()
            mezo.addItems(extra)
            mezo.setCurrentText(alap)
        else:
            mezo = QLineEdit(alap)
        return mezo

    def ram(self):
        if self.ramdoboz is None:
            return 0
        return int(self.ramdoboz.value())

    def ramallitas(self, ertek):
        if self.ramdoboz is not None:
            self.ramdoboz.setValue(int(ertek))

    def ertekek(self, verzio=""):
        adat = {}
        for kulcs, mezotipus, alap, extra, csoport in self.sema:
            mezo = self.mezok[kulcs]
            if mezotipus == "b":
                ertek = "true" if mezo.isChecked() else "false"
            elif mezotipus == "i":
                ertek = str(mezo.value())
            elif mezotipus == "c":
                ertek = mezo.currentText()
            else:
                ertek = mezo.text().replace("\n", " ").strip()
            if kulcs == "level-type":
                ertek = leveltipus(ertek, verzio)
            adat[kulcs] = ertek
        return adat

    def feltoltes(self, adat):
        for kulcs, mezotipus, alap, extra, csoport in self.sema:
            if kulcs not in adat:
                continue
            ertek = adat[kulcs]
            mezo = self.mezok[kulcs]
            if mezotipus == "b":
                mezo.setChecked(ertek.strip().lower() == "true")
            elif mezotipus == "i":
                try:
                    mezo.setValue(int(ertek))
                except ValueError:
                    pass
            elif mezotipus == "c":
                if kulcs == "level-type":
                    ertek = leveltipus(ertek, "")
                index = mezo.findText(ertek)
                if index >= 0:
                    mezo.setCurrentIndex(index)
            else:
                mezo.setText(ertek)


class keszitomunka(QThread):
    uzenet = Signal(str)
    haladas = Signal(int)
    vege = Signal(bool, str)

    def __init__(self, adatok, szulo=None):
        super().__init__(szulo)
        self.adatok = adatok

    def run(self):
        try:
            self.keszites()
            self.vege.emit(True, "")
        except Exception as hiba:
            shutil.rmtree(self.adatok["mappa"], ignore_errors=True)
            self.vege.emit(False, str(hiba) or repr(hiba))

    def telepitofuttatas(self, java, jar, mappa):
        kapcsolok = {}
        if os.name == "nt":
            kapcsolok["creationflags"] = 0x08000000
        folyamat = subprocess.Popen(
            [str(java), "-jar", jar, "--installServer"],
            cwd=str(mappa),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            **kapcsolok
        )
        utolsok = []
        for sor in folyamat.stdout:
            sor = sor.strip()
            if sor:
                utolsok.append(sor)
                utolsok = utolsok[-15:]
                self.uzenet.emit(sor[:120])
        kod = folyamat.wait()
        if kod != 0:
            raise RuntimeError(t("telepito_hiba") + "\n" + "\n".join(utolsok))

    def keszites(self):
        adat = self.adatok
        tipus = adat["tipus"]
        verzio = adat["verzio"]
        mappa = adat["mappa"]
        mappa.mkdir(parents=True)
        meta = {
            "nev": adat["nev"],
            "tipus": tipus,
            "verzio": verzio,
            "ram": adat["ram"],
            "java": 0,
            "fajl": "",
            "playitcim": "",
            "alagut": "off",
            "pinggy": [{"engedelyezve": True, "tipus": "udp" if tipus == "bedrock" else "tcp", "port": 19133 if tipus == "bedrock" else 25565, "jelszo": ""}, {"engedelyezve": False, "tipus": "udp", "port": 19133 if tipus == "bedrock" else 25565, "jelszo": ""}, {"engedelyezve": False, "tipus": "http", "port": 8000, "jelszo": ""}],
            "letrehozva": datetime.now().isoformat(timespec="seconds"),
        }
        javas = tipus in javatipusok
        foverzio = 0
        if javas:
            foverzio = javafoverzio(verzio)
            if foverzio == 16:
                foverzio = 17
            meta["java"] = foverzio
            self.uzenet.emit(t("java_letoltes", verzio=foverzio))
            self.haladas.emit(0)
            javaletoltes(foverzio, self.haladas.emit)
        self.uzenet.emit(t("jar_letoltes"))
        self.haladas.emit(0)
        cel = mappa / "server.jar"
        if tipus == "vanilla":
            url = mojangverzioadat(verzio)["downloads"]["server"]["url"]
            fajlletoltes(url, cel, self.haladas.emit)
            meta["fajl"] = "server.jar"
        elif tipus == "paper":
            paperjar(verzio, cel, self.haladas.emit)
            meta["fajl"] = "server.jar"
        elif tipus == "purpur":
            purpurjar(verzio, cel, self.haladas.emit)
            meta["fajl"] = "server.jar"
        elif tipus == "fabric":
            fabricjar(verzio, cel, self.haladas.emit)
            meta["fajl"] = "server.jar"
        elif tipus in ("forge", "neoforge"):
            if tipus == "forge":
                forgever = forgeverzio(verzio)
                if not forgever:
                    raise RuntimeError("Forge " + verzio)
                nev = "%s-%s" % (verzio, forgever)
                url = "https://maven.minecraftforge.net/net/minecraftforge/forge/%s/forge-%s-installer.jar" % (nev, nev)
            else:
                neover = neoforgeverzio(verzio)
                if not neover:
                    raise RuntimeError("NeoForge " + verzio)
                url = "https://maven.neoforged.net/releases/net/neoforged/neoforge/%s/neoforge-%s-installer.jar" % (neover, neover)
            fajlletoltes(url, mappa / "installer.jar", self.haladas.emit)
            self.uzenet.emit(t("telepites"))
            self.haladas.emit(-1)
            self.telepitofuttatas(javautvonal(foverzio), "installer.jar", mappa)
            self.haladas.emit(100)
            (mappa / "installer.jar").unlink(missing_ok=True)
            (mappa / "installer.jar.log").unlink(missing_ok=True)
        elif tipus == "bedrock":
            url, bedrockver = bedrockadat()
            meta["verzio"] = bedrockver
            zipcel = mappa / "bedrock.zip"
            fajlletoltes(url, zipcel, self.haladas.emit)
            with zipfile.ZipFile(zipcel) as archivum:
                archivum.extractall(mappa)
            zipcel.unlink(missing_ok=True)
            futtathato = mappa / ("bedrock_server.exe" if os.name == "nt" else "bedrock_server")
            if os.name != "nt" and futtathato.exists():
                futtathato.chmod(0o755)
        elif tipus == "pumpkin":
            kiadas = pumpkinkiadas()
            eszkoz = eszkozvalasztas(kiadas["assets"])
            if not eszkoz:
                raise RuntimeError("PumpkinMC binary not found for this platform")
            nev = "pumpkin.exe" if os.name == "nt" else "pumpkin"
            fajlletoltes(eszkoz["browser_download_url"], mappa / nev, self.haladas.emit)
            if os.name != "nt":
                (mappa / nev).chmod(0o755)
            meta["fajl"] = nev
            meta["verzio"] = "latest"
        self.uzenet.emit(t("konfig_iras"))
        if javas:
            (mappa / "eula.txt").write_text("eula=true\n", encoding="utf-8")
            tulajdonsagiras(mappa / "server.properties", adat["ertekek"], True)
        elif tipus == "bedrock":
            tulajdonsagiras(mappa / "server.properties", adat["ertekek"], False)
        metamentes(mappa, meta)


class letrehozoablak(QDialog):
    def __init__(self, szulo=None):
        super().__init__(szulo)
        self.setWindowTitle(t("szerver_letrehozasa"))
        self.resize(820, 760)
        self.munkas = None
        self.betoltesjel = 0
        fo = QVBoxLayout(self)
        urlap = QFormLayout()
        self.nevmezo = QLineEdit()
        self.tipusdoboz = QComboBox()
        for kulcs in tipusnevek:
            self.tipusdoboz.addItem(tipusfelirat(kulcs), kulcs)
        self.verziodoboz = QComboBox()
        self.verziocimke = QLabel()
        verziosor = QHBoxLayout()
        verziosor.addWidget(self.verziodoboz, 1)
        verziosor.addWidget(self.verziocimke)
        urlap.addRow(t("nev") + ":", self.nevmezo)
        urlap.addRow(t("tipus") + ":", self.tipusdoboz)
        urlap.addRow(t("verzio") + ":", verziosor)
        fo.addLayout(urlap)
        self.pumpkincimke = QLabel(t("pumpkin_fejlesztes") + "\n" + t("pumpkin_gep") + "\n" + t("pumpkin_kezi"))
        self.pumpkincimke.setObjectName("figyelmeztetes")
        self.pumpkincimke.setWordWrap(True)
        fo.addWidget(self.pumpkincimke)
        self.szerkesztok = QStackedWidget()
        self.javaszerkeszto = beallitasszerkeszto("java")
        self.bedrockszerkeszto = beallitasszerkeszto("bedrock")
        self.szerkesztok.addWidget(self.javaszerkeszto)
        self.szerkesztok.addWidget(self.bedrockszerkeszto)
        self.szerkesztok.addWidget(QWidget())
        fo.addWidget(self.szerkesztok, 1)
        self.eulacsekk = QCheckBox(t("eula_elfogadas"))
        fo.addWidget(self.eulacsekk)
        self.haladassav = QProgressBar()
        self.haladassav.setVisible(False)
        self.uzenetcimke = QLabel()
        self.uzenetcimke.setVisible(False)
        fo.addWidget(self.uzenetcimke)
        fo.addWidget(self.haladassav)
        gombsor = QHBoxLayout()
        gombsor.addStretch()
        self.megsemgomb = QPushButton(t("megse"))
        self.letrehozgomb = QPushButton(t("letrehozas"))
        self.letrehozgomb.setObjectName("elsodleges")
        self.megsemgomb.clicked.connect(self.reject)
        self.letrehozgomb.clicked.connect(self.keszites)
        gombsor.addWidget(self.megsemgomb)
        gombsor.addWidget(self.letrehozgomb)
        fo.addLayout(gombsor)
        self.tipusdoboz.currentIndexChanged.connect(self.tipusvaltas)
        self.tipusvaltas()

    def tipusvaltas(self):
        kulcs = self.tipusdoboz.currentData()
        self.pumpkincimke.setVisible(kulcs == "pumpkin")
        if kulcs == "bedrock":
            self.szerkesztok.setCurrentIndex(1)
        elif kulcs == "pumpkin":
            self.szerkesztok.setCurrentIndex(2)
        else:
            self.szerkesztok.setCurrentIndex(0)
        self.eulacsekk.setVisible(kulcs in javatipusok)
        self.verziokbetoltese()

    def verziokbetoltese(self):
        kulcs = self.tipusdoboz.currentData()
        self.betoltesjel += 1
        jel = self.betoltesjel
        self.verziodoboz.clear()
        if kulcs == "pumpkin":
            self.verziodoboz.addItem(t("legfrissebb"), "latest")
            self.verziodoboz.setEnabled(False)
            self.verziocimke.setText("")
            self.letrehozgomb.setEnabled(True)
            return
        self.verziodoboz.setEnabled(False)
        self.letrehozgomb.setEnabled(False)
        self.verziocimke.setText(t("verzio_betoltes"))
        if kulcs == "bedrock":
            fuggveny = lambda: [bedrockadat()[1]]
        else:
            fuggveny = lambda: verziolista(kulcs)
        hatterfeladat(
            fuggveny,
            lambda lista, azonosito=jel, tipus=kulcs: self.verziokkesz(lista, azonosito, tipus),
            lambda hiba, azonosito=jel: self.verziohiba(hiba, azonosito),
        )

    def verziokkesz(self, lista, jel, tipus):
        if jel != self.betoltesjel or self.munkas is not None:
            return
        self.verziodoboz.clear()
        for ver in lista:
            self.verziodoboz.addItem(ver, ver)
        self.verziodoboz.setEnabled(tipus != "bedrock" and bool(lista))
        self.letrehozgomb.setEnabled(bool(lista))
        self.verziocimke.setText("")

    def verziohiba(self, uzenet, jel):
        if jel != self.betoltesjel:
            return
        self.verziocimke.setText(t("verzio_hiba", hiba=uzenet))

    def reject(self):
        if self.munkas is not None and self.munkas.isRunning():
            return
        super().reject()

    def zarolas(self, zarolt):
        for elem in (self.nevmezo, self.tipusdoboz, self.verziodoboz, self.szerkesztok, self.eulacsekk, self.letrehozgomb, self.megsemgomb):
            elem.setEnabled(not zarolt)

    def keszites(self):
        nev = self.nevmezo.text().strip()
        if not nev:
            QMessageBox.warning(self, t("figyelem"), t("nev_hianyzik"))
            return
        mappanev = re.sub(r'[\\/:*?"<>|]', "_", nev).strip(" .")
        if not mappanev:
            QMessageBox.warning(self, t("figyelem"), t("nev_hianyzik"))
            return
        mappa = szerverekmappa / mappanev
        if mappa.exists():
            QMessageBox.warning(self, t("figyelem"), t("nev_foglalt"))
            return
        tipus = self.tipusdoboz.currentData()
        verzio = self.verziodoboz.currentData() or self.verziodoboz.currentText()
        if not verzio:
            return
        if tipus in javatipusok and not self.eulacsekk.isChecked():
            QMessageBox.warning(self, t("figyelem"), t("eula_kell"))
            return
        if tipus == "bedrock":
            ertekek = self.bedrockszerkeszto.ertekek()
            ram = 0
        elif tipus == "pumpkin":
            ertekek = {}
            ram = 0
        else:
            ertekek = self.javaszerkeszto.ertekek(verzio)
            ram = self.javaszerkeszto.ram()
        adatok = {"nev": nev, "mappa": mappa, "tipus": tipus, "verzio": verzio, "ram": ram, "ertekek": ertekek}
        self.zarolas(True)
        self.haladassav.setVisible(True)
        self.haladassav.setRange(0, 100)
        self.haladassav.setValue(0)
        self.uzenetcimke.setVisible(True)
        self.uzenetcimke.setText(t("keszul"))
        self.munkas = keszitomunka(adatok, self)
        self.munkas.uzenet.connect(self.uzenetcimke.setText)
        self.munkas.haladas.connect(self.haladaskezeles)
        self.munkas.vege.connect(self.munkavege)
        self.munkas.start()

    def haladaskezeles(self, ertek):
        if ertek < 0:
            self.haladassav.setRange(0, 0)
        else:
            self.haladassav.setRange(0, 100)
            self.haladassav.setValue(ertek)

    def munkavege(self, sikeres, uzenet):
        self.munkas.wait()
        self.munkas = None
        if sikeres:
            self.accept()
            return
        self.zarolas(False)
        self.haladassav.setVisible(False)
        self.uzenetcimke.setVisible(False)
        QMessageBox.critical(self, t("hiba"), uzenet)


class iranyitooldal(QWidget):
    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        tipus = szerver.tipus()
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        gombok = QHBoxLayout()
        self.startgomb = QPushButton(t("start"))
        self.startgomb.setObjectName("zold")
        self.stopgomb = QPushButton(t("stop"))
        self.stopgomb.setObjectName("piros")
        self.ujragomb = QPushButton(t("restart"))
        self.startgomb.clicked.connect(szerver.inditas)
        self.stopgomb.clicked.connect(szerver.leallitas)
        self.ujragomb.clicked.connect(szerver.ujrainditas)
        gombok.addWidget(self.startgomb)
        gombok.addWidget(self.stopgomb)
        gombok.addWidget(self.ujragomb)
        gombok.addStretch()
        fo.addLayout(gombok)
        if tipus == "pumpkin":
            figyelmeztetes = QLabel(t("pumpkin_fejlesztes") + " " + t("pumpkin_gep") + " " + t("pumpkin_kezi"))
            figyelmeztetes.setObjectName("figyelmeztetes")
            figyelmeztetes.setWordWrap(True)
            fo.addWidget(figyelmeztetes)
            mappagomb = QPushButton(t("pumpkin_mappa"))
            mappagomb.clicked.connect(lambda: mappamegnyitas(szerver.mappa))
            fo.addWidget(mappagomb, 0, Qt.AlignmentFlag.AlignLeft)
        self.konzol = QPlainTextEdit()
        self.konzol.setObjectName("konzol")
        self.konzol.setReadOnly(True)
        self.konzol.setMaximumBlockCount(5000)
        self.konzol.setPlainText("\n".join(szerver.sorok))
        fo.addWidget(self.konzol, 1)
        beviteli = QHBoxLayout()
        self.beviteli = QLineEdit()
        self.beviteli.setPlaceholderText(t("konzol_bevitel"))
        self.kuldgomb = QPushButton(t("kuldes"))
        self.beviteli.returnPressed.connect(self.kuldes)
        self.kuldgomb.clicked.connect(self.kuldes)
        beviteli.addWidget(self.beviteli, 1)
        beviteli.addWidget(self.kuldgomb)
        fo.addLayout(beviteli)
        memoriadoboz = QGroupBox(t("memoria"))
        memoriaelrendezes = QHBoxLayout(memoriadoboz)
        self.memoriasav = QProgressBar()
        self.memoriasav.setTextVisible(False)
        self.memoriacimke = QLabel("0 MB")
        memoriaelrendezes.addWidget(self.memoriasav, 1)
        memoriaelrendezes.addWidget(self.memoriacimke)
        fo.addWidget(memoriadoboz)
        playitdoboz = QGroupBox(t("playit_doboz"))
        playitelrendezes = QVBoxLayout(playitdoboz)
        playitsor = QHBoxLayout()
        self.playitgomb = QPushButton(t("playit_be"))
        self.playitgomb.clicked.connect(self.playitvaltas)
        self.playitcimke = QLabel()
        playitsor.addWidget(self.playitgomb)
        playitsor.addWidget(self.playitcimke, 1)
        playitelrendezes.addLayout(playitsor)
        self.claimcimke = QLabel()
        self.claimcimke.setOpenExternalLinks(True)
        self.claimcimke.setVisible(False)
        playitelrendezes.addWidget(self.claimcimke)
        cimsor = QHBoxLayout()
        cimsor.addWidget(QLabel(t("playit_cim")))
        self.cimmezo = QLineEdit(szerver.meta.get("playitcim", ""))
        self.cimmezo.setPlaceholderText(t("playit_cim_tipp"))
        self.cimmezo.editingFinished.connect(self.cimmentes)
        masolasgomb = QPushButton(t("masolas"))
        masolasgomb.clicked.connect(self.cimmasolas)
        cimsor.addWidget(self.cimmezo, 1)
        cimsor.addWidget(masolasgomb)
        playitelrendezes.addLayout(cimsor)
        tipp = QLabel(t("playit_tipp", port=szerver.portszam()))
        tipp.setObjectName("halvany")
        tipp.setWordWrap(True)
        playitelrendezes.addWidget(tipp)
        fo.addWidget(playitdoboz)
        szolgaltatosor = QHBoxLayout()
        szolgaltatosor.addWidget(QLabel(t("alagut_mindketto")))
        infogomb = QPushButton("ⓘ")
        infogomb.setToolTip(t("pinggy_info"))
        infogomb.clicked.connect(lambda: QMessageBox.information(self, t("alagut_valaszto"), t("pinggy_info") + "\n\n" + t("svc_info")))
        szolgaltatosor.addWidget(infogomb)
        szolgaltatosor.addStretch()
        fo.addLayout(szolgaltatosor)
        pinggydoboz = QGroupBox(t("pinggy_doboz"))
        pinggyelrendezes = QVBoxLayout(pinggydoboz)
        self.pinggymezok = []
        for index in range(3):
            adat = szerver.meta.get("pinggy", [])[index]
            sor = QHBoxLayout()
            engedelyezve = QCheckBox(str(index + 1))
            engedelyezve.setChecked(bool(adat.get("engedelyezve")))
            tipusdoboz = QComboBox()
            tipusdoboz.addItem("TCP", "tcp")
            tipusdoboz.addItem("UDP / Bedrock", "udp")
            tipusdoboz.addItem("HTTP", "http")
            tipusdoboz.setCurrentIndex(max(0, tipusdoboz.findData(adat.get("tipus", "tcp"))))
            portmezo = QSpinBox()
            portmezo.setRange(1, 65535)
            portmezo.setValue(int(adat.get("port") or 25565))
            sor.addWidget(engedelyezve)
            sor.addWidget(tipusdoboz)
            sor.addWidget(QLabel(t("pinggy_port") + ":"))
            sor.addWidget(portmezo)
            pinggyelrendezes.addLayout(sor)
            self.pinggymezok.append((engedelyezve, tipusdoboz, portmezo))
            engedelyezve.toggled.connect(self.pinggymentese)
            tipusdoboz.currentIndexChanged.connect(self.pinggymentese)
            portmezo.valueChanged.connect(self.pinggymentese)
        self.pinggyparancs = QLabel()
        self.pinggyparancs.setObjectName("halvany")
        self.pinggyparancs.setWordWrap(True)
        pinggyelrendezes.addWidget(self.pinggyparancs)
        pinggytipp = QLabel(t("pinggy_tipp") + "\n" + t("pinggy_window") + "\n" + t("svc_info"))
        pinggytipp.setWordWrap(True)
        pinggytipp.setObjectName("halvany")
        pinggyelrendezes.addWidget(pinggytipp)
        pinggybinarissor = QHBoxLayout()
        pinggybinarissor.addWidget(QLabel(t("pinggy_binaris")))
        self.pinggybinarisallapot = QLabel()
        self.pinggybinarisallapot.setObjectName("halvany")
        pinggybinarissor.addWidget(self.pinggybinarisallapot, 1)
        linkcimke = QLabel('<a href="https://pinggy.io/cli/">https://pinggy.io/cli/</a>')
        linkcimke.setOpenExternalLinks(True)
        pinggybinarissor.addWidget(linkcimke)
        letoltesgomb = QPushButton(t("pinggy_letoltes"))
        letoltesgomb.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://pinggy.io/cli/")))
        pinggybinarissor.addWidget(letoltesgomb)
        importgomb = QPushButton(t("pinggy_import"))
        importgomb.clicked.connect(self.pinggybinarisimport)
        pinggybinarissor.addWidget(importgomb)
        torlesgomb = QPushButton(t("pinggy_torles"))
        torlesgomb.clicked.connect(self.pinggybinaristorles)
        pinggybinarissor.addWidget(torlesgomb)
        pinggyelrendezes.addLayout(pinggybinarissor)
        pinggygombsor = QHBoxLayout()
        self.pinggygomb = QPushButton(t("pinggy_indit"))
        self.pinggygomb.clicked.connect(self.pinggyvaltas)
        pinggygombsor.addWidget(self.pinggygomb)
        self.pinggyujragomb = QPushButton(t("pinggy_ujra"))
        self.pinggyujragomb.clicked.connect(self.pinggyujrainditas)
        pinggygombsor.addWidget(self.pinggyujragomb)
        pinggygombsor.addStretch()
        pinggyelrendezes.addLayout(pinggygombsor)
        self.pinggyertesites = QCheckBox(t("pinggy_ertesites"))
        self.pinggyertesites.setChecked(szerver.meta.get("pinggyertesites", True))
        self.pinggyertesites.toggled.connect(self.pinggyertesitesmentese)
        pinggyelrendezes.addWidget(self.pinggyertesites)
        self.pinggyallapot = QLabel()
        self.pinggyallapot.setObjectName("halvany")
        pinggyelrendezes.addWidget(self.pinggyallapot)
        fo.addWidget(pinggydoboz)
        pingdoboz = QGroupBox(t("ping_doboz"))
        pingelrendezes = QHBoxLayout(pingdoboz)
        self.pinggomb = QPushButton(t("ping_gomb"))
        self.pinggomb.clicked.connect(self.pingteszt)
        self.pingeredmeny = QLabel("")
        pingelrendezes.addWidget(self.pinggomb)
        pingelrendezes.addWidget(self.pingeredmeny, 1)
        fo.addWidget(pingdoboz)
        szerver.sorkesz.connect(self.konzolsor)
        szerver.allapotvaltozas.connect(self.frissit)
        szerver.playitvaltozas.connect(self.playitfrissites)
        self.idozito = QTimer(self)
        self.idozito.timeout.connect(self.memoriafrissites)
        self.idozito.start(2000)
        self.frissit()
        self.memoriafrissites()
        self.pinggymentese()
        self.pinggybinarisfrissitese()

    def konzolsor(self, sor):
        self.konzol.appendPlainText(sor)

    def kuldes(self):
        szoveg = self.beviteli.text().strip()
        if szoveg:
            self.szerver.parancs(szoveg)
        self.beviteli.clear()

    def frissit(self):
        fut = self.szerver.fut()
        foglalt = self.szerver.javafoglalt
        self.startgomb.setEnabled(not fut and not foglalt)
        self.stopgomb.setEnabled(fut)
        self.ujragomb.setEnabled(fut)
        self.beviteli.setEnabled(fut)
        self.kuldgomb.setEnabled(fut)
        self.playitfrissites()

    def memoriafrissites(self):
        if psutil is None:
            self.memoriacimke.setText(t("nincs_psutil"))
            return
        hasznalt = self.szerver.memoria()
        osszes = int(self.szerver.meta.get("ram") or 0) if self.szerver.tipus() in javatipusok else 0
        if osszes > 0:
            self.memoriasav.setRange(0, osszes)
            self.memoriasav.setValue(min(hasznalt, osszes))
            szazalek = int(hasznalt * 100 / osszes)
            self.memoriacimke.setText("%d / %d MB (%d%%)" % (hasznalt, osszes, szazalek))
        else:
            self.memoriasav.setRange(0, 1)
            self.memoriasav.setValue(0)
            self.memoriacimke.setText("%d MB" % hasznalt)

    def playitvaltas(self):
        if self.szerver.playitfut():
            self.szerver.playitleallitas()
        else:
            self.szerver.playitinditas()

    def pinggyadatok(self):
        eredmeny = []
        for engedelyezve, tipusdoboz, portmezo in self.pinggymezok:
            eredmeny.append({"engedelyezve": engedelyezve.isChecked(), "tipus": tipusdoboz.currentData(), "port": portmezo.value(), "jelszo": ""})
        return eredmeny

    def pinggymentese(self):
        adat = self.pinggyadatok()
        self.szerver.meta["pinggy"] = adat
        self.szerver.metamentese()
        parancsok = []
        for tunnel in adat:
            if tunnel["engedelyezve"]:
                program, argumentumok = pinggyparancs(tunnel)
                parancsok.append(program + " " + " ".join(argumentumok))
        self.pinggyparancs.setText(t("pinggy_parancsok") + ":\n" + "\n".join(parancsok))

    def pinggyvaltas(self):
        if self.szerver.pinggyfut():
            self.szerver.pinggyleallitas()
        else:
            self.pinggymentese()
            self.szerver.pinggyinditas(self.szerver.meta.get("pinggy", []))
        self.playitfrissites()

    def pinggyujrainditas(self):
        self.pinggymentese()
        self.szerver.pinggyujrainditas()

    def pinggybinarisfrissitese(self):
        if pinggyprogram():
            self.pinggybinarisallapot.setText(str(Path(pinggyprogram()).name))
        else:
            self.pinggybinarisallapot.setText(t("pinggy_nincs"))

    def pinggybinarisimport(self):
        if self.szerver.pinggyfut():
            QMessageBox.warning(self, t("figyelem"), t("elobb_alljon_le"))
            return
        fajl, _ = QFileDialog.getOpenFileName(self, t("pinggy_import"), str(Path.home()), "Executable (*)")
        if not fajl:
            return
        try:
            cel = pinggyimportal(fajl)
        except OSError as hiba:
            QMessageBox.critical(self, t("hiba"), str(hiba))
            return
        self.pinggybinarisfrissitese()
        self.pinggyallapot.setText(t("pinggy_import_ok", fajl=cel.name))

    def pinggybinaristorles(self):
        if self.szerver.pinggyfut():
            QMessageBox.warning(self, t("figyelem"), t("elobb_alljon_le"))
            return
        if not pinggyimportalttorles():
            self.pinggybinarisfrissitese()
            return
        self.pinggybinarisfrissitese()
        self.pinggyallapot.setText(t("pinggy_torles_ok"))

    def pinggyertesitesmentese(self, engedelyezve):
        self.szerver.meta["pinggyertesites"] = engedelyezve
        self.szerver.metamentese()

    def playitfrissites(self):
        fut = self.szerver.playitfut()
        self.playitgomb.setText(t("playit_ki") if fut else t("playit_be"))
        self.playitgomb.setEnabled(not self.szerver.playitfoglalt)
        self.playitcimke.setText(self.szerver.playitallapot or t("playit_nincs"))
        if self.szerver.playitclaim:
            self.claimcimke.setText('<a href="%s">%s</a>' % (self.szerver.playitclaim, t("playit_claim")))
            self.claimcimke.setVisible(True)
        else:
            self.claimcimke.setVisible(False)
        cim = self.szerver.meta.get("playitcim", "")
        if cim and self.cimmezo.text() != cim and not self.cimmezo.hasFocus():
            self.cimmezo.setText(cim)
        if hasattr(self, "pinggygomb"):
            self.pinggygomb.setText(t("pinggy_leallit") if self.szerver.pinggyfut() else t("pinggy_indit"))
            self.pinggymentese()
            self.pinggyallapot.setText(t("pinggy_allapot") + ": " + (self.szerver.pinggyallapot or t("pinggy_all")))

    def cimmentes(self):
        self.szerver.playitcimmentes(self.cimmezo.text())

    def cimmasolas(self):
        QApplication.clipboard().setText(self.cimmezo.text().strip())

    def pingteszt(self):
        szoveg = self.cimmezo.text().strip()
        if not szoveg:
            self.pingeredmeny.setText(t("ping_nincs_cim"))
            return
        self.szerver.playitcimmentes(szoveg)
        bedrock = self.szerver.tipus() == "bedrock"
        host, port = cimfelbontas(szoveg, 19132 if bedrock else 25565)
        self.pinggomb.setEnabled(False)
        self.pingeredmeny.setText(t("ping_mero"))
        hatterfeladat(lambda: pingmeres(host, port, bedrock), self.pingkesz, self.pinghiba)

    def pingkesz(self, eredmeny):
        atlag, legkisebb, legnagyobb = eredmeny
        self.pinggomb.setEnabled(True)
        self.pingeredmeny.setText(t("ping_eredmeny", atlag=int(round(atlag)), legkisebb=int(round(legkisebb)), legnagyobb=int(round(legnagyobb))))

    def pinghiba(self, uzenet):
        self.pinggomb.setEnabled(True)
        self.pingeredmeny.setText(t("ping_hiba", hiba=uzenet))


class vilagoldal(QWidget):
    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        self.bedrock = szerver.tipus() == "bedrock"
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        self.nevcimke = QLabel()
        self.nevcimke.setObjectName("alcim")
        fo.addWidget(self.nevcimke)
        fo.addWidget(QLabel(t("vilag_seed")))
        self.seedmezo = QLineEdit()
        fo.addWidget(self.seedmezo)
        self.ujragomb = QPushButton(t("vilag_ujra"))
        self.ujragomb.setObjectName("piros")
        self.ujragomb.clicked.connect(self.ujragenerals)
        fo.addWidget(self.ujragomb, 0, Qt.AlignmentFlag.AlignLeft)
        fo.addSpacing(12)
        sor = QHBoxLayout()
        self.mappagomb = QPushButton(t("vilag_mappa_feltoltes"))
        self.zipgomb = QPushButton(t("vilag_zip_feltoltes"))
        self.mentesgomb = QPushButton(t("vilag_mentes"))
        self.megnyitasgomb = QPushButton(t("vilag_megnyitas"))
        self.mappagomb.clicked.connect(self.mappafeltoltes)
        self.zipgomb.clicked.connect(self.zipfeltoltes)
        self.mentesgomb.clicked.connect(self.mentes)
        self.megnyitasgomb.clicked.connect(self.vilagmegnyitas)
        for gomb in (self.mappagomb, self.zipgomb, self.mentesgomb, self.megnyitasgomb):
            sor.addWidget(gomb)
        sor.addStretch()
        fo.addLayout(sor)
        self.allapotcimke = QLabel("")
        self.allapotcimke.setObjectName("halvany")
        fo.addWidget(self.allapotcimke)
        fo.addStretch()

    def tulajdonsagfajl(self):
        return self.szerver.mappa / "server.properties"

    def tulajdonsagok(self):
        return tulajdonsagolvasas(self.tulajdonsagfajl(), not self.bedrock)

    def vilagnev(self):
        alap = "Bedrock level" if self.bedrock else "world"
        return self.tulajdonsagok().get("level-name", alap)

    def vilagmappak(self):
        nev = self.vilagnev()
        if self.bedrock:
            return [self.szerver.mappa / "worlds" / nev]
        return [self.szerver.mappa / nev, self.szerver.mappa / (nev + "_nether"), self.szerver.mappa / (nev + "_the_end")]

    def frissit(self):
        self.nevcimke.setText(t("vilag_nev", nev=self.vilagnev()))
        self.seedmezo.setText(self.tulajdonsagok().get("level-seed", ""))

    def leallitva(self):
        if self.szerver.fut():
            QMessageBox.warning(self, t("figyelem"), t("elobb_alljon_le"))
            return False
        return True

    def ujragenerals(self):
        if not self.leallitva():
            return
        if QMessageBox.question(self, t("figyelem"), t("vilag_ujra_kerdes")) != QMessageBox.StandardButton.Yes:
            return
        for mappa in self.vilagmappak():
            if mappa.exists():
                shutil.rmtree(mappa, ignore_errors=True)
        tulajdonsagiras(self.tulajdonsagfajl(), {"level-seed": self.seedmezo.text().strip()}, not self.bedrock)
        QMessageBox.information(self, t("kesz"), t("vilag_ujra_kesz"))

    def munka(self, fuggveny, siker):
        self.setEnabled(False)
        hatterfeladat(fuggveny, lambda eredmeny: self.munkavege(eredmeny or siker, None), lambda hiba: self.munkavege(None, hiba))

    def munkavege(self, siker, hiba):
        self.setEnabled(True)
        if hiba:
            QMessageBox.critical(self, t("hiba"), hiba)
            return
        QMessageBox.information(self, t("kesz"), siker)
        self.frissit()

    def vilagkereses(self, gyoker):
        jelzo = "levelname.txt" if self.bedrock else "level.dat"
        gyoker = Path(gyoker)
        if (gyoker / jelzo).exists():
            return gyoker
        for mappa, almappak, fajlok in os.walk(gyoker):
            if jelzo in fajlok:
                return Path(mappa)
        return None

    def vilagtelepites(self, forras):
        for mappa in self.vilagmappak():
            if mappa.exists():
                shutil.rmtree(mappa, ignore_errors=True)
        cel = self.vilagmappak()[0]
        cel.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(forras, cel)

    def mappafeltoltes(self):
        if not self.leallitva():
            return
        kivalasztott = QFileDialog.getExistingDirectory(self, t("kivalasztas"), str(Path.home()))
        if not kivalasztott:
            return
        forras = self.vilagkereses(kivalasztott)
        if forras is None:
            QMessageBox.warning(self, t("figyelem"), t("vilag_nem_talalt"))
            return
        if QMessageBox.question(self, t("figyelem"), t("vilag_csere_kerdes")) != QMessageBox.StandardButton.Yes:
            return

        def feladat():
            self.vilagtelepites(forras)
            return t("vilag_feltoltve")

        self.munka(feladat, t("vilag_feltoltve"))

    def zipfeltoltes(self):
        if not self.leallitva():
            return
        fajl, szuro = QFileDialog.getOpenFileName(self, t("kivalasztas"), str(Path.home()), "Zip (*.zip)")
        if not fajl:
            return
        if QMessageBox.question(self, t("figyelem"), t("vilag_csere_kerdes")) != QMessageBox.StandardButton.Yes:
            return
        ideiglenes = self.szerver.mappa / "_import_tmp"

        def feladat():
            shutil.rmtree(ideiglenes, ignore_errors=True)
            try:
                with zipfile.ZipFile(fajl) as archivum:
                    archivum.extractall(ideiglenes)
                forras = self.vilagkereses(ideiglenes)
                if forras is None:
                    raise RuntimeError(t("vilag_nem_talalt"))
                self.vilagtelepites(forras)
            finally:
                shutil.rmtree(ideiglenes, ignore_errors=True)
            return t("vilag_feltoltve")

        self.munka(feladat, t("vilag_feltoltve"))

    def mentes(self):
        if not self.leallitva():
            return
        mappak = [mappa for mappa in self.vilagmappak() if mappa.exists()]
        if not mappak:
            QMessageBox.information(self, t("figyelem"), t("vilag_nincs_mit_menteni"))
            return
        cel = self.szerver.mappa / "backups"
        cel.mkdir(exist_ok=True)
        fajl = cel / ("vilag_%s.zip" % datetime.now().strftime("%Y%m%d_%H%M%S"))

        def feladat():
            with zipfile.ZipFile(fajl, "w", zipfile.ZIP_DEFLATED) as archivum:
                for mappa in mappak:
                    for gyoker, almappak, fajlok in os.walk(mappa):
                        for nev in fajlok:
                            teljes = Path(gyoker) / nev
                            try:
                                archivum.write(teljes, teljes.relative_to(self.szerver.mappa))
                            except OSError:
                                pass
            return t("vilag_mentve", fajl=fajl.name)

        self.munka(feladat, t("vilag_mentve", fajl=fajl.name))

    def vilagmegnyitas(self):
        mappamegnyitas(self.vilagmappak()[0])


class backupoldal(QWidget):
    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        backup = szerver.meta.get("backup", {})
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        cim = QLabel(t("backup_title"))
        cim.setObjectName("alcim")
        fo.addWidget(cim)
        tipp = QLabel(t("backup_tip"))
        tipp.setObjectName("halvany")
        tipp.setWordWrap(True)
        fo.addWidget(tipp)
        beallitasok = QGroupBox()
        urlap = QFormLayout(beallitasok)
        self.engedelyezve = QCheckBox(t("backup_enabled"))
        self.engedelyezve.setChecked(backup.get("engedelyezve", True))
        urlap.addRow(self.engedelyezve)
        mappasor = QHBoxLayout()
        self.mappamezo = QLineEdit(str(backup.get("mappa") or (szerver.mappa / "backups")))
        self.mappagomb = QPushButton(t("backup_browse"))
        self.mappagomb.clicked.connect(self.mappavalasztas)
        mappasor.addWidget(self.mappamezo, 1)
        mappasor.addWidget(self.mappagomb)
        urlap.addRow(t("backup_location"), mappasor)
        self.indulaskor = QCheckBox(t("backup_startup"))
        self.indulaskor.setChecked(backup.get("indulaskor", True))
        urlap.addRow(self.indulaskor)
        self.intervallum = QSpinBox()
        self.intervallum.setRange(0, 10080)
        self.intervallum.setValue(max(0, int(backup.get("intervallum") or 0)))
        self.intervallum.setSuffix(" min")
        self.intervallum.setToolTip(t("backup_disabled"))
        urlap.addRow(t("backup_interval"), self.intervallum)
        self.megtar = QSpinBox()
        self.megtar.setRange(1, 1000)
        self.megtar.setValue(max(1, int(backup.get("megtart") or 1)))
        urlap.addRow(t("backup_keep"), self.megtar)
        self.elotag = QLineEdit(str(backup.get("elo_tag") or "backup"))
        urlap.addRow(t("backup_prefix"), self.elotag)
        fo.addWidget(beallitasok)
        gombsor = QHBoxLayout()
        self.mentesgomb = QPushButton(t("backup_now"))
        self.mentesgomb.setObjectName("elsodleges")
        self.mentesgomb.clicked.connect(self.mentesmost)
        gombsor.addWidget(self.mentesgomb)
        self.megnyitasgomb = QPushButton(t("backup_open"))
        self.megnyitasgomb.clicked.connect(lambda: mappamegnyitas(self.backupadatok()["mappa"]))
        gombsor.addWidget(self.megnyitasgomb)
        gombsor.addStretch()
        fo.addLayout(gombsor)
        self.allapot = QLabel()
        self.allapot.setObjectName("halvany")
        self.allapot.setWordWrap(True)
        fo.addWidget(self.allapot)
        fo.addStretch()
        for mezo in (self.engedelyezve, self.indulaskor):
            mezo.toggled.connect(self.mentes)
        self.intervallum.valueChanged.connect(self.mentes)
        self.megtar.valueChanged.connect(self.mentes)
        self.mappamezo.editingFinished.connect(self.mentes)
        self.elotag.editingFinished.connect(self.mentes)

    def backupadatok(self):
        return {
            "engedelyezve": self.engedelyezve.isChecked(),
            "mappa": self.mappamezo.text().strip() or str(self.szerver.mappa / "backups"),
            "indulaskor": self.indulaskor.isChecked(),
            "intervallum": self.intervallum.value(),
            "megtart": self.megtar.value(),
            "elo_tag": self.elotag.text().strip() or "backup",
        }

    def mentes(self):
        self.szerver.meta["backup"] = self.backupadatok()
        self.szerver.metamentese()

    def mappavalasztas(self):
        mappa = QFileDialog.getExistingDirectory(self, t("backup_location"), self.mappamezo.text() or str(Path.home()))
        if mappa:
            self.mappamezo.setText(mappa)
            self.mentes()

    def mentesmost(self):
        self.mentes()
        self.mentesgomb.setEnabled(False)
        self.allapot.setText(t("dolgozom"))
        elotte = len(self.szerver.sorok)
        self.szerver.backupinditas(True)
        QTimer.singleShot(500, lambda: self.mentesallapot(elotte))

    def mentesallapot(self, elotte):
        if self.szerver.backupfolyamatban:
            QTimer.singleShot(500, lambda: self.mentesallapot(elotte))
            return
        self.mentesgomb.setEnabled(True)
        if len(self.szerver.sorok) > elotte:
            self.allapot.setText(self.szerver.sorok[-1])


class jatekosoldal(QWidget):
    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        self.bedrock = szerver.tipus() == "bedrock"
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        cim = QLabel(t("online_jatekosok"))
        cim.setObjectName("alcim")
        fo.addWidget(cim)
        self.jatekoslista = QListWidget()
        fo.addWidget(self.jatekoslista, 1)
        feherdoboz = QGroupBox(t("whitelist_kezeles"))
        feherelrendezes = QVBoxLayout(feherdoboz)
        self.fehercsekk = QCheckBox(t("whitelist_be"))
        self.fehercsekk.toggled.connect(self.fehervaltas)
        feherelrendezes.addWidget(self.fehercsekk)
        self.feherlista = QListWidget()
        feherelrendezes.addWidget(self.feherlista)
        feherdoboz_sor = QHBoxLayout()
        self.nevmezo = QLineEdit()
        self.nevmezo.setPlaceholderText(t("jatekos_nev"))
        self.nevmezo.returnPressed.connect(self.hozzaad)
        hozzaadgomb = QPushButton(t("hozzaadas"))
        eltavolitgomb = QPushButton(t("eltavolitas"))
        eltavolitgomb.setObjectName("piros")
        hozzaadgomb.clicked.connect(self.hozzaad)
        eltavolitgomb.clicked.connect(self.eltavolit)
        feherdoboz_sor.addWidget(self.nevmezo, 1)
        feherdoboz_sor.addWidget(hozzaadgomb)
        feherdoboz_sor.addWidget(eltavolitgomb)
        feherelrendezes.addLayout(feherdoboz_sor)
        fo.addWidget(feherdoboz, 1)
        szerver.jatekosvaltozas.connect(self.jatekoslistafrissites)
        szerver.allapotvaltozas.connect(self.jatekoslistafrissites)
        self.frissit()

    def tulajdonsagok(self):
        return tulajdonsagolvasas(self.szerver.mappa / "server.properties", not self.bedrock)

    def feherfajl(self):
        return self.szerver.mappa / ("allowlist.json" if self.bedrock else "whitelist.json")

    def frissit(self):
        self.jatekoslistafrissites()
        kulcs = "allow-list" if self.bedrock else "white-list"
        be = self.tulajdonsagok().get(kulcs, "false").lower() == "true"
        self.fehercsekk.blockSignals(True)
        self.fehercsekk.setChecked(be)
        self.fehercsekk.blockSignals(False)
        self.feherfrissites()

    def jatekoslistafrissites(self):
        self.jatekoslista.clear()
        nevek = list(self.szerver.meta.get("jatekosok", []))
        for nev in self.szerver.jatekosok:
            if nev not in nevek:
                nevek.append(nev)
        if not nevek:
            elem = QListWidgetItem(t("nincs_jatekos"))
            elem.setFlags(Qt.ItemFlag.NoItemFlags)
            self.jatekoslista.addItem(elem)
            return
        for nev in nevek:
            sor = QWidget()
            elrendezes = QHBoxLayout(sor)
            elrendezes.setContentsMargins(8, 4, 8, 4)
            online = nev in self.szerver.jatekosok
            allapot = t("fut") if online else t("all")
            elrendezes.addWidget(QLabel(nev), 1)
            elrendezes.addWidget(QLabel(("● " if online else "○ ") + allapot))
            gombok = [("ban", "piros", lambda _=False, n=nev: self.szerver.parancs("ban " + n)),
                      ("ipban", "piros", lambda _=False, n=nev: self.szerver.parancs("ban-ip " + n)),
                      ("op", "", lambda _=False, n=nev: self.szerver.parancs("op " + n)),
                      ("adat_torles", "piros", lambda _=False, n=nev: self.adattorles(n))]
            for kulcs, stilus, muvelet in gombok:
                gomb = QPushButton(t(kulcs))
                if stilus:
                    gomb.setObjectName(stilus)
                if self.bedrock and kulcs != "op":
                    gomb.setEnabled(False)
                gomb.clicked.connect(muvelet)
                elrendezes.addWidget(gomb)
            elem = QListWidgetItem()
            elem.setSizeHint(sor.sizeHint())
            elem.setFlags(Qt.ItemFlag.NoItemFlags)
            self.jatekoslista.addItem(elem)
            self.jatekoslista.setItemWidget(elem, sor)

    def jatekosuuid(self, nev):
        try:
            gyorsitotar = json.loads((self.szerver.mappa / "usercache.json").read_text(encoding="utf-8"))
            for elem in gyorsitotar:
                if elem.get("name", "").lower() == nev.lower():
                    return elem["uuid"]
        except Exception:
            pass
        if self.tulajdonsagok().get("online-mode", "true").lower() != "true":
            return uuidkeres(nev, False)
        return None

    def adattorles(self, nev):
        if QMessageBox.question(self, t("figyelem"), t("adat_torles_kerdes", nev=nev)) != QMessageBox.StandardButton.Yes:
            return
        azonosito = self.jatekosuuid(nev)
        if not azonosito:
            QMessageBox.warning(self, t("figyelem"), t("uuid_nincs"))
            return
        self.szerver.parancs("kick " + nev)
        QTimer.singleShot(1500, lambda: self.adatfajlok(azonosito))

    def adatfajlok(self, azonosito):
        vilag = self.szerver.mappa / self.tulajdonsagok().get("level-name", "world")
        torolt = 0
        for almappa in ("playerdata", "stats", "advancements", "players"):
            gyoker = vilag / almappa
            if not gyoker.exists():
                continue
            for ut in list(gyoker.rglob(azonosito + "*")):
                if ut.is_file():
                    try:
                        ut.unlink()
                        torolt += 1
                    except OSError:
                        pass
        QMessageBox.information(self, t("kesz"), t("adat_torolve", db=torolt))

    def feherbeolvasas(self):
        try:
            adat = json.loads(self.feherfajl().read_text(encoding="utf-8"))
            return [elem for elem in adat if isinstance(elem, dict) and elem.get("name")]
        except Exception:
            return []

    def feherfrissites(self):
        self.feherlista.clear()
        for elem in self.feherbeolvasas():
            self.feherlista.addItem(elem["name"])

    def fehervaltas(self, be):
        kulcs = "allow-list" if self.bedrock else "white-list"
        ertekek = {kulcs: "true" if be else "false"}
        if not self.bedrock:
            ertekek["enforce-whitelist"] = "true" if be else "false"
        tulajdonsagiras(self.szerver.mappa / "server.properties", ertekek, not self.bedrock)
        if self.szerver.fut():
            elotag = "allowlist" if self.bedrock else "whitelist"
            self.szerver.parancs(elotag + (" on" if be else " off"))

    def hozzaad(self):
        nev = self.nevmezo.text().strip()
        minta = r"[\w ]{1,32}" if self.bedrock else r"\w{1,16}"
        if not re.fullmatch(minta, nev):
            QMessageBox.warning(self, t("figyelem"), t("hibas_nev"))
            return
        elotag = "allowlist" if self.bedrock else "whitelist"
        if self.szerver.fut():
            self.szerver.parancs("%s add %s" % (elotag, nev))
            self.nevmezo.clear()
            QTimer.singleShot(1200, self.feherfrissites)
            return
        if self.bedrock:
            self.feherirasa(nev, None)
            return
        online = self.tulajdonsagok().get("online-mode", "true").lower() == "true"
        hatterfeladat(lambda: uuidkeres(nev, online), lambda azonosito: self.feherirasa(nev, azonosito), self.feherhiba)

    def feherhiba(self, uzenet):
        QMessageBox.warning(self, t("figyelem"), uzenet)

    def feherirasa(self, nev, azonosito):
        lista = self.feherbeolvasas()
        if not any(elem["name"].lower() == nev.lower() for elem in lista):
            if self.bedrock:
                lista.append({"ignoresPlayerLimit": False, "name": nev})
            else:
                lista.append({"uuid": azonosito, "name": nev})
            self.feherfajl().write_text(json.dumps(lista, indent=2), encoding="utf-8")
        self.nevmezo.clear()
        self.feherfrissites()

    def eltavolit(self):
        elem = self.feherlista.currentItem()
        if not elem:
            return
        nev = elem.text()
        if self.szerver.fut():
            elotag = "allowlist" if self.bedrock else "whitelist"
            self.szerver.parancs("%s remove %s" % (elotag, nev))
            QTimer.singleShot(1200, self.feherfrissites)
            return
        lista = [sor for sor in self.feherbeolvasas() if sor["name"] != nev]
        self.feherfajl().write_text(json.dumps(lista, indent=2), encoding="utf-8")
        self.feherfrissites()


class modoldal(QWidget):
    def __init__(self, szerver, almappa, cimkulcs, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        self.mappa = szerver.mappa / almappa
        self.setAcceptDrops(True)
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        cim = QLabel(t(cimkulcs))
        cim.setObjectName("alcim")
        fo.addWidget(cim)
        tipp = QLabel(t("mod_tipp"))
        tipp.setObjectName("halvany")
        tipp.setWordWrap(True)
        fo.addWidget(tipp)
        gombok = QHBoxLayout()
        importgomb = QPushButton(t("import_gomb"))
        importgomb.setObjectName("elsodleges")
        mappagomb = QPushButton(t("mappa_megnyitas"))
        frissitgomb = QPushButton(t("frissites"))
        importgomb.clicked.connect(self.importvalasztas)
        mappagomb.clicked.connect(lambda: mappamegnyitas(self.mappa))
        frissitgomb.clicked.connect(self.frissit)
        gombok.addWidget(importgomb)
        gombok.addWidget(mappagomb)
        gombok.addWidget(frissitgomb)
        gombok.addStretch()
        fo.addLayout(gombok)
        alcim = QLabel(t("importalt"))
        alcim.setObjectName("alcim")
        fo.addWidget(alcim)
        self.lista = QListWidget()
        fo.addWidget(self.lista, 1)
        self.frissit()

    def dragEnterEvent(self, esemeny):
        if esemeny.mimeData().hasUrls():
            esemeny.acceptProposedAction()

    def dropEvent(self, esemeny):
        utak = [url.toLocalFile() for url in esemeny.mimeData().urls() if url.toLocalFile().lower().endswith(".jar")]
        self.importalas(utak)

    def importvalasztas(self):
        fajlok, szuro = QFileDialog.getOpenFileNames(self, t("fajl_valasztas"), str(Path.home() / "Downloads"), "Jar (*.jar)")
        self.importalas(fajlok)

    def importalas(self, fajlok):
        if not fajlok:
            return
        self.mappa.mkdir(parents=True, exist_ok=True)
        for fajl in fajlok:
            try:
                shutil.copy2(fajl, self.mappa / Path(fajl).name)
            except OSError as hiba:
                QMessageBox.warning(self, t("hiba"), str(hiba))
        self.frissit()

    def frissit(self):
        self.lista.clear()
        fajlok = []
        if self.mappa.exists():
            for ut in self.mappa.iterdir():
                nev = ut.name.lower()
                if ut.is_file() and (nev.endswith(".jar") or nev.endswith(".jar.disabled")):
                    fajlok.append(ut)
        fajlok.sort(key=lambda ut: ut.name.lower())
        if not fajlok:
            elem = QListWidgetItem(t("ures_lista"))
            elem.setFlags(Qt.ItemFlag.NoItemFlags)
            self.lista.addItem(elem)
            return
        for ut in fajlok:
            kikapcsolt = ut.name.lower().endswith(".disabled")
            nev = ut.name[:-9] if kikapcsolt else ut.name
            sor = QWidget()
            elrendezes = QHBoxLayout(sor)
            elrendezes.setContentsMargins(8, 4, 8, 4)
            elrendezes.addWidget(QLabel(nev), 1)
            allapotcimke = QLabel(t("kikapcsolva") if kikapcsolt else t("bekapcsolva"))
            allapotcimke.setObjectName("all" if kikapcsolt else "fut")
            elrendezes.addWidget(allapotcimke)
            kapcsologomb = QPushButton(t("bekapcsol") if kikapcsolt else t("kikapcsol"))
            kapcsologomb.clicked.connect(lambda _=False, f=ut: self.kapcsolas(f))
            torlesgomb = QPushButton(t("torles"))
            torlesgomb.setObjectName("piros")
            torlesgomb.clicked.connect(lambda _=False, f=ut: self.torles(f))
            elrendezes.addWidget(kapcsologomb)
            elrendezes.addWidget(torlesgomb)
            elem = QListWidgetItem()
            elem.setSizeHint(sor.sizeHint())
            elem.setFlags(Qt.ItemFlag.NoItemFlags)
            self.lista.addItem(elem)
            self.lista.setItemWidget(elem, sor)

    def kapcsolas(self, ut):
        if ut.name.lower().endswith(".disabled"):
            uj = ut.with_name(ut.name[:-9])
        else:
            uj = ut.with_name(ut.name + ".disabled")
        try:
            ut.replace(uj)
        except OSError as hiba:
            QMessageBox.warning(self, t("hiba"), str(hiba))
        self.frissit()

    def torles(self, ut):
        if QMessageBox.question(self, t("figyelem"), t("torles_fajl_kerdes", nev=ut.name)) != QMessageBox.StandardButton.Yes:
            return
        try:
            ut.unlink()
        except OSError as hiba:
            QMessageBox.warning(self, t("hiba"), str(hiba))
        self.frissit()


class beallitasoldal(QWidget):
    torolve = Signal()

    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        self.tipus = szerver.tipus()
        self.szerkeszto = None
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        if self.tipus == "pumpkin":
            figyelmeztetes = QLabel(t("pumpkin_fejlesztes") + "\n" + t("pumpkin_gep") + "\n" + t("pumpkin_kezi"))
            figyelmeztetes.setObjectName("figyelmeztetes")
            figyelmeztetes.setWordWrap(True)
            fo.addWidget(figyelmeztetes)
            mappagomb = QPushButton(t("pumpkin_mappa"))
            mappagomb.clicked.connect(lambda: mappamegnyitas(szerver.mappa))
            fo.addWidget(mappagomb, 0, Qt.AlignmentFlag.AlignLeft)
            fo.addStretch()
        else:
            if self.tipus in javatipusok:
                javacimke = QLabel(t("java_info", verzio=szerver.meta.get("java")))
                javacimke.setObjectName("halvany")
                fo.addWidget(javacimke)
            self.szerkeszto = beallitasszerkeszto("bedrock" if self.tipus == "bedrock" else "java")
            fo.addWidget(self.szerkeszto, 1)
            mentesgomb = QPushButton(t("mentes"))
            mentesgomb.setObjectName("elsodleges")
            mentesgomb.clicked.connect(self.mentes)
            fo.addWidget(mentesgomb, 0, Qt.AlignmentFlag.AlignLeft)
        torlesgomb = QPushButton(t("szerver_torlese"))
        torlesgomb.setObjectName("piros")
        torlesgomb.clicked.connect(self.torles)
        fo.addWidget(torlesgomb, 0, Qt.AlignmentFlag.AlignLeft)
        self.frissit()

    def escape(self):
        return self.tipus != "bedrock"

    def frissit(self):
        if self.szerkeszto is None:
            return
        adat = tulajdonsagolvasas(self.szerver.mappa / "server.properties", self.escape())
        self.szerkeszto.feltoltes(adat)
        self.szerkeszto.ramallitas(self.szerver.meta.get("ram") or 2048)

    def mentes(self):
        ertekek = self.szerkeszto.ertekek(self.szerver.meta.get("verzio", ""))
        tulajdonsagiras(self.szerver.mappa / "server.properties", ertekek, self.escape())
        if self.tipus != "bedrock":
            self.szerver.meta["ram"] = self.szerkeszto.ram()
            self.szerver.metamentese()
        uzenet = t("mentve")
        if self.szerver.fut():
            uzenet += "\n" + t("ujrainditas_kell")
        QMessageBox.information(self, t("kesz"), uzenet)

    def torles(self):
        if self.szerver.fut():
            QMessageBox.warning(self, t("figyelem"), t("elobb_alljon_le"))
            return
        if QMessageBox.question(self, t("figyelem"), t("torles_kerdes")) != QMessageBox.StandardButton.Yes:
            return
        self.szerver.playitleallitas()
        self.szerver.pinggyleallitas()
        shutil.rmtree(self.szerver.mappa, ignore_errors=True)
        self.torolve.emit()


class szerveroldal(QWidget):
    vissza = Signal()

    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        tipus = szerver.tipus()
        pumpkin = tipus == "pumpkin"
        modos = tipus in ("fabric", "forge", "neoforge")
        pluginos = tipus in ("paper", "purpur")
        gyoker = QHBoxLayout(self)
        gyoker.setContentsMargins(0, 0, 0, 0)
        gyoker.setSpacing(0)
        self.oldalsav = QFrame()
        self.oldalsav.setObjectName("oldalsav")
        self.oldalsav.setFixedWidth(230)
        sav = QVBoxLayout(self.oldalsav)
        sav.setContentsMargins(12, 12, 12, 12)
        visszagomb = QPushButton("←  " + t("vissza"))
        visszagomb.clicked.connect(self.vissza)
        sav.addWidget(visszagomb)
        sav.addSpacing(10)
        self.csoport = QButtonGroup(self)
        self.csoport.setExclusive(True)
        self.verem = QStackedWidget()
        self.oldalak = []
        elemek = [
            ("menu_iranyitas", lambda: iranyitooldal(szerver), True),
            ("menu_vilag", lambda: vilagoldal(szerver), not pumpkin),
            ("backup_menu", lambda: backupoldal(szerver), True),
            ("menu_jatekosok", lambda: jatekosoldal(szerver), not pumpkin),
            ("menu_modok", lambda: modoldal(szerver, "mods", "modok_cim"), modos),
            ("menu_pluginek", lambda: modoldal(szerver, "plugins", "pluginek_cim"), pluginos),
            ("menu_beallitasok", lambda: beallitasoldal(szerver), True),
        ]
        self.navgombok = []
        for index, (kulcs, gyarto, elerheto) in enumerate(elemek):
            oldal = gyarto() if elerheto else QWidget()
            if isinstance(oldal, beallitasoldal):
                oldal.torolve.connect(self.vissza)
            self.oldalak.append(oldal)
            self.verem.addWidget(oldal)
            gomb = QPushButton(t(kulcs))
            gomb.setObjectName("navgomb")
            gomb.setCheckable(True)
            if not elerheto:
                gomb.setEnabled(False)
                gomb.setToolTip(t("nem_elerheto"))
            self.csoport.addButton(gomb, index)
            self.navgombok.append(gomb)
            sav.addWidget(gomb)
        sav.addStretch()
        mappagomb = QPushButton(t("mappa_megnyitas"))
        mappagomb.clicked.connect(lambda: mappamegnyitas(szerver.mappa))
        sav.addWidget(mappagomb)
        self.navgombok[0].setChecked(True)
        self.csoport.idClicked.connect(self.oldalvaltas)
        jobb = QVBoxLayout()
        jobb.setContentsMargins(16, 12, 16, 12)
        felso = QHBoxLayout()
        self.hamburger = QPushButton("☰")
        self.hamburger.setFixedWidth(40)
        self.hamburger.clicked.connect(self.savvaltas)
        cim = QLabel(szerver.meta["nev"])
        cim.setObjectName("oldalcim")
        verzio = szerver.meta.get("verzio", "")
        if verzio == "latest":
            verzio = t("legfrissebb")
        leiras = QLabel("%s · %s" % (tipusnevek.get(tipus, tipus), verzio))
        leiras.setObjectName("halvany")
        self.allapotcimke = QLabel()
        felso.addWidget(self.hamburger)
        felso.addWidget(cim)
        felso.addWidget(leiras)
        felso.addStretch()
        felso.addWidget(self.allapotcimke)
        jobb.addLayout(felso)
        jobb.addWidget(self.verem, 1)
        gyoker.addWidget(self.oldalsav)
        gyoker.addLayout(jobb, 1)
        szerver.allapotvaltozas.connect(self.allapotfrissites)
        self.allapotfrissites()

    def savvaltas(self):
        self.oldalsav.setVisible(not self.oldalsav.isVisible())

    def oldalvaltas(self, index):
        self.verem.setCurrentIndex(index)
        oldal = self.oldalak[index]
        if hasattr(oldal, "frissit"):
            oldal.frissit()

    def allapotfrissites(self):
        if self.szerver.fut():
            self.allapotcimke.setText("● " + t("fut"))
            self.allapotcimke.setObjectName("fut")
        else:
            self.allapotcimke.setText("○ " + t("all"))
            self.allapotcimke.setObjectName("all")
        self.allapotcimke.style().unpolish(self.allapotcimke)
        self.allapotcimke.style().polish(self.allapotcimke)


stilus = """
QWidget { background: #1e1f26; color: #e6e6ea; font-size: 13px; }
QLabel { background: transparent; }
QLabel#focim { font-size: 26px; font-weight: bold; }
QLabel#oldalcim { font-size: 20px; font-weight: bold; }
QLabel#alcim { font-size: 15px; font-weight: bold; }
QLabel#halvany { color: #8c8fa1; }
QLabel#fut { color: #4ade80; font-weight: bold; }
QLabel#all { color: #9ca3af; font-weight: bold; }
QLabel#figyelmeztetes { background: #3b2f12; color: #fbbf24; border: 1px solid #f59e0b; border-radius: 6px; padding: 8px; }
QLabel#szervernev { font-size: 16px; font-weight: bold; }
QFrame#oldalsav { background: #16171c; border-right: 1px solid #2c2e3a; }
QFrame#oldalsav QPushButton, QFrame#oldalsav QLabel { background: transparent; }
QFrame#szerversor { background: #2a2c36; border-radius: 8px; }
QPushButton { background: #343746; border: none; border-radius: 6px; padding: 7px 14px; }
QPushButton:hover { background: #41455a; }
QPushButton:disabled { color: #6b6e7c; background: #2a2c36; }
QPushButton#elsodleges { background: #2e9e5b; font-weight: bold; }
QPushButton#elsodleges:hover { background: #36b36a; }
QPushButton#zold { background: #2e9e5b; }
QPushButton#zold:disabled { background: #2a2c36; }
QPushButton#piros { background: #a33b3b; }
QPushButton#piros:hover { background: #bd4747; }
QPushButton#piros:disabled { background: #2a2c36; }
QPushButton#navgomb { text-align: left; padding: 10px 14px; background: transparent; }
QPushButton#navgomb:hover { background: #2a2c36; }
QPushButton#navgomb:checked { background: #2e9e5b; font-weight: bold; }
QPushButton#navgomb:disabled { color: #5b5e6c; }
QLineEdit, QSpinBox, QComboBox, QPlainTextEdit { background: #14151a; border: 1px solid #3a3d4d; border-radius: 5px; padding: 5px; selection-background-color: #2e9e5b; }
QPlainTextEdit#konzol { font-family: Consolas, "DejaVu Sans Mono", monospace; font-size: 12px; }
QComboBox QAbstractItemView { background: #14151a; selection-background-color: #2e9e5b; }
QCheckBox::indicator { width: 16px; height: 16px; border: 1px solid #5a5e72; border-radius: 3px; background: #14151a; }
QCheckBox::indicator:checked { background: #2e9e5b; }
QListWidget { background: transparent; border: none; outline: 0; }
QListWidget::item { margin: 3px 0; border-radius: 6px; }
QListWidget::item:selected { background: #2f3342; }
QListWidget#szerverlista::item:selected, QListWidget#szerverlista::item:hover { background: #343746; }
QGroupBox { border: 1px solid #3a3d4d; border-radius: 8px; margin-top: 12px; padding: 12px 8px 8px 8px; font-weight: bold; }
QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 4px; }
QProgressBar { background: #14151a; border: 1px solid #3a3d4d; border-radius: 5px; height: 16px; text-align: center; }
QProgressBar::chunk { background: #2e9e5b; border-radius: 4px; }
QTabWidget::pane { border: 1px solid #3a3d4d; border-radius: 6px; }
QTabBar::tab { background: #2a2c36; padding: 8px 16px; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
QTabBar::tab:selected { background: #2e9e5b; }
QScrollArea { background: transparent; border: none; }
QScrollBar:vertical { background: #14151a; width: 10px; }
QScrollBar::handle:vertical { background: #3a3d4d; border-radius: 5px; min-height: 24px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QToolTip { background: #14151a; color: #e6e6ea; border: 1px solid #3a3d4d; }
"""


class foablak(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("cim"))
        self.resize(1150, 780)
        self.szerverek = {}
        self.biztoskilepes = False
        self.aktualisoldal = None
        self.verem = QStackedWidget()
        self.setCentralWidget(self.verem)
        self.fooldal = QWidget()
        fo = QVBoxLayout(self.fooldal)
        fo.setContentsMargins(28, 24, 28, 24)
        felso = QHBoxLayout()
        cim = QLabel(t("cim"))
        cim.setObjectName("focim")
        felso.addWidget(cim)
        felso.addStretch()
        self.letrehozgomb = QPushButton(t("szerver_letrehozasa"))
        self.letrehozgomb.setObjectName("elsodleges")
        self.letrehozgomb.clicked.connect(self.letrehozas)
        self.nyelvgomb = QPushButton("Language")
        self.nyelvgomb.clicked.connect(self.nyelvablak)
        felso.addWidget(self.letrehozgomb)
        felso.addWidget(self.nyelvgomb)
        fo.addLayout(felso)
        fo.addSpacing(12)
        self.lista = QListWidget()
        self.lista.setObjectName("szerverlista")
        self.lista.itemClicked.connect(self.szervermegnyitas)
        fo.addWidget(self.lista, 1)
        self.urescimke = QLabel(t("nincs_szerver"))
        self.urescimke.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.urescimke.setObjectName("halvany")
        fo.addWidget(self.urescimke, 1)
        self.verem.addWidget(self.fooldal)
        self.listafrissites()

    def sorkeszites(self, szerver):
        kocka = QFrame()
        kocka.setObjectName("szerversor")
        elrendezes = QHBoxLayout(kocka)
        elrendezes.setContentsMargins(16, 10, 16, 10)
        bal = QVBoxLayout()
        nev = QLabel(szerver.meta.get("nev", "?"))
        nev.setObjectName("szervernev")
        verzio = szerver.meta.get("verzio", "")
        if verzio == "latest":
            verzio = t("legfrissebb")
        leiras = QLabel("%s · %s" % (tipusnevek.get(szerver.tipus(), szerver.tipus()), verzio))
        leiras.setObjectName("halvany")
        bal.addWidget(nev)
        bal.addWidget(leiras)
        if szerver.fut():
            allapotcimke = QLabel("● " + t("fut"))
            allapotcimke.setObjectName("fut")
        else:
            allapotcimke = QLabel("○ " + t("all"))
            allapotcimke.setObjectName("all")
        elrendezes.addLayout(bal, 1)
        elrendezes.addWidget(allapotcimke)
        kocka.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        for gyerek in kocka.findChildren(QWidget):
            gyerek.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        return kocka

    def listafrissites(self):
        nevek = []
        if szerverekmappa.exists():
            for mappa in sorted(szerverekmappa.iterdir(), key=lambda ut: ut.name.lower()):
                if (mappa / "mcmaker.json").exists():
                    nevek.append(mappa.name)
        for nev in list(nevek):
            if nev not in self.szerverek:
                try:
                    folyamat = szerverfolyamat(szerverekmappa / nev)
                except Exception:
                    nevek.remove(nev)
                    continue
                folyamat.allapotvaltozas.connect(self.listafrissites)
                self.szerverek[nev] = folyamat
        for nev in list(self.szerverek):
            if nev not in nevek and not self.szerverek[nev].fut():
                self.szerverek[nev].deleteLater()
                del self.szerverek[nev]
        self.lista.clear()
        for nev in nevek:
            szerver = self.szerverek[nev]
            kocka = self.sorkeszites(szerver)
            elem = QListWidgetItem()
            elem.setSizeHint(QSize(0, 74))
            elem.setData(Qt.ItemDataRole.UserRole, nev)
            self.lista.addItem(elem)
            self.lista.setItemWidget(elem, kocka)
        self.lista.setVisible(bool(nevek))
        self.urescimke.setVisible(not nevek)

    def szervermegnyitas(self, elem):
        nev = elem.data(Qt.ItemDataRole.UserRole)
        szerver = self.szerverek.get(nev)
        if szerver is None:
            return
        szerver.meta = metabetoltes(szerver.mappa)
        oldal = szerveroldal(szerver)
        oldal.vissza.connect(self.visszalepes)
        self.verem.addWidget(oldal)
        self.verem.setCurrentWidget(oldal)
        self.aktualisoldal = oldal

    def visszalepes(self):
        oldal = self.aktualisoldal
        self.verem.setCurrentWidget(self.fooldal)
        if oldal is not None:
            self.verem.removeWidget(oldal)
            oldal.deleteLater()
        self.aktualisoldal = None
        self.listafrissites()

    def letrehozas(self):
        ablak = letrehozoablak(self)
        if ablak.exec() == QDialog.DialogCode.Accepted:
            self.listafrissites()

    def futoszerverek(self):
        return [szerver for szerver in self.szerverek.values() if szerver.fut()]

    def mindenleallitasa(self):
        ablak = QDialog(self)
        ablak.setWindowTitle(t("leallitas_folyamatban"))
        elrendezes = QVBoxLayout(ablak)
        elrendezes.addWidget(QLabel(t("leallitas_folyamatban")))
        savja = QProgressBar()
        savja.setRange(0, 0)
        elrendezes.addWidget(savja)
        ablak.setModal(True)
        ablak.show()
        QApplication.processEvents()
        for szerver in self.szerverek.values():
            szerver.playitleallitas()
            szerver.pinggyleallitas()
            szerver.leallitas()
        hatar = time.time() + 70
        while self.futoszerverek() and time.time() < hatar:
            QApplication.processEvents()
            time.sleep(0.05)
        for szerver in self.futoszerverek():
            szerver.folyamat.kill()
            szerver.folyamat.waitForFinished(3000)
        ablak.close()

    def nyelvablak(self):
        ablak = QDialog(self)
        ablak.setWindowTitle("Language")
        elrendezes = QVBoxLayout(ablak)
        doboz = QComboBox()
        doboz.addItem("English", "en")
        doboz.addItem("Magyar", "hu")
        doboz.setCurrentIndex(doboz.findData(allapot["nyelv"]))
        elrendezes.addWidget(doboz)
        gombok = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        gombok.accepted.connect(ablak.accept)
        gombok.rejected.connect(ablak.reject)
        elrendezes.addWidget(gombok)
        if ablak.exec() != QDialog.DialogCode.Accepted:
            return
        uj = doboz.currentData()
        if uj != allapot["nyelv"]:
            self.nyelvvaltoztatas(uj)

    def nyelvvaltoztatas(self, uj):
        if self.futoszerverek():
            if QMessageBox.question(self, t("figyelem"), t("nyelv_leallitas")) != QMessageBox.StandardButton.Yes:
                return
        self.mindenleallitasa()
        beallitasok = beallitasbetoltes()
        beallitasok["nyelv"] = uj
        beallitasmentes(beallitasok)
        self.biztoskilepes = True
        if getattr(sys, "frozen", False):
            argumentumok = [sys.executable] + sys.argv[1:]
        else:
            argumentumok = [sys.executable] + sys.argv
        subprocess.Popen(argumentumok)
        QApplication.quit()

    def closeEvent(self, esemeny):
        if self.biztoskilepes:
            esemeny.accept()
            return
        if self.futoszerverek():
            valasz = QMessageBox.question(self, t("kilepes_cim"), t("kilepes_szoveg"), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if valasz != QMessageBox.StandardButton.Yes:
                esemeny.ignore()
                return
        self.mindenleallitasa()
        self.biztoskilepes = True
        esemeny.accept()


def pinggysegitofolyamat():
    jel = "--cubiclantern-pinggy-tunnel"
    try:
        index = sys.argv.index(jel)
    except ValueError:
        return 1
    parancs = sys.argv[index + 1:]
    if not parancs:
        return 1
    if os.name == "nt":
        if sys.stdout is None or sys.stderr is None:
            try:
                import ctypes
                ctypes.windll.kernel32.AttachConsole(-1)
            except (AttributeError, OSError):
                pass
            try:
                if sys.stdout is None:
                    sys.stdout = open("CONOUT$", "w", encoding="utf-8", errors="replace")
                if sys.stderr is None:
                    sys.stderr = open("CONOUT$", "w", encoding="utf-8", errors="replace")
            except OSError:
                pass
        try:
            from winpty import PtyProcess
        except ImportError:
            folyamat = subprocess.Popen(parancs, stdin=subprocess.PIPE)
            time.sleep(2)
            try:
                folyamat.stdin.write(b"\n")
                folyamat.stdin.flush()
                folyamat.stdin.close()
            except (BrokenPipeError, OSError):
                pass
            return folyamat.wait()
        folyamat = PtyProcess.spawn(subprocess.list2cmdline(parancs))
        def kimenet():
            while True:
                try:
                    adat = folyamat.read()
                except (EOFError, OSError):
                    break
                if adat:
                    sys.stdout.write(adat)
                    sys.stdout.flush()
                elif not folyamat.isalive():
                    break
        szal = threading.Thread(target=kimenet, daemon=True)
        szal.start()
        time.sleep(2)
        try:
            folyamat.write("\r\n")
        except (EOFError, OSError):
            pass
        while folyamat.isalive():
            time.sleep(0.2)
        szal.join(timeout=1)
        return 0
    import pty
    import select
    pid, leiro = pty.fork()
    if pid == 0:
        os.execvp(parancs[0], parancs)
    kezd = time.monotonic()
    while True:
        if time.monotonic() - kezd >= 2:
            try:
                os.write(leiro, b"\r\n")
            except OSError:
                pass
            break
        elerheto, _, _ = select.select([leiro], [], [], 0.1)
        if elerheto:
            try:
                os.read(leiro, 4096)
            except OSError:
                break
    while True:
        elerheto, _, _ = select.select([leiro], [], [], 0.1)
        if elerheto:
            try:
                os.read(leiro, 4096)
            except OSError:
                break
        kilepesi, status = os.waitpid(pid, os.WNOHANG)
        if kilepesi == pid:
            return os.waitstatus_to_exitcode(status)


def inditas():
    mappakeszites()
    beallitasok = beallitasbetoltes()
    nyelv = beallitasok.get("nyelv", "en")
    if nyelv not in szovegek:
        nyelv = "en"
    allapot["nyelv"] = nyelv
    if "nyelv" not in beallitasok:
        beallitasok["nyelv"] = nyelv
        beallitasmentes(beallitasok)
    aplikacio = QApplication(sys.argv)
    aplikacio.setStyle("Fusion")
    aplikacio.setStyleSheet(stilus)
    ablak = foablak()
    ablak.show()
    sys.exit(aplikacio.exec())


if __name__ == "__main__":
    if "--cubiclantern-pinggy-tunnel" in sys.argv:
        sys.exit(pinggysegitofolyamat())
    inditas()
