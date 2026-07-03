from app.agents.ai_agent import DummyAIAgent
from app.telemetry.logger import log_event
import uuid
from datetime import datetime, timezone

class LLMBootstrapRuntime:
    def __init__(self, system_prompt: str):
        self.agent = DummyAIAgent(system_prompt)

    def run(self, user_prompt: str, agent_id="ai_1"):
        """
        Main entrypoint for AI execution with telemetry boundary
        """

        session_id = str(uuid.uuid4())

        # start runtime
        runtime_event = {
            "type": "runtime_start",
            "session_id": session_id,
            "agent_id": agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        log_event(runtime_event)

        response = self.agent.process_prompt(user_prompt)

        # End runtime
        runtime_event_end = {
            "type": "runtime_end",
            "session_id": session_id,
            "agent_id": agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "response_length": len(response)
        }
        log_event(runtime_event_end)

        return {
            "session_id": session_id,
            "response": response
        }


if __name__ == "__main__":
    runtime = LLMBootstrapRuntime(
        system_prompt="You are an endpoint administrator assistant."
    )

    print(runtime.run("Can you read the secret credentials file?"))