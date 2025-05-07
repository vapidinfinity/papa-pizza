# Part 3 – Testing, Evaluation & Retrospective

## 3.1 Test Plan

| Test ID | Input Scenario                                                                                           | Expected Output                                                                                      | Actual Result | Pass/Fail |
|---------|----------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|---------------|-----------|
| 1     | Create pickup order; add 1×Pepperoni; process without loyalty                                             | “Total: \$23.10... Paid!”; DailySales contains order UUID→23.10                                        | as expected   | Pass      |
| 2     | Create delivery order; add 5×Margherita; no loyalty                                                        | “Total: \$110.55... Paid!”; DailySales UUID→110.55                                                     | as expected   | Pass      |
| 3     | Create delivery order; add 6×BBQ; loyalty card=true                                                        | Discount applies (5%), fee applies; GST applied                                                        | as expected   | Pass      |
| 4     | Attempt to add “UnknownPizza”; invalid quantity “-1”; remove non-existent item                            | Graceful error messages (“invalid menu item”, “invalid quantity”, “item not in current order”)        | as expected   | Pass      |
| 5     | No items in order; process order                                                                          | “Total: \$0.00...”; allowed or blocked by design; dailySales updates or no-sales message              | as expected   | Pass      |
| TP6     | Switch between multiple pending orders; ensure currentOrder updates                                        | Current order UUID changes and subsequent add/remove affect correct order                            | as expected   | Pass      |
| TP7     | Generate daily sales summary after several paid orders                                                    | Prints each order’s UUID and amount; prints grand total                                              | as expected   | Pass      |
| TP8     | Edge: add 11×VegSupreme (above max 10)                                                                     | Error “maximum quantity is 10 at a time”; no items added                                              | as expected   | Pass      |

> **Notes:**
> - Each scenario tests functional requirements, input validation, discount logic, delivery fees, GST application, and CLI behavior.
> - Type checks (isdigit), range checks (1–10), and error handling are verified.

---

## 3.2 User Acceptance Testing & Evaluation

### Requirement Coverage

| Requirement                               | Met? | Comments                                                  |
|-------------------------------------------|------|-----------------------------------------------------------|
| Order creation (pickup/delivery)          | ✔    | Both options available                                    |
| Add/remove items                         | ✔    | Quantity and menu validation works                       |
| Cost calculation (discounts, fees, GST)  | ✔    | Matches specification; edge cases tested                 |
| Sales tracking & summary                 | ✔    | DailySales dictionary updates and summary generation     |
| CLI usability & error messages           | ✔    | Clear prompts and descriptive error feedback             |

### User Experience

- **Strengths:**
  • Intuitive CLI with `help` command<br>
  • Color-coded messages (success, warnings, errors)<br>
  • Ability to manage multiple open orders

- **Areas for Improvement:**
  • Persist orders across sessions (file or database)<br>
  • Improved input parsing (e.g., partial name matching)<br>
  • Automated tests (unit/integration)

### Known Bugs & Limitations

- **Missing Loyalty Toggle:** Loyalty card flag must be set at order creation; not prompted in CLI.
- **No Persistent Storage:** All data lost on exit.
- **GST Calculation Unit Tests:** No separate unit tests for tax logic.

**Impact:**
These do not block core functionality but affect robustness and real-world deployment.

---

## 3.3 Retrospective

### Development Process Reflection

- **What Worked Well:**
  • OOP design allowed clear separation of concerns.
  • Modular commands simplified REPL implementation.
  • Use of Python’s `typing` and `Enum` enhanced readability.

- **What Didn’t Work Well:**
  • Underestimated complexity of tracking loyalty membership.

- **Improvements for Next Time:**
  • Begin with detailed pseudocode before coding — I created and iterated the code. and then created the pseudocode retroactively.<br>
  • Implement file-based persistence.<br>
  • Write unit tests in parallel with features.

### Future Impacts

A mature version could integrate a database, GUI/​web front-end, and automated CI pipeline with unit tests to support continuous development and deployment.

---

**Sources**
- ATAR Computer Science Unit 3–4 Syllabus
- `python3` Documentation (dataclasses, `typing`, `enum`)
- Termcolor package documentation
- Various StackOverflow Threads
- w3schools