---
id: clr-0012-order-item-removal
status: open
blocks_candidate: false
affected_refs:
  - sales
  - sales.order
  - sales.add-order-item
  - sales.cancel-order
  - sales.order.item-additions-do-not-merge
  - sales.order.submitted-items-immutable
question: Must a Draft Order support removing or modifying an Order Item before submission?
requested_decisions:
  - Decide whether Item removal and Quantity modification belong in the Sales conformance target.
  - If they are excluded, record the exclusion in the Sales Context rather than leaving it implicit.
---

# Removing or changing an Item on a Draft Order

Sales defines four Commands. An Order Draft can gain Items and can be cancelled or submitted as a whole, but no Command removes an Item or changes its Quantity. CLR-0008 established that equivalent additions never merge, so a Customer who adds the wrong Product or the wrong Quantity has no corrective action short of cancelling the entire Order.

The absence looks deliberate for a minimal revision, and the Cancelled Order vocabulary already distinguishes cancellation from deletion. The Sales Context states its exclusions explicitly for Payment, Return, and related behavior, but says nothing about Item removal, so a reader cannot tell whether the omission is a scope decision or an oversight.

This request is marked non-blocking. Every pinned Scenario passes without an answer, and nothing in the current rules becomes ambiguous; the question is whether the conformance target is the intended one.

## Known interpretations

1. Removal and modification are out of scope for this revision, and the Sales Context should record the exclusion alongside its existing ones so the boundary is explicit.
2. Removal belongs in the conformance target and needs its own Command, with the resulting Order total, Item identity, and lifecycle effects defined.
3. Correction is already fully expressed. Cancelling the Order Draft and creating a new one is the intended business behavior, and the vocabulary should say so rather than leaving readers to infer it.
