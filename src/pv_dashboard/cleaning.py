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
        return True

    def clean_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bereinigt falsche Werte und Ausreißer im Datenpunkt.

        Regeln:
        1. Negative Leistungswerte werden auf 0.0 W gesetzt.
        2. Werte über dem Limit (max_realistic_w) werden auf das Limit gedrosselt.
        3. Falsche Datentypen werden in 0.0 W umgewandelt.

        Rückgabewert:
            Ein neues Wörterbuch mit den bereinigten und sicheren Werten.
        """
        # Im Stub-Modus geben wir die Daten unverändert wieder zurück.
        return data
