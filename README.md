# PhotovoltaikDashboard

Ein modulares Python-System zur Echtzeit-Erfassung, Bereinigung, Speicherung und mathematischen Analyse von Photovoltaik-Erzeugungsdaten und Stromverbräuchen.

Die Anwendung ist als leichtgewichtiges, containerisiertes System konzipiert, das im Hintergrund kontinuierlich Leistungsdaten von einer Sensor-API abfragt, validiert und persistiert, während ein interaktives Flask-Webinterface die historischen und aktuellen Metriken visualisiert.

Dieses Projekt wurde als Einzelarbeit von Nikolas Auer durchgeführt. Alle Phasen der Entwicklung wurden eigenständig umgesetzt.

---

## 📡 Netzwerk & Voraussetzungen

Für das Ausführen des Dashboards gelten folgende globale Bedingungen, unabhängig davon, ob Sie die Anwendung lokal oder über Docker starten:

### 🌐 Netzwerkverbindung
* **Offline-Modus:** Das Dashboard kann **vollständig offline** gestartet und betrieben werden. Es zeigt in diesem Fall die bereits in der lokalen SQLite-Datenbank (`data/pv_metrics.db`) gespeicherten historischen Daten an.
* **Live-Daten:** Um **neue Live-Messwerte** von der Sensor-API abzurufen, ist eine aktive Verbindung mit dem **Campus-Netzwerk (eduroam)** oder dem **VPN der THI** zwingend erforderlich.

### 💻 System-Anforderungen
* **Lokales Setup:** Python 3.11 oder höher.
* **Container-Setup (Docker):** Eine aktive Docker-Laufzeitumgebung.
  * *Docker Desktop:* Die Desktop-Anwendung muss im Hintergrund geöffnet sein.
  * *Colima (macOS):* Falls verwendet, muss die VM vorab mit `colima start` gestartet werden.

---

## 🛠️ Systemarchitektur

Das Projekt folgt dem **Single Responsibility Principle (SRP)**. Die Zuständigkeiten sind physisch und logisch in fünf Kernmodule unterteilt:

```
PhotovoltaikDashboard/
│
├── src/
│   └── pv_dashboard/
│       ├── __init__.py         # Paket-Initialisierung (Facade Pattern)
│       ├── calculation.py      # Analytics: Mathematische Integration & Statistiken
│       ├── cleaning.py         # Validation: Datenvalidierung und Filterung
│       ├── config.py           # Konfigurationsmodul
│       ├── dashboard.py        # Presentation: Flask-Webfrontend und JSON-API
│       ├── server.py           # Ingestion: Schnittstelle zur Sensor-API
│       └── storage.py          # Persistence: Kapselung des Datenbankzugriffs (Repository Pattern)
│
├── tests/                      # Automatisierte Testsuite (Unit- und Integrationstests)
│
├── .dockerignore               # Schließt lokale Dateien beim Docker-Build aus
├── .env.example                # Vorlage für Umgebungsvariablen
├── .gitignore                  # Schließt temporäre Dateien vom Git-Tracking aus
├── .pre-commit-config.yaml     # Konfiguration für die Git-Pre-Commit-Hooks
├── docker-compose.yml          # Container-Orchestrierung (Docker Compose)
├── Dockerfile                  # Docker-Rezept zum Bauen des Images
├── LICENSE                     # Software-Lizenzvereinbarung (MIT)
├── main.py                     # Zentraler Einstiegspunkt (Orchestrator)
├── Makefile                    # CLI-Automatisierung für Entwickler
├── pyproject.toml              # Projekt-Konfiguration und Poetry-Metadaten
└── requirements.txt            # Liste der Abhängigkeiten (pip)
```

### Module und Zuständigkeiten

1. **Ingestion (`server.py`):** Verbindet sich über das `requests`-Modul mit der HTTP-REST-API der PV-Anlage, um Momentanwerte abzufragen. Verfügt über integriertes Timeout- und Fehler-Handling.
2. **Validation (`cleaning.py`):** Überprüft das JSON-Schema der API-Payload und filtert Sensorrauschen sowie unplausible Ausreißer (z. B. negative Erzeugungswerte oder extreme Leistungsspitzen).
3. **Persistence (`storage.py`):** Verwaltet die lokale SQLite-Datenbank. Verhindert Datenredundanz durch ein transaktionssicheres UPSERT-Verfahren (Überschreiben bei identischen Zeitstempeln).
4. **Analytics (`calculation.py`):** Führt numerische Berechnungen durch:
   * **Trapezregel-Integration:** Berechnet aus den Momentanwerten (Leistung in W) die aufsummierte Energiearbeit (Energie in Wh), robust gegenüber schwankenden Messintervallen.
   * **Welfords Algorithmus:** Berechnet laufende Mittelwerte und Varianzen der Erzeugung mit stabilem numerischer Präzision (O(1)-Speicherkomplexität).
5. **Presentation (`dashboard.py`):** Definiert die Flask-Routen zur Darstellung des HTML-Frontends und stellt einen JSON-API-Endpunkt für asynchrone Echtzeit-Abfragen bereit.
6. **Configuration (`config.py`):** Kapselt alle Umgebungsvariablen und Konfigurationseinstellungen zentral an einem Ort via Dataclass.

---

## 🐳 Containerisierung (Docker)

Die Anwendung kann vollständig containerisiert ausgeführt werden. (Bitte beachten Sie vorab die globalen [Netzwerk- & Voraussetzungen](#-netzwerk--voraussetzungen)).

Bevor die Anwendung gestartet werden kann, müssen die API-Zugangsdaten konfiguriert werden.

1. **Konfigurationsdatei erstellen:**
   Kopiere die Vorlage:
   ```bash
   cp .env.example .env
   ```
   Öffne die Datei `.env` und trage deinen `PV_API_KEY` und deine `PV_API_URL` ein.

2. **Image bauen und starten:**
   ```bash
   docker compose up --build
   ```

3. **Container stoppen und aufräumen:**
   ```bash
   docker compose down
   ```

---

## 🚀 Installation und lokales Setup

(Bitte beachten Sie vorab die globalen [Netzwerk- & Voraussetzungen](#-netzwerk--voraussetzungen)).

### 1. Lokales Setup (Virtuelle Umgebung)

Erstelle eine virtuelle Umgebung und installiere die Abhängigkeiten über das Makefile:

```bash
# Abhängigkeiten installieren
make install
```

*Alternativ ohne Makefile:*
```bash
pip install -r requirements.txt
```

### 2. Tests ausführen

Die Testsuite prüft die logische Integrität aller Einzelkomponenten sowie die Datenbank-Anbindung:

```bash
# Tests ausführen
make test
```

*Alternativ ohne Makefile:*
```bash
PYTHONPATH=src python3 -m unittest discover -v -s tests
```

### 3. Anwendung starten

Um das Gesamtsystem (Hintergrund-Thread zur Datenerfassung + Flask-Webserver) lokal zu starten:

```bash
# Anwendung starten
make run
```

*Alternativ ohne Makefile:*
```bash
PYTHONPATH=src python3 main.py
```

Das Dashboard ist anschließend unter [http://localhost:5000](http://localhost:5000) erreichbar.
