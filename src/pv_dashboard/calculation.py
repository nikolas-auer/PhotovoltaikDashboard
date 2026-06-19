"""
Modul für mathematische Berechnungen (KPI Computation).

Dieses Modul übernimmt die Berechnung aller Kennzahlen und Analysen. Es berechnet
das Integral (Gesamtenergie) aus den einzelnen Datenpunkten und führt laufende Statistiken.
"""

from typing import Any, Dict, List, Tuple


class MetricsCalculator:
    """
    Diese Klasse berechnet die mathematischen Kennzahlen.
    """

    def __init__(self):
        """
        Initialisiert den Rechner und setzt die Statistik-Zwischenspeicher zurück.
        """
        self.reset_running_stats()

    def reset_running_stats(self) -> None:
        """
        Setzt alle Variablen für die schrittweise Mittelwertberechnung zurück.
        """
        # Anzahl der Datenpunkte
        self.n = 0
        # Laufender Mittelwert
        self.running_mean = 0.0
        # Hilfsvariable für die Varianz nach Welfords Algorithmus
        self.running_m2 = 0.0

    def calculate_total_energy(
        self, data_points: List[Dict[str, Any]], metric_key: str = "generation_w"
    ) -> float:
        """
        Berechnet das Integral über die Momentanwerte (Leistung in W),
        um die Gesamtenergiearbeit in Wattstunden (Wh) zu erhalten.

        Dazu wird die mathematische Trapezregel angewendet. Diese ist besonders
        robust, da sie unregelmäßige Zeitabstände (dt) zwischen den Messpunkten
        (z. B. durch Latenz) exakt berücksichtigt.

        Argumente:
            data_points: Eine chronologische Liste von Datenpunkten.
            metric_key: Welches Feld aufsummiert werden soll (z. B. generation_w oder consumption_w).

        Rückgabewert:
            Die aufsummierte Energiearbeit in Wattstunden (Wh) als float.
        """
        if not data_points or len(data_points) < 2:
            return 0.0

        from datetime import datetime

        # Daten parsen und chronologisch sortieren
        parsed_points = []
        for p in data_points:
            try:
                ts = datetime.fromisoformat(p["timestamp"])
                val = float(p[metric_key])
                parsed_points.append((ts, val))
            except (ValueError, KeyError, TypeError):
                continue

        parsed_points.sort(key=lambda x: x[0])

        if len(parsed_points) < 2:
            return 0.0

        total_energy = 0.0
        for i in range(len(parsed_points) - 1):
            t1, p1 = parsed_points[i]
            t2, p2 = parsed_points[i + 1]
            dt = (t2 - t1).total_seconds()
            if dt > 0:
                dt_hours = dt / 3600.0
                interval_energy = ((p1 + p2) / 2.0) * dt_hours
                total_energy += interval_energy

        return total_energy

    def update_running_stats(self, new_value: float) -> Tuple[float, float]:
        """
        Aktualisiert den laufenden Mittelwert und die Varianz mit Welfords Algorithmus.

        Dieser Algorithmus berechnet die Werte schrittweise mit jedem neuen Datenpunkt.
        Vorteil: Es müssen nicht alle Millionen Datenpunkte eines Jahres im Arbeitsspeicher
        gehalten werden (Speicherschonung, O(1)-Komplexität und vermeiden von Rundungsfehlern).

        Argumente:
            new_value: Der neue, bereinigte Leistungswert (in W).

        Rückgabewert:
            Ein Tupel (laufender_mittelwert, laufende_varianz).
        """
        self.n += 1
        delta = new_value - self.running_mean
        self.running_mean += delta / self.n
        delta2 = new_value - self.running_mean
        self.running_m2 += delta * delta2

        variance = 0.0
        if self.n > 1:
            variance = self.running_m2 / (self.n - 1)

        return self.running_mean, variance

    def calculate_self_sufficiency_ratio(
        self, data_points: List[Dict[str, Any]]
    ) -> float:
        """
        Berechnet das Verhältnis vom Verbrauch aus PV zum Gesamtverbrauch

        Formel: (Integral über min(PV-Erzeugung, Verbrauch) dt) / (Integral über Verbrauch dt) * 100

        Argumente:
            data_points: Eine chronologische Liste von Datenpunkten.

        Rückgabewert:
            Prozentwert zwischen 0.0 und 100.0 als float.
        """
        if not data_points or len(data_points) < 2:
            return 0.0

        from datetime import datetime

        # Daten parsen (Datenbank-Strings in Python-Objekte umwandeln) und chronologisch sortieren
        parsed_points = []
        for p in data_points:
            try:
                ts = datetime.fromisoformat(p["timestamp"])
                gen = float(p["generation_w"])
                con = float(p["consumption_w"])
                parsed_points.append((ts, gen, con))
            except (ValueError, KeyError, TypeError):
                continue

        parsed_points.sort(key=lambda x: x[0])

        if len(parsed_points) < 2:
            return 0.0

        total_consumption_energy = 0.0
        pv_used_energy = 0.0

        for i in range(len(parsed_points) - 1):
            t1, gen1, con1 = parsed_points[i]
            t2, gen2, con2 = parsed_points[i + 1]
            dt = (t2 - t1).total_seconds()
            if dt > 0:
                dt_hours = dt / 3600.0

                # Trapezregel für Gesamtverbrauch
                avg_con = (con1 + con2) / 2.0
                total_consumption_energy += avg_con * dt_hours

                # Trapezregel für genutzt PV-Energie (min(generation, consumption))
                pv1 = min(gen1, con1)
                pv2 = min(gen2, con2)
                avg_pv_used = (pv1 + pv2) / 2.0
                pv_used_energy += avg_pv_used * dt_hours

        if total_consumption_energy == 0.0:
            return 0.0

        return min((pv_used_energy / total_consumption_energy) * 100.0, 100.0)
