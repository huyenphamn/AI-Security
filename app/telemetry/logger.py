import os

LOG_FILE = "logs/telemetry.json"

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(LOG_FILE, "w") as f:     # freah log for each tests
        f.write("")

def log_event(event_json: str):
    with open(LOG_FILE, "a") as f:
        f.write(event_json + "\n")