from ..events import inventory_events as inv_ev

class RFIDSensor:
    """Simulates an RFID sensor that detects when items enter or leave the warehouse."""

    def __init__(self, event_bus):
        self.event_bus = event_bus

    def simulate_item_arrival(self, item_id, quantity, name=None, location=None):
        """Simulate that new stock has arrived."""
        self.event_bus.emit(inv_ev.ITEM_ADDED, item_id=item_id, quantity=quantity, name=name, location=location)

    def simulate_item_departure(self, item_id, quantity):
        """Simulate that some stock is leaving (manually)."""
        self.event_bus.emit(inv_ev.ITEM_REMOVED, item_id=item_id, quantity=quantity)
