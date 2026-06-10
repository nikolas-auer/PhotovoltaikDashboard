"""
Modul für die Datenbereinigung (Data Cleaning).

Bevor die vom Server abgeholten Rohdaten in der Datenbank gespeichert werden,
müssen sie überprüft werden. Falsche Datentypen oder extreme Messfehler (Ausreißer)
werden hier korrigiert.
"""

from typing import Any, Dict


class PVDataCleaner:
    """
    Diese Klasse bereinigt und validiert die eingehenden Datenpunkte.
    Sie setzt das Single Responsibility Principle um, indem sie sich nur um Datenqualität kümmert.
    """

    def __init__(self, max_realistic_w: float = 20000.0):
        """
        Initialisiert den Cleaner mit Grenzwerten für unplausible Messdaten.

        Einheit: Watt (W) für die Momentanleistung (entsprechend der PP4-Vorgabe).
        """
        # Werte über 20 kW (20000 W) gelten als Sensorfehler
        self.max_realistic_w = max_realistic_w

    def validate_schema(self, data: Dict[str, Any]) -> bool:
        """
        Prüft, ob der Datenpunkt die richtige JSON-Struktur besitzt.
        Es wird gecheckt, ob Pflichtfelder wie der Zeitstempel und die Leistungsdaten da sind.

        Rückgabewert:
            True, wenn die Struktur korrekt ist.
            False, wenn wichtige Felder fehlen oder falsch formatiert sind.
        """
        # Hier wird später geprüft, ob z.B. das Feld "timestamp" im ISO-Format vorliegt
        # und ob die benötigten Messdaten (pv_generation_w etc.) existieren.
        return True

    def clean_fields(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Bereinigt falsche Werte und Ausreißer im Datenpunkt.

        Regeln:
        1. Negative Leistungswerte (physikalisch unmöglich) werden auf 0.0 W gesetzt.
        2. Werte über dem Limit (max_realistic_w) werden auf das Limit gedrosselt (Clamping).
        3. Falsche Datentypen (z.B. Text anstatt Zahlen) werden in 0.0 W umgewandelt.

        Rückgabewert:
            Ein neues Wörterbuch mit den bereinigten und sicheren Werten.
        """
        # Im Stub-Modus geben wir die Daten unverändert wieder zurück.
        # Später wird hier z. B. eine Kopie erzeugt und bereinigt (Functional Programming / Immutability).
        return data
