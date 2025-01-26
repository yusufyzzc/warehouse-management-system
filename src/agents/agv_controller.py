from ..events import order_events as ord_ev
from ..events.alert_events import ALERT_RAISED

class AGVController:
    """Simulates an AGV (robot) that picks and transports items once an order is approved."""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        event_bus.register_listener(ord_ev.ORDER_APPROVED, self.on_order_approved)

    def on_order_approved(self, order_id, items):
        print(f"[AGV] Starting pick process for order {order_id}...")
        success = True
        if not success:
            self.event_bus.emit(ALERT_RAISED, title="AGV Error", message=f"AGV failed to pick order {order_id}.")
        else:
            print(f"[AGV] Successfully picked items for order {order_id}. Transporting to shipping area...")
