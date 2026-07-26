---
id: clr-0009-dependency-unavailability
status: resolved
blocks_candidate: false
affected_refs:
  - customer.verify-order-authority
  - pricing.quote-order-item
  - sales.create-order-draft
  - sales.add-order-item
  - sales.order.must-belong-to-verified-customer
  - sales.order.item-subtotal-is-pricing-authoritative
question: What outcome is required when a pinned cross-context dependency cannot return an authoritative decision?
requested_decisions:
  - Decide whether dependency unavailability is a domain outcome of the calling Command or lies outside the business contract.
  - Define the stable failure code, if any, that an unavailable dependency produces.
  - Confirm that an unavailable dependency leaves Order state and Domain Event occurrences unchanged.
---

# Cross-context dependency cannot answer

Both Interaction contracts define the outcomes of an authoritative decision: Customer reports existence and authorization, Pricing reports quote validity and the Item subtotal. Neither defines what the calling Command observes when the dependency returns no decision at all.

Both Interaction contracts also declare `unspecified_behavior: policy: prohibited_to_assume`. An implementer who reaches this condition is therefore required to stop rather than choose, which means Create Order Draft and Add Order Item currently have a reachable path with no defined outcome.

The question matters because the three interpretations below are observably different at the Sales boundary, so two conforming implementations could disagree about the same situation.

## Known interpretations

1. Unavailability is a domain outcome of the calling Command and needs its own stable failure code, leaving Order state and Domain Event occurrences unchanged like every other declared failure.
2. Unavailability is not a business observation. It belongs to delivery concerns outside this contract set, and the Command produces no domain outcome until the dependency answers.
3. Unavailability maps onto the existing negative decisions, so an unreachable Customer behaves as `CUSTOMER_NOT_FOUND` and an unreachable Pricing behaves as `PRICE_QUOTE_NOT_FOUND`.

Interpretation 3 makes "the dependency did not answer" indistinguishable from "the dependency answered no", which the current failure definitions describe as authoritative reports. Interpretation 2 leaves the Command without a terminal outcome, which no existing Scenario expresses. Interpretation 1 adds a failure code to a Command boundary that `architecture_constraints` requires to stay stable.

## Resolution

Human domain review selected interpretation 1. Unavailability is a domain outcome of the calling Command, because a caller that cannot obtain a decision must be able to distinguish "retry is appropriate" from "the answer is no".

`customer.verify-order-authority` declares `CUSTOMER_AUTHORITY_UNAVAILABLE` and `pricing.quote-order-item` declares `PRICE_QUOTE_UNAVAILABLE`. Create Order Draft and Add Order Item declare the matching Command failures, each leaving state and Domain Event occurrences unchanged. Sales MUST NOT report a missing, unauthorized, expired, or invalid decision when the dependency returned no decision at all.

See [DEC-0005](../decisions/DEC-0005-dependency-unavailability.md).
