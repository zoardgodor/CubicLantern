APP_VERSION = "v1.3.0L"
APP_VERSION_URL = "https://zoardgodor.github.io/CubicLantern/version.txt"
APP_WEBSITE_URL = "https://zoardgodor.github.io/CubicLantern/"

import sys
import os
import re
import json
import base64
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
import signal
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal, QProcess, QProcessEnvironment, QTimer, QUrl, QObject, QSize
from PySide6.QtGui import QAction, QDesktopServices, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QStackedWidget, QDialog, QDialogButtonBox, QLineEdit,
    QComboBox, QCheckBox, QSpinBox, QTabWidget, QScrollArea, QFormLayout, QPlainTextEdit,
    QProgressBar, QMessageBox, QFileDialog, QFrame, QGroupBox, QButtonGroup, QSystemTrayIcon, QMenu
)

try:
    import psutil
except ImportError:
    psutil = None


def adatmappakeresese():
    alap = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(alap) / "CubicLantern"


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
