"""
Konfigurationsmodul.

Dieses Modul verwaltet alle Einstellungen des PV-Dashboards über eine
zentrale Datenklasse (dataclass).
"""

import os
from dataclasses import dataclass


def load_env_file():
    """
    Lädt Umgebungsvariablen aus einer .env-Datei, falls vorhanden.
    Verhindert das Einchecken von Credentials in Git.
    """
    env_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        ".env",
    )
    if not os.path.exists(env_path):
        # Fallback auf aktuelles Verzeichnis für Tests/Docker
        env_path = ".env"

    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        # Anführungszeichen entfernen falls vorhanden
                        val = val.strip().strip("'\"")
                        os.environ[key.strip()] = val
        except Exception:
            pass


# Lade Umgebungsvariablen vor der Initialisierung der Config-Klasse
load_env_file()


@dataclass
class Config:
    """
    Klasse zur Kapselung aller Konfigurationsparameter.
    Lädt Werte standardmäßig aus Umgebungsvariablen oder nutzt sichere Fallbacks.
    """

    # 1. API-Verbindung zur PV-Anlage
    pv_api_url: str = os.getenv("PV_API_URL", "https://api.solar-thi.de/v1/metrics")
    pv_api_key: str = os.getenv("PV_API_KEY", "")

    # 2. Intervall für den Hintergrund-Scraper (in Sekunden)
    scraping_interval_seconds: float = float(os.getenv("PV_SCRAPING_INTERVAL", "10.0"))

    # 3. Datenbank-Pfad
    db_path: str = os.getenv("PV_DB_PATH", "data/pv_metrics.db")

    # 4. Physikalische Grenzwerte (in Watt) für das Cleaning
    max_realistic_w: float = float(os.getenv("PV_MAX_REALISTIC_W", "500000.0"))
