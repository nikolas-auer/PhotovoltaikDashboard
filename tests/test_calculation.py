"""
Unit-Tests für das calculation.py Modul.
"""

import unittest
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

    def test_calculate_total_energy_returns_float(self):
        """
        Prüft, ob die Funktion zur Integralberechnung eine Fließkommazahl (float) zurückgibt.
        """
        result = self.calculator.calculate_total_energy([])
        self.assertIsInstance(result, float)
        self.assertEqual(result, 0.0)

    def test_update_running_stats_returns_tuple(self):
        """
        Prüft, ob die Welford-Funktion ein Paar (Mittelwert, Varianz) als Tupel zurückliefert.
        """
        result = self.calculator.update_running_stats(100.0)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
