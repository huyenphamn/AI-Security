import sys
import os
import uuid
from datetime import datetime, timezone, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from correlation.incident_builder import IncidentBuilder

def run_tests():
    print("--- Initializing Correlation Engine Test ---")
    
    engine = IncidentBuilder(time_window_seconds=2)

    now = datetime.now(timezone.utc)

    # Time: 0s
    alert_1 = {
        "detector": "PromptInjectionDetector",
        "severity": "HIGH",
        "event_id": str(uuid.uuid4()),
        "timestamp": now.isoformat().replace("+00:00", "Z")
    }

    # Time + 1 - Group with alert1
    alert_2 = {
        "detector": "SuspiciousCommandDetector",
        "severity": "CRITICAL",
        "event_id": str(uuid.uuid4()),
        "timestamp": (now + timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
    }

    # Time: + 4 - time window expire - new incident
    alert_3 = {
        "detector": "SensitiveFileAccessDetector",
        "severity": "HIGH",
        "event_id": str(uuid.uuid4()),
        "timestamp": (now + timedelta(seconds=4)).isoformat().replace("+00:00", "Z")
    }

    print("\nProcessing Alert 1...")
    chain_1 = engine.process_alert(alert_1)
    print(f"Active Incident ID: {chain_1['incident_id']} | Total Alerts: {len(chain_1['alerts'])}")

    print("\nProcessing Alert 2 (+1 second later)...")
    chain_2 = engine.process_alert(alert_2)
    print(f"Active Incident ID: {chain_2['incident_id']} | Total Alerts: {len(chain_2['alerts'])}")
    
    if chain_1['incident_id'] == chain_2['incident_id']:
        print("SUCCESS: Alerts happened within 2 seconds and were correctly grouped!")
    else:
        print("FAIL: Alerts should have been grouped!")

    print("\nProcessing Alert 3 (+4 seconds later)...")
    chain_3 = engine.process_alert(alert_3)
    print(f"Active Incident ID: {chain_3['incident_id']} | Total Alerts: {len(chain_3['alerts'])}")
    
    if chain_1['incident_id'] != chain_3['incident_id']:
        print("SUCCESS: Time window expired, new incident chain was created!")
    else:
        print("FAIL: Alert 3 should have started a new incident.")

    print("\nForce Closing Stale Incidents...")
    future_time = now + timedelta(seconds=10)
    engine._close_stale_incidents(future_time)
    
    print(f"Total Finalized Incident Chains: {len(engine.closed_attack_chains)}")
    if len(engine.closed_attack_chains) == 2:
        print("SUCCESS: Memory successfully cleared and incidents finalized.")

if __name__ == "__main__":
    run_tests()