"""
Modul für den Datenabruf (Data Scraper).

Dieses Modul ist dafür zuständig, die aktuellen Leistungsdaten der Photovoltaik-Anlage
von der Schnittstelle abzufragen.
"""

from typing import Any, Dict
from .config import Config


class PVDataCollector:
    """
    Diese Klasse holt die aktuellen Leistungsdaten der PV-Anlage ab.
    """

    def __init__(self, config: Config = None):
        """
        Initialisiert den Datensammler mit der API-Konfiguration.
        """
        # Falls keine Config übergeben wird, erstellen wir eine Standard-Config.
        self.config = config or Config()
        # Setzt ein Timeout (wie lange wir auf eine Antwort warten)
        self.timeout_seconds = 5.0

    def fetch_latest_data(self) -> Dict[str, Any]:
        """
        Fragt den aktuellen Datenpunkt vom Server ab (GET-Request).

        Diese Funktion führt den Netzwerk-Aufruf durch und fängt eventuelle
        Fehler ab, damit das gesamte Programm nicht abstürzt.

        Rückgabewert:
            Ein Python-Wörterbuch (dict) mit den gelieferten JSON-Werten.
        """
        # Für das Gerüst (Stub) geben wir erst einmal ein leeres Wörterbuch zurück.
        return {}
