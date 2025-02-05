class Telemetry:
    def __init__(self):
        self.logs = []

    def log_event(self, event_type, data):
        self.logs.append({"event": event_type, "data": data})
        if len(self.logs) > 50:
            self.logs.pop(0)

    def get_logs(self):
        return self.logs
