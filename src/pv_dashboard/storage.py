"""
Modul für die Datenspeicherung (Data Storage).

Dieses Modul verwaltet die lokale Speicherung unserer Messwerte in einer SQLite-Datenbank.
Es stellt sicher, dass historische Daten auch nach einem Systemabsturz erhalten bleiben.
"""

from datetime import datetime
from typing import Any, Dict, List
from .config import Config


class PVDataRepository:
    """
    Diese Klasse kapselt alle SQL-Befehle und verwaltet die SQLite-Verbindung.
    """

    def __init__(self, config: Config = None, db_path: str = None):
        """
        Initialisiert das Repository. Nimmt entweder eine Config oder einen direkten
        Pfad für Tests entgegen (z. B. ':memory:').
        """
        self.config = config or Config()
        self.db_path = db_path or self.config.db_path
        self.initialize_database()

    def initialize_database(self) -> None:
        """
        Erstellt die SQLite-Tabelle, falls diese noch nicht auf der Festplatte existiert.
        Definiert Spalten für Zeitstempel, Erzeugung, Verbrauch und Status.
        """
        # Später wird hier eine Verbindung mit sqlite3 aufgebaut.
        pass

    def save_data_point(self, data: Dict[str, Any]) -> bool:
        """
        Speichert einen bereinigten Datenpunkt dauerhaft in die SQLite-Tabelle.

        Nutzt "INSERT OR REPLACE" (UPSERT), um bei doppelten Zeitstempeln
        den Wert einfach zu aktualisieren, anstatt einen Fehler zu werfen.

        Rückgabewert:
            True, wenn das Speichern erfolgreich war, sonst False.
        """
        return True

    def get_historical_data(
        self, start_time: datetime, end_time: datetime
    ) -> List[Dict[str, Any]]:
        """
        Liest alle historischen Datenpunkte in einem bestimmten Zeitfenster aus.

        Wird vom Dashboard verwendet, um z. B. die Leistungskurve für heute anzuzeigen.

        Rückgabewert:
            Eine Liste von Wörterbüchern (dict), die den SQL-Ergebnissen entsprechen.
        """
        return []
