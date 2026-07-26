---
id: clr-0004-customer-authority
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order.must-belong-to-verified-customer
  - sales.create-order-draft
  - customer.verify-order-authority
question: Must the Customer exist, and must the actor be authorized to create the Order for that Customer?
requested_decisions:
  - Define the source that establishes Customer existence.
  - Define actor-to-Customer authorization semantics.
  - Define stable failure codes and forbidden side effects.
---

# Customer existence and authority

Association alone does not establish that the Customer exists or that the actor may act for it.

## Resolution

Human domain review selected Customer as the authority. Before creating an Order, Sales invokes `customer.verify-order-authority`; missing Customer and unauthorized actor decisions map to `CUSTOMER_NOT_FOUND` and `CUSTOMER_NOT_AUTHORIZED` with no Sales side effects.
