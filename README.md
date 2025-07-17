# Log Analyzer

`analyzeLogs.py` analyzes a web server log file to detect suspicious IP addresses based on request frequency and burst behavior.

---

## Included Files

- `analyzeLogs.py` — Python script that processes the log file and prints suspicious IPs.
- `sample-log.log` — Example log file for testing.
- `Dockerfile` — Docker configuration to build and run the analyzer easily.

---

## Requirements

- [Docker] installed on your system  
  **OR**  
- **Python 3.12.10 or newer** (if running the script directly without Docker)

---

## How to Run

### Option 1: Using Docker

1. Build the Docker image:

   ```bash
   docker build -t log-analyzer .
