"""
Integrationstest für das PhotovoltaikDashboard.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json
from pv_dashboard.config import Config
from pv_dashboard.server import PVDataCollector
from pv_dashboard.cleaning import PVDataCleaner
from pv_dashboard.storage import PVDataRepository
from pv_dashboard.calculation import MetricsCalculator
from pv_dashboard.dashboard import create_app


class TestPVSystemIntegration(unittest.TestCase):
    """
    Integrationstest für das Zusammenspiel aller PV-Dashboard Komponenten:
    API -> Cleaning -> Storage -> Calculation -> Flask Frontend.
    """

    def setUp(self):
        """
        Setzt eine temporäre SQLite-Datenbank und die Test-Umgebung auf.
        """
        import os

        self.db_path = "test_integration.db"
        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

        self.config = Config(
            pv_api_url="https://mock-api.de/data",
            pv_api_key="mock-key",
            db_path=self.db_path,
            max_realistic_w=50000.0,
        )

        # Komponenten initialisieren
        self.collector = PVDataCollector(config=self.config)
        self.cleaner = PVDataCleaner(config=self.config)
        self.repo = PVDataRepository(config=self.config)
        self.calculator = MetricsCalculator()

        # Flask-App mit Test-Repository starten
        self.app = create_app(config=self.config, db_path=self.db_path)
        self.app_client = self.app.test_client()

    def tearDown(self):
        """
        Löscht die temporäre Test-Datenbank.
        """
        import os

        if os.path.exists(self.db_path):
            try:
                os.remove(self.db_path)
            except OSError:
                pass

    @patch("requests.get")
    def test_full_pipeline_flow(self, mock_get):
        """
        Simuliert die gesamte Datenpipeline über alle Stationen hinweg.
        """
        ts_1 = datetime.now() - timedelta(hours=1)
        ts_2 = datetime.now()

        api_payload_1 = {
            "collected_at": ts_1.isoformat(),
            "data": [
                {"path": "pv-anlage", "type": "generation", "value": 10000.0},
                {"path": "einspeisung", "type": "consumption", "value": 5000.0},
            ],
        }
        api_payload_2 = {
            "collected_at": ts_2.isoformat(),
            "data": [
                {"path": "pv-anlage", "type": "generation", "value": 12000.0},
                {"path": "einspeisung", "type": "consumption", "value": 6000.0},
            ],
        }

        # Datenpunkt 1 simulieren (API -> Cleaning -> Storage)
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = api_payload_1
        mock_get.return_value = mock_response

        raw_data_1 = self.collector.fetch_latest_data()
        self.assertDictEqual(raw_data_1, api_payload_1)

        cleaned_data_1 = self.cleaner.clean_fields(raw_data_1)
        self.assertEqual(cleaned_data_1["generation_w"], 10000.0)
        self.assertEqual(cleaned_data_1["consumption_w"], 5000.0)
        self.assertTrue(self.repo.save_data_point(cleaned_data_1))

        # Datenpunkt 2 simulieren (API -> Cleaning -> Storage)
        mock_response.json.return_value = api_payload_2
        raw_data_2 = self.collector.fetch_latest_data()
        cleaned_data_2 = self.cleaner.clean_fields(raw_data_2)
        self.assertTrue(self.repo.save_data_point(cleaned_data_2))

        # Berechnungen auf DB-Daten prüfen
        db_points = self.repo.get_historical_data(
            ts_1 - timedelta(minutes=5), ts_2 + timedelta(minutes=5)
        )
        self.assertEqual(len(db_points), 2)

        # Erwartet (Mittelwert über 1h): Erzeugung = 11 kWh (11000 Wh), Verbrauch = 5.5 kWh (5500 Wh)
        total_gen_wh = self.calculator.calculate_total_energy(db_points, "generation_w")
        total_con_wh = self.calculator.calculate_total_energy(
            db_points, "consumption_w"
        )
        self.assertAlmostEqual(total_gen_wh, 11000.0, places=1)
        self.assertAlmostEqual(total_con_wh, 5500.0, places=1)

        # Autarkiegrad verifizieren (Erwartet: 100% Autarkie)
        ratio = self.calculator.calculate_self_sufficiency_ratio(db_points)
        self.assertEqual(ratio, 100.0)

        # Flask Web-Interface und APIs prüfen
        with patch.object(
            PVDataRepository, "get_historical_data", return_value=db_points
        ):
            # Frontend laden
            response = self.app_client.get("/")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Photovoltaik-Dashboard", response.data)

            # Live-API prüfen
            api_live = self.app_client.get("/api/live")
            self.assertEqual(api_live.status_code, 200)
            live_json = json.loads(api_live.data)
            self.assertEqual(live_json["generation_w"], 12000.0)
            self.assertEqual(live_json["consumption_w"], 6000.0)

            # Verlauf-API prüfen
            api_historical = self.app_client.get("/api/historical")
            self.assertEqual(api_historical.status_code, 200)
            hist_json = json.loads(api_historical.data)
            self.assertEqual(len(hist_json), 2)
            self.assertEqual(hist_json[1]["cumulative_gen_wh"], 11000.0)


if __name__ == "__main__":
    unittest.main()
