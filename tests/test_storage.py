"""
Unit-Tests für das storage.py Modul.
"""

import unittest
from datetime import datetime, timedelta
from pv_dashboard.storage import PVDataRepository
from pv_dashboard.config import Config


class TestPVDataRepository(unittest.TestCase):
    """
    Testklasse zur Verifizierung des Datenbankzugriffs.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt.
        Nutzt eine temporäre SQLite-Datei für Tests.
        """
        import os

        self.db_path = "test_storage.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass
        self.config = Config(db_path=self.db_path)
        self.repo = PVDataRepository(config=self.config)

    def tearDown(self):
        """
        Wird nach jedem Test ausgeführt. Löscht die temporäre Datenbankdatei.
        """
        import os

        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    def test_save_and_retrieve_data_point(self):
        """
        Prüft, ob ein Datenpunkt erfolgreich gespeichert und wieder ausgelesen werden kann.
        """
        now = datetime.now()
        test_data = {
            "timestamp": now.isoformat(),
            "generation_w": 150.0,
            "consumption_w": 200.0,
        }

        # Speichern
        self.assertTrue(self.repo.save_data_point(test_data))

        # Abrufen
        start_time = now - timedelta(seconds=1)
        end_time = now + timedelta(seconds=1)
        retrieved = self.repo.get_historical_data(start_time, end_time)

        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0]["generation_w"], 150.0)
        self.assertEqual(retrieved[0]["consumption_w"], 200.0)

    def test_upsert_behavior(self):
        """
        Prüft, ob bei doppeltem Zeitstempel der Datensatz aktualisiert statt verdoppelt wird (UPSERT).
        """
        ts_str = "2026-06-15T12:00:00+02:00"
        ts_dt = datetime.fromisoformat(ts_str)

        data_1 = {"timestamp": ts_str, "generation_w": 100.0, "consumption_w": 50.0}
        data_2 = {"timestamp": ts_str, "generation_w": 120.0, "consumption_w": 60.0}

        self.assertTrue(self.repo.save_data_point(data_1))
        self.assertTrue(self.repo.save_data_point(data_2))

        retrieved = self.repo.get_historical_data(
            ts_dt - timedelta(seconds=1), ts_dt + timedelta(seconds=1)
        )

        # Es darf nur 1 Zeile existieren und diese muss die neueren Werte von data_2 besitzen
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0]["generation_w"], 120.0)
        self.assertEqual(retrieved[0]["consumption_w"], 60.0)

    def test_get_historical_data_filtering(self):
        """
        Prüft, ob get_historical_data korrekt nach Start- und Endzeitpunkt filtert.
        """
        base_time = datetime(2026, 6, 15, 12, 0, 0)

        # Drei Datenpunkte im Abstand von 1 Stunde speichern
        for i in range(3):
            ts = base_time + timedelta(hours=i)
            self.repo.save_data_point(
                {
                    "timestamp": ts.isoformat(),
                    "generation_w": 100.0 * i,
                    "consumption_w": 100.0 * i,
                }
            )

        # Abfrage schränkt auf den mittleren Datenpunkt ein
        start = base_time + timedelta(minutes=30)
        end = base_time + timedelta(hours=1, minutes=30)
        retrieved = self.repo.get_historical_data(start, end)

        self.assertEqual(len(retrieved), 1)
        # Muss der zweite Punkt sein (index i=1)
        self.assertEqual(retrieved[0]["generation_w"], 100.0)


if __name__ == "__main__":
    unittest.main()
