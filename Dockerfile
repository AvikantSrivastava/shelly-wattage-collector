FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shelly-exporter.py .

ENV SHELLY_HOST=""
ENV SHELLY_USERNAME="admin"
ENV SHELLY_PASSWORD=""
ENV SCRAPE_INTERVAL_SECONDS="15"
ENV LISTEN_PORT="8080"

EXPOSE 8080

CMD ["python", "shelly-exporter.py"]
