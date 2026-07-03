import uuid
from datetime import datetime

class EventParser:
    def parse(self, event: dict):
        """
        Convert raw telemetry event into normalized correlation-ready format
        """

        event_id = str(uuid.uuid4())

        event_type = event.get("type", "unknown")
        risk = event.get("risk", 0.0)
        is_malicious = event.get("is_malicious", False)
        agent_id = event.get("agent_id", "unknown")

        # Severity Mapping
        if risk >= 0.8:
            severity = "critical"
        elif risk >= 0.5:
            severity = "high"
        elif risk >= 0.2:
            severity = "medium"
        else:
            severity = "low"

        # Normalized event type
        type_mapping = {
            "prompt": "AI_PROMPT",
            "tool": "AI_TOOL_CALL",
            "file": "FILE_ACCESS",
            "network": "NETWORK_ACTIVITY",
            "process": "PROCESS_ACTIVITY"
        }

        normalized_type = type_mapping.get(event_type, "UNKNOWN_EVENT")

        # Tagging
        tags = []
        if is_malicious:
            tags.append("malicious")

        if event_type == "prompt" and risk > 0.6:
            tags.append("prompt_injection")

        if event_type == "tool":
            tags.append("tool_usage")

        # Final
        parsed_event = {
            "event_id": event_id,
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "normalized_type": normalized_type,
            "agent_id": agent_id,
            "risk_score": risk,
            "is_malicious": is_malicious,
            "severity": severity,
            "tags": tags,
            "raw": event  # For forensic analysis later
        }

        return parsed_event