"""
main.py für das PhotovoltaikDashboard.

Dieses Skript koordiniert das gesamte System:
1. Es startet einen Hintergrundthread für den Daten-Scraper.
2. Es startet den Flask-Webserver im Hauptthread.
"""

import logging
import time
from threading import Thread
from pv_dashboard.dashboard import create_app

# Konfiguration des Loggings (Ausgabe von Systemmeldungen auf dem Bildschirm / im Terminal)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)

# Der Pfad zur SQLite-Datenbankdatei, wenn doch CSV: pv_metrics.csv
DATABASE_FILE = "pv_metrics.db"


def background_scraper_loop():
    """
    Diese Funktion läuft kontinuierlich in einem eigenen Hintergrund-Thread.
    Sie fragt alle 5 Sekunden den Server, vcn dem die Daten sind, ab.
    """
    logger.info("Hintergrund-Scraper-Loop wurde gestartet...")

    # Hier läuft später die Endlosschleife zur regelmäßigen Datenabfrage

    while True:
        logger.info("Simuliere: Abfrage des nächsten 5-Sekunden-Datenpunkts...")
        time.sleep(5.0)


def main():
    """
    Hauptfunktion zum Starten des Systems.
    """
    logger.info("Photovoltaik-Dashboard System wird gestartet...")

    # 1. Starten des Scraper-Threads im Hintergrund (daemon=True sorgt dafür,
    #    dass der Thread beendet wird, wenn das Hauptprogramm beendet wird)
    scraper_thread = Thread(target=background_scraper_loop, daemon=True)
    scraper_thread.start()

    # 2. Erstellen und Starten des Flask-Webservers
    app = create_app(db_path=DATABASE_FILE)
    logger.info("Flask Webserver startet. Öffne http://localhost:5000 im Browser.")

    # Startet den Server (lokal erreichbar auf Port 5000)
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
