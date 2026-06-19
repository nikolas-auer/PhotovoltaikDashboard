"""
Unit-Tests für das calculation.py Modul.
"""

import unittest
from datetime import datetime, timedelta
from pv_dashboard.calculation import MetricsCalculator


class TestMetricsCalculator(unittest.TestCase):
    """
    Testklasse zur Absicherung der mathematischen Berechnungen.
    """

    def setUp(self):
        """
        Wird vor jedem Test ausgeführt. Initialisiert den Berechner.
        """
        self.calculator = MetricsCalculator()

    def test_calculate_total_energy_constant(self):
        """
        Prüft, ob ein konstanter Wert über 1 Stunde korrekt zu 1000 Wh integriert wird.
        """
        base_time = datetime(2026, 6, 15, 12, 0, 0)
        data = [
            {"timestamp": base_time.isoformat(), "generation_w": 1000.0},
            {
                "timestamp": (base_time + timedelta(hours=1)).isoformat(),
                "generation_w": 1000.0,
            },
        ]
        result = self.calculator.calculate_total_energy(data, "generation_w")
        self.assertEqual(result, 1000.0)

    def test_calculate_total_energy_ramp(self):
        """
        Prüft die Trapezregel bei linear steigender Erzeugung.
        Erzeugung steigt in 2 Stunden von 0 W auf 1000 W an.
        Mittelwert = 500 W, Dauer = 2 h -> Energie = 1000 Wh.
        """
        base_time = datetime(2026, 6, 15, 12, 0, 0)
        data = [
            {"timestamp": base_time.isoformat(), "generation_w": 0.0},
            {
                "timestamp": (base_time + timedelta(hours=2)).isoformat(),
                "generation_w": 1000.0,
            },
        ]
        result = self.calculator.calculate_total_energy(data, "generation_w")
        self.assertEqual(result, 1000.0)

    def test_update_running_stats_welford(self):
        """
        Prüft, ob der Welford-Algorithmus schrittweise Mittelwert und Varianz korrekt berechnet.
        Für Werte [10.0, 20.0, 30.0]:
        Mittelwert = 20.0, Stichprobenvarianz (Schnitt durch N-1) = 100.0.
        """
        self.calculator.update_running_stats(10.0)
        self.calculator.update_running_stats(20.0)
        mean, var = self.calculator.update_running_stats(30.0)

        self.assertEqual(mean, 20.0)
        self.assertEqual(var, 100.0)

    def test_calculate_self_sufficiency_ratio(self):
        """
        Prüft die Berechnung des Verhältnisses von Verbrauch aus PV zu Gesamtverbrauch.
        Szenario: 1 Stunde lang konstant 1000 W erzeugt und 2000 W verbraucht.
        -> Genutzte PV-Energie = 1000 Wh, Gesamtverbrauch = 2000 Wh -> 50% Autarkie.
        """
        base_time = datetime(2026, 6, 15, 12, 0, 0)
        data = [
            {
                "timestamp": base_time.isoformat(),
                "generation_w": 1000.0,
                "consumption_w": 2000.0,
            },
            {
                "timestamp": (base_time + timedelta(hours=1)).isoformat(),
                "generation_w": 1000.0,
                "consumption_w": 2000.0,
            },
        ]

        ratio = self.calculator.calculate_self_sufficiency_ratio(data)
        self.assertEqual(ratio, 50.0)


if __name__ == "__main__":
    unittest.main()
