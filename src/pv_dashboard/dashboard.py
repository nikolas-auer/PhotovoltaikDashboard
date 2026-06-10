"""
Modul für das Web-Interface (Dashboard).

Hier wird die Flask-Webapplikation instanziiert und die Benutzeroberfläche
sowie API-Schnittstellen für das Frontend konfiguriert.
"""

from flask import Flask


def create_app(db_path: str = "pv_metrics.db") -> Flask:
    """
    Erstellt und konfiguriert die Flask-Webanwendung (Application Factory Pattern).

    Dieses Muster erlaubt es, die App flexibel mit verschiedenen Datenbank-Pfaden
    (z. B. einer echten Datei oder einer schnellen In-Memory-Datenbank für Tests) zu starten.

    Argumente:
        db_path: Pfad zur SQLite-Datenbank.

    Rückgabewert:
        Die fertige Flask-Applikationsinstanz.
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        """
        Rendert das HTML-Dashboard im Webbrowser.

        Holt die historischen Daten der Datenbank, lässt die Gesamtenergie über das
        Berechnungsmodul integrieren und stellt die Werte in einem schönen UI dar.
        """
        # Später: Laden der Historie und Rendern einer HTML-Vorlage
        return "<h1>Photovoltaik Dashboard (Gerüst lauffähig)</h1>"

    @app.route("/api/live")
    def api_live_data():
        """
        Ein API-Endpunkt, der den allerneuesten Datenpunkt als JSON liefert.
        Kann von Javascript-Skripten auf der Webseite abgefragt werden (Live-Updates).
        """
        # Später: Abruf des neuesten Werts und JSON-Formatierung
        return {"status": "success", "message": "Stub-API aktiv"}

    return app
