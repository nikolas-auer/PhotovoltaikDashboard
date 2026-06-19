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
from pv_dashboard.server import PVDataCollector
from pv_dashboard.cleaning import PVDataCleaner
from pv_dashboard.storage import PVDataRepository

# Konfiguration des Loggings (Ausgabe von Systemmeldungen auf dem Bildschirm / im Terminal)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s"
)
logger = logging.getLogger(__name__)


def background_scraper_loop(config: Config):
    """
    Diese Funktion läuft kontinuierlich in einem eigenen Hintergrund-Thread.
    Sie fragt alle X Sekunden den Server ab, bereinigt die Daten und speichert sie.
    """
    logger.info("Hintergrund-Scraper-Loop wurde gestartet...")

    collector = PVDataCollector(config=config)
    cleaner = PVDataCleaner(config=config)
    repo = PVDataRepository(config=config)

    while True:
        try:
            logger.info("Rufe aktuellen Datenpunkt von API ab...")
            raw_data = collector.fetch_latest_data()
            if raw_data:
                cleaned_data = cleaner.clean_fields(raw_data)
                if cleaned_data:
                    success = repo.save_data_point(cleaned_data)
                    if success:
                        logger.info(
                            f"Datenpunkt gespeichert: Erzeugung={cleaned_data['generation_w']}W, Verbrauch={cleaned_data['consumption_w']}W"
                        )
                    else:
                        logger.warning("Speichern des Datenpunkts fehlgeschlagen.")
                else:
                    logger.warning(
                        "Datenpunkt-Bereinigung ergab ungültige Daten (Schemafehler oder Ausreißer)."
                    )
            else:
                logger.warning("Keine Rohdaten vom Server empfangen.")
        except Exception as e:
            logger.error(f"Unerwarteter Fehler im Scraper-Thread: {e}")

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
