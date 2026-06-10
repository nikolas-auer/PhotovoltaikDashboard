"""
Modul für den Datenabruf (Data Scraper).

Dieses Modul ist dafür zuständig, die aktuellen Leistungsdaten der Photovoltaik-Anlage
von der Schnittstelle abzufragen.
"""

import os
from typing import Any, Dict


class PVDataCollector:
    """
    Diese Klasse holt die aktuellen Leistungsdaten der PV-Anlage ab.
    """

    def __init__(self, api_url: str = None, api_key: str = None):
        """
        Initialisiert den Datensammler mit der API-Adresse und dem Schlüssel.

        Wenn keine Werte angegeben werden, sucht Python automatisch nach
        Umgebungsvariablen (das erhöht die Sicherheit).
        """
        # Setzt die Ziel-URL
        self.api_url = api_url or os.getenv(
            "PV_API_URL", "https://api.solar-thi.de/v1/metrics"
        )
        # Setzt den API-Schlüssel
        self.api_key = api_key or os.getenv("PV_API_KEY", "")
        # Setzt ein Timeout (wie lange wir auf eine Antwort warten)
        self.timeout_seconds = 5.0

    def fetch_latest_data(self) -> Dict[str, Any]:
        """
        Fragt den aktuellen Datenpunkt vom Server ab (GET-Request).

        Diese Funktion führt den Netzwerk-Aufruf durch und fängt eventuelle
        Fehler (wie z. B. Verbindungsverlust, falsche Passwörter oder Server-Abstürze)
        ab, damit das gesamte Programm nicht abstürzt.

        Rückgabewert:
            Ein Python-Wörterbuch (dict) mit den gelieferten JSON-Werten.
        """
        # Hier wird später der echte Aufruf mit dem requests-Modul implementiert.
        # Beispiel: response = requests.get(self.api_url, headers=...)
        # Für das Gerüst (Stub) geben wir erst einmal ein leeres Wörterbuch zurück.
        return {}
