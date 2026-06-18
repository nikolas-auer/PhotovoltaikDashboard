"""
Modul für die Datenspeicherung (Data Storage).

Dieses Modul verwaltet die lokale Speicherung unserer Messwerte in einer SQLite-Datenbank.
Es stellt sicher, dass historische Daten auch nach einem Systemabsturz erhalten bleiben.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List
from .config import Config

logger = logging.getLogger(__name__)


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
        Definiert Spalten für Zeitstempel, Erzeugung und Verbrauch.
        """
        import sqlite3

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS pv_data (
                        timestamp TEXT PRIMARY KEY,
                        generation_w REAL NOT NULL,
                        consumption_w REAL NOT NULL
                    )
                """)
                conn.commit()
            logger.info(f"SQLite Datenbank initialisiert unter: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Fehler bei der Datenbank-Initialisierung: {e}")

    def save_data_point(self, data: Dict[str, Any]) -> bool:
        """
        Speichert einen bereinigten Datenpunkt dauerhaft in die SQLite-Tabelle.

        Nutzt "INSERT OR REPLACE" (UPSERT), um bei doppelten Zeitstempeln
        den Wert einfach zu aktualisieren, anstatt einen Fehler zu werfen.

        Rückgabewert:
            True, wenn das Speichern erfolgreich war, sonst False.
        """
        import sqlite3

        if (
            not data
            or "timestamp" not in data
            or "generation_w" not in data
            or "consumption_w" not in data
        ):
            logger.warning("Ungültiger Datenpunkt zum Speichern übergeben.")
            return False

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO pv_data (timestamp, generation_w, consumption_w)
                    VALUES (?, ?, ?)
                """,
                    (data["timestamp"], data["generation_w"], data["consumption_w"]),
                )
                conn.commit()
            logger.debug(f"Datenpunkt für {data['timestamp']} erfolgreich gespeichert.")
            return True
        except sqlite3.Error as e:
            logger.error(f"Fehler beim Speichern des Datenpunkts: {e}")
            return False

    def get_historical_data(
        self, start_time: datetime, end_time: datetime
    ) -> List[Dict[str, Any]]:
        """
        Liest alle historischen Datenpunkte in einem bestimmten Zeitfenster aus.

        Wird vom Dashboard verwendet, um z. B. die Leistungskurve für heute anzuzeigen.

        Rückgabewert:
            Eine Liste von Wörterbüchern (dict), die den SQL-Ergebnissen entsprechen.
        """
        import sqlite3

        start_str = start_time.isoformat()
        end_str = end_time.isoformat()
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT timestamp, generation_w, consumption_w
                    FROM pv_data
                    WHERE timestamp >= ? AND timestamp <= ?
                    ORDER BY timestamp ASC
                """,
                    (start_str, end_str),
                )
                rows = cursor.fetchall()

                result = []
                for row in rows:
                    result.append(
                        {
                            "timestamp": row["timestamp"],
                            "generation_w": row["generation_w"],
                            "consumption_w": row["consumption_w"],
                        }
                    )
                return result
        except sqlite3.Error as e:
            logger.error(f"Fehler beim Abrufen historischer Daten: {e}")
            return []
