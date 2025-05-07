# Part 1 – Investigation & Design

## 1.1 Investigate

### Project Development Steps and Timeline

| Phase                         | Tasks                                                                                                  | Dependencies     | Timeline (Hours) | Milestone             |
| ----------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------- | ---------------- | --------------------- |
| 1. Requirements & Planning    | • Gather requirements, define scope and constraints<br>• Produce detailed schedule with milestones     | N/A              | 2                | Requirements approved |
| 2. Design & Pseudocode        | • Create structured pseudocode including error paths<br>• Develop trace tables for core and edge cases | Phase 1 complete | 2                | Design reviewed       |
| 3. Implementation Setup       | • Scaffold project, install dependencies, set up repo<br>• Create base classes and interfaces          | Phase 2 complete | 2                | Project scaffolded    |
| 4. Feature Development        | • Implement Order, Menu, Discount, Tracking modules<br>• Prompt loyalty toggle, validation handling    | Phase 3 complete | 6                | Core features working |
| 5. Testing & Debugging        | • Write and run unit/integration tests for edge cases<br>• Validate error handling and workflows       | Phase 4 complete | 1                | All tests passing     |
| 6. Documentation & Evaluation | • Update docs, test plan, UAT, retrospective<br>• Final code review and polish                         | Phase 5 complete | 2                | Submission-ready      |

---

### Problem Outline

**Scope & Constraints**

- CLI-based pizza ordering only; no GUI or web interface
- In-memory session storage (no file/db persistence); stub for future persistence
- Python 3.9+, hostile input expected (invalid commands, out-of-range)

**Purpose & Objectives**

- Provide staff with clear CLI to manage multiple orders
- Enforce pricing rules (discounts, fees, GST) accurately
- Ensure robust validation and user feedback
- Maintain daily sales summary for end-of-day reporting

---

### Problem Description

A detailed explanation of the PapaPizza Ordering System covering objectives, order process, cost rules, tracking and additional features:

1. **Order Workflow**

   - Staff initiates an order via `order create` (pickup/delivery + loyalty status).
   - Items added/removed with `order item add/remove` with full validation (1–10, existing menu).
   - `order process` calculates costs, prompts payment, records into daily sales.
   - `order summary` outputs individual orders and grand total.

2. **Cost Calculation**

   - Raw cost = Σ(price × quantity).
   - 5% discount applied `if cost > 100 or self.has_loyalty_card` or customer has loyalty card.
   - $8 delivery fee `if service_type is DELIVERY`.
   - 10% GST applied to subtotal after discounts & fees.

3. **Tracking & Reporting**

   - Unique `uuid` per order.
   - In-memory daily sales dictionary to accumulate totals.
   - End-of-day summary lists each order ID, amount, and aggregates.

4. **Additional Features**
   - Maximum 10 items per addition; negative or zero quantities rejected.
   - Graceful errors for unknown commands, invalid service types, mismatched switch/remove IDs.
   - Help command, user prompts, inline validation ensure usability.

---

### Requirements List ([MoSCoW](https://en.wikipedia.org/wiki/MoSCoW_method))

#### Must Have (Functional)

<!--ran out of heading levels 💔-->

1. Create new order with prompt for service type and loyalty card status
2. Add/remove pizza items by name and quantity, enforcing max 1–10
3. Validate all menu selections and quantities with clear messages
4. Compute raw cost, discount, delivery fee, and GST correctly
5. Mark orders paid and record totals to daily sales summary
6. Generate end-of-day summary with individual and grand totals

#### Should Have (Functional)

- Help command listing available operations
- Switching between pending orders by ID

#### Could Have (Functional)

- Partial name matching for menu items
- Color-coded CLI output for statuses

#### Non-Functional Requirements

- **Performance:** Order operations <0.1s
- **Reliability:** No crashes on invalid input; stable CLI loop
- **Maintainability:** Modular OOP design, clear naming, docstrings, inline comments

---

## 1.2 Design

### Pseudocode Algorithm

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
        if qty < 1 or qty > 10:
            throw Error("Quantity must be 1-10")
        pizza ← MENU.lookup(name)
        if pizza is null:
            throw Error("Invalid menu item")
        for i in 1..qty:
            currentOrder.items.append(pizza)
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
    loop until exit:
        cmd, args ← promptUser()
        if cmd not in VALID_COMMANDS:
            displayError("Unknown command, type 'help'")
            continue
        switch cmd:
            case "order create":
                service ← parseService(args)
                loyalty ← prompt("Loyalty card? (yes/no)")
                manager.createOrder(service, loyalty == 'yes')
            case "order add":
                if args.length < 2:
                    displayError("Usage: order add <item> <qty>")
                else:
                    manager.addItem(args[0], toInt(args[1]))
            case "order remove":
                ...error checks...
            case "order process":
                manager.processOrder()
            case "order summary":
                manager.generateDailySummary()
            case "help":
                displayHelp()
            case "quit":
                exit loop
```

> **Notes on Structure:**
>
> - Modular classes with clear properties/methods.
> - Use of arrays/lists and dictionary for sales.
> - Control flow: loops, conditionals.

---

### Trace Tables

| Test Case | Items            | Service  | RawCost | Discount | Fee ($8) | Subtotal | GST (10%) | Total With GST |
| --------- | ---------------- | -------- | ------- | -------- | -------- | -------- | --------- | -------------- |
| 1         | 1×Pepperoni      | PICKUP   | 21.00   | 0.00     | 0.00     | 21.00    | 2.10      | 23.10          |
| 2         | 5×Margherita     | DELIVERY | 92.50   | 0.00     | 8.00     | 100.50   | 10.05     | 110.55         |
| 3         | 5×BBQ Meatlovers | DELIVERY | 127.50  | 6.38     | 8.00     | 129.12   | 12.91     | 142.03         |
| 4         | 6×Veg Supreme    | PICKUP   | 135.00  | 6.75     | 0.00     | 128.25   | 12.82     | 141.07         |
| 5         | _none_           | PICKUP   | 0.00    | 0.00     | 0.00     | 0.00     | 0.00      | 0.00           |
| 6         | 10×Hawaiian      | DELIVERY | 190.00  | 9.50     | 8.00     | 188.50   | 18.85     | 207.35         |
| 7 (edge)  | qty=0 or qty=-1  | N/A      | —       | —        | —        | —        | —         | Error          |
| 8 (edge)  | qty=11           | N/A      | —       | —        | —        | —        | —         | Error          |

---
