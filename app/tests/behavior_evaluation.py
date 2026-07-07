from app.detectors.behavior_ml.detector import BehaviorMLDetector
from sklearn.metrics import classification_report, accuracy_score
from datasets import load_from_disk
import torch

def run_evaluation():

    print("Loading behavior dataset...")

    dataset = load_from_disk(
        "./behavior_test_dataset"
    )
    detector = BehaviorMLDetector()

    predictions = []
    labels = []
    print(f"Evaluating {len(dataset)} samples...")


    for item in dataset:

        input_ids = torch.tensor(
            [item["input_ids"]]
        )

        attention_mask = torch.tensor(
            [item["attention_mask"]]
        )

        result = detector.predict_tokens(
            input_ids,
            attention_mask
        )

        pred_label = (
            1
            if result["malicious"]
            else 0
        )

        true_label = item["labels"]
        predictions.append(pred_label)
        labels.append(true_label)
    print("\n--- Behavior ML Evaluation ---")
    print(
        f"Accuracy: {accuracy_score(labels, predictions):.4f}"
    )
    print(
        classification_report(
            labels,
            predictions,
            target_names=[
                "Benign",
                "Malicious"
            ]
        )
    )
if __name__ == "__main__":
    run_evaluation()