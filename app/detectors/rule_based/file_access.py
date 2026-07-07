from app.detectors.rule_based.base import BaseDetector

class SensitiveFileAccessDetector(BaseDetector):
    def __init__(self):
        super().__init__()
        self.sensitive_keywords = ["secret", "credential", "password", ".env", "id_rsa"] # Keyword sensitive files

    def evaluate(self, event_dict: dict) -> dict | None:
        if event_dict.get("action_type") != "file_access":
            return None
        
        target_file = event_dict.get("target", "").lower()
        
        for keyword in self.sensitive_keywords: # Check if agents try to access files with those keywords
            if keyword in target_file:
                return {
                    "detector": self.name,
                    "severity": "HIGH",
                    "reason": f"AI attempted to access sensitive file matching: '{keyword}'",
                    "event_id": event_dict.get("event_id"),
                    "timestamp": event_dict.get("timestamp")
                }
                
        return None