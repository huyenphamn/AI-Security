import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass(kw_only=True)
class BaseTelemetry:
    timestamp: str
    event_id: str
    agent_id: str = "agent_001"

    def to_json(self):
        return json.dumps(asdict(self))

@dataclass(kw_only=True)
class PromptActivity(BaseTelemetry):
    user_prompt: str
    system_prompt: str

@dataclass(kw_only=True)
class AIAgentAction(BaseTelemetry):
    action_type: str
    target: str
    status: str