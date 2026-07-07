from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os

class PromptInjectionMLDetector:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.name = "PromptInjectionMLDetector"
        project_root = os.path.abspath(
            os.path.join(base_dir, "..", "..", "..")
        )

        model_path = os.path.join(
            project_root,
            "models",
            "prompt_injection_detector"
        )

        model_path = os.path.abspath(model_path)

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=True
        )

        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            local_files_only=True
        )

    def evaluate(self, event):
        # Only evaluate if the event is a is a prompt
        if "user_prompt" not in event:
            return None

        prompt_text = event["user_prompt"]

        prediction = self.predict(prompt_text)

        if prediction["is_injection"]:
            return {
                "type": "prompt_injection",
                "risk": prediction["score"],
                "is_malicious": True
            }

        return None

    def predict(self, text: str):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=256
        )

        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)[0]

        injection_score = probs[1].item()

        return {
            "is_injection": injection_score > 0.85,
            "score": injection_score
        }