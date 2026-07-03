import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_FILE = os.path.join(BASE_DIR, "logs", "telemetry.json")


def setup_logger():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "w") as f:
        f.write("")


def log_event(event_json: str):
    with open(LOG_FILE, "a") as f:
        f.write(event_json + "\n")