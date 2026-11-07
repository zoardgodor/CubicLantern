def pinggysegitofolyamat():
    jel = "--cubiclantern-pinggy-tunnel"
    try:
        index = sys.argv.index(jel)
    except ValueError:
        return 1
    if len(sys.argv) <= index + 1:
        return 1
    try:
        payload = base64.b64decode(sys.argv[index + 1]).decode("utf-8")
        adatok = json.loads(payload)
        parancs = [adatok["program"]] + adatok["argumentumok"]
    except (ValueError, KeyError, TypeError, UnicodeDecodeError):
        try:
            adatok = json.loads(sys.argv[index + 1])
            parancs = [adatok["program"]] + adatok["argumentumok"]
        except (json.JSONDecodeError, KeyError, TypeError):
            adatok = {"program": sys.argv[index + 1], "argumentumok": sys.argv[index + 2:], "tipus": "tcp"}
            parancs = [adatok["program"]] + adatok["argumentumok"]
    if adatok.get("nyelv") in szovegek:
        allapot["nyelv"] = adatok["nyelv"]
    try:
        kilepesi_kod = pinggyptyparancs(parancs)
    except OSError as hiba:
        kilepesi_kod = 1
        if not adatok.get("pinggy_cli"):
            raise
        print("Pinggy CLI could not be started: %s" % hiba)
    if not adatok.get("pinggy_cli"):
        return kilepesi_kod
    if adatok.get("tipus") == "udp":
        print(t("pinggy_udp_fallback"))
        pinggyhibavarakozas()
        return 0
    if not adatok.get("fallback"):
        print(t("pinggy_ssh_hianyzik"))
        pinggyhibavarakozas()
        return 0
    ssh = sshprogram()
    if not ssh:
        print(t("pinggy_ssh_hianyzik"))
        pinggyhibavarakozas()
        return 0
    adatok["fallback"][0] = ssh
    print(t("pinggy_cli_hiba"))
    sys.stdout.flush()
    try:
        return pinggyptyparancs(adatok["fallback"])
    except OSError as hiba:
        print("OpenSSH could not be started: %s" % hiba)
        print(t("pinggy_ssh_hianyzik"))
        pinggyhibavarakozas()
        return 0


def pinggyhibavarakozas():
    print("Press Enter to retry after installing or repairing the required client.")
    sys.stdout.flush()
    try:
        sys.stdin.readline()
    except (AttributeError, OSError):
        time.sleep(30)


def pinggyptyparancs(parancs):
    import pty
    import select

    def kiir(adat):
        szoveg = adat.decode("utf-8", errors="replace")
        sys.stdout.write(szoveg)
        sys.stdout.flush()

    pid, leiro = pty.fork()
    if pid == 0:
        os.execvp(parancs[0], parancs)
    elozo_kezelok = {}
    gyerek_kilepett = False

    def gyerek_leallitasa(jel, keret):
        try:
            os.killpg(pid, jel)
        except OSError:
            try:
                os.kill(pid, jel)
            except OSError:
                pass

    for jel in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        elozo_kezelok[jel] = signal.signal(jel, gyerek_leallitasa)
    try:
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
                    kiir(os.read(leiro, 4096))
                except OSError:
                    break
        while True:
            elerheto, _, _ = select.select([leiro], [], [], 0.1)
            if elerheto:
                try:
                    kiir(os.read(leiro, 4096))
                except OSError:
                    pass
            kilepesi, status = os.waitpid(pid, os.WNOHANG)
            if kilepesi == pid:
                gyerek_kilepett = True
                return os.waitstatus_to_exitcode(status)
    finally:
        for jel, kezelo in elozo_kezelok.items():
            signal.signal(jel, kezelo)
        if not gyerek_kilepett:
            gyerek_leallitasa(signal.SIGTERM, None)
            try:
                os.waitpid(pid, 0)
            except ChildProcessError:
                pass
        try:
            os.close(leiro)
        except OSError:
            pass


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
