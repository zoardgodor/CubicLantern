def mappakeszites():
    regi_adatmappamigracio()
    for mappa in (adatmappa, szerverekmappa, javamappa, playitmappa, pinggymappa):
        mappa.mkdir(parents=True, exist_ok=True)


def regi_adatmappamigracio():
    alap = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    regi = Path(alap) / "MinecraftServerMaker"
    if not regi.is_dir():
        return
    if not adatmappa.exists():
        regi.rename(adatmappa)
        return

    def osszefesul(forras, cel):
        for elem in forras.iterdir():
            cel_elem = cel / elem.name
            if not cel_elem.exists() and not cel_elem.is_symlink():
                elem.rename(cel_elem)
            elif elem.is_dir() and not elem.is_symlink() and cel_elem.is_dir() and not cel_elem.is_symlink():
                osszefesul(elem, cel_elem)
                if not any(elem.iterdir()):
                    elem.rmdir()

    osszefesul(regi, adatmappa)
    if not any(regi.iterdir()):
        regi.rmdir()


def lan_ipv4_cim():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as kapcsolat:
            kapcsolat.connect(("192.0.2.1", 80))
            cim = kapcsolat.getsockname()[0]
        if cim and not cim.startswith(("127.", "169.254.")) and cim != "0.0.0.0":
            return cim
    except OSError:
        pass
    if psutil is not None:
        try:
            halozati_cimek = psutil.net_if_addrs()
        except (OSError, psutil.Error):
            return None
        for cimadatok in halozati_cimek.values():
            for cimadat in cimadatok:
                cim = cimadat.address
                if cimadat.family == socket.AF_INET and not cim.startswith(("127.", "169.254.")) and cim != "0.0.0.0":
                    return cim
    return None


def beallitasbetoltes():
    try:
        return json.loads(beallitasfajl.read_text(encoding="utf-8"))
    except Exception:
        return {}


def beallitasmentes(adat):
    beallitasfajl.write_text(json.dumps(adat, indent=2), encoding="utf-8")


def metabetoltes(mappa):
    adat = json.loads((Path(mappa) / "mcmaker.json").read_text(encoding="utf-8"))
    alapport = 19132 if adat.get("tipus") == "bedrock" else 25565
    adat.setdefault("alagut", "off")
    adat.setdefault("pinggy", [{"engedelyezve": True, "tipus": "udp" if adat.get("tipus") == "bedrock" else "tcp", "port": alapport, "jelszo": ""}, {"engedelyezve": False, "tipus": "udp", "port": alapport, "jelszo": ""}, {"engedelyezve": False, "tipus": "http", "port": 8000, "jelszo": ""}])
    modositva = False
    for tunnel in adat["pinggy"]:
        if tunnel.get("tipus") == "udp" and int(tunnel.get("port") or 0) == 25565:
            tunnel["port"] = 19132
            modositva = True
    if modositva:
        metamentes(mappa, adat)
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


def szovegletoltes(url, idokorlat=30):
    with keres(url, idokorlat) as valasz:
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


def fajlkivonat(ut, algoritmus):
    kivonat = hashlib.new(algoritmus)
    with open(ut, "rb") as fajl:
        for blokk in iter(lambda: fajl.read(65536), b""):
            kivonat.update(blokk)
    return kivonat.hexdigest()


def eszkozkivonat(eszkoz):
    digest = str(eszkoz.get("digest") or "")
    algoritmus, elvalaszto, ertek = digest.partition(":")
    hosszak = {"md5": 32, "sha256": 64, "sha384": 96, "sha512": 128}
    if elvalaszto and algoritmus in hosszak and re.fullmatch(r"[0-9a-fA-F]{%d}" % hosszak[algoritmus], ertek):
        return algoritmus, ertek.lower()
    return None, None


def verzioszamok(szoveg):
    return tuple(int(szam) for szam in re.findall(r"\d+", szoveg))


