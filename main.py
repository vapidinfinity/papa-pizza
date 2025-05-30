#!/usr/bin/env python3.13

#  _ __   __ _ _ __   __ _ 
# | '_ \ / _` | '_ \ / _` |
# | |_) | (_| | |_) | (_| |
# | .__/ \__,_| .__/ \__,_|
# |_|__ (_)___|_|____ _    
# | '_ \| |_  /_  / _` |   
# | |_) | |/ / / / (_| |   
# | .__/|_/___/___\__,_| 🍕 
# |_|              by esi ✦         

import signal
import sys

from typing import Callable
from abc import ABC, abstractmethod
from enum import Enum
import inspect

import uuid

from termcolor import cprint, colored
from colorama import just_fix_windows_console as enable_windows_ansi_interpretation

# fix windows terminal misinterpreting ANSI escape sequences
enable_windows_ansi_interpretation()

# establish a base class for order items
class OrderItem(ABC):
    """Abstract base class for items that can be ordered."""
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

# pizza implementation uses `OrderItem` as its base class
class Pizza(OrderItem):
    """Concrete OrderItem representing a pizza with a name and a price."""
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    # implement OrderItem abstract methods without setters -- this will ensure immutability
    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price


class ServiceType(Enum):
    """Enumeration of service types: pickup or delivery."""
    PICKUP = 0
    DELIVERY = 1

# Initialise menu with pizza names and prices
# Get the price of a pizza from the menu
menu: list[OrderItem] = [
    Pizza("Pepperoni", 21.00),
    Pizza("Chicken Supreme", 23.50),
    Pizza("BBQ Meatlovers", 25.50),
    Pizza("Veg Supreme", 22.50),
    Pizza("Hawaiian", 19.00),
    Pizza("Margherita", 18.50),
]

class Order:
    """Represents a customer order, its items, service type, discounts, and payment status."""
    def __init__(self, items: list[OrderItem], service_type: ServiceType, has_loyalty_card: bool = False):
        self.uuid = uuid.uuid4()
        self.items = items
        self.service_type = service_type
        self.has_loyalty_card = has_loyalty_card
        self.is_discounted = False
        self.paid = False

    # Calculate the cost of the order based on menu prices
    @property
    def raw_cost(self):
        """Return sum of item prices before discounts, fees, or taxes."""
        return sum(item.price for item in self.items)
    
    # Calculate total cost, apply discounts and delivery charges
    @property
    def total_cost(self):
        """Compute total cost including discounts, delivery fee, and GST."""
        cost = self.raw_cost
        # Apply 5% discount for loyalty or bulk orders > $100
        if cost > 100 or self.has_loyalty_card:
            cost *= 0.95
            self.is_discounted = True

        if self.service_type is ServiceType.PICKUP:
            pass
        elif self.service_type is ServiceType.DELIVERY:
            # Apply delivery charge if order is for delivery
            cost += 8.00
        else:
            raise ValueError("Invalid service type!")

        return cost * 1.1 # add 10% GST
    
