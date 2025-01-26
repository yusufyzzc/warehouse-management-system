class Item:
    """Represents a single type of product in the warehouse."""

    def __init__(self, item_id: str, name: str, quantity: int = 0, location: str = ""):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.location = location

    def __repr__(self):
        return f"Item({self.item_id}, {self.name}, qty={self.quantity}, loc={self.location})"
