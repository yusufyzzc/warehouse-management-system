from ..events import order_events as ord_ev
from ..events import inventory_events as inv_ev
from ..models.order import Order

class OrderProcessor:
    """Handles order creation, approval, and updates."""

    def __init__(self, event_bus, inventory_tracker):
        self.event_bus = event_bus
        self.inventory_tracker = inventory_tracker
        self.orders = {}

        event_bus.register_listener(ord_ev.ORDER_CREATED, self.on_order_created)

    def on_order_created(self, order_id, items):
        """When a new order is created, let's check inventory for each item."""
        new_order = Order(order_id, items)
        self.orders[order_id] = new_order
        print(f"[OrderProcessor] Received new order: {new_order}")

        can_fulfill = True
        for item_line in items:
            item_id = item_line["item_id"]
            quantity = item_line["quantity"]

            item = self.inventory_tracker.get_item(item_id)
            if not item or item.quantity < quantity:
                can_fulfill = False
                print(
                    f"[OrderProcessor] Not enough stock for {item_id}: requested {quantity},"
                    f" available {item.quantity if item else 0}."
                )
                break

        if can_fulfill:
            for item_line in items:
                self.event_bus.emit(
                    inv_ev.ITEM_REMOVED,
                    item_id=item_line["item_id"],
                    quantity=item_line["quantity"],
                )
            new_order.status = "APPROVED"
            print(f"[OrderProcessor] Order {order_id} has been approved.")
            self.event_bus.emit(ord_ev.ORDER_APPROVED, order_id=order_id, items=items)
        else:
            new_order.status = "REJECTED"
            print(f"[OrderProcessor] Order {order_id} rejected due to insufficient stock.")

    def get_all_orders(self):
        return list(self.orders.values())

    def get_order(self, order_id):
        return self.orders.get(order_id)
