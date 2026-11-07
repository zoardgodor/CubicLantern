class foablak(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("cim"))
        self.resize(1150, 780)
        self.szerverek = {}
        self.biztoskilepes = False
        self.aktualisoldal = None
        self.frissitesi_verzio = None
        self.talca_kilepes = False
        self.verem = QStackedWidget()
        self.setCentralWidget(self.verem)
        self.talcaikon = QSystemTrayIcon(QIcon(), self)
        csomagoltmappa = Path(getattr(sys, "_MEIPASS", ""))
        ikonok = (
            csomagoltmappa / "icon-CL.ico",
            Path(__file__).resolve().parent / "icon-CL.ico",
            Path(__file__).resolve().parent.parent / "icon-CL.ico",
            Path(__file__).resolve().parent.parent / "icon-CL-icon-pack" / "icon-CL.ico",
        )
        for ikon in ikonok:
            if ikon.exists():
                self.talcaikon.setIcon(QIcon(str(ikon)))
                break
        self.talcamenu = QMenu(self)
        megnyitas = QAction(t("megnyitas"), self)
        megnyitas.triggered.connect(self.talcamegnyitasa)
        kilepes = QAction(t("kilepes"), self)
        kilepes.triggered.connect(self.talcakilepes)
        self.talcamenu.addAction(megnyitas)
        self.talcamenu.addSeparator()
        self.talcamenu.addAction(kilepes)
        self.talcaikon.setContextMenu(self.talcamenu)
        self.talcaikon.activated.connect(self.talcaesemeny)
        self.talcaikon.setVisible(False)
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
        self.frissitesgomb = QPushButton(t("app_update_button"))
        self.frissitesgomb.clicked.connect(self.appfrissitesinditasa)
        self.frissitesgomb.setVisible(False)
        self.nyelvgomb = QPushButton("Language")
        self.nyelvgomb.clicked.connect(self.nyelvablak)
        felso.addWidget(self.frissitesgomb)
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
        self.talcabeallitasa(beallitasbetoltes().get("talca", False))
        self.listafrissites()
        QTimer.singleShot(0, self.appfrissiteskeresese)

    def appfrissiteskeresese(self):
        hatterfeladat(
            legujabbappverzio,
            self.appfrissiteskereseskesz,
            self.appfrissiteskereseshhiba,
        )

    def appfrissiteskereseshhiba(self, hiba):
        self.frissitesgomb.setToolTip(str(hiba))

    def appfrissiteskereseskesz(self, verzio):
        if not verzio:
            return
        self.frissitesi_verzio = verzio
        uzenet = QMessageBox(self)
        uzenet.setWindowTitle(t("app_update_title"))
        uzenet.setText(t("app_update_prompt", verzio=verzio))
        frissitesgomb = uzenet.addButton(t("app_update_now"), QMessageBox.ButtonRole.AcceptRole)
        uzenet.addButton(t("app_update_later"), QMessageBox.ButtonRole.RejectRole)
        uzenet.exec()
        if uzenet.clickedButton() == frissitesgomb:
            self.appfrissitesinditasa()
        else:
            self.frissitesgomb.setVisible(True)

    def appfrissitesinditasa(self):
        if not QDesktopServices.openUrl(QUrl(APP_WEBSITE_URL)):
            QMessageBox.information(
                self,
                t("app_update_title"),
                t("app_update_website", url=APP_WEBSITE_URL),
            )
            return
        self.mindenleallitasa()
        self.biztoskilepes = True
        self.close()

    def talcabeallitasa(self, engedelyezve):
        if engedelyezve and QSystemTrayIcon.isSystemTrayAvailable():
            self.talcaikon.show()
        else:
            self.talcaikon.hide()

    def talcamegnyitasa(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def talcaesemeny(self, ok):
        if ok in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self.talcamegnyitasa()

    def talcakilepes(self):
        self.talca_kilepes = True
        if self.close():
            self.talcaikon.hide()
            QApplication.quit()

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
        if not self.talca_kilepes and beallitasbetoltes().get("talca", False) and QSystemTrayIcon.isSystemTrayAvailable():
            self.hide()
            self.talcaikon.show()
            esemeny.ignore()
            return
        if self.futoszerverek():
            valasz = QMessageBox.question(self, t("kilepes_cim"), t("kilepes_szoveg"), QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if valasz != QMessageBox.StandardButton.Yes:
                esemeny.ignore()
                return
        self.mindenleallitasa()
        self.biztoskilepes = True
        esemeny.accept()
