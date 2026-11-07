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
        folyamat = subprocess.Popen(
            [str(java), "-jar", jar, "--installServer"],
            cwd=str(mappa),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            creationflags=subprocess.CREATE_NO_WINDOW,
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
            "pinggy": [{"engedelyezve": True, "tipus": "udp" if tipus == "bedrock" else "tcp", "port": 19132 if tipus == "bedrock" else 25565, "jelszo": ""}, {"engedelyezve": False, "tipus": "udp", "port": 19132, "jelszo": ""}, {"engedelyezve": False, "tipus": "http", "port": 8000, "jelszo": ""}],
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
            meta["jar_build"], meta["jar_sha256"] = paperjar(verzio, cel, self.haladas.emit)
            meta["fajl"] = "server.jar"
        elif tipus == "purpur":
            meta["jar_build"], meta["jar_md5"] = purpurjar(verzio, cel, self.haladas.emit)
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
        elif tipus == "pumpkin":
            kiadas = pumpkinkiadas()
            eszkoz = eszkozvalasztas(kiadas["assets"])
            if not eszkoz:
                raise RuntimeError("PumpkinMC binary not found for this platform")
            nev = "pumpkin.exe"
            fajlletoltes(eszkoz["browser_download_url"], mappa / nev, self.haladas.emit)
            meta["fajl"] = nev
            meta["verzio"] = "latest"
            meta["jar_version"] = str(kiadas.get("tag_name") or kiadas.get("name") or "latest")
            algoritmus, digest = eszkozkivonat(eszkoz)
            if digest:
                if fajlkivonat(mappa / nev, algoritmus) != digest:
                    raise RuntimeError("PumpkinMC server file checksum mismatch.")
                meta["jar_" + algoritmus] = digest
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


class konzolablak(QDialog):
    def __init__(self, szerver, szulo=None):
        super().__init__(szulo, Qt.WindowType.Window)
        self.szerver = szerver
        self.setWindowTitle(t("konzol_megnyitasa") + " — " + szerver.meta.get("nev", "Minecraft"))
        self.resize(900, 580)
        fo = QVBoxLayout(self)
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
        szerver.sorkesz.connect(self.konzolsor)
        szerver.allapotvaltozas.connect(self.frissit)
        self.frissit()

    def konzolsor(self, sor):
        self.konzol.appendPlainText(sor)

    def kuldes(self):
        szoveg = self.beviteli.text().strip()
        if szoveg and self.szerver.fut():
            self.szerver.parancs(szoveg)
        self.beviteli.clear()

    def frissit(self):
        fut = self.szerver.fut()
        self.beviteli.setEnabled(fut)
        self.kuldgomb.setEnabled(fut)

    def closeEvent(self, esemeny):
        esemeny.ignore()
        self.hide()


class iranyitooldal(QWidget):
    def __init__(self, szerver, szulo=None):
        super().__init__(szulo)
        self.szerver = szerver
        self.konzolablak = konzolablak(szerver, self)
        self.killgombaktiv = False
        tipus = szerver.tipus()
        fo = QVBoxLayout(self)
        fo.setContentsMargins(0, 0, 0, 0)
        gombok = QHBoxLayout()
        self.startgomb = QPushButton(t("start"))
        self.startgomb.setObjectName("zold")
        self.stopgomb = QPushButton(t("stop"))
        self.stopgomb.setObjectName("piros")
        self.ujragomb = QPushButton(t("restart"))
        self.startgomb.clicked.connect(self.inditas)
        self.stopgomb.clicked.connect(self.leallitas)
        self.ujragomb.clicked.connect(self.ujrainditas)
        self.konzolgomb = QPushButton(t("konzol_megnyitasa"))
        self.konzolgomb.clicked.connect(self.konzolmegnyitasa)
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
        self.konzolelonezet = QPlainTextEdit()
        self.konzolelonezet.setObjectName("konzol")
        self.konzolelonezet.setReadOnly(True)
        self.konzolelonezet.setMaximumBlockCount(300)
        self.konzolelonezet.setPlainText("\n".join(szerver.sorok))
        fo.addWidget(self.konzolelonezet, 1)
        self.memoriacimke = QLabel()
        self.memoriacimke.setObjectName("halvany")
        self.memoriasav = QProgressBar()
        self.memoriasav.setTextVisible(True)
        fo.addWidget(self.memoriacimke)
        fo.addWidget(self.memoriasav)
        fo.addWidget(self.konzolgomb, 0, Qt.AlignmentFlag.AlignLeft)
        self.memoriaidozito = QTimer(self)
        self.memoriaidozito.timeout.connect(self.memoriafrissites)
        self.memoriaidozito.start(1000)
        szerver.sorkesz.connect(self.konzolelonesor)
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
        self.playitablak = QDialog(self, Qt.WindowType.Window)
        self.playitablak.setWindowTitle("Playit")
        self.playitablak.resize(620, 420)
        playitfo = QVBoxLayout(self.playitablak)
        playitfo.addWidget(playitdoboz)
        szolgaltatosor = QHBoxLayout()
        szolgaltatosor.addWidget(QLabel(t("alagut_mindketto")))
        infogomb = QPushButton("ⓘ")
        infogomb.setToolTip(t("pinggy_info"))
        infogomb.clicked.connect(lambda: QMessageBox.information(self, t("alagut_valaszto"), t("pinggy_info") + "\n\n" + t("svc_info")))
        szolgaltatosor.addWidget(infogomb)
        szolgaltatosor.addStretch()
        pinggyablak = QDialog(self, Qt.WindowType.Window)
        pinggyablak.setWindowTitle("Pinggy")
        pinggyablak.resize(760, 680)
        self.pinggyablak = pinggyablak
        pinggyfo = QVBoxLayout(pinggyablak)
        pinggyfo.addLayout(szolgaltatosor)
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
            alapport = 19132 if adat.get("tipus") == "udp" else (8000 if adat.get("tipus") == "http" else 25565)
            portmezo.setValue(int(adat.get("port") or alapport))
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
        self.pinggycimek = QLabel()
        self.pinggycimek.setWordWrap(True)
        self.pinggycimek.setObjectName("halvany")
        pinggyelrendezes.addWidget(self.pinggycimek)
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
        self.pinggyallapot.setWordWrap(True)
        pinggyelrendezes.addWidget(self.pinggyallapot)
        pinggyfo.addWidget(pinggydoboz)
        szolgaltatogombok = QHBoxLayout()
        self.playitgombablak = QPushButton("Playit")
        self.pinggygombablak = QPushButton("Pinggy")
        self.playitgombablak.clicked.connect(self.playitablakmegnyitasa)
        self.pinggygombablak.clicked.connect(self.pinggyablakmegnyitasa)
        szolgaltatogombok.addWidget(self.playitgombablak)
        szolgaltatogombok.addWidget(self.pinggygombablak)
        szolgaltatogombok.addStretch()
        fo.addLayout(szolgaltatogombok)
        szerver.allapotvaltozas.connect(self.frissit)
        szerver.playitvaltozas.connect(self.playitfrissites)
        self.frissit()
        self.pinggymentese()
        self.pinggybinarisfrissitese()

    def konzolmegnyitasa(self):
        self.konzolablak.show()
        self.konzolablak.raise_()
        self.konzolablak.activateWindow()

    def konzolelonesor(self, sor):
        self.konzolelonezet.appendPlainText(sor)

    def playitablakmegnyitasa(self):
        self.playitablak.show()
        self.playitablak.raise_()
        self.playitablak.activateWindow()

    def pinggyablakmegnyitasa(self):
        self.pinggyablak.show()
        self.pinggyablak.raise_()
        self.pinggyablak.activateWindow()

    def inditas(self):
        self.konzolmegnyitasa()
        self.szerver.inditas()

    def leallitas(self):
        self.szerver.leallitas()
        QTimer.singleShot(2000, self.killgombmutatasa)

    def killgombmutatasa(self):
        if self.szerver.fut():
            self.stopgomb.setText(t("kill"))
            self.stopgomb.clicked.disconnect(self.leallitas)
            self.stopgomb.clicked.connect(self.killkerdes)
            self.killgombaktiv = True

    def killkerdes(self):
        valasz = QMessageBox.question(
            self,
            t("kill_cim"),
            t("kill_szoveg"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if valasz == QMessageBox.StandardButton.Yes:
            self.szerver.kenyszerleallitas(self.szerver.leallitasjel)

    def ujrainditas(self):
        self.konzolmegnyitasa()
        self.szerver.ujrainditas()

    def frissit(self):
        fut = self.szerver.fut()
        foglalt = self.szerver.javafoglalt
        self.startgomb.setEnabled(not fut and not foglalt)
        self.stopgomb.setEnabled(fut)
        self.ujragomb.setEnabled(fut)
        if not fut and self.killgombaktiv:
            self.stopgomb.setText(t("stop"))
            self.stopgomb.clicked.disconnect(self.killkerdes)
            self.stopgomb.clicked.connect(self.leallitas)
            self.killgombaktiv = False
        self.playitfrissites()

    def memoriafrissites(self):
        osszes = max(0, int(self.szerver.meta.get("ram") or 0))
        hasznalt = max(0, int(self.szerver.memoria()))
        if osszes <= 0:
            self.memoriacimke.clear()
            self.memoriasav.setRange(0, 1)
            self.memoriasav.setValue(0)
            self.memoriasav.setVisible(False)
            return
        self.memoriasav.setVisible(True)
        self.memoriasav.setRange(0, osszes)
        self.memoriasav.setValue(min(hasznalt, osszes))
        self.memoriacimke.setText("%s: %d / %d MB" % (t("memoria"), hasznalt, osszes))

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
        lan = lan_ipv4_cim() or t("pinggy_lan_nincs")
        cimek = t("pinggy_csatlakozas", port=self.szerver.portszam(), lan=lan)
        if any(tunnel["engedelyezve"] and tunnel["tipus"] == "tcp" for tunnel in adat):
            cimek += "\n" + t("pinggy_tcp_tipp")
        self.pinggycimek.setText(cimek)
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
            tunnelek = [tunnel for tunnel in self.szerver.meta.get("pinggy", []) if tunnel.get("engedelyezve")]
            if any(tunnel.get("tipus") == "udp" for tunnel in tunnelek) and not pinggyprogram():
                QMessageBox.warning(self, t("figyelem"), t("pinggy_hianyzik"))
                self.szerver.pinggyallapot = t("pinggy_hianyzik")
                self.playitfrissites()
                return
            if not pinggyprogram() and any(tunnel.get("tipus") != "udp" for tunnel in tunnelek) and not sshprogram():
                QMessageBox.warning(self, t("figyelem"), t("pinggy_ssh_hianyzik"))
                self.szerver.pinggyallapot = t("pinggy_ssh_hianyzik")
                self.playitfrissites()
                return
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
        self.playitgomb.setObjectName("zold" if fut else "")
        self.playitgomb.style().unpolish(self.playitgomb)
        self.playitgomb.style().polish(self.playitgomb)
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
            pinggyfut = self.szerver.pinggyfut()
            self.pinggygomb.setText(t("pinggy_leallit") if pinggyfut else t("pinggy_indit"))
            self.pinggygomb.setObjectName("zold" if pinggyfut else "")
            self.pinggygomb.style().unpolish(self.pinggygomb)
            self.pinggygomb.style().polish(self.pinggygomb)
            self.pinggygombablak.setObjectName("zold" if pinggyfut else "")
            self.pinggygombablak.style().unpolish(self.pinggygombablak)
            self.pinggygombablak.style().polish(self.pinggygombablak)
            self.pinggymentese()
            self.pinggyallapot.setText(t("pinggy_allapot") + ": " + (self.szerver.pinggyallapot or t("pinggy_all")))

    def cimmentes(self):
        self.szerver.playitcimmentes(self.cimmezo.text())

    def cimmasolas(self):
        QApplication.clipboard().setText(self.cimmezo.text().strip())

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
        self.jarfrissitescimke = None
        self.jarfrissitesgomb = None
        if self.tipus in ("paper", "purpur", "pumpkin"):
            self.jarfrissitescimke = QLabel()
            self.jarfrissitescimke.setWordWrap(True)
            self.jarfrissitescimke.setObjectName("halvany")
            self.jarfrissitesgomb = QPushButton(t("jar_update_search"))
            self.jarfrissitesgomb.clicked.connect(self.jarfrissiteskeresese)
            fo.addWidget(self.jarfrissitescimke)
            fo.addWidget(self.jarfrissitesgomb, 0, Qt.AlignmentFlag.AlignLeft)
            QTimer.singleShot(0, self.jarfrissiteskeresese)
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
        talcagomb = QCheckBox(t("talca"))
        talcagomb.setChecked(beallitasbetoltes().get("talca", False))
        talcagomb.toggled.connect(self.talcamentese)
        fo.addWidget(talcagomb, 0, Qt.AlignmentFlag.AlignLeft)
        torlesgomb = QPushButton(t("szerver_torlese"))
        torlesgomb.setObjectName("piros")
        torlesgomb.clicked.connect(self.torles)
        fo.addWidget(torlesgomb, 0, Qt.AlignmentFlag.AlignLeft)
        self.frissit()

    def talcamentese(self, engedelyezve):
        beallitasok = beallitasbetoltes()
        beallitasok["talca"] = engedelyezve
        beallitasmentes(beallitasok)
        ablak = self.window()
        if hasattr(ablak, "talcabeallitasa"):
            ablak.talcabeallitasa(engedelyezve)

    def jarfrissiteskeresese(self):
        if self.jarfrissitesgomb is None:
            return
        self.jarfrissitesgomb.setEnabled(False)
        self.jarfrissitescimke.setText(t("jar_update_checking"))
        hatterfeladat(
            lambda: jarfrissitesadatok(self.szerver.mappa),
            self.jarfrissiteskesz,
            self.jarfrissiteshiba,
        )

    def jarfrissiteskesz(self, frissites):
        self.jarfrissitesgomb.setEnabled(True)
        if frissites is None:
            self.jarfrissitescimke.setText(t("jar_update_none"))
            return
        self.jarfrissitescimke.setText(t("jar_update_available", verzio=frissites["verzio"]))
        valasz = QMessageBox.question(
            self,
            t("figyelem"),
            t("jar_update_available", verzio=frissites["verzio"]),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if valasz == QMessageBox.StandardButton.Yes:
            self.jarfrissitesletoltes(frissites)

    def jarfrissiteshiba(self, hiba):
        self.jarfrissitesgomb.setEnabled(True)
        self.jarfrissitescimke.setText(t("jar_update_offline"))
        self.jarfrissitescimke.setToolTip(str(hiba))

    def jarfrissitesletoltes(self, frissites):
        if self.szerver.fut():
            QMessageBox.warning(self, t("figyelem"), t("jar_update_running"))
            return
        self.jarfrissitesgomb.setEnabled(False)
        self.jarfrissitescimke.setText(t("jar_update_downloading", verzio=frissites["verzio"]))
        hatterfeladat(
            lambda: jarfrissitesletoltes(self.szerver.mappa, frissites),
            self.jarfrissiteskeszlet,
            self.jarfrissitesletolteshiba,
        )

    def jarfrissiteskeszlet(self, verzio):
        self.szerver.meta = metabetoltes(self.szerver.mappa)
        self.jarfrissitesgomb.setEnabled(True)
        self.jarfrissitescimke.setText(t("jar_update_done", verzio=verzio))

    def jarfrissitesletolteshiba(self, hiba):
        self.jarfrissitesgomb.setEnabled(True)
        self.jarfrissitescimke.setText(t("jar_update_error", hiba=hiba))
        QMessageBox.warning(self, t("hiba"), t("jar_update_error", hiba=hiba))

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
