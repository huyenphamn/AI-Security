from app.telemetry.events import AIAgentAction
from app.telemetry.logger import log_event
import uuid
from datetime import datetime, timezone


class EndpointMonitor:
    """
    Simulated endpoint telemetry collector (EDR-style), generates OS-level events for correlation engine.
    """

    def log_process_event(self, process_name: str, status="RUNNING"):
        event = AIAgentAction(
            timestamp=self._now(),
            event_id=str(uuid.uuid4()),
            action_type="process_execution",
            target=process_name,
            status=status
        )
        log_event(event.to_json())

    def log_file_event(self, filepath: str, status="ACCESSED"):
        event = AIAgentAction(
            timestamp=self._now(),
            event_id=str(uuid.uuid4()),
            action_type="file_operation",
            target=filepath,
            status=status
        )
        log_event(event.to_json())

    def log_network_event(self, destination: str, status="CONNECTED"):
        event = AIAgentAction(
            timestamp=self._now(),
            event_id=str(uuid.uuid4()),
            action_type="network_connection",
            target=destination,
            status=status
        )
        log_event(event.to_json())

    def _now(self):
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")