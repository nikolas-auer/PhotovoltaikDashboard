.PHONY: install test run help

install:         ## Installiert die Bibliotheken aus requirements.txt
	pip install -r requirements.txt

test:            ## Führt die Tests aus
	PYTHONPATH=src python3 -m unittest discover -v -s tests

run:             ## Startet das System (Hintergrund-Scraper + Flask-Server)
	PYTHONPATH=src python3 main.py

help:            ## Zeigt diese Hilfe an
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