class OrderManager:
    """Manage creation, modification, processing, and listing of multiple orders."""
    def __init__(self):
        # initialise the Papa Pizza system with empty order list and daily sales dictionary
        self.orders: list[Order] = []
        self.current_order_uuid = None
        self.daily_sales = {}

    def print_order(self, order, with_index: bool = True):
        """Display details of a single order, optionally numbered."""
        if with_index:
            try:
                index = self.orders.index(order) + 1 if with_index else None
            except ValueError:
                cprint("order not found in the list.", "red")
                return

            cprint(f"{index}. {order.service_type.name.lower()} order {order.uuid}:", "green")
        else:
            cprint(f"{order.service_type.name.lower()} order {order.uuid}:", "green")

        print("\t" + f"items: {', '.join([item.name for item in order.items]) or 'none'}")
        print("\t" + f"service type: {order.service_type.name}")
        print("\t" + f"total cost: ${order.total_cost:.2f}")
        print("\t" + f"paid: {'yes' if order.paid else 'no'}")

    def list_orders(self):
        """List all orders or report none exist."""
        if not self.orders:
            cprint("no orders found :(", "red")
            return

        for order in self.orders:
            self.print_order(order)

    def _get_order_by_uuid(self, order_uuid: uuid.UUID) -> Order:  # changed parameter type from str to uuid.UUID
        return next((order for order in self.orders if order.uuid == order_uuid), None)

    # Add an order to the system
    def create_order(self, type: str | None = None):
        """Interactively prompt to create a new order with service type and loyalty flag."""
        # prompt service type
        if type is None:
            type = input("Order type? (pickup/delivery): ").strip().lower()

        try:
            service_type = ServiceType[type.upper()]
        except:
            cprint("invalid service type!", "red")
            return
        
        # prompt loyalty card status
        prompt = input("does customer have a loyalty card? (y/N): ").strip().lower()
        has_loyalty = parse_boolean_input(prompt, handle_invalid=True)

        order = self._create_order([], service_type, has_loyalty)
        if len(self.orders) > 1:
            prompt = input("do you want to switch to this order? (y/N): ")
            if parse_boolean_input(prompt, handle_invalid=False):
                self._switch_order(self.orders.index(order) + 1)
        else:
            self._switch_order(self.orders.index(order) + 1)

    def _create_order(self, items: list[OrderItem], service_type: ServiceType, has_loyalty: bool) -> Order:
        """Instantiate and register a new Order internally."""
        order = Order(items, service_type, has_loyalty)
        self.orders.append(order)
        cprint(f"order {order.uuid} created successfully!", "green")
        return order


    # Remove an order from the system
    def remove_order(self):
        """Interactively remove an order by its list index."""
        self.list_orders()
        prompt = input(f"which order would you like to remove? (1-{len(self.orders)}):")

        if not prompt.isdigit():
            cprint("invalid order index", "red")
            return
        
        order_index = int(prompt)
        if order_index < 1 or order_index > len(self.orders):
            cprint("invalid order index", "red")
            return
        
        self._remove_order(order_index)

    def _remove_order(self, order_index: int):
        """Remove an order by its adjusted index and clear current selection if needed."""
        # correct the order index to match the list index
        true_order_index = order_index - 1
        if self.current_order_uuid == self.orders[true_order_index].uuid:
            self.current_order_uuid = None
        
        self.orders.pop(true_order_index)
        cprint(f"order {order_index} removed successfully!", "green")


    # switch order focus    
    def switch_order(self):
        """Interactively switch the current focus to an existing order."""
        self.list_orders()
        prompt = input(f"which order would you like to switch to? (1-{len(self.orders)}): ")

        if not prompt.isdigit() or int(prompt) < 1 or int(prompt) > len(self.orders):
            cprint("invalid order index", "red")
            return

        order_index = int(prompt)
        self._switch_order(order_index)

    def _switch_order(self, order_index: int) -> Order | None:
        """Switch focus internally to the chosen order index."""
        true_order_index = order_index - 1
        if 0 <= true_order_index < len(self.orders):
            new_order = self.orders[true_order_index]
            if self.current_order_uuid == new_order.uuid:
                cprint("this is already your current order!", "yellow")
                return None
            
            self.current_order_uuid = new_order.uuid
            cprint(f"switched to order {new_order.uuid}", "green")
            return new_order
        else:
            cprint("invalid order id; switch will not occur.", "red")
            return None

    def _check_current_order(self):
        """Ensure there's a valid, unpaid current order or prompt next steps."""
        order = self._get_order_by_uuid(self.current_order_uuid)
        if order is None:
            cprint("no current order selected.", "red")
            if self.orders:
                prompt = input("would you like to select an order? (y/N): ")
                if parse_boolean_input(prompt, handle_invalid=True):
                    self.switch_order()
                    return
            else:
                prompt = input("would you like to create an order? (y/N): ")
                if parse_boolean_input(prompt, handle_invalid=True):
                    self.create_order()
                    return
        else:
            if order.paid:
                cprint("this order has already been paid for.", "red")
                prompt = input("would you like to switch to a different order? (y/N): ")
                if parse_boolean_input(prompt, handle_invalid=True):
                    self.switch_order()
                    return
                
    
    def add_order_item(self, item: str | None = None, quantity: str | None = "1"):
        """Add a menu item in given quantity to the current order."""
        # Prompt for item if not provided
        if item is None:
            item = input("enter the name of the menu item you'd like to add (or type 'menu' to review the options): ").strip().lower()

        item = next((menu_item for menu_item in menu if menu_item.name.lower() == item), None)

        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity < 1:
                raise ValueError
        except:
            prompt = input("Enter a valid quantity (1 or more): ")
            if not prompt.isdigit() or int(prompt) < 1:
                cprint("invalid quantity", "red")
                return
            quantity = int(prompt)

        # check for maximum quantity
        if quantity > 10:
            cprint("maximum quantity is 10 at a time. try adding items again to add more.", "red")
            return

        for _ in range(quantity):
            self._add_order_item(item)

    def _add_order_item(self, item: OrderItem):
        """Helper to append a single OrderItem to the current order."""
        self._check_current_order()

        order = self._get_order_by_uuid(self.current_order_uuid)
        if order is None:
            cprint("order not found.", "red")
            return

        order.items.append(item)
        cprint(f"added {item.name} to order {order.uuid}", "green")


    def remove_order_item(self):
        """Interactively remove a given quantity of a menu item from the current order."""
        prompt = input("which menu item would you like to remove?: ")
        prompt = prompt.strip().lower()

        item = next((item for item in menu if item.name.lower() == prompt), None)
        if item is None:
            cprint("invalid menu item", "red")
            return
        
        prompt = input("how many of this item would you like to remove? ")
        if not prompt.isdigit() or int(prompt) < 1:
            cprint("invalid quantity", "red")
            return
        quantity = int(prompt)

        for _ in range(quantity):
            self._remove_order_item(item)

    def _remove_order_item(self, item: OrderItem):
        """Helper to remove a single OrderItem from the current order."""
        self._check_current_order()

        order = self._get_order_by_uuid(self.current_order_uuid)
        if item in order.items:
            order.items.remove(item)
            cprint(f"removed {item.name} from order {order.uuid}", "green")
        else:
            cprint(f"{item.name} not in current order.", "red")


    # Process orders
    def process_order(self):
        """Process payment for the current order, apply extras, and record it in daily sales."""
        self._check_current_order()

        order = self._get_order_by_uuid(self.current_order_uuid)
        if order is None:
            cprint("order not found.", "red")
            return

        if order.paid:
            cprint("order already paid.", "red")
            return

        extras = []
        # constants so i can be lazy and hardcode it
        if order.is_discounted:
            extras.append(f"a 10% discount")
        if order.service_type is ServiceType.DELIVERY:
            extras.append(f"$8.00 delivery")

        extras.append(f"10% GST")

        # smoothly concatenate the extras!
        extras_str = f", including {' and '.join(extras)}" if extras else ""
        print(f"the total for order {order.uuid} is ${order.total_cost:.2f}{extras_str}.")
        prompt = input(f"would you like to pay now? (y/N): ")
        if parse_boolean_input(prompt, handle_invalid=True):
            order.paid = True
            cprint(f"order {order.uuid} paid successfully!", "green")
            # Update daily sales
            self.daily_sales[order.uuid] = order.total_cost
            cprint(f"order {order.uuid} has been added to the daily sales summary.", "green")
        else:
            cprint("payment cancelled", "yellow")


    # Generate daily sales summary
    def generate_daily_sales_summary(self):
        """Print each paid order’s total and the grand total sales for the day."""
        if not self.daily_sales:
            cprint("no sales to summarise :(", "red")
            return

        for order_uuid, total_cost in self.daily_sales.items():
            print(f"order {order_uuid}: {colored(f"${total_cost:.2f}", "green")}")

        total_sales = sum(self.daily_sales.values())
        cprint(f"total sales for today: ${total_sales:.2f}", "green")

        cprint("thank you for using papa-pizza!", "green")

