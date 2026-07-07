from app.detectors.prompt_injection.detector import PromptInjectionDetector
import re

class RuleEngine:
    def __init__(self):
        self.ml_detector = PromptInjectionDetector()

    def check(self, prompt: str):
        # Fast rule-based checks
        rule_flags = []

        patterns = [
            r"ignore previous instructions",
            r"system prompt",
            r"jailbreak",
            r"reveal.*prompt",
        ]

        for p in patterns:
            if re.search(p, prompt.lower()):
                rule_flags.append("rule_match")

        # ML model scoring
        ml_result = self.ml_detector.predict(prompt)

        # Decision logic
        final_score = ml_result["score"] + (0.3 if rule_flags else 0)

        return {
            "is_injection": final_score > 0.6,
            "ml_score": ml_result["score"],
            "rule_flags": rule_flags,
            "final_score": final_score
        }