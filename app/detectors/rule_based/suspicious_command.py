from app.detectors.rule_based.base import BaseDetector

class SuspiciousCommandDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.risky_binaries = ["curl", "wget", "powershell", "cmd.exe", "bash -i"] # commonly used attack commands

    def evaluate(self, event_dict: dict) -> dict | None:
        if event_dict.get("action_type") != "terminal_execution":
            return None
        
        target_command = event_dict.get("target", "").lower()
        
        for binary in self.risky_binaries: # Check if they contain attack commands
            if binary in target_command:
                return {
                    "detector": self.name,
                    "severity": "CRITICAL",
                    "reason": f"Suspicious binary execution attempted: '{binary}'",
                    "event_id": event_dict.get("event_id"),
                    "timestamp": event_dict.get("timestamp")
                }
                
        return None