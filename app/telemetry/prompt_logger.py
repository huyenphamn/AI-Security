import json
import uuid
from datetime import datetime, timezone
from app.detectors.rule_engine import RuleEngine
from app.telemetry.logger import log_event


class PromptLogger:
    def __init__(self):
        self.detector = RuleEngine()

    def log_prompt(self, prompt, agent_id="agent_001", metadata=None):
        result = self.detector.check(prompt)

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "event_id": str(uuid.uuid4()),
            "agent_id": agent_id,

            "type": "prompt",
            "content": prompt,

            "risk": result["final_score"],
            "is_malicious": result["is_injection"],

            "metadata": metadata or {}
        }
        log_event(json.dumps(event))

        return event