def parse_boolean_input(prompt: str, handle_invalid: bool = False) -> bool:
    """Parse 'y/n' input, returning True for yes. Invalid only retried if handle_invalid=True."""
    if prompt.lower() in ["y", "yes"]:
        return True
    elif prompt.lower() in ["n", "no"] or not handle_invalid:
        return False
    else:
        cprint("invalid input, please try again.", "red")
        return False
class Command:
    """Bind a CLI command name to a function and its description."""
    def __init__(self, name: str, function: Callable, description: str):
        self.name = name
        self.__function__ = function
        self.description = description

    def execute(self, tokens: list[str], required_count=None):
        """Validate argument count then invoke the bound function."""
        signature = inspect.signature(self.__function__)
        params = list(signature.parameters.values())

        #
        required_param_count = sum(
            param.default == inspect.Parameter.empty and param.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY)
            for param in params
        )

        # Validate token count
        if not required_param_count <= len(tokens) <= len(params):
            cprint(f"invalid number of arguments for command '{self.name}' — (expected {required_count}-{len(params)}, got {len(tokens)})", "red")
            return None

        return self.__function__(*tokens)

class CommandParser:
    """Parse user input, map to commands, and run them in a REPL."""
    def __init__(self):
        # Register basic commands
        self.commands = [
            Command("help", self.show_help, "Display this help message."),
            Command("h", self.show_help, "Alias for 'help'."),
            Command("quit", self.quit, "Exit the program."),
            Command("exit", lambda: cprint("use quit to exit", "yellow"), "Alias for 'quit'."),
        ]

    def parse_and_execute(self, input_str):
        """Match the input string to a registered command and execute."""
        tokens = input_str.strip().split()
        
        for command in self.commands:
            name_parts = command.name.split()
            # if the command name matches the input, omit the matching indexes
            if tokens[:len(name_parts)] == name_parts:
                args = tokens[len(name_parts):]
                return command.execute(args)
        
        cprint("unknown command. type 'help'.", "red")
        return None

    def show_help(self):
        """Display help with all available command names and descriptions."""
        cprint("available commands:", "green", attrs=["bold"])
        for cmd in self.commands:
            signature = inspect.signature(cmd.__function__)

            # format params
            params = " ".join(
                f"<{param} {value.default if value.default is not None else '(optional)'}>"
                for param, value in signature.parameters.items()
            )

            # concatenate command name and params
            cmd_with_params = f"{colored(cmd.name, 'blue')} {colored(params, 'cyan')}"

            print(f"{cmd_with_params.ljust(max(len(cmd.name) for cmd in self.commands) + 50)}  {cmd.description}")

    # Exit the program
    @staticmethod
    def quit():
        """Prompt for confirmation and exit the application on yes."""
        prompt = input(colored("are you sure you want to quit? (y/N): ", "yellow"))
        if parse_boolean_input(prompt, handle_invalid=False):
            cprint("okay, see ya!", "green")
            sys.exit(0)
        else:
            cprint("okay, continuing...", "green")
            return

    # User input menu
    def start_repl(self):
        """Begin the interactive prompt loop until quit."""
        while True:
            user_input = input(colored("\n> ", "blue")).strip()
            if user_input:
                self.parse_and_execute(user_input)

