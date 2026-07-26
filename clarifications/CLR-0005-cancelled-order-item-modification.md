---
id: clr-0005-cancelled-order-item-modification
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order.cancelled-is-terminal
  - sales.add-order-item
  - sales.order-lifecycle
question: Must Add Order Item against a cancelled Order be rejected, and with which failure code?
requested_decisions:
  - Define whether cancellation freezes Order Items.
  - Define the stable outcome and forbidden side effects.
---

# Cancelled Order Item modification

The earlier invariant made cancelled lifecycle state terminal but did not state whether Items became immutable.

## Resolution

Human domain review selected complete immutability for cancelled Orders. Add Order Item returns `ORDER_CANCELLED`; Items, total, state, and Domain Event occurrences remain unchanged.
