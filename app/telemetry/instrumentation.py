import functools
import uuid
from datetime import datetime, timezone
from app.telemetry.events import AIAgentAction
from app.telemetry.logger import log_event

def monitor_tool(action_type: str):
    """
    Intercepts tool execution and logs as AI Telemetry.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Intercept the target
            target = args[0] if args else str(kwargs)
            status = "SUCCESS"
            
            try:
                result = func(*args, **kwargs) 
                return result
            except Exception as e:
                status = f"FAILED: {str(e)}"
                raise
            finally:
                # Build and log AT Telemetry
                event = AIAgentAction(
                    timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    event_id=str(uuid.uuid4()),
                    action_type=action_type,
                    target=target,
                    status=status
                )
                log_event(event.to_json())
                
        return wrapper
    return decorator