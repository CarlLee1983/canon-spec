---
id: clr-0008-order-item-identity
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order
  - sales.order.item-must-have-unique-id
  - sales.order.item-additions-do-not-merge
  - sales.add-order-item
  - sales.order-item-added
question: Does an Order Item require stable identity and Product reference, and can equivalent additions merge?
requested_decisions:
  - Define whether each successful addition appends a distinct Item.
  - Define stable Order Item identity and Product reference semantics.
  - Define whether equivalent Items merge.
---

# Order Item identity and merging

The earlier draft could not implement repeated additions consistently without an append-versus-merge decision.

## Resolution

Human domain review selected Sales-allocated stable Order Item IDs and required Product references. Each successful Add Order Item appends one distinct Item; equivalent Products or Quotes do not merge automatically in Sales 2.0.0.
