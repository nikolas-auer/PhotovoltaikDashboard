"""
main.py für das PhotovoltaikDashboard.

Dieses Skript koordiniert das gesamte System:
1. Es startet einen Hintergrundthread für den Daten-Scraper.
2. Es startet den Flask-Webserver im Hauptthread.
"""

import logging
import time
from threading import Thread
from pv_dashboard import Config
from pv_dashboard.dashboard import create_app

# Konfiguration des Loggings (Ausgabe von Systemmeldungen auf dem Bildschirm / im Terminal)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


def background_scraper_loop(config: Config):
    """
    Diese Funktion läuft kontinuierlich in einem eigenen Hintergrund-Thread.
    Sie fragt alle X Sekunden den Server ab (Intervall aus Config).
    """
    logger.info("Hintergrund-Scraper-Loop wurde gestartet...")

    while True:
        logger.info("Simuliere: Abfrage des nächsten Datenpunkts...")
        time.sleep(config.scraping_interval_seconds)


def main():
    """
    Hauptfunktion zum Starten des Systems.
    """
    logger.info("Photovoltaik-Dashboard System wird gestartet...")
    config = Config()

    # 1. Starten des Scraper-Threads im Hintergrund (daemon=True sorgt dafür,
    #    dass der Thread beendet wird, wenn das Hauptprogramm beendet wird)
    scraper_thread = Thread(target=background_scraper_loop, args=(config,), daemon=True)
    scraper_thread.start()

    # 2. Erstellen und Starten des Flask-Webservers
    app = create_app(config=config)
    logger.info("Flask Webserver startet. Öffne http://localhost:5000 im Browser.")

    # Startet den Server (lokal erreichbar auf Port 5000)
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
