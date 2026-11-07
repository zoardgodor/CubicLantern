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
    if sys.stdout is None or sys.stderr is None or sys.stdin is None:
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
            if sys.stdin is None:
                sys.stdin = open("CONIN$", "r", encoding="utf-8", errors="replace")
        except OSError:
            pass
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
    try:
        from winpty import PtyProcess, WinptyError
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
    try:
        folyamat = PtyProcess.spawn(subprocess.list2cmdline(parancs))
    except WinptyError as hiba:
        raise OSError(str(hiba)) from hiba

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
    return folyamat.wait()


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
