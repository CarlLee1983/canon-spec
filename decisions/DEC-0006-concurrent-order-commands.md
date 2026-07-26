---
schema_version: "1.0"
kind: decision
id: DEC-0006
version: "1.0.0"
status: draft
title: Concurrent Commands against one Order fail visibly rather than silently
problem: Every Scenario applied one Command to a known Order state, so nothing defined what happens when two Commands reach the same Order without an ordering between them, and an implementation that read a total, added a subtotal, and wrote it back could pass every Scenario while silently losing an Item's contribution.
background: Conformance in this repository is defined by observation at the business boundary rather than by source structure. A condition that different persistence and execution models resolve differently therefore moves the decision out of the contract and into each implementation, which is what the repository exists to prevent.
decision: Declare concurrency a business-visible conflict. At most one of two Commands changing the same Order takes effect, and every other Command fails with ORDER_CONCURRENT_MODIFICATION without state changes or Domain Event occurrences. Which Command takes effect is deliberately unspecified.
rejected_options:
  - Require every implementation to serialize Commands against one Order so that concurrency is invisible at the boundary.
  - Leave concurrency outside the business contract as a delivery concern.
  - State that Sales assumes a single operator per Order without defining what happens when the assumption is violated.
consequences:
  - A lost update becomes a visible, retryable failure instead of a silent arithmetic error, which matters most because the condition is rare and therefore unlikely to be noticed.
  - The stable failure surface of Add Order Item, Submit Order, and Cancel Order grows by one code each, and callers must be prepared to retry.
  - Implementations remain free to choose any conflict-detection strategy, because only the absence of side effects for the Commands that do not take effect is specified.
  - The invariant is filed under the idempotency category because the Aggregate schema's category enum has no concurrency value; the categories describe rule families rather than the full domain vocabulary.
revisit_when:
  - Concurrent Commands against one Order become routine rather than exceptional, which would make retry cost outweigh serialization cost.
  - A reviewed contract introduces multi-Order or cross-Aggregate Commands whose conflict semantics this rule cannot express.
contract_refs:
  - sales
  - sales.order
  - sales.order.concurrent-commands-do-not-interleave
  - sales.order.total-equals-quoted-item-subtotals
  - sales.order.single-order-submitted-event
  - sales.add-order-item
  - sales.submit-order
  - sales.cancel-order
---

# Concurrent Commands against one Order fail visibly rather than silently

The YAML front matter records the trade-off. Normative behavior remains authoritative only in the referenced contracts. Resolves [CLR-0011](../clarifications/CLR-0011-concurrent-order-commands.md).

The reasoning turns on rarity cutting the opposite way from intuition. Because a concurrent collision is expected to be rare, the retry cost of a declared conflict is nearly zero, while the same rarity is exactly what would keep a silent lost update from ever being noticed. Serialization would buy invisibility at the price of an obligation every implementation must carry on every Command.

**Falsified if:** concurrent Commands against one Order become the normal case rather than the exception, or `contracts/sales/aggregates/order.yaml` no longer declares an invariant requiring that Commands which do not take effect leave no state change and no Domain Event occurrence.
