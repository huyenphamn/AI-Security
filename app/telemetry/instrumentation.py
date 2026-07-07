import functools
import uuid
from datetime import datetime, timezone

from app.telemetry.events import AIAgentAction
from app.telemetry.logger import log_event


def monitor_tool(action_type: str, tool_name: str):

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            target = args[0] if args else str(kwargs)

            status = "SUCCESS"

            try:
                result = func(*args, **kwargs)
                return result

            except Exception as e:
                status = f"FAILED: {str(e)}"
                raise

            finally:

                event = {
                    "timestamp": datetime.now(timezone.utc)
                    .isoformat()
                    .replace("+00:00", "Z"),

                    "event_id": str(uuid.uuid4()),

                    "event_type": "tool",

                    "tool": tool_name,

                    "action_type": action_type,

                    "target": target,

                    "status": status
                }

                log_event(event)

        return wrapper

    return decorator