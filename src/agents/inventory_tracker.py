from ..events import inventory_events as inv_ev
from ..events.alert_events import ALERT_RAISED
from ..models.item import Item

class InventoryTracker:
    """Manages item inventory, listens for additions/removals, and emits low-stock alerts."""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.items = {}  # item_id -> Item

        # Register relevant event listeners
        event_bus.register_listener(inv_ev.ITEM_ADDED, self.on_item_added)
        event_bus.register_listener(inv_ev.ITEM_REMOVED, self.on_item_removed)
        event_bus.register_listener(inv_ev.INVENTORY_CHECK, self.on_inventory_check)

    def on_item_added(self, item_id, quantity, name=None, location=None):
        # If item doesn't exist, create it
        if item_id not in self.items:
            self.items[item_id] = Item(item_id, name or "Unknown", 0, location or "Unknown")
        self.items[item_id].quantity += quantity

        print(f"[InventoryTracker] Added {quantity} of {item_id}, total is now {self.items[item_id].quantity}.")

    def on_item_removed(self, item_id, quantity):
        if item_id in self.items:
            self.items[item_id].quantity -= quantity
            if self.items[item_id].quantity < 0:
                self.items[item_id].quantity = 0
            print(f"[InventoryTracker] Removed {quantity} of {item_id}, total is now {self.items[item_id].quantity}.")
            
            # Check if stock is low
            if self.items[item_id].quantity < 3:  # example threshold
                self.event_bus.emit(ALERT_RAISED,
                    title="Low Stock",
                    message=f"Item {item_id} is running low: {self.items[item_id].quantity} in stock."
                )
        else:
            print(f"[InventoryTracker] Cannot remove from item {item_id}, it does not exist.")

    def on_inventory_check(self):
        """Periodically check inventory and raise alerts if needed."""
        for item_id, item in self.items.items():
            if item.quantity < 3:
                self.event_bus.emit(ALERT_RAISED,
                    title="Low Stock",
                    message=f"Item {item_id} has low stock: {item.quantity}."
                )

    def get_all_items(self):
        return list(self.items.values())

    def get_item(self, item_id):
        return self.items.get(item_id, None)