def stabilverzio(szoveg):
    return re.fullmatch(r"\d+(\.\d+)+", szoveg) is not None


def rendezes(lista):
    return sorted(set(lista), key=verzioszamok, reverse=True)


def verziokulcs(verzio):
    talalat = re.fullmatch(r"v?(\d+(?:\.\d+)*)(.*)", str(verzio).strip(), re.IGNORECASE)
    if not talalat:
        return None
    szamok = tuple(int(resz) for resz in talalat.group(1).split("."))
    utotag = talalat.group(2).strip().lower()
    return szamok, utotag


def ujabbappverzio(tavoli, helyi=APP_VERSION):
    tavoli_kulcs = verziokulcs(tavoli)
    helyi_kulcs = verziokulcs(helyi)
    return tavoli_kulcs is not None and helyi_kulcs is not None and tavoli_kulcs > helyi_kulcs


def legujabbappverzio():
    kulcs = platformnev()
    for sor in szovegletoltes(APP_VERSION_URL, 8).splitlines():
        nev, elvalaszto, verzio = sor.partition("=")
        if elvalaszto and nev.strip().lower() == kulcs:
            verzio = verzio.strip()
            return verzio if ujabbappverzio(verzio) else None
    raise ValueError("No version entry for " + kulcs)


def platformnev():
    return "linux"


def architektura():
    gep = platform.machine().lower()
    if gep in ("arm64", "aarch64"):
        return "arm64"
    return "x86_64"


def eszkozvalasztas(eszkozok):
    archszavak = ("arm64", "aarch64") if architektura() == "arm64" else ("x86_64", "x64", "amd64")
    tiltott = (".sha256", ".sha1", ".md5", ".zip", ".tar.gz", ".txt", ".sig", ".pdb", ".json", ".deb", ".rpm", ".msi")
    jeloltek = []
    for eszkoz in eszkozok:
        nev = eszkoz["name"].lower()
        if nev.endswith(tiltott):
            continue
        if "linux" not in nev:
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


def paperjaradat(mc):
    try:
        adat = jsonlekeres("https://fill.papermc.io/v3/projects/paper/versions/%s/builds/latest" % mc)
        letoltes = adat["downloads"]["server:default"]
        return int(adat.get("build") or adat.get("id")), letoltes["url"], letoltes["checksums"]["sha256"]
    except Exception:
        epitesek = jsonlekeres("https://api.papermc.io/v2/projects/paper/versions/%s/builds" % mc)["builds"]
        utolso = epitesek[-1]
        nev = utolso["downloads"]["application"]["name"]
        url = "https://api.papermc.io/v2/projects/paper/versions/%s/builds/%s/downloads/%s" % (mc, utolso["build"], nev)
        return int(utolso["build"]), url, None


def paperjar(mc, cel, haladas):
    epites, url, sha256 = paperjaradat(mc)
    fajlletoltes(url, cel, haladas)
    if sha256 and fajlkivonat(cel, "sha256") != sha256:
        raise RuntimeError("Paper server JAR checksum mismatch.")
    return epites, sha256


def purpurjaradat(mc):
    adat = jsonlekeres("https://api.purpurmc.org/v2/purpur/%s/latest" % mc)
    epites = adat["build"]
    url = "https://api.purpurmc.org/v2/purpur/%s/%s/download" % (mc, epites)
    return int(epites), url, adat.get("md5")


def purpurjar(mc, cel, haladas):
    epites, url, md5 = purpurjaradat(mc)
    fajlletoltes(url, cel, haladas)
    if md5 and fajlkivonat(cel, "md5") != md5:
        raise RuntimeError("Purpur server JAR checksum mismatch.")
    return epites, md5


