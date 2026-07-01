import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class BaseTelemetry:
    timestamp: str
    event_id: str
    agent_id: str = "agent_001"

    def to_json(self):
        return json.dumps(asdict(self))

@dataclass
class PromptActivity(BaseTelemetry):
    user_prompt: str
    system_prompt: str

@dataclass
class AIAgentAction(BaseTelemetry):
    action_type: str
    target: str
    status: str