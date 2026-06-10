"""
Modul für die Datenspeicherung (Data Storage).

Dieses Modul verwaltet die lokale Speicherung unserer Messwerte in einer SQLite-Datenbank.
Es stellt sicher, dass historische Daten auch nach einem Systemabsturz erhalten bleiben.
"""

from datetime import datetime
from typing import Any, Dict, List


class PVDataRepository:
    """
    Diese Klasse kapselt alle SQL-Befehle und verwaltet die SQLite-Verbindung.
    """

    def __init__(self, db_path: str = "pv_metrics.db"):
        """
        Initialisiert das Repository und den Pfad zur Datenbankdatei.
        Ruft direkt die Initialisierung der Tabellen auf.
        """
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self) -> None:
        """
        Erstellt die SQLite-Tabelle, falls diese noch nicht auf der Festplatte existiert.
        Definiert Spalten für Zeitstempel, Erzeugung, Verbrauch und Status.
        """
        # Später wird hier eine Verbindung mit sqlite3 aufgebaut
        # und ein SQL-Befehl wie "CREATE TABLE IF NOT EXISTS pv_metrics..." ausgeführt.
        pass

    def save_data_point(self, data: Dict[str, Any]) -> bool:
        """
        Speichert einen bereinigten Datenpunkt dauerhaft in die SQLite-Tabelle.

        Nutzt "INSERT OR REPLACE" (UPSERT), um bei doppelten Zeitstempeln
        den Wert einfach zu aktualisieren, anstatt einen Fehler zu werfen.

        Rückgabewert:
            True, wenn das Speichern erfolgreich war, sonst False.
        """
        # Hier wird der SQL-Insert-Befehl vorbereitet und ausgeführt.
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
        # Hier wird ein SELECT-Befehl mit Zeitfiltern (WHERE timestamp >= ?) ausgeführt.
        return []
