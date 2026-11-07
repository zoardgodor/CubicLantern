from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    import base64
    import json
    import os
    import re
    import shutil
    import subprocess
    import sys
    import time
    import urllib.request
    import uuid
    import zipfile
    from pathlib import Path

    javamappa: Path
    playitmappa: Path
    pinggymappa: Path
    allapot: dict[str, Any]
    ugynok: str
    architektura: Any
    platformnev: Any
    fajlletoltes: Any
    jsonlekeres: Any
    eszkozvalasztas: Any
    mappakeszites: Any
    lan_ipv4_cim: Any
    t: Any


def javautvonal(foverzio):
    mappa = javamappa / str(foverzio)
    nev = "java.exe"
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
        with zipfile.ZipFile(ideiglenes) as archivum:
            archivum.extractall(cel)
    finally:
        ideiglenes.unlink(missing_ok=True)
    ut = javautvonal(foverzio)
    if not ut:
        raise RuntimeError("Java")
    return ut


def playitletoltes(haladas=None):
    nev = "playit.exe"
    cel = playitmappa / nev
    if cel.exists():
        return cel
    url = None
    try:
        kiadas = jsonlekeres("https://api.github.com/repos/playit-cloud/playit-agent/releases/latest")
        eszkoznev = "playit-windows-x86_64-signed.exe" if architektura() == "x86_64" else None
        eszkoz = next(
            (elem for elem in kiadas["assets"] if elem["name"] == eszkoznev),
            None,
        ) if eszkoznev else eszkozvalasztas(kiadas["assets"])
        if eszkoz:
            url = eszkoz["browser_download_url"]
    except Exception:
        url = None
    if not url:
        url = "https://github.com/playit-cloud/playit-agent/releases/latest/download/playit-windows-x86_64-signed.exe"
    fajlletoltes(url, cel, haladas)
    return cel


def kulonterminal(program, argumentumok, munkamappa, cim):
    munkamappa = str(munkamappa)
    indito = subprocess.STARTUPINFO()
    setattr(indito, "lpTitle", cim)
    return subprocess.Popen(
        [str(program)] + [str(x) for x in argumentumok],
        cwd=munkamappa,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        startupinfo=indito,
    )


def pinggyprogram():
    nev = "pinggy.exe"
    jeloltek = [pinggymappa / nev, Path.cwd() / nev, Path(__file__).resolve().parent / nev]
    if getattr(sys, "frozen", False):
        jeloltek.insert(0, Path(sys.executable).resolve().parent / nev)
    for jelolt in jeloltek:
        if jelolt.is_file():
            return str(jelolt)
    return shutil.which(nev)


def sshprogram():
    nev = "ssh.exe"
    talalat = shutil.which(nev)
    if talalat:
        return talalat
    talalat = Path(os.environ.get("WINDIR", r"C:\Windows")) / "System32" / "OpenSSH" / nev
    if talalat.is_file():
        return str(talalat)
    return None


def pinggyimportal(forras):
    mappakeszites()
    cel = pinggymappa / "pinggy.exe"
    shutil.copy2(forras, cel)
    return cel


def pinggyimportalttorles():
    cel = pinggymappa / "pinggy.exe"
    try:
        cel.unlink()
    except FileNotFoundError:
        return False
    return True


def pinggysshparancs(tunnel):
    tipus = tunnel.get("tipus", "tcp")
    if tipus == "udp":
        return None
    port = int(tunnel.get("port") or (19132 if tipus == "udp" else 25565))
    cel = "127.0.0.1:%d" % port
    host = "free.pinggy.io" if tipus == "http" else "tcp@free.pinggy.io"
    return sshprogram() or "ssh.exe", ["-p", "443", "-R0:" + cel, host]


def pinggyparancs(tunnel):
    tipus = tunnel.get("tipus", "tcp")
    port = int(tunnel.get("port") or (19132 if tipus == "udp" else 25565))
    cel = "127.0.0.1:%d" % port
    program = pinggyprogram()
    if program:
        cel = "localhost:%d" % port
        celirany = "udp@free.pinggy.io" if tipus == "udp" else ("free.pinggy.io" if tipus == "http" else "tcp@free.pinggy.io")
        return program, ["-p", "443", "-R0:" + cel, celirany]
    if tipus == "udp":
        program = "pinggy.exe"
        return program, ["-p", "443", "-R0:" + cel, "udp@free.pinggy.io"]
    return pinggysshparancs(tunnel)


def pinggyparancsszoveg(program, argumentumok):
    return subprocess.list2cmdline([program] + argumentumok)


def powershellszoveg(szoveg):
    return "'" + str(szoveg).replace("'", "''") + "'"


def pinggysegitoprogram(program, argumentumok, fallback=None, tipus="tcp"):
    if getattr(sys, "frozen", False):
        elo = [sys.executable, "--cubiclantern-pinggy-tunnel"]
    else:
        elo = [sys.executable, str(Path(__file__).resolve()), "--cubiclantern-pinggy-tunnel"]
    adatok = {
        "program": str(program),
        "argumentumok": [str(x) for x in argumentumok],
        "fallback": fallback,
        "tipus": tipus,
        "pinggy_cli": program == pinggyprogram(),
        "nyelv": allapot.get("nyelv", "en"),
    }
    if fallback:
        adatok["fallback"] = [str(fallback[0])] + [str(x) for x in fallback[1]]
    payload = base64.b64encode(json.dumps(adatok).encode("utf-8")).decode("ascii")
    return elo + [payload]


def pinggyterminal(tunnel, mappa, cim):
    mappa = Path(mappa)
    launcher = mappa / (".cubiclantern_pinggy_%s.ps1" % uuid.uuid4().hex)
    parancs = pinggyparancs(tunnel)
    if parancs is None:
        raise RuntimeError("The selected Pinggy tunnel type is not supported.")
    program, argumentumok = parancs
    cli = pinggyprogram()
    fallback = pinggysshparancs(tunnel) if cli and tunnel.get("tipus", "tcp") != "udp" else None
    segito = pinggysegitoprogram(program, argumentumok, fallback, tunnel.get("tipus", "tcp"))
    lista = ", ".join(powershellszoveg(x) for x in segito[1:])
    tipus = tunnel.get("tipus", "tcp")
    port = int(tunnel.get("port") or (19132 if tipus == "udp" else 25565))
    lan = lan_ipv4_cim() or t("pinggy_lan_nincs")
    sorok = [
        "Write-Host 'CubicLantern Pinggy tunnel'",
        "$Host.UI.RawUI.WindowTitle = %s" % powershellszoveg(cim),
        "Write-Host 'No password or interactive confirmation is required.'",
    ]
    sorok += ["Write-Host %s" % powershellszoveg(sor) for sor in t("pinggy_csatlakozas", port=port, lan=lan).splitlines()]
    if tunnel.get("tipus", "tcp") == "tcp":
        sorok.append("Write-Host %s" % powershellszoveg(t("pinggy_tcp_tipp")))
    sorok += [
        "$program = %s" % powershellszoveg(segito[0]),
        "Write-Host 'The tunnel is running in this window.'",
        "while ($true) {",
        "Start-Process -FilePath $program -ArgumentList @(%s) -NoNewWindow -Wait" % lista,
        "Start-Sleep -Seconds 2",
        "}",
    ]
    launcher.write_text("\r\n".join(sorok) + "\r\n", encoding="utf-8")
    return subprocess.Popen(
        ["cmd.exe", "/d", "/c", "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(launcher)],
        cwd=str(mappa),
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )


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
