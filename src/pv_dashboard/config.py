"""
Konfigurationsmodul.

Dieses Modul verwaltet alle Einstellungen des PV-Dashboards über eine
zentrale Datenklasse (dataclass).
"""

import os
from dataclasses import dataclass


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
    scraping_interval_seconds: float = float(os.getenv("PV_SCRAPING_INTERVAL", "5.0"))

    # 3. Datenbank-Pfad
    db_path: str = os.getenv("PV_DB_PATH", "pv_metrics.db")

    # 4. Physikalische Grenzwerte (in Watt) für das Cleaning
    max_realistic_w: float = float(os.getenv("PV_MAX_REALISTIC_W", "20000.0"))
