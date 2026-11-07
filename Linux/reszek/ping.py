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

