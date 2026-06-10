# 1. Starten mit einem Python-Image
FROM python:3.11-slim

# 2. Erstellen eines Ordners für unsere App im Container
WORKDIR /app

# 3. Kopieren der requirements.txt in den Container
COPY requirements.txt .

# 4. Installieren der benötigten Bibliotheken (Flask und requests)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Kopieren des gesamten Projektcodes in den Container
COPY . .

# 6. Teilen Python im Container mit, wo es die Module suchen soll
ENV PYTHONPATH=src

# 7. Teilen Docker mit, dass die App auf Port 5000 erreichbar ist
EXPOSE 5000

# 8. Der Befehl, der ausgeführt wird, wenn der Container startet
CMD ["python", "main.py"]
