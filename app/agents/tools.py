# agent/tools.py

from app.telemetry.instrumentation import monitor_tool
import subprocess


@monitor_tool(action_type="file_access")
def read_file(filepath: str) -> str:
    """
    Simulated file read tool.
    """
    print(f"[TOOL] read_file - {filepath}")

    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"[ERROR] File not found: {filepath}"


@monitor_tool(action_type="terminal_execution")
def execute_command(command: str) -> str:
    """
    Simulated terminal execution tool.
    """
    print(f"[TOOL] execute_command - {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout or result.stderr

    except Exception as e:
        return f"[ERROR] Command failed: {str(e)}"


@monitor_tool(action_type="network_request")
def http_request(url: str) -> str:
    """
    Simulated network tool (for exfiltration scenarios in tests).
    """
    print(f"[TOOL] http_request - {url}")
    return f"[SIMULATED RESPONSE] fetched from {url}"