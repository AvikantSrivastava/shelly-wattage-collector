#!/usr/bin/env python3
import os
import sys
import time
import logging

import requests
from requests.auth import HTTPDigestAuth
from prometheus_client import start_http_server, Gauge


SHELLY_HOST = os.environ.get("SHELLY_HOST", "10.0.0.86")
SHELLY_SWITCH_ID = os.environ.get("SHELLY_SWITCH_ID", "0")
SHELLY_USERNAME = os.environ.get("SHELLY_USERNAME", "admin")
SHELLY_PASSWORD = os.environ.get("SHELLY_PASSWORD")
SCRAPE_INTERVAL = float(os.environ.get("SCRAPE_INTERVAL_SECONDS", "15"))
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8080"))
REQUEST_TIMEOUT = float(os.environ.get("REQUEST_TIMEOUT_SECONDS", "5"))

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("shelly_exporter")


if not SHELLY_PASSWORD:
    log.error("SHELLY_PASSWORD is not set; refusing to start.")
    sys.exit(1)

AUTH = HTTPDigestAuth(SHELLY_USERNAME, SHELLY_PASSWORD)
URL = f"http://{SHELLY_HOST}/rpc/Switch.GetStatus?id={SHELLY_SWITCH_ID}"

LABELS = ["shelly_host"]
g_output = Gauge("shelly_output", "Switch output state (1=on, 0=off)", LABELS)
g_apower = Gauge("shelly_power_watts", "Active power draw in watts", LABELS)
g_voltage = Gauge("shelly_voltage_volts", "Line voltage", LABELS)
g_current = Gauge("shelly_current_amps", "Line current in amps", LABELS)
g_freq = Gauge("shelly_frequency_hz", "Line frequency in Hz", LABELS)
g_energy_total = Gauge(
    "shelly_energy_total_wh", "Cumulative active energy in watt-hours", LABELS
)
g_temp_c = Gauge("shelly_temperature_celsius", "Device temperature", LABELS)
g_on_time = Gauge("shelly_on_time_seconds", "Cumulative on-time in seconds", LABELS)
g_switch_count = Gauge("shelly_switch_on_count", "Number of times switched on", LABELS)
g_up = Gauge("shelly_up", "1 if the last scrape succeeded, else 0", LABELS)


def poll_once() -> None:
    labels = {"shelly_host": SHELLY_HOST}
    try:
        resp = requests.get(URL, auth=AUTH, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        g_output.labels(**labels).set(1 if data.get("output") else 0)
        g_apower.labels(**labels).set(data.get("apower", 0))
        g_voltage.labels(**labels).set(data.get("voltage", 0))
        g_current.labels(**labels).set(data.get("current", 0))
        g_freq.labels(**labels).set(data.get("freq", 0))
        g_energy_total.labels(**labels).set(data.get("aenergy", {}).get("total", 0))
        g_temp_c.labels(**labels).set(data.get("temperature", {}).get("tC", 0))
        g_on_time.labels(**labels).set(data.get("counts", {}).get("on_time", 0))
        g_switch_count.labels(**labels).set(data.get("counts", {}).get("switch_on", 0))
        g_up.labels(**labels).set(1)

    except Exception as exc:
        log.warning("scrape failed: %s", exc)
        g_up.labels(**labels).set(0)


def main() -> None:
    log.info(
        "starting shelly_exporter: host=%s port=%d interval=%.1fs",
        SHELLY_HOST,
        LISTEN_PORT,
        SCRAPE_INTERVAL,
    )
    start_http_server(LISTEN_PORT)
    while True:
        poll_once()
        time.sleep(SCRAPE_INTERVAL)


if __name__ == "__main__":
    main()
