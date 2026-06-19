"""
Modul für das Web-Interface (Dashboard).

Hier wird die Flask-Webapplikation instanziiert und die Benutzeroberfläche
sowie API-Schnittstellen für das Frontend konfiguriert.
"""

from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
from .config import Config
from .storage import PVDataRepository
from .calculation import MetricsCalculator
import logging

logger = logging.getLogger(__name__)


def create_app(config: Config = None, db_path: str = None) -> Flask:
    """
    Erstellt und konfiguriert die Flask-Webanwendung (Application Factory Pattern).

    Dieses Muster erlaubt es, die App flexibel mit verschiedenen Datenbank-Pfaden
    (z. B. einer echten Datei oder einer schnellen In-Memory-Datenbank für Tests) zu starten.
    """
    app = Flask(__name__)

    # Konfiguration laden
    cfg = config or Config()
    repo = PVDataRepository(config=cfg, db_path=db_path)
    calculator = MetricsCalculator()

    @app.route("/")
    def index():
        """
        Rendert das HTML-Dashboard im Webbrowser.

        Holt die historischen Daten der Datenbank, lässt die Gesamtenergie über das
        Berechnungsmodul integrieren und stellt die Werte in einem schönen UI dar.
        """
        now = datetime.now()

        # Startzeitpunkte für Tag (heute 00:00), Monat (1. des Monats 00:00) und Jahr (1. Januar 00:00)
        start_of_today = datetime(now.year, now.month, now.day)
        start_of_month = datetime(now.year, now.month, 1)
        start_of_year = datetime(now.year, 1, 1)

        # Abfragen aus dem Repository
        today_data = repo.get_historical_data(start_of_today, now)
        month_data = repo.get_historical_data(start_of_month, now)
        year_data = repo.get_historical_data(start_of_year, now)

        # 1. Momentanwerte (letzter Datenpunkt)
        latest_point = {}
        if today_data:
            latest_point = today_data[-1]
        else:
            # falls heute noch keine Daten da sind (z.B. nach Mitternacht)
            all_data = repo.get_historical_data(now - timedelta(hours=24), now)
            if all_data:
                latest_point = all_data[-1]

        current_gen = latest_point.get("generation_w", 0.0) if latest_point else 0.0
        current_con = latest_point.get("consumption_w", 0.0) if latest_point else 0.0

        # 2. Tageswerte (Integration über heute)
        daily_gen_wh = calculator.calculate_total_energy(today_data, "generation_w")
        daily_con_wh = calculator.calculate_total_energy(today_data, "consumption_w")
        daily_ratio = calculator.calculate_self_sufficiency_ratio(today_data)

        # 3. Monatswerte (Integration über den Monat)
        monthly_gen_wh = calculator.calculate_total_energy(month_data, "generation_w")
        monthly_con_wh = calculator.calculate_total_energy(month_data, "consumption_w")
        monthly_ratio = calculator.calculate_self_sufficiency_ratio(month_data)

        # 4. Jahreswerte (Integration über das Jahr)
        yearly_gen_wh = calculator.calculate_total_energy(year_data, "generation_w")
        yearly_con_wh = calculator.calculate_total_energy(year_data, "consumption_w")
        yearly_ratio = calculator.calculate_self_sufficiency_ratio(year_data)

        return render_template(
            "index.html",
            current_gen=round(current_gen, 1),
            current_con=round(current_con, 1),
            daily_gen_wh=round(daily_gen_wh, 1),
            daily_con_wh=round(daily_con_wh, 1),
            daily_ratio=round(daily_ratio, 1),
            monthly_gen_wh=round(monthly_gen_wh, 1),
            monthly_con_wh=round(monthly_con_wh, 1),
            monthly_ratio=round(monthly_ratio, 1),
            yearly_gen_wh=round(yearly_gen_wh, 1),
            yearly_con_wh=round(yearly_con_wh, 1),
            yearly_ratio=round(yearly_ratio, 1),
        )

    @app.route("/api/live")
    def api_live_data():
        """
        Ein API-Endpunkt, der den allerneuesten Datenpunkt als JSON liefert.
        Kann von Javascript-Skripten auf der Webseite abgefragt werden (Live-Updates).
        """
        now = datetime.now()
        # Letzte 5 Minuten abfragen
        data = repo.get_historical_data(now - timedelta(minutes=5), now)
        if data:
            latest = data[-1]
        else:
            # Letzte 24 Stunden abfrage
            data = repo.get_historical_data(now - timedelta(hours=24), now)
            latest = (
                data[-1]
                if data
                else {
                    "generation_w": 0.0,
                    "consumption_w": 0.0,
                    "timestamp": now.isoformat(),
                }
            )

        return jsonify(
            {
                "status": "success",
                "timestamp": latest.get("timestamp"),
                "generation_w": round(latest.get("generation_w", 0.0), 1),
                "consumption_w": round(latest.get("consumption_w", 0.0), 1),
            }
        )

    @app.route("/api/historical")
    def api_historical_data():
        """
        Gibt die historischen Daten von heute als JSON zurück,
        inklusive der kumulativen Tageserzeugung in Wh.
        """
        now = datetime.now()
        start_of_today = datetime(now.year, now.month, now.day)
        today_data = repo.get_historical_data(start_of_today, now)

        # Chronologisch sortieren
        today_data_sorted = sorted(today_data, key=lambda x: x["timestamp"])

        chart_data = []
        running_gen_wh = 0.0
        parsed_points = []

        # Parse alle Punkte für die Berechnung
        for p in today_data_sorted:
            try:
                ts = datetime.fromisoformat(p["timestamp"])
                gen = float(p["generation_w"])
                con = float(p["consumption_w"])
                parsed_points.append((ts, gen, con))
            except (ValueError, KeyError, TypeError):
                continue

        # Kumulative Erzeugung berechnen (Trapezregel schrittweise)
        for i in range(len(parsed_points)):
            ts, gen, con = parsed_points[i]
            if i > 0:
                ts_prev, gen_prev, _ = parsed_points[i - 1]
                dt = (ts - ts_prev).total_seconds()
                if dt > 0:
                    dt_hours = dt / 3600.0
                    running_gen_wh += ((gen_prev + gen) / 2.0) * dt_hours

            chart_data.append(
                {
                    "label": ts.strftime("%H:%M:%S"),
                    "generation_w": round(gen, 1),
                    "consumption_w": round(con, 1),
                    "cumulative_gen_wh": round(running_gen_wh, 1),
                }
            )

        return jsonify(chart_data)

    return app
