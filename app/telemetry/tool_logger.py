from app.telemetry.events import AIAgentAction
from app.telemetry.logger import log_event
import uuid
from datetime import datetime, timezone


def log_tool_event(action_type: str, target: str, status: str = "SUCCESS", agent_id="agent_001"):
    """
    Manual tool event logger (used for non-decorated tool calls if needed)
    """
    event = AIAgentAction(
        timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        event_id=str(uuid.uuid4()),
        agent_id=agent_id,
        action_type=action_type,
        target=target,
        status=status
    )

    log_event(event.to_json())