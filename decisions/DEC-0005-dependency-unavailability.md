---
schema_version: "1.0"
kind: decision
id: DEC-0005
version: "1.0.0"
status: draft
title: An unanswerable dependency is a distinct Command outcome
problem: Both Interaction contracts defined what an authoritative decision looks like but not what the calling Command observes when no decision arrives, leaving Create Order Draft and Add Order Item with a reachable path that had no defined outcome.
background: Customer is authoritative for Customer existence and actor authority, and Pricing is authoritative for Quote validity and the Item subtotal. Both Interaction contracts declare unspecified behavior prohibited to assume, so an implementer reaching an unanswered dependency was required to stop rather than choose.
decision: Treat an unanswerable dependency as a domain outcome of the calling Command. customer.verify-order-authority declares CUSTOMER_AUTHORITY_UNAVAILABLE and pricing.quote-order-item declares PRICE_QUOTE_UNAVAILABLE, and the calling Commands declare matching failures that leave state and Domain Event occurrences unchanged.
rejected_options:
  - Treat unavailability as a delivery concern outside the business contract, leaving the Command with no terminal outcome.
  - Map an unanswered dependency onto the existing negative decisions so that an unreachable Customer behaves as CUSTOMER_NOT_FOUND.
  - Let each implementation choose whether to retry, fail, or proceed without the decision.
consequences:
  - A caller can distinguish an absent decision from a negative decision, which is the distinction that determines whether retrying is appropriate.
  - The stable failure surface of Create Order Draft and Add Order Item grows by one code each.
  - Conformance fixtures must be able to simulate a dependency that returns no decision, not only one that returns a negative decision.
  - An implementation that reports a missing or unauthorized Customer when Customer never answered is non-conforming and observably so.
revisit_when:
  - A reviewed Customer or Pricing Contract defines its own availability semantics that Sales should consume instead.
  - Human domain reviewers decide that retry policy belongs in the business contract rather than with the caller.
contract_refs:
  - sales
  - sales.create-order-draft
  - sales.add-order-item
  - sales.order.must-belong-to-verified-customer
  - sales.order.item-subtotal-is-pricing-authoritative
  - customer
  - customer.verify-order-authority
  - pricing
  - pricing.quote-order-item
---

# An unanswerable dependency is a distinct Command outcome

The YAML front matter records the trade-off. Normative behavior remains authoritative only in the referenced contracts. Resolves [CLR-0009](../clarifications/CLR-0009-dependency-unavailability.md).

The decision rests on one observation: "I cannot determine the answer" and "the answer is no" lead a caller to different next actions. Collapsing them makes a transient condition permanent, because a caller told that a Customer does not exist has no reason to try again.

**Falsified if:** an unavailable dependency and a negative decision would lead every caller to the same next action, or the failure codes `CUSTOMER_AUTHORITY_UNAVAILABLE` and `PRICE_QUOTE_UNAVAILABLE` disappear from `contracts/customer/interactions/verify-order-authority.yaml`, `contracts/pricing/interactions/quote-order-item.yaml`, `contracts/sales/commands/create-order-draft.yaml`, or `contracts/sales/commands/add-order-item.yaml`.
