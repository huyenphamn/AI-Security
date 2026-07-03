# AI-Security

## Overview

AI-Security is a simulated AI security monitoring system designed to detect and correlate malicious interactions targeting an AI agent.

The system simulates real-world threats such as:
- Prompt injection attacks
- Sensitive file access attempts
- Malicious command execution

It combines:
- Telemetry logging (AI + tool actions)
- Rule-based + ML-based detection
- Event correlation into attack chains

## System Architecture

User Prompt
   &darr;
AI Agent (agent/)
   &darr;
Telemetry Logging (telemetry/)
   &darr;
Detection Layer (detectors/)
   - Rule Engine (fast detection)
   - ML Classifier (DistilBERT prompt injection model)
   &darr;
Alert Generation
   &darr;
Correlation Engine (correlation/)
   - Groups alerts in time window
   - Builds attack chains
   &darr;
Incident Output + (future) Visualization Layer

## End-to-End Pipeline

1. A user prompt is sent to the AI agent
2. The agent may:
   - Respond normally
   - Execute a tool (file read / command execution)
3. All actions are logged as telemetry events
4. Detection engines analyze logs:
   - Rule-based detection (regex/keywords)
   - ML classifier (prompt injection detection using DistilBERT)
5. Alerts are generated when malicious behavior is detected
6. The correlation engine groups alerts into incidents using a time window

## Modules

### agent/
Simulated LLM agent that can:
- Process prompts
- Call tools (file access, shell commands)
- Generate telemetry logs

### telemetry/
Captures system-wide events:
- Prompt logs
- Tool execution logs
- Structured event tracking

### detectors/
Security detection layer:
- Rule engine: fast keyword/regex detection
- ML classifier: HuggingFace DistilBERT model for prompt injection detection

### correlation/
Groups related alerts into attack chains using time-window based correlation.

### graph/ (future)
Will visualize incidents as attack graphs using NetworkX / Neo4j.

## ML Model (Prompt Injection Detection)

A DistilBERT-based classifier trained on the `deepset/prompt-injections` dataset.

### Performance
--- Evaluation Results ---
Accuracy: 0.9397

Classification Report:
              precision  |  recall  | f1-score  |  support

        Safe   |    0.92  |    0.96  |   0.94   |     56
   Injection   |   0.96   |  0.92   |   0.94    |    60

    accuracy   |                        0.94    |   116
   macro avg   |    0.94   |  0.94      0.94    |   116
weighted avg   |    0.94   |  0.94      0.94    |   116

### Evaluation Dataset
- HuggingFace dataset: deepset/prompt-injections

## How to Run

### Install dependencies
```bash
pip install -r requirements.txt
python3 -m app.main
python3 -m app.tests.attack_scenarios
python3 -m app.tests.evaluation

```