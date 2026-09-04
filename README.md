# shelly-wattage-collector

A Prometheus exporter for Shelly smart plugs that exposes power metrics.

Link: https://us.shelly.com/products/shelly-plug-us-gen4-white

## Docker

```bash
docker pull ghcr.io/avikantsrivastava/shelly-wattage-collector:latest
```

### Docker Compose

```yaml
services:
  shelly-exporter:
    image: ghcr.io/avikantsrivastava/shelly-wattage-collector:latest
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - SHELLY_HOST=10.0.0.86
      - SHELLY_USERNAME=admin
      - SHELLY_PASSWORD=your_password
      - SHELLY_SWITCH_ID=0
      - SCRAPE_INTERVAL_SECONDS=15
      - LISTEN_PORT=8080
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SHELLY_HOST` | `10.0.0.86` | IP address of your Shelly device |
| `SHELLY_USERNAME` | `admin` | Username for Shelly authentication |
| `SHELLY_PASSWORD` | (required) | Password for Shelly authentication |
| `SHELLY_SWITCH_ID` | `0` | Switch ID to monitor |
| `SCRAPE_INTERVAL_SECONDS` | `15` | Polling interval in seconds |
| `LISTEN_PORT` | `8080` | Port for Prometheus metrics endpoint |
| `REQUEST_TIMEOUT_SECONDS` | `5` | HTTP request timeout |
| `LOG_LEVEL` | `INFO` | Logging level |

## Metrics

The exporter exposes the following metrics at `/metrics`:

- `shelly_power_watts` - Active power draw in watts
- `shelly_voltage_volts` - Line voltage
- `shelly_current_amps` - Line current in amps
- `shelly_frequency_hz` - Line frequency in Hz
- `shelly_energy_total_wh` - Cumulative energy in watt-hours
- `shelly_temperature_celsius` - Device temperature
- `shelly_output` - Switch state (1=on, 0=off)
- `shelly_on_time_seconds` - Cumulative on-time
- `shelly_switch_on_count` - Number of times switched on
- `shelly_up` - Scrape success indicator
