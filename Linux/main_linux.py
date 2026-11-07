from pathlib import Path


def betoltes():
    mappa = Path(__file__).with_name("reszek")
    fajlok = (
        "alap.py",
        "szoveg.py",
        "halozat.py",
        "letoltes.py",
        "ping.py",
        "folyamat.py",
        "oldalak.py",
        "stilus.py",
        "ablak.py",
        "inditas.py",
    )
    for nev in fajlok:
        utvonal = mappa / nev
        kod = utvonal.read_text(encoding="utf-8")
        exec(compile(kod, str(utvonal), "exec"), globals())

betoltes()