class Application:
    """Wire together CLI commands with the OrderManager and start the REPL."""
    def __init__(self, *args):
        self.order_manager = OrderManager()

        parser = CommandParser()
        parser.commands.append(Command("menu", self.show_menu, "Show the menu"))

        parser.commands.append(Command("order create", self.order_manager.create_order, "Add an order"))
        parser.commands.append(Command("order remove", self.order_manager.remove_order, "Remove an order"))
        parser.commands.append(Command("order list", self.order_manager.list_orders, "List all orders"))
        parser.commands.append(Command("order process", self.order_manager.process_order, "Process an order"))
        # parser.commands.append(Command("order process all", self.order_manager.process_all_orders, "Process all available orders"))
        parser.commands.append(Command("order switch", self.order_manager.switch_order, "Switch to a different order"))

        parser.commands.append(Command("order item add", self.order_manager.add_order_item, "Add an item to the current order"))
        parser.commands.append(Command("order item remove", self.order_manager.remove_order_item, "Remove an item from the current order"))

        parser.commands.append(Command("order summary", self.order_manager.generate_daily_sales_summary, "Generate daily sales summary"))

        cprint("""
welcome to papa-pizza 🍕,
your local pizza store's ordering backend!
           
by vapidinfinity, aka esi
    """, "green", attrs=["bold"])

        print("""this is a simple command line interface for ordering pizza.
for more information, type 'help' or 'h' at any time.
to exit the program, type 'quit' or 'exit'.""")

        if args:
            parser.parse_and_execute(" ".join(args))

        parser.start_repl()

    # Show menu
    @staticmethod
    def show_menu():
        """Print Papa Pizza’s menu of available items."""
        cprint("papa-pizza's famous menu", None, attrs=["bold"])

        current_item = None
        for item in menu:
            if type(item) is not type(current_item):
                current_item = item
                cprint(f"\n{type(item).__name__}:", "green", attrs=["bold"])
                
            cprint(f"{item.name}: ${item.price:.2f}", "green")
            
# Main function to run the program
def main():
    """Entry point: instantiate Application with optional CLI args."""
    args = sys.argv[1:]
    Application(*args)

class SignalHandler:
    """Handle system SIGINT (Ctrl+C) to remind user to use 'quit'."""
    # signal handler to handle ctrl+c
    @staticmethod
    def sigint(_, __):
        """Custom SIGINT handler printing a warning then exiting."""
        cprint("\n" + "next time, use quit!", "yellow")
        sys.exit(0)

# register signal handler for (ctrl+c) SIGINT
signal.signal(signal.SIGINT, SignalHandler.sigint)

if __name__ == "__main__":
    main()