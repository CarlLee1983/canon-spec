---
id: clr-0007-order-id-allocation
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order.must-have-sales-allocated-unique-id
  - sales.create-order-draft
  - sales.order-draft-created
question: Which party allocates Order ID, and is the identifier supplied to or returned by Create Order Draft?
requested_decisions:
  - Choose the authoritative allocator.
  - Define collision handling.
  - Confirm the Create Order Draft input and result shape.
---

# Order ID allocation

The earlier draft exposed order_id as caller input only to make examples deterministic.

## Resolution

Human domain review selected Sales allocation. Create Order Draft no longer accepts Order ID; Sales allocates it and returns it in the outcome and Event. Allocation collisions are internal retries and do not create a domain failure. Conformance fixtures may predetermine the allocator result for deterministic Scenarios.
