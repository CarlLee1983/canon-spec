---
id: clr-0001-submitted-order-cancellation
status: resolved
blocks_candidate: false
affected_refs:
  - sales
  - sales.cancel-order
  - sales.order-lifecycle
  - sales.order-cancelled
  - sales.order.cancel-before-submission-only
question: Can a submitted Order be cancelled, and how does Sales determine that it has not been fulfilled?
requested_decisions:
  - Define whether submitted to cancelled is a permitted transition.
  - Define the authoritative evidence required for post-submission reversal.
  - Define the stable failure code and forbidden side effects when cancellation is not permitted.
---

# Submitted Order cancellation

Cancellation, refund, and Return create different business consequences once payment or fulfillment may have occurred.

## Resolution

Human domain review selected draft-only cancellation for Sales 2.0.0. `sales.cancel-order` rejects a submitted Order with `ORDER_ALREADY_SUBMITTED`. Refund and Return are distinct future behaviors requiring Payment, Fulfillment, Shipment, or Returns contracts; `OrderCancelled` does not represent them.
