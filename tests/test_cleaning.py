"""
Unit-Tests für das cleaning.py Modul.
"""

import unittest
from pv_dashboard.cleaning import PVDataCleaner
from pv_dashboard.config import Config


class TestPVDataCleaner(unittest.TestCase):
    """
    Testklasse für die Datenbereinigungs- und Validierungsfunktionen.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert den Cleaner mit config.
        """
        self.config = Config(max_realistic_w=1000.0)
        self.cleaner = PVDataCleaner(config=self.config)

        self.valid_payload = {
            "collected_at": "2026-06-15T12:00:00+02:00",
            "data": [
                {"path": "device1", "type": "generation", "value": 150.0},
                {"path": "device2", "type": "generation", "value": 50.0},
                {"path": "device3", "type": "consumption", "value": 200.0},
            ],
            "age_seconds": 1.5,
        }

    def test_validate_schema_valid(self):
        """
        Prüft, ob ein gültiges JSON-Schema erfolgreich validiert wird.
        """
        self.assertTrue(self.cleaner.validate_schema(self.valid_payload))

    def test_validate_schema_invalid(self):
        """
        Prüft, ob unvollständige oder fehlerhafte Daten erkannt werden.
        """
        # Fehlendes collected_at
        self.assertFalse(self.cleaner.validate_schema({"data": []}))
        # Falscher Datentyp für data
        self.assertFalse(
            self.cleaner.validate_schema(
                {"collected_at": "2026-06-15T12:00:00", "data": "string"}
            )
        )
        # Falscher Datentyp für Typen in data
        self.assertFalse(
            self.cleaner.validate_schema(
                {
                    "collected_at": "2026-06-15T12:00:00",
                    "data": [{"type": "wrong_type", "value": 10.0}],
                }
            )
        )

    def test_clean_fields_aggregation_and_rules(self):
        """
        Prüft, ob Datenwerte korrekt bereinigt, gedrosselt und aggregiert werden.
        """
        dirty_payload = {
            "collected_at": "2026-06-15T12:00:00+02:00",
            "data": [
                {
                    "path": "pv1",
                    "type": "generation",
                    "value": -50.0,
                },  # Negativ -> wird 0
                {
                    "path": "pv2",
                    "type": "generation",
                    "value": 1500.0,
                },  # Über Limit (1000) -> wird 1000
                {"path": "con1", "type": "consumption", "value": 300.0},  # Normal
                {
                    "path": "con2",
                    "type": "consumption",
                    "value": "invalid",
                },  # Falscher Typ -> wird 0.0
            ],
        }

        cleaned = self.cleaner.clean_fields(dirty_payload)
        self.assertIsInstance(cleaned, dict)
        self.assertEqual(cleaned["timestamp"], "2026-06-15T12:00:00+02:00")

        # Generation: 0.0 (von -50) + 1000.0 (gedrosselt von 1500) = 1000.0
        self.assertEqual(cleaned["generation_w"], 1000.0)

        # Consumption: 300.0 + 0.0 (von "invalid") = 300.0
        self.assertEqual(cleaned["consumption_w"], 300.0)


if __name__ == "__main__":
    unittest.main()
