"""
Unit-Tests für das server.py Modul.
"""

import unittest
from unittest.mock import patch, MagicMock
import requests
from pv_dashboard.server import PVDataCollector
from pv_dashboard.config import Config


class TestPVDataCollector(unittest.TestCase):
    """
    Testklasse, die prüft, ob der Datensammler korrekt arbeitet.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert den Sammler mit Config.
        """
        self.config = Config(
            pv_api_url="https://mock-pv-server.de/api", pv_api_key="mock-key"
        )
        self.collector = PVDataCollector(config=self.config)

    @patch("requests.get")
    def test_fetch_latest_data_success(self, mock_get):
        """
        Prüft, ob fetch_latest_data bei einem erfolgreichen API-Aufruf die korrekten Daten zurückgibt.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "collected_at": "2026-06-15T12:00:00+02:00",
            "data": [
                {"path": "device1", "type": "generation", "value": 120.5},
                {"path": "device2", "type": "consumption", "value": 80.0},
            ],
        }
        mock_get.return_value = mock_response

        data = self.collector.fetch_latest_data()
        self.assertIsInstance(data, dict)
        self.assertEqual(data["collected_at"], "2026-06-15T12:00:00+02:00")
        self.assertEqual(len(data["data"]), 2)
        mock_get.assert_called_once_with(
            "https://mock-pv-server.de/api",
            headers={"X-API-Key": "mock-key"},
            timeout=5.0,
            verify=False,
        )

    @patch("requests.get")
    def test_fetch_latest_data_failure(self, mock_get):
        """
        Prüft, ob fetch_latest_data bei einem HTTP-Fehler ein leeres Dictionary zurückgibt, ohne abzustürzen.
        """
        mock_get.side_effect = requests.exceptions.HTTPError("Mocked HTTP Error")

        data = self.collector.fetch_latest_data()
        self.assertIsInstance(data, dict)
        self.assertEqual(len(data), 0)


if __name__ == "__main__":
    unittest.main()
