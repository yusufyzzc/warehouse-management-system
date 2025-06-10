import tkinter as tk
from tkinter import ttk, messagebox

from .event_bus import EventBus
from .agents.inventory_tracker import InventoryTracker
from .agents.order_processor import OrderProcessor
from .agents.agv_controller import AGVController
from .agents.rfid_sensor import RFIDSensor
from .agents.alert_system import AlertSystem

from .events import order_events as ord_ev
from .events import inventory_events as inv_ev
from .events import alert_events as al_ev


class WarehouseApp(tk.Tk):
    """Main tkinter application for the warehouse EDP system."""

    def __init__(self):
        super().__init__()
        self.title("Warehouse Management System")
        self.geometry("900x500")

        self.event_bus = EventBus()

        self.inventory_tracker = InventoryTracker(self.event_bus)
        self.order_processor = OrderProcessor(self.event_bus, self.inventory_tracker)
        self.agv_controller = AGVController(self.event_bus)
        self.rfid_sensor = RFIDSensor(self.event_bus)
        self.alert_system = AlertSystem(self.event_bus)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill=tk.BOTH)

        self._create_inventory_tab()
        self._create_orders_tab()
        self._create_alerts_tab()
        self._create_agv_tab()


    # INVENTORY TAB

    def _create_inventory_tab(self):
        inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="Inventory")

        # Frame for adding items
        add_item_frame = ttk.LabelFrame(inventory_frame, text="Add Item to Inventory")
        add_item_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(add_item_frame, text="Item ID:").grid(row=0, column=0, sticky="w")
        self.entry_item_id = ttk.Entry(add_item_frame)
        self.entry_item_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_item_frame, text="Name:").grid(row=1, column=0, sticky="w")
        self.entry_name = ttk.Entry(add_item_frame)
        self.entry_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_item_frame, text="Quantity:").grid(row=2, column=0, sticky="w")
        self.entry_quantity = ttk.Entry(add_item_frame)
        self.entry_quantity.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(add_item_frame, text="Location:").grid(row=3, column=0, sticky="w")
        self.entry_location = ttk.Entry(add_item_frame)
        self.entry_location.grid(row=3, column=1, padx=5, pady=5)

        add_btn = ttk.Button(add_item_frame, text="Add to Inventory", command=self._add_item_to_inventory)
        add_btn.grid(row=4, column=0, columnspan=2, pady=10)

        # Frame for removing items
        remove_item_frame = ttk.LabelFrame(inventory_frame, text="Remove Item from Inventory")
        remove_item_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(remove_item_frame, text="Item ID:").grid(row=0, column=0, sticky="w")
        self.entry_rem_item_id = ttk.Entry(remove_item_frame)
        self.entry_rem_item_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(remove_item_frame, text="Quantity:").grid(row=1, column=0, sticky="w")
        self.entry_rem_quantity = ttk.Entry(remove_item_frame)
        self.entry_rem_quantity.grid(row=1, column=1, padx=5, pady=5)

        remove_btn = ttk.Button(remove_item_frame, text="Remove from Inventory", command=self._remove_item_from_inventory)
        remove_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Frame to display current inventory
        inventory_list_frame = ttk.LabelFrame(inventory_frame, text="Current Inventory")
        inventory_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        

        self.inventory_tree = ttk.Treeview(  
            inventory_list_frame,
            columns=("ItemID", "Name", "Quantity", "Location"),
            show="headings"
            )
        self.inventory_tree.heading("ItemID", text="Item ID")
        self.inventory_tree.heading("Name", text="Name")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Location", text="Location")

        self.inventory_tree.pack(fill=tk.BOTH, expand=True)

        
        refresh_btn = ttk.Button(inventory_list_frame, text="Refresh", command=self._refresh_inventory_view)
        refresh_btn.pack(pady=5)


    def _add_item_to_inventory(self):
        item_id = self.entry_item_id.get()
        name = self.entry_name.get()
        quantity_str = self.entry_quantity.get()
        location = self.entry_location.get()

        if not (item_id and quantity_str.isdigit()):
            messagebox.showerror("Error", "Invalid input for adding item.")
            return

        quantity = int(quantity_str)
        self.rfid_sensor.simulate_item_arrival(item_id, quantity, name=name, location=location)
        messagebox.showinfo("Success", f"Added {quantity} of {name} to inventory.")
        self._refresh_inventory_view()

    def _remove_item_from_inventory(self):
        item_id = self.entry_rem_item_id.get()
        quantity_str = self.entry_rem_quantity.get()

        if not (item_id and quantity_str.isdigit()):
            messagebox.showerror("Error", "Invalid input for removing item.")
            return

        quantity = int(quantity_str)
        self.rfid_sensor.simulate_item_departure(item_id, quantity)
        messagebox.showinfo("Success", f"Removed {quantity} of {item_id} from inventory.")
        self._refresh_inventory_view()

    def _refresh_inventory_view(self):   
        for row in self.inventory_tree.get_children():
            self.inventory_tree.delete(row)

        items = self.inventory_tracker.get_all_items()
        for item in items:
            self.inventory_tree.insert(
                "",
                tk.END,
                values=(item.item_id, item.name, item.quantity, item.location)
            )


    # ORDERS TAB

    def _create_orders_tab(self):
        orders_frame = ttk.Frame(self.notebook)
        self.notebook.add(orders_frame, text="Orders")

        # Frame for creating orders
        create_order_frame = ttk.LabelFrame(orders_frame, text="Create Order")
        create_order_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(create_order_frame, text="Order ID:").grid(row=0, column=0, sticky="w")
        self.entry_order_id = ttk.Entry(create_order_frame)
        self.entry_order_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(create_order_frame, text="Item ID(s) [Comma-Separated]:").grid(row=1, column=0, sticky="w")
        self.entry_order_item_ids = ttk.Entry(create_order_frame)
        self.entry_order_item_ids.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(create_order_frame, text="Quantities [Comma-Separated]:").grid(row=2, column=0, sticky="w")
        self.entry_order_quantities = ttk.Entry(create_order_frame)
        self.entry_order_quantities.grid(row=2, column=1, padx=5, pady=5)

        create_order_btn = ttk.Button(create_order_frame, text="Create Order", command=self._create_order)
        create_order_btn.grid(row=3, column=0, columnspan=2, pady=10)

        # Frame to display existing orders
        orders_list_frame = ttk.LabelFrame(orders_frame, text="Existing Orders")
        orders_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.orders_tree = ttk.Treeview(orders_list_frame, columns=("Status", "Items"), show="headings")
        self.orders_tree.heading("Status", text="Status")
        self.orders_tree.heading("Items", text="Items")
        self.orders_tree.pack(fill=tk.BOTH, expand=True)

        refresh_orders_btn = ttk.Button(orders_list_frame, text="Refresh", command=self._refresh_orders_view)
        refresh_orders_btn.pack(pady=5)

    def _create_order(self):
        order_id = self.entry_order_id.get()
        item_ids_str = self.entry_order_item_ids.get()
        quantities_str = self.entry_order_quantities.get()

        if not (order_id and item_ids_str and quantities_str):
            messagebox.showerror("Error", "Invalid order input.")
            return

        item_ids = [x.strip() for x in item_ids_str.split(",")]
        quantity_list = [q.strip() for q in quantities_str.split(",")]

        if len(item_ids) != len(quantity_list):
            messagebox.showerror("Error", "Item IDs and quantities must match in length.")
            return

        items_data = []
        for idx, q_str in zip(item_ids, quantity_list):
            if not q_str.isdigit():
                messagebox.showerror("Error", f"Quantity must be a number, got '{q_str}'")
                return
            items_data.append({"item_id": idx, "quantity": int(q_str)})

        self.event_bus.emit(ord_ev.ORDER_CREATED, order_id=order_id, items=items_data)
        messagebox.showinfo("Success", f"Order {order_id} created!")
        self._refresh_orders_view()

    def _refresh_orders_view(self):
        for row in self.orders_tree.get_children():
            self.orders_tree.delete(row)

        orders = self.order_processor.get_all_orders()
        for order in orders:
            item_summary = ", ".join([f"{i['item_id']} x{i['quantity']}" for i in order.items])
            self.orders_tree.insert("", tk.END, values=(order.status, item_summary))

    # ALERTS TAB

    def _create_alerts_tab(self):
        alerts_frame = ttk.Frame(self.notebook)
        self.notebook.add(alerts_frame, text="Alerts")

        # Alert display
        self.alerts_listbox = tk.Listbox(alerts_frame, height=15)
        self.alerts_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons
        alert_button_frame = ttk.Frame(alerts_frame)
        alert_button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        refresh_alerts_btn = ttk.Button(alert_button_frame, text="Refresh Alerts", command=self._refresh_alerts_view)
        refresh_alerts_btn.pack(pady=5)

        resolve_alert_btn = ttk.Button(alert_button_frame, text="Resolve Selected Alert", command=self._resolve_selected_alert)
        resolve_alert_btn.pack(pady=5)

    def _refresh_alerts_view(self):
        self.alerts_listbox.delete(0, tk.END)
        for alert in self.alert_system.get_active_alerts():
            self.alerts_listbox.insert(tk.END, f"{alert['title']}: {alert['message']}")

    def _resolve_selected_alert(self):
        sel = self.alerts_listbox.curselection()
        if not sel:
            return
        alert_text = self.alerts_listbox.get(sel[0])
        # The title is the part before the colon
        split_idx = alert_text.find(":")
        if split_idx > 0:
            title = alert_text[:split_idx].strip()
            self.event_bus.emit(al_ev.ALERT_RESOLVED, title=title)
        self._refresh_alerts_view()

    # AGV / DIAGNOSTICS TAB

    def _create_agv_tab(self):
        agv_frame = ttk.Frame(self.notebook)
        self.notebook.add(agv_frame, text="AGV / Diagnostics")

        # Simple label
        label = ttk.Label(agv_frame, text="AGV events occur automatically when an order is approved.\nCheck console logs for AGV activity.")
        label.pack(padx=10, pady=10)


def main():
    app = WarehouseApp()
    app.mainloop()


if __name__ == "__main__":
    main()
