"""
Unit-Tests für das cleaning.py Modul.
"""

import unittest
from pv_dashboard.cleaning import PVDataCleaner


class TestPVDataCleaner(unittest.TestCase):
    """
    Testklasse für die Datenbereinigungs- und Validierungsfunktionen.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert den Cleaner.
        """
        self.cleaner = PVDataCleaner()

    def test_validate_schema_returns_boolean(self):
        """
        Prüft, ob die Schema-Validierungsfunktion einen Wahrheitswert (bool) liefert.
        """
        test_payload = {}
        result = self.cleaner.validate_schema(test_payload)
        self.assertIsInstance(result, bool)

    def test_clean_fields_returns_dictionary(self):
        """
        Prüft, ob die Bereinigungsfunktion die Struktur als Wörterbuch zurückgibt.
        """
        test_payload = {}
        cleaned = self.cleaner.clean_fields(test_payload)
        self.assertIsInstance(cleaned, dict)


if __name__ == "__main__":
    unittest.main()
