---
schema_version: "1.0"
kind: decision
id: DEC-0004
version: "1.0.0"
status: draft
title: Pre-submission cancellation is distinct from refund and Return
problem: Treating every post-submission reversal as Order cancellation would hide payment, fulfillment, shipment, refund, and Return consequences inside one Sales state transition.
background: A submitted Order may already be paid or fulfilled, while those facts are owned outside Sales and are not present in the current contract set.
decision: Limit sales.cancel-order to draft Orders; a submitted Order remains submitted in Sales and post-submission compensation requires future contracts owned with Payment, Fulfillment, Shipment, or Returns.
rejected_options:
  - Allow submitted to cancelled without checking external consequences.
  - Treat OrderCancelled as equivalent to refunded or returned.
  - Copy payment and fulfillment state into Sales without cross-context contracts.
consequences:
  - OrderCancelled has an unambiguous pre-submission meaning.
  - Cancel Order returns ORDER_ALREADY_SUBMITTED for submitted Orders.
  - Future refund or Return work must introduce explicit contracts rather than extending cancellation by assumption.
revisit_when:
  - Reviewed Payment, Fulfillment, Shipment, or Returns contracts define a post-submission compensation workflow.
contract_refs:
  - sales
  - sales.order
  - sales.order.cancel-before-submission-only
  - sales.cancel-order
  - sales.order-cancelled
  - sales.order-lifecycle
---

# Pre-submission cancellation is distinct from refund and Return

The YAML front matter records the trade-off. Normative behavior remains authoritative only in the referenced contracts.
