"""
Modul für den Datenabruf (Data Scraper).

Dieses Modul ist dafür zuständig, die aktuellen Leistungsdaten der Photovoltaik-Anlage
von der Schnittstelle abzufragen.
"""

import logging
import requests
import urllib3
from typing import Any, Dict
from .config import Config

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PVDataCollector:
    """
    Diese Klasse holt die aktuellen Leistungsdaten der PV-Anlage ab.
    """

    def __init__(self, config: Config = None):
        """
        Initialisiert den Datensammler mit der API-Konfiguration.
        """
        self.config = config or Config()
        self.timeout_seconds = 5.0

    def fetch_latest_data(self) -> Dict[str, Any]:
        """
        Fragt den aktuellen Datenpunkt vom Server ab (GET-Request).

        Diese Funktion führt den Netzwerk-Aufruf durch und fängt eventuelle
        Fehler ab, damit das gesamte Programm nicht abstürzt.

        Rückgabewert:
            Ein Python-Wörterbuch (dict) mit den gelieferten JSON-Werten.
        """
        if not self.config.pv_api_url:
            logger.error("API URL ist nicht konfiguriert.")
            return {}

        headers = {}
        if self.config.pv_api_key:
            headers["X-API-Key"] = self.config.pv_api_key

        try:
            logger.debug(f"Rufe Daten ab von: {self.config.pv_api_url}")
            # verify=False entspricht dem -k Parameter in curl
            response = requests.get(
                self.config.pv_api_url,
                headers=headers,
                timeout=self.timeout_seconds,
                verify=False,
            )
            response.raise_for_status()
            data = response.json()
            logger.info("PV-Daten erfolgreich von API abgerufen.")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen der PV-Daten: {e}")
            return {}
