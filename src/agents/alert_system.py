from ..events.alert_events import ALERT_RAISED, ALERT_RESOLVED

class AlertSystem:
    """Handles alert notifications and resolution."""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.alerts = []  # Keep a list of active alerts

        event_bus.register_listener(ALERT_RAISED, self.on_alert_raised)
        event_bus.register_listener(ALERT_RESOLVED, self.on_alert_resolved)

    def on_alert_raised(self, title, message):
        alert_info = {"title": title, "message": message}
        self.alerts.append(alert_info)
        print(f"[AlertSystem] ALERT: {title} - {message}")

    def on_alert_resolved(self, title):
        self.alerts = [a for a in self.alerts if a["title"] != title]
        print(f"[AlertSystem] ALERT RESOLVED: {title}")

    def get_active_alerts(self):
        return self.alerts
