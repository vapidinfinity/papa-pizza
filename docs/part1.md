# Part 1 – Investigation & Design

## 1.1 Investigate

### Project Development Steps and Timeline

| Phase                        | Description                                                                                  | Timeline (Hours) |
|------------------------------|----------------------------------------------------------------------------------------------|------------------|
| 1. Investigate & Plan        | • Break down requirements<br>• Produce development schedule<br>• Define objectives & scope   | 2                |
| 2. Algorithm Design          | • Write structured pseudocode<br>• Create trace tables for core logic                        | 2                |
| 3. Implementation (Part 2)   | • Develop Python OOP solution<br>• Apply modular coding, classes, inheritance                | 7              |
| 4. Testing & Documentation   | • Develop test plan<br>• Execute tests and record results                                    | 2                |
| 5. Evaluation & Retrospective| • Conduct user acceptance testing<br>• Reflect on process and code quality                   | 3                |

---

### Problem Outline

**Purpose:**
Build a PapaPizza Ordering System to accept and process pizza orders at a local shop, calculate costs with discounts, surcharges, and GST, and track daily sales.

**Objectives:**
1. Allow order creation (pickup or delivery).
2. Compute individual order totals (menu price, delivery fee, loyalty/volume discounts, GST).
3. Maintain a cumulative daily sales summary.
4. Demonstrate Object-Oriented Programming, modular design, and data structures.

---

### Problem Description

1. **Objective:**
   - Provide a CLI application for staff to create, modify, process, and summarize pizza orders.

2. **Cost Calculation Method:**
   - Sum item prices (quantity × unit price).
   - Apply 5% discount if raw total > $100 or customer has a loyalty card.
   - Add an $8 delivery fee for home deliveries.
   - Apply 10% GST on the amount after discounts and fees.

3. **Order Tracking & Sales:**
   - Store each order with a unique ID, items, service type, and payment status.
   - On payment, record the order total into a daily sales dictionary.
   - Generate end-of-day summary listing each order and grand total.

4. **Additional Features:**
   - Support adding/removing items from an open order.
   - Switch between multiple pending orders.
   - Enforce maximum quantity per item.
   - Graceful handling of invalid input (menus, quantities, indices).

---

### Requirements List

#### Functional Requirements
1. Create new order (pickup or delivery).
2. Add/remove pizza items by name and quantity.
3. Validate menu selections and quantity.
4. Calculate raw cost, apply discounts, fees, and GST.
5. Mark orders as paid and record into daily sales.
6. List all orders with details; generate daily sales summary.

#### Non-Functional Requirements
- **Usability:** Clear CLI prompts, help command, meaningful error messages.
- **Performance:** Fast calculation (< 0.1 s per order).
- **Reliability:** Prevent crashes on invalid input; persist in-memory for session.
- **Maintainability:** Modular code, OOP design, clear naming, comments.

---

## 1.2 Design

### Pseudocode Algorithm (Structured)

```pseudocode
// Data Structures
MENU: array of Pizza{name: string, price: float}
DAILY_SALES: dictionary<UUID, float>

// Class Definitions
class Pizza:
    property name: string
    property price: float

class Order:
    property id: UUID
    property items: list<Pizza>
    property serviceType: enum {PICKUP, DELIVERY}
    property hasLoyaltyCard: boolean
    property paid: boolean
    method rawCost() -> float:
        return sum(item.price for item in items)
    method discountAmount() -> float:
        if rawCost() > 100 OR hasLoyaltyCard then
            return rawCost() * 0.05
        else
            return 0
    method deliveryFee() -> float:
        if serviceType == DELIVERY then return 8 else return 0
    method totalBeforeGST() -> float:
        return rawCost() - discountAmount() + deliveryFee()
    method totalWithGST() -> float:
        return totalBeforeGST() * 1.10

class OrderManager:
    property orders: list<Order>
    property currentOrder: Order?
    property dailySales: dictionary<UUID, float>
    method createOrder(serviceType, hasLoyalty):
        order ← new Order(uuid(), [], serviceType, hasLoyalty, false)
        orders.append(order)
        currentOrder ← order
    method addItem(pizzaName, qty):
        pizza ← find MENU by name
        for i in 1..qty do currentOrder.items.append(pizza)
    method removeItem(pizzaName, qty):
        // remove up to qty occurrences
    method processOrder():
        display totalBeforeGST and totalWithGST
        if confirmPayment() then
            currentOrder.paid ← true
            dailySales[currentOrder.id] ← currentOrder.totalWithGST()
    method generateDailySummary():
        for each (id, amount) in dailySales:
            print id, amount
        print sum of dailySales.values()

// Main REPL
function main():
    manager ← new OrderManager()
    loop:
        cmd ← promptUser()
        switch cmd:
            case "order create": ...
            case "order item add": ...
            ...
            case "order summary": manager.generateDailySummary()
            case "quit": exit()
```

> **Notes on Structure:**
> - Modular classes with clear properties/methods.
> - Use of arrays/lists and dictionary for sales.
> - Control flow: loops, conditionals.

---

### Trace Tables

Test core calculations for several scenarios.

| Test Case | Items                     | Service  | RawCost | Discount (5%) | Fee ($8) | Subtotal |
|-----------|---------------------------|----------|---------|---------------|----------|----------|
| 1         | 1×Pepperoni ($21.00)      | PICKUP   | 21.00   | 0.00          | 0.00     | 21.00    |
| 2         | 5×Margherita ($92.50)     | DELIVERY | 92.50   | 0.00          | 8.00     | 100.50   |
| 3         | 5×BBQ ($127.50)           | DELIVERY | 127.50  | 6.38          | 8.00     | 129.12   |
| 4         | 6×VegSupreme ($135.00)    | PICKUP   | 135.00  | 6.75          | 0.00     | 128.25   |
| 5         | *no items*                | PICKUP   | 0.00    | 0.00          | 0.00     | 0.00     |