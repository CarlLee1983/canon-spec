---
id: clr-0011-concurrent-order-commands
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order
  - sales.order-lifecycle
  - sales.add-order-item
  - sales.submit-order
  - sales.cancel-order
  - sales.order.total-equals-quoted-item-subtotals
  - sales.order.item-must-have-unique-id
  - sales.order.single-order-submitted-event
question: What outcome is required when two Commands targeting the same Order are processed concurrently?
requested_decisions:
  - Decide whether concurrent Commands against one Order are serialized as a business rule or left undefined.
  - Define the outcome of the losing Command when two Commands would both change the same Order.
  - Confirm whether Order total and Order Item identity remain correct under concurrent Add Order Item Commands.
---

# Concurrent Commands against one Order

Every Scenario applies exactly one Command to a known Order state, so the contracts describe sequential behavior only. Nothing states what happens when two Commands reach the same Order without an ordering between them.

Several rules become ambiguous in that situation. Two concurrent Add Order Item Commands must each append a distinct Item and must leave the Order total equal to the sum of authoritative subtotals; an implementation that reads the total, adds a subtotal, and writes it back can satisfy every pinned Scenario and still lose one Item's contribution. A concurrent Submit Order and Cancel Order pair can reach either terminal state, and both orderings are consistent with the state machine read in isolation.

The question matters more here than in a single-implementation project. The repository defines conformance as observation at the business boundary, so a condition that different persistence and execution models resolve differently moves the decision out of the contract and into each implementation, which is what this repository exists to prevent.

## Known interpretations

1. Commands against one Order are serialized as a business rule. Concurrency is invisible at the boundary, and every conforming implementation produces a result identical to some sequential order of the same Commands.
2. Concurrency is a declared conflict. The losing Command receives a stable failure code, leaving state and Domain Event occurrences unchanged, and the caller decides whether to retry.
3. Concurrency is outside the business contract. The rules describe one Command at a time, and simultaneous arrival is a delivery concern each implementation settles for itself.

## Resolution

Human domain review selected interpretation 2. Concurrent Commands against one Order are expected to be rare rather than routine, which makes a declared conflict cheaper than a serialization obligation placed on every implementation, and far safer than leaving the condition undefined.

`sales.order.concurrent-commands-do-not-interleave` requires that at most one of two Commands changing the same Order takes effect. Every other Command fails with `ORDER_CONCURRENT_MODIFICATION` and creates no state change and no Domain Event occurrence, so a lost update becomes a visible, retryable failure instead of a silent one. Which Command wins is deliberately not specified; only the absence of side effects for the others is.

See [DEC-0006](../decisions/DEC-0006-concurrent-order-commands.md).
