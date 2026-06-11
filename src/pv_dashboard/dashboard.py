"""
Modul für das Web-Interface (Dashboard).

Hier wird die Flask-Webapplikation instanziiert und die Benutzeroberfläche
sowie API-Schnittstellen für das Frontend konfiguriert.
"""

from flask import Flask
from .config import Config


def create_app(config: Config = None, db_path: str = None) -> Flask:
    """
    Erstellt und konfiguriert die Flask-Webanwendung (Application Factory Pattern).

    Dieses Muster erlaubt es, die App flexibel mit verschiedenen Datenbank-Pfaden
    (z. B. einer echten Datei oder einer schnellen In-Memory-Datenbank für Tests) zu starten.
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        """
        Rendert das HTML-Dashboard im Webbrowser.

        Holt die historischen Daten der Datenbank, lässt die Gesamtenergie über das
        Berechnungsmodul integrieren und stellt die Werte in einem schönen UI dar.
        """
        return "<h1>Photovoltaik Dashboard (Gerüst lauffähig)</h1>"

    @app.route("/api/live")
    def api_live_data():
        """
        Ein API-Endpunkt, der den allerneuesten Datenpunkt als JSON liefert.
        Kann von Javascript-Skripten auf der Webseite abgefragt werden (Live-Updates).
        """
        return {"status": "success", "message": "Stub-API aktiv"}

    return app
