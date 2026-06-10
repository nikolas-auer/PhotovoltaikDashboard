"""
Unit-Tests für das server.py Modul.
"""

import unittest
from pv_dashboard.server import PVDataCollector


class TestPVDataCollector(unittest.TestCase):
    """
    Testklasse, die prüft, ob der Datensammler korrekt arbeitet.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert den Sammler.
        """
        self.collector = PVDataCollector()

    def test_fetch_latest_data_structure(self):
        """
        Prüft, ob die Funktion zum Abrufen der Daten existiert und ein
        Dictionary zurückgibt.
        """
        data = self.collector.fetch_latest_data()
        self.assertIsInstance(data, dict)
        # Für das Gerüst (Stub) ist dieser einfache Test erfolgreich
        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    unittest.main()
