---
id: clr-0002-price-snapshot-authority
status: resolved
blocks_candidate: false
affected_refs:
  - sales.order.item-retains-price-snapshot
  - sales.order.item-subtotal-is-pricing-authoritative
  - sales.add-order-item
  - sales.order-item-added
  - pricing.quote-order-item
question: Who supplies and validates the Price Snapshot used when an Order Item is added?
requested_decisions:
  - Define the Pricing responsibility and the party allowed to provide the snapshot.
  - Define when the snapshot is captured and what validity evidence accompanies it.
  - Define failure outcomes when a Quote cannot be validated.
---

# Price Snapshot authority

Treating caller input, internal Sales data, or Pricing as the authority would create different business behavior.

## Resolution

Human domain review selected Pricing as the authority. `pricing.quote-order-item` validates the Price Quote and returns the complete snapshot Sales retains. `sales.add-order-item` accepts a Price Quote ID rather than a caller-authored price.
