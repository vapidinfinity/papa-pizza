#!/usr/bin/env python3

import uuid
import signal
import sys

from typing import Protocol
from enum import Enum

from termcolor import cprint, colored

class OrderItem(Protocol):
    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price


class Pizza(OrderItem):
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price


class ServiceType(Enum):
    PICKUP = 0
    DELIVERY = 1


# Initialise menu with pizza names and prices
menu: list[OrderItem] = [
    Pizza("Pepperoni", 21.00),
    Pizza("Chicken Supreme", 23.50),
    Pizza("BBQ Meatlovers", 25.50),
    Pizza("Veg Supreme", 22.50),
    Pizza("Hawaiian", 19.00),
    Pizza("Margherita", 18.50),
]

# Initialise order with pizza type and quantity


class Order:
    # Initialise pizza order with pizza type and quantity
    def __init__(self, items: list[OrderItem], service_type: ServiceType):
        self.id = uuid.uuid4()
        self.items = items
        self.quantity = len(items)
        # Calculate the cost of the order based on menu prices
        self._raw_cost = sum(item.price for item in items)
        self.service_type = service_type

        self.total_cost = self._raw_cost
        if service_type == ServiceType.PICKUP:
            pass
        elif service_type == ServiceType.DELIVERY:
            # Apply delivery charge if order is for delivery
            self.total_cost += 8.00
        else:
            raise ValueError("Invalid service type!")

        # Apply discount if total cost (after applying previous discounts) exceeds $100
        if self.total_cost > 100:
            self.total_cost *= 0.9

    @property
    def raw_cost(self):
        return self._raw_cost


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

class CommandParser:
    def __init__(self):
        self.commands = {
            "order": {
                "create": self.create_order,
                "add_item": self.add_order_item,
                "remove": self.remove_order,
                "process": self.process_orders,
            },
            "menu": self.show_menu,
            "summary": self.generate_daily_sales_summary,
            "exit": lambda _: cprint("use 'quit' to exit", "yellow"),
            "help": self.show_help,
            "quit": self.quit,
        }
    
    def _parse_boolean_input(self, prompt: str, handle_invalid: bool = False) -> bool:
        if prompt.lower() in ["y", "yes"]:
            return True
        elif prompt.lower() in ["n", "no"] or not handle_invalid:
            return False
        else:
            cprint("invalid input, please try again.", "red")
            return self._handle_boolean_input(input(prompt), handle_invalid)

    def parse_command(self, command_str: str):
        tokens = command_str.strip().lower().split()
        if not tokens:
            cprint("No command provided.", "red")
            return
        self._execute_command(self.commands, tokens)

    # Recursively executes commands by pathfinding through the command tree.
    def _execute_command(self, current, tokens: list):
        if tokens:
            key = tokens[0]
            # if 'current' is a dict, take the first(next) token as the key and proceed.
            if isinstance(current, dict):
                if key in current:
                    # recursively call the command again
                    return self._execute_command(current[key], tokens[1:])
                else:
                    cprint(f"unknown command: {key}", "red")
                    return
            elif isinstance(current, callable):
                return current(tokens)
            else:
                cprint("invalid command configuration.", "red")
        else:
            # if 'current' is callable, call it passing the remaining tokens.
            if callable(current):
                return current()
            else:
                cprint(f"incomplete command, unable to infer variable {current}.", "red")

    def create_order(self):
        pass

    def remove_order(self):
        pass

    def add_order_item(self, tokens: list):
        pass

    def process_orders(self):
        pass

    def show_menu(self):
        cprint("papa-pizza's famous menu", "")
        for item in menu:
            cprint(f"{item.name}: ${item.price:.2f}", "green")

    def generate_daily_sales_summary(self):
        pass

    def show_help(self):
        print("available commands: ")
        for command in self.commands:
            if isinstance(self.commands[command], dict):
                cprint(f"{command} -> {', '.join(self.commands[command].keys())}", "green")
            else:
                cprint(command, "green")

    def quit(self):
        prompt = input(colored("are you sure you want to exit? (y/N): ", "yellow"))
        if self._parse_boolean_input(prompt, handle_invalid=True):
            cprint("okay, see ya!", "green")
            exit(0)
        else:
            cprint("okay, continuing...", "green")
            return


def main():
    cprint("""
welcome to papa-pizza 🍕,
your local pizza store's ordering backend!
           
by vapidinfinity, aka esi
    """, "green")

    parser = CommandParser()
    while True:
        parser.parse_command(input(colored("\n> ", "blue")))




# Calculate the cost of the order based on menu prices

# Initialise the Papa Pizza system with empty order list and daily sales dictionary

# Add an order to the system

# Remove an order from the system

# Process orders, calculate total cost, apply discounts and delivery charges

    # Update daily sales

# Generate daily sales summary

# Main function to run the program

    # User input menu
    # Add order
    # Remove order
    # Process orders
    # Show menu
    # Generate daily sales summary
    # Exit the program

if __name__ == "__main__":
    main()
