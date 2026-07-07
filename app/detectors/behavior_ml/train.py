from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

import numpy as np
import evaluate
import kagglehub
import json
import os
from datasets import Dataset
# Download dataset
path = kagglehub.dataset_download(
    "cyberprince/ai-agent-evasion-dataset"
)
json_file = os.path.join(
    path,
    "AI Agent Evasion Dataset.jsonl"
)
# Load jsonl
examples = []

with open(json_file, "r") as f:
    for line in f:
        examples.append(json.loads(line))

dataset = Dataset.from_list(examples)
print(dataset[0])

def convert_label(example):
    example["label"] = (
        1 
        if example["label"] == "malicious"
        else 0
    )
    return example
dataset = dataset.map(convert_label)
def create_text(example):

    text = f"""
    Prompt:
    {example['prompt']}

    Attack Type:
    {example['attack_type']}

    Context:
    {example['context']}
    """

    return {
        "text": example["prompt"]
    }
dataset = dataset.map(create_text)
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=256
    )

    tokens["labels"] = example["label"]

    return tokens

dataset = dataset.train_test_split(
    test_size=0.2,
    seed=42
)

tokenized = dataset.map(
    preprocess,
    batched=True,
    remove_columns=dataset["train"].column_names
)

tokenized["test"].save_to_disk(
    "./behavior_test_dataset"
)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2
)

args = TrainingArguments(
    output_dir="./models",
    eval_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=3,
    learning_rate=2e-5,
    per_device_train_batch_size=8
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"]
)

trainer.train()
trainer.save_model(
    "./models/behavior_detector"
)
tokenizer.save_pretrained(
    "./models/behavior_detector"
)