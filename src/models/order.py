from typing import List

class Order:
    """Represents an order with multiple items (if needed)."""

    def __init__(self, order_id: str, items: List[dict], status: str = "PENDING"):
        """
        :param order_id: Unique identifier for the order
        :param items: List of dicts, each dict like {"item_id": "XYZ", "quantity": 10}
        :param status: The current status of the order (PENDING, APPROVED, CANCELED, etc.)
        """
        self.order_id = order_id
        self.items = items
        self.status = status

    def __repr__(self):
        return f"Order({self.order_id}, status={self.status}, items={self.items})"
