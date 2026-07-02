import uuid
from datetime import datetime
class IncidentBuilder: 
    """State machine that monitors incoming alerts"""
    def __init__(self, time_window_seconds=5):
        self.time_window = time_window_seconds
        # Holds open incidents
        self.active_incidents = []
        # Holds timed out incidents
        self.closed_attack_chains = []
    
    def _parse_time(self, time_str: str) -> datetime:
        """Convert ISO string timestamps back into Python datetime objects"""
        return datetime.fromisoformat(time_str.replace("Z", "+00:00")) # For python 3.10 compatibility

    def process_alert(self, alert: dict) -> dict:
        """
        Evaluates a new alert against active incidents
        Returns the updated incident dictionary
        """
        alert_time = self._parse_time(alert["timestamp"])
        matched_incident = None

        for incident in self.active_incidents: # Check if it fits into an existing incident chain 
            last_updated = self._parse_time(incident["last_updated"])
            time_diff = (alert_time - last_updated).total_seconds()
            
            if time_diff <= self.time_window: # Attach alert if it happens within the time window
                incident["alerts"].append(alert)
                incident["last_updated"] = alert["timestamp"]
                matched_incident = incident
                break
        
        # Add new incident chain if not matched
        if not matched_incident:
            matched_incident = {
                "incident_id": str(uuid.uuid4()),
                "status": "OPEN",
                "start_time": alert["timestamp"],
                "last_updated": alert["timestamp"],
                "alerts": [alert]
            }
            self.active_incidents.append(matched_incident)

        # Evict incidents that timed out
        self._close_stale_incidents(alert_time)

        return matched_incident
    
    def _close_stale_incidents(self, current_time: datetime):
        """
        If active incident hasn't received a new alert within the time window, marked as closed
        """
        active_incidents = []
        
        for incident in self.active_incidents:
            last_updated = self._parse_time(incident["last_updated"])
            time_since_last_alert = (current_time - last_updated).total_seconds()
            
            if time_since_last_alert > self.time_window:
                incident["status"] = "CLOSED" # The window has closed. The attack chain is finalized.
                self.closed_attack_chains.append(incident)
            else:
                active_incidents.append(incident)
                
        self.active_incidents = active_incidents