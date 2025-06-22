# import json
# import os
# from datetime import datetime
# from typing import Dict, List
#
#
# class NegativeQuantityError(Exception):
#     pass
#
#
# class NegativePriceError(Exception):
#     pass
#
#
# class ItemNotFoundError(Exception):
#     pass
#
#
# class Inventory:
#     def __init__(self, filename: str | list = "inventory.json"):
#         self.filename = filename
#         self.items: Dict[int, Dict] = {}
#         self.next_id = 1
#         self.load_inventory()
#
#     def _validate_item(self, quantity: int, price: float):
#         if quantity < 0:
#             raise NegativeQuantityError("Quantity cannot be negative")
#         if price < 0:
#             raise NegativePriceError("Price cannot be negative")
#
#     def add_item(self, name: str, quantity: int, price: float) -> int:
#         self._validate_item(quantity, price)
#
#         item_id = self.next_id
#         self.items[item_id] = {
#             "name": name,
#             "quantity": quantity,
#             "price": price,
#             "date_added": datetime.now().isoformat()
#         }
#         self.next_id += 1
#         self.save_inventory()
#         return item_id
#
#     def remove_item(self, item_id: int) -> None:
#         if item_id not in self.items:
#             raise ItemNotFoundError(f"Item with ID {item_id} not found")
#         del self.items[item_id]
#         self.save_inventory()
#
#     def search(self, name: str) -> List[Dict]:
#         return [{"id": id, **item} for id, item in self.items.items()
#                 if name.lower() in item["name"].lower()]
#
#     def low_stock_alert(self, threshold: int) -> List[Dict]:
#         return [{"id": id, **item} for id, item in self.items.items()
#                 if item["quantity"] < threshold]
#
#     def save_inventory(self) -> None:
#         with open(self.filename, 'w') as f:
#             json.dump({
#                 "next_id": self.next_id,
#                 "items": self.items
#             }, f, indent=2)
#
#     def load_inventory(self) -> None:
#         if not os.path.exists(self.filename):
#             return
#
#         try:
#             with open(self.filename, 'r') as f:
#                 data = json.load(f)
#                 self.next_id = data["next_id"]
#                 self.items = {int(k): v for k, v in data["items"].items()}
#         except (json.JSONDecodeError, KeyError):
#             self.next_id = 1
#             self.items = {}
#
#     def get_all_items(self) -> Dict[int, Dict]:
#         return self.items


import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class NegativeQuantityError(Exception):
    pass


class NegativePriceError(Exception):
    pass


class ItemNotFoundError(Exception):
    pass


class Inventory:
    def __init__(self, filename: str = "inventory.json"):
        self.filename = filename
        self.items: Dict[int, Dict] = {}
        self.next_id = 1
        self.load_inventory()

    def _validate_item(self, quantity: int, price: float):
        if quantity < 0:
            raise NegativeQuantityError("Quantity cannot be negative")
        if price < 0:
            raise NegativePriceError("Price cannot be negative")

    def add_item(self, name: str, quantity: int, price: float) -> int:
        self._validate_item(quantity, price)

        item_id = self.next_id
        self.items[item_id] = {
            "name": name,
            "quantity": quantity,
            "price": price,
            "date_added": datetime.now().isoformat()
        }
        self.next_id += 1
        self.save_inventory()
        return item_id

    def remove_item(self, item_id: int) -> None:
        if item_id not in self.items:
            raise ItemNotFoundError(f"Item with ID {item_id} not found")
        del self.items[item_id]
        self.save_inventory()

    def search(self, name: str) -> List[Dict]:
        return [{"id": id, **item} for id, item in self.items.items()
                if name.lower() in item["name"].lower()]

    def low_stock_alert(self, threshold: int) -> List[Dict]:
        return [{"id": id, **item} for id, item in self.items.items()
                if item["quantity"] < threshold]

    def save_inventory(self) -> None:
        with open(self.filename, 'w') as f:
            json.dump({
                "next_id": self.next_id,
                "items": self.items
            }, f, indent=2)

    def load_inventory(self) -> None:
        try:
            if not os.path.exists(self.filename):
                self.items = {}
                self.next_id = 1
                return

            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.items = {int(k): v for k, v in data.get("items", {}).items()}
                self.next_id = data.get("next_id", max(self.items.keys(), default=0) + 1)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error loading inventory: {e}")
            self.items = {}
            self.next_id = 1

    def get_all_items(self) -> Dict[int, Dict]:
        return self.items

    def get_item(self, item_id: int) -> Optional[Dict]:
        return self.items.get(item_id)