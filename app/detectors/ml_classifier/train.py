from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)
import numpy as np
import evaluate

dataset = load_dataset("deepset/prompt-injections")
 
model_name = "distilbert-base-uncased" # Use distilbert model
tokenizer = AutoTokenizer.from_pretrained(model_name)

def preprocess(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=256
    )

tokenized = dataset.map(preprocess, batched=True)

model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=2
)

accuracy = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = np.argmax(logits, axis=1)
    return accuracy.compute(predictions=preds, references=labels)

args = TrainingArguments(
    output_dir="./models",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=2,
    weight_decay=0.01
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=tokenized["train"],
    eval_dataset=tokenized["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.save_model("./models/prompt_injection_detector")
tokenizer.save_pretrained("./models/prompt_injection_detector")