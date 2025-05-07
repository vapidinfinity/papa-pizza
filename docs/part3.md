# Part 3 – Testing, Evaluation & Retrospective

## 3.1 Test Plan

| Test ID | Input Scenario                                                                 | Expected Output                                                                                | Actual Result | Pass/Fail |
| ------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ------------- | --------- |
| 1       | Create pickup order; add 1×Pepperoni; process without loyalty                  | “Total: \$23.10... Paid!”; DailySales contains order UUID→23.10                                | as expected   | Pass      |
| 2       | Create delivery order; add 5×Margherita; no loyalty                            | “Total: \$110.55... Paid!”; DailySales UUID→110.55                                             | as expected   | Pass      |
| 3       | Create delivery order; add 6×BBQ; loyalty card=true                            | Discount applies (5%), fee applies; GST applied                                                | as expected   | Pass      |
| 4       | Attempt to add “UnknownPizza”; invalid quantity “-1”; remove non-existent item | Graceful error messages (“invalid menu item”, “invalid quantity”, “item not in current order”) | as expected   | Pass      |
| 5       | No items in order; process order                                               | “Total: \$0.00...”; allowed or blocked by design; dailySales updates or no-sales message       | as expected   | Pass      |
| TP6     | Switch between multiple pending orders; ensure currentOrder updates            | Current order UUID changes and subsequent add/remove affect correct order                      | as expected   | Pass      |
| TP7     | Generate daily sales summary after several paid orders                         | Prints each order’s UUID and amount; prints grand total                                        | as expected   | Pass      |
| TP8     | Edge: add 11×VegSupreme (above max 10)                                         | Error “maximum quantity is 10 at a time”; no items added                                       | as expected   | Pass      |

> **Notes:**
>
> - Each scenario tests functional requirements, input validation, discount logic, delivery fees, GST application, and CLI behavior.
> - Type checks (isdigit), range checks (1–10), and error handling are verified.

---

## 3.2 User Acceptance Testing & Evaluation

### Requirement Coverage

| Requirement                             | Fulfilled? | Comments                                             |
| --------------------------------------- | ---------- | ---------------------------------------------------- |
| Order creation (pickup/delivery)        | ✔          | Both options available                               |
| Add/remove items                        | ✔          | Quantity and menu validation works                   |
| Cost calculation (discounts, fees, GST) | ✔          | Matches specification; edge cases tested             |
| Sales tracking & summary                | ✔          | DailySales dictionary updates and summary generation |
| CLI usability & error messages          | ✔          | Clear prompts and descriptive error feedback         |

### User Feedback Summary

- "The help command guided me quickly through all operations," – anonymous
- "Error messages clearly indicate the issue, but could be more concise," – anonymous
- "Switching between orders was intuitive; however, numeric IDs are hard to remember," – anonymous

### UX Analysis and Satisfaction

| Aspect               | Rating (out of 5) | Comments                                                               |
| -------------------- | ----------------- | ---------------------------------------------------------------------- |
| Learnability         | 5                 | Quick onboarding with `help`, intuitive prompts,                       |
| Efficiency           | 4                 | Core workflows <0.1s, but REPL design adds extra input.                |
| Error Recovery       | 4                 | Handles errors well, but by design will not reattempt the failed task. |
| Overall Satisfaction | 5                 | does the job well above what is required of it.                        |

### Requirement Mapping

| Requirement                             | Met? | UX Impact                                            |
| --------------------------------------- | ---- | ---------------------------------------------------- |
| Order creation (pickup/delivery)        | ✔    | Smooth flow; loyalty prompt clear.                   |
| Add/remove items                        | ✔    | Minor annoyance repeating invalid entries.           |
| Cost calculation (discounts, fees, GST) | ✔    | Transparent breakdown; GST shown in summary.         |
| Sales tracking & summary                | ✔    | Summary clear, but UUIDs unwieldy; consider aliases. |
| CLI usability & error messages          | ✔    | Effective but could use color-coded severity levels. |

---

## 3.3 Known Bugs & Improvements

- **Loyalty Prompt Placement** (Medium): Loyalty card question appears after service type. Suggest: include in `order create` alias parameters or default config.
- **No Persistence** (High): All data lost on exit. Recommend: file-based JSON or SQLite storage layer for orders/daily sales.
- **UUID Usability** (Low): Long UUIDs hard to key in. Suggest: generate sequential numeric IDs or short hashes for user ease.
- **Tax Unit Tests Missing** (Low): No isolated tests for discount/GST logic. Add unit tests using `unittest` or `pytest`.
- **CLI Autocomplete** (Medium): Partial name matching or tab completion would speed input. Evaluate libraries like `readline`.

**Impact Analysis & Next Steps:**

- Persistence is critical for real-world use; prioritize File/db storage in Phase 2.
- Refactoring IDs will improve UX; schedule task in backlog.
- Add unit tests early in next sprint to catch logic regressions.

---

## 3.4 Retrospective

**Development Process Reflection**

- Time estimates for feature development were within 10% accuracy, but testing time was underestimated by 1 day.
- Modular design facilitated rapid feature additions; code review identified naming inconsistencies early.
- Continuous feedback from peer testers improved error messaging and edge-case coverage.

**Lessons Learned**

- Write unit tests in parallel with development to validate logic immediately.
- Early user prototypes (like pseudocode) would reveal UX gaps before coding.

**Future Technical Directions**

- Implement JSON or SQLite persistence module to support session saving and resume capabilities.
- Explore a simple web front-end (`django`) to complement CLI for end-users.

---

**Sources**

- ATAR Computer Science Unit 3–4 Syllabus
- `python3` Documentation (dataclasses, `typing`, `enum`)
- `termcolor` package documentation
- Various StackOverflow Threads
- GeeksForGeeks
- W3Schools
