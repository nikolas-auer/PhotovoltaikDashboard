"""
Unit-Tests für das storage.py Modul.
"""

import unittest
from pv_dashboard.storage import PVDataRepository


class TestPVDataRepository(unittest.TestCase):
    """
    Testklasse zur Verifizierung des Datenbankzugriffs.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt.
        Nutzt ":memory:", um die Datenbank rein im Arbeitsspeicher (RAM) aufzubauen.
        Dadurch werden keine temporären Testdateien auf der Festplatte abgelegt.
        """
        self.repo = PVDataRepository(db_path=":memory:")

    def test_save_data_point_stub(self):
        """
        Prüft, ob das Speichern-Gerüst aufgerufen werden kann und standardmäßig True liefert.
        """
        test_data = {}
        result = self.repo.save_data_point(test_data)
        self.assertTrue(result)

    def test_get_historical_data_stub(self):
        """
        Prüft, ob die Abfrage-Funktion aufgerufen werden kann und eine Liste zurückliefert.
        """
        from datetime import datetime

        now = datetime.now()
        data = self.repo.get_historical_data(now, now)
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