def jarfrissitesadatok(mappa):
    mappa = Path(mappa)
    meta = metabetoltes(mappa)
    tipus = meta.get("tipus")
    if tipus == "paper":
        epites, url, sha256 = paperjaradat(meta["verzio"])
        telepitett = meta.get("jar_build")
        if telepitett is None and sha256:
            cel = mappa / (meta.get("fajl") or "server.jar")
            if cel.is_file() and fajlkivonat(cel, "sha256") == sha256:
                meta["jar_build"] = epites
                meta["jar_sha256"] = sha256
                metamentes(mappa, meta)
                return None
        if telepitett is not None and int(telepitett) >= epites:
            return None
        return {"tipus": tipus, "verzio": str(epites), "kulcs": "jar_build", "ertek": epites, "url": url, "cel": meta.get("fajl") or "server.jar", "hash_algoritmus": "sha256", "hash": sha256}
    if tipus == "purpur":
        epites, url, md5 = purpurjaradat(meta["verzio"])
        telepitett = meta.get("jar_build")
        if telepitett is None and md5:
            cel = mappa / (meta.get("fajl") or "server.jar")
            if cel.is_file() and fajlkivonat(cel, "md5") == md5:
                meta["jar_build"] = epites
                meta["jar_md5"] = md5
                metamentes(mappa, meta)
                return None
        if telepitett is not None and int(telepitett) >= epites:
            return None
        return {"tipus": tipus, "verzio": str(epites), "kulcs": "jar_build", "ertek": epites, "url": url, "cel": meta.get("fajl") or "server.jar", "hash_algoritmus": "md5", "hash": md5}
    if tipus == "pumpkin":
        kiadas = pumpkinkiadas()
        verzio = str(kiadas.get("tag_name") or kiadas.get("name") or "")
        eszkoz = eszkozvalasztas(kiadas.get("assets", []))
        if not verzio or not eszkoz:
            raise RuntimeError("PumpkinMC update asset was not found for Linux.")
        algoritmus, digest = eszkozkivonat(eszkoz)
        if not meta.get("jar_version") and digest:
            cel = mappa / (meta.get("fajl") or "pumpkin")
            if cel.is_file() and fajlkivonat(cel, algoritmus) == digest:
                meta["jar_version"] = verzio
                meta["jar_" + algoritmus] = digest
                metamentes(mappa, meta)
                return None
        if meta.get("jar_version") == verzio:
            return None
        return {"tipus": tipus, "verzio": verzio, "kulcs": "jar_version", "ertek": verzio, "url": eszkoz["browser_download_url"], "cel": meta.get("fajl") or "pumpkin", "hash_algoritmus": algoritmus, "hash": digest}
    return None


def jarfrissitesletoltes(mappa, frissites):
    mappa = Path(mappa)
    cel = mappa / frissites["cel"]
    ideiglenes = cel.with_name(cel.name + ".update")
    try:
        fajlletoltes(frissites["url"], ideiglenes)
        if frissites.get("hash"):
            if fajlkivonat(ideiglenes, frissites["hash_algoritmus"]) != frissites["hash"]:
                raise RuntimeError("Downloaded server file checksum mismatch.")
        ideiglenes.replace(cel)
        if frissites["tipus"] == "pumpkin":
            cel.chmod(cel.stat().st_mode | 0o111)
    finally:
        ideiglenes.unlink(missing_ok=True)
        ideiglenes.with_name(ideiglenes.name + ".resz").unlink(missing_ok=True)
    meta = metabetoltes(mappa)
    meta[frissites["kulcs"]] = frissites["ertek"]
    if frissites.get("hash"):
        meta["jar_" + frissites["hash_algoritmus"]] = frissites["hash"]
    metamentes(mappa, meta)
    return frissites["verzio"]


def fabricjar(mc, cel, haladas):
    betolto = [elem["version"] for elem in jsonlekeres("https://meta.fabricmc.net/v2/versions/loader") if elem.get("stable")][0]
    telepito = [elem["version"] for elem in jsonlekeres("https://meta.fabricmc.net/v2/versions/installer") if elem.get("stable")][0]
    fajlletoltes("https://meta.fabricmc.net/v2/versions/loader/%s/%s/%s/server/jar" % (mc, betolto, telepito), cel, haladas)
