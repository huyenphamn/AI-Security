from detectors.base import BaseDetector

class PromptInjectionDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.suspicious_keywords = [
            "ignore previous", 
            "override", 
            "jailbreak",
            "system prompt"
        ]

    def evaluate(self, event_dict: dict) -> dict | None:
        # Filter out irrelevant events - only care about prompt activities
        if "user_prompt" not in event_dict:
            return None
        
        user_prompt = event_dict.get("user_prompt", "").lower()
        
        # Check heuristics
        for keyword in self.suspicious_keywords:
            if keyword in user_prompt:
                # return standard alert
                return {
                    "detector": self.name,
                    "severity": "HIGH",
                    "reason": f"Prompt injection pattern detected: '{keyword}'",
                    "event_id": event_dict.get("event_id"),
                    "timestamp": event_dict.get("timestamp")
                }
                
        return None