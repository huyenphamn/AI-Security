from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os


class BehaviorMLDetector:
    def __init__(self):
        base_dir = os.path.dirname(
        os.path.abspath(__file__)
        )
        self.name = "BehaviorMLDetector"
        project_root = os.path.abspath(
            os.path.join(base_dir, "..", "..", "..")
        )

        model_path = os.path.join(
            project_root,
            "models",
            "behavior_detector"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=True
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            local_files_only=True
        )

    def evaluate(self,event):

        if "action_type" not in event:
            return None

        text = f"""
        Prompt:
        {event.get('user_prompt','')}

        Attack Type:
        {event.get('action_type','unknown')}

        Context:
        Tool execution using {event.get('tool')}
        Command/File Target:
        {event.get('target')}
        """

        result = self.predict(text)

        if result["malicious"]:
            return {
                "type": "malicious_behavior",
                "risk": result["score"],
                "is_malicious": True
            }

        return None

    def predict(self,text):
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        with torch.no_grad():
            output = self.model(**inputs)
            probs = torch.softmax(
                output.logits,
                dim=1
            )[0]

        score = probs[1].item()

        return {
            "malicious": score > 0.5,
            "score": score
        }
    
    def predict_tokens(self, input_ids, attention_mask):
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            probs = torch.softmax(
                outputs.logits,
                dim=1
            )[0]

        score = probs[1].item()

        return {
            "malicious": score > 0.5,
            "score": score
        }