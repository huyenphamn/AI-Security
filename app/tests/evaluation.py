from app.detectors.prompt_injection.detector import PromptInjectionMLDetector
from datasets import load_dataset
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

def run_evaluation():
    print("Loading test dataset for evaluation...")
    dataset = load_dataset("deepset/prompt-injections", split="test")
    
    detector = PromptInjectionMLDetector()
    
    predictions = []
    labels = []

    print(f"Evaluating {len(dataset)} prompts...")
    
    # Batch prediction
    for item in dataset:
        text = item['text']
        true_label = item['label'] # 0 for safe, 1 for injection
        
        result = detector.predict(text)
        pred_label = 1 if result["is_injection"] else 0
        
        predictions.append(pred_label)
        labels.append(true_label)

    # Calculate Metrics
    print("\n--- Evaluation Results ---")
    print(f"Accuracy: {accuracy_score(labels, predictions):.4f}")
    print("\nClassification Report:")
    # Precision, Recall, and F1-Score
    print(classification_report(labels, predictions, target_names=["Safe", "Injection"]))

if __name__ == "__main__":
    run_evaluation()