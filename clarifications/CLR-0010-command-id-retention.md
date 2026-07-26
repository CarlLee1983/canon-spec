---
id: clr-0010-command-id-retention
status: open
blocks_candidate: false
affected_refs:
  - sales.order.command-id-idempotency
  - sales.order.command-id-conflict
  - sales.create-order-draft
  - sales.add-order-item
  - sales.submit-order
  - sales.cancel-order
question: For how long must a Sales-wide Command ID remain reserved for replay and conflict detection?
requested_decisions:
  - Decide whether Command ID reservation is unbounded or has a defined business lifetime.
  - Define the outcome of reusing a Command ID whose reservation has lapsed, if lapsing is permitted.
  - Confirm whether reservation lifetime is a business observation or an operational concern.
---

# Command ID reservation lifetime

CLR-0006 established Sales-wide Command ID uniqueness and normalized input comparison, and the Order Aggregate carries both the replay rule and the conflict rule. Neither states how long a Command ID stays reserved.

The question is observable, not operational. If a reservation may lapse, then repeating an old Command ID succeeds as a new Command; if it may not, the same request returns `COMMAND_ID_CONFLICT`. The two answers differ at the Sales boundary for identical input.

This request is marked non-blocking because the strictest reading — reservation never lapses — satisfies every rule as currently written, so an implementation can be built and can pass every pinned Scenario without an answer. The mark is a proposal for the domain reviewer, not a ruling; raising it to blocking is reasonable if unbounded retention is considered an unacceptable obligation to place on every conforming implementation.

## Known interpretations

1. Reservation is unbounded. Every Command ID ever accepted stays reserved for the lifetime of the Sales Context, and every conforming implementation retains that history without limit.
2. Reservation has a defined business lifetime stated in the contract. After it lapses the identifier is free, and reuse is treated as a new Command rather than a conflict.
3. Reservation lifetime is deliberately outside the business contract. The rules describe only the reserved window, and its extent is left to each deployment, accepting that two conforming implementations may answer the same reuse differently.
