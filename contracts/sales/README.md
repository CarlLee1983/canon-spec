# Sales Contract Index

Status: draft  
Revision: 2.0.0

Sales owns the lifecycle and invariants of the Order Aggregate described by [context.yaml](context.yaml). This directory contains specifications only and has no production Sales implementation.

## Normative contracts

- Context: [context.yaml](context.yaml)
- Vocabulary: [vocabulary.yaml](vocabulary.yaml)
- Aggregate: [order.yaml](aggregates/order.yaml)
- State machine: [order-lifecycle.yaml](state-machines/order-lifecycle.yaml)
- Commands:
  - [Create Order Draft](commands/create-order-draft.yaml)
  - [Add Order Item](commands/add-order-item.yaml)
  - [Submit Order](commands/submit-order.yaml)
  - [Cancel Order](commands/cancel-order.yaml)
- Events:
  - [OrderDraftCreated](events/order-draft-created.yaml)
  - [OrderItemAdded](events/order-item-added.yaml)
  - [OrderSubmitted](events/order-submitted.yaml)
  - [OrderCancelled](events/order-cancelled.yaml)
- Cross-context dependencies:
  - [Customer authority verification](../customer/interactions/verify-order-authority.yaml)
  - [Pricing Quote resolution](../pricing/interactions/quote-order-item.yaml)

## Acceptance Scenarios

- Create Order Draft:
  - [Authorized creation succeeds](scenarios/create-order-draft-success.yaml)
  - [Identical replay is idempotent](scenarios/create-order-draft-idempotently.yaml)
  - [Missing Customer is rejected](scenarios/reject-customer-not-found.yaml)
  - [Unauthorized actor is rejected](scenarios/reject-unauthorized-customer.yaml)
  - [Conflicting Command ID is rejected](scenarios/reject-command-id-conflict.yaml)
- Add Order Item:
  - [Fractional quoted Item succeeds](scenarios/add-item-success.yaml)
  - [Zero-priced quoted Item succeeds](scenarios/add-free-item-success.yaml)
  - [Invalid Quantity is rejected](scenarios/reject-invalid-quantity.yaml)
  - [Submitted Order modification is rejected](scenarios/reject-modification-after-submit.yaml)
  - [Cancelled Order modification is rejected](scenarios/reject-modification-after-cancel.yaml)
  - [Expired Price Quote is rejected](scenarios/reject-expired-price-quote.yaml)
  - [Currency mismatch is rejected](scenarios/reject-currency-mismatch.yaml)
  - [Negative Price Quote is rejected](scenarios/reject-negative-price-quote.yaml)
- Submit Order:
  - [Non-empty Draft succeeds](scenarios/submit-order-success.yaml)
  - [Empty Draft is rejected](scenarios/reject-empty-order.yaml)
  - [Cancelled Order resubmission is rejected](scenarios/reject-cancelled-order-resubmission.yaml)
  - [Identical replay is idempotent](scenarios/submit-order-idempotently.yaml)
- Cancel Order:
  - [Draft cancellation succeeds](scenarios/cancel-draft-order.yaml)
  - [Submitted Order cancellation is rejected](scenarios/reject-cancel-after-submit.yaml)

## Boundary summary

- Customer decides whether a Customer exists and an actor may create an Order for that Customer.
- Pricing validates fractional Quantity and Unit of Measure, calculates and rounds the Item subtotal, and returns the complete Price Quote evidence.
- Sales allocates Order and Order Item IDs, preserves quote evidence, sums same-currency Item subtotals, and protects lifecycle and idempotency.
- Cancel Order means pre-submission cancellation only. Refund and Return require future Context contracts.

All eight original Clarification Requests were resolved by human domain decisions for this revision. Human domain review has authorized promotion to `candidate`; the contracts remain candidate until an authorized human domain reviewer marks them accepted.

For a non-normative human-readable view, open the [Traditional Chinese Order business logic guide](../../docs/zh-TW/order-business-logic.html). AI agents and implementations MUST continue to use the YAML contracts and one exact implementation manifest as their source.
