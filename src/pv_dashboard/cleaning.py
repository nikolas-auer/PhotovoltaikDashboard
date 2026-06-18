"""
Modul für die Datenbereinigung (Data Cleaning).

Bevor die vom Server abgeholten Rohdaten in der Datenbank gespeichert werden,
müssen sie überprüft werden. Falsche Datentypen oder extreme Messfehler (Ausreißer)
werden hier korrigiert.
"""

from typing import Any, Dict
from .config import Config


class PVDataCleaner:
    """
    Diese Klasse bereinigt und validiert die eingehenden Datenpunkte.
    Sie setzt das Single Responsibility Principle um, indem sie sich nur um Datenqualität kümmert.
    """

    def __init__(self, config: Config = None):
        """
        Initialisiert den Cleaner mit Grenzwerten aus der API-Konfiguration.
        """
        self.config = config or Config()

    def validate_schema(self, data: Dict[str, Any]) -> bool:
        """
        Prüft, ob der Datenpunkt die richtige JSON-Struktur besitzt.
        Es wird gecheckt, ob Pflichtfelder wie der Zeitstempel und die Leistungsdaten da sind.

        Rückgabewert:
            True, wenn die Struktur korrekt ist.
            False, wenn wichtige Felder fehlen oder falsch formatiert sind.
        """
        if not isinstance(data, dict):
            return False
        if "collected_at" not in data or "data" not in data:
            return False
        if not isinstance(data["data"], list):
            return False

        # Zeitstempel-Format prüfen
        from datetime import datetime

        try:
            datetime.fromisoformat(data["collected_at"])
        except (ValueError, TypeError):
            return False

        for item in data["data"]:
            if not isinstance(item, dict):
                return False
            if "type" not in item or "value" not in item:
                return False
            if item["type"] not in ("generation", "consumption"):
                return False
        return True

    def clean_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bereinigt falsche Werte und Ausreißer im Datenpunkt.

        Regeln:
        1. Negative Leistungswerte werden auf 0.0 W gesetzt.
        2. Werte über dem Limit (max_realistic_w) werden auf das Limit gedrosselt.
        3. Falsche Datentypen werden in 0.0 W umgewandelt.

        Rückgabewert:
            Ein neues Wörterbuch mit den bereinigten und aggregierten Werten:
            {
                "timestamp": str,
                "generation_w": float,
                "consumption_w": float
            }
            Bei ungültigem Schema wird ein leeres Dictionary zurückgegeben.
        """
        if not self.validate_schema(data):
            return {}

        timestamp = data["collected_at"]
        total_generation = 0.0
        total_consumption = 0.0

        for item in data["data"]:
            val = item["value"]
            # Falsche Datentypen umwandeln
            try:
                val = float(val)
            except (ValueError, TypeError):
                val = 0.0

            # 1. Negative Leistungswerte werden auf 0.0 W gesetzt
            if val < 0.0:
                val = 0.0
            # 2. Werte über dem Limit werden gedrosselt
            elif val > self.config.max_realistic_w:
                val = self.config.max_realistic_w

            if item["type"] == "generation":
                total_generation += val
            elif item["type"] == "consumption":
                total_consumption += val

        return {
            "timestamp": timestamp,
            "generation_w": total_generation,
            "consumption_w": total_consumption,
        }
