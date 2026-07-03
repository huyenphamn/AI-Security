import uuid
from datetime import datetime

class IncidentBuilder:
    def __init__(self, time_window_seconds=5):
        self.time_window = time_window_seconds
        self.active_incidents = []
        self.closed_attack_chains = []

    def _parse_time(self, time_str: str) -> datetime:
        return datetime.fromisoformat(time_str.replace("Z", "+00:00"))

    def process_alert(self, alert: dict) -> dict:
        alert_time = self._parse_time(alert["timestamp"])
        matched_incident = None

        for incident in self.active_incidents:
            last_updated = self._parse_time(incident["last_updated"])
            time_diff = (alert_time - last_updated).total_seconds()

            if (
                time_diff <= self.time_window and
                incident.get("agent_id") == alert.get("agent_id")
            ):
                incident["alerts"].append(alert)
                incident["last_updated"] = alert["timestamp"]

                # track event types for attack classification
                incident.setdefault("event_types", set()).add(alert.get("type"))

                matched_incident = incident
                break

        if not matched_incident:
            matched_incident = {
                "incident_id": str(uuid.uuid4()),
                "status": "OPEN",
                "start_time": alert["timestamp"],
                "last_updated": alert["timestamp"],
                "agent_id": alert.get("agent_id"),
                "alerts": [alert],
                "event_types": set([alert.get("type")])
            }
            self.active_incidents.append(matched_incident)

        self._close_stale_incidents(alert_time)
        return matched_incident

    def _close_stale_incidents(self, current_time: datetime):
        active_incidents = []

        for incident in self.active_incidents:
            last_updated = self._parse_time(incident["last_updated"])
            time_since = (current_time - last_updated).total_seconds()

            if time_since > self.time_window:
                incident["status"] = "CLOSED"

                # convert set to list for JSON safety
                incident["event_types"] = list(incident.get("event_types", []))

                self.closed_attack_chains.append(incident)
            else:
                active_incidents.append(incident)

        self.active_incidents = active_incidents