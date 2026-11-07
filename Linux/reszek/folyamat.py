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
        nev = "unix_args.txt"
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
            return str(self.mappa / "bedrock_server"), []
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
        if self.tipus() == "bedrock":
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
        if not pinggyprogram() and any(tunnel.get("tipus") != "udp" for tunnel in aktiv) and not sshprogram():
            self.pinggyaktiv = False
            self.pinggyallapot = t("pinggy_ssh_hianyzik")
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
                pidfajl = getattr(folyamat, "pinggy_pidfajl", None)
                launcher = getattr(folyamat, "pinggy_launcher", None)
                if pidfajl is not None and launcher is not None:
                    for _ in range(10):
                        try:
                            pid = int(pidfajl.read_text(encoding="ascii").strip())
                        except (OSError, ValueError):
                            if folyamat.poll() is not None:
                                break
                            time.sleep(0.1)
                            continue
                        try:
                            parancssor = Path("/proc/%d/cmdline" % pid).read_bytes()
                        except OSError:
                            parancssor = b""
                        if str(launcher).encode() in parancssor:
                            try:
                                os.kill(pid, 15)
                            except OSError:
                                pass
                            break
                        time.sleep(0.1)
                    try:
                        folyamat.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        try:
                            os.killpg(folyamat.pid, 15)
                        except OSError:
                            folyamat.terminate()
                        try:
                            folyamat.wait(timeout=2)
                        except subprocess.TimeoutExpired:
                            try:
                                os.killpg(folyamat.pid, 9)
                            except OSError:
                                folyamat.kill()
                            folyamat.wait(timeout=2)
                    for fajl in (pidfajl, launcher):
                        if fajl is not None:
                            fajl.unlink(missing_ok=True)
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
        self.kiir(t("backup_saved", fajl=Path(fajl).name))
        self.allapotvaltozas.emit()

    def backuphiba(self, uzenet):
        self.backupfolyamatban = False
        self.kiir(t("backup_error", hiba=uzenet))
        self.allapotvaltozas.emit()

    def backupfigyelo(self):
        backup = self.meta.get("backup", {})
        if not self.fut() or not backup.get("engedelyezve", True) or int(backup.get("intervallum") or 0) <= 0:
            return
        if time.monotonic() >= self.backupkovetkezo:
            self.backupinditas()

