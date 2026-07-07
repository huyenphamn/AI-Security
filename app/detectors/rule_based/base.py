class BaseDetector:
    def __init__(self):
        self.name = self.__class__.__name__

    def evaluate(self, event_dict: dict) -> dict | None:
        """
        Evaluates a telemetry event dictionary.
        Returns an alert dictionary if malicious activity is found, otherwise None.
        """
        raise NotImplementedError("Detectors must implement the evaluate method.